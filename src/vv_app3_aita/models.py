#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
APP3 — AITA
------------------------------------------------------------
File: models.py

Description :
    Modèles métier de l’application APP3 AITA :
      - Requirement
      - TestIdea
      - TestCase

Rôle :
    - Porter le contrat de données (input / pipeline / export)
    - Garantir des objets validables (audit-ready)
    - Aucun traitement IA ici (séparation des responsabilités)

Contraintes :
    - Déterministe
    - Validations minimales intégrées (ModelError)
============================================================
"""

from __future__ import annotations

# ============================================================
# 📦 Imports
# ============================================================
from dataclasses import dataclass, field
from typing import List, Mapping, Optional


# ============================================================
# ⚠️ Exceptions spécifiques au module
# ============================================================
class ModelError(Exception):
    """Erreur liée aux modèles métier (validation, mapping, etc.)."""


# ============================================================
# 🧩 Modèles
# ============================================================
@dataclass(frozen=True)
class Requirement:
    """
    Exigence système.

    Champs attendus :
        - requirement_id
        - title
        - description
        - criticality
        - source (optionnel)
    """

    requirement_id: str
    title: str
    description: str
    criticality: str
    source: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "Requirement":
        """
        Construit une Requirement depuis un dict (ex: ligne CSV).

        Args:
            data: mapping contenant les champs requis.

        Returns:
            Requirement

        Raises:
            ModelError: si champ requis manquant ou vide.
        """
        for key in ("requirement_id", "title", "description", "criticality"):
            if key not in data or not str(data[key]).strip():
                raise ModelError(f"Champ requis manquant: {key}")

        source_val = data.get("source")
        source = str(source_val).strip() if source_val and str(source_val).strip() else None

        return cls(
            requirement_id=str(data["requirement_id"]).strip(),
            title=str(data["title"]).strip(),
            description=str(data["description"]).strip(),
            criticality=str(data["criticality"]).strip(),
            source=source,
        )


@dataclass(frozen=True)
class TestIdea:
    """
    Idée de test (issue de checklist et/ou IA).

    Notes :
        - origin est une information d’audit (CHECKLIST / AI / etc.)
        - idea_id doit rester stable et traçable.
    """

    idea_id: str
    requirement_id: str
    category: str
    description: str
    origin: str = "CHECKLIST"

    def is_ai_generated(self) -> bool:
        """Retourne True si l’idée est d’origine IA."""
        return (self.origin or "").strip().upper() == "AI"


@dataclass
class TestCase:
    """
    Cas de test généré (pack).

    Notes :
        - validate() garantit un minimum de complétude pour export/audit.
        - Le contenu est orienté "recruteur-friendly" mais reste auditable.
    """

    test_id: str
    requirement_id: str
    title: str
    description: str
    preconditions: List[str] = field(default_factory=list)
    steps: List[str] = field(default_factory=list)
    expected_results: List[str] = field(default_factory=list)
    source_ideas: List[str] = field(default_factory=list)

    def validate(self) -> None:
        """
        Valide le TestCase (contrat minimal).

        Raises:
            ModelError: si champ obligatoire manquant.
        """
        if not (self.test_id or "").strip():
            raise ModelError("test_id obligatoire")
        if not (self.requirement_id or "").strip():
            raise ModelError("requirement_id obligatoire")
        if not (self.title or "").strip():
            raise ModelError("title obligatoire")
        if not self.steps:
            raise ModelError("steps requis")
        if not self.expected_results:
            raise ModelError("expected_results requis")


# ============================================================
# Public exports
# ============================================================
__all__ = [
    "ModelError",
    "Requirement",
    "TestIdea",
    "TestCase",
]
