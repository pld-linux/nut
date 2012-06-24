Summary:	Network UPS Tools
Summary(pl):	Sieciowe narz�dzie do UPS-�w
Name:		nut
Version:	1.4.0
Release:	3
License:	GPL
Group:		Applications/System
Source0:	http://penguin.harrison.k12.co.us/mirrors/nut/release/1.4/%{name}-%{version}.tar.gz
# Source0-md5:	1ddf547866db0f1eeb9c535ba0339906
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}-upsmon.init
Source4:	http://www.nixz.net/nut/everups.c
# NoSource4-md5:	526bd50f3f5cedf6d60b99998f866b0d
Patch0:		%{name}-client.patch
Patch1:		%{name}-datadir.patch
Patch2:		%{name}-noX11.patch
URL:		http://www.exploits.org/nut/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gd-devel >= 2.0.15
BuildRequires:	libpng-devel
BuildRequires:	openssl-devel >= 0.9.6m
PreReq:		rc-scripts
Requires(pre):  /bin/id
Requires(pre):  /usr/bin/getgid
Requires(pre):  /usr/sbin/useradd
Requires(pre):  /usr/sbin/groupadd
Requires(post,preun):   /sbin/chkconfig
Requires(postun):       /usr/sbin/groupdel
Requires(postun):       /usr/sbin/userdel
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

This nut ships with modified everups.c - support for Ever UPS models
(by Mikolaj Tutak <mtutak@eranet.pl>)

%description -l pl
Te programy s� cz�ci� projektu do monitorowania wielu UPS-�w w jakim�
otoczeniu. Wiele modeli ma porty szeregowe i pozwala na jak�� form�
sprawdzania stanu. Ta funkcjonalno�� pozwala na bezpieczne
zatrzymywanie system�w, sprawdzanie stanu zasilania przez WWW i inne.

Ta wersja posiada zmieniony sterownik everups.c - obs�uguje zasilacze
firmy Ever UPS models (autorstwa Miko�aja Tutaka <mtutak@eranet.pl>)

%description -l ru
��� ��������� - ����� ������� �� ����������� ��������� UPS. � ������
������� ���� ���������� �����, ����������� ��������� ��������� ����
UPS. ��� ����������� ���� ������������, ��� ��� ��������, ���
���������� ���������� ��������� �����������, ������������ �������
����� ��� � �.�.

%description -l uk
� �������� � �������� ������� �� ��Φ������� Ҧ�����Φ���� UPS.
������ ������� ����� ��Ҧ���Φ �����, �� ��������� ����צ���� ���� ���
UPS. �� �����צ��� ���� �����������, �� �� �������, ��� ���������
��������� ������� ����'���Ҧ�, צ��̦���������� ������� ����� ���,
����.

%package common
Summary:	Package with common files for nut daemon and its clients
Summary(pl):	Pakiet z plikami wsp�lnymi dla demona nut i jego klient�w
Group:		Applications/System

%description common
Package with common files for nut daemon and its clients.

%description common -l pl
Pakiet z plikami wsp�lnymi dla demona nut i jego klient�w.

%package client
Summary:	Multi-vendor UPS Monitoring Project Client Utilities
Summary(pl):	Narz�dzia klienckie do monitorowania UPS-�w
Summary(uk):	Network UPS Tools - �̦�����˦ ���̦�� ��Φ�������
Summary(ru):	Network UPS Tools - ���������� ������� �����������
Group:		Applications/System
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{version}

%description client
This package includes the client utilities that are required to
monitor a UPS that the client host is plugged into but monitored via
serial cable by another host on the network....

%description client -l pl
Ten pakiet zawiera narz�dzia kliencie potrzebne do monitorowania UPS-a
do kt�rego pod��czony jest komputer kliencki, kiedy kabel szeregowy
UPS-a jest pod��czony do innego komputera w sieci.

%description client -l ru
���� ����� �������� ���������� �������, ����������� ��� �����������
UPS, � �������� ���������� ���� ����� ������, �� UPS ���������
��������� � ������� ���������� � ����.

%description client -l uk
��� ����� ������� �̦�����˦ ���̦��, ���Ҧ�Φ ��� ��Φ������� UPS, ��
����� �̦�������� ���� ��� ������, ��� UPS Ʀ����� Ц��������� ��
������ ����'����� � ����֦.

