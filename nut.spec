Name:		nut
Version:	0.42.2
Release:	1
License:	GPL
Group:		Utilities/System
Group(pl):	Narzêdzia/System
Source:		http://www.exploits.org/nut/release/%{name}-%{version}.tar.gz
Patch01:	nut-makefile-rpm-%{version}.patch
BuildRoot:	/tmp/%{name}-%{version}-root
Requires:	nut-client
Prereq:		chkconfig fileutils

%define		_sysconfdir=/etc/ups

%description
These programs are part of a developing project to monitor the assortment
of UPSes that are found out there in the field. Many models have serial
serial ports of some kind that allow some form of state checking. This
capability has been harnessed where possible to allow for safe shutdowns,
live status tracking on web pages, and more.

%package client
Group:		Utilities/System
Group(pl):	Narzêdzia/System
Summary:	Multi-vendor UPS Monitoring Project Client Utilities

%description client
This package includes the client utilities that are required to monitor a
ups that the client host is plugged into but monitored via serial cable by
another host on the network....

%package nocgi
Summary:	Multi-vendor UPS Monitoring Project Server w/o CGI utils
Group:		Utilities/System
Group(pl):	Narzêdzia/System

%description nocgi
These programs are part of a developing project to monitor the assortment
of UPSes that are found out there in the field. Many models have serial
serial ports of some kind that allow some form of state checking. This
capability has been harnessed where possible to allow for safe shutdowns,
live status tracking on web pages, and more.

%prep
%setup -q
%patch01 -p0


%build
LDFLAGS="-s"; export LDFLAGS
%configure \
	--with-statepath=/var/state/ups \
	--enable-celsius \
	--with-uid=99 \
	--with-gid=99
make

%install
rm -rf %{buildroot}
make CONFPATH=%{buildroot}%{_sysconfdir}/ups BASEPATH=%{buildroot}%{_prefix} STATEPATH=%{buildroot}/var/state/ups install
make CONFPATH=%{buildroot}%{_sysconfdir}/ups BASEPATH=%{buildroot}%{_prefix} STATEPATH=%{buildroot}/var/state/ups install-cgi
install -d %{buildroot}%{_sysconfdir}/sysconfig
cp scripts/RedHat-6.0/ups-config %{buildroot}%{_sysconfdir}/sysconfig/ups

install -d %{buildroot}/var/state/ups

# install SYSV init stuff
install -d %{buildroot}%{_sysconfdir}/rc.d/init.d
cp scripts/RedHat-6.0/ups %{buildroot}%{_sysconfdir}/rc.d/init.d

%preun client
%{_sysconfdir}/rc.d/init.d/ups stop

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
%{_prefix}/cgi-bin/multimon.cgi
%{_prefix}/cgi-bin/upsimage.cgi
%{_prefix}/cgi-bin/upsset.cgi
%{_prefix}/cgi-bin/upsstats.cgi

%files client
%defattr(644,root,root,755)
%config(noreplace) %{_sysconfdir}/ups/hosts.conf
%config(noreplace) %{_sysconfdir}/ups/multimon.conf
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/ups/upsd.conf
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/ups/upsmon.conf
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/sysconfig/ups
%dir %attr(755,nobody,nobody) /var/state/ups
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/ups
%attr(755,root,root) %{_bindir}/upsc
%attr(755,root,root) %{_bindir}/upsct
%attr(755,root,root) %{_bindir}/upsct2
%attr(755,root,root) %{_bindir}/upsmon

%files nocgi
%defattr(644,root,root,755)
%doc COPYING CREDITS Changes QUICKSTART README docs
%attr(755,root,root) %{_bindir}/apcsmart
%attr(755,root,root) %{_bindir}/bestups
%attr(755,root,root) %{_bindir}/fentonups
%attr(755,root,root) %{_bindir}/genericups
%attr(755,root,root) %{_bindir}/optiups
%attr(755,root,root) %{_bindir}/ups-trust425+625
%attr(755,root,root) %{_bindir}/upsd
%attr(755,root,root) %{_bindir}/upslog
