%if %{_use_internal_dependency_generator}
%define __noautoreq 'perl\\(VMware::VmPerl(.*)\\)'
%else
%define _requires_exceptions perl\(VMware::VmPerl
%endif

%global build_gnbd 0

%define module_name gnbd
%define major	3
%define fmajor	4
%define libcman		%mklibname cman %{major}
%define devcman		%mklibname -d cman
%define libccs		%mklibname ccs %{major}
%define devccs		%mklibname -d ccs
%define libdlm		%mklibname dlm %{major}
%define devdlm		%mklibname -d dlm
%define libdlm_lt	%mklibname dlm_lt %{major}
%define devdlm_lt	%mklibname -d dlm_lt
%define libdlmcontrol	%mklibname dlmcontrol %{major}
%define devdlmcontrol	%mklibname -d dlmcontrol
%define libfence	%mklibname fence %{fmajor}
%define devfence	%mklibname -d fence
%define libfenced	%mklibname fence %{major}
%define devfenced	%mklibname -d fence
%define liblogthread	%mklibname logthread %{major}
%define devlogthread	%mklibname -d logthread

Summary:	Redhat suite for clustered filesystems
Name:		cluster
Version:	3.0.17
Release:	10
License:	GPL
Group:		System/Kernel and hardware
Url:		http://sources.redhat.com/cluster/wiki
Source0:	https://fedorahosted.org/releases/c/l/cluster/cluster-%{version}.tar.gz
Source1:	gfs-2.6.18-2.6.23.patch

# Remove apc_snmp, as its compilation is broken
Patch0:		cluster-2.03.07-fix-cman-init.patch
Patch2:		cluster-2.03.11-gfs-should-start-clvmd.patch

BuildRequires:	openldap-devel
# For perl binding
BuildRequires:	perl-devel
BuildRequires:	pkgconfig(libSaAmf)
BuildRequires:	pkgconfig(libvirt)
Buildrequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(ncurses)
# For fence_xvm
BuildRequires:	pkgconfig(nss)
# For ldap configuration support
BuildRequires:	pkgconfig(slang)

Requires:	cman
Requires:	gfs-utils
Requires:	rgmanager

%description
Redhat suite for clustered filesystems.

#----------------------------------------------------------------------------

%package -n %{libcman}
Summary:	Shared Librairies for Cluster Manager
Group:		Development/Other

%description  -n %{libcman}
Shared Librairies for Cluster Manager.

%files -n %{libcman}
%{_libdir}/libcman.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devcman}
Summary:	Cluster Manager header files and development libraries
Group:		Development/Other
Requires:	%{libcman} = %{EVRD}
Provides:	cman-devel = %{EVRD}

%description -n %{devcman}
This package contains header files and development libraries.

%files -n %{devcman}
%{_libdir}/libcman.so
%{_includedir}/libcman.h
%{_libdir}/pkgconfig/libcman.pc

#----------------------------------------------------------------------------

%package -n %{libccs}
Summary:	Shared Librairies for Cluster Configuration Service
Group:		Development/Other

%description  -n %{libccs}
Shared Librairies for Cluster Configuration Service.

%files -n %{libccs}
%{_libdir}/libccs.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devccs}
Summary:	Development libraries for Cluster Configuration Service
Group:		Development/Other
Requires:	%{libccs} = %{EVRD}
Provides:	ccs-devel = %{EVRD}

%description -n %{devccs}
Development libraries for Cluster Configuration Service.

%files -n %{devccs}
%{_libdir}/libccs.so
%{_includedir}/ccs.h
%{_libdir}/pkgconfig/libccs.pc

#----------------------------------------------------------------------------

%package -n %{libdlm}
Summary:	Shared Librairies for the Distributed Lock Manager
Group:		Development/Other

%description -n %{libdlm}
Shared Librairies for cluster.

%files -n %{libdlm}
%{_libdir}/libdlm.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devdlm}
Summary:	Distributed Lock Manager header files and development libraries
Group:		Development/Other
Requires:	%{libdlm} = %{EVRD}
Provides:	dlm-devel = %{EVRD}

%description -n %{devdlm}
This package contains header files and development libraries.

