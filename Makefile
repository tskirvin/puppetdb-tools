## RPM Makefile template
##
## Allows for consistent RPM builds, using mock, with the files copied
## into a central RPM repository.

##
## Usage:
##    make
##    make rpm-nosign
##
##    make lint
##    make linti
##
##    make rpm-sign
##    make copy-to-afs
##

#########################################################################
### Local Configuration #################################################
#########################################################################
## All local configuration should go into 'Makefile.local' in the source
## build directory; this will be included below.  This allows you to
## override directives from the central configuration, and to populate
## additional variables (like, say, FILES_LOCAL, which will be used to 
## decide when to run maketar).


#########################################################################
### Central Configuration - EDIT AT YOUR OWN RISK #######################
#########################################################################
### EDIT AT YOUR OWN RISK

## What shell will we do all of this work in?  Must be at start.
SHELL = /bin/bash

## Build Architecture
ARCH =  `egrep "^BuildArch" *.spec | cut -d' ' -f2`

## What files to track?  Will decide whether we need to re-build the .tar
FILES =  Makefile maketar

## Python causes problems in /usr/local for rpmlint; work around it
FIX_PATH = `echo $(PATH) | sed -e 's/\/usr\/local\/bin//'`

## Root directory under which various repos exist (in AFS)
LOC  = /afs/.slac.stanford.edu/package/RedHat/slac

# Package name
NAME = `pwd | tr '/' '\n' | tail -1`

## Which version of RHEL is this?
RHEL = `cat /etc/redhat-release | cut -d ' ' -f 7 | cut -d'.' -f1`

## A quoted release for use in SRPM
RHL  =  \`cat /etc/redhat-release | cut -d ' ' -f 7 | cut -d'.' -f1\`

## What is the name of our default work directory?
RHDIR = ~/rpm

# The location of the SRPM
SRPM =  ${RHDIR}/SRPMS/$(NAME)-$(VERS)-`egrep ^Release *.spec | cut -d' ' -f2 | perl -pe s/\%\{rel\}/${RHL}/`.src.rpm

## Package version string
VERS =  `egrep "^\%define vers" *.spec | cut -d' ' -f3`

## Package release string without RHEL version included
XREL =  `egrep ^Release *.spec | cut -d' ' -f2 | perl -pe s/\%\{rel\}//`

## The final name of the RPM that's being generated
RPM_BASE = $(NAME)-$(VERS)-$(XREL)
RPM      = $(RPM_BASE).$(ARCH).rpm

## Local local configuration
-include Makefile.local

#########################################################################
### main () #############################################################
#########################################################################

all: rpm

# rpm:        srpm build-EL5 build-EL6 rpm-sign
# rpm-nosign: srpm build-EL5 build-EL6
rpm:        srpm build-5
rpm-nosign: srpm build-5

## has to be clever to deal with backwards compatibility within SRPMs
srpm: tar
	@echo "Creating SRPM..."
	rpmbuild -bs \
		--define "_source_filedigest_algorithm md5" \
		--define "_binary_filedigest_algorithm md5" \
		*.spec
	@echo

tar: $(FILES) $(FILES_LOCAL)
	@echo
	@echo Creating tar file using './maketar'
	@./maketar
	@echo

#########################################################################
### Per-Architecture Builds #############################################
#########################################################################

build-5: tar
	rpmbuild -ba *spec

build-EL5: build-EL5-i386 build-EL5-x86_64 build-EL5-noarch
build-EL6: build-EL6-i386 build-EL6-x86_64 build-EL6-noarch

build-EL5-i386: srpm
	@if [[ $(ARCH) == "i386" || $(ARCH) == "i686" ]]; then \
		echo "mock -v --uniqueext=$(USER) -r rhel-5-i386 --arch i386 \
			--resultdir $(RHDIR)/RPMS/rhel-5-i386 $(SRPM)" ; \
		mock -v --uniqueext=$(USER) -r rhel-5-i386 --arch i386 \
			--resultdir $(RHDIR)/RPMS/rhel-5-i386 $(SRPM) ; \
		mock -r rhel-5-i386 --uniqueext=$(USER) clean ; \
	fi

