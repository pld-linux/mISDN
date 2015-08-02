#
# TODO:
# - shouldn't headers be provided by 2.6.27 linux-libc-headers instead of -devel here?
#
# Conditional build:
%bcond_with	kernel		# mISDN merged in 2.6.27, needs update if needed
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%if %{without kernel}
%undefine       with_dist_kernel
%endif
#
%define		rel	1
Summary:	mISDN - modular ISDN
Summary(pl.UTF-8):	mISDN - modularny ISDN
Name:		mISDN
Version:	2.0.35
Release:	%{rel}
Epoch:		1
License:	GPL v2+
Group:		Base/Kernel
# git clone git://git.misdn.eu/mISDN.git
# git archive --format=tar --prefix=mISDN-2.0.35/ v2.0.35 | xz > ../mISDN-2.0.35.tar.xz
Source0:	%{name}-%{version}.tar.xz
# Source0-md5:	2c35bb1b3ebfaf40914360f5328d134d
URL:		https://www.misdn.eu/wiki/Main_Page
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.332
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mISDN (modular ISDN) is the new ISDN stack of the Linux kernel version
2.6+.

%description -l pl.UTF-8
mISDN (modularny ISDN) to nowy stos ISDN dla jądra Linuksa w wersji
2.6 i nowszych.

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
%setup -q

%build
%if %{with kernel}
%configure
cp mISDN.cfg.default standalone/mISDN.cfg

# insufficient, needs update?
cp -r include/linux drivers/isdn/hardware/mISDN/

%build_kernel_modules -m l3udss1,mISDN_capi,mISDN_core,mISDN_dtmf,mISDN_x25dte,mISDN_isac,mISDN_l1,mISDN_l2,avmfritz,netjetpci,hfcpci,hfcsusb,hfcsmini,sedlfax,w6692pci,xhfc,mISDN_dsp,mISDN_loop -C drivers/isdn/hardware/mISDN/

%ifnarch hppa mips ppc ppc64 s390 s390x sparc sparc64
%build_kernel_modules -m hfcmulti -C drivers/isdn/hardware/mISDN/
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

# devel files
install -d $RPM_BUILD_ROOT%{_includedir}/linux
install include/linux/*.h $RPM_BUILD_ROOT%{_includedir}/linux

%if %{with kernel}
# kernel modules
cd drivers/isdn/hardware/mISDN
sep="%{?with_dist_kernel:dist}%{!?with_dist_kernel:nondist}"
mods=$(echo *-${sep}.ko | sed -e "s#-${sep}.ko##g" -e 's# #,#g')
%install_kernel_modules -m $mods -d kernel/drivers/isdn/hardware/mISDN
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-isdn-mISDN
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-isdn-mISDN
%depmod %{_kernel_ver}

%if %{with kernel}
%files -n kernel%{_alt_kernel}-isdn-mISDN
%defattr(644,root,root,755)
%dir /lib/modules/%{_kernel_ver}/kernel/drivers/isdn/hardware/mISDN
/lib/modules/%{_kernel_ver}/kernel/drivers/isdn/hardware/mISDN/*.ko*
%endif

%files devel
%defattr(644,root,root,755)
%{_includedir}/linux/mISDNdsp.h
%{_includedir}/linux/mISDNhw.h
%{_includedir}/linux/mISDNif.h
