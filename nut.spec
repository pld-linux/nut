Summary:	Network UPS Tools
Summary(pl):	Sieciowe narzêdzie do UPS-ów
Name:		nut
Version:	0.99.2
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://www.exploits.org/nut/testing/0.99/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}-upsmon.init
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-client.patch
URL:		http://www.exploits.org/nut/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gd-devel >= 2.0.1
BuildRequires:	libpng-devel
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	smartupstools

%define		_sysconfdir	/etc/ups

%description
These programs are part of a developing project to monitor the
assortment of UPSes that are found out there in the field. Many models
have serial serial ports of some kind that allow some form of state
checking. This capability has been harnessed where possible to allow
for safe shutdowns, live status tracking on web pages, and more.

%description -l pl
Te programy s± czê¶ci± projektu do monitorowania wielu UPS-ów w jakim¶
otoczeniu. Wiele modeli ma porty szeregowe i pozwala na jak±¶ formê
sprawdzania stanu. Ta funkcjonalno¶æ pozwala na bezpieczne
zatrzymywanie systemów, sprawdzanie stanu zasilania przez WWW i inne.

%package client
Summary:	Multi-vendor UPS Monitoring Project Client Utilities
Summary(pl):	Narzêdzia klienckie do monitorowania UPS-ów
Group:		Applications/System
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig

%description client
This package includes the client utilities that are required to
monitor a UPS that the client host is plugged into but monitored via
serial cable by another host on the network....

%description client -l pl
Ten pakiet zawiera narzêdzia kliencie potrzebne do monitorowania UPS-a
do którego pod³±czony jest komputer kliencki, kiedy kabel szeregowy
UPS-a jest pod³±czony do innego komputera w sieci.

%package cgi
Summary:	Multi-vendor UPS Monitoring Project Server - CGI utils
Summary(pl):	Narzêdzia CGI do monitorowania UPS-ów
Group:		Applications/System

%description cgi
These programs are part of a developing project to monitor the
assortment of UPSes that are found out there in the field. Many models
have serial serial ports of some kind that allow some form of state
checking. This capability has been harnessed where possible to allow
for safe shutdowns, live status tracking on web pages, and more. This
package contains CGI utils.

%description cgi -l pl
Te programy s± czê¶ci± projektu do monitorowania wielu UPS-ów w jakim¶
otoczeniu. Wiele modeli ma porty szeregowe i pozwala na jak±¶ formê
sprawdzania stanu. Ta funkcjonalno¶æ pozwala na bezpieczne
zatrzymywanie systemów, sprawdzanie stanu zasilania przez WWW i inne.
Ten pakiet zawiera narzêdzia CGI.

%package devel
Summary:	Files for NUT clients development
Summary(pl):	Pliki do tworzenia klientów NUT-a
Group:		Development/Libraries
# it does NOT require nut

%description devel
Object file and header for developing NUT clients.

%description devel -l pl
Plik wynikowy oraz nag³ówek s³u¿±ce do tworzenia klientów NUT-a.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
install /usr/share/automake/config.* .
%{__aclocal}
%{__autoconf}
%configure \
	--with-cgi \
	--with-linux-hiddev=%{_includedir}/linux/hiddev.h \
	--with-statepath=%{_var}/lib/ups \
	--with-drvpath=%{_libdir}/nut \
	--with-cgipath=/home/services/httpd/cgi-bin \
	--with-user=nobody \
	--with-group=ttyS
%{__make} all cgi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/{sysconfig,rc.d/init.d},/var/lib/ups} \
	$RPM_BUILD_ROOT{%{_libdir}/nut,%{_includedir}}

%{__make} install install-cgi \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ups
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ups
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/upsmon

rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/*
install -m644 conf/*.users conf/*.conf $RPM_BUILD_ROOT%{_sysconfdir}

install -m644 clients/upsfetch.o $RPM_BUILD_ROOT%{_libdir}
install -m644 clients/upsfetch.h $RPM_BUILD_ROOT%{_includedir}

ln -s %{_libdir}/nut/upsdrvctl $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

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

%preun client
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/upsmon ]; then
		/etc/rc.d/init.d/upsmon stop >&2
	fi
	/sbin/chkconfig --del upsmon
fi

%files
%defattr(644,root,root,755)
%doc NEWS README CHANGES CREDITS docs/*
%attr(755,root,root) %{_bindir}/upscmd
%attr(755,root,root) %{_bindir}/upslog
%attr(755,root,root) %{_sbindir}/upsdrvctl
%attr(755,root,root) %{_sbindir}/upsd
%config(noreplace) /etc/sysconfig/ups
%attr(754,root,root) /etc/rc.d/init.d/ups
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/upsd.conf
%attr(640,root,nobody) %config(noreplace) %{_sysconfdir}/ups.conf
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/upsd.users
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir %attr(750,nobody,root) /var/lib/ups
%dir %attr(755,root,root) %{_libdir}/nut
%attr(755,root,root) %{_libdir}/nut/*

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/upsc
%attr(755,root,root) %{_bindir}/upsct
%attr(755,root,root) %{_bindir}/upsct2
%attr(755,root,root) %{_sbindir}/upsmon
%attr(755,root,root) %{_sbindir}/upssched
%attr(755,root,root) %{_sbindir}/upssched-cmd
%attr(754,root,root) /etc/rc.d/init.d/upsmon
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/upsmon.conf
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/upssched.conf

%files cgi
%defattr(644,root,root,755)
%attr(755,root,root) /home/services/httpd/cgi-bin/*.cgi
%config(noreplace) %{_sysconfdir}/hosts.conf
%config(noreplace) %{_sysconfdir}/multimon.conf
%config(noreplace) %{_sysconfdir}/upsset.conf

%files devel
%defattr(644,root,root,755)
%{_libdir}/upsfetch.o
%{_includedir}/upsfetch.h
