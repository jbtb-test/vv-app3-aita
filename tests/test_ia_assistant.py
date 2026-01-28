"""
============================================================
tests/test_ia_assistant.py
------------------------------------------------------------
Description :
    Tests unitaires (pytest) pour APP3 AITA — ia_assistant.py (fallback IA).

Objectifs :
    - Vérifier ENABLE_AI=0 => IA OFF => []
    - Vérifier ENABLE_AI=1 + OPENAI_API_KEY absente => [] (fallback)
    - Vérifier ENABLE_AI=1 + OPENAI_API_KEY présente => 1 idée IA (stub)
    - Vérifier is_ai_enabled() strict (uniquement "1")
    - Vérifier robustesse (pas d’exception propagée)

Usage :
    pytest -q
============================================================
"""

from __future__ import annotations

import os
import pytest

from vv_app3_aita import models
from vv_app3_aita.ia_assistant import is_ai_enabled, generate_ai_test_ideas


# ============================================================
# 🔧 Fixtures
# ============================================================
@pytest.fixture
def sample_requirement() -> models.Requirement:
    return models.Requirement(
        requirement_id="REQ-AI-001",
        title="AI req",
        description="desc",
        criticality="LOW",
        source="UNIT",
    )


# ============================================================
# 🧪 Tests
# ============================================================
@pytest.mark.parametrize("value, expected", [("0", False), ("", False), ("false", False), ("1", True), ("01", False)])
def test_is_ai_enabled_strict(value: str, expected: bool, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ENABLE_AI", value)
    assert is_ai_enabled() is expected


def test_generate_ai_test_ideas_ai_disabled_returns_empty(
    sample_requirement: models.Requirement, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    monkeypatch.setenv("ENABLE_AI", "0")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with caplog.at_level("INFO"):
        ideas = generate_ai_test_ideas(sample_requirement)

    assert ideas == []
    assert any("IA désactivée" in rec.message for rec in caplog.records)


def test_generate_ai_test_ideas_enabled_but_missing_key_returns_empty(
    sample_requirement: models.Requirement, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    monkeypatch.setenv("ENABLE_AI", "1")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with caplog.at_level("WARNING"):
        ideas = generate_ai_test_ideas(sample_requirement)

    assert ideas == []
    assert any("OPENAI_API_KEY" in rec.message for rec in caplog.records)
    assert any("ENABLE_AI" in rec.message or "IA" in rec.message for rec in caplog.records)



def test_generate_ai_test_ideas_enabled_with_key_returns_stub_idea(
    sample_requirement: models.Requirement, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    monkeypatch.setenv("ENABLE_AI", "1")
    monkeypatch.setenv("OPENAI_API_KEY", "dummy-key-for-tests")

    with caplog.at_level("INFO"):
        ideas = generate_ai_test_ideas(sample_requirement)

    assert isinstance(ideas, list)
    assert len(ideas) == 1

    idea = ideas[0]
    assert isinstance(idea, models.TestIdea)

    assert idea.requirement_id == sample_requirement.requirement_id
    assert idea.category == "AI"
    assert idea.origin.upper() == "AI"
    assert idea.idea_id == f"{sample_requirement.requirement_id}-AI-1"
    assert "IA-suggested" in idea.description

    assert any("IA (stub)" in rec.message for rec in caplog.records)


def test_generate_ai_test_ideas_never_raises(sample_requirement: models.Requirement) -> None:
    """
    Sécurité absolue R1 : la fonction ne doit pas lever d’exception en usage normal.
    Ici on vérifie juste qu’un appel hors config retourne soit [] soit 1 idée.
    """
    # On ne touche pas à l'env ici: ce test doit rester robuste.
    ideas = generate_ai_test_ideas(sample_requirement)
    assert isinstance(ideas, list)
