%if 0%{?_version:1}
%define         _verstr      %{_version}
%else
%define         _verstr      0.25.2
%endif

%define config_dir    %{_sysconfdir}/consul-template.d
%define debug_package %{nil}

Name:           consul-template
Version:        %{_verstr}
Release:        1%{?dist}
Summary:        Consul Template provides a convenient way to populate values from Consul into the filesystem.

Group:          System Environment/Daemons
License:        Mozilla Public License, version 2.0
URL:            https://github.com/hashicorp/consul-template

Source0:        https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.tgz
Source1:        %{name}.service
Source2:        %{name}.sysconfig
Source10:       %{name}-base-config.conf

BuildRequires:  systemd-units

Requires:           consul
Requires(pre):      shadow-utils
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
The daemon consul-template queries a Consul instance and updates
any number of specified templates on the filesystem.
As an added bonus, consul-template can optionally run arbitrary
commands when the update process completes.

%package config
Summary:    Configuration files for %{name}
Group:      System Environment/Daemons

%description config
Example configuration files for the %{name} service.

%prep
%setup -q -c

%build

%install
mkdir -p %{buildroot}%{config_dir}/config
mkdir -p %{buildroot}%{config_dir}/template
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -p -D -m 0644 %{SOURCE10} %{buildroot}%{config_dir}/config/%{name}.hcl
%{__install} -p -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

%pre

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root,-)
%{_unitdir}/%{name}.service
%{_bindir}/%{name}
%dir %{config_dir}/config
%dir %{config_dir}/template
%config(noreplace) %{config_dir}/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%changelog
