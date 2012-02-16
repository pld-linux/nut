# TODO:
#	- upsdrvctl (used by ups.init) doesn't recognize status and reload commands
#
# Conditional build:
%bcond_without	usb			# build without usb drivers
%bcond_with	hal			# build with hal support (DEPRECATED)
%bcond_without	snmp			# build without snmp driver
%bcond_without	cgi			# build without cgi support
%bcond_without	neon			# build with neon based XML/HTTP driver
#
Summary:	Network UPS Tools
Summary(pl.UTF-8):	Sieciowe narzędzie do UPS-ów
Name:		nut
Version:	2.6.3
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://www.networkupstools.org/source/2.6/%{name}-%{version}.tar.gz
# Source0-md5:	8db00c21f8bc03add6e14d15f634ec6a
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}-upsmon.init
Source4:	%{name}.sysconfig.upsmon
Patch0:		%{name}-client.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-smartdp-load.patch
Patch3:		%{name}-upssched-cmd-sysconf.patch
Patch4:		%{name}-matrix.patch
Patch5:		%{name}-more_models.patch
URL:		http://www.networkupstools.org/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_hal:BuildRequires:	dbus-glib-devel}
%{?with_cgi:BuildRequires:	gd-devel >= 2.0.15}
%{?with_hal:BuildRequires:	hal-devel >= 0.5.8}
BuildRequires:	libtool
%{?with_usb:BuildRequires:	libusb-compat-devel}
BuildRequires:	libwrap-devel
%{?with_neon:BuildRequires:	neon-devel}
%{?with_snmp:BuildRequires:	net-snmp-devel}
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{version}-%{release}
Requires:	rc-scripts
Obsoletes:	smartupstools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/ups
%define		_udevrulesdir	/etc/udev/rules.d

%description
These programs are part of a developing project to monitor the
assortment of UPSes that are found out there in the field. Many models
have serial serial ports of some kind that allow some form of state
checking. This capability has been harnessed where possible to allow
for safe shutdowns, live status tracking on web pages, and more.

%description -l pl.UTF-8
Te programy są częścią projektu do monitorowania wielu UPS-ów w jakimś
otoczeniu. Wiele modeli ma porty szeregowe i pozwala na jakąś formę
sprawdzania stanu. Ta funkcjonalność pozwala na bezpieczne
zatrzymywanie systemów, sprawdzanie stanu zasilania przez WWW i inne.

%description -l ru.UTF-8
Эти программы - часть проекта по мониторингу различных UPS. У многих
моделей есть сериальные порты, позволяющие проверять состояние этих
UPS. Эта возможность была использована, где это возможно, для
выполнения безопасных остановов компьютеров, отслеживания статуса
через веб и т.п.

%description -l uk.UTF-8
Ці програми є частиною проекту по моніторингу різноманітних UPS.
Багато моделей мають серіальні порти, що дозволять перевіряти стан цих
UPS. Ця можливість була використана, де це можливо, для виконання
безпечних зупинок комп'ютерів, відслідковування статусу через веб,
тощо.

%package common
Summary:	Package with common files for nut daemon and its clients
Summary(pl.UTF-8):	Pakiet z plikami wspólnymi dla demona nut i jego klientów
Group:		Applications/System
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/groupmod
Requires(pre):	/usr/sbin/useradd
Provides:	group(ups)
Provides:	user(ups)

%description common
Package with common files for nut daemon and its clients.

%description common -l pl.UTF-8
Pakiet z plikami wspólnymi dla demona nut i jego klientów.

%package client
Summary:	Multi-vendor UPS Monitoring Project Client Utilities
Summary(pl.UTF-8):	Narzędzia klienckie do monitorowania UPS-ów
Summary(ru.UTF-8):	Network UPS Tools - клиентские утилиты мониторинга
Summary(uk.UTF-8):	Network UPS Tools - клієнтські утиліти моніторингу
Group:		Applications/System
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{version}-%{release}
Requires:	rc-scripts

%description client
This package includes the client utilities that are required to
monitor a UPS that the client host is plugged into but monitored via
serial cable by another host on the network....

%description client -l pl.UTF-8
Ten pakiet zawiera narzędzia kliencie potrzebne do monitorowania UPS-a
do którego podłączony jest komputer kliencki, kiedy kabel szeregowy
UPS-a jest podłączony do innego komputera w sieci.

%description client -l ru.UTF-8
Этот пакет включает клиентские утилиты, необходимые для мониторинга
UPS, к которому клиентский хост имеет доступ, но UPS физически
подключен к другому компьютеру в сети.

