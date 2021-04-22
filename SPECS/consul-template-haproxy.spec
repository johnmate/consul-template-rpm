%if 0%{?_version:1}
%define         _verstr      %{_version}
%else
%define         _verstr      0.1.0
%endif

%define config_dir    %{_sysconfdir}/consul-template.d
%define debug_package %{nil}

Name:           consul-template-haproxy
Version:        %{_verstr}
Release:        1%{?dist}
Summary:        HAproxy teplates for Consul Template.

Source11:       %{name}-config.conf
Source12:       %{name}-template.ctmpl

Requires:      consul-template
Requires:      haproxy

%description
haproxy templates for consul-template

%package config
Summary:    Configuration files for %{name}
Group:      System Environment/Daemons

%description config
Example configuration files for the %{name} service.

%prep
%setup -q -c

%install
%{__install} -p -D -m 0644 %{SOURCE11} %{buildroot}%{config_dir}/config/haproxy.hcl
%{__install} -p -D -m 0644 %{SOURCE12} %{buildroot}%{config_dir}/template/haproxy.ctmpl

%files config
%defattr(-,root,root,-)
%dir %{config_dir}/config
%dir %{config_dir}/template
%config(noreplace) %{config_dir}/*

%changelog
