#
# TODO:
#		- remove from cvs when 2.6.27@kernel.spec will be ready.
#		http://lwn.net/Articles/291630/
#
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%define		mISDN_version		%(echo %{version} |tr . _)

%define		rel	9
Summary:	mISDN - modular ISDN
Summary(pl.UTF-8):	mISDN - modularny ISDN
Name:		mISDN
Version:	1.1.8
Release:	%{rel}
Epoch:		1
License:	GPL
Group:		Base/Kernel
Source0:	http://www.misdn.org/downloads/releases/%{name}-%{mISDN_version}.tar.gz
# Source0-md5:	29c55ffe0b35668a41eaed3b1c3ddfe2
URL:		http://www.misdn.org/
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.332
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mISDN (modular ISDN) is the new ISDN stack of the Linux kernel version
2.6.

%description -l pl.UTF-8
mISDN (modularny ISDN) to nowy stos ISDN dla jądra Linuksa w wersji
2.6.

%package init
Summary:	init scripts for mISDN
Summary(pl.UTF-8): Skrypty inicjalizujące dla mISDN
Group:		Applications/Communications
Requires:	bc
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Requires:	which

%description init
mISDN boot-time initialization.

%description init -l pl.UTF-8
Inicjalizacja mISDN w czasie startu systemu.

%package -n kernel%{_alt_kernel}-isdn-mISDN
Summary:	Linux driver for mISDN
Summary(pl.UTF-8):	Sterownik dla Linuksa do mISDN
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(mISDN)

%description -n kernel%{_alt_kernel}-isdn-mISDN
This is driver for mISDN for Linux.

This package contains Linux module.

%description -n kernel%{_alt_kernel}-isdn-mISDN -l pl.UTF-8
Sterownik dla Linuksa do mISDN.

Ten pakiet zawiera moduł jądra Linuksa.

%package devel
Summary:	Development header files for mISDN
Summary(pl.UTF-8):	Pliki nagłówkowe mISDN
Group:		Development/Libraries

%description devel
Development header files for mISDN.

%description devel -l pl.UTF-8
Pliki nagłówkowe mISDN.

%prep
%setup -q -n %{name}-%{mISDN_version}

%build
cp -r include/linux drivers/isdn/hardware/mISDN/

sed s/CONFIG_MISDN_MEMDEBUG=y//g add.config > drivers/isdn/hardware/mISDN/Makefile
echo "CONFIG_MISDN_NETJET=y" >> drivers/isdn/hardware/mISDN/Makefile
echo "CONFIG_MISDN_HFCUSB=y" >> drivers/isdn/hardware/mISDN/Makefile
echo "CONFIG_MISDN_HFCMINI=y" >> drivers/isdn/hardware/mISDN/Makefile
%ifnarch hppa mips ppc ppc64 s390 s390x sparc sparc64
echo "CONFIG_MISDN_HFCMULTI=y" >> drivers/isdn/hardware/mISDN/Makefile
%endif
echo "CONFIG_MISDN_XHFC=y" >> drivers/isdn/hardware/mISDN/Makefile
echo "CONFIG_MISDN_DSP=y" >> drivers/isdn/hardware/mISDN/Makefile
echo "CONFIG_MISDN_LOOP=y" >> drivers/isdn/hardware/mISDN/Makefile

sed -e 's#$(.*)#m#g' drivers/isdn/hardware/mISDN/Makefile.v2.6 >> drivers/isdn/hardware/mISDN/Makefile
%build_kernel_modules -m l3udss1,mISDN_capi,mISDN_core,mISDN_dtmf,mISDN_x25dte,mISDN_isac,mISDN_l1,mISDN_l2,avmfritz,netjetpci,hfcpci,hfcsusb,hfcsmini,sedlfax,w6692pci,xhfc,mISDN_dsp,mISDN_loop -C drivers/isdn/hardware/mISDN/

%ifnarch hppa mips ppc ppc64 s390 s390x sparc sparc64
%build_kernel_modules -m hfcmulti -C drivers/isdn/hardware/mISDN/
%endif

%install
rm -rf $RPM_BUILD_ROOT

# init files
install -d $RPM_BUILD_ROOT{%{_bindir},/etc/rc.d/init.d}
install std2kern stddiff $RPM_BUILD_ROOT%{_bindir}
install misdn-init $RPM_BUILD_ROOT/etc/rc.d/init.d

# devel files
install -d $RPM_BUILD_ROOT%{_includedir}/linux
install include/linux/*.h $RPM_BUILD_ROOT%{_includedir}/linux

# kernel modules
cd drivers/isdn/hardware/mISDN
sep="%{?with_dist_kernel:dist}%{!?with_dist_kernel:nondist}"
mods=$(echo *-${sep}.ko | sed -e "s#-${sep}.ko##g" -e 's# #,#g')
%install_kernel_modules -m $mods -d kernel/drivers/isdn/hardware/mISDN

%clean
rm -rf $RPM_BUILD_ROOT

%post init
/sbin/chkconfig --add misdn-init
%service misdn-init restart

%preun init
if [ "$1" = "0" ]; then
	%service misdn-init stop
	/sbin/chkconfig --del misdn-init
fi

%post	-n kernel%{_alt_kernel}-isdn-mISDN
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-isdn-mISDN
%depmod %{_kernel_ver}

%files init
%defattr(644,root,root,755)
%doc README.misdn-init
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(755,root,root) %{_bindir}/*

%files -n kernel%{_alt_kernel}-isdn-mISDN
%defattr(644,root,root,755)
%dir /lib/modules/%{_kernel_ver}/kernel/drivers/isdn/hardware/mISDN
/lib/modules/%{_kernel_ver}/kernel/drivers/isdn/hardware/mISDN/*.ko*

%files devel
%defattr(644,root,root,755)
%{_includedir}/linux/*.h
