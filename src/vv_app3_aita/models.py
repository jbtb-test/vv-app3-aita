#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
APP3 — AITA
------------------------------------------------------------
File: models.py

Rôle :
    Modèles métier de l’application APP3 AITA :
      - Requirement
      - TestIdea
      - TestCase

    Aucun traitement IA ici.
============================================================
"""

from __future__ import annotations

# ============================================================
# 📦 Imports
# ============================================================
from dataclasses import dataclass, field
from typing import List, Optional


# ============================================================
# ⚠️ Exceptions spécifiques
# ============================================================
class ModelError(Exception):
    """Erreur liée aux modèles métier."""


# ============================================================
# 🧩 Modèles
# ============================================================
@dataclass(frozen=True)
class Requirement:
    requirement_id: str
    title: str
    description: str
    criticality: str
    source: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Requirement":
        for key in ("requirement_id", "title", "description", "criticality"):
            if key not in data or not str(data[key]).strip():
                raise ModelError(f"Champ requis manquant: {key}")

        return cls(
            requirement_id=str(data["requirement_id"]).strip(),
            title=str(data["title"]).strip(),
            description=str(data["description"]).strip(),
            criticality=str(data["criticality"]).strip(),
            source=str(data.get("source")).strip() if data.get("source") else None,
        )


@dataclass(frozen=True)
class TestIdea:
    idea_id: str
    requirement_id: str
    category: str
    description: str
    origin: str = "CHECKLIST"

    def is_ai_generated(self) -> bool:
        return self.origin.upper() == "AI"


@dataclass
class TestCase:
    test_id: str
    requirement_id: str
    title: str
    description: str
    preconditions: List[str] = field(default_factory=list)
    steps: List[str] = field(default_factory=list)
    expected_results: List[str] = field(default_factory=list)
    source_ideas: List[str] = field(default_factory=list)

    def validate(self) -> None:
        if not self.test_id:
            raise ModelError("test_id obligatoire")
        if not self.steps:
            raise ModelError("steps requis")
        if not self.expected_results:
            raise ModelError("expected_results requis")
