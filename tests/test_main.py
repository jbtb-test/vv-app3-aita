"""
============================================================
tests.test_main
------------------------------------------------------------
Description :
    Baseline unit tests for APP3 AITA skeleton (standardization phase).

Usage :
    pytest -q
============================================================
"""

import pytest

from vv_app3_aita.main import ModuleError, process


@pytest.fixture
def sample_input():
    return {"key": "value"}


@pytest.fixture
def invalid_input():
    return None


def test_process_nominal(sample_input):
    out = process(sample_input)
    assert out.ok is True
    assert out.payload["key"] == "value"
    assert out.message == "OK"


def test_process_error(invalid_input):
    with pytest.raises(ModuleError):
        process(invalid_input)
