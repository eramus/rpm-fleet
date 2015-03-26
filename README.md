To Install:
===========

An RPM spec file to build and install fleet. Heavily inspired by rpm-etcd made by Nathan Milford.

`sudo yum -y install rpmdevtools && rpmdev-setuptree`

`wget https://raw.github.com/odise/rpm-fleet/master/fleet.spec -O ~/rpmbuild/SPECS/fleet.spec`

`wget https://raw.github.com/odise/rpm-fleet/master/fleet.service -O ~/rpmbuild/SOURCE/fleet.service`

`wget https://raw.github.com/odise/rpm-fleet/master/fleet.conf -O ~/rpmbuild/SOURCE/fleet.conf`

`wget https://github.com/coreos/fleet/releases/download/v0.9.1/fleet-v0.9.1-linux-amd64.tar.gz -O ~/rpmbuild/SOURCES/fleet-v0.9.1-linux-amd64.tar.gz`

`rpmbuild -bb ~/rpmbuild/SPECS/fleet.spec`

