%define name vrb
%define version 0.5.0
%define release %mkrel 1
%define major 0
%define libname %mklibname %name %major

Summary: The Virtual Ring Buffer (VRB)
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://vrb.slashusr.org/%{name}-%{version}.tar.bz2
Patch1: vrb-0.5.0-gcc-opt.patch
License: LGPL
Group: System/Libraries
Url: http://vrb.slashusr.org/

%description
The Virtual Ring Buffer (VRB) is an implementation of a character FIFO
ring buffer. It provides direct access to the buffer so the calling
program can construct output data in place, or parse input data in place,
without the extra step of copying data to or from a calling program
provided buffer area.

%package -n %libname
Summary: The Virtual Ring Buffer (VRB) library
Group: System/Libraries
Provides: lib%name = %version-%release

%description -n %libname
The Virtual Ring Buffer (VRB) is an implementation of a character FIFO
ring buffer. It provides direct access to the buffer so the calling
program can construct output data in place, or parse input data in place,
without the extra step of copying data to or from a calling program
provided buffer area.

%package -n %libname-devel
Summary: The Virtual Ring Buffer (VRB) development files
Group: Development/Other
Provides: lib%name-devel = %version-%release
Requires: %libname = %version-%release

%description -n %libname-devel
The Virtual Ring Buffer (VRB) is an implementation of a character FIFO
ring buffer. It provides direct access to the buffer so the calling
program can construct output data in place, or parse input data in place,
without the extra step of copying data to or from a calling program
provided buffer area.

%prep
%setup -q
%patch1 -p0

%build
echo %optflags > Compile.opt
./configure --prefix=%buildroot/usr

# Don't try %make - This makefile is ugly
make

# We need to rebuild vrb against a clean lib
#rm -f lib/libvrb.so
#rm -f bin/vbuf
#make build_pgm 

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

if [ "%_lib" != "lib" ]; then
  mv %buildroot/%_prefix/lib %buildroot%_libdir
fi

mkdir -p %buildroot%_mandir/man3
cp -p vrb/man/man3/*.3 %buildroot%_mandir/man3

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %libname -p  /sbin/ldconfig

%postun -n %libname -p  /sbin/ldconfig

%files
%defattr(-,root,root)
%_bindir/*
%_mandir/man3/*

%files -n %libname
%defattr(-,root,root)
%_libdir/*.so.*

%files -n %libname-devel
%defattr(-,root,root)
%_libdir/*.so
%_libdir/*.a*
%_includedir/*.h