build-EL5-x86_64: srpm
	@if [[ $(ARCH) == "x86_64" ]]; then \
		echo "mock -v --uniqueext=$(USER) -r rhel-5-x86_64 --arch x86_64 \
			--resultdir $(RHDIR)/RPMS/rhel-5-x86_64 $(SRPM)" ; \
		mock -v --uniqueext=$(USER) -r rhel-5-x86_64 --arch x86_64 \
			--resultdir $(RHDIR)/RPMS/rhel-5-x86_64 $(SRPM) ; \
		mock -r rhel-5-x86_64 --uniqueext=$(USER) clean ; \
	fi

build-EL5-noarch: srpm
	@if [[ $(ARCH) == "noarch" ]]; then \
		echo "mock -v --uniqueext=$(USER) -r rhel-5-i386 --arch i386 \
			--resultdir $(RHDIR)/RPMS/rhel-5-i386 $(SRPM)" ; \
		mock -v --uniqueext=$(USER) -r rhel-5-i386 --arch i386 \
			--resultdir $(RHDIR)/RPMS/rhel-5-i386 $(SRPM) ; \
		mock -r rhel-5-i386 --uniqueext=$(USER) clean ; \
	fi

build-EL6-i386: srpm
	@if [[ $(ARCH) == "i386" || $(ARCH) == "i686" ]]; then \
		echo "mock -v --uniqueext=$(USER) -r rhel-6-i386 --arch i386 \
			--resultdir $(RHDIR)/RPMS/rhel-6-i386 $(SRPM)" ; \
		mock -v --uniqueext=$(USER) -r rhel-6-i386 --arch i386 \
			--resultdir $(RHDIR)/RPMS/rhel-6-i386 $(SRPM) ; \
		mock -r rhel-6-i386 --uniqueext=$(USER) clean ; \
	fi

build-EL6-x86_64: srpm
	@if [[ $(ARCH) == "x86_64" ]]; then \
		echo "mock -v --uniqueext=$(USER) -r rhel-6-x86_64 --arch x86_64 \
			--resultdir $(RHDIR)/RPMS/rhel-6-x86_64 $(SRPM)" ; \
		mock -v --uniqueext=$(USER) -r rhel-6-x86_64 --arch x86_64 \
			--resultdir $(RHDIR)/RPMS/rhel-6-x86_64 $(SRPM) ; \
		mock -r rhel-6-x86_64 --uniqueext=$(USER) clean ; \
	fi

build-EL6-noarch: srpm
	@if [[ $(ARCH) == "noarch" ]]; then \
		echo "mock -v --uniqueext=$(USER) -r rhel-6-i386 --arch i386 \
			--resultdir $(RHDIR)/RPMS/rhel-6-i386 $(SRPM)" ; \
		mock -v --uniqueext=$(USER) -r rhel-6-i386 --arch i386 \
			--resultdir $(RHDIR)/RPMS/rhel-6-i386 $(SRPM) ; \
		mock -r rhel-6-i386 --uniqueext=$(USER) clean ; \
	fi

#########################################################################
### Per-Architecture AFS Copying ########################################
#########################################################################

copy-to-afs: confirm copy-EL5 copy-EL6
	@echo "Run 'make afs-release' to release the volume"

copy-EL5: copy-EL5-i386 copy-EL5-x86_64 copy-EL5-noarch
copy-EL6: copy-EL6-i386 copy-EL6-x86_64 copy-EL6-noarch

copy-EL5-i386: confirm-EL5-i386
	@echo "Copy to EL5"
	@if [[ $(ARCH) == 'i386' ]]; then \
		echo "cp -i $(RHDIR)/RPMS/rhel-5-i386/$(RPM_BASE).*86*rpm $(LOC)/EL5-i386" ; \
		echo "Press enter to continue..."; \
		read ; \
		cp -i $(RHDIR)/RPMS/rhel-5-i386/$(RPM_BASE).*86*rpm $(LOC)/EL5-i386 ; \
	fi

copy-EL5-x86_64: confirm-EL5-x86_64
	@if [[ $(ARCH) == 'x86_64' ]]; then \
		echo "cp -i $(RHDIR)/RPMS/rhel-5-x86_64/$(RPM_BASE).*86*rpm $(LOC)/EL5-x86_64" ; \
		echo "Press enter to continue..."; \
		read ; \
		cp -i $(RHDIR)/RPMS/rhel-5-x86_64/$(RPM_BASE).*86*rpm $(LOC)/EL5-x86_64 ; \
	fi

