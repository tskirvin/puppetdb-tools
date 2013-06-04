%define vers 1
%define lname cms-puppetdb-scripts
%define source0 ./%{lname}-%{vers}.tar.gz

Name: cms-puppetdb-scripts
Summary: Scripts for querying the puppetdb
Version: %{vers}
Release: 0
License: BSD
Packager: Tim Skirvin <tskirvin@fnal.gov>
Group: Applications/System
BuildRoot: /var/tmp/%{name}-buildroot
Vendor: Fermi CMS
Source0: %{source0}
BuildArch: noarch
Distribution: CMS
Requires: python python-dateutil python-requests
# BuildRequires: rsync

URL: http://www.fnal.gov/

%description
USCMS-T1 @ FNAL - scripts for querying the puppetdb

%prep
# On the following line, you'll have to add "-a n" for each source file
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

%changelog
* Tue Jun 04 2013   Tim Skirvin <tskirvin@fnal.gov>  1-0
- initial version: puppetdb-tooquiet
