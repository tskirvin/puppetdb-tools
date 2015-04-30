Name:           cms-puppetdb-utils
Summary:        Scripts for querying the puppetdb
Version:        2.2.0
Release:        0
Packager:       Tim Skirvin <tskirvin@fnal.gov>
Group:          Applications/System
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        %{name}-%{version}-%{release}.tar.gz
BuildArch:      noarch
Requires:       python python-dateutil python-requests

BuildRequires:  rsync
Vendor:         Fermi USCMS-T1
License:        BSD
Distribution:   CMS
URL:            http://www.fnal.gov/

%description
USCMS-T1 @ FNAL - scripts for querying the puppetdb

%prep

%setup -c -n %{name}-%{version}

%build

%install
if [[ $RPM_BUILD_ROOT != "/" ]]; then
    rm -rf $RPM_BUILD_ROOT
fi

mkdir -p usr/share/man/man8
for i in `ls usr/sbin`; do
    pod2man --section 8 --center="System Commands" usr/sbin/${i} \
        > usr/share/man/man8/${i}.8 ;
    bzip2 usr/share/man/man8/${i}.8 ;
done

rsync -Crlpt ./usr ${RPM_BUILD_ROOT}
rsync -Crlpt ./etc ${RPM_BUILD_ROOT}
for i in bin sbin; do
    if [ -d ${RPM_BUILD_ROOT}/$i ]; then
        chmod 0755 ${RPM_BUILD_ROOT}
    fi
done

%clean
if [[ $RPM_BUILD_ROOT != "/" ]]; then
    rm -rf $RPM_BUILD_ROOT
fi

%files
%defattr(-,root,root)
/usr/share/man/man8/*
/usr/sbin/*
/etc/puppetdb/puppetdb.json

%changelog
* Thu Apr 30 2015   Tim Skirvin <tskirvin@fnal.gov>  2.2.0-0
- added puppetdb-uuid-by-host

* Fri Feb 27 2015   Tim Skirvin <tskirvin@fnal.gov>  2.1.0-1
- changed to better versioning scheme
- puppetdb-tangled, puppetdb-tooquiet, and puppetdb-failed have a
  consistent output scheme ('%-25s' for host width, etc)

* Thu Feb  5 2015   Tim Skirvin <tskirvin@fnal.gov>  2-4
- puppetdb-report-uptime - new script that reports on uptimes/kernels

* Mon Oct 20 2014   Tim Skirvin <tskirvin@fnal.gov>  2-3
- puppetdb-manager - lists hosts with associated primaries/secondaries
- puppetdb-failed - now prints system role along with the hostname
- puppetdb-tooquiet - now prints system role along with the hostname 
- puppetdb-tooquiet - now following central json config

* Mon Oct 20 2014   Tim Skirvin <tskirvin@fnal.gov>  2-2
- puppetdb-node-csv - now prints primary/secondary as well

* Thu Mar 06 2014   Tim Skirvin <tskirvin@fnal.gov>  2-1
- puppetdb-node-csv - new script
- puppetdb-failed - only lists puppetdb nodes that are active
- puppetdb-failed, puppetdb-tangled - now returns in sorted order

* Thu Mar 06 2014   Tim Skirvin <tskirvin@fnal.gov>  2-0
- added puppetdb-node-failed and puppetdb-node-tangled
- puppetdb-tooquiet changed its text
- added central configuration file in /etc/puppetdb

* Mon Feb 24 2014   Tim Skirvin <tskirvin@fnal.gov>  1-3
- now pointing at cmspuppetdb1
- puppetdb-node-events now points at v3 API

* Mon Feb 24 2014   Tim Skirvin <tskirvin@fnal.gov>  1-2
- cleanup for local build system and spec file

* Tue Jun 04 2013   Tim Skirvin <tskirvin@fnal.gov>  1-1
- initial version: puppetdb-node-events
- initial version: puppetdb-node-report
- initial version: puppetdb-node-resources

* Tue Jun 04 2013   Tim Skirvin <tskirvin@fnal.gov>  1-0
- initial version: puppetdb-tooquiet
