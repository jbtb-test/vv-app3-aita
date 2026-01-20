"""
============================================================
tests/test_models.py
------------------------------------------------------------
Description :
    Tests unitaires (pytest) pour APP3 AITA — models.py

Objectifs :
    - Vérifier parsing nominal (Requirement.from_dict)
    - Vérifier validation des entrées et erreurs (ModelError)
    - Vérifier helpers (TestIdea.is_ai_generated)
    - Vérifier validation TestCase.validate (nominal + KO)

Usage :
    pytest -q
============================================================
"""

from __future__ import annotations

import pytest

from vv_app3_aita import models


# ============================================================
# 🔧 Fixtures
# ============================================================
@pytest.fixture
def req_dict_minimal() -> dict:
    return {
        "requirement_id": "REQ-MOD-001",
        "title": "Title",
        "description": "Desc",
        "criticality": "HIGH",
    }


@pytest.fixture
def req_dict_with_source() -> dict:
    return {
        "requirement_id": "REQ-MOD-002",
        "title": "Title 2",
        "description": "Desc 2",
        "criticality": "LOW",
        "source": "DOORS",
    }


@pytest.fixture
def valid_testcase() -> models.TestCase:
    return models.TestCase(
        test_id="TC-REQMOD001-POS-aaaa1111",
        requirement_id="REQ-MOD-001",
        title="[POSITIVE] Title",
        description="Generated from idea",
        preconditions=["Known initial state"],
        steps=["Step 1"],
        expected_results=["Expected 1"],
        source_ideas=["REQ-MOD-001-POS-1"],
    )


# ============================================================
# 🧪 Tests — Requirement
# ============================================================
def test_requirement_from_dict_nominal_minimal(req_dict_minimal: dict) -> None:
    req = models.Requirement.from_dict(req_dict_minimal)

    assert isinstance(req, models.Requirement)
    assert req.requirement_id == "REQ-MOD-001"
    assert req.title == "Title"
    assert req.description == "Desc"
    assert req.criticality == "HIGH"
    assert req.source is None


def test_requirement_from_dict_nominal_with_source(req_dict_with_source: dict) -> None:
    req = models.Requirement.from_dict(req_dict_with_source)
    assert req.source == "DOORS"


@pytest.mark.parametrize(
    "bad_dict, missing_key",
    [
        ({}, "requirement_id"),
        ({"requirement_id": "REQ", "title": "", "description": "D", "criticality": "HIGH"}, "title"),
        ({"requirement_id": "REQ", "title": "T", "description": "", "criticality": "HIGH"}, "description"),
        ({"requirement_id": "REQ", "title": "T", "description": "D", "criticality": ""}, "criticality"),
    ],
)
def test_requirement_from_dict_missing_required_raises(bad_dict: dict, missing_key: str) -> None:
    with pytest.raises(models.ModelError) as exc:
        models.Requirement.from_dict(bad_dict)

    # message contractuel: "Champ requis manquant: <key>"
    assert missing_key in str(exc.value)


# ============================================================
# 🧪 Tests — TestIdea
# ============================================================
def test_testidea_is_ai_generated_false_by_default() -> None:
    idea = models.TestIdea(
        idea_id="REQ-1-POS-1",
        requirement_id="REQ-1",
        category="POSITIVE",
        description="x",
    )
    assert idea.origin == "CHECKLIST"
    assert idea.is_ai_generated() is False


@pytest.mark.parametrize("origin_value", ["AI", "ai", "Ai"])
def test_testidea_is_ai_generated_true(origin_value: str) -> None:
    idea = models.TestIdea(
        idea_id="REQ-1-AI-1",
        requirement_id="REQ-1",
        category="AI",
        description="x",
        origin=origin_value,
    )
    assert idea.is_ai_generated() is True


# ============================================================
# 🧪 Tests — TestCase.validate
# ============================================================
def test_testcase_validate_nominal(valid_testcase: models.TestCase) -> None:
    # ne doit pas lever
    valid_testcase.validate()


def test_testcase_validate_missing_test_id_raises(valid_testcase: models.TestCase) -> None:
    tc = models.TestCase(
        test_id="",
        requirement_id=valid_testcase.requirement_id,
        title=valid_testcase.title,
        description=valid_testcase.description,
        preconditions=valid_testcase.preconditions,
        steps=valid_testcase.steps,
        expected_results=valid_testcase.expected_results,
        source_ideas=valid_testcase.source_ideas,
    )
    with pytest.raises(models.ModelError) as exc:
        tc.validate()
    assert "test_id" in str(exc.value)


def test_testcase_validate_missing_steps_raises(valid_testcase: models.TestCase) -> None:
    tc = models.TestCase(
        test_id=valid_testcase.test_id,
        requirement_id=valid_testcase.requirement_id,
        title=valid_testcase.title,
        description=valid_testcase.description,
        preconditions=valid_testcase.preconditions,
        steps=[],
        expected_results=valid_testcase.expected_results,
        source_ideas=valid_testcase.source_ideas,
    )
    with pytest.raises(models.ModelError) as exc:
        tc.validate()
    assert "steps" in str(exc.value)


def test_testcase_validate_missing_expected_results_raises(valid_testcase: models.TestCase) -> None:
    tc = models.TestCase(
        test_id=valid_testcase.test_id,
        requirement_id=valid_testcase.requirement_id,
        title=valid_testcase.title,
        description=valid_testcase.description,
        preconditions=valid_testcase.preconditions,
        steps=valid_testcase.steps,
        expected_results=[],
        source_ideas=valid_testcase.source_ideas,
    )
    with pytest.raises(models.ModelError) as exc:
        tc.validate()
    assert "expected_results" in str(exc.value)
