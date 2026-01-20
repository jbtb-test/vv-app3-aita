"""
============================================================
tests/test_export.py
------------------------------------------------------------
Description :
    Tests unitaires (pytest) pour APP3 AITA — exports (MD / JSON).

Objectifs :
    - Vérifier export JSON (schema, meta.count, champs)
    - Vérifier export MD (lisibilité, sections attendues)
    - Vérifier déterminisme (ordre stable dans JSON)
    - Vérifier fallback pack vide (exports générés)
    - Vérifier validation des entrées (TestCase invalide => ModelError)

Usage :
    pytest -q
============================================================
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from vv_app3_aita import models
from vv_app3_aita.export import export_test_pack_json, export_test_pack_md


# ============================================================
# 🔧 Fixtures
# ============================================================
@pytest.fixture
def tc_a() -> models.TestCase:
    return models.TestCase(
        test_id="TC-REQ-A-BOUNDARY-00000001",
        requirement_id="REQ-A",
        title="[BOUNDARY] Req A",
        description="Origin: CHECKLIST",
        preconditions=["Known initial state"],
        steps=["Step A1"],
        expected_results=["Expected A1"],
        source_ideas=["REQ-A-BND-1"],
    )


@pytest.fixture
def tc_b() -> models.TestCase:
    return models.TestCase(
        test_id="TC-REQ-B-NEGATIVE-00000002",
        requirement_id="REQ-B",
        title="[NEGATIVE] Req B",
        description="Origin: CHECKLIST",
        preconditions=["Known initial state"],
        steps=["Step B1"],
        expected_results=["Expected B1"],
        source_ideas=["REQ-B-NEG-1"],
    )


# ============================================================
# 🧪 Tests — JSON
# ============================================================
def test_export_json_schema_and_count(tmp_path: Path, tc_a: models.TestCase, tc_b: models.TestCase) -> None:
    out = tmp_path / "test_pack.json"
    export_test_pack_json([tc_a, tc_b], out)

    assert out.exists()
    payload = json.loads(out.read_text(encoding="utf-8"))

    assert payload["meta"]["format"] == "vv-app3-aita.test-pack.v1"
    assert payload["meta"]["count"] == 2
    assert isinstance(payload["tests"], list)
    assert len(payload["tests"]) == 2

    # Champs attendus
    required_keys = {
        "test_id",
        "requirement_id",
        "title",
        "description",
        "preconditions",
        "steps",
        "expected_results",
        "source_ideas",
    }
    assert required_keys.issubset(set(payload["tests"][0].keys()))


def test_export_json_is_deterministic_sorted_by_requirement_then_test_id(
    tmp_path: Path, tc_a: models.TestCase, tc_b: models.TestCase
) -> None:
    """
    export.py trie par (requirement_id, test_id). On fournit l'entrée inversée et on vérifie l'ordre.
    """
    out = tmp_path / "test_pack.json"

    # Inversé volontairement
    export_test_pack_json([tc_b, tc_a], out)
    payload = json.loads(out.read_text(encoding="utf-8"))

    tests = payload["tests"]
    assert [t["requirement_id"] for t in tests] == ["REQ-A", "REQ-B"]
    assert tests[0]["test_id"] == tc_a.test_id
    assert tests[1]["test_id"] == tc_b.test_id


# ============================================================
# 🧪 Tests — MD
# ============================================================
def test_export_md_header_and_sections(tmp_path: Path, tc_a: models.TestCase, tc_b: models.TestCase) -> None:
    out = tmp_path / "test_pack.md"
    export_test_pack_md([tc_a, tc_b], out)

    assert out.exists()
    text = out.read_text(encoding="utf-8")

    # Header + count
    assert "# Test Pack — APP3 AITA" in text
    assert "- Count: **2**" in text

    # Grouping sections
    assert "## Requirement: `REQ-A`" in text
    assert "## Requirement: `REQ-B`" in text

    # Test sections
    assert f"### {tc_a.test_id} — {tc_a.title}" in text
    assert "**Preconditions**" in text
    assert "**Steps**" in text
    assert "**Expected results**" in text
    assert "**Source ideas**" in text


def test_export_md_empty_pack_generates_readable_stub(tmp_path: Path) -> None:
    out = tmp_path / "test_pack.md"
    export_test_pack_md([], out)

    assert out.exists()
    text = out.read_text(encoding="utf-8")

    assert "# Test Pack — APP3 AITA" in text
    assert "- Count: **0**" in text
    assert "## No tests generated" in text


def test_export_json_empty_pack_generates_valid_schema(tmp_path: Path) -> None:
    out = tmp_path / "test_pack.json"
    export_test_pack_json([], out)

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["meta"]["count"] == 0
    assert payload["meta"]["format"] == "vv-app3-aita.test-pack.v1"
    assert payload["tests"] == []


# ============================================================
# 🧪 Tests — Validation des entrées
# ============================================================
def test_export_raises_if_testcase_invalid(tmp_path: Path, tc_a: models.TestCase) -> None:
    """
    export.py appelle tc.validate(). Si tc invalide => ModelError.
    """
    bad = models.TestCase(
        test_id="",  # invalide
        requirement_id=tc_a.requirement_id,
        title=tc_a.title,
        description=tc_a.description,
        preconditions=tc_a.preconditions,
        steps=tc_a.steps,
        expected_results=tc_a.expected_results,
        source_ideas=tc_a.source_ideas,
    )

    with pytest.raises(models.ModelError):
        export_test_pack_json([bad], tmp_path / "x.json")

    with pytest.raises(models.ModelError):
        export_test_pack_md([bad], tmp_path / "x.md")
