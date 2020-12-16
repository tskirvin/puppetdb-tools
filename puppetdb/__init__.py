"""
Shared functions for use by puppetdb scripts.
"""

#########################################################################
### Configuration #######################################################
#########################################################################

config_file = '/etc/puppetdb/puppetdb.json'
role_fact = 'role'

#########################################################################
### Declarations ########################################################
#########################################################################

import dateutil.parser, dateutil.tz
import json, optparse, os, re, requests, sys

## this isn't ideal, but until I actually start verifying the cert this
## is the best I can do
try:
    import urllib3
    urllib3.disable_warnings()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except Exception as e:
    print(e)
    pass

## necessary on CentOS 8 to use more recent SSL settings
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'HIGH:!DH:!aNULL'

## sub-urls that we support
api = {
    3: {
        'event_counts': '/v3/event-counts',
        'events':       '/v3/events',
        'facts':        '/v3/facts',
        'nodes':        '/v3/nodes',
        'reports':      '/v3/reports',
        'resources':    '/v3/resources',
    },
    4: {
        'event_counts':  '/pdb/query/v4/event-counts',
        'events':        '/pdb/query/v4/events',
        'facts':         '/pdb/query/v4/facts',
        'fact-contents': '/pdb/query/v4/fact-contents',
        'nodes':         '/pdb/query/v4/nodes',
        'reports':       '/pdb/query/v4/reports',
        'resources':     '/pdb/query/v4/resources',
    }
}

#########################################################################
### Subroutines #########################################################
#########################################################################

def eventChangeString(event, **kwargs):
    """
    Creates and returns a single-line formatted string describing a single
    event, based on the output of the puppetdb 'events' endpoint.  This
    string is generally of the format:

        Service[ipmi]: stopped -> running (success)

    Events with the status 'skipped' or 'noop' are skipped unless the
    'no_skip' flag is passwd via kwargs.
    """

    opt = kwargs['opt']

    if (opt.api_version < 4):
        new = event['new-value']
        old = event['old-value']
        title = event['resource-title']
        type = event['resource-type']
    else:
        new = event['new_value']
        old = event['old_value']
        title = event['resource_title']
        type = event['resource_type']

    status = event['status']
    message = event['message']

    if 'no_skip' in kwargs: skip = kwargs['no_skip']
    else:                   skip = True

    if skip and status == 'skipped':
        return None

    if skip and status == 'noop':
        return None

    string = "%s[%s]: %s -> %s (%s)" % (type, title, old, new, message)

    if status != 'failure':
        return None

    return string

def eventSuccessByReport(report_id, opt):
    """
    Queries the puppetdb to pull down an event_counts response.  Returns
    True if there were no failures, noops, or skips, and False otherwise.
    """

    try:
        event_query = ['=', "report", report_id.encode('ascii')]
        query = "%s" % event_query
        payload = {
            'query': json.dumps(eval(query)),
            'summarize_by': 'certname',
            'count_by':     'certname',
        }
        if (opt.api_version < 4):
            payload['summarize-by'] = payload.pop('summarize_by')
            payload['count-by'] = payload.pop('count_by')

    except SyntaxError:
        raise Exception('Malformed query, check examples for help')

    headers = {'Accept': 'application/json'}
    try:
        url = generateUrl('event_counts', opt)
        if opt.debug: print("url: %s" % url)
        if opt.debug: print("query: %s" % query)
        r = request(url, headers=headers, params=payload)
        for event in r.json():
            if event['failures'] > 0: return False
            if event['noops'] > 0: return False
            if event['skips'] > 0: return False
        return True

    except Exception as e:
        raise(e)
    except:
        raise Exception('bad json?: %s')

