# TODO: /var/lib/ups dir ownership (shouldn't be nobody)
Summary:	Network UPS Tools
Summary(pl):	Sieciowe narzЙdzie do UPS-Сw
Summary(ru):	NUT - Network UPS Tools
Summary(uk):	NUT - Network UPS Tools
Name:		nut
Version:	1.2.3
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://penguin.harrison.k12.co.us/mirrors/nut/release/1.2/%{name}-%{version}.tar.gz
# Source0-md5:	87dd831a819d06904cbe06e70dcf3c2f
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}-upsmon.init
Patch0:		%{name}-client.patch
URL:		http://www.exploits.org/nut/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gd-devel >= 2.0.1
BuildRequires:	libpng-devel
BuildRequires:	openssl-devel >= 0.9.7
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{version}
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
Te programy s╠ czЙ╤ci╠ projektu do monitorowania wielu UPS-Сw w jakim╤
otoczeniu. Wiele modeli ma porty szeregowe i pozwala na jak╠╤ formЙ
sprawdzania stanu. Ta funkcjonalno╤Ф pozwala na bezpieczne
zatrzymywanie systemСw, sprawdzanie stanu zasilania przez WWW i inne.

%description -l ru
Эти программы - часть проекта по мониторингу различных UPS. У многих
моделей есть сериальные порты, позволяющие проверять состояние этих
UPS. Эта возможность была использована, где это возможно, для
выполнения безопасных остановов компьютеров, отслеживания статуса
через веб и т.п.

%description -l uk
Ц╕ програми ╓ частиною проекту по мон╕торингу р╕зноман╕тних UPS.
Багато моделей мають сер╕альн╕ порти, що дозволять перев╕ряти стан цих
UPS. Ця можлив╕сть була використана, де це можливо, для виконання
безпечних зупинок комп'ютер╕в, в╕дсл╕дковування статусу через веб,
тощо.

%package common
Summary:	Package with common files for nut daemon and its clients
Summary(pl):	Pakiet z plikami wspСlnymi dla demona nut i jego klientСw
Group:		Applications/System

%description common
Package with common files for nut daemon and its clients.

%description common -l pl
Pakiet z plikami wspСlnymi dla demona nut i jego klientСw.

%package client
Summary:	Multi-vendor UPS Monitoring Project Client Utilities
Summary(pl):	NarzЙdzia klienckie do monitorowania UPS-Сw
Summary(uk):	Network UPS Tools - кл╕╓нтськ╕ утил╕ти мон╕торингу
Summary(ru):	Network UPS Tools - клиентские утилиты мониторинга
Group:		Applications/System
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{version}

%description client
This package includes the client utilities that are required to
monitor a UPS that the client host is plugged into but monitored via
serial cable by another host on the network....

%description client -l pl
Ten pakiet zawiera narzЙdzia kliencie potrzebne do monitorowania UPS-a
do ktСrego podЁ╠czony jest komputer kliencki, kiedy kabel szeregowy
UPS-a jest podЁ╠czony do innego komputera w sieci.

%description client -l ru
Этот пакет включает клиентские утилиты, необходимые для мониторинга
UPS, к которому клиентский хост имеет доступ, но UPS физически
подключен к другому компьютеру в сети.

%description client -l uk
Цей пакет включа╓ кл╕╓нтськ╕ утил╕ти, потр╕бн╕ для мон╕торингу UPS, до
якого кл╕╓нтський хост ма╓ доступ, але UPS ф╕зично п╕дключений до
╕ншого комп'ютеру в мереж╕.

%package cgi
Summary:	Multi-vendor UPS Monitoring Project Server - CGI utils
Summary(pl):	NarzЙdzia CGI do monitorowania UPS-Сw
Summary(ru):	Network UPS Tools - CGI утилиты
Summary(uk):	Network UPS Tools - CGI утил╕ти
Group:		Applications/System
Requires:	%{name}-common = %{version}

%description cgi
These programs are part of a developing project to monitor the
assortment of UPSes that are found out there in the field. Many models
have serial serial ports of some kind that allow some form of state
checking. This capability has been harnessed where possible to allow
for safe shutdowns, live status tracking on web pages, and more. This
package contains CGI utils.

