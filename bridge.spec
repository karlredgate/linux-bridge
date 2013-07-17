%define revcount %(git rev-list HEAD | wc -l)
%define treeish %(git rev-parse --short HEAD)
%define localmods %(git diff-files --exit-code --quiet  || date +.m%%j%%H%%M%%S)

Summary: Unity Kernel Bridge
Name: unity-bridge
Version: 7.0
Release: %{revcount}.%{treeish}%{localmods}
Distribution: CentOS
Group: System Environment/Kernel
License: Proprietary
Vendor: Karl Redgate
Packager: Karl N. Redgate <Karl.Redgate@gmail.com>
Requires: kernel


%define _topdir %(echo $PWD)/rpm
BuildRoot: %{_topdir}/BUILDROOT
%define Exports %(echo $PWD)/exports

Requires(post): module-init-tools

%description
Modified Linux bridge to allow address locking.

%prep
%build

%install
tar -C %{Exports} -cf - . | (cd $RPM_BUILD_ROOT; tar xf -)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
/lib/modules

%post
[ "$1" -gt 1 ] && {
    : echo "`date '+%%b %%e %%H:%%M:%%S'`: Upgrading"
}

[ "$1" = 1 ] && {
    : echo "`date '+%%b %%e %%H:%%M:%%S'`: New install"
}

depmod -a

%changelog

* Wed Jun 12 2013 Karl Redgate <Karl.Redgate@gmail.com>
- Initial build

# vim:autoindent
