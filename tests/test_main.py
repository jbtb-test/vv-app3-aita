"""
============================================================
tests.test_main
------------------------------------------------------------
Description :
    Baseline unit tests for APP3 AITA CLI skeleton.

    Contract tested:
      - process(args) expects an argparse.Namespace with:
          - input: Path
          - out_dir: Path
          - enable_ai: bool
          - verbose: bool
      - process raises ModuleError if input does not exist
      - process creates out_dir if needed (no-op pipeline for now)

Usage :
    pytest -q
============================================================
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pytest

from vv_app3_aita.main import ModuleError, process


def _ns(input_path: Path, out_dir: Path, enable_ai: bool = False, verbose: bool = False) -> argparse.Namespace:
    """Helper to build a minimal argparse.Namespace matching main.process contract."""
    return argparse.Namespace(
        input=input_path,
        out_dir=out_dir,
        enable_ai=enable_ai,
        verbose=verbose,
    )


def test_process_nominal(tmp_path: Path):
    # Arrange
    input_file = tmp_path / "requirements.csv"
    input_file.write_text("requirement_id,title,description,criticality\nREQ-1,t,d,HIGH\n", encoding="utf-8")

    out_dir = tmp_path / "out"

    args = _ns(input_file, out_dir)

    # Act / Assert (no exception)
    process(args)

    # Out dir should be created
    assert out_dir.exists()
    assert out_dir.is_dir()


def test_process_error_input_missing(tmp_path: Path):
    # Arrange: input does not exist
    input_file = tmp_path / "missing.csv"
    out_dir = tmp_path / "out"
    args = _ns(input_file, out_dir)

    # Act / Assert
    with pytest.raises(ModuleError):
        process(args)
