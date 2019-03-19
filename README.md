# puppetdb-tools

This package provides tools to interact with a puppetdb via a CLI.  These
scripts use a (configurable-via-environment-variable) json config to
determine how to talk to the server.

These tools were written to be *less* general than any existing tools I've
seen out there.  Specifically, I don't want to write the necessary JSON
input at the command-line every time I'm trying to do a basic query.

These scripts should support both the v3 and v4 PuppetDB APIs.

## What is puppetdb?

<http://docs.puppetlabs.com/puppetdb/latest/index.html>

## Scripts

This is not an exhaustive list.

### puppetdb-fact

Queries for a given fact, and lists the hosts that have that fact (along
with the value of the fact).  A specific value can be specified as well.
Example: `puppetdb-fact puppetversion`

### puppetdb-failed

puppetdb-failed queries the puppetdb to find out which hosts failed on
their last puppet check-in.

### puppetdb-failed-list

Queries the puppetdb for hosts that had failures in their last run, and
prints out all of the things failed.  This is a useful report to send out
via email to your team.

### puppetdb-farmlet

Queries the puppetdb for host names, based on zone/role/subrole (our local
three-level way of looking up hostnames).

### puppetdb-hosts

List all hosts in the puppetdb.

### puppetdb-last-successful-run

For each host that failed its last puppet run, find out when it last had
a successful puppet run.  This can be useful for determining whether a
machine is really "supported" any more, especially in conjunction with
puppetdb-tooquiet.

### puppetdb-node-classes

List the classes deployed on a given system.  Should match the per-host
classes.txt file.

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

### puppetdb-report-uptime

Lists kernel versions and facts.

### puppetdb-resources

Search for a given resource type across all hosts, e.g.
`puppetdb-resources Class --match Mysql::Server`

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

## Local Scripts

These scripts may not be helpful to others, but are templates for our own
use and show how we interact with facts.  These may be useful to others as
templates.

* puppetdb-host-csv
* puppetdb-manager
* puppetdb-monitor
* puppetdb-report-usage
* puppetdb-uuid-by-host

-------------------------------------------------------------------------------

## Config Files

### /etc/puppetdb/puppetdb.json

This should work for talking to an https port, where auth requires your own puppet cert (which will only work as root):

    {
        "server": "https://{puppetdb_fqdn}:8081",
        "ca": "/etc/puppetlabs/puppet/ssl/certs/ca.pem",
        "cert": "/etc/puppetlabs/puppet/ssl/certs/{fqdn}.fnal.gov.pem",
        "key": "/etc/puppetlabs/puppet/ssl/private_keys/{fqdn}.fnal.gov.pem",
        "api_version": 4
    }

If you can make queries via http (e.g. without auth):


    {
        "server": "http://{puppetdb_fqdn}:8080",
        "api_version": 3
    }

### Environment Variables

You can select alternate configuration files by setting `PUPPETDB_CONFIG`,
e.g.:

    export PUPPETDB_CONFIG=~/rpm/puppetdb-tools/etc/puppetdb/puppetdb3.json
