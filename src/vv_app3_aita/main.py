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
        exigences → idées de tests → pack de tests (MD / JSON)

    La logique métier est déléguée aux modules dédiés.
    L’IA est optionnelle, non décisionnelle et non bloquante.

Usage :
    python -m vv_app3_aita.main --help
============================================================
"""

from __future__ import annotations

# ============================================================
# 📦 Imports
# ============================================================
import argparse
import logging
import sys
from pathlib import Path


# ============================================================
# 🧾 Logging (local, autonome)
# ============================================================
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
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
class ModuleError(Exception):
    """Erreur spécifique au module main (contrat public pour les tests)."""

# ============================================================
# 🔧 Fonctions principales
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
        help="Active les suggestions IA (non bloquant)",
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

    if not args.input.exists():
        raise ModuleError(f"Fichier d’entrée introuvable: {args.input}")

    args.out_dir.mkdir(parents=True, exist_ok=True)

    # Pipeline implémenté dans les étapes suivantes
    log.info("Pipeline non implémenté (scaffold uniquement).")


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
        log.info("Fin APP3 AITA (no-op)")
        return 0

    except ModuleError as e:
        log.error(str(e))
        return 1
    except Exception as e:
        log.exception("Erreur inattendue")
        return 2


if __name__ == "__main__":
    sys.exit(main())
