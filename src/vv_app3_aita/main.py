#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
APP3 — AITA
------------------------------------------------------------
File: main.py

Description :
    Point d’entrée CLI de l’application APP3 AITA.

Rôle :
    Orchestre le pipeline de test design :
        requirements (CSV) -> test ideas -> test pack -> exports (MD / JSON)

Contraintes :
    - IA optionnelle (ENABLE_AI=1), suggestion-only, non bloquante
    - Déterminisme prioritaire (tri stable des idées)
    - Exports générés même si pack vide (fallback-safe)

Usage :
    python -m vv_app3_aita.main --out-dir data/outputs --verbose
    (Mode IA)
    . .\\tools\\load_env_secret.ps1
    $env:ENABLE_AI="1"
    python -m vv_app3_aita.main --out-dir data/outputs --verbose
============================================================
"""

from __future__ import annotations

# ============================================================
# 📦 Imports
# ============================================================
import argparse
import csv
import logging
import sys
from pathlib import Path

from vv_app3_aita.checklist import generate_test_ideas
from vv_app3_aita.export import export_test_pack_json, export_test_pack_md
from vv_app3_aita.generator import generate_test_pack
from vv_app3_aita.ia_assistant import generate_ai_test_ideas, is_ai_enabled
from vv_app3_aita.models import ModelError, Requirement, TestCase, TestIdea


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
        # Évite les doublons si un root logger est configuré ailleurs.
        logger.propagate = False
    return logger


log = get_logger(__name__)


# ============================================================
# ⚠️ Exceptions spécifiques au module
# ============================================================
class ModuleError(Exception):
    """Erreur spécifique au module main (contrat public pour les tests)."""


# ============================================================
# 🔧 IO helpers
# ============================================================
def load_requirements_csv(path: Path) -> list[Requirement]:
    """
    Charge un CSV exigences en objets Requirement.

    Colonnes attendues (minimal) :
        requirement_id,title,description,criticality
    Optionnel :
        source

    Args:
        path: chemin du CSV.

    Returns:
        Liste de Requirement.

    Raises:
        ModuleError: fichier absent, CSV invalide, erreur de parsing modèle.
    """
    if not path.exists():
        raise ModuleError(f"Fichier d’entrée introuvable: {path}")

    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8")

    reader = csv.DictReader(text.splitlines())
    if not reader.fieldnames:
        raise ModuleError("CSV invalide: en-têtes absents")

    required = {"requirement_id", "title", "description", "criticality"}
    missing = required - {h.strip() for h in reader.fieldnames if h}
    if missing:
        raise ModuleError(f"CSV invalide: colonnes manquantes: {sorted(missing)}")

    reqs: list[Requirement] = []
    for idx, row in enumerate(reader, start=2):  # header = line 1
        try:
            reqs.append(Requirement.from_dict(row))
        except ModelError as e:
            raise ModuleError(f"CSV invalide (ligne {idx}): {e}") from e

    return reqs


# ============================================================
# 🔧 Core pipeline helpers
# ============================================================
def build_ideas(requirements: list[Requirement]) -> list[TestIdea]:
    """
    Construit les idées de tests (checklist + IA optionnelle).

    - Checklist : toujours active (déterministe)
    - IA : active uniquement si ENABLE_AI=1 (suggestion-only, non bloquant)

    Args:
        requirements: exigences en entrée.

    Returns:
        Liste d’objets TestIdea (tri stable).
    """
    ideas: list[TestIdea] = []

    # Checklist ideas (always executed)
    for r in requirements:
        ideas.extend(generate_test_ideas(r))

    # Optional AI ideas (ENABLE_AI=1 uniquement)
    if is_ai_enabled():
        log.info("IA activée via ENABLE_AI=1 (suggestion-only)")
        for r in requirements:
            ideas.extend(generate_ai_test_ideas(r))
    else:
        log.info("IA désactivée (ENABLE_AI!=1)")

    # Stable sort for auditability
    ideas.sort(key=lambda i: (i.requirement_id, (i.category or "").upper(), i.idea_id))
    return ideas


# ============================================================
# 🔧 CLI
# ============================================================
def build_arg_parser() -> argparse.ArgumentParser:
    """
    Construit le parser CLI.

    Returns:
        argparse.ArgumentParser
    """
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
        "--verbose",
        action="store_true",
        help="Logs verbeux",
    )

    return parser


def process(args: argparse.Namespace) -> None:
    """
    Exécute le pipeline complet (hors parsing CLI).

    Args:
        args: arguments CLI déjà parsés.

    Raises:
        ModuleError: en cas d’entrée invalide ou d’erreur contrôlée.
    """
    log.info("Démarrage APP3 AITA")
    log.debug("Arguments CLI: %s", args)

    reqs = load_requirements_csv(args.input)
    if not reqs:
        raise ModuleError("Aucune exigence chargée depuis le CSV.")

    args.out_dir.mkdir(parents=True, exist_ok=True)

    ideas = build_ideas(reqs)
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
    """
    Point d’entrée CLI (module exécutable).

    Args:
        argv: argv optionnel (tests), sinon sys.argv.

    Returns:
        Code retour:
            0 = OK
            1 = erreur contrôlée (ModuleError)
            2 = erreur inattendue
    """
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
