#!/usr/bin/env python3
# ============================================================
# APP3 — AITA
# ------------------------------------------------------------
# File: main.py
#
# Rôle :
#   Point d’entrée CLI de l’application APP3 AITA.
#   Orchestre le pipeline de test design :
#     exigences → idées de tests → pack de tests (MD / JSON).
#
#   La logique métier est déléguée aux modules dédiés.
#   L’IA est optionnelle, non décisionnelle et non bloquante.
#
# Usage :
#   python -m vv_app3_aita.main --help
#   python -m vv_app3_aita.main --input data/inputs/requirements.csv
#
# Architecture :
#   - main.py        : orchestration CLI
#   - models.py      : modèles métier
#   - checklist.py   : checklist test design (ISTQB)
#   - generator.py   : génération du pack de tests
#   - export.py      : exports MD / JSON
#   - ia_assistant.py: suggestions IA (optionnel)
# ============================================================

from __future__ import annotations

import argparse
import logging
from pathlib import Path
import sys


# ------------------------------------------------------------
# Logging configuration
# ------------------------------------------------------------
def configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s - %(message)s",
    )


# ------------------------------------------------------------
# CLI arguments
# ------------------------------------------------------------
def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vv-app3-aita",
        description=(
            "APP3 AITA — AI-assisted Test Ideas & Traceability Accelerator\n"
            "Generate a structured test design pack from requirements "
            "(IA optionnelle, suggestion-only)."
        ),
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/inputs/requirements.csv"),
        help="Path to input requirements CSV file (default: data/inputs/requirements.csv)",
    )

    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data/outputs"),
        help="Output directory for generated test packs (default: data/outputs)",
    )

    parser.add_argument(
        "--enable-ai",
        action="store_true",
        help="Enable AI-assisted test idea suggestions (optional, non-blocking)",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    return parser


# ------------------------------------------------------------
# Main orchestration
# ------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    configure_logging(args.verbose)

    logging.info("Starting APP3 AITA")
    logging.debug("Arguments: %s", args)

    # Validate input
    if not args.input.exists():
        logging.error("Input file not found: %s", args.input)
        return 1

    # Prepare output directory
    args.out_dir.mkdir(parents=True, exist_ok=True)
    logging.info("Output directory: %s", args.out_dir)

    # Placeholder for pipeline execution
    # (Implemented in steps 3.7+)
    logging.info("Pipeline execution not yet implemented (scaffold only).")

    logging.info("APP3 AITA finished successfully (no-op run).")
    return 0


# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main())
