Summary:	Network UPS Tools
Name:		nut
Version:	0.44.1
Release:	2
License:	GPL
Group:		Utilities/System
Group(pl):	Narzêdzia/System
Source0:	http://www.exploits.org/nut/release/%{name}-%{version}.tar.gz
Source1:	ups.init
Patch0:		%{name}-DESTDIR.patch
URL:		http://www.exploits.org/nut/
BuildRequires:	gd-devel
BuildRequires:	libpng-devel
Prereq:		chkconfig
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
Requires:	%{name} = %{version}

%description cgi
These programs are part of a developing project to monitor the assortment
of UPSes that are found out there in the field. Many models have serial
serial ports of some kind that allow some form of state checking. This
capability has been harnessed where possible to allow for safe shutdowns,
live status tracking on web pages, and more.

%prep
%setup -q
%patch -p1

%build
%configure \
	--with-statepath=/var/lib/ups \
	--with-uid=99 \
	--with-gid=99
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/{sysconfig,rc.d/init.d},%{_mandir}/man8,/var/lib/ups}

%{__make} install install-cgi \
	DESTDIR=$RPM_BUILD_ROOT \
	CGIPATH=/home/httpd/cgi-bin

install scripts/RedHat-6.0/ups-config $RPM_BUILD_ROOT/etc/sysconfig/ups
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ups

install man/powercom.8 $RPM_BUILD_ROOT%{_mandir}/man8

gzip -9nf CREDITS Changes QUICKSTART README docs/{FAQ,Changes*,*.txt,cables/*}

%post
/sbin/chkconfig --add ups
if [ -f /var/lock/subsys/ups ]; then
	/etc/rc.d/init.d/ups restart >&2
else
	echo "Run \"/etc/rc.d/init.d/ups start\" to start NUT ups daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/ups ]; then
		/etc/rc.d/init.d/ups stop >&2
	fi
	/sbin/chkconfig --del ups
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz docs/{,cables}/*.gz
%attr(755,root,root) %{_bindir}/apcsmart
%attr(755,root,root) %{_bindir}/bestups
%attr(755,root,root) %{_bindir}/fentonups
%attr(755,root,root) %{_bindir}/genericups
%attr(755,root,root) %{_bindir}/optiups
%attr(755,root,root) %{_bindir}/ups-trust425+625
%attr(755,root,root) %{_bindir}/upsd
%attr(755,root,root) %{_bindir}/upslog
%config(noreplace) /etc/sysconfig/ups
%attr(754,root,root) /etc/rc.d/init.d/ups
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/upsd.conf
%{_mandir}/man8/*

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/upsc
%attr(755,root,root) %{_bindir}/upsct
%attr(755,root,root) %{_bindir}/upsct2
%attr(755,root,root) %{_bindir}/upsmon
%config(noreplace) %{_sysconfdir}/hosts.conf
%config(noreplace) %{_sysconfdir}/multimon.conf
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/upsmon.conf
%dir %attr(775,root,nobody) /var/lib/ups

%files cgi
%defattr(644,root,root,755)
%attr(755,root,root) /home/httpd/cgi-bin/*.cgi
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/upsset.passwd