%description client -l uk.UTF-8
Цей пакет включає клієнтські утиліти, потрібні для моніторингу UPS, до
якого клієнтський хост має доступ, але UPS фізично підключений до
іншого комп'ютеру в мережі.

%package cgi
Summary:	Multi-vendor UPS Monitoring Project Server - CGI utils
Summary(pl.UTF-8):	Narzędzia CGI do monitorowania UPS-ów
Summary(ru.UTF-8):	Network UPS Tools - CGI утилиты
Summary(uk.UTF-8):	Network UPS Tools - CGI утиліти
Group:		Applications/System
Requires:	%{name}-common = %{version}-%{release}

%description cgi
These programs are part of a developing project to monitor the
assortment of UPSes that are found out there in the field. Many models
have serial serial ports of some kind that allow some form of state
checking. This capability has been harnessed where possible to allow
for safe shutdowns, live status tracking on web pages, and more. This
package contains CGI utils.

%description cgi -l pl.UTF-8
Te programy są częścią projektu do monitorowania wielu UPS-ów w jakimś
otoczeniu. Wiele modeli ma porty szeregowe i pozwala na jakąś formę
sprawdzania stanu. Ta funkcjonalność pozwala na bezpieczne
zatrzymywanie systemów, sprawdzanie stanu zasilania przez WWW i inne.
Ten pakiet zawiera narzędzia CGI.

%description cgi -l ru.UTF-8
Этот пакет включает CGI программы для доступа к информации о статусе
UPS через веб-интерфейс.

%description cgi -l uk.UTF-8
Цей пакет включає CGI програми для доступу до інформації про статус
UPS через веб-інтерфейс.

%package devel
Summary:	Files for NUT clients development
Summary(pl.UTF-8):	Pliki do tworzenia klientów NUT-a
Group:		Development/Libraries
Requires:	%{name}-common = %{version}-%{release}
Requires:	openssl-devel >= 0.9.7c

%description devel
Object file and header for developing NUT clients.

%description devel -l pl.UTF-8
Plik wynikowy oraz nagłówek służące do tworzenia klientów NUT-a.

%package hal
Summary:	NUT integration with FreeDesktop HAL
Summary(pl.UTF-8):	Pliki do integracji NUT-a z HAL-em
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description hal
NUT integration with FreeDesktop HAL.

%description hal -l pl.UTF-8
Pliki do integracji NUT-a z HAL-em.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
cp -f /usr/share/automake/config.sub .
%{__libtoolize}
%{__aclocal} -I m4
%{__automake}
%{__autoconf}
%configure \
	--datadir=%{_datadir}/%{name} \
	--with-htmlpath=%{_datadir}/%{name}/html \
	--with-serial \
	--with%{!?with_usb:out}-usb \
	--with%{!?with_snmp:out}-snmp \
	--with%{!?with_hal:out}-hal \
	--with%{!?with_cgi:out}-cgi \
	--with-dev \
	--with%{!?with_neon:out}-neon \
	--with-ssl \
	--with-ipv6 \
	%{?with_usb:--with-udev-dir=/etc/udev} \
	%{?with_hal:--with-hal-callouts-path=%{_libdir}/hal} \
	%{?with_hal:--with-hal-fdi-path=%{_datadir}/hal/fdi/information/20thirdparty} \
	--with-statepath=%{_var}/lib/ups \
	--with-drvpath=/lib/nut \
	--with-cgipath=/home/services/httpd/cgi-bin \
	--with-user=ups \
	--with-group=ups

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{sysconfig,rc.d/init.d},/var/lib/ups,/lib/nut,/sbin}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ups
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ups
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/upsmon
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/upsmon

