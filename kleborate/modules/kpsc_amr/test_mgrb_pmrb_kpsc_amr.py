"""
Copyright 2023 Kat Holt
Copyright 2020 Ryan Wick (rrwick@gmail.com)
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
import pytest
import pathlib

from kleborate.shared.resMinimap import read_class_file, get_res_headers, resminimap_assembly
from kleborate.modules.kpsc_amr.kpsc_amr import get_headers, get_results


def get_test_genome_dir():
    return pathlib.Path(__file__).parents[3] / 'test' / 'test_res_mgrb_pmrb'

"""
Tests calling of colistin resistance via the truncation of mgrB/pmrB.
"""

def test_get_results_1():
    Args = collections.namedtuple('Args', ['kpsc_amr_min_identity', 'kpsc_amr_min_coverage', 'kpsc_amr_min_spurious_identity', 'kpsc_amr_min_spurious_coverage'])
    results = get_results(get_test_genome_dir() / 'test_res_mgrb_pmrb_1.fasta', None,
                          Args(kpsc_amr_min_identity=90.0, kpsc_amr_min_coverage=80.0, kpsc_amr_min_spurious_identity=80.0, kpsc_amr_min_spurious_coverage=40.0), {})
    assert results['Col_mutations'] == '-'


def test_get_results_2():
    #A frameshift in pmrB should cause an early stop and lead to a colisitin resistance call.
    Args = collections.namedtuple('Args', ['kpsc_amr_min_identity', 'kpsc_amr_min_coverage', 'kpsc_amr_min_spurious_identity', 'kpsc_amr_min_spurious_coverage'])
    results = get_results(get_test_genome_dir() / 'test_res_mgrb_pmrb_2.fasta', None,
                          Args(kpsc_amr_min_identity=90.0, kpsc_amr_min_coverage=80.0, kpsc_amr_min_spurious_identity=80.0, kpsc_amr_min_spurious_coverage=40.0), {})
    assert results['Col_mutations'] == 'PmrB-42%'


def test_get_results_3():
    #This tests an early stop mutation (without a frameshift) in pmrB.

    Args = collections.namedtuple('Args', ['kpsc_amr_min_identity', 'kpsc_amr_min_coverage', 'kpsc_amr_min_spurious_identity', 'kpsc_amr_min_spurious_coverage'])
    results = get_results(get_test_genome_dir() / 'test_res_mgrb_pmrb_3.fasta', None,
                          Args(kpsc_amr_min_identity=90.0, kpsc_amr_min_coverage=80.0, kpsc_amr_min_spurious_identity=80.0, kpsc_amr_min_spurious_coverage=40.0), {})
    assert results['Col_mutations'] == 'PmrB-38%'


def test_get_results_4():
    Args = collections.namedtuple('Args', ['kpsc_amr_min_identity', 'kpsc_amr_min_coverage', 'kpsc_amr_min_spurious_identity', 'kpsc_amr_min_spurious_coverage'])
    results = get_results(get_test_genome_dir() / 'test_res_mgrb_pmrb_4.fasta', None,
                          Args(kpsc_amr_min_identity=90.0, kpsc_amr_min_coverage=80.0, kpsc_amr_min_spurious_identity=80.0, kpsc_amr_min_spurious_coverage=40.0), {})
    assert results['Col_mutations'] == 'MgrB-0%'


def test_get_results_5():
    Args = collections.namedtuple('Args', ['kpsc_amr_min_identity', 'kpsc_amr_min_coverage', 'kpsc_amr_min_spurious_identity', 'kpsc_amr_min_spurious_coverage'])
    results = get_results(get_test_genome_dir() / 'SRR2098701.fasta', None,
                          Args(kpsc_amr_min_identity=90.0, kpsc_amr_min_coverage=80.0, kpsc_amr_min_spurious_identity=80.0, kpsc_amr_min_spurious_coverage=40.0), {})
    assert results['Col_mutations'] == 'PmrB-58%'

