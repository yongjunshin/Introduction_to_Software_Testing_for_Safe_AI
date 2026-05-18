"""Baseline test for mutmut.

mutmut requires a passing test command for its baseline run. We deliberately
do NOT exercise the SuT here so that every mutant ends up in the `survived`
bucket — we compute our own test-to-mutant kill matrix in-process by
extracting each mutant's source via `mutmut apply`.
"""


def test_baseline_passes():
    assert True
