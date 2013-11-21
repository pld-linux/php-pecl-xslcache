%define		php_name	php%{?php_suffix}
%define		modname		xslcache
Summary:	%{modname} - A modification of PHP's standard XSL extension that caches the parsed XSL stylesheet representation
Summary(pl.UTF-8):	%{modname} - modyfikacja standardowego rozszerzenia XSL PHP, które buforuje przetworzone reprezentacje arkuszów stylów XSL
Name:		%{php_name}-pecl-%{modname}
Version:	0.7.2
Release:	1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	8c8570503baf7c9711f2d7bf842c292d
URL:		http://pecl.php.net/package/xslcache
BuildRequires:	libxslt-devel >= 1.1.0
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The XSL Cache extension is a modification of PHP's standard XSL
extension that caches the parsed XSL stylesheet representation between
sessions for 2.5x boost in performance for sites that repeatedly apply
the same transform. Although there is still some further work that
could be done on the extension, this code is already proving
beneficial in production use for a few applications on the New York
Times' website.

%prep
%setup -q -c
mv %{modname}-%{version}/* .

%build
phpize
%configure \
	--with-xslcache=%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
