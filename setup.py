from setuptools import setup
import glob, re, os

## get documentation from README.md
with open("README.md", "r") as fh:
    long_description = fh.read()

## get version from spec file
with open('ecf-puppetdb-tools.spec', 'r') as fh:
    for line in fh:
        m = re.search("^Version:\s+(.*)\s*$", line)
        if m:
            version=m.group(1)
            break

## get list of files to install
pyfiles = glob.glob(os.path.join('*', '*.py'))
pyfiles = [pyfile[:-3] for pyfile in pyfiles]

scripts = glob.glob(os.path.join('usr/sbin/*'))
man     = glob.glob(os.path.join('man/man1/*'))

setup (
  author_email = 'tskirvin@fnal.gov',
  author = 'Tim Skirvin',
  data_files = [ ( 'share/man/man1', man ) ],
  description = 'puppetdb tools and shared libraries',
  keywords = ['puppetdb', 'puppet'],
  license = 'Perl Artistic',
  long_description_content_type = 'text/markdown',
  long_description = long_description,
  maintainer_email = 'tskirvin@fnal.gov',
  maintainer  = 'Tim Skirvin',
  name = 'puppetdb-tools',
  package_dir = { 'puppetdb': 'puppetdb' },
  py_modules = pyfiles,
  scripts = scripts,
  url = 'http://github.com/tskirvin/puppetdb-tools',
  version = version,
)
