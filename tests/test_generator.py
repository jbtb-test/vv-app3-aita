"""
============================================================
tests/test_generator.py
------------------------------------------------------------
Description :
    Tests unitaires (pytest) pour APP3 AITA — génération du pack de tests.

Objectifs :
    - Vérifier comportement nominal (pack généré)
    - Vérifier déterminisme (IDs/ordre stables)
    - Vérifier filtrage des idées (requirements inconnues ignorées)
    - Vérifier fallback (entrées vides -> [])
    - Vérifier conformité des objets TestCase (validate OK)

Usage :
    pytest -q
============================================================
"""

from __future__ import annotations

import pytest

from vv_app3_aita.generator import generate_test_pack
from vv_app3_aita import models


# ============================================================
# 🔧 Fixtures
# ============================================================
@pytest.fixture
def req_a() -> models.Requirement:
    return models.Requirement(
        requirement_id="REQ-GEN-001",
        title="Req A title",
        description="Req A description",
        criticality="HIGH",
        source="UNIT",
    )


@pytest.fixture
def req_b() -> models.Requirement:
    return models.Requirement(
        requirement_id="REQ-GEN-002",
        title="Req B title",
        description="Req B description",
        criticality="LOW",
        source="UNIT",
    )


@pytest.fixture
def ideas_mixed(req_a: models.Requirement, req_b: models.Requirement) -> list[models.TestIdea]:
    """
    Liste d'idées contenant :
    - 2 idées valides (REQ-GEN-001, REQ-GEN-002)
    - 1 idée orpheline (REQ-UNKNOWN) => doit être ignorée
    """
    return [
        models.TestIdea(
            idea_id=f"{req_a.requirement_id}-POS-1",
            requirement_id=req_a.requirement_id,
            category="POSITIVE",
            description="Nominal behavior idea",
            origin="CHECKLIST",
        ),
        models.TestIdea(
            idea_id=f"{req_b.requirement_id}-NEG-1",
            requirement_id=req_b.requirement_id,
            category="NEGATIVE",
            description="Negative behavior idea",
            origin="CHECKLIST",
        ),
        models.TestIdea(
            idea_id="REQ-UNKNOWN-AI-1",
            requirement_id="REQ-UNKNOWN",
            category="AI",
            description="Orphan AI idea",
            origin="AI",
        ),
    ]


# ============================================================
# 🧪 Tests
# ============================================================
def test_generate_test_pack_empty_inputs_returns_empty() -> None:
    """
    Fallback-safe : si requirements ou ideas vides => [].
    """
    assert generate_test_pack([], []) == []
    assert generate_test_pack([models.Requirement("REQ-X", "t", "d", "LOW", "UNIT")], []) == []


def test_generate_test_pack_filters_unknown_requirements(
    req_a: models.Requirement, req_b: models.Requirement, ideas_mixed: list[models.TestIdea]
) -> None:
    """
    Filtrage : les idées référencées sur des requirements inconnues sont ignorées.
    """
    tcs = generate_test_pack([req_a, req_b], ideas_mixed)

    # On attend 2 tests (idée orpheline ignorée)
    assert len(tcs) == 2
    assert {tc.requirement_id for tc in tcs} == {req_a.requirement_id, req_b.requirement_id}


def test_generate_test_pack_nominal_produces_valid_testcases(
    req_a: models.Requirement, req_b: models.Requirement, ideas_mixed: list[models.TestIdea]
) -> None:
    """
    Nominal : chaque TestCase généré est valide et contient les champs attendus.
    """
    tcs = generate_test_pack([req_a, req_b], ideas_mixed)
    assert tcs, "Le pack ne doit pas être vide en nominal"

    for tc in tcs:
        assert isinstance(tc, models.TestCase)

        # Champs clés non vides
        assert tc.test_id
        assert tc.requirement_id
        assert tc.title
        assert tc.description

        assert isinstance(tc.preconditions, list) and len(tc.preconditions) > 0
        assert isinstance(tc.steps, list) and len(tc.steps) > 0
        assert isinstance(tc.expected_results, list) and len(tc.expected_results) > 0
        assert isinstance(tc.source_ideas, list) and len(tc.source_ideas) > 0

        # Traceability : 1 source idea = idea_id
        assert tc.source_ideas[0].startswith(tc.requirement_id)

        # Validation modèle (garantie V&V)
        tc.validate()


def test_generate_test_pack_deterministic_output(
    req_a: models.Requirement, req_b: models.Requirement, ideas_mixed: list[models.TestIdea]
) -> None:
    """
    Déterminisme : même inputs => mêmes outputs (ordre + IDs + contenu clé).
    """
    tcs_1 = generate_test_pack([req_a, req_b], ideas_mixed)
    tcs_2 = generate_test_pack([req_a, req_b], ideas_mixed)

    assert len(tcs_1) == len(tcs_2)

    key_1 = [
        (
            tc.test_id,
            tc.requirement_id,
            tc.title,
            tc.description,
            tuple(tc.preconditions),
            tuple(tc.steps),
            tuple(tc.expected_results),
            tuple(tc.source_ideas),
        )
        for tc in tcs_1
    ]
    key_2 = [
        (
            tc.test_id,
            tc.requirement_id,
            tc.title,
            tc.description,
            tuple(tc.preconditions),
            tuple(tc.steps),
            tuple(tc.expected_results),
            tuple(tc.source_ideas),
        )
        for tc in tcs_2
    ]
    assert key_1 == key_2


def test_generate_test_pack_test_id_format_contains_req_and_category(req_a: models.Requirement) -> None:
    """
    Vérifie que l'ID inclut le requirement + la catégorie (slugifiée), comme défini dans generator.py.
    """
    ideas = [
        models.TestIdea(
            idea_id=f"{req_a.requirement_id}-BND-1",
            requirement_id=req_a.requirement_id,
            category="BOUNDARY",
            description="Boundary idea",
            origin="CHECKLIST",
        )
    ]
    tcs = generate_test_pack([req_a], ideas)
    assert len(tcs) == 1

    tc = tcs[0]
    # Format attendu : TC-<REQSLUG>-<CATSLUG>-<HASH>
    assert tc.test_id.startswith("TC-")
    assert "REQGEN001" in tc.test_id  # REQ-GEN-001 -> REQGEN001
    assert "-BOUNDARY-" in tc.test_id
