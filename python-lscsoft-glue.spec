#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	Grid LSC User Engine
Summary(pl.UTF-8):	Silnik użytkownika Grid LSC
Name:		python-lscsoft-glue
# keep 2.x here for python2 support; python3 package (3.0.1+) in python3-lscsoft-glue.spec
Version:	2.0.0
Release:	1
License:	GPL v3+
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/lscsoft-glue/
Source0:	https://files.pythonhosted.org/packages/source/l/lscsoft-glue/lscsoft-glue-%{version}.tar.gz
# Source0-md5:	2ae608b582b6ea43dd0b2f34ccda6625
URL:		https://pypi.org/project/lscsoft-glue/
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-ligo-segments
BuildRequires:	python-numpy
BuildRequires:	python-pyOpenSSL
BuildRequires:	python-six
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
Requires:	python-modules >= 1:2.7
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

# require lal, ligolw_test01 additionally requires matplotlib
%{__sed} -i -e 's/^\t\(ligolw_test01\|test_ligolw_lsctables\|test_ligolw_table\|test_ligolw_utils_segments\)/\t /' test/Makefile

%build
%py_build

%if %{with tests}
# adjust doctest for py2
%{__sed} -i -e 's/100500000000$/100500000000L/' build-2/lib.*/glue/lal.py

PYTHONPATH=$(readlink -f build-2/lib.*) \
%{__make} -C test \
	PYTHON=%{__python}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%py_postclean

for f in $RPM_BUILD_ROOT%{_bindir}/ligolw_* ; do
	%{__mv} "$f" "${f}-2"
done

# not here; change to FHS-compatible locations if required
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/etc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/var

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/dmtdq_seg_insert
%attr(755,root,root) %{_bindir}/ldbdc
%attr(755,root,root) %{_bindir}/ldbdd
%attr(755,root,root) %{_bindir}/ldg_submit_dax
%attr(755,root,root) %{_bindir}/ligolw_cbc_glitch_page-2
%attr(755,root,root) %{_bindir}/ligolw_combine_segments-2
%attr(755,root,root) %{_bindir}/ligolw_diff-2
%attr(755,root,root) %{_bindir}/ligolw_dq_active-2
%attr(755,root,root) %{_bindir}/ligolw_dq_active_cats-2
%attr(755,root,root) %{_bindir}/ligolw_dq_grapher-2
%attr(755,root,root) %{_bindir}/ligolw_dq_query-2
%attr(755,root,root) %{_bindir}/ligolw_geo_fr_to_dq-2
%attr(755,root,root) %{_bindir}/ligolw_inspiral2mon-2
%attr(755,root,root) %{_bindir}/ligolw_print_tables-2
%attr(755,root,root) %{_bindir}/ligolw_publish_dqxml-2
%attr(755,root,root) %{_bindir}/ligolw_segment_diff-2
%attr(755,root,root) %{_bindir}/ligolw_segment_insert-2
%attr(755,root,root) %{_bindir}/ligolw_segment_intersect-2
%attr(755,root,root) %{_bindir}/ligolw_segment_query-2
%attr(755,root,root) %{_bindir}/ligolw_segment_union-2
%attr(755,root,root) %{_bindir}/ligolw_segments_from_cats-2
%attr(755,root,root) %{_bindir}/ligolw_segments_from_cats_split-2
%attr(755,root,root) %{_bindir}/ligolw_veto_def_check-2
%attr(755,root,root) %{_bindir}/ligolw_veto_sngl_trigger-2
%attr(755,root,root) %{_bindir}/segdb_coalesce
%dir %{py_sitedir}/glue
%{py_sitedir}/glue/*.py[co]
%dir %{py_sitedir}/glue/auth
%{py_sitedir}/glue/auth/*.py[co]
%dir %{py_sitedir}/glue/ligolw
%attr(755,root,root) %{py_sitedir}/glue/ligolw/*.so
%{py_sitedir}/glue/ligolw/*.py[co]
%dir %{py_sitedir}/glue/ligolw/utils
%{py_sitedir}/glue/ligolw/utils/*.py[co]
%dir %{py_sitedir}/glue/segmentdb
%{py_sitedir}/glue/segmentdb/*.py[co]
%{py_sitedir}/lscsoft_glue-%{version}-py*.egg-info
