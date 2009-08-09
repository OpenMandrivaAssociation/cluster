%define name	cluster
%define module_name gnbd
%define major   2
%define version 2.03.11
%define release %mkrel 3
%define cmanlibname %mklibname cman %major 
%define cmanlibnamedevel %mklibname -d cman
%define dlmlibname %mklibname dlm %major 
%define dlmlibnamedevel %mklibname -d dlm
%define _requires_exceptions perl\(VMware::VmPerl

Name:		%name
Version:	%{version}
Release:	%{release}
Summary:	Redhat suite for clustered filesystems
License:	GPL
Source:		ftp://sources.redhat.com/pub/cluster/releases/%{name}-%{version}.tar.gz
Source1:	gfs-2.6.18-2.6.23.patch

# Remove apc_snmp, as its compilation is broken
Patch: cluster-2.03.07-fix-cman-init.patch
Patch1: cluster-2.03.07-kernel-2.6.25.patch
Patch2: cluster-2.03.11-gfs-should-start-clvmd.patch

Url:		ftp://sources.redhat.com/pub/cluster/releases/
Group:		System/Kernel and hardware
Buildroot:	%{_tmppath}/%{name}-%{version}-root
Buildrequires:	libxml2-devel
BuildRequires:	openais-devel
BuildRequires:	volume_id-devel
BuildRequires:	slang-devel
BuildRequires:	ncurses-devel
BuildRequires:	libvirt-devel
# For fence_xvm
BuildRequires:	nss-devel
#Requires:	%{libname}
Requires:	gfs-utils cman rgmanager

%description
Redhat suite for clustered filesystems

%package -n     %{cmanlibname}
Summary:        Shared Librairies for Cluster Manager
Group:          Development/Other

%description  -n %{cmanlibname}
Shared Librairies for Cluster Manager

%package -n %{cmanlibnamedevel}
Summary:        Cluster Manager header files and static libraries
Group:          Development/Other
Requires:       %{cmanlibname} = %{version}
Provides:	cman-devel = %{version}

%description -n %{cmanlibnamedevel}
This package contains header files and static libraries.

%package -n     %{dlmlibname}
Summary:        Shared Librairies for the Distributed Lock Manager
Group:          Development/Other

%description  -n %{dlmlibname}
Shared Librairies for cluster

%package devel
Summary:        Cluster Manager header files and static libraries
Group:          Development/Other
Requires:	dlm-devel cman-devel

%description devel
Cluster Manager header files and static libraries

%package -n %{dlmlibnamedevel}
Summary:        Distributed Lock Manager header files and static libraries
Group:          Development/Other
Requires:       %{dlmlibname} = %{version}
Provides:	dlm-devel = %{version}

%description -n %{dlmlibnamedevel}
This package contains header files and static libraries.


%package -n dkms-%{module_name}
Summary:	Redhat's cluster suite kernel modules
Group:          System/Kernel and hardware
Requires(pre):  dkms
Requires(post): dkms

%description -n dkms-%{module_name}
The dynamic kernel modules

%package -n dkms-gfs
Summary:	Global File System Kernel Driver
Group:          System/Kernel and hardware
Requires(pre):  dkms
Requires(post): dkms

%description -n dkms-gfs
The dynamic kernel module package for Global File System

This package is only required for kernels older than 2.6.24
(newer kernels ship with a gfs driver)

%package -n cman
Group:		System/Kernel and hardware
Summary:	Cluster Manager
Requires:	openais libxml2-utils
Requires(pre):		rpm-helper
Requires(post):		rpm-helper

%description -n cman
Cluster Manager

%package -n rgmanager
Group:		System/Kernel and hardware
Summary:	Resource Group Manager
Requires(pre):		rpm-helper
Requires(post):		rpm-helper

%description -n rgmanager
Resource Group Manager


%package -n gfs-utils
Group:		System/Kernel and hardware
Summary:	Global Filesystem Utilities
Requires:	gfs2-utils
Requires(pre):		rpm-helper
Requires(post):		rpm-helper

%description -n gfs-utils
Global Filesystem Utilities

%package -n gfs2-utils
Group:		System/Kernel and hardware
Summary:	Global Filesystem Utilities
Requires:	kmod(gfs2)
Requires(pre):		rpm-helper
Requires(post):		rpm-helper

%description -n gfs2-utils
Global Filesystem Utilities

%package -n gnbd
Group:		System/Kernel and hardware
Summary:	Global Network Block Device utilities
Requires:	kmod(gnbd)

%description -n gnbd
Global Network Block Device utilities

%prep
%setup -q -n %{name}-%{version}
%patch -p1 -b .orig
%patch2 -p1 -b .shouldstartclvmd
%if %mdkversion <= 200810
%patch1 -p1 -b .kernel2625
%endif
cp Makefile Makefile.make

%build

./configure \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir} \
	--incdir=%{_includedir} \
	--without_kernel_modules \
	--disable_kernel_check \
	--nssincdir=%{_includedir}/nss \
	--nsprincdir=%{_includedir}/nspr4 \
	--enable_xen
#--kernel_src=/usr/src/linux \

#Fixing some weird harcoded path
perl -pi -e 's|-DPLUGINDIR=\\\"\$\{plugindir\}\\\"|-DPLUGINDIR=\\"%{_libdir}/magma\\"|g' magma/lib/Makefile
perl -pi -e 's|-DPLUGINDIR=\\\"\$\{plugindir\}\\\"|-DPLUGINDIR=\\"%{_libdir}/magma\\"|g' magma/tests/Makefile

