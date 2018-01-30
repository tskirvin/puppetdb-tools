## Config File Format - standardize

It would be nice to use the same config file as Puppet Enterprise's
PuppetDB CLI, e.g.:

    {
      "puppetdb": {
        "server_urls": "https://<PUPPETDB_HOST>:8081",
        "cacert": "/etc/puppetlabs/puppet/ssl/certs/ca.pem",
        "cert": "/etc/puppetlabs/puppet/ssl/certs/<WORKSTATION_HOST>.pem",
        "key": "/etc/puppetlabs/puppet/ssl/private_keys/<WORKSTATION_HOST>.pem"
      }
    }

See https://docs.puppet.com/puppetdb/5.1/pdb_client_tools.html#example-configuration-file-pe-client-tools
