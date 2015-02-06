%define name	nagios-check_xendomains
%define version	20070528
%define release	11

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Nagios Xen plugin
Group:		Networking/Other
License:	BSD
URL:		http://beta.perseverantia.com/devel/?project=nagiosplug
Source0:	http://beta.perseverantia.com/devel/src/plugins/check_xendomains.py
Patch:      check_xendomains-fix-shellbang.patch
BuildArch:	noarch
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

install -d -m 755 %{buildroot}%{_datadir}/nagios/plugins
install -m 755 check_xendomains.py %{buildroot}%{_datadir}/nagios/plugins/check_xendomains

install -d -m 755 %{buildroot}%{_sysconfdir}/nagios/plugins.d
cat > %{buildroot}%{_sysconfdir}/nagios/plugins.d/check_xendomains.cfg <<'EOF'
define command{
	command_name	check_xendomains
	command_line	%{_datadir}/nagios/plugins/check_xendomains -H $HOSTADDRESS$
}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_datadir}/nagios/plugins/check_xendomains
%config(noreplace) %{_sysconfdir}/nagios/plugins.d/check_xendomains.cfg


%changelog
* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 20070528-10mdv2011.0
+ Revision: 612985
- the mass rebuild of 2010.1 packages

* Wed Apr 28 2010 Guillaume Rousse <guillomovitch@mandriva.org> 20070528-9mdv2010.1
+ Revision: 540288
- this is a noarch plugin

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 20070528-8mdv2010.0
+ Revision: 430147
- rebuild

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 20070528-7mdv2009.0
+ Revision: 253545
- rebuild

* Wed Mar 05 2008 Guillaume Rousse <guillomovitch@mandriva.org> 20070528-5mdv2008.1
+ Revision: 180030
- fix python shellbang to avoid dependency on python 2.4

* Fri Feb 15 2008 Guillaume Rousse <guillomovitch@mandriva.org> 20070528-4mdv2008.1
+ Revision: 168930
- fix configuration (thanks oden)

* Fri Feb 15 2008 Guillaume Rousse <guillomovitch@mandriva.org> 20070528-3mdv2008.1
+ Revision: 168915
- add a configuration file

* Fri Feb 15 2008 Oden Eriksson <oeriksson@mandriva.com> 20070528-2mdv2008.1
+ Revision: 168866
- it can't be a noarch package

* Fri Feb 01 2008 Guillaume Rousse <guillomovitch@mandriva.org> 20070528-1mdv2008.1
+ Revision: 161129
- import nagios-check_xendomains


* Fri Feb 01 2008 Guillaume Rousse <guillomovitch@mandriva.org> 20070528-1mdv2008.1
- first mandriva package
