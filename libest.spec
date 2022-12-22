# %%global _prefix /opt

Name:           libest
Version:        3.2.0
Release:        1%{?dist}
Summary:        EST stack written in C

License:        LGPLv2+
URL:            https://github.com/dogtagpki/libest
Source:         https://github.com/dogtagpki/%{name}/archive/v%{version}-pki/%{name}-%{version}-pki.tar.gz

BuildRequires: gcc
BuildRequires: make
BuildRequires: autoconf automake libtool
BuildRequires: openssl-devel
%description
libest project is an EST stack written in C.
EST is used for secure certificate enrollment and is compatible
with Suite B certs (as well as RSA and DSA certificates).
EST is a suitable replacement for SCEP.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The package contains libraries and header files for
developing applications that use libest.

%prep
%setup -n libest-%{version}-pki

%build
%configure --disable-safec
V=1 make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.{a,la}
mkdir -p %{buildroot}/%{_docdir}/%{name}/example
find . -type f \( -name "*.c*" -o -name "*.h*" -o -name "*.o" -o -name "estserver" -o -name "Makefile*" \) | xargs rm -rf
cp -r %{_builddir}/%{name}-%{version}-pki/example/server %{buildroot}/%{_docdir}/%{name}/example

%ldconfig_scriptlets

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README AUTHORS
%docdir %{_docdir}/%{name}/example/server
%doc %{_docdir}/%{name}/example/server
%exclude %{_docdir}/%{name}/example/server/.libs
%{_libdir}/lib*.so
%{_bindir}/est*

%files devel
%{_includedir}/est/est.h

%changelog
* Fri Jul 29 2022 Viktor Ashirov <vashirov@redhat.com> - 3.2.0-1
- Initial release libest-3.2.0
