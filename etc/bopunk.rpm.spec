Summary: BoPunk gaphical firmware management application. 
Name: bopunk
Version: 0.4
Release: 1
Copyright: GPL
Group: Hardware/Other
BuildRoot: /var/tmp/%{name}-buildroot

%description
The BoPunk gui application allows users to browse for firmwares to downlod
and use for their device. Users can also download and upload firmware files
from and to the device. The Firmware tab allows users to adjust device 
variables. 

%prep
%setup 
%patch 

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/local/
mkdir -p $RPM_BUILD_ROOT/usr/local/lib/
mkdir -p $RPM_BUILD_ROOT/usr/local/bin/

install -s -m 755 eject $RPM_BUILD_ROOT/usr/bin/eject
install -m 644 eject.1 $RPM_BUILD_ROOT/usr/man/man1/eject.1 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README TODO COPYING ChangeLog

/usr/bin/eject
/usr/man/man1/eject.1

%changelog
* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com> 
- Injected new description and group.

[ Some changelog entries trimmed for brevity.  -Editor. ]
      
