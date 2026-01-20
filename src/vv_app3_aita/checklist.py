#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
APP3 — AITA
------------------------------------------------------------
File: checklist.py

Rôle :
    Génération déterministe d’idées de tests à partir
    d’une exigence système selon une checklist ISTQB.

    - Sans IA
    - Stable
    - Testable
============================================================
"""

from __future__ import annotations

# ============================================================
# 📦 Imports
# ============================================================
from typing import List

from vv_app3_aita.models import Requirement, TestIdea


# ============================================================
# ⚠️ Exceptions spécifiques
# ============================================================
class ChecklistError(Exception):
    """Erreur liée à la checklist de test design."""


# ============================================================
# 🔧 Fonctions principales
# ============================================================
def generate_test_ideas(requirement: Requirement) -> List[TestIdea]:
    base = requirement.requirement_id
    ideas: List[TestIdea] = []

    ideas.append(TestIdea(f"{base}-POS-1", base, "POSITIVE", "Nominal behavior"))

    ideas.extend(
        [
            TestIdea(f"{base}-NEG-1", base, "NEGATIVE", "Invalid inputs rejected"),
            TestIdea(f"{base}-NEG-2", base, "NEGATIVE", "Missing mandatory inputs"),
        ]
    )

    ideas.extend(
        [
            TestIdea(f"{base}-BND-1", base, "BOUNDARY", "Minimum boundary value"),
            TestIdea(f"{base}-BND-2", base, "BOUNDARY", "Maximum boundary value"),
        ]
    )

    ideas.append(
        TestIdea(f"{base}-ROB-1", base, "ROBUSTNESS", "Unexpected conditions")
    )

    ideas.append(
        TestIdea(f"{base}-SEC-1", base, "SECURITY", "Unauthorized access attempt")
    )

    return ideas