copy-EL5-noarch: confirm-EL5-noarch
	@if [[ $(ARCH) == 'noarch' ]]; then \
		echo "cp -i $(RHDIR)/RPMS/rhel-5-i386/$(RPM_BASE).noarch.rpm $(LOC)/EL5-i386" ; \
		echo "Press enter to continue..."; \
		read ; \
		cp -i $(RHDIR)/RPMS/rhel-5-i386/$(RPM_BASE).noarch.rpm $(LOC)/EL5-noarch; \
	fi

copy-EL6-i386: confirm-EL6-i386
	@echo "Copy to EL6"
	@if [[ $(ARCH) == 'i386' ]]; then \
		echo "cp -i $(RHDIR)/RPMS/rhel-6-i386/$(RPM_BASE).*86*rpm $(LOC)/EL6-i386" ; \
		echo "Press enter to continue..."; \
		read ; \
		cp -i $(RHDIR)/RPMS/rhel-6-i386/$(RPM_BASE).*86*rpm $(LOC)/EL6-i386 ; \
	fi

copy-EL6-x86_64: confirm-EL6-x86_64
	@if [[ $(ARCH) == 'x86_64' ]]; then \
		echo "cp -i $(RHDIR)/RPMS/rhel-6-x86_64/$(RPM_BASE).*86*rpm $(LOC)/EL6-x86_64" ; \
		echo "Press enter to continue..."; \
		read ; \
		cp -i $(RHDIR)/RPMS/rhel-6-x86_64/$(RPM_BASE).*86*rpm $(LOC)/EL6-x86_64 ; \
	fi

copy-EL6-noarch: confirm-EL6-noarch
	@if [[ $(ARCH) == 'noarch' ]]; then \
		echo "cp -i $(RHDIR)/RPMS/rhel-6-i386/$(RPM_BASE).noarch.rpm $(LOC)/EL6-i386" ; \
		echo "Press enter to continue..."; \
		read ; \
		cp -i $(RHDIR)/RPMS/rhel-6-i386/$(RPM_BASE).noarch.rpm $(LOC)/EL6-noarch; \
	fi

## release the volume
make afs-release:
	remctl -p 46157 nis1 vos release /afs/slac/package/RedHat

#########################################################################
### Per-Architecture RPM Confirmation ###################################
#########################################################################

confirm: confirm-EL5 confirm-EL6

confirm-EL5: confirm-EL5-i386 confirm-EL5-x86_64 confirm-EL5-noarch
confirm-EL6: confirm-EL6-i386 confirm-EL6-x86_64 confirm-EL6-noarch

confirm-EL5-i386:
	@if [[ $(ARCH) == 'i386' ]]; then \
		echo "rpm -qpi $(RHDIR)/RPMS/rhel-5-i386/$(RPM_BASE).*86*rpm" ; \
		rpm -qpi $(RHDIR)/RPMS/rhel-5-i386/$(RPM_BASE).*86*rpm | grep Signature \
			| grep 1f94f2f5d8f9ae5a ; \
	fi

confirm-EL5-x86_64:
	@if [[ $(ARCH) == 'x86_64' ]]; then \
		echo "rpm -qpi $(RHDIR)/RPMS/rhel-5-x86_64/$(RPM_BASE).*86*rpm" ; \
		rpm -qpi $(RHDIR)/RPMS/rhel-5-x86_64/$(RPM_BASE).*86*rpm | grep Signature \
			| grep 1f94f2f5d8f9ae5a ; \
	fi

confirm-EL5-noarch:
	@if [[ $(ARCH) == 'noarch' ]]; then \
		echo "rpm -qpi $(RHDIR)/RPMS/rhel-5-i386/$(RPM_BASE).noarch.rpm" ; \
		rpm -qpi $(RHDIR)/RPMS/rhel-5-i386/$(RPM_BASE).noarch.rpm | grep Signature \
			| grep 1f94f2f5d8f9ae5a ; \
	fi

confirm-EL6-i386:
	@if [[ $(ARCH) == 'i386' ]]; then \
		echo "rpm -qpi $(RHDIR)/RPMS/rhel-6-i386/$(RPM_BASE).*86*rpm" ; \
		rpm -qpi $(RHDIR)/RPMS/rhel-6-i386/$(RPM_BASE).*86*rpm | grep Signature \
			| grep 1f94f2f5d8f9ae5a ; \
	fi

