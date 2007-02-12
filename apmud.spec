Summary:	Power Manager daemon for Apple PowerBooks
Summary(pl.UTF-8):   Demon zarządzający poborem energii dla komputerów Apple PowerBook
Name:		apmud
Version:	1.0.0
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://linuxppc.jvc.nl/%{name}-%{version}.tgz
# Source0-md5:	51f3d8a65e92d26ceee7b2e9e06773d3
Source1:	%{name}.init
Patch0:		%{name}-pwrctl.patch
URL:		http://linuxppc.jvc.nl/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	dev
Requires:	hdparm
Provides:	apmd
Obsoletes:	apmd
ExclusiveArch:	ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pmud is a daemon which periodically polls the PMU (power manager) and
performs functions such as enabling or disabling devices appropriately
when the power source changes. It can also be instructed to signal
init(8) that a power-failure has occured.

%description -l pl.UTF-8
pmud to demon regularnie odpytujący PMU (jednostkę zarządzające
energią) i wykonujący funkcje takie jak włączanie i wyłączanie
urządzeń odpowiednio do zmian źródła zasilania. Może także powiadomić
proces init o wystąpieniu awarii zasilania.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,power}

install pmud snooze wakebay fblevel $RPM_BUILD_ROOT%{_sbindir}
install Batmon $RPM_BUILD_ROOT%{_bindir}
install xmouse $RPM_BUILD_ROOT%{_bindir}

install pmud.8 snooze.8 fblevel.8 batmon.8 $RPM_BUILD_ROOT%{_mandir}/man8
install xmouse.8 $RPM_BUILD_ROOT%{_mandir}/man8

install power.conf $RPM_BUILD_ROOT/etc/sysconfig/power
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pmud
install pwrctl $RPM_BUILD_ROOT%{_sysconfdir}/power/pwrctl

ln -sf %{_sbindir}/snooze $RPM_BUILD_ROOT%{_bindir}/apm

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add pmud
%service pmud restart "pmud daemon"

%preun
if [ "$1" = "0" ]; then
	%service pmud stop
	/sbin/chkconfig --del pmud
fi

%files
%defattr(644,root,root,755)
%doc BUGS CHANGES INSTALL README THANKS TODO pwrctl-local
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/power
%attr(754,root,root) /etc/rc.d/init.d/pmud
%dir %{_sysconfdir}/power
%attr(640,root,root) %{_sysconfdir}/power/pwrctl
%{_mandir}/man8/*
