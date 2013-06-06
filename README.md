# cms-puppetdb-utils

This package provides some basic tools to query a puppetdb via a CLI.  The
tools are currently hard-coded to talk to my local puppetdb, but should be
fairly trivially customizable to point at a server of your choice.

These tools were written to be *less* general than any existing tools I've
seen out there.  Specifically, I don't want to write the necessary JSON
input at the command-line every time I'm trying to do a basic query; I
just want to 

## What is puppetdb?

[http://docs.puppetlabs.com/puppetdb/latest/index.html]

## Scripts

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

### puppetdb-tooquiet

Lists nodes that have not checked into the server for the last 48 hours
(configurable).  Suitable for sending as an email to your team.