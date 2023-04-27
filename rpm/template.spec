%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-launch-testing
Version:        2.1.0
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS launch_testing package

License:        Apache License 2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       %{name}-runtime%{?_isa?} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}

%description
A package to create tests which involve launch files and multiple processes.

%package runtime
Summary:        Runtime-only files for launch_testing package
Requires:       python%{python3_pkgversion}-pytest
Requires:       ros-rolling-ament-index-python-runtime
Requires:       ros-rolling-launch-runtime
Requires:       ros-rolling-launch-xml-runtime
Requires:       ros-rolling-launch-yaml-runtime
Requires:       ros-rolling-osrf-pycommon-runtime
Requires:       ros-rolling-ros-workspace-runtime
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  ros-rolling-ros-workspace-devel

%if 0%{?with_tests}
BuildRequires:  ros-rolling-ament-copyright-devel
BuildRequires:  ros-rolling-ament-flake8-devel
BuildRequires:  ros-rolling-ament-pep257-devel
BuildRequires:  ros-rolling-launch-devel
%endif

%description runtime
Runtime-only files for launch_testing package

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%py3_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%py3_install -- --prefix "/opt/ros/rolling"

for f in \
    /opt/ros/rolling/include/ \
    /opt/ros/rolling/share/ament_index/resource_index/packages/ \
    /opt/ros/rolling/share/launch_testing/cmake/ \
    /opt/ros/rolling/share/launch_testing/package.dsv \
    /opt/ros/rolling/share/launch_testing/package.xml \
; do
    if [ -e %{buildroot}$f ]; then echo $f; fi
done > devel_files

%if 0%{?with_tests}
%check
# Look for a directory with a name indicating that it contains tests
TEST_TARGET=$(ls -d * | grep -m1 "\(test\|tests\)" ||:)
if [ -n "$TEST_TARGET" ] && %__python3 -m pytest --version; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%__python3 -m pytest $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files -f devel_files

%files runtime
/opt/ros/rolling
%exclude /opt/ros/rolling/include/
%exclude /opt/ros/rolling/share/ament_index/resource_index/packages/
%exclude /opt/ros/rolling/share/launch_testing/cmake
%exclude /opt/ros/rolling/share/launch_testing/package.dsv
%exclude /opt/ros/rolling/share/launch_testing/package.xml

%changelog
* Thu Apr 27 2023 Aditya Pande <aditya.pande@openrobotics.org> - 2.1.0-1
- Autogenerated by Bloom

* Wed Apr 12 2023 Aditya Pande <aditya.pande@openrobotics.org> - 2.0.1-1
- Autogenerated by Bloom

* Tue Apr 11 2023 Aditya Pande <aditya.pande@openrobotics.org> - 2.0.0-1
- Autogenerated by Bloom

* Tue Mar 21 2023 Aditya Pande <aditya.pande@openrobotics.org> - 1.4.1-2
- Autogenerated by Bloom

