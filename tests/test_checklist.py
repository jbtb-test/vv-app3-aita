"""
============================================================
tests/test_checklist.py
------------------------------------------------------------
Description :
    Tests unitaires (pytest) pour APP3 AITA — checklist ISTQB.

Objectifs :
    - Vérifier comportement nominal (génération idées)
    - Vérifier déterminisme (ordre et contenu stables)
    - Vérifier structure des idées (champs, catégories, IDs)
    - Vérifier validation des entrées (erreur si requirement invalide)

Usage :
    pytest -q
============================================================
"""

from __future__ import annotations

import pytest

from vv_app3_aita.checklist import generate_test_ideas
from vv_app3_aita.models import Requirement, ModelError


# ============================================================
# 🔧 Fixtures
# ============================================================
@pytest.fixture
def sample_requirement() -> Requirement:
    return Requirement(
        requirement_id="REQ-UT-001",
        title="Sample requirement",
        description="Some description",
        criticality="HIGH",
        source="UNIT",
    )


# ============================================================
# 🧪 Tests
# ============================================================
def test_generate_test_ideas_nominal(sample_requirement: Requirement) -> None:
    """
    Nominal : la checklist génère un set d’idées stable et complet.
    """
    ideas = generate_test_ideas(sample_requirement)

    assert isinstance(ideas, list)
    assert len(ideas) == 7, "Checklist attendue: POS(1) + NEG(2) + BND(2) + ROB(1) + SEC(1)"

    # Vérifie catégories attendues
    categories = [i.category for i in ideas]
    assert categories.count("POSITIVE") == 1
    assert categories.count("NEGATIVE") == 2
    assert categories.count("BOUNDARY") == 2
    assert categories.count("ROBUSTNESS") == 1
    assert categories.count("SECURITY") == 1

    # Vérifie que toutes les idées pointent vers la requirement
    assert all(i.requirement_id == sample_requirement.requirement_id for i in ideas)

    # Vérifie présence de descriptions non vides
    assert all((i.description or "").strip() for i in ideas)


def test_generate_test_ideas_deterministic(sample_requirement: Requirement) -> None:
    """
    Déterminisme : même entrée => même sortie (ordre + champs).
    """
    ideas_1 = generate_test_ideas(sample_requirement)
    ideas_2 = generate_test_ideas(sample_requirement)

    assert len(ideas_1) == len(ideas_2)

    # Comparaison stricte sur les champs clés (sans dépendre de __eq__)
    key_1 = [(i.idea_id, i.requirement_id, i.category, i.description, i.origin) for i in ideas_1]
    key_2 = [(i.idea_id, i.requirement_id, i.category, i.description, i.origin) for i in ideas_2]
    assert key_1 == key_2


def test_generate_test_ideas_ids_format(sample_requirement: Requirement) -> None:
    """
    Vérifie le format des IDs : <REQ>-<TAG>-<N> et unicité.
    """
    ideas = generate_test_ideas(sample_requirement)
    ids = [i.idea_id for i in ideas]

    assert len(ids) == len(set(ids)), "Les idea_id doivent être uniques"

    prefix = sample_requirement.requirement_id + "-"
    assert all(x.startswith(prefix) for x in ids)

    # Vérifie tags attendus dans les IDs
    assert any("-POS-" in x for x in ids)
    assert sum(1 for x in ids if "-NEG-" in x) == 2
    assert sum(1 for x in ids if "-BND-" in x) == 2
    assert any("-ROB-" in x for x in ids)
    assert any("-SEC-" in x for x in ids)


def test_requirement_from_dict_invalid_raises() -> None:
    """
    Validation entrée : un requirement invalide doit être rejeté au parsing (from_dict).
    Ici, requirement_id est manquant => ModelError attendu.
    """
    with pytest.raises(ModelError):
        Requirement.from_dict(
            {
                "requirement_id": "",
                "title": "Bad req",
                "description": "Bad",
                "criticality": "LOW",
                "source": "UNIT",
            }
        )

