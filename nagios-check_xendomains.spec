%define name	nagios-check_xendomains
%define version	20070528
%define release	%mkrel 2

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Nagios Xen plugin
Group:		Networking/Other
License:	BSD
URL:		http://beta.perseverantia.com/devel/?project=nagiosplug
Source0:	http://beta.perseverantia.com/devel/src/plugins/check_xendomains.py
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Plugin for Nagios (written in Python to check Xen's state on a remote host. As
for now, it just checks that Xend is running (well, it really checks that
xend-http-server is running) and lists the nodes running on the remote host.

%prep

%build


%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_libdir}/nagios/plugins
install -m 755 %{SOURCE0} %{buildroot}%{_libdir}/nagios/plugins

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/nagios/plugins/check_xendomains.py
