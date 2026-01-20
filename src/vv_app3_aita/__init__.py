# -*- coding: utf-8 -*-
"""
vv_app3_aita
============

APP3 AITA — AI-assisted Test Ideas & Traceability Accelerator

Public API (stable)
-------------------
- Domain models: Requirement, TestIdea, TestCase
- Core pipeline pieces: generate_test_pack, export_test_pack_md, export_test_pack_json

Design constraints
------------------
- AI is suggestion-only and optional
- Deterministic & auditable outputs
"""

from __future__ import annotations

from vv_app3_aita.models import Requirement, TestIdea, TestCase
from vv_app3_aita.generator import generate_test_pack
from vv_app3_aita.export import export_test_pack_md, export_test_pack_json

__version__ = "1.0.0"

__all__ = [
    "__version__",
    # Models
    "Requirement",
    "TestIdea",
    "TestCase",
    # Generator
    "generate_test_pack",
    # Export
    "export_test_pack_md",
    "export_test_pack_json",
]
