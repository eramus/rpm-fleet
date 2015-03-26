# Copyright 2014, Jan Nabbefeld
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# To Install:
#
# sudo yum -y install rpmdevtools && rpmdev-setuptree
# wget https://raw.github.com/odise/rpm-fleet/master/fleet.spec -O ~/rpmbuild/SPECS/fleet.spec
# wget https://raw.github.com/odise/rpm-fleet/master/fleet.service -O ~/rpmbuild/SOURCE/fleet.service
# wget https://raw.github.com/odise/rpm-fleet/master/fleet.conf -O ~/rpmbuild/SOURCE/fleet.conf
# wget https://github.com/coreos/fleet/releases/download/v0.9.1/fleet-v0.9.1-linux-amd64.tar.gz -O ~/rpmbuild/SOURCES/fleet-v0.9.1-linux-amd64.tar.gz
# rpmbuild -bb ~/rpmbuild/SPECS/fleet.spec

%define debug_package %{nil}
%define etcd_user  %{name}
%define etcd_group %{name}
%define etcd_data  %{_localstatedir}/lib/%{name}

Name:      fleet
Version:   0.9.1
Release:   1
Summary:   A Distributed init System.
License:   Apache 2.0
URL:       https://github.com/coreos/fleet
Group:     System Environment/Daemons
Source0:   https://github.com/coreos/%{name}/releases/download/v%{version}/%{name}-v%{version}-linux-amd64.tar.gz
Source1:   %{name}.service
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
Packager:  Jan Nabbefeld <jan.nabbefeld@kreuzwerker.de>, Louis Zeun <louiszeun@louiszeun.com>
Requires(pre): shadow-utils
Requires(post): /bin/systemctl
Requires(preun): /bin/systemctl
Requires(postun): /bin/systemctl

%description
Fleet ties together systemd and etcd into a distributed init system.
Think of it as an extension of systemd that operates at the cluster level
instead of the machine level. This project is very low level and is
designed as a foundation for higher order orchestration.

%prep
%setup -n %{name}-v%{version}-linux-amd64

%build
rm -rf %{buildroot}

echo  %{buildroot}

%install
install -d -m 755 %{buildroot}/%{_bindir}
install    -m 755 %{_builddir}/%{name}-v%{version}-linux-amd64/fleetd    %{buildroot}/%{_bindir}
install    -m 755 %{_builddir}/%{name}-v%{version}-linux-amd64/fleetctl %{buildroot}/%{_bindir}

install -d -m 755 %{buildroot}/%{_sysconfdir}/fleet
install    -m 644 %_sourcedir/%{name}.conf    %{buildroot}/%{_sysconfdir}/fleet/%{name}.conf

install -d -m 755 %{buildroot}/usr/share/doc/%{name}-v%{version}
install    -m 644 %{_builddir}/%{name}-v%{version}-linux-amd64/README.md    %{buildroot}/%{_defaultdocdir}/%{name}-v%{version}

install -d -m 755 %{buildroot}/%{_sysconfdir}/systemd/system
install    -m 644 %_sourcedir/%{name}.service    %{buildroot}/%{_sysconfdir}/systemd/system/%{name}.service

%clean
rm -rf %{buildroot}

#%pre
#getent group %{etcd_group} >/dev/null || groupadd -r %{etcd_group}
#getent passwd %{etcd_user} >/dev/null || /usr/sbin/useradd --comment "etcd Daemon User" --shell /bin/bash -M -r -g %{etcd_group} --home %{etcd_data} %{etcd_user}

%post
systemctl enable %{name} > /dev/null 2>&1
systemctl start %{name} > /dev/null 2>&1

%preun
if [ $1 = 0 ]; then
  systemctl stop %{name} > /dev/null 2>&1
  systemctl disable %{name} > /dev/null 2>&1
fi

%files
%defattr(-,root,root)
%{_bindir}/fleet*
%{_sysconfdir}/fleet/%{name}.conf
%{_defaultdocdir}/%{name}-v%{version}/*.md
%config(noreplace) %{_sysconfdir}/systemd/system/%{name}.service

%changelog
* Thu Mar 26 2015 Louis Zeun <louiszeun@louiszeun.com> 0.2.0
- Update to v.0.9.1
- Provide conf file to manage fleetd parameters
* Wed Oct 08 2014 Jan Nabbefeld <jan.nabbefeld@kreuzwerker.de> 0.1.0
- Initial spec.
