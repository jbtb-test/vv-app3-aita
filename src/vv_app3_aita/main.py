#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
APP3 — AITA
------------------------------------------------------------
File: main.py

Rôle :
    Point d’entrée CLI de l’application APP3 AITA.

    Orchestre le pipeline de test design :
        requirements (CSV) -> test ideas -> test pack -> exports (MD / JSON)

    IA optionnelle, suggestion-only, non bloquante.
============================================================
"""

from __future__ import annotations

import argparse
import csv
import logging
import os
import sys
from pathlib import Path

from vv_app3_aita.models import ModelError, Requirement, TestIdea, TestCase
from vv_app3_aita.checklist import generate_test_ideas
from vv_app3_aita.ia_assistant import generate_ai_test_ideas
from vv_app3_aita.generator import generate_test_pack
from vv_app3_aita.export import export_test_pack_json, export_test_pack_md


# ============================================================
# 🧾 Logging (local, autonome)
# ============================================================
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


log = get_logger(__name__)


# ============================================================
# ⚠️ Exceptions spécifiques
# ============================================================
class ModuleError(Exception):
    """Erreur spécifique au module main (contrat public pour les tests)."""


# ============================================================
# 🔧 IO helpers
# ============================================================
def load_requirements_csv(path: Path) -> list[Requirement]:
    """
    Load requirements from CSV into Requirement objects.

    Expected columns (minimal):
        requirement_id,title,description,criticality
    Optional:
        source
    """
    if not path.exists():
        raise ModuleError(f"Fichier d’entrée introuvable: {path}")

    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        # fallback
        text = path.read_text(encoding="utf-8")

    reader = csv.DictReader(text.splitlines())
    if not reader.fieldnames:
        raise ModuleError("CSV invalide: en-têtes absents")

    required = {"requirement_id", "title", "description", "criticality"}
    missing = required - set([h.strip() for h in reader.fieldnames if h])
    if missing:
        raise ModuleError(f"CSV invalide: colonnes manquantes: {sorted(missing)}")

    reqs: list[Requirement] = []
    for idx, row in enumerate(reader, start=2):  # header = line 1
        try:
            reqs.append(Requirement.from_dict(row))
        except ModelError as e:
            raise ModuleError(f"CSV invalide (ligne {idx}): {e}") from e

    return reqs


def build_ideas(requirements: list[Requirement], *, enable_ai: bool) -> list[TestIdea]:
    """
    Build test ideas from checklist + optional AI.
    Deterministic ordering, AI never blocks.
    """
    ideas: list[TestIdea] = []

    # Checklist ideas (deterministic)
    for r in requirements:
        ideas.extend(generate_test_ideas(r))

    # Optional AI ideas: enable via env var to match ia_assistant contract
    os.environ["ENABLE_AI"] = "1" if enable_ai else "0"
    if enable_ai:
        for r in requirements:
            ideas.extend(generate_ai_test_ideas(r))

    # Stable sort for auditability
    ideas.sort(key=lambda i: (i.requirement_id, i.category.upper(), i.idea_id))
    return ideas


# ============================================================
# 🔧 CLI
# ============================================================
def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vv-app3-aita",
        description=(
            "APP3 AITA — AI-assisted Test Ideas & Traceability Accelerator\n"
            "(IA optionnelle, suggestion-only)"
        ),
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/inputs/requirements.csv"),
        help="CSV exigences (défaut: data/inputs/requirements.csv)",
    )

    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data/outputs"),
        help="Dossier de sortie (défaut: data/outputs)",
    )

    parser.add_argument(
        "--enable-ai",
        action="store_true",
        help="Active les suggestions IA (non bloquant, suggestion-only)",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Logs verbeux",
    )

    return parser


def process(args: argparse.Namespace) -> None:
    log.info("Démarrage APP3 AITA")
    log.debug("Arguments CLI: %s", args)

    reqs = load_requirements_csv(args.input)
    if not reqs:
        raise ModuleError("Aucune exigence chargée depuis le CSV.")

    args.out_dir.mkdir(parents=True, exist_ok=True)

    ideas = build_ideas(reqs, enable_ai=bool(args.enable_ai))
    if not ideas:
        log.warning("Aucune idée de test générée (checklist/IA).")

    test_pack: list[TestCase] = generate_test_pack(reqs, ideas, logger=log)
    if not test_pack:
        log.warning("Pack de tests vide (rien à exporter).")

    out_json = args.out_dir / "test_pack.json"
    out_md = args.out_dir / "test_pack.md"

    export_test_pack_json(test_pack, out_json, logger=log)
    export_test_pack_md(test_pack, out_md, logger=log)

    log.info("Exports générés: %s ; %s", out_md, out_json)


# ============================================================
# ▶️ Main
# ============================================================
def main(argv: list[str] | None = None) -> int:
    try:
        parser = build_arg_parser()
        args = parser.parse_args(argv)

        if args.verbose:
            log.setLevel(logging.DEBUG)

        process(args)
        log.info("Fin APP3 AITA")
        return 0

    except ModuleError as e:
        log.error(str(e))
        return 1
    except Exception:
        log.exception("Erreur inattendue")
        return 2


if __name__ == "__main__":
    sys.exit(main())
