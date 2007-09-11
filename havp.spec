Summary:	HTTP Antivirus Proxy
Summary(pl.UTF-8):	Antywirusowe Proxy HTTP
Name:		havp
Version:	0.86
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://www.server-side.de/download/%{name}-%{version}.tar.gz
# Source0-md5:	c99c8da224c72844882623086e2b1618
Source1:	%{name}.init
Source2:	%{name}.logrotate
URL:		http://www.server-side.de/
BuildRequires:	autoconf
BuildRequires:	clamav-devel
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(postun,pre):	/usr/sbin/usermod
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/lib/rpm/user_group.sh
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(pre):	/usr/sbin/usermod
Requires:	clamav
Requires:	logrotate >= 3.7-4
Provides:	group(havp)
Provides:	user(havp)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HAVP (HTTP Antivirus Proxy) is a proxy with antivirus scanner. The
main aims continous, non-blocking downloads and smooth scanning of
dynamic or password proctected HTTP traffic.

HAVP has a parent and transparent proxy mode. It can be used with
squid or standalone.

%description -l pl.UTF-8
HAVP (HTTP Antivirus Proxy) jest serwerem proxy z antywirusem. Głownym
celem jest ciągłe i nie blokujące ściągania skanowanie ruchu HTTP.

HAVP może działać jako proxy nadrzędne lub transparentne. Może też być
używane w połączeniu ze squidem lub samodzielnie.

%prep
%setup -q

%build
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

install -d $RPM_BUILD_ROOT/etc/logrotate.d
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

install -d $RPM_BUILD_ROOT/var/run/%{name}
install -d $RPM_BUILD_ROOT/var/log/%{name}
install -d $RPM_BUILD_ROOT/var/log/archive/%{name}
touch $RPM_BUILD_ROOT/var/log/%{name}/access.log
touch $RPM_BUILD_ROOT/var/log/%{name}/%{name}.log

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 215 havp
%useradd -u 215 -d /tmp -s /bin/false -c "HTTP Antivirus Proxy" -g havp havp
m=$(%addusertogroup clamav havp)
if [ -n "$m" ]; then
	echo >&2 "$m"
	%service -q clamd restart
fi

%post
/sbin/chkconfig --add %{name}
touch /var/log/%{name}/access.log
touch /var/log/%{name}/%{name}.log
chown havp:root /var/log/%{name}/*
chmod 640 /var/log/%{name}/*
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%userremove havp
	%groupremove havp
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog INSTALL
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/templates
%dir %attr(770,root,havp) /var/run/%{name}
%dir %attr(750,root,havp) /var/log/%{name}
%dir %attr(750,root,havp) /var/log/archive/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,havp,root) %ghost /var/log/%{name}/access.log
%attr(640,havp,root) %ghost /var/log/%{name}/%{name}.log
# %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,havp) %{_sysconfdir}/%{name}/blacklist
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,havp) %{_sysconfdir}/%{name}/whitelist
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,havp) %{_sysconfdir}/%{name}/%{name}.config
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/templates/css2
%lang(br) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/templates/br
%lang(de) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/templates/de
%lang(en) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/templates/en
%lang(es) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/templates/es
%lang(fr) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/templates/fr
%lang(it) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/templates/it
%lang(nl) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/templates/nl
%lang(pf) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/templates/pf
%lang(pl) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/templates/pl
%lang(ru) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/templates/ru
%lang(sv) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/templates/sv
%attr(755,root,root) %{_sbindir}/*
