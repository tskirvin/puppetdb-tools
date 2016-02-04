# cms-puppetdb-utils

This package provides some basic tools to query a puppetdb via a CLI.
Most of the scripts use a centrally-installed json file, but some are
still hard-coded to talk to my local puppetdb.  In both cases, it should
be fairly simple to point at a server of your choice.

These tools were written to be *less* general than any existing tools I've
seen out there.  Specifically, I don't want to write the necessary JSON
input at the command-line every time I'm trying to do a basic query.

These scripts currently only work with the v3 PuppetDB API.  

## What is puppetdb?

http://docs.puppetlabs.com/puppetdb/latest/index.html

## Scripts

This is not an exhaustive list.

### puppetdb-fact

Queries for a given fact, and lists the hosts that have that fact (along
with the value of the fact).  A specific value can be specified as well.

### puppetdb-failed

puppetdb-failed queries the puppetdb to find out which hosts failed on
their last puppet check-in.  

### puppetdb-failed-list

Queries the puppetdb for hosts that had failures in their last run, and
prints out all of the things failed.  This is a useful report to send out
via email to your team.

### puppetdb-node-events

Lists events that have affected a given node over the last 48 hours
(configurable) in much the same format as you would have seen running the
`puppet agent -t` manually.

### puppetdb-node-facts

Lists facts on a node or set of nodes; this should be grep-able enough to
let you find, say, uptime across a large swath of hosts, or similar.

### puppetdb-node-resources

Lists resources deployed on a node or set of nodes.  This is very
powerful, and the CLI is probably not good enough for what you'd actually
want to do with the package.

### puppetdb-tangled

puppetdb-tangled queries the puppetdb to find hosts which are "tangled",
and reports on the associated hosts/events on STDOUT.  A "tangled" host
is defined as one where an event is occurring on that host and over and
over again over the last several runs, which probably indicates that a
change is not successful.  For instance, Package['foo'] removes
Package['bar'] and then Package['bar'] is installed afterwards.

### puppetdb-tooquiet

Lists nodes that have not checked into the server for the last 48 hours
(configurable).  Suitable for sending as an email to your team.

### puppetdb-wrapper

Simple bash script to wrap curl with the values of 'key' and 'cert' that
come out of the central configuration file.  

-------------------------------------------------------------------------------

## Config Files

### /etc/puppetdb/puppetdb.json

This should work for talking to an https port, where auth requires your own puppet cert (which will only work as root):

    {
        "ca": "/etc/puppetlabs/puppet/ssl/certs/ca.pem",
        "cert": "/etc/puppetlabs/puppet/ssl/certs/{fqdn}.fnal.gov.pem",
        "key": "/etc/puppetlabs/puppet/ssl/private_keys/{fqdn}.fnal.gov.pem",
        "server": "https://{puppetdb_fqdn}:8081",
        "nodes_url_base": "/v3/nodes",
        "events_url_base": "/v3/events",
        "facts_url_base": "/v3/facts",
        "reports_url_base": "/v3/reports",
        "resources_url_base": "/v3/resources",
        "event_counts_url_base": "/v3/event-counts"
    }

If you can make queries via http (e.g. without auth):


    {
        "server": "http://{puppetdb_fqdn}:8080",
        "nodes_url_base": "/v3/nodes",
        "events_url_base": "/v3/events",
        "facts_url_base": "/v3/facts",
        "reports_url_base": "/v3/reports",
        "resources_url_base": "/v3/resources",
        "event_counts_url_base": "/v3/event-counts"
    }