def generateParser(text, usage_text):
    """
    Generate an OptionParser object for use across all scripts.  We want
    something consistent so we can use the same server/site/user options
    globally.
    """
    parseConfig()

    if 'role_fact' in config: role = config['role_fact']
    else:                     role = role_fact

    p = optparse.OptionParser(usage=usage_text, description=text)
    p.add_option('--debug', dest='debug', action='store_true',
        default=False, help='set to print debugging information')
    group = optparse.OptionGroup(p, "connection options")
    group.add_option('--server', dest='server', default=config['server'],
        help='puppetdb server (default: %default)')
    group.add_option('--api_version', dest='api_version', type='int',
        default=config['api_version'],
        help='puppetdb API version (default: %default)')
    p.add_option_group(group)
    p.add_option('--role_fact', dest='role_fact', default=role,
        help='role fact (default: %default)')
    return p

def generateUrl(action, optHash, *argArray):
    """
    Create a puppetdb URL based on optHash (which came from
    generateParser() and parse_args()) and an argument array.
    """

    try:
        url = "%s%s" % (optHash.server, api[optHash.api_version][action])
    except Exception as e:
        raise Exception("%s (bad api version?)", e)

    if len(argArray) > 0:
        url = "%s/%s" % (url, '/'.join(argArray))

    return url

def hostFact(fact, opt, value=None):
    """
    Return a hash of name-to-fact values for a given fact.
    """
    if value:   url = generateUrl('facts', opt, fact, value)
    else:       url = generateUrl('facts', opt, fact)

    payload = {}

    if opt.debug:
        print("url: %s" % url)
        print("params: %s" % payload)

    headers = {'Accept': 'application/json'}
    try:
        r = request(url, headers=headers)
    except Exception as e:
        raise(e)

    if len(r.json()) == 0:
        return {}

    hash = {}
    for node in r.json():
        name = node['certname']
        hash[name] = node['value']

    return hash

def hostFactHash(factArray, opt, value=None):
    """
    Use the fact-contents endpoint to look up facts.  We take a factArray
    instead of a simple fact; otherwise this works like hostFact().
    """
    url = generateUrl('fact-contents', opt)

    try:
        q1_array = []
        for f in factArray:
            q1_array.append('"%s"' % f.encode('ascii'))
        q1 = ['=', "path", factArray]
        if value:
            q2 = ['=', 'value', value]
            query = ['and', q1, q2]
        else:
            query = q1
        query = "%s" % query
        payload = {
            'query': json.dumps(eval(query)),
        }
    except Exception as e:
        raise Exception('Malformed query, check examples for help')

    if opt.debug:
        print("url: %s" % url)
        print("params: %s" % payload)

    headers = {'Accept': 'application/json'}
    try:
        r = request(url, headers=headers, params=payload)
    except Exception as e:
        raise Exception('%s (bad json?: %s)' % (e, payload))

    if len(r.json()) == 0:
        return {}

    hash = {}
    for node in r.json():
        name = node['certname']
        hash[name] = node['value']

    return hash

def hostFactWild(fact, opt):
    """
    Return a hash of name-to-fact values for a given fact wildcard.
    """
    url = generateUrl('facts', opt)

    query = "['~', 'name', '%s']" % fact
    try:
        payload = {'query': json.dumps(eval(query))}
    except SyntaxError:
        raise Exception('Malformed query, check examples for help')

    if opt.debug:
        print("url: %s" % url)
        print("params: %s" % payload)

    headers = {'Accept': 'application/json'}
    try:
        r = request(url, headers=headers, params=payload)
    except Exception as e:
        raise(e)

    if len(r.json()) == 0:
        return {}

    hash = {}
    for node in r.json():
        name = node['certname']
        fact = node['name']
        value = node['value']
        if fact in hash:
            hash[name][fact] = value
        else:
            hash[name] = {}
            hash[name][fact] = value

    return hash

