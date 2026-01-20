"""
============================================================
tests/test_main.py
------------------------------------------------------------
Description :
    Tests d’intégration (pytest) pour APP3 AITA — orchestration main.process().

Objectifs :
    - Vérifier comportement nominal (génération outputs MD/JSON)
    - Vérifier validation des entrées CSV (erreurs encapsulées ModuleError)
    - Vérifier création out_dir + fichiers générés

Usage :
    pytest -q
============================================================
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pytest

from vv_app3_aita.main import ModuleError, process


# ============================================================
# 🔧 Helpers / Fixtures
# ============================================================
def _ns(input_path: Path, out_dir: Path, enable_ai: bool = False, verbose: bool = False) -> argparse.Namespace:
    """Build a minimal argparse.Namespace matching main.process contract."""
    return argparse.Namespace(
        input=input_path,
        out_dir=out_dir,
        enable_ai=enable_ai,
        verbose=verbose,
    )


@pytest.fixture
def csv_header() -> str:
    return "requirement_id,title,description,criticality\n"


@pytest.fixture
def csv_one_req() -> str:
    return "requirement_id,title,description,criticality\nREQ-1,t,d,HIGH\n"


# ============================================================
# 🧪 Tests
# ============================================================
def test_process_nominal_generates_outputs(tmp_path: Path, csv_one_req: str) -> None:
    """
    Nominal : process() doit créer out_dir + générer test_pack.md et test_pack.json.
    """
    input_file = tmp_path / "requirements.csv"
    input_file.write_text(csv_one_req, encoding="utf-8")

    out_dir = tmp_path / "out"
    args = _ns(input_file, out_dir, enable_ai=False, verbose=False)

    process(args)

    assert out_dir.exists() and out_dir.is_dir()

    out_md = out_dir / "test_pack.md"
    out_json = out_dir / "test_pack.json"
    assert out_md.exists() and out_md.is_file()
    assert out_json.exists() and out_json.is_file()

    # Sanity content (recruiter-readable marker)
    md_text = out_md.read_text(encoding="utf-8")
    assert "Test Pack" in md_text
    assert "Requirement" in md_text


def test_process_error_input_missing(tmp_path: Path) -> None:
    """
    Entrée inexistante : ModuleError attendu.
    """
    input_file = tmp_path / "missing.csv"
    out_dir = tmp_path / "out"
    args = _ns(input_file, out_dir)

    with pytest.raises(ModuleError):
        process(args)


def test_process_error_missing_required_columns(tmp_path: Path) -> None:
    """
    CSV invalide : colonnes requises manquantes => ModuleError.
    """
    input_file = tmp_path / "requirements.csv"
    # missing 'criticality'
    input_file.write_text("requirement_id,title,description\nREQ-1,t,d\n", encoding="utf-8")

    out_dir = tmp_path / "out"
    args = _ns(input_file, out_dir)

    with pytest.raises(ModuleError) as exc:
        process(args)

    assert "colonnes manquantes" in str(exc.value)


def test_process_error_invalid_row_model(tmp_path: Path, csv_header: str) -> None:
    """
    CSV invalide : ligne non conforme au modèle => ModuleError (encapsulation de ModelError).
    Exemple : title vide.
    """
    input_file = tmp_path / "requirements.csv"
    input_file.write_text(csv_header + "REQ-1,,d,HIGH\n", encoding="utf-8")

    out_dir = tmp_path / "out"
    args = _ns(input_file, out_dir)

    with pytest.raises(ModuleError) as exc:
        process(args)

    assert "CSV invalide" in str(exc.value)


def test_process_error_empty_csv_no_data(tmp_path: Path, csv_header: str) -> None:
    """
    CSV valide mais sans données : process() doit lever ModuleError (aucune exigence chargée).
    """
    input_file = tmp_path / "requirements.csv"
    input_file.write_text(csv_header, encoding="utf-8")

    out_dir = tmp_path / "out"
    args = _ns(input_file, out_dir)

    with pytest.raises(ModuleError) as exc:
        process(args)

    assert "Aucune exigence" in str(exc.value)