%description cgi -l pl
Te programy s╠ czЙ╤ci╠ projektu do monitorowania wielu UPS-Сw w jakim╤
otoczeniu. Wiele modeli ma porty szeregowe i pozwala na jak╠╤ formЙ
sprawdzania stanu. Ta funkcjonalno╤Ф pozwala na bezpieczne
zatrzymywanie systemСw, sprawdzanie stanu zasilania przez WWW i inne.
Ten pakiet zawiera narzЙdzia CGI.

%description cgi -l ru
Этот пакет включает CGI программы для доступа к информации о статусе
UPS через веб-интерфейс.

%description cgi -l uk
Цей пакет включа╓ CGI програми для доступу до ╕нформац╕╖ про статус
UPS через веб-╕нтерфейс.

%package devel
Summary:	Files for NUT clients development
Summary(pl):	Pliki do tworzenia klientСw NUT-a
Group:		Development/Libraries
Requires:	openssl-devel >= 0.9.7
# it does NOT require nut

%description devel
Object file and header for developing NUT clients.

%description devel -l pl
Plik wynikowy oraz nagЁСwek sЁu©╠ce do tworzenia klientСw NUT-a.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
LDFLAGS="-L%{_prefix}/X11R6/lib"; export LDFLAGS
%configure \
	--with-ssl \
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
install -d $RPM_BUILD_ROOT{/sbin,/etc/{sysconfig,rc.d/init.d},/var/lib/ups} \
	$RPM_BUILD_ROOT{%{_libdir}/nut,%{_includedir}}

%{__make} install install-cgi \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ups
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ups
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/upsmon

rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/*
install conf/*.users conf/*.conf conf/*.html $RPM_BUILD_ROOT%{_sysconfdir}

install clients/upsclient.o $RPM_BUILD_ROOT%{_libdir}
install clients/upsclient.h $RPM_BUILD_ROOT%{_includedir}

cat > $RPM_BUILD_ROOT/sbin/poweroff-ups << EOF
#!/bin/sh
/etc/rc.d/init.d/ups powerdown
EOF

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
%attr(755,root,root) %{_bindir}/upscmd
%attr(755,root,root) %{_bindir}/upslog
%attr(755,root,root) %{_bindir}/upsrw
%attr(755,root,root) %{_sbindir}/upsd
%attr(755,root,root) /sbin/poweroff-ups
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/ups
%attr(754,root,root) /etc/rc.d/init.d/ups
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/upsd.conf
%attr(640,root,nobody) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ups.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/upsd.users
%{_mandir}/man5/ups.conf.5*
%{_mandir}/man5/upsd.conf.5*
%{_mandir}/man5/upsd.users.5*
%{_mandir}/man8/[!u]*.8*
%{_mandir}/man8/upscmd.8*
%{_mandir}/man8/upsd.8*
%{_mandir}/man8/upsdrvctl.8*
%{_mandir}/man8/upslog.8*
%{_mandir}/man8/upsrw.8*
%dir %attr(750,nobody,root) /var/lib/ups
%dir %{_libdir}/nut
%attr(755,root,root) %{_libdir}/nut/*

%files common
%defattr(644,root,root,755)
%doc NEWS README CHANGES CREDITS docs
%dir %{_sysconfdir}

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/upsc
%attr(755,root,root) %{_sbindir}/upsmon
%attr(755,root,root) %{_sbindir}/upssched
%attr(755,root,root) %{_sbindir}/upssched-cmd
%attr(754,root,root) /etc/rc.d/init.d/upsmon
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/upsmon.conf
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/upssched.conf
%{_mandir}/man5/upsmon.conf.5*
%{_mandir}/man5/upssched.conf.5*
%{_mandir}/man8/upsc.8*
%{_mandir}/man8/upsmon.8*
%{_mandir}/man8/upssched.8*

%files cgi
%defattr(644,root,root,755)
%attr(755,root,root) /home/services/httpd/cgi-bin/*.cgi
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/hosts.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/upsset.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.html
%{_mandir}/man5/hosts.conf.5*
%{_mandir}/man5/upsset.conf.5*
%{_mandir}/man5/upsstats.html.5*
%{_mandir}/man8/upsimage.cgi.8*
%{_mandir}/man8/upsset.cgi.8*
%{_mandir}/man8/upsstats.cgi.8*

%files devel
%defattr(644,root,root,755)
%{_libdir}/upsclient.o
%{_includedir}/upsclient.h
