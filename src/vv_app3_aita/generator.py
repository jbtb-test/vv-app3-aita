#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
APP3 — AITA
------------------------------------------------------------
File: generator.py

Description :
    Générer un pack de tests structuré (liste de TestCase)
    à partir :
        - requirements (Requirement)
        - test ideas (TestIdea) issues de la checklist et/ou IA

Rôle :
    - Construire des TestCase déterministes (IDs et ordre stables)
    - Produire un contenu audit-ready (traçable via source_ideas)
    - Assurer des objets valides (tc.validate()) avant export

Contraintes projet :
    - Déterministe (IDs + ordre stables)
    - IA suggestion-only : aucune décision automatique
    - Fallback-safe : entrées vides => retourne []

API :
    generate_test_pack(requirements, test_ideas, *, logger=None) -> list[TestCase]
============================================================
"""

from __future__ import annotations

# ============================================================
# 📦 Imports
# ============================================================
import hashlib
import logging
import re
from typing import Optional

from vv_app3_aita.models import Requirement, TestCase, TestIdea

_LOG = logging.getLogger(__name__)
_SLUG_RX = re.compile(r"[^a-z0-9]+")


# ============================================================
# 🔧 Helpers
# ============================================================
def _slugify(value: str, *, max_len: int = 24) -> str:
    """
    Normalise une chaîne en "slug" ASCII simple (a-z0-9-).

    Args:
        value: valeur brute.
        max_len: longueur max du slug.

    Returns:
        slug en minuscules, tronqué si nécessaire.
    """
    s = (value or "").strip().lower()
    s = _SLUG_RX.sub("-", s).strip("-")
    return s[:max_len] if len(s) > max_len else s


def _stable_hash(text: str, *, n: int = 8) -> str:
    """
    Hash stable (sha256) tronqué à n caractères.

    Args:
        text: texte à hasher.
        n: taille du token.

    Returns:
        token hex stable.
    """
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()[:n]


def _is_usable_idea(idea: TestIdea, req_by_id: dict[str, Requirement]) -> bool:
    """Retourne True si l’idée pointe vers une requirement connue."""
    rid = (idea.requirement_id or "").strip()
    return bool(rid) and rid in req_by_id


# ============================================================
# 🔧 Fonction principale
# ============================================================
def generate_test_pack(
    requirements: list[Requirement],
    test_ideas: list[TestIdea],
    *,
    logger: Optional[logging.Logger] = None,
) -> list[TestCase]:
    """
    Génère un pack de tests structuré, déterministe et validé.

    Règles :
        - Si requirements ou test_ideas vide => []
        - Filtre : seules les idées liées à des requirements connues sont gardées
        - Tri déterministe : requirement_id, category, idea_id
        - test_id déterministe : TC-<REQ>-<CAT>-<HASH>
        - steps/expected_results toujours non vides (sinon validate() échoue)

    Args:
        requirements: exigences d’entrée.
        test_ideas: idées de tests (checklist et/ou IA).
        logger: logger optionnel (sinon logger module).

    Returns:
        Liste de TestCase valides (peut être vide).
    """
    log = logger or _LOG

    if not requirements or not test_ideas:
        log.info(
            "generate_test_pack: nothing to generate (requirements=%s, ideas=%s).",
            len(requirements or []),
            len(test_ideas or []),
        )
        return []

    req_by_id: dict[str, Requirement] = {
        r.requirement_id: r for r in requirements if (r.requirement_id or "").strip()
    }

    # Filtre : on garde uniquement les idées qui pointent sur une requirement connue
    usable_ideas: list[TestIdea] = [i for i in test_ideas if _is_usable_idea(i, req_by_id)]

    if not usable_ideas:
        log.warning("generate_test_pack: no usable ideas linked to known requirements.")
        return []

    usable_ideas.sort(
        key=lambda i: (
            (i.requirement_id or "").strip(),
            (i.category or "").strip().upper(),
            (i.idea_id or "").strip(),
        )
    )

    out: list[TestCase] = []
    seen: set[str] = set()

    for idea in usable_ideas:
        req = req_by_id[(idea.requirement_id or "").strip()]

        category = (idea.category or "GENERIC").strip().upper()
        rid_slug = _slugify(req.requirement_id).upper().replace("-", "")
        cat_slug = _slugify(category, max_len=12).upper().replace("-", "")

        token = _stable_hash(
            f"{req.requirement_id}|{category}|{idea.idea_id}|{idea.description}",
            n=8,
        )
        test_id = f"TC-{rid_slug}-{cat_slug}-{token}"

        # Rare collision handling (deterministic fallback)
        if test_id in seen:
            token2 = _stable_hash(
                f"{req.requirement_id}|{category}|{idea.idea_id}|dup",
                n=8,
            )
            test_id = f"TC-{rid_slug}-{cat_slug}-{token2}"
        seen.add(test_id)

        # Titre orienté recruteur : catégorie + requirement title
        title = f"[{category}] {req.title}".strip()

        # Description auditable : idée + extrait requirement
        desc_parts: list[str] = []
        if idea.description:
            desc_parts.append(f"Idea: {idea.description}")
        if req.description:
            desc_parts.append(f"Requirement excerpt: {req.description[:220]}")
        if idea.origin:
            desc_parts.append(f"Origin: {idea.origin}")
        description = "\n".join(desc_parts).strip() or "Generated from test idea."

        # Preconditions / Steps / Expected (toujours non vides)
        preconditions = ["System is in a known initial state."]
        steps = [
            "Prepare the system under test.",
            f"Execute the scenario for: {idea.description or category}.",
            "Capture evidences (logs, outputs, system state).",
        ]
        expected_results = [
            "Observed behavior matches the requirement intent.",
            "No unexpected side effects are observed.",
        ]

        tc = TestCase(
            test_id=test_id,
            requirement_id=req.requirement_id,
            title=title,
            description=description,
            preconditions=preconditions,
            steps=steps,
            expected_results=expected_results,
            source_ideas=[idea.idea_id],
        )

        # Validation modèle (garantie V&V)
        tc.validate()
        out.append(tc)

    log.info("generate_test_pack: generated %s test cases.", len(out))
    return out
