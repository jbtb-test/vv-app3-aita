#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
APP3 — AITA
------------------------------------------------------------
File: ia_assistant.py

Rôle :
    Génération optionnelle d’idées de tests via IA.

    - IA suggestion-only
    - Jamais bloquante
    - Fallback strict (retourne [])
============================================================
"""

from __future__ import annotations

# ============================================================
# 📦 Imports
# ============================================================
import logging
import os
import sys
from typing import List

from vv_app3_aita.models import Requirement, TestIdea


# ============================================================
# 🧾 Logging (local)
# ============================================================
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(stream=sys.stderr)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


log = get_logger(__name__)


# ============================================================
# ⚠️ Exceptions spécifiques
# ============================================================
class AIAssistantError(Exception):
    """Erreur interne IA (jamais propagée)."""


# ============================================================
# 🔧 Fonctions principales
# ============================================================
def is_ai_enabled() -> bool:
    """Détermine si l’IA est explicitement activée."""
    return os.getenv("ENABLE_AI", "0") == "1"


def generate_ai_test_ideas(requirement: Requirement) -> List[TestIdea]:
    """
    Génère des idées de tests complémentaires via IA.

    En cas de problème (IA désactivée, clé absente, erreur),
    retourne toujours une liste vide.
    """

    if not is_ai_enabled():
        log.info("IA désactivée (ENABLE_AI=0)")
        return []

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        log.warning("IA activée mais OPENAI_API_KEY absente => fallback []")

        return []

    try:
        # ⚠️ IA simulée / stub volontaire
        # L’appel réel sera branché ultérieurement
        log.info("Appel IA simulé pour exigence %s", requirement.requirement_id)

        return [
            TestIdea(
                idea_id=f"{requirement.requirement_id}-AI-1",
                requirement_id=requirement.requirement_id,
                category="AI",
                description="IA-suggested edge case scenario",
                origin="AI",
            )
        ]

    except Exception as exc:  # pragma: no cover - sécurité absolue
        log.error("Erreur IA ignorée => fallback []: %s", exc)
        return []
