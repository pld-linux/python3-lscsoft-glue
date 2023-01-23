#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Grid LSC User Engine
Summary(pl.UTF-8):	Silnik użytkownika Grid LSC
Name:		python3-lscsoft-glue
Version:	3.0.1
Release:	1
License:	GPL v3+
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/lscsoft-glue/
Source0:	https://files.pythonhosted.org/packages/source/l/lscsoft-glue/lscsoft-glue-%{version}.tar.gz
# Source0-md5:	9414ea200a8711dd699a1df520aa6746
URL:		https://pypi.org/project/lscsoft-glue/
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-ligo-segments
BuildRequires:	python3-numpy
BuildRequires:	python3-pyOpenSSL
BuildRequires:	python3-pyRXP
BuildRequires:	python3-six
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
Requires:	python3-modules >= 1:3.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Glue is a collection of utilities for running data analysis pipelines
for online and offline analysis as well as accessing various grid
utilities. It also provides the infrastructure for the segment
database.

%description -l pl.UTF-8
Glue to zbiór narzędzi do uruchamiania potoków analizy danych online
jak i offline, a także dostępu do różnych narzędzi do danych
tabelarycznych. Zapewnia także infrastrukturę do bazy danych
przedziałów.

%prep
%setup -q -n lscsoft-glue-%{version}

# fails with py3
%{__sed} -i -e '/^\tglue_ligolw_ilwd_verify /d' test/Makefile

# uses remote DTD
%{__sed} -i -e '/^\ttest_ldbd /d' test/Makefile

# doctest failure
%{__sed} -i -e '/^\ttest_ligolw_ligolw /d' test/Makefile

# require lal, ligolw_test01 additionally requires matplotlib
%{__sed} -i -e '/^\t\(ligolw_test01\|test_ligolw_lsctables\|test_ligolw_table\|test_ligolw_utils_segments\) /d' test/Makefile

# too exact comparisons
%{__sed} -i -e 's/test_swig_comparison/disabled_swig_comparison/' test/lal_verify.py

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(readlink -f build-3/lib.*) \
%{__make} -C test \
	PYTHON=%{__python3}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/ligolw_combine_segments
%attr(755,root,root) %{_bindir}/ligolw_diff
%attr(755,root,root) %{_bindir}/ligolw_dq_active
%attr(755,root,root) %{_bindir}/ligolw_dq_active_cats
%attr(755,root,root) %{_bindir}/ligolw_inspiral2mon
%attr(755,root,root) %{_bindir}/ligolw_print_tables
%{_datadir}/lscsoft-glue
%dir %{py3_sitedir}/glue
%{py3_sitedir}/glue/*.py
%{py3_sitedir}/glue/__pycache__
%dir %{py3_sitedir}/glue/ligolw
%attr(755,root,root) %{py3_sitedir}/glue/ligolw/*.so
%{py3_sitedir}/glue/ligolw/*.py
%{py3_sitedir}/glue/ligolw/__pycache__
%dir %{py3_sitedir}/glue/ligolw/utils
%{py3_sitedir}/glue/ligolw/utils/*.py
%{py3_sitedir}/glue/ligolw/utils/__pycache__
%dir %{py3_sitedir}/glue/segmentdb
%{py3_sitedir}/glue/segmentdb/*.py
%{py3_sitedir}/glue/segmentdb/__pycache__
%{py3_sitedir}/lscsoft_glue-%{version}-py*.egg-info