for i in $RPM_BUILD_ROOT%{_sysconfdir}/*.sample; do
	mv -f $i ${i%.sample}
done

%{!?with_usb:rm -f $RPM_BUILD_ROOT%{_udevrulesdir}/52-nut-usbups.rules}

cat > $RPM_BUILD_ROOT/sbin/poweroff-ups << EOF
#!/bin/sh
/etc/rc.d/init.d/ups powerdown
EOF

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ups
%service ups restart "NUT ups daemon"

%preun
if [ "$1" = "0" ]; then
	%service ups stop
	/sbin/chkconfig --del ups
fi

%pre common
# move to trigger?
if [ -n "`/usr/bin/getgid ups 2> /dev/null`" ] && [ "`/usr/bin/getgid ups 2> /dev/null`" = 121 ]; then
	/usr/sbin/groupmod -g 76 ups
	chgrp ups %{_sysconfdir}/{upsd.conf,ups.conf,upsd.users}
	/usr/sbin/usermod -g 76 ups
fi
%groupadd -g 76 ups
%useradd -u 70 -d /usr/share/empty -s /bin/false -c "UPS Manager User" -g ups ups

%post common -p /sbin/ldconfig

%postun common
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%userremove ups
	%groupremove ups
fi

%post client
/sbin/chkconfig --add upsmon
%service upsmon restart "NUT upsmon daemon"

%preun client
if [ "$1" = "0" ]; then
	%service upsmon stop
	/sbin/chkconfig --del upsmon
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nut-scanner
%attr(755,root,root) %{_bindir}/upscmd
%attr(755,root,root) %{_bindir}/upslog
%attr(755,root,root) %{_bindir}/upsrw
%attr(755,root,root) %{_sbindir}/upsd
%attr(755,root,root) /sbin/poweroff-ups
%attr(755,root,root) %ghost %{_libdir}/libnutscan.so.1
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ups
%attr(754,root,root) /etc/rc.d/init.d/ups
%attr(640,root,ups) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nut.conf
%attr(640,root,ups) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/upsd.conf
%attr(640,root,ups) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ups.conf
%attr(640,root,ups) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/upsd.users
%{_mandir}/man5/ups.conf.5*
%{_mandir}/man5/upsd.conf.5*
%{_mandir}/man5/upsd.users.5*
%{_mandir}/man8/nut-scanner.8*
%{_mandir}/man8/upscmd.8*
%{_mandir}/man8/upscode2.8*
%{_mandir}/man8/upsd.8*
%{_mandir}/man8/upsdrvctl.8*
%{_mandir}/man8/upslog.8*
%{_mandir}/man8/upsrw.8*
%dir %attr(770,root,ups) /var/lib/ups
%dir /lib/nut
%attr(755,root,root) /lib/nut/apcsmart
%attr(755,root,root) /lib/nut/apcsmart-old
%attr(755,root,root) /lib/nut/bcmxcp
%{?with_usb:%attr(755,root,root) /lib/nut/bcmxcp_usb}
%attr(755,root,root) /lib/nut/belkin
%attr(755,root,root) /lib/nut/belkinunv
%attr(755,root,root) /lib/nut/bestfcom
%attr(755,root,root) /lib/nut/bestfortress
%attr(755,root,root) /lib/nut/bestuferrups
%attr(755,root,root) /lib/nut/bestups
%attr(755,root,root) /lib/nut/blazer_ser
%{?with_usb:%attr(755,root,root) /lib/nut/blazer_usb}
%attr(755,root,root) /lib/nut/clone
%attr(755,root,root) /lib/nut/clone-outlet
%attr(755,root,root) /lib/nut/dummy-ups
%attr(755,root,root) /lib/nut/etapro
%attr(755,root,root) /lib/nut/everups
%attr(755,root,root) /lib/nut/gamatronic
%attr(755,root,root) /lib/nut/genericups
%attr(755,root,root) /lib/nut/isbmex
%attr(755,root,root) /lib/nut/ivtscd
%attr(755,root,root) /lib/nut/liebert
%attr(755,root,root) /lib/nut/liebert-esp2
%attr(755,root,root) /lib/nut/masterguard
%attr(755,root,root) /lib/nut/metasys
%attr(755,root,root) /lib/nut/mge-shut
%attr(755,root,root) /lib/nut/mge-utalk
%attr(755,root,root) /lib/nut/microdowell
%{?with_neon:%attr(755,root,root) /lib/nut/netxml-ups}
%attr(755,root,root) /lib/nut/newmge-shut
%attr(755,root,root) /lib/nut/oneac
%attr(755,root,root) /lib/nut/optiups
%attr(755,root,root) /lib/nut/powercom
%attr(755,root,root) /lib/nut/powerpanel
%attr(755,root,root) /lib/nut/rhino
%{?with_usb:%attr(755,root,root) /lib/nut/richcomm_usb}
%attr(755,root,root) /lib/nut/safenet
%attr(755,root,root) /lib/nut/skel
%{?with_snmp:%attr(755,root,root) /lib/nut/snmp-ups}
%attr(755,root,root) /lib/nut/solis
%attr(755,root,root) /lib/nut/tripplite
%attr(755,root,root) /lib/nut/tripplitesu
%{?with_usb:%attr(755,root,root) /lib/nut/tripplite_usb}
%attr(755,root,root) /lib/nut/upscode2
%attr(755,root,root) /lib/nut/upsdrvctl
%{?with_usb:%attr(755,root,root) /lib/nut/usbhid-ups}
%attr(755,root,root) /lib/nut/victronups
%{_datadir}/nut
%{_mandir}/man5/nut.conf.5*
%{_mandir}/man8/apcsmart.8*
%{_mandir}/man8/apcsmart-old.8*
%{_mandir}/man8/bcmxcp.8*
%{?with_usb:%{_mandir}/man8/bcmxcp_usb.8*}
%{_mandir}/man8/belkin.8*
%{_mandir}/man8/belkinunv.8*
%{_mandir}/man8/bestfcom.8*
%{_mandir}/man8/bestfortress.8*
%{_mandir}/man8/bestuferrups.8*
%{_mandir}/man8/bestups.8*
%{_mandir}/man8/blazer.8*
%{_mandir}/man8/clone.8*
%{_mandir}/man8/dummy-ups.8*
%{_mandir}/man8/etapro.8*
%{_mandir}/man8/everups.8*
%{_mandir}/man8/gamatronic.8*
%{_mandir}/man8/genericups.8*
%{_mandir}/man8/isbmex.8*
%{_mandir}/man8/ivtscd.8*
%{_mandir}/man8/liebert.8*
%{_mandir}/man8/liebert-esp2.8*
%{_mandir}/man8/masterguard.8*
%{_mandir}/man8/metasys.8*
%{_mandir}/man8/mge-shut.8*
%{_mandir}/man8/mge-utalk.8*
%{_mandir}/man8/microdowell.8*
%{?with_neon:%{_mandir}/man8/netxml-ups.8*}
%{_mandir}/man8/nutupsdrv.8*
%{_mandir}/man8/oneac.8*
%{_mandir}/man8/optiups.8*
%{_mandir}/man8/powercom.8*
%{_mandir}/man8/powerpanel.8*
%{_mandir}/man8/rhino.8*
%{?with_usb:%{_mandir}/man8/richcomm_usb.8*}
%{_mandir}/man8/safenet.8*
%{?with_snmp:%{_mandir}/man8/snmp-ups.8*}
%{_mandir}/man8/solis.8*
%{_mandir}/man8/tripplite.8*
%{_mandir}/man8/tripplitesu.8*
%{?with_usb:%{_mandir}/man8/tripplite_usb.8*}
%{?with_usb:%{_mandir}/man8/usbhid-ups.8*}
%{_mandir}/man8/victronups.8*
%{?with_usb:%config(noreplace) %verify(not md5 mtime size) %{_udevrulesdir}/52-nut-usbups.rules}

%files common
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS README UPGRADING ChangeLog docs
%dir %{_sysconfdir}
%attr(755,root,root) %ghost %{_libdir}/libupsclient.so.1
%attr(755,root,root) %{_libdir}/libupsclient.so.*.*.*

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/upsc
%attr(755,root,root) %{_sbindir}/upsmon
%attr(755,root,root) %{_sbindir}/upssched
%attr(754,root,root) /etc/rc.d/init.d/upsmon
%attr(640,root,ups) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/upsmon.conf
%attr(640,root,ups) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/upssched.conf
%attr(750,root,ups) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/upssched-cmd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/upsmon
%{_mandir}/man5/upsmon.conf.5*
%{_mandir}/man5/upssched.conf.5*
%{_mandir}/man8/upsc.8*
%{_mandir}/man8/upsmon.8*
%{_mandir}/man8/upssched.8*

%if %{with cgi}
%files cgi
%defattr(644,root,root,755)
%{_datadir}/%{name}/html
%attr(755,root,root) /home/services/httpd/cgi-bin/*.cgi
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hosts.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/upsset.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.html
%{_mandir}/man5/hosts.conf.5*
%{_mandir}/man5/upsset.conf.5*
%{_mandir}/man5/upsstats.html.5*
%{_mandir}/man8/upsimage.cgi.8*
%{_mandir}/man8/upsset.cgi.8*
%{_mandir}/man8/upsstats.cgi.8*
%endif

%if %{with hal}
%files hal
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/hal/hald-addon-bcmxcp_usb
%attr(755,root,root) %{_libdir}/hal/hald-addon-blazer_usb
%attr(755,root,root) %{_libdir}/hal/hald-addon-tripplite_usb
%attr(755,root,root) %{_libdir}/hal/hald-addon-usbhid-ups
%{_datadir}/hal/fdi/information/20thirdparty/20-ups-nut-device.fdi
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libupsclient.so
%{_pkgconfigdir}/libupsclient.pc
%{_includedir}/*.h
%{_mandir}/man3/*.3*
