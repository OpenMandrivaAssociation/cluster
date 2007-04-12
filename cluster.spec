%define name	cluster
%define module_name dkms-cluster
%define major   1
%define version 1.03.00
%define release %mkrel 2
%define libname %mklibname %name %major 

Name:		%name
Version:	%{version}
Release:	%{release}
Summary:	Redhat suite for clustered filesystems
License:	GPL
Source:		ftp://sources.redhat.com/pub/cluster/releases/%{name}-%{version}.tar.gz

# Remove apc_snmp, as its compilation is broken
Patch1: cluster-1.02.99-nosnmp.patch
Patch2: cluster-1.03.00-lccs.patch
# gw trim dkms build system
Patch3: dkms-cluster-1.03.00-dkms.patch
Url:		ftp://sources.redhat.com/pub/cluster/releases/
Group:		System/Kernel and hardware
Buildroot:	%{_tmppath}/%{name}-%{version}-root
Buildrequires:	libxml2-devel, kernel-source
Requires:	%{libname}
Conflicts:	gfs, gfs-kernel,ccs,cman,cman-kernel,dlm,dlm-kernel,fence,gulm,magma,magma-plugins,rgmanager
Requires(pre):		rpm-helper
Requires(post):		rpm-helper

%description
Redhat suite for clustered filesystems

%package -n     %{libname}
Summary:        Shared Librairies for GFS
Group:          Development/Other

%description  -n %{libname}
Shared Librairies for cluster

%package -n %{name}-devel
Summary:        GFS header files and static libraries
Group:          Development/Other
Requires:       %{name} = %{version}
Requires:       %{libname} = %{version}

%description -n %{name}-devel
This package contains header files and static libraries.


%package -n %{module_name}
Summary:	Redhat's cluster suite kernel modules
Group:          System/Kernel and Hardware
Requires(pre):  dkms
Requires(post): dkms

%description -n %{module_name}
The dynamic kernel modules

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
%patch2 -p1 -b .lccs
cp Makefile Makefile.make

%build

./configure --kernel_src=/usr/src/linux \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir} \
	--incdir=%{_includedir}

#Fixing some weird harcoded path
perl -pi -e 's|-DPLUGINDIR=\\\"\$\{plugindir\}\\\"|-DPLUGINDIR=\\"%{_libdir}/magma\\"|g' magma/lib/Makefile
perl -pi -e 's|-DPLUGINDIR=\\\"\$\{plugindir\}\\\"|-DPLUGINDIR=\\"%{_libdir}/magma\\"|g' magma/tests/Makefile

make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_mandir}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{version}
mkdir -p $RPM_BUILD_ROOT/%{_libdir}
mkdir -p $RPM_BUILD_ROOT/%{_includedir}
mkdir -p $RPM_BUILD_ROOT/%{_initrddir}

#BEGIN OF DKMS PART
mkdir -p %{buildroot}/usr/src/%{module_name}-%{version}
cp -a *-kernel configure %{buildroot}/usr/src/%{module_name}-%{version}
cp Makefile.make %{buildroot}/usr/src/%{module_name}-%{version}/Makefile
pushd .
cd %{buildroot}/usr/src/%{module_name}-%{version}
patch -p1 < %PATCH3
make clean
popd
cat > %{buildroot}/usr/src/%{module_name}-%{version}/dkms.conf <<EOF
PACKAGE_VERSION="%{version}"

# Items below here should not have to change with each driver version
PACKAGE_NAME="%{module_name}"
MAKE[0]="cd \${dkms_tree}/\${PACKAGE_NAME}/\${PACKAGE_VERSION}/build ; ./configure --kernel_src=\${kernel_source_dir}; make"
CLEAN="cd \${dkms_tree}/\${PACKAGE_NAME}/\${PACKAGE_VERSION}/build ; make clean"

BUILT_MODULE_NAME[0]="cman"
BUILT_MODULE_LOCATION[0]="build/module/cluster"
DEST_MODULE_NAME[0]="cman"
DEST_MODULE_LOCATION[0]="/kernel/cluster"

BUILT_MODULE_NAME[1]="dlm"
BUILT_MODULE_LOCATION[1]="build/module/cluster"
DEST_MODULE_NAME[1]="dlm"
DEST_MODULE_LOCATION[1]="/kernel/cluster"

