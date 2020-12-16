Name:           ecf-puppetdb-tools
Summary:        Scripts for querying the puppetdb
Version:        2.2.4
Release:        0%{?dist}
Group:          Applications/System
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        %{name}-%{version}-%{release}.tar.gz
BuildArch:      noarch

%if 0%{?rhel} == 8
Requires:       python3 python3-dateutil python3-requests
BuildRequires:  python3 python3-setuptools python3-rpm-macros rsync perl-podlators
%else
Requires:       python36 python36-dateutil python36-requests
BuildRequires:  python36 python36-setuptools python3-rpm-macros rsync perl-podlators
%endif

License:        BSD
Distribution:   ECF-SSI
URL:            https://github.com/tskirvin/puppetdb-tools

%description
Scripts and libraries for querying puppetdb

%prep

%setup -c -q -n %{name}-%{version}

%build

%install
if [[ $RPM_BUILD_ROOT != "/" ]]; then
    rm -rf $RPM_BUILD_ROOT
fi

mkdir -p usr/share/man/man1
for i in `ls usr/bin`; do
    pod2man --section 1 --center="System Commands" usr/bin/${i} \
        > usr/share/man/man1/${i}.1 ;
    bzip2 usr/share/man/man1/${i}.1 ;
done

rsync -Crlpt ./usr ${RPM_BUILD_ROOT}
for i in bin sbin; do
    if [ -d ${RPM_BUILD_ROOT}/$i ]; then
        chmod 0755 ${RPM_BUILD_ROOT}
    fi
done

python3 setup.py install --prefix=${RPM_BUILD_ROOT}/usr \
    --single-version-externally-managed --record=installed_files
exit 0

%clean
if [[ $RPM_BUILD_ROOT != "/" ]]; then
    rm -rf $RPM_BUILD_ROOT
fi

%files
%defattr(-,root,root)
/usr/share/man/man1/*
/usr/bin/*
%{python3_sitelib}/puppetdb/*py*
%{python3_sitelib}/*egg-info

%changelog
* Wed Dec 15 2020   Tim Skirvin <tskirvin@fnal.gov>  2.2.4-0
- nodesFailed() - AND -> and (newer puppetdb doesn't like the former)

* Mon Nov 16 2020   Tim Skirvin <tskirvin@fnal.gov>  2.2.3-0
- lint fixes
- lots of calls to Exception fixed

* Tue Feb 25 2020   Tim Skirvin <tskirvin@fnal.gov>  2.2.2-0
- CentOS 8 support
- adding minimum SSL versions
- puppetdb-uuid-by-host - changed beyond recognition (see CHANGELOG)

* Mon Aug 19 2019   Tim Skirvin <tskirvin@fnal.gov>  2.2.1-0
- flake8 python linting for all

* Fri Aug 16 2019   Tim Skirvin <tskirvin@fnal.gov>  2.2.0-0
- converted everything to python 3

* Tue Mar 19 2019   Tim Skirvin <tskirvin@fnal.gov>  2.1.4-0
- moving the changelog to CHANGELOG.md going forwards
- generally re-working for distribution via pypi

* Wed Feb 06 2019   Tim Skirvin <tskirvin@fnal.gov>  2.1.3-0
- puppetdb-resources - returns json as an array, not a list of hashes

* Tue Jan 15 2019   Tim Skirvin <tskirvin@fnal.gov>  2.1.2-1
- trying again to turn off ssl warnings (SL7 only)

* Thu Nov 01 2018   Tim Skirvin <tskirvin@fnal.gov>  2.1.2-0
- puppetdb-node-facts - use 'certname' for searching instead of the fqdn fact

* Wed Oct 03 2018   Tim Skirvin <tskirvin@fnal.gov>  2.1.1-0
- disabling more urllib3 warnings (probably too many)

* Fri Sep 21 2018   Tim Skirvin <tskirvin@fnal.gov>  2.1.0-0
- puppetdb-failed-list - add '--short' and '--text' options
- hostFailedWhy() output format now includes the source of the message
  (which makes it much more useful)

* Thu Sep 20 2018   Tim Skirvin <tskirvin@fnal.gov>  2.0.12-0
- puppetdb-tooquiet - sorts output
- hostFailedWhy() and nodesFailed() now look at reports endpoint instead
  of events endpoint (catches more things that fail differently)

* Thu Jan 18 2018   Tim Skirvin <tskirvin@fnal.gov>  2.0.11-1
- added hostFactHash() to support querying structured facts

* Wed Oct 18 2017   Tim Skirvin <tskirvin@fnal.gov>  2.0.10-1
- puppetdb-tangled - added a '--count' parameter

* Tue Sep 26 2017   Tim Skirvin <tskirvin@fnal.gov>  2.0.9-1
- adding SL7 support

* Fri Aug 18 2017   Tim Skirvin <tskirvin@fnal.gov>  2.0.9-0
- added '--json' to puppetdb-node-facts

* Wed Apr 19 2017   Tim Skirvin <tskirvin@fnal.gov>  2.0.8-0
- hostFact() - added a 'value' option to query for specific values

* Tue Jan 17 2017   Tim Skirvin <tskirvin@fnal.gov>  2.0.7-0
- hostFactWild() - now goes to the right facts URL

* Tue Jan 03 2017   Tim Skirvin <tskirvin@fnal.gov>  2.0.6-0
- puppetdb-report-usage - fixed some bugs where hosts aren't everywhere

* Tue Dec 13 2016   Tim Skirvin <tskirvin@fnal.gov>  2.0.5-0
- puppetdb-report-usage - added chart headers

* Tue Dec 13 2016   Tim Skirvin <tskirvin@fnal.gov>  2.0.4-0
- puppetdb-report-usage - new script

* Tue Sep 13 2016   Tim Skirvin <tskirvin@fnal.gov>  2.0.3-0
- puppetdb-tangled - fixed

* Wed Sep 07 2016   Tim Skirvin <tskirvin@fnal.gov>  2.0.2-0
- fixed eventChangeString() to work with both v3 and v4 APIs
  
* Wed Aug 10 2016   Tim Skirvin <tskirvin@fnal.gov>  2.0.1-0
- puppetdb-tangled - fixed the reporting to work the "old way"

* Mon Aug 08 2016   Tim Skirvin <tskirvin@fnal.gov>  2.0.0-0
- added full support for v3 + v4 APIs
- made puppetdb module, offloaded a lot of every script into it
- lots of miscellaneous fixes

* Wed May 18 2016   Tim Skirvin <tskirvin@fnal.gov>  1.0.9-0
- puppetdb-last-successful-run - new script
- puppetdb-tooquiet - added '--debug'

* Tue Apr 26 2016   Tim Skirvin <tskirvin@fnal.gov>  1.0.8-0
- puppetdb-failed-list - only show active nodes

* Thu Apr 14 2016   Tim Skirvin <tskirvin@fnal.gov>  1.0.7-0
- puppetdb-failed - get role_fact from the config files

* Thu Apr 14 2016   Tim Skirvin <tskirvin@fnal.gov>  1.0.6-2
- puppetdb-resources ssl fix (when will I get time to fix it globally?)

* Wed Mar 23 2016   Tim Skirvin <tskirvin@fnal.gov>  1.0.6-1
- puppetdb-host-csv ssl fix

* Wed Mar 23 2016   Tim Skirvin <tskirvin@fnal.gov>  1.0.6-0
- added puppetdb-node-classes
- puppetdb-node-resources works in the SSL world

* Wed Mar 23 2016   Tim Skirvin <tskirvin@fnal.gov>  1.0.5-2
- setting the no-warnings-from-ssl-with-requests-module thing globally

* Tue Mar 22 2016   Tim Skirvin <tskirvin@fnal.gov>  1.0.5-1
- setting puppetdb.json as a config file

* Tue Mar 22 2016   Tim Skirvin <tskirvin@fnal.gov>  1.0.5-0
- puppetdb-farmlet - looks up hosts by zone/role/subrole

* Thu Feb  4 2016   Tim Skirvin <tskirvin@fnal.gov>  1.0.4-0
- puppetdb-fact - focused fact queries 
- puppetdb-node-facts - lists all facts from all nodes
- puppetdb-wrapper - simple bash wrapper to do curl queries

* Wed Jan 20 2016   Tim Skirvin <tskirvin@fnal.gov>  1.0.3-0
- puppetdb-tooquiet - customizable role fact
- puppetdb-failed - customizable role fact
- added puppetdb-failed-list

* Wed Dec 23 2015   Tim Skirvin <tskirvin@fnal.gov>  1.0.2-0
- puppetdb-tangled - now skips 'noop'

* Thu Dec 03 2015   Tim Skirvin <tskirvin@fnal.gov>  1.0.1-0
- added puppetdb-failed
- removed 'role' bits from puppetdb-failed and puppetdb-tooquiet

* Wed Nov 25 2015   Tim Skirvin <tskirvin@fnal.gov>  1.0.0-0
- initial version (forked from from cms-puppetdb-utils)