%package cgi
Summary:	Multi-vendor UPS Monitoring Project Server - CGI utils
Summary(pl):	Narz�dzia CGI do monitorowania UPS-�w
Summary(ru):	Network UPS Tools - CGI �������
Summary(uk):	Network UPS Tools - CGI ���̦��
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
Te programy s� cz�ci� projektu do monitorowania wielu UPS-�w w jakim�
otoczeniu. Wiele modeli ma porty szeregowe i pozwala na jak�� form�
sprawdzania stanu. Ta funkcjonalno�� pozwala na bezpieczne
zatrzymywanie system�w, sprawdzanie stanu zasilania przez WWW i inne.
Ten pakiet zawiera narz�dzia CGI.

%description cgi -l ru
���� ����� �������� CGI ��������� ��� ������� � ���������� � �������
UPS ����� ���-���������.

%description cgi -l uk
��� ����� ������� CGI �������� ��� ������� �� �������æ� ��� ������
UPS ����� ���-���������.

%package devel
Summary:	Files for NUT clients development
Summary(pl):	Pliki do tworzenia klient�w NUT-a
Group:		Development/Libraries
Requires:	openssl-devel >= 0.9.6k
# it does NOT require nut

%description devel
Object file and header for developing NUT clients.

%description devel -l pl
Plik wynikowy oraz nag��wek s�u��ce do tworzenia klient�w NUT-a.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
#%{!?_without_new_everups_driver:install %{SOURCE4} drivers/everups.c }

%build
%{__aclocal}
%{__autoconf}
%configure \
	--with-ssl \
	--with-cgi \
	--with-linux-hiddev=%{_includedir}/linux/hiddev.h \
	--with-statepath=%{_var}/lib/ups \
	--with-drvpath=/lib/nut \
	--with-cgipath=/home/httpd/cgi-bin \
	--with-user=ups \
	--with-group=ups
%{__make} all cgi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/sbin,/etc/{sysconfig,rc.d/init.d},/var/lib/ups} \
	$RPM_BUILD_ROOT{/lib/nut,%{_libdir},%{_includedir}/nut}

%{__make} install DESTDIR=$RPM_BUILD_ROOT
	
%{__make} install install-cgi \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ups
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ups
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/upsmon

rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/*
install conf/*.users conf/*.conf conf/*.html $RPM_BUILD_ROOT%{_sysconfdir}

install clients/upsclient.o common/parseconf.o $RPM_BUILD_ROOT%{_libdir}
install clients/upsclient.h include/parseconf.h $RPM_BUILD_ROOT%{_includedir}/nut

cat > $RPM_BUILD_ROOT/sbin/poweroff-ups << EOF
#!/bin/sh
/etc/rc.d/init.d/ups powerdown
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/usr/bin/getgid ups`" ]; then
	if [ "`getgid ups`" != "121" ]; then
		echo "Error: group ups doesn't have gid=121. Correct this before installing %{name}." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 121 -r -f ups
fi
if [ -n "`id -u ups 2>/dev/null`" ]; then
	if [ "`id -u ups`" != "70" ]; then
		echo "Error: user ups doesn't have uid=70. Correct this before installing %{name}." 1>&2
		exit 1
	fi
else
	echo "Adding user ups UID=70."
	/usr/sbin/useradd -u 70 -r -d /no/home -s /bin/false -c "UPS Manager User" -g ups ups 1>&2
fi


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

%postun
if [ "$1" = "0" ]; then
	echo "Removing user ups."
	/usr/sbin/userdel ups
	echo "Removing group ups."
	/usr/sbin/groupdel ups
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
%attr(640,root,ups) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/upsd.conf
%attr(640,root,ups) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ups.conf
%attr(640,root,ups) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/upsd.users
%{_mandir}/man5/ups.conf.5*
%{_mandir}/man5/upsd.conf.5*
%{_mandir}/man5/upsd.users.5*
%{_mandir}/man8/[!u]*.8*
%{_mandir}/man8/upscmd.8*
%{_mandir}/man8/upsd.8*
%{_mandir}/man8/upsdrvctl.8*
%{_mandir}/man8/upslog.8*
%{_mandir}/man8/upsrw.8*
%dir %attr(770,root,ups) /var/lib/ups
%dir /lib/nut
%attr(755,root,root) /lib/nut/*
%{_datadir}/nut

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
%attr(755,root,root) /home/httpd/cgi-bin/*.cgi
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
%{_libdir}/parseconf.o
%{_includedir}/nut
