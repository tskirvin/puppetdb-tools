"""
Shared functions for use by puppetdb scripts
"""

#########################################################################
### Configuration #######################################################
#########################################################################

config_file = '/etc/puppetdb/puppetdb.json'
role_fact = 'role'

#########################################################################
### Declarations ########################################################
#########################################################################

import json, optparse, os, re, requests, sys

## this isn't ideal, but until I actually start verifying the cert this
## is the best I can do
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

options = {
    'facts_url_base': "relative URL to puppetdb for facts query",
    'nodes_url_base': "relative URL to puppetdb for default node query",
    'resources_url_base': "relative URL to puppetdb for resources query",
}

#########################################################################
### Subroutines #########################################################
#########################################################################

def generateParser (text, usage_text):
    """
    Generate an OptionParser object for use across all scripts.  We want
    something consistent so we can use the same server/site/user options
    globally.
    """
    parseConfig()

    if 'role_fact' in config:
        role_fact = config['role_fact']

    p = optparse.OptionParser(usage=usage_text, description=text)
    p.add_option('--debug', dest='debug', action='store_true',
        default=False, help='set to print debugging information')
    group = optparse.OptionGroup(p, "connection options")
    group.add_option('--server', dest='server', default=config['server'],
        help='puppetdb server (default: %default)')
    for i in options.keys():
        group.add_option("--%s" % i, dest="%s" % i, default=config[i],
            help=options[i])
    p.add_option_group(group)
    p.add_option('--role_fact', dest='role_fact', default=role_fact,
        help='role fact (default: %default)')
    return p

def hostFact(fact, opt):
    """
    Return a hash of name-to-fact values for a given fact.
    """
    url = "%s%s" % ( opt.server, opt.facts_url_base )

    query = "['=', 'name', '%s']" % fact
    try:
        payload = { 'query': json.dumps(eval(query))}
    except SyntaxError:
        p.error('Malformed query, check examples for help')

    if opt.debug:
        print "url: %s" % url
        print "params: %s" % payload

    headers = {'Accept': 'application/json'}
    try:
        r = request(url, headers=headers, params=payload)
    except Exception, e:
        p.error('%s (bad json?: %s)' % (e, payload))

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
    url = "%s%s" % ( opt.server, opt.facts_url_base )

    query = "['~', 'name', '%s']" % fact
    try:
        payload = { 'query': json.dumps(eval(query))}
    except SyntaxError:
        p.error('Malformed query, check examples for help')

    if opt.debug:
        print "url: %s" % url
        print "params: %s" % payload

    headers = {'Accept': 'application/json'}
    try:
        r = request(url, headers=headers, params=payload)
    except Exception, e:
        p.error('%s (bad json?: %s)' % (e, payload))

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
    except IOError, e:
        print "file error:  %s" % e
        sys.exit (2)
    except Exception, e:
        print "unknown error:  %s" % e
        sys.exit (2)

    return config

def queryNodes(query, opt):
    """
    """
    headers = {'Accept': 'application/json'}
    try:
        payload = { 'query': json.dumps(eval(query))}
    except SyntaxError:
        p.error('Malformed query: %s' % query)

    url = "%s%s" % (opt.server, opt.nodes_url_base)
    if opt.debug: 
        print "url: %s" % url
        print "params: %s" % payload

    try:
        r = request(url, headers=headers, params=payload)
        items = []
        for node in r.json():
            items.append(node)
        return items
    except Exception, e:
        raise "error (bad json?): %s" % e

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
    if re.match('^https:', url):
        r = (config['cert'], config['key'])
    else:
        r = ()

    return r
