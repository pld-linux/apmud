Summary:	Power Manager daemon for Apple PowerBooks
Summary(pl):	Demon zarz±dzaj±cy poborem energii dla komputerów Apple PowerBook
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
Requires:	chkconfig
Requires:	dev
Requires:	hdparm
Provides:	apmd
ExclusiveArch:	ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	apmd

%description
pmud is a daemon which periodically polls the PMU (power manager) and
performs functions such as enabling or disabling devices appropriately
when the power source changes. It can also be instructed to signal
init(8) that a power-failure has occured.

%description -l pl
pmud to demon regularnie odpytuj±cy PMU (jednostkê zarz±dzaj±ce
energi±) i wykonuj±cy funkcje takie jak w³±czanie i wy³±czanie
urz±dzeñ odpowiednio do zmian ¼ród³a zasilania. Mo¿e tak¿e powiadomiæ
proces init o wyst±pieniu awarii zasilania.

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
if [ -f /var/lock/subsys/pmud ]; then
	/etc/rc.d/init.d/pmud restart >&2
else
	echo "Run \"/etc/rc.d/init.d/pmud start\" to start pmud daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/pmud ]; then
		/etc/rc.d/init.d/pmud stop >&2
	fi
	/sbin/chkconfig --del pmud
fi

%files
%defattr(644,root,root,755)
%doc BUGS CHANGES INSTALL README THANKS TODO pwrctl-local
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/*
%attr(644,root,root) /etc/sysconfig/power
%attr(754,root,root) /etc/rc.d/init.d/pmud
%attr(640,root,root) %{_sysconfdir}/power/pwrctl
%{_mandir}/man8/*
