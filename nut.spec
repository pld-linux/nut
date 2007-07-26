# TODO:
#	- unpackaged files:
#		/usr/html/{{bottom,header,index}.html,nut-banner.png}
#		/etc/udev/rules.d/52_nut-usbups.rules
#	- upsdrvctl (used by ups.init) doesn't recognize status and reload commands
#
# Conditional build:
%bcond_without	usb			# build without usb drivers
%bcond_without	hal			# build without hal support
%bcond_without	snmp			# build without snmp driver
%bcond_without	cgi			# build without cgi support
#
Summary:	Network UPS Tools
Summary(pl.UTF-8):	Sieciowe narzędzie do UPS-ów
Name:		nut
Version:	2.2.0
Release:	0.5
License:	GPL
Group:		Applications/System
Source0:	http://eu1.networkupstools.org/source/2.2/%{name}-%{version}.tar.gz
# Source0-md5:	a3570515d80804051d4e7631e8a3eb12
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}-upsmon.init
Source4:	%{name}.sysconfig.upsmon
Patch0:		%{name}-client.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-smartdp-load.patch
Patch3:		%{name}-upssched-cmd-sysconf.patch
URL:		http://www.networkupstools.org/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_hal:BuildRequires:	dbus-glib-devel}
%{?with_cgi:BuildRequires:	gd-devel >= 2.0.15}
%{?with_hal:BuildRequires:	hal-devel}
%{?with_usb:BuildRequires:	libusb-devel}
%{?with_snmp:BuildRequires:	net-snmp-devel}
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{version}-%{release}
Requires:	rc-scripts
Obsoletes:	smartupstools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/ups

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
Requires:	openssl-devel >= 0.9.7c
# it does NOT require nut

%description devel
Object file and header for developing NUT clients.

%description devel -l pl.UTF-8
Plik wynikowy oraz nagłówek służące do tworzenia klientów NUT-a.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
cp -f /usr/share/automake/config.sub .
%{__aclocal} -I m4
%{__automake}
%{__autoconf}
%configure \
	--datadir=%{_datadir}/%{name} \
	%{?with_hal:--with-hal} \
	%{!?with_hal:--without-hal} \
	--with-serial \
	%{?with_snmp:--with-snmp} \
	%{!?with_snmp:--without-snmp} \
	%{?with_usb:--with-usb} \
	%{!?with_usb:--without-usb} \
	--with-ssl \
	%{?with_cgi:--with-cgi} \
	%{!?with_cgi:--without-cgi} \
	--with-linux-hiddev=%{_includedir}/linux/hiddev.h \
	--with-statepath=%{_var}/lib/ups \
	--with-drvpath=/lib/nut \
	--with-cgipath=/home/services/httpd/cgi-bin \
	--with-user=ups \
	--with-group=ups
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/sbin,/etc/{sysconfig,rc.d/init.d},/var/lib/ups} \
	$RPM_BUILD_ROOT{/lib/nut,%{_libdir},%{_includedir}/nut}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ups
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ups
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/upsmon
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/upsmon

