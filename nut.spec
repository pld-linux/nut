Summary:	Network UPS Tools
Summary(pl):	Sieciowe narz�dzie do UPS-�w
Summary(ru):	NUT - Network UPS Tools
Summary(uk):	NUT - Network UPS Tools
Name:		nut
Version:	1.2.0
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://penguin.harrison.k12.co.us/mirrors/nut/release/1.2/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}-upsmon.init
Patch0:		%{name}-client.patch
Patch1:		%{name}-fideltronik.patch
URL:		http://www.exploits.org/nut/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gd-devel >= 2.0.1
BuildRequires:	libpng-devel
BuildRequires:	openssl-devel
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
Te programy s� cz�ci� projektu do monitorowania wielu UPS-�w w jakim�
otoczeniu. Wiele modeli ma porty szeregowe i pozwala na jak�� form�
sprawdzania stanu. Ta funkcjonalno�� pozwala na bezpieczne
zatrzymywanie system�w, sprawdzanie stanu zasilania przez WWW i inne.

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

%package client
Summary:	Multi-vendor UPS Monitoring Project Client Utilities
Summary(pl):	Narz�dzia klienckie do monitorowania UPS-�w
Summary(uk):	Network UPS Tools - �̦�����˦ ���̦�� ��Φ�������
Summary(ru):	Network UPS Tools - ���������� ������� �����������
Group:		Applications/System
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig

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

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__aclocal}
%{__autoconf}
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
install -d $RPM_BUILD_ROOT/{etc/{sysconfig,rc.d/init.d},/var/lib/ups} \
	$RPM_BUILD_ROOT{%{_libdir}/nut,%{_includedir}}

%{__make} install install-cgi \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ups
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ups
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/upsmon

rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/*
install conf/*.users conf/*.conf $RPM_BUILD_ROOT%{_sysconfdir}

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
%doc NEWS README CHANGES CREDITS docs
%attr(755,root,root) %{_bindir}/upscmd
%attr(755,root,root) %{_bindir}/upslog
%attr(755,root,root) %{_bindir}/upsrw
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
%config(noreplace) %{_sysconfdir}/upsset.conf
