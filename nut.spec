Summary:	Network UPS Tools
Name:		nut
Version:	0.43.0
Release:	2
License:	GPL
Group:		Utilities/System
Group(pl):	Narzêdzia/System
Source:		http://www.exploits.org/nut/release/%{name}-%{version}.tar.gz
URL:		http://www.exploits.org/nut/
Prereq:		chkconfig
Prereq:		fileutils
Requires:	nut-client
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/ups

%description
These programs are part of a developing project to monitor the assortment
of UPSes that are found out there in the field. Many models have serial
serial ports of some kind that allow some form of state checking. This
capability has been harnessed where possible to allow for safe shutdowns,
live status tracking on web pages, and more.

%package client
Summary:	Multi-vendor UPS Monitoring Project Client Utilities
Group:		Utilities/System
Group(pl):	Narzêdzia/System

%description client
This package includes the client utilities that are required to monitor a
ups that the client host is plugged into but monitored via serial cable by
another host on the network....

%package cgi
Summary:	Multi-vendor UPS Monitoring Project Server - CGI utils
Group:		Utilities/System
Group(pl):	Narzêdzia/System

%description cgi
These programs are part of a developing project to monitor the assortment
of UPSes that are found out there in the field. Many models have serial
serial ports of some kind that allow some form of state checking. This
capability has been harnessed where possible to allow for safe shutdowns,
live status tracking on web pages, and more.

%prep
%setup -q

%build
LDFLAGS="-s"; export LDFLAGS
%configure \
	--with-statepath=/var/lib/ups \
	--with-uid=99 \
	--with-gid=99
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/{sysconfig,rc.d/init.d},var/lib/ups}
%{__make} CONFPATH=$RPM_BUILD_ROOT%{_sysconfdir}/ups BASEPATH=$RPM_BUILD_ROOT%{_prefix} STATEPATH=$RPM_BUILD_ROOT/var/lib/ups install
%{__make} CONFPATH=$RPM_BUILD_ROOT%{_sysconfdir}/ups BASEPATH=$RPM_BUILD_ROOT%{_prefix} STATEPATH=$RPM_BUILD_ROOT/var/lib/ups install-cgi

install scripts/RedHat-6.0/ups-config $RPM_BUILD_ROOT/etc/sysconfig/ups
install scripts/RedHat-6.0/ups $RPM_BUILD_ROOT/etc/rc.d/init.d

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
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CREDITS Changes QUICKSTART README docs
%attr(755,root,root) %{_bindir}/apcsmart
%attr(755,root,root) %{_bindir}/bestups
%attr(755,root,root) %{_bindir}/fentonups
%attr(755,root,root) %{_bindir}/genericups
%attr(755,root,root) %{_bindir}/optiups
%attr(755,root,root) %{_bindir}/ups-trust425+625
%attr(755,root,root) %{_bindir}/upsd
%attr(755,root,root) %{_bindir}/upslog

%files client
%defattr(644,root,root,755)
%config(noreplace) %{_sysconfdir}/ups/hosts.conf
%config(noreplace) %{_sysconfdir}/ups/multimon.conf
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/upsd.conf
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/upsmon.conf
%attr(644,root,root) %config(noreplace) /etc/sysconfig/ups
%attr(754,root,root) /etc/rc.d/init.d/ups
%attr(755,root,root) %{_bindir}/upsc
%attr(755,root,root) %{_bindir}/upsct
%attr(755,root,root) %{_bindir}/upsct2
%attr(755,root,root) %{_bindir}/upsmon
%dir %attr(755,nobody,nobody) /var/lib/ups

%files cgi
%defattr(644,root,root,755)
%doc CREDITS Changes QUICKSTART README docs
%{_prefix}/cgi-bin/multimon.cgi
%{_prefix}/cgi-bin/upsimage.cgi
%{_prefix}/cgi-bin/upsset.cgi
%{_prefix}/cgi-bin/upsstats.cgi