make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_mandir}
mkdir -p %{buildroot}/%{_datadir}/%{name}-%{version}
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}/%{_includedir}
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/etc/cluster

#BEGIN OF DKMS PART
mkdir -p %{buildroot}/usr/src/%{module_name}-%{version}-%{release}
cp -a gnbd-kernel/src/* %{buildroot}/usr/src/%{module_name}-%{version}-%{release}
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

%clean
rm -rf $RPM_BUILD_ROOT

%post -n dkms-%{module_name}
dkms add -m %{module_name} -v %{version}-%{release} --rpm_safe_upgrade
dkms build -m %{module_name} -v %{version}-%{release} --rpm_safe_upgrade
dkms install -m %{module_name} -v %{version}-%{release} --rpm_safe_upgrade

%preun -n dkms-%{module_name}
dkms remove -m %{module_name} -v %{version}-%{release} --rpm_safe_upgrade --all ||:

%post -n dkms-gfs
dkms add -m gfs -v %{version}-%{release} --rpm_safe_upgrade
dkms build -m gfs -v %{version}-%{release} --rpm_safe_upgrade
dkms install -m gfs -v %{version}-%{release} --rpm_safe_upgrade

%preun -n dkms-gfs
dkms remove -m gfs -v %{version}-%{release} --rpm_safe_upgrade --all ||:

%post -n rgmanager
%_post_service rgmanager

%preun -n rgmanager
%_preun_service rgmanager

%post -n cman
%_post_service cman
%_post_service qdiskd
%_post_service scsi_reserve

%preun -n cman
%_preun_service cman
%_preun_service qdiskd
%_preun_service scsi_reserve

%post -n gfs-utils
%_post_service gfs

%preun -n gfs-utils
%_preun_service gfs

%post -n gfs2-utils
%_post_service gfs

%preun -n gfs2-utils
%_preun_service gfs2

%if %mdkversion < 200900
%post -n %{dlmlibname} -p /sbin/ldconfig
%post -n %{cmanlibname} -p /sbin/ldconfig
%postun -n %{dlmlibname} -p /sbin/ldconfig
%postun -n %{cmanlibname} -p /sbin/ldconfig
%endif

%files -n dkms-%{module_name}
%defattr(-,root,root)
%_usrsrc/%{module_name}-%{version}-%{release}

%files -n dkms-gfs
%defattr(-,root,root)
%_usrsrc/gfs-%{version}-%{release}

%files -n %{cmanlibnamedevel}
%defattr(-,root,root)
%{_libdir}/*cman*.a
%{_libdir}/*cman.so
%{_includedir}/libcman.h

%files -n %{dlmlibnamedevel}
%defattr(-,root,root)
%{_libdir}/*dlm*.a
%{_libdir}/*dlm*.so
%{_mandir}/man3/*dlm*.3.*
%{_includedir}/libdlm.h

%files -n %{cmanlibname}
%defattr(-,root,root)
%{_libdir}/*cman.so.%{major}*

%files -n %{dlmlibname}
%defattr(-,root,root)
%{_libdir}/*dlm*.so.%{major}*

%files devel
%defattr(-,root,root)
%{_datadir}/doc/%name
%exclude %{_includedir}/ccs.h
%exclude %{_libdir}/libccs.a

%files -n rgmanager
%defattr(-,root,root)
%{_initrddir}/rgmanager
%{_sbindir}/clu*
%{_sbindir}/rg_test
%{_datadir}/cluster
%{_mandir}/man8/clu*.8.*

%files -n cman
%defattr(-,root,root)
%{_initrddir}/cman
%{_initrddir}/qdiskd
%{_initrddir}/scsi_reserve
%{_sbindir}/cman*
%{_sbindir}/fence*
%{_sbindir}/dlm*
%{_sbindir}/ccs*
%{_sbindir}/group*
%{_sbindir}/*qdisk*
%{_sbindir}/gfs_controld
%dir /etc/cluster
%attr(0755,root,root) %{_datadir}/fence
%{_datadir}/snmp/mibs/*.mib
%{_libdir}/lcrso/service_cman.lcrso
%config/etc/udev/rules.d/51-dlm.rules
%{_mandir}/man8/cman*.8.*
%{_mandir}/man5/cman.5.*
%{_mandir}/man5/cluster.conf.5.*
%{_mandir}/man5/qdisk.5.*
%{_mandir}/man8/fence*.8.*
%{_mandir}/man8/dlm*.8.*
%{_mandir}/man8/ccs*.8.*
%{_mandir}/man7/ccs.7.*
%{_mandir}/man8/*group*.8.*
%{_mandir}/man8/*qdisk*.8.*

%files -n gfs-utils
%defattr(-,root,root)
/sbin/*.gfs
%{_sbindir}/*.gfs
%{_sbindir}/gfs_*
%exclude %{_sbindir}/gfs_controld
%{_initrddir}/gfs
%{_mandir}/man8/gfs_*.8.*
%{_mandir}/man8/gfs.8.*

%files -n gfs2-utils
%defattr(-,root,root)
%{_sbindir}/*.gfs2
/sbin/*.gfs2
%{_sbindir}/gfs2_*
%{_initrddir}/gfs2
%{_mandir}/man8/*gfs2*.8.*

%files -n gnbd
%defattr(-,root,root)
%{_sbindir}/gnbd_*
%{_mandir}/man8/gnbd*.8.*
