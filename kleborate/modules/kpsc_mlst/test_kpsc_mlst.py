"""
This file contains tests for Kleborate. To run all tests, go the repo's root directory and run:
  python3 -m pytest

To get code coverage stats:
  coverage run --source . -m pytest && coverage report -m

Copyright 2023 Kat Holt
Copyright 2023 Ryan Wick (rrwick@gmail.com)
https://github.com/katholt/Kleborate/

This file is part of Kleborate. Kleborate is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version. Kleborate is distributed in
the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License along with Kleborate. If
not, see <https://www.gnu.org/licenses/>.
"""

import collections
import pathlib
import pytest

from .kpsc_mlst import *


def get_test_genome_dir():
    return pathlib.Path(__file__).parents[3] / 'test' / 'test_genomes'


def test_get_headers():
    # stdout_headers must be a subset of full_headers.
    full_headers, stdout_headers = get_headers()
    assert all(h in full_headers for h in stdout_headers)


def test_check_cli_options_1():
    Args = collections.namedtuple('Args', ['kpsc_mlst_min_identity', 'kpsc_mlst_min_coverage',
                                           'kpsc_mlst_required_exact_matches'])
    check_cli_options(Args(kpsc_mlst_min_identity=90.0, kpsc_mlst_min_coverage=90.0,
                           kpsc_mlst_required_exact_matches=3))


def test_check_cli_options_2():
    Args = collections.namedtuple('Args', ['kpsc_mlst_min_identity', 'kpsc_mlst_min_coverage',
                                           'kpsc_mlst_required_exact_matches'])
    with pytest.raises(SystemExit):
        check_cli_options(Args(kpsc_mlst_min_identity=0.90, kpsc_mlst_min_coverage=90.0,
                               kpsc_mlst_required_exact_matches=3))


def test_check_cli_options_3():
    Args = collections.namedtuple('Args', ['kpsc_mlst_min_identity', 'kpsc_mlst_min_coverage',
                                           'kpsc_mlst_required_exact_matches'])
    with pytest.raises(SystemExit):
        check_cli_options(Args(kpsc_mlst_min_identity=-90.0, kpsc_mlst_min_coverage=0.90,
                               kpsc_mlst_required_exact_matches=3))


def test_check_cli_options_4():
    Args = collections.namedtuple('Args', ['kpsc_mlst_min_identity', 'kpsc_mlst_min_coverage',
                                           'kpsc_mlst_required_exact_matches'])
    with pytest.raises(SystemExit):
        check_cli_options(Args(kpsc_mlst_min_identity=-10.0, kpsc_mlst_min_coverage=90.0,
                               kpsc_mlst_required_exact_matches=3))


def test_check_cli_options_5():
    Args = collections.namedtuple('Args', ['kpsc_mlst_min_identity', 'kpsc_mlst_min_coverage',
                                           'kpsc_mlst_required_exact_matches'])
    with pytest.raises(SystemExit):
        check_cli_options(Args(kpsc_mlst_min_identity=90.0, kpsc_mlst_min_coverage=120.0,
                               kpsc_mlst_required_exact_matches=3))


def test_check_cli_options_6():
    Args = collections.namedtuple('Args', ['kpsc_mlst_min_identity', 'kpsc_mlst_min_coverage',
                                           'kpsc_mlst_required_exact_matches'])
    with pytest.raises(SystemExit):
        check_cli_options(Args(kpsc_mlst_min_identity=90.0, kpsc_mlst_min_coverage=90.0,
                               kpsc_mlst_required_exact_matches=-2))


def test_check_external_programs_1(mocker):
    # Tests the good case where minimap2 is found.
    mocker.patch(
        'shutil.which',
        side_effect=lambda x: {'minimap2': '/usr/bin/minimap2'}[x],
    )
    check_external_programs()


def test_check_external_programs_2(mocker):
    # Tests the bad case where minimap2 is missing.
    mocker.patch(
        'shutil.which',
        side_effect=lambda x: {'minimap2': None}[x],
    )
    with pytest.raises(SystemExit):
        check_external_programs()


def test_get_results_1():
    Args = collections.namedtuple('Args', ['kpsc_mlst_min_identity', 'kpsc_mlst_min_coverage',
                                           'kpsc_mlst_required_exact_matches'])
    results = get_results(get_test_genome_dir() / 'GCF_000968155.1.fna.gz',
                          Args(kpsc_mlst_min_identity=90.0, kpsc_mlst_min_coverage=80.0,
                               kpsc_mlst_required_exact_matches=3))
    assert results['klebsiella_st'] == 'ST66'
    assert results['gapA'] == '2'
    assert results['infB'] == '3'
    assert results['mdh'] == '2'
    assert results['pgi'] == '1'
    assert results['phoE'] == '10'
    assert results['rpoB'] == '1'
    assert results['tonB'] == '13'


def test_get_results_2():
    Args = collections.namedtuple('Args', ['kpsc_mlst_min_identity', 'kpsc_mlst_min_coverage',
                                           'kpsc_mlst_required_exact_matches'])
    results = get_results(get_test_genome_dir() / 'GCF_001068035.1.fna.gz',
                          Args(kpsc_mlst_min_identity=90.0, kpsc_mlst_min_coverage=80.0,
                               kpsc_mlst_required_exact_matches=3))
    assert results['klebsiella_st'] == 'ST592-1LV'
    assert results['gapA'] == '2'
    assert results['infB'] == '3'
    assert results['mdh'] == '6'
    assert results['pgi'] == '-'
    assert results['phoE'] == '9'
    assert results['rpoB'] == '4'
    assert results['tonB'] == '13'
