Summary:	Network UPS Tools
Summary(pl):	Sieciowe narz�dzie do UPS-�w
Name:		nut
Version:	0.45.1
Release:	2
License:	GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Source0:	http://www.exploits.org/nut/release/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}-upsmon.init
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-client.patch
Patch2:		%{name}-lookup_for_libgd_ac_fix.patch
URL:		http://www.exploits.org/nut/
BuildRequires:	autoconf
BuildRequires:	gd-devel >= 2.0.1
BuildRequires:	libpng-devel
Prereq:		rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/ups

%description
These programs are part of a developing project to monitor the
assortment of UPSes that are found out there in the field. Many models
have serial serial ports of some kind that allow some form of state
checking. This capability has been harnessed where possible to allow
for safe shutdowns, live status tracking on web pages, and more.

%package client
Summary:	Multi-vendor UPS Monitoring Project Client Utilities
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System

%description client
This package includes the client utilities that are required to
monitor a ups that the client host is plugged into but monitored via
serial cable by another host on the network....

%package cgi
Summary:	Multi-vendor UPS Monitoring Project Server - CGI utils
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System

%description cgi
These programs are part of a developing project to monitor the
assortment of UPSes that are found out there in the field. Many models
have serial serial ports of some kind that allow some form of state
checking. This capability has been harnessed where possible to allow
for safe shutdowns, live status tracking on web pages, and more.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
autoconf
%configure \
	--with-statepath=/var/lib/ups \
	--with-uid=nobody \
	--with-group=ttyS
%{__make} all cgi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/{sysconfig,rc.d/init.d},/var/lib/ups}

%{__make} install install-cgi \
	DESTDIR=$RPM_BUILD_ROOT \
	CGIPATH=/home/httpd/cgi-bin

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ups
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ups
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/upsmon

gzip -9nf CREDITS README docs/{FAQ,Changes*,*.txt,cables/*}

#%pre
#if [ -n "`id -u ups 2>/dev/null`" ]; then
#	if [ "`id -u ups`" != "68" ]; then
#		echo "Warning: user ups does not have uid=68. Correct this before installing NUT" 1>&2
#		exit 1
#	fi
#else
#       /usr/sbin/useradd -u 68 -r -d /var/lib/ups -s /bin/sh -c "Network UPS Tools User" -g ttyS ups 1>&2
#fi

%post
/sbin/chkconfig --add ups
if [ -f /var/lock/subsys/ups ]; then
	/etc/rc.d/init.d/ups restart >&2
else
	echo "Run \"/etc/rc.d/init.d/ups start\" to start NUT ups daemon."
fi

%post client
/sbin/chkconfig --add upsmon
if [ -f /var/lock/subsys/upsmon ]; then
	/etc/rc.d/init.d/upsmon restart >&2
else
	echo "Run \"/etc/rc.d/init.d/upsmon start\" to start NUT upsmon daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/ups ]; then
		/etc/rc.d/init.d/ups stop >&2
	fi
	/sbin/chkconfig --del ups
fi

#%postun
#if [ "$1" = "0" ]; then
#	userdel ups 2>&1
#fi

%preun client
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/upsmon ]; then
		/etc/rc.d/init.d/upsmon stop >&2
	fi
	/sbin/chkconfig --del upsmon
fi
	
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz docs/{,cables}/*.gz
%attr(755,root,root) %{_bindir}/aeg
%attr(755,root,root) %{_bindir}/apcsmart
%attr(755,root,root) %{_bindir}/belkin
%attr(755,root,root) %{_bindir}/bestfort
%attr(755,root,root) %{_bindir}/bestuferrups
%attr(755,root,root) %{_bindir}/bestups
%attr(755,root,root) %{_bindir}/engetron
%attr(755,root,root) %{_bindir}/everups
%attr(755,root,root) %{_bindir}/fentonups
%attr(755,root,root) %{_bindir}/genericups
%attr(755,root,root) %{_bindir}/ipt-anzen
%attr(755,root,root) %{_bindir}/mge-ellipse
%attr(755,root,root) %{_bindir}/mgeups
%attr(755,root,root) %{_bindir}/multilink
%attr(755,root,root) %{_bindir}/mustekups
%attr(755,root,root) %{_bindir}/newapc
%attr(755,root,root) %{_bindir}/optiups
%attr(755,root,root) %{_bindir}/powercom
%attr(755,root,root) %{_bindir}/sec
%attr(755,root,root) %{_bindir}/sms
%attr(755,root,root) %{_bindir}/toshiba1500
%attr(755,root,root) %{_bindir}/upscmd
%attr(755,root,root) %{_bindir}/upsdrvctl
%attr(755,root,root) %{_bindir}/upseyeux
%attr(755,root,root) %{_bindir}/ups-trust425+625
%attr(755,root,root) %{_sbindir}/upsd
%attr(755,root,root) %{_bindir}/upslog
%config(noreplace) /etc/sysconfig/ups
%attr(754,root,root) /etc/rc.d/init.d/ups
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/upsd.conf
%{_mandir}/man8/*
%dir %attr(750,nobody,root) /var/lib/ups

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/upsc
%attr(755,root,root) %{_bindir}/upsct
%attr(755,root,root) %{_bindir}/upsct2
%attr(755,root,root) %{_sbindir}/upsmon
%attr(755,root,root) %{_sbindir}/upssched
%attr(755,root,root) %{_sbindir}/upssched-cmd
%config(noreplace) %{_sysconfdir}/hosts.conf
%config(noreplace) %{_sysconfdir}/multimon.conf
%attr(754,root,root) /etc/rc.d/init.d/upsmon
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/upsmon.conf

%files cgi
%defattr(644,root,root,755)
%attr(755,root,root) /home/httpd/cgi-bin/*.cgi
#%attr(600,root,root) %config(noreplace) %{_sysconfdir}/upsset.passwd
