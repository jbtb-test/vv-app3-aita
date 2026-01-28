#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
APP3 — AITA
------------------------------------------------------------
File: ia_assistant.py

Description :
    Module IA encapsulé (optionnel) pour générer des idées
    complémentaires de tests à partir d’une exigence.

Rôle :
    - IA suggestion-only (ne modifie jamais les datasets)
    - Jamais bloquante (fallback strict [])
    - Contrôle via ENABLE_AI=1 + OPENAI_API_KEY

Contraintes :
    - Aucun appel réseau obligatoire (stub contrôlé)
    - Si IA désactivée ou non disponible => retourne []
============================================================
"""

from __future__ import annotations

# ============================================================
# 📦 Imports
# ============================================================
import logging
import os
import sys
from typing import List, Optional

from vv_app3_aita.models import Requirement, TestIdea


# ============================================================
# 🧾 Logging (local, autonome)
# ============================================================
def get_logger(name: str) -> logging.Logger:
    """
    Crée un logger stable (stderr), sans dépendance externe.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(stream=sys.stderr)
        fmt = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger


# ============================================================
# 🧾 Logging (standard, capturable par pytest caplog)
# ============================================================
log = logging.getLogger(__name__)


# ============================================================
# ⚠️ Exceptions spécifiques au module
# ============================================================
class AIAssistantError(Exception):
    """Erreur interne IA (jamais propagée au caller)."""


# ============================================================
# 🔧 Fonctions principales
# ============================================================
def is_ai_enabled() -> bool:
    """
    Détermine si l’IA est explicitement activée.

    Source of truth :
        - ENABLE_AI=1

    Returns:
        True si ENABLE_AI=1, sinon False.
    """
    return os.getenv("ENABLE_AI", "0") == "1"


def _get_api_key() -> Optional[str]:
    """Retourne la clé API si présente, sinon None."""
    api_key = os.getenv("OPENAI_API_KEY")
    return api_key.strip() if api_key and api_key.strip() else None


def generate_ai_test_ideas(requirement: Requirement) -> List[TestIdea]:
    """
    Génère des idées de tests complémentaires via IA (suggestion-only).

    Contrat :
        - IA désactivée (ENABLE_AI!=1) -> []
        - OPENAI_API_KEY absente -> []
        - Erreur interne -> [] (non bloquant)

    Args:
        requirement: exigence source.

    Returns:
        Liste d'objets TestIdea (peut être vide).
    """
    rid = (getattr(requirement, "requirement_id", "") or "").strip()
    if not rid:
        # Fallback-safe : pas d'exigence exploitable
        log.warning("IA: requirement_id manquant => fallback []")
        return []

    if not is_ai_enabled():
        log.info("IA désactivée (ENABLE_AI!=1) => fallback []")
        return []

    api_key = _get_api_key()
    if not api_key:
        log.warning("IA activée mais OPENAI_API_KEY absente => fallback []")
        return []

    try:
        # STUB contrôlé (pas d'appel réseau)
        log.info("IA (stub): génération suggestions pour %s", rid)

        return [
            TestIdea(
                idea_id=f"{rid}-AI-1",
                requirement_id=rid,
                category="AI",
                description="IA-suggested edge case scenario",
                origin="AI",
            )
        ]
    except Exception as exc:  # pragma: no cover
        log.error("Erreur IA ignorée => fallback []: %s", exc)
        return []
