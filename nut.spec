Summary: Multi-vendor UPS Monitoring Project
Name: nut
Version: 0.42.2
Release: 1
Group: Applications/System
Source: http://www.exploits.org/nut/release/%{name}-%{version}.tar.gz
Copyright: GPL
BuildRoot: /var/tmp/%{name}-%{version}-root
Requires: nut-client
Prereq: chkconfig fileutils

# remove chown /var/state so that we don't have to build rpms as root.
Patch01: nut-makefile-rpm-%{version}.patch


%description
These programs are part of a developing project to monitor the assortment 
of UPSes that are found out there in the field. Many models have serial 
serial ports of some kind that allow some form of state checking. This
capability has been harnessed where possible to allow for safe shutdowns, 
live status tracking on web pages, and more.

%package client
Group: Applications/System
Summary: Multi-vendor UPS Monitoring Project Client Utilities

%description client
This package includes the client utilities that are required to monitor a
ups that the client host is plugged into but monitored via serial cable by
another host on the network....

%package nocgi
Group: Applications/System
Summary: Multi-vendor UPS Monitoring Project Server w/o CGI utils

%description nocgi
These programs are part of a developing project to monitor the assortment 
of UPSes that are found out there in the field. Many models have serial 
serial ports of some kind that allow some form of state checking. This
capability has been harnessed where possible to allow for safe shutdowns, 
live status tracking on web pages, and more.
 
%prep
%setup
%patch01 -p0


%build
./configure \
--prefix=/usr \
--sysconfdir=/etc/ups \
--with-statepath=/var/state/ups \
--with-uid=99 \
--with-gid=99
make

%install
rm -rf %{buildroot}
make CONFPATH=%{buildroot}/etc/ups BASEPATH=%{buildroot}/usr STATEPATH=%{buildroot}/var/state/ups install
make CONFPATH=%{buildroot}/etc/ups BASEPATH=%{buildroot}/usr STATEPATH=%{buildroot}/var/state/ups install-cgi
mkdir -p %{buildroot}/etc/sysconfig
cp scripts/RedHat-6.0/ups-config %{buildroot}/etc/sysconfig/ups

mkdir -p %{buildroot}/var/state/ups

# install SYSV init stuff
mkdir -p %{buildroot}/etc/rc.d/init.d
cp scripts/RedHat-6.0/ups %{buildroot}/etc/rc.d/init.d

%preun client
/etc/rc.d/init.d/ups stop

%postun
echo "You may want to chown root:tty /dev/ttyS#, where # is the \n"
echo "number of the serial port that the UPS was connected to... \n"

%postun client
/sbin/chkconfig --del ups

%post client
/sbin/chkconfig --add ups

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING CREDITS Changes QUICKSTART README docs
/usr/bin/apcsmart
/usr/bin/bestups
/usr/bin/fentonups
/usr/bin/genericups
/usr/bin/optiups
/usr/bin/ups-trust425+625
/usr/bin/upsd
/usr/bin/upslog
/usr/cgi-bin/multimon.cgi
/usr/cgi-bin/upsimage.cgi
/usr/cgi-bin/upsset.cgi
/usr/cgi-bin/upsstats.cgi

%files client
%defattr(-,root,root)
%config(noreplace) /etc/ups/hosts.conf
%config(noreplace) /etc/ups/multimon.conf
%config(noreplace) %attr(600,root,root) /etc/ups/upsd.conf
%config(noreplace) %attr(600,root,root) /etc/ups/upsmon.conf
%config(noreplace) %attr(644,root,root) /etc/sysconfig/ups
%dir %attr(755,nobody,nobody) /var/state/ups
%attr(755,root,root) /etc/rc.d/init.d/ups
/usr/bin/upsc
/usr/bin/upsct
/usr/bin/upsct2
/usr/bin/upsmon

%files nocgi
%defattr(-,root,root)
%doc COPYING CREDITS Changes QUICKSTART README docs
/usr/bin/apcsmart
/usr/bin/bestups
/usr/bin/fentonups
/usr/bin/genericups
/usr/bin/optiups
/usr/bin/ups-trust425+625
/usr/bin/upsd
/usr/bin/upslog


%changelog
* Thu Jan 20 2000 <bo-rpm@vircio.com> (0.42.2-1)
- Updated package to new release
- Dropped bestups patch since that is fixed in 0.42.2

* Sat Dec 18 1999 <bo-rpm@vircio.com> (0.42.1-4)
- Package now uses chkconfig

* Sat Dec 18 1999 <bo-rpm@vircio.com> (0.42.1-3)
- applied an improved patch to deal with the 
  bestups string length issue.

* Sat Dec 11 1999 <bo-rpm@vircio.com> (0.42.1-1)
- fixed string length in bestups.c line 279.

* Sat Dec 11 1999 <bo-rpm@vircio.com> (0.42.1-1)
- upgraded package to 0.42.1 from 0.42.0

* Mon Dec 6 1999 <bo-rpm@vircio.com> (0.42.0-8)
- added requirement of nut-client for nut.

* Mon Dec 6 1999 <bo-rpm@vircio.com> (0.42.0-7)
- removed overlapping files between the nut and nut-client rpms

* Mon Nov 23 1999 <bo-rpm@vircio.com> (0.42.0-6)
- stop ups before uninstalling

* Mon Nov 23 1999 <bo-rpm@vircio.com> (0.42.0-5)
- build against gd 1.6.3

* Thu Nov 03 1999 <bo-rpm@vircio.com> (0.42.0-4)
- Initial build of nut (well almost).
- Removed chmod from the make file so that the package
  does not have to be built as root.....
