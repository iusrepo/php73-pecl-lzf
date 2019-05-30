%global pecl_name LZF
%global ini_name  40-lzf.ini
%global php       php73

Name:           %{php}-pecl-lzf
Version:        1.6.7
Release:        2%{?dist}
Summary:        Extension to handle LZF de/compression
License:        PHP
URL:            https://pecl.php.net/package/%{pecl_name}
Source0:        https://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRequires:  %{php}-devel
BuildRequires:  pear1 %{php}-cli %{php}-common %{php}-xml
BuildRequires:  liblzf-devel
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

Provides:       php-pecl(%{pecl_name}) = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}

# safe replacement
Provides:       php-pecl-%{pecl_name} = %{version}-%{release}
Provides:       php-pecl-%{pecl_name}%{?_isa} = %{version}-%{release}
Conflicts:      php-pecl-%{pecl_name} < %{version}-%{release}


%description
This extension provides LZF compression and decompression using the liblzf
library.  LZF is a very fast compression algorithm, ideal for saving space with
a slight speed cost.


%prep
%setup -c -q
sed -e '/name="lib/d' -i package.xml
rm -r %{pecl_name}-%{version}/lib/

sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml

cat > %{ini_name} << EOF
; Enable %{pecl_name} extension module
extension=lzf.so
EOF


%build
cd %{pecl_name}-%{version}
phpize
%configure --enable-lzf --with-liblzf
%make_build


%install
make -C %{pecl_name}-%{version} install INSTALL_ROOT=%{buildroot}
install -D -p -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

install -D -p -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{pecl_name}.xml

for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -D -p -m 644 %{pecl_name}-%{version}/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd %{pecl_name}-%{version}
TEST_PHP_EXECUTABLE=%{__php} \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__php} run-tests.php \
    -n -q \
    -d extension=%{buildroot}%{php_extdir}/lzf.so


%triggerin -- pear1
if [ -x %{__pecl} ]; then
    %{pecl_install} %{pecl_xmldir}/%{pecl_name}.xml >/dev/null || :
fi


%posttrans
if [ -x %{__pecl} ]; then
    %{pecl_install} %{pecl_xmldir}/%{pecl_name}.xml >/dev/null || :
fi


%postun
if [ $1 -eq 0 -a -x %{__pecl} ]; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%license %{pecl_name}-%{version}/LICENSE
%doc %{pecl_docdir}/%{pecl_name}
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/lzf.so
%{pecl_xmldir}/%{pecl_name}.xml


%changelog
* Thu May 30 2019 Carl George <carl@george.computer> - 1.6.7-2
- Port from Fedora to IUS

* Thu May 30 2019 Carl George <carl@george.computer> - 1.6.7-1
- Latest upstream

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 16 2018 Carl George <carl@george.computer> - 1.6.6-2
- Provide arch-specific pecl name
- Fix license and documentation handling

* Thu Oct 11 2018 Remi Collet <remi@remirepo.net> - 1.6.6-1
- Rebuild for https://fedoraproject.org/wiki/Changes/php73
- update to 1.6.6

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 03 2017 Remi Collet <remi@fedoraproject.org> - 1.6.5-7
- rebuild for https://fedoraproject.org/wiki/Changes/php72

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.6.5-4
- Rebuild due to bug in RPM (RHBZ #1468476)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 14 2016 Remi Collet <remi@fedoraproject.org> - 1.6.5-2
- rebuild for https://fedoraproject.org/wiki/Changes/php71

* Mon Jun 27 2016 Remi Collet <remi@fedoraproject.org> - 1.6.5-1
- update to 1.6.5
- rebuild for https://fedoraproject.org/wiki/Changes/php70

* Thu Feb 25 2016 Remi Collet <remi@fedoraproject.org> - 1.6.2-11
- drop scriptlets (replaced by file triggers in php-pear) #1310546

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 19 2014 Remi Collet <rcollet@redhat.com> - 1.6.2-7
- rebuild for https://fedoraproject.org/wiki/Changes/Php56
- add numerical prefix to extension configuration file

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 22 2013 Remi Collet <rcollet@redhat.com> - 1.6.2-4
- rebuild for http://fedoraproject.org/wiki/Features/Php55

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Oct 28 2012 Andrew Colin Kissa - 1.6.2-2
- Fix php spec macros
- Fix Zend API version checks

* Sat Oct 20 2012 Andrew Colin Kissa - 1.6.2-1
- Upgrade to latest upstream
- Fix bugzilla #838309 #680230

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 1.5.2-9
- rebuild against PHP 5.4, with upstream patch
- add filter to avoid private-shared-object-provides
- add minimal %%check

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 15 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 1.5.2-7
- Fix bugzilla #715791

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.5.2-4
- rebuild for new PHP 5.3.0 ABI (20090626)

* Mon Jun 22 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.5.2-3
- Consistent use of macros

* Mon Jun 22 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.5.2-2
- Fixes to the install to retain timestamps and other fixes raised in review

* Sun Jun 14 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.5.2-1
- Initial RPM package