def hostFailedWhy(hostname, opt):
    """
    Look at the latest system report for a given host, and determine why
    the run failed.  Returns a text string (as an array) suitable for
    printing (from eventChangeString()).
    """
    url = generateUrl('reports', opt)

    host_query = "['=', 'certname', '%s']" % hostname
    time_query = "['=', 'latest_report?', 'true']"
    query = "['and', %s, %s]" % (host_query, time_query)
    try:
        payload = {'query': json.dumps(eval(query))}
    except SyntaxError:
        raise Exception('Malformed query, check examples for help')

    headers = {'Accept': 'application/json'}
    if opt.debug:
        print("url: %s" % url)
        print("payload: %s" % payload)

    r = request(url, params=payload, headers=headers)
    for event in r.json():
        return reportChangeString(event, opt=opt)

    return ""

def hostFailedWhyEvents(hostname, opt):
    """
    Look at the latest system report for a given host, and determine why
    the run failed.  Returns a text string (as an array) suitable for
    printing (from eventChangeString()).
    """
    url = generateUrl('events', opt)

    host_query = "['=', 'certname', '%s']" % hostname
    time_query = "['=', 'latest_report?', 'true']"
    query = "['and', %s, %s]" % (host_query, time_query)
    try:
        payload = { 'query': json.dumps(eval(query))}
    except SyntaxError:
        p.error('Malformed query, check examples for help')

    headers = {'Accept': 'application/json'}
    if opt.debug:
        print("url: %s" % url)
        print("payload: %s" % payload)

    r = request(url, params=payload, headers=headers)
    text = []
    for event in r.json():
        string = eventChangeString(event, opt=opt)
        if string is not None:
            text.append(string)

    return text

def hostRoles(opt):
    """
    Return a dict matching hostnames and system roles (as selected via
    role_fact).
    """
    return hostFact(opt.role_fact, opt)

def nodesFailed(host_search, opt):
    """
    Return a list of hosts that failed.
    """

    url = generateUrl('reports', opt)
    try:
        latest_query = "['=', 'latest_report?', True]"
        failed_query = "['=', 'status', 'failed']"
        host_query = ['~', 'certname', '^%s$' % host_search]
        query = "['and', %s, %s, %s]" \
            % (host_query, latest_query, failed_query)
        payload = {'query': json.dumps(eval(query))}

    except SyntaxError:
        raise('Malformed query, check examples for help')

    headers = {'Accept': 'application/json'}
    try:
        if opt.debug:
            print("url: %s" % url)
            print("payload: %s" % payload)
        r = request(url, headers=headers, params=payload)
        items = []
        for node in r.json():
            if 'certname' in node:
                items.append(node['certname'])
        return items

    except Exception as e:
        raise(e)
    except:
        raise Exception('bad json?: %s')

def nodesFailedEvents(host_search, opt):
    """
    Return a list of hosts that failed by looking at event counts.
    """

    url = generateUrl('event_counts', opt)
    try:
        host_query = ['~', 'certname', '^%s$' % host_search]
        time_query = "['=', 'latest_report?', 'true']"
        query = "['and', %s, %s]" \
            % (host_query, time_query)

        payload = {
            'query':         json.dumps(eval(query)),
            'summarize_by':  'certname',
            'count_by':      'certname',
            'counts_filter': json.dumps(['>', 'failures', 0])
        }
        # support old version of the API
        if (opt.api_version < 4):
            payload['summarize-by'] = payload.pop('summarize_by')
            payload['count-by'] = payload.pop('count_by')
            payload['counts-filter'] = payload.pop('counts_filter')
    except SyntaxError:
        raise('Malformed query, check examples for help')

    headers = {'Accept': 'application/json'}
    try:
        if opt.debug:
            print("url: %s" % url)
            print("payload: %s" % payload)
        r = request(url, headers=headers, params=payload)
        items = []
        for node in r.json():
            if 'subject' in node:
                items.append(node['subject']['title'])
        return items

    except Exception as e:
        raise(e)
    except:
        raise Exception('bad json?: %s')