confirm-EL6-x86_64:
	@if [[ $(ARCH) == 'x86_64' ]]; then \
		echo "rpm -qpi $(RHDIR)/RPMS/rhel-6-x86_64/$(RPM_BASE).*86*rpm" ; \
		rpm -qpi $(RHDIR)/RPMS/rhel-6-x86_64/$(RPM_BASE).*86*rpm | grep Signature \
			| grep 1f94f2f5d8f9ae5a ; \
	fi

confirm-EL6-noarch:
	@if [[ $(ARCH) == 'noarch' ]]; then \
		echo "rpm -qpi $(RHDIR)/RPMS/rhel-6-i386/$(RPM_BASE).noarch.rpm" ; \
		rpm -qpi $(RHDIR)/RPMS/rhel-6-i386/$(RPM_BASE).noarch.rpm | grep Signature \
			| grep 1f94f2f5d8f9ae5a ; \
	fi

#########################################################################
### Per-Architecture RPM Signing ########################################
#########################################################################

rpm-sign: sign-EL5 sign-EL6

sign-EL5: sign-EL5-i386 sign-EL5-x86_64 sign-EL5-noarch
sign-EL6: sign-EL6-i386 sign-EL6-x86_64 sign-EL6-noarch

sign-EL5-i386:
	@if [[ $(ARCH) == 'i386' ]]; then \
		echo "rpm --resign $(RHDIR)/RPMS/rhel-5-i386/$(RPM_BASE).*86*rpm" ; \
		rpm --resign $(RHDIR)/RPMS/rhel-5-i386/$(RPM_BASE).*86*rpm \
			2>&1 | grep -v "input reopened" ; \
	fi

sign-EL5-x86_64:
	@if [[ $(ARCH) == 'x86_64' ]]; then \
		echo "rpm --resign $(RHDIR)/RPMS/rhel-5-x86_64/$(RPM_BASE).*86*rpm" ; \
		rpm --resign $(RHDIR)/RPMS/rhel-5-x86_64/$(RPM_BASE).*86*rpm \
			2>&1 | grep -v "input reopened" ; \
	fi

sign-EL5-noarch:
	@if [[ $(ARCH) == 'noarch' ]]; then \
		echo "rpm --resign $(RHDIR)/RPMS/rhel-5-i386/$(RPM_BASE).noarch.rpm" ; \
		rpm --resign $(RHDIR)/RPMS/rhel-5-i386/$(RPM_BASE).noarch.rpm \
			2>&1 | grep -v "input reopened" ; \
	fi

sign-EL6-i386:
	@if [[ $(ARCH) == 'i386' ]]; then \
		echo "rpm --resign $(RHDIR)/RPMS/rhel-6-i386/$(RPM_BASE).*86*rpm" ; \
		rpm --resign $(RHDIR)/RPMS/rhel-6-i386/$(RPM_BASE).*86*rpm \
			2>&1 | grep -v "input reopened" ; \
	fi

sign-EL6-x86_64:
	@if [[ $(ARCH) == 'x86_64' ]]; then \
		echo "rpm --resign $(RHDIR)/RPMS/rhel-6-x86_64/$(RPM_BASE).*86*rpm" ; \
		rpm --resign $(RHDIR)/RPMS/rhel-6-x86_64/$(RPM_BASE).*86*rpm \
			2>&1 | grep -v "input reopened" ; \
	fi

sign-EL6-noarch:
	@if [[ $(ARCH) == 'noarch' ]]; then \
		echo "rpm --resign $(RHDIR)/RPMS/rhel-6-i386/$(RPM_BASE).noarch.rpm" ; \
		rpm --resign $(RHDIR)/RPMS/rhel-6-i386/$(RPM_BASE).noarch.rpm \
			2>&1 | grep -v "input reopened" ; \
	fi

#########################################################################
### rpmlint #############################################################
#########################################################################

lint:
	@echo "rpmlint $(RHDIR)/RPMS/$(RPM)"
	@find $(RHDIR)/RPMS/ -name "$(NAME)-$(VERS)-$(XREL).*.rpm" \
		| grep -v 'src.rpm' | PATH=$(FIX_PATH) xargs rpmlint

# Add warnings to the lint output
linti:
	@echo "rpmlint -i $(RHDIR)/rhel-*-*/$(RPM)"
	@find $(RHDIR)/RPMS/ -name "$(NAME)-$(VERS)-$(XREL).*.rpm" \
		| grep -v 'src.rpm' | PATH=$(FIX_PATH) xargs rpmlint -i
