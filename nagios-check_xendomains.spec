%define name	nagios-check_xendomains
%define version	20070528
%define release	%mkrel 5

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Nagios Xen plugin
Group:		Networking/Other
License:	BSD
URL:		http://beta.perseverantia.com/devel/?project=nagiosplug
Source0:	http://beta.perseverantia.com/devel/src/plugins/check_xendomains.py
Patch:      check_xendomains-fix-shellbang.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Plugin for Nagios (written in Python to check Xen's state on a remote host. As
for now, it just checks that Xend is running (well, it really checks that
xend-http-server is running) and lists the nodes running on the remote host.

%prep
cp %{SOURCE0} check_xendomains.py
%patch -p0

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_libdir}/nagios/plugins
install -m 755 check_xendomains.py %{buildroot}%{_libdir}/nagios/plugins

install -d -m 755 %{buildroot}%{_sysconfdir}/nagios/plugins.d
cat > %{buildroot}%{_sysconfdir}/nagios/plugins.d/check_xendomains.cfg <<'EOF'
define command{
	command_name	check_xendomains
	command_line	%{_libdir}/nagios/plugins/check_xendomains -H $HOSTADDRESS$
}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/nagios/plugins/check_xendomains.py
%config(noreplace) %{_sysconfdir}/nagios/plugins.d/check_xendomains.cfg