BUILT_MODULE_NAME[2]="lock_harness"
BUILT_MODULE_LOCATION[2]="build/module/fs/gfs_locking/lock_harness"
DEST_MODULE_NAME[2]="lock_harness"
DEST_MODULE_LOCATION[2]="/kernel/fs/gfs_locking/lock_harness/"

BUILT_MODULE_NAME[3]="lock_nolock"
BUILT_MODULE_LOCATION[3]="build/module/fs/gfs_locking/lock_nolock"
DEST_MODULE_NAME[3]="lock_nolock"
DEST_MODULE_LOCATION[3]="/kernel/fs/gfs_locking/lock_nolock/"

BUILT_MODULE_NAME[4]="lock_dlm"
BUILT_MODULE_LOCATION[4]="build/module/fs/gfs_locking/lock_dlm"
DEST_MODULE_NAME[4]="lock_dlm"
DEST_MODULE_LOCATION[4]="/kernel/fs/gfs_locking/lock_dlm/"

BUILT_MODULE_NAME[5]="lock_gulm"
BUILT_MODULE_LOCATION[5]="build/module/fs/gfs_locking/lock_gulm"
DEST_MODULE_NAME[5]="lock_gulm"
DEST_MODULE_LOCATION[5]="/kernel/fs/gfs_locking/lock_gulm/"

BUILT_MODULE_NAME[6]="gfs"
BUILT_MODULE_LOCATION[6]="build/module/fs/gfs"
DEST_MODULE_NAME[6]="gfs"
DEST_MODULE_LOCATION[6]="/kernel/fs/gfs/"

BUILT_MODULE_NAME[7]="gnbd"
BUILT_MODULE_LOCATION[7]="build/module/drivers/block/gnbd/"
DEST_MODULE_NAME[7]="gnbd"
DEST_MODULE_LOCATION[7]="/kernel/drivers/block/gnbd/"

REMAKE_INITRD="no"
AUTOINSTALL=yes
POST_INSTALL="post-install"
POST_REMOVE="post-remove"
EOF
# END OF DKMS STUFF

#BEGIN OF MAIN RPM
perl -pi -e 's/BUILDDIR =.*/BUILDDIR =\$\{RPM_BUILD_ROOT\}/' Makefile
make

#Fixing some weird directory
pushd $RPM_BUILD_ROOT
mv man/* $RPM_BUILD_ROOT%{_mandir}
mv *sh $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
mv lib/* $RPM_BUILD_ROOT%{_libdir} 
mv etc/init.d/* $RPM_BUILD_ROOT/%{_initrddir}
mv incdir/* $RPM_BUILD_ROOT/%{_includedir}

#Removing unecessary files for runtime
rm -f ocf-shellfuncs
rm -f svclib_nfslock
rm -rf module
rm -rf incdir
rm -rf slib 
rm -rf lib
rm -rf man
rm -rf etc/init.d
popd
#END OF MAIN RPM

#multiarch part
%multiarch_includes $RPM_BUILD_ROOT%{_includedir}/magma-build.h
#end of multiarch part

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{module_name}
dkms add -m %{module_name} -v %{version} --rpm_safe_upgrade
dkms build -m %{module_name} -v %{version} --rpm_safe_upgrade
dkms install -m %{module_name} -v %{version} --rpm_safe_upgrade

%preun -n %{module_name}
dkms remove -m %{module_name} -v %{version} --rpm_safe_upgrade --all ||:

%post
%_post_service lock_gulmd
%_post_service fenced
%_post_service ccsd
%_post_service cman
%_post_service gfs
%_post_service rgmanager

%postun -n %{libname}
/sbin/ldconfig

%post -n %{libname}
/sbin/ldconfig


%preun
%_preun_service lock_gulmd
%_preun_service fenced
%_preun_service ccsd
%_preun_service cman
%_preun_service gfs
%_preun_service rgmanager

%files -n %{module_name}
%defattr(-,root,root)
%_usrsrc/%{module_name}-%{version}

%files -n %{name}-devel
%defattr(-,root,root)
%{_includedir}/*
%multiarch %{multiarch_includedir}/magma-build.h
%{_libdir}/*.a

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so*

%files
%defattr(-,root,root)
%{_initrddir}/ccsd
%{_initrddir}/cman
%{_initrddir}/fenced
%{_initrddir}/gfs
%{_initrddir}/lock_gulmd
%{_initrddir}/rgmanager
%{_initrddir}/qdiskd
%{_libdir}/magma
%{_datadir}/%{name}-%{version}
%{_mandir}/man?/*
/sbin/*


