#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%define		mISDN_version		%(echo %{version} |tr . _)

%define		_rel	1
Summary:	mISDN - modular ISDN
Summary(pl.UTF-8):	mISDN - modularny ISDN
Name:		mISDN
Version:	1.1.7
Release:	%{_rel}
Epoch:		1
License:	GPL
Group:		Base/Kernel
Source0:	http://www.misdn.org/downloads/releases/%{name}-%{mISDN_version}.tar.gz
# Source0-md5:	6f502c8131e3e3a159c72214e0a933bc
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

%package -n kernel-isdn-mISDN
Summary:	Linux driver for mISDN
Summary(pl.UTF-8):	Sterownik dla Linuksa do mISDN
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(mISDN)

%description -n kernel-isdn-mISDN
This is driver for mISDN for Linux.

This package contains Linux module.

%description -n kernel-isdn-mISDN -l pl.UTF-8
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

install -d $RPM_BUILD_ROOT%{_includedir}/linux
install include/linux/*.h $RPM_BUILD_ROOT%{_includedir}/linux

cd drivers/isdn/hardware/mISDN
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/drivers/isdn/hardware/mISDN

sep="%{?with_dist_kernel:dist}%{!?with_dist_kernel:nondist}"
for mod in *-${sep}.ko; do
	m=$(echo "$mod" | sed -e "s#-${sep}.ko##g")
	install "$mod" $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/drivers/isdn/hardware/mISDN/${m}.ko
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-isdn-mISDN
%depmod %{_kernel_ver}

%postun	-n kernel-isdn-mISDN
%depmod %{_kernel_ver}

%files -n kernel-isdn-mISDN
%defattr(644,root,root,755)
%dir /lib/modules/%{_kernel_ver}/drivers/isdn/hardware/mISDN
/lib/modules/%{_kernel_ver}/drivers/isdn/hardware/mISDN/*.ko*

%files devel
%defattr(644,root,root,755)
%{_includedir}/linux/*.h
