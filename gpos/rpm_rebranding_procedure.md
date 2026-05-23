# Procedure
- Make sure you are in the gpos minimal docker container or the VM
for gpos docker:
> docker run -it release.enlightcloud.com/gpos/gpos:minimal bash

This will open the bash inside the container for gpos.

1. Search for the latest version package from the following website:
> https://centos.pkgs.org/
So go to this website and search for the specified packages and get the latest version for
CentOS stream 9 x86_64 (even aarch works)

2. make sure that repdevtools and wget are installed in the container.
> dnf install wget rpmdevtools

3. copy that specific link
4. wget it on the gpos container
> wget <copied link>


5. whatever src rpm you downloaded, we have to extract the specs and source from that package, so we do this:
> rpm -ivh <whatever_package_downloaded>.src.rpm

6. There will be 2 files inside the extracted package folder
`SPECS` and `SOURCES`
All the changes that needs to be made will be in these 2 folders only.

7. cd into the SPECS folder
> cd SPECS

8. rpm build the spec file - basically through the spec file it will pull all the sources and build a new srpm and
rpm package.
> rpmbuild -ba <whatever_package_downloaded>.spec

9. After the above command is completed execution, it will generate 2 new folders RPM and SRPM.
