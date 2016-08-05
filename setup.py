from distutils.core import setup

import os
import glob

pyfiles = glob.glob(os.path.join('*', '*.py'))
pyfiles = [pyfile[:-3] for pyfile in pyfiles]

setup (
  name             = 'puppetdb',
  version          = '2.0.0',
  description      = 'puppetdb-tools shared libraries',
  maintainer       = 'Tim Skirvin',
  maintainer_email = 'tskirvin@fnal.gov',
  package_dir      = { 'puppetdb': 'puppetdb' },
  url              = 'http://github.com/tskirvin/puppetdb-tools',
  py_modules       = pyfiles,
)
