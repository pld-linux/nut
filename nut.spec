Summary:	Network UPS Tools
Summary(pl):	Sieciowe narz�dzie do UPS-�w
Name:		nut
Version:	0.45.0
Release:	0
License:	GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Source0:	http://www.exploits.org/nut/release/%{name}-%{version}.tar.gz
Source1:	ups.init
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-ever.patch
URL:		http://www.exploits.org/nut/
BuildRequires:	gd-devel
BuildRequires:	libpng-devel
Prereq:		chkconfig
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
Requires:	%{name} = %{version}

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

%build
%configure \
	--with-statepath=/var/lib/ups \
	--with-uid=99 \
	--with-gid=99
%{__make} all cgi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/{sysconfig,rc.d/init.d},/var/lib/ups}

%{__make} install install-cgi \
	DESTDIR=$RPM_BUILD_ROOT \
	CGIPATH=/home/httpd/cgi-bin

install scripts/RedHat-6.0/ups-config $RPM_BUILD_ROOT/etc/sysconfig/ups
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ups

(
cd $RPM_BUILD_ROOT/etc/ups
for i in `ls *`
do
  mv $i `basename $i .sample`
done
)

gzip -9nf CREDITS README docs/{FAQ,Changes*,*.txt,cables/*}

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

%attr(755,root,root) %{_bindir}/belkin
%attr(755,root,root) %{_bindir}/bestfort
%attr(755,root,root) %{_bindir}/bestuferrups
%attr(755,root,root) %{_bindir}/engetron
%attr(755,root,root) %{_bindir}/ipt-anzen
%attr(755,root,root) %{_bindir}/mge-ellipse
%attr(755,root,root) %{_bindir}/mgeups
%attr(755,root,root) %{_bindir}/multilink
%attr(755,root,root) %{_bindir}/mustekups
%attr(755,root,root) %{_bindir}/powercom
%attr(755,root,root) %{_bindir}/sec
%attr(755,root,root) %{_bindir}/toshiba1500
%attr(755,root,root) %{_bindir}/upseyeux
%attr(755,root,root) %{_bindir}/victronups
%attr(755,root,root) %{_bindir}/everups

%attr(755,root,root) %{_sbindir}/upsd
%attr(755,root,root) %{_bindir}/upslog
%config(noreplace) /etc/sysconfig/ups
%attr(754,root,root) /etc/rc.d/init.d/ups
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/upsd.conf
%{_mandir}/man8/*
%dir %attr(775,root,nobody) /var/lib/ups

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/upsc
%attr(755,root,root) %{_bindir}/upsct
%attr(755,root,root) %{_bindir}/upsct2
%attr(755,root,root) %{_sbindir}/upsmon
%attr(755,root,root) %{_sbindir}/upssched
%config(noreplace) %{_sysconfdir}/hosts.conf
%config(noreplace) %{_sysconfdir}/multimon.conf
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/upsmon.conf

%files cgi
%defattr(644,root,root,755)
%attr(755,root,root) /home/httpd/cgi-bin/*.cgi
#%attr(600,root,root) %config(noreplace) %{_sysconfdir}/upsset.passwd
