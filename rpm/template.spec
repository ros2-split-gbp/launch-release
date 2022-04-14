%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-launch-pytest
Version:        1.0.1
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS launch_pytest package

License:        Apache License 2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       python%{python3_pkgversion}-pytest
Requires:       ros-rolling-ament-index-python
Requires:       ros-rolling-launch
Requires:       ros-rolling-launch-testing
Requires:       ros-rolling-osrf-pycommon
Requires:       ros-rolling-ros-workspace
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  ros-rolling-ament-copyright
BuildRequires:  ros-rolling-ament-flake8
BuildRequires:  ros-rolling-ament-pep257
BuildRequires:  ros-rolling-launch
BuildRequires:  ros-rolling-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
A package to create tests which involve launch files and multiple processes.

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

%files
/opt/ros/rolling

%changelog
* Wed Apr 13 2022 Aditya Pande <aditya.pande@openrobotics.org> - 1.0.1-1
- Autogenerated by Bloom

* Tue Apr 12 2022 Aditya Pande <aditya.pande@openrobotics.org> - 1.0.0-1
- Autogenerated by Bloom

* Fri Apr 08 2022 Aditya Pande <aditya.pande@openrobotics.org> - 0.23.1-1
- Autogenerated by Bloom

* Wed Mar 30 2022 Aditya Pande <aditya.pande@openrobotics.org> - 0.23.0-1
- Autogenerated by Bloom

* Mon Mar 28 2022 Aditya Pande <aditya.pande@openrobotics.org> - 0.22.0-1
- Autogenerated by Bloom

* Tue Mar 01 2022 Aditya Pande <aditya.pande@openrobotics.org> - 0.21.1-1
- Autogenerated by Bloom

* Tue Feb 08 2022 Aditya Pande <aditya.pande@openrobotics.org> - 0.21.0-2
- Autogenerated by Bloom

