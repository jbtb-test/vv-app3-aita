#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
APP3 — AITA
------------------------------------------------------------
File: checklist.py

Description :
    Génération déterministe d’idées de tests à partir
    d’une exigence système selon une checklist ISTQB.

Rôle :
    - Fournir un socle de test design standard (hors IA)
    - Génération stable, reproductible et auditable
    - Base commune avant enrichissement IA éventuel

Design constraints :
    - Sans IA
    - Déterministe
    - Testable unitairement
============================================================
"""

from __future__ import annotations

# ============================================================
# 📦 Imports
# ============================================================
from typing import List

from vv_app3_aita.models import Requirement, TestIdea


# ============================================================
# ⚠️ Exceptions spécifiques au module
# ============================================================
class ChecklistError(Exception):
    """Erreur liée à la génération d’idées de tests (checklist)."""


# ============================================================
# 🔧 Fonctions principales
# ============================================================
def generate_test_ideas(requirement: Requirement) -> List[TestIdea]:
    """
    Génère une liste déterministe d’idées de tests
    à partir d’une exigence système.

    Checklist couverte :
        - Cas nominal (POSITIVE)
        - Cas négatifs (NEGATIVE)
        - Valeurs limites (BOUNDARY)
        - Robustesse (ROBUSTNESS)
        - Sécurité (SECURITY)

    Args:
        requirement: exigence système source.

    Returns:
        Liste d’objets TestIdea, ordonnée et stable.

    Raises:
        ChecklistError: si l’exigence est invalide.
    """
    if not requirement or not requirement.requirement_id:
        raise ChecklistError("Exigence invalide ou identifiant manquant.")

    base = requirement.requirement_id
    ideas: List[TestIdea] = []

    # Nominal
    ideas.append(
        TestIdea(
            f"{base}-POS-1",
            base,
            "POSITIVE",
            "Nominal behavior",
        )
    )

    # Négatif
    ideas.extend(
        [
            TestIdea(
                f"{base}-NEG-1",
                base,
                "NEGATIVE",
                "Invalid inputs rejected",
            ),
            TestIdea(
                f"{base}-NEG-2",
                base,
                "NEGATIVE",
                "Missing mandatory inputs",
            ),
        ]
    )

    # Limites
    ideas.extend(
        [
            TestIdea(
                f"{base}-BND-1",
                base,
                "BOUNDARY",
                "Minimum boundary value",
            ),
            TestIdea(
                f"{base}-BND-2",
                base,
                "BOUNDARY",
                "Maximum boundary value",
            ),
        ]
    )

    # Robustesse
    ideas.append(
        TestIdea(
            f"{base}-ROB-1",
            base,
            "ROBUSTNESS",
            "Unexpected conditions",
        )
    )

    # Sécurité
    ideas.append(
        TestIdea(
            f"{base}-SEC-1",
            base,
            "SECURITY",
            "Unauthorized access attempt",
        )
    )

    return ideas
