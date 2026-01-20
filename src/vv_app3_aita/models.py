# ============================================================
# APP3 — AITA
# ------------------------------------------------------------
# File: models.py
#
# Rôle :
#   Définition des modèles métier de l’application APP3 AITA.
#
#   Ces modèles représentent :
#     - les exigences d’entrée
#     - les idées de tests générées
#     - les cas de test structurés exportables
#
#   Aucun traitement IA ici.
#   Aucun effet de bord.
# ============================================================

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


# ------------------------------------------------------------
# Requirement
# ------------------------------------------------------------
@dataclass(frozen=True)
class Requirement:
    """Représente une exigence système d’entrée."""

    requirement_id: str
    title: str
    description: str
    criticality: str
    source: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Requirement":
        required_fields = ["requirement_id", "title", "description", "criticality"]

        for field_name in required_fields:
            if field_name not in data or not str(data[field_name]).strip():
                raise ValueError(f"Missing or empty requirement field: {field_name}")

        return cls(
            requirement_id=str(data["requirement_id"]).strip(),
            title=str(data["title"]).strip(),
            description=str(data["description"]).strip(),
            criticality=str(data["criticality"]).strip(),
            source=str(data.get("source")).strip() if data.get("source") else None,
        )


# ------------------------------------------------------------
# TestIdea
# ------------------------------------------------------------
@dataclass(frozen=True)
class TestIdea:
    """Représente une idée de test (fonctionnelle ou non)."""

    idea_id: str
    requirement_id: str
    category: str
    description: str
    origin: str = "CHECKLIST"  # CHECKLIST | AI

    def is_ai_generated(self) -> bool:
        return self.origin.upper() == "AI"


# ------------------------------------------------------------
# TestCase
# ------------------------------------------------------------
@dataclass
class TestCase:
    """Représente un cas de test structuré."""

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
            raise ValueError("test_id is mandatory")
        if not self.requirement_id:
            raise ValueError("requirement_id is mandatory")
        if not self.title:
            raise ValueError("title is mandatory")
        if not self.steps:
            raise ValueError("At least one test step is required")
        if not self.expected_results:
            raise ValueError("At least one expected result is required")