for i in $RPM_BUILD_ROOT%{_sysconfdir}/*.sample; do
	mv -f $i ${i%.sample}
done

install clients/upsclient.o common/parseconf.o $RPM_BUILD_ROOT%{_libdir}
install clients/upsclient.h include/parseconf.h $RPM_BUILD_ROOT%{_includedir}/nut

cat > $RPM_BUILD_ROOT/sbin/poweroff-ups << EOF
#!/bin/sh
/etc/rc.d/init.d/ups powerdown
EOF

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
if [ -n "`/usr/bin/getgid ups`" ] && [ "`/usr/bin/getgid ups`" = 121 ]; then
	/usr/sbin/groupmod -g 76 ups
	chgrp ups %{_sysconfdir}/{upsd.conf,ups.conf,upsd.users}
	/usr/sbin/usermod -g 76 ups
fi
%groupadd -g 76 ups
%useradd -u 70 -d /usr/share/empty -s /bin/false -c "UPS Manager User" -g ups ups

%post client
/sbin/chkconfig --add upsmon
%service upsmon restart "NUT upsmon daemon"

%preun client
if [ "$1" = "0" ]; then
	%service upsmon stop
	/sbin/chkconfig --del upsmon
fi

%postun common
if [ "$1" = "0" ]; then
	%userremove ups
	%groupremove ups
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/upscmd
%attr(755,root,root) %{_bindir}/upslog
%attr(755,root,root) %{_bindir}/upsrw
%attr(755,root,root) %{_sbindir}/upsd
%attr(755,root,root) /sbin/poweroff-ups
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ups
%attr(754,root,root) /etc/rc.d/init.d/ups
%attr(640,root,ups) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/upsd.conf
%attr(640,root,ups) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ups.conf
%attr(640,root,ups) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/upsd.users
%{_mandir}/man5/ups.conf.5*
%{_mandir}/man5/upsd.conf.5*
%{_mandir}/man5/upsd.users.5*
%{_mandir}/man8/upscmd.8*
%{_mandir}/man8/upscode2.8*
%{_mandir}/man8/upsd.8*
%{_mandir}/man8/upsdrvctl.8*
%{_mandir}/man8/upslog.8*
%{_mandir}/man8/upsrw.8*
%dir %attr(770,root,ups) /var/lib/ups
%dir /lib/nut
%attr(755,root,root) /lib/nut/al175
%attr(755,root,root) /lib/nut/apcsmart
%attr(755,root,root) /lib/nut/bcmxcp
%{?with_usb:%attr(755,root,root) /lib/nut/bcmxcp_usb}
%attr(755,root,root) /lib/nut/belkin
%attr(755,root,root) /lib/nut/belkinunv
%attr(755,root,root) /lib/nut/bestfcom
%attr(755,root,root) /lib/nut/bestuferrups
%attr(755,root,root) /lib/nut/bestups
%attr(755,root,root) /lib/nut/cpsups
%attr(755,root,root) /lib/nut/cyberpower
%attr(755,root,root) /lib/nut/dummy-ups
%{?with_usb:%attr(755,root,root) /lib/nut/energizerups}
%attr(755,root,root) /lib/nut/etapro
%attr(755,root,root) /lib/nut/everups
%attr(755,root,root) /lib/nut/gamatronic
%attr(755,root,root) /lib/nut/genericups
%if %{with hal}
%attr(755,root,root) /lib/nut/hald-addon-bcmxcp_usb
%attr(755,root,root) /lib/nut/hald-addon-megatec_usb
%attr(755,root,root) /lib/nut/hald-addon-tripplite_usb
%attr(755,root,root) /lib/nut/hald-addon-usbhid-ups
%endif
%attr(755,root,root) /lib/nut/isbmex
%attr(755,root,root) /lib/nut/liebert
%attr(755,root,root) /lib/nut/masterguard
%attr(755,root,root) /lib/nut/megatec
%{?with_usb:%attr(755,root,root) /lib/nut/megatec_usb}
%attr(755,root,root) /lib/nut/metasys
%attr(755,root,root) /lib/nut/mge-shut
%attr(755,root,root) /lib/nut/mge-utalk
%attr(755,root,root) /lib/nut/newmge-shut
%attr(755,root,root) /lib/nut/nitram
%attr(755,root,root) /lib/nut/oneac
%attr(755,root,root) /lib/nut/optiups
%attr(755,root,root) /lib/nut/powercom
%attr(755,root,root) /lib/nut/powerpanel
%attr(755,root,root) /lib/nut/rhino
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
%{_mandir}/man8/al175.8*
%{_mandir}/man8/apcsmart.8*
%{_mandir}/man8/bcmxcp.8*
%{?with_usb:%{_mandir}/man8/bcmxcp_usb.8*}
%{_mandir}/man8/belkin.8*
%{_mandir}/man8/belkinunv.8*
%{_mandir}/man8/bestfcom.8*
%{_mandir}/man8/bestuferrups.8*
%{_mandir}/man8/bestups.8*
%{_mandir}/man8/cpsups.8*
%{_mandir}/man8/cyberpower.8*
%{_mandir}/man8/dummy-ups.8*
%{?with_usb:%{_mandir}/man8/energizerups.8*}
%{_mandir}/man8/etapro.8*
%{_mandir}/man8/everups.8*
%{_mandir}/man8/gamatronic.8*
%{_mandir}/man8/genericups.8*
%{_mandir}/man8/isbmex.8*
%{_mandir}/man8/liebert.8*
%{_mandir}/man8/masterguard.8*
%{_mandir}/man8/megatec.8*
%{?with_usb:%{_mandir}/man8/megatec_usb.8*}
%{_mandir}/man8/metasys.8*
%{_mandir}/man8/mge-shut.8*
%{_mandir}/man8/mge-utalk.8*
%{_mandir}/man8/nitram.8*
%{_mandir}/man8/nutupsdrv.8*
%{_mandir}/man8/oneac.8*
%{_mandir}/man8/optiups.8*
%{_mandir}/man8/powercom.8*
%{_mandir}/man8/powerpanel.8*
%{_mandir}/man8/rhino.8*
%{_mandir}/man8/safenet.8*
%{?with_snmp:%{_mandir}/man8/snmp-ups.8*}
%{_mandir}/man8/solis.8*
%{_mandir}/man8/tripplite.8*
%{_mandir}/man8/tripplitesu.8*
%{?with_usb:%{_mandir}/man8/tripplite_usb.8*}
%{?with_usb:%{_mandir}/man8/usbhid-ups.8*}
%{_mandir}/man8/victronups.8*

%files common
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS README UPGRADING ChangeLog docs
%dir %{_sysconfdir}

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

%files devel
%defattr(644,root,root,755)
%{_libdir}/upsclient.o
%{_libdir}/parseconf.o
%{_includedir}/nut
