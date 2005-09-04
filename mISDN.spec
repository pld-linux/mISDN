#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%define		mISDN_version		CVS-2005-07-06

Summary:	mISDN - modular ISDN
Summary(pl):	mISDN - modularny ISDN
Name:		mISDN
Version:	2005.07.06
%define		_rel	0.1
Release:	%{_rel}
License:	GPL
Group:		Base/Kernel
Source0: 	ftp://ftp.isdn4linux.de/pub/isdn4linux/CVS-Snapshots/%{name}-%{mISDN_version}.tar.bz2
# Source0-md5:	f8892d49e00e3fa26e65e22084edd472
URL:		http://www.isdn4linux.de/mISDN/
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.217
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mISDN (modular ISDN) is the new ISDN stack of the Linux kernel version
2.6.

%description -l pl
mISDN (modularny ISDN) to nowy stos ISDN dla j±dra Linuksa w wersji
2.6.

%package -n kernel-isdn-mISDN
Summary:	Linux driver for mISDN
Summary(pl):	Sterownik dla Linuksa do mISDN
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif

%description -n kernel-isdn-mISDN
This is driver for mISDN for Linux.

This package contains Linux module.

%description -n kernel-isdn-mISDN -l pl
Sterownik dla Linuksa do mISDN.

Ten pakiet zawiera modu³ j±dra Linuksa.

%package -n kernel-smp-isdn-mISDN
Summary:	Linux SMP driver for mISDN
Summary(pl):	Sterownik dla Linuksa SMP do mISDN
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel-smp-isdn-mISDN
This is driver for mISDN for Linux.

This package contains Linux SMP module.

%description -n kernel-smp-isdn-mISDN -l pl
Sterownik dla Linuksa do mISDN.

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%package devel
Summary:	Development header files for mISDN
Summary(pl):	Pliki nag³ówkowe mISDN
Group:		Development/Libraries

%description devel
Development header files for mISDN.

%description devel -l pl
Pliki nag³ówkowe mISDN.

%prep
%setup -q -n %{name}-%{mISDN_version}

%build
cd drivers/isdn/hardware/mISDN
sed -e 's#$(.*)#m#g' Makefile.v2.6 > Makefile

for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
	cp -a ../../../../include/linux/*.h include/linux
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	touch include/config/MARKER

	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}

	for mod in *.ko; do
		m=$(echo "$mod" | sed -e 's#.ko##g')
		mv ${m}.ko ../${m}-${cfg}.ko
	done
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_includedir}/linux
install include/linux/*.h $RPM_BUILD_ROOT%{_includedir}/linux

cd drivers/isdn/hardware
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/drivers/isdn/hardware/mISDN

sep="%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}"
for mod in *-${sep}.ko; do
	m=$(echo "$mod" | sed -e "s#-${sep}.ko##g")
	install "$mod" $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/drivers/isdn/hardware/mISDN/${m}.ko
done

%if %{with smp} && %{with dist_kernel}
for mod in *-smp.ko; do
	m=$(echo "$mod" | sed -e 's#-smp.ko##g')
	install "$mod" $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/drivers/isdn/hardware/mISDN/${m}.ko
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-isdn-mISDN
%depmod %{_kernel_ver}

%postun	-n kernel-isdn-mISDN
%depmod %{_kernel_ver}

%post	-n kernel-smp-isdn-mISDN
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-isdn-mISDN
%depmod %{_kernel_ver}smp

%files -n kernel-isdn-mISDN
%defattr(644,root,root,755)
%dir /lib/modules/%{_kernel_ver}/drivers/isdn/hardware/mISDN
/lib/modules/%{_kernel_ver}/drivers/isdn/hardware/mISDN/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-isdn-mISDN
%defattr(644,root,root,755)
%dir /lib/modules/%{_kernel_ver}smp/drivers/isdn/hardware/mISDN
/lib/modules/%{_kernel_ver}smp/drivers/isdn/hardware/mISDN/*.ko*
%endif

%files devel
%defattr(644,root,root,755)
%{_includedir}/linux/*.h