%files -n %{devdlm}
%{_libdir}/libdlm.so
%{_mandir}/man3/*dlm*.3.*
%{_includedir}/libdlm.h
%{_libdir}/pkgconfig/libdlm.pc

#----------------------------------------------------------------------------

%package -n %{libdlm_lt}
Summary:	Shared Librairies for the Distributed Lock Manager
Group:		Development/Other
Conflicts:	%{_lib}dlm3 < 3.0.17-7

%description -n %{libdlm_lt}
Shared Librairies for cluster.

%files -n %{libdlm_lt}
%{_libdir}/libdlm_lt.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devdlm_lt}
Summary:	Distributed Lock Manager header files and development libraries
Group:		Development/Other
Requires:	%{libdlm_lt} = %{EVRD}
Provides:	dlm_lt-devel = %{EVRD}
Conflicts:	%{_lib}dlm-devel < 3.0.17-7

%description -n %{devdlm_lt}
This package contains header files and development libraries.

%files -n %{devdlm_lt}
%{_libdir}/libdlm_lt.so
%{_libdir}/pkgconfig/libdlm_lt.pc

#----------------------------------------------------------------------------

%package -n %{libdlmcontrol}
Summary:	Shared Librairies for the Distributed Lock Manager
Group:		Development/Other
Conflicts:	%{_lib}dlm3 < 3.0.17-7

%description -n %{libdlmcontrol}
Shared Librairies for cluster.

%files -n %{libdlmcontrol}
%{_libdir}/libdlmcontrol.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devdlmcontrol}
Summary:	Distributed Lock Manager header files and development libraries
Group:		Development/Other
Requires:	%{libdlmcontrol} = %{EVRD}
Provides:	dlmcontrol-devel = %{EVRD}
Conflicts:	%{_lib}dlm-devel < 3.0.17-7

%description -n %{devdlmcontrol}
This package contains header files and development libraries.

%files -n %{devdlmcontrol}
%{_libdir}/libdlmcontrol.so
%{_libdir}/pkgconfig/libdlmcontrol.pc
%{_includedir}/libdlmcontrol.h

#----------------------------------------------------------------------------

%package -n %{libfence}
Summary:	Shared Librairies for cluster fencing
Group:		Development/Other
Conflicts:	%{_lib}fence3 < 3.0.17-7
Obsoletes:	%{_lib}fence3 < 3.0.17-7

%description -n %{libfence}
Shared Librairies for cluster fencing.

%files -n %{libfence}
%{_libdir}/libfence.so.%{fmajor}*

#----------------------------------------------------------------------------

%package -n %{devfence}
Summary:	Development libraries for cluster fencing
Group:		Development/Other
Requires:	%{libfence} = %{EVRD}
Provides:	fence-devel = %{EVRD}

%description -n %{devfence}
Development libraries for cluster fencing.

%files -n %{devfence}
%{_includedir}/libfence.h
%{_libdir}/libfence.so
%{_libdir}/pkgconfig/libfence.pc

#----------------------------------------------------------------------------

%package -n %{libfenced}
Summary:	Shared Librairies for cluster fencing
Group:		Development/Other
Conflicts:	%{_lib}fence3 < 3.0.17-7

%description -n %{libfenced}
Shared Librairies for cluster fencing.

%files -n %{libfenced}
%{_libdir}/libfenced.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devfenced}
Summary:	Development libraries for cluster fencing
Group:		Development/Other
Requires:	%{libfenced} = %{EVRD}
Provides:	fenced-devel = %{EVRD}
Conflicts:	%{_lib}fence-devel < 3.0.17-7

%description -n %{devfenced}
Development libraries for cluster fencing.

%files -n %{devfenced}
%{_includedir}/libfenced.h
%{_libdir}/libfenced.so
%{_libdir}/pkgconfig/libfenced.pc

#----------------------------------------------------------------------------

%package -n %{liblogthread}
Summary:	Shared Librairies for cluster fencing
Group:		Development/Other

%description  -n %{liblogthread}
Shared Librairies for cluster fencing.

%files -n %{liblogthread}
%{_libdir}/liblogthread.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devlogthread}
Summary:	Development libraries for cluster fencing
Group:		Development/Other
Requires:	%{liblogthread} = %{EVRD}
Provides:	logthread-devel = %{EVRD}

%description -n %{devlogthread}
Development libraries for cluster fencing.

%files -n %{devlogthread}
%{_includedir}/*logthread*.h
%{_libdir}/liblogthread.so
%{_libdir}/pkgconfig/liblogthread*.pc

#----------------------------------------------------------------------------

%package devel
Summary:	Cluster Manager header files and development libraries
Group:		Development/Other
Requires:	%{devcman} = %{EVRD}
Requires:	%{devccs} = %{EVRD}
Requires:	%{devdlm} = %{EVRD}
Requires:	%{devdlm_lt} = %{EVRD}
Requires:	%{devdlmcontrol} = %{EVRD}
Requires:	%{devfence} = %{EVRD}
Requires:	%{devfenced} = %{EVRD}
Requires:	%{devlogthread} = %{EVRD}

%description devel
Cluster Manager header files and development libraries.

%files devel
%{_datadir}/doc/%{name}

#----------------------------------------------------------------------------

%package -n perl-Cluster-CCS
Summary:	Perl bindings for Cluster Configuration Service
Group:		Development/Perl

%description -n perl-Cluster-CCS
Perl bindings for Cluster Configuration Service.

%files -n perl-Cluster-CCS
%{perl_vendorarch}/auto/Cluster/CCS
%{perl_vendorarch}/Cluster/CCS.pm
%{_mandir}/man3/Cluster::CCS.3pm.*

#----------------------------------------------------------------------------

%if %{build_gnbd}
%package -n dkms-%{module_name}
Summary:	Redhat's cluster suite kernel modules
Group:		System/Kernel and hardware
Requires(pre,post):	dkms

%description -n dkms-%{module_name}
The dynamic kernel modules.

%files -n dkms-%{module_name}
%{_usrsrc}/%{module_name}-%{version}-%{release}

%post -n dkms-%{module_name}
dkms add -m %{module_name} -v %{version}-%{release} --rpm_safe_upgrade
dkms build -m %{module_name} -v %{version}-%{release} --rpm_safe_upgrade
dkms install -m %{module_name} -v %{version}-%{release} --rpm_safe_upgrade

%preun -n dkms-%{module_name}
dkms remove -m %{module_name} -v %{version}-%{release} --rpm_safe_upgrade --all ||:
%endif

#----------------------------------------------------------------------------

%package -n dkms-gfs
Summary:	Global File System Kernel Driver
Group:		System/Kernel and hardware
Requires(pre,post):	dkms

%description -n dkms-gfs
The dynamic kernel module package for Global File System.

This package is only required for kernels older than 2.6.24
(newer kernels ship with a gfs driver).

%files -n dkms-gfs
%{_usrsrc}/gfs-%{version}-%{release}

%post -n dkms-gfs
dkms add -m gfs -v %{version}-%{release} --rpm_safe_upgrade
dkms build -m gfs -v %{version}-%{release} --rpm_safe_upgrade
dkms install -m gfs -v %{version}-%{release} --rpm_safe_upgrade

%preun -n dkms-gfs
dkms remove -m gfs -v %{version}-%{release} --rpm_safe_upgrade --all ||:

#----------------------------------------------------------------------------

%package -n cman
Group:		System/Kernel and hardware
Summary:	Cluster Manager
Requires:	openais >= 1.1.0
Requires:	libxml2-utils
Requires:	fence-agents
Requires(pre,post):	rpm-helper
# Try and ensure we upgrade packages that depend on cman
Conflicts:	gfs-utils < %{version}, gfs2-utils < %{version},
Conflicts:	rgmanager < %{version}, gnbd < %{version}

%description -n cman
Cluster Manager.

%files -n cman
%{_initrddir}/cman
%{_sbindir}/cman*
%{_sbindir}/fence*
%{_sbindir}/dlm*
%{_sbindir}/ccs*
%{_sbindir}/group*
%{_sbindir}/*qdisk*
%{_sbindir}/gfs_control*
%{_sbindir}/confdb2ldif
%dir /etc/cluster
%config(noreplace) %{_sysconfdir}/logrotate.d/cluster
%dir /var/log/cluster
%{_libdir}/lcrso/service_cman.lcrso
%{_libdir}/lcrso/config_*.lcrso
%config /etc/udev/rules.d/51-dlm.rules
%{_mandir}/man8/cman*.8.*
%{_mandir}/man5/cman.5.*
%{_mandir}/man5/cluster.conf.5.*
%{_mandir}/man5/qdisk.5.*
%{_mandir}/man8/fence*.8.*
%{_mandir}/man8/dlm*.8.*
%{_mandir}/man8/ccs*.8.*
%{_mandir}/man8/*group*.8.*
%{_mandir}/man8/*qdisk*.8.*
%{_mandir}/man8/confdb2ldif.8.*
%{_mandir}/man8/gfs_control*.8.*
%doc doc/usage.txt
%doc config/plugins/ldap/99cluster.ldif

%post -n cman
%_post_service cman
%_post_service qdiskd
%_post_service scsi_reserve

%preun -n cman
%_preun_service cman
%_preun_service qdiskd
%_preun_service scsi_reserve

#----------------------------------------------------------------------------

%package -n rgmanager
Group:		System/Kernel and hardware
Summary:	Resource Group Manager
Requires(pre,post):	rpm-helper
Requires:	fence-agents
Requires:	resource-agents

%description -n rgmanager
Resource Group Manager.

%files -n rgmanager
%{_initrddir}/rgmanager
%{_sbindir}/clu*
%{_sbindir}/rgmanager
%{_sbindir}/rg_test
%{_datadir}/cluster
%{_mandir}/man8/clu*.8.*
%{_mandir}/man8/rgmanager.8.*

%post -n rgmanager
%_post_service rgmanager

%preun -n rgmanager
%_preun_service rgmanager

#----------------------------------------------------------------------------

%if 0
%package -n gfs-utils
Group:		System/Kernel and hardware
Summary:	Global Filesystem Utilities
Requires:	gfs2-utils
Requires(pre,post):	rpm-helper

%description -n gfs-utils
Global Filesystem Utilities.

%files -n gfs-utils
/sbin/*.gfs
%{_sbindir}/gfs_*
%exclude %{_sbindir}/gfs_controld
%{_initrddir}/gfs
%{_mandir}/man8/gfs_*.8.*
%{_mandir}/man8/*gfs.8.*

%post -n gfs-utils
%_post_service gfs

%preun -n gfs-utils
%_preun_service gfs
%endif

#----------------------------------------------------------------------------

%package -n gfs2-utils
Group:		System/Kernel and hardware
Summary:	Global Filesystem Utilities
Requires:	kmod(gfs2)
Requires(pre,post):	rpm-helper

%description -n gfs2-utils
Global Filesystem Utilities.

%files -n gfs2-utils
/sbin/*.gfs2
%{_sbindir}/gfs2_*
%{_initrddir}/gfs2
%{_mandir}/man8/*gfs2*.8.*

%post -n gfs2-utils
%_post_service gfs

%preun -n gfs2-utils
%_preun_service gfs2

#----------------------------------------------------------------------------

%if %{build_gnbd}
%package -n gnbd
Group:		System/Kernel and hardware
Summary:	Global Network Block Device utilities
Requires:	kmod(gnbd)

%description -n gnbd
Global Network Block Device utilities.

%files -n gnbd
%{_sbindir}/gnbd_*
%{_mandir}/man8/gnbd*.8.*
%endif

#----------------------------------------------------------------------------

%prep
%setup -q
%patch2 -p1 -b .shouldstartclvmd
cp Makefile Makefile.make

%build
./configure \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir} \
	--incdir=%{_includedir} \
	--nssincdir=%{_includedir}/nss \
	--nsprincdir=%{_includedir}/nspr4 \
	--without_fence_agents \
	--without_resource_agents \
	--without_kernel_modules \
	--disable_kernel_check

#Fixing some weird harcoded path
perl -pi -e 's|-DPLUGINDIR=\\\"\$\{plugindir\}\\\"|-DPLUGINDIR=\\"%{_libdir}/magma\\"|g' magma/lib/Makefile
perl -pi -e 's|-DPLUGINDIR=\\\"\$\{plugindir\}\\\"|-DPLUGINDIR=\\"%{_libdir}/magma\\"|g' magma/tests/Makefile

make

%install
mkdir -p %{buildroot}/%{_mandir}
mkdir -p %{buildroot}/%{_datadir}/%{name}-%{version}
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}/%{_includedir}
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/etc/cluster

#BEGIN OF DKMS PART
%if %{build_gnbd}
mkdir -p %{buildroot}/usr/src/%{module_name}-%{version}-%{release}
#cp -a gnbd-kernel/src/* %{buildroot}/usr/src/%{module_name}-%{version}-%{release}
cat > %{buildroot}/usr/src/%{module_name}-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_VERSION="%{version}-%{release}"
# Items below here should not have to change with each driver version
PACKAGE_NAME="%{module_name}"
MAKE[0]="make -C \${kernel_source_dir} M=\${dkms_tree}/\${PACKAGE_NAME}/\${PACKAGE_VERSION}/build KERNELRELEASE=\${kernelver} USING_KBUILD=yes modules"
CLEAN="make -C \${kernel_source_dir} M=\${dkms_tree}/\${PACKAGE_NAME}/\${PACKAGE_VERSION}/build KERNELRELEASE=\${kernelver} USING_KBUILD=yes clean"

BUILT_MODULE_NAME[0]="gnbd"
BUILT_MODULE_LOCATION[0]=""
DEST_MODULE_NAME[0]="gnbd"
DEST_MODULE_LOCATION[0]="/kernel/drivers/block/gnbd/"

REMAKE_INITRD="no"
AUTOINSTALL=yes
POST_INSTALL="post-install"
POST_REMOVE="post-remove"
EOF
%endif

# GFS driver
mkdir -p %{buildroot}/usr/src/gfs-%{version}-%{release}/patches
cp -a gfs-kernel/src/* %{buildroot}/usr/src/gfs-%{version}-%{release}
install -m644 %{SOURCE1} %{buildroot}/usr/src/gfs-%{version}-%{release}/patches
cat > %{buildroot}/usr/src/gfs-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_VERSION="%{version}-%{release}"
# Items below here should not have to change with each driver version
PACKAGE_NAME="gfs"
MAKE[0]="make -C \${kernel_source_dir} M=\${dkms_tree}/\${PACKAGE_NAME}/\${PACKAGE_VERSION}/build/gfs KERNELRELEASE=\${kernelver} USING_KBUILD=yes modules"
CLEAN="make -C \${kernel_source_dir} M=\${dkms_tree}/\${PACKAGE_NAME}/\${PACKAGE_VERSION}/build/gfs KERNELRELEASE=\${kernelver} USING_KBUILD=yes clean"

PATCH[0]=gfs-2.6.18-2.6.23.patch
PATCH_MATCH[0]="^2.6.(1[8-9]|2[0-3])"

BUILT_MODULE_NAME[0]="gfs"
BUILT_MODULE_LOCATION[0]="gfs"
DEST_MODULE_NAME[0]="gfs"
DEST_MODULE_LOCATION[0]="/kernel/drivers/block/gfs/"
BUILD_EXCLUSIVE_KERNEL="^2.6.(1[0-9]|2[0-3])"

REMAKE_INITRD="no"
AUTOINSTALL=yes
POST_INSTALL="post-install"
POST_REMOVE="post-remove"
EOF
# END OF DKMS STUFF

#BEGIN OF MAIN RPM
perl -pi -e 's/BUILDDIR =.*/BUILDDIR =\$\{RPM_BUILD_ROOT\}/' Makefile
%makeinstall_std
mkdir -p %{buildroot}/%{_initrddir}
mv %{buildroot}/%{_sysconfdir}/init.d/* %{buildroot}/%{_initrddir}
mv %{buildroot}/usr/libexec/* %{buildroot}/%{_libdir}
rm -f %{buildroot}%{_libdir}/*.a
chmod +x %{buildroot}%{_libdir}/lcrso/*.lcrso
chmod +x %{buildroot}%{_libdir}/*.so.*