def nodesList(host_search, opt):
    """
    Returns an array listing all active nodes on the puppetdb.
    """

    url = generateUrl('nodes', opt)
    items = []

    try:
        query = "['~', ['fact', 'fqdn'], '^%s$']" % host_search
        payload = {'query': json.dumps(eval(query))}
        headers = {'Accept': 'application/json'}
        r = request(url, headers=headers, params=payload)
        for node in r.json():
            if 'certname' in node: name = node['certname']
            else:                  name = node['name']
            items.append(name)

    except Exception as e:
        raise(e)

    return items

def parseConfig():
    """
    Load a json configuration from a configuration file, which comes from
    either the local config_file or ENV['PUPPETDB_CONFIG'].  Sets a global
    'config' variable.
    """
    global config

    file = os.getenv('PUPPETDB_CONFIG', config_file)

    try:
        config = json.load(open(file, 'r'))
    except IOError as e:
        print("file error:  %s" % e)
        sys.exit(2)
    except Exception as e:
        print("unknown error:  %s" % e)
        sys.exit(2)

    return config

def queryNodes(query, opt):
    """
    """
    headers = {'Accept': 'application/json'}
    try:
        payload = {'query': json.dumps(eval(query))}
    except SyntaxError:
        raise Exception('Malformed query: %s' % query)

    url = generateUrl('nodes', opt)
    if opt.debug:
        print("url: %s" % url)
        print("params: %s" % payload)

    try:
        r = request(url, headers=headers, params=payload)
        items = []
        for node in r.json():
            items.append(node)
        return items
    except Exception as e:
        raise(e)

def reportChangeString(report, **kwargs):
    """
    Creates and returns an array of strings showing a change from the
    report endpoint.  This is the text that puppet itself generated.  It
    only shows 'errs' at this point.
    """

    opt = kwargs['opt']

    levels = ['err']
    if 'levels' in kwargs:
        levels = kwargs['levels']

    text_match = '.*'
    try: text_match = opt.text
    except Exception as e: text_match = '.*'

    try:
        data = report['logs']['data']
    except Exception as e:
        raise Exception('tried to load data from report: %s' % e)

    r = []
    for entry in data:
        msg = entry['message']
        source = entry['source']
        level = entry['level']
        if level in levels:
            if re.search(text_match, msg):
                r.append("%s - %s" % (source, msg))

    return r

def reportsPerHost(host, opt):
    """
    Return a hash of puppet reports on a per-host basis.  The keys are the
    timestamp of the report, the values are the reports themselves (a
    hash, pulled from the json).  See:

        https://docs.puppet.com/puppetdb/2.3/api/query/v3/reports.html

    """
    url = generateUrl('reports', opt)
    try:
        host_query = ['=', 'certname', host.encode('ascii')]
        query = "%s" % host_query
        payload = {'query': json.dumps(eval(query))}
    except SyntaxError:
        raise Exception('Malformed query, check examples for help')

    headers = {'Accept': 'application/json'}
    if opt.debug: print("url: %s" % url)
    if opt.debug: print("query: %s" % query)

    try:
        r = request(url, headers=headers, params=payload)
        items = {}
        for event in r.json():
            ts = event['receive-time']
            items[ts] = event
        return items

    except Exception as e: raise(e)
    except: raise Exception('bad json?: %s')


def request(url, **kwargs):
    """
    Wrapper around requests.  Returns the requests object.
    """
    return requests.get(url, cert=requestCert(url), verify=False, **kwargs)

def requestCert(url):
    """
    If the URL is https, then we will need to pass config['cert'] and
    config['key'].
    """
    if re.match('^https:', url):    r = (config['cert'], config['key'])
    else:                           r = ()

    return r

def timeFromTimestamp(timestamp):
    """
    Parse a timestamp with dateutil.parser.parse(), and set to the local
    timezone.  This is still usable for date math.
    """
    if timestamp is None:
        return False

    ts = dateutil.parser.parse(timestamp)
    local = ts.astimezone(dateutil.tz.tzlocal())
    return local
