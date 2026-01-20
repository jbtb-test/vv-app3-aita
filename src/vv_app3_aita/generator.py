"""
vv_app3_aita.generator
=====================

APP3 AITA — Test Pack Generator (ISTQB-oriented, deterministic)

Goal
----
Generate a structured, recruiter-friendly and auditable test pack (TestCase list)
from:
- requirements (Requirement)
- test ideas (TestIdea) produced by checklist + optional AI assistant

Key properties
--------------
- Deterministic IDs and ordering (no randomness).
- AI-agnostic: works without AI and never raises for normal "empty" scenarios.
- Suggestion-only: generator does not "decide" anything; it transforms ideas into test cases.

Public API
----------
- generate_test_pack(requirements, test_ideas, *, logger=None) -> list[TestCase]

Usage (example)
---------------
from vv_app3_aita.generator import generate_test_pack

tcs = generate_test_pack(requirements=reqs, test_ideas=ideas)
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
import hashlib
import logging
import re
from typing import Any, Iterable, Optional

# Local imports (expected in APP3 baseline)
# NOTE: keep these imports light and stable.
from vv_app3_aita.models import Requirement, TestIdea, TestCase


_LOG = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers (determinism, normalization)
# ---------------------------------------------------------------------------

_slug_rx = re.compile(r"[^a-z0-9]+")


def _slugify(value: str, *, max_len: int = 48) -> str:
    """Normalize a string into a stable slug (lowercase, alnum + dashes)."""
    s = (value or "").strip().lower()
    s = _slug_rx.sub("-", s).strip("-")
    return s[:max_len] if len(s) > max_len else s


def _stable_hash(text: str, *, n: int = 8) -> str:
    """Stable short hash used in IDs (deterministic across runs)."""
    h = hashlib.sha256((text or "").encode("utf-8")).hexdigest()
    return h[:n]


def _safe_get(obj: Any, name: str, default: Any = "") -> Any:
    """Read attribute or dict key safely."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _to_dict(obj: Any) -> dict[str, Any]:
    """Best-effort conversion to dict without raising."""
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return dict(obj)
    if is_dataclass(obj):
        return asdict(obj)
    if hasattr(obj, "model_dump"):  # pydantic v2
        try:
            return obj.model_dump()
        except Exception:
            return {}
    if hasattr(obj, "dict"):  # pydantic v1
        try:
            return obj.dict()
        except Exception:
            return {}
    # Generic fallback: introspect known fields via dir is risky; keep minimal
    return {}


def _instantiate_testcase(payload: dict[str, Any]) -> Optional[TestCase]:
    """
    Instantiate TestCase in a tolerant way.
    - Prefer TestCase(**payload)
    - Fallback to TestCase.from_dict(payload) if available
    """
    try:
        return TestCase(**payload)  # type: ignore[arg-type]
    except Exception:
        pass

    from_dict = getattr(TestCase, "from_dict", None)
    if callable(from_dict):
        try:
            return from_dict(payload)
        except Exception:
            return None
    return None


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def generate_test_pack(
    requirements: list[Requirement],
    test_ideas: list[TestIdea],
    *,
    logger: Optional[logging.Logger] = None,
) -> list[TestCase]:
    """
    Generate a deterministic and structured list of TestCase from requirements + test ideas.

    Rules:
    - Never raises for empty inputs: returns [].
    - Deterministic ordering:
        - sort by requirement_id
        - then by idea "kind"/"category"
        - then by idea title hash
    - Deterministic IDs: TC-<REQ>-<KIND>-<HASH>

    Expected minimal fields (best-effort):
    - Requirement: requirement_id, title, description, criticality
    - TestIdea: requirement_id, title, description, kind/category, priority, rationale, tags
    - TestCase: test_id, title, description, linked_requirements_raw, steps, expected_results, priority, tags

    Returns:
        list[TestCase]
    """
    log = logger or _LOG

    if not requirements or not test_ideas:
        log.info("generate_test_pack: nothing to generate (requirements=%s, ideas=%s).", len(requirements or []), len(test_ideas or []))
        return []

    # Build a map for enrichment (req metadata)
    req_by_id: dict[str, Requirement] = {}
    for r in requirements:
        rid = str(_safe_get(r, "requirement_id", "")).strip()
        if rid:
            req_by_id[rid] = r

    # Filter ideas that point to known requirements (but keep unknown as "orphan ideas" if any)
    normalized_ideas: list[TestIdea] = []
    for idea in test_ideas:
        rid = str(_safe_get(idea, "requirement_id", "")).strip()
        if not rid:
            continue
        normalized_ideas.append(idea)

    if not normalized_ideas:
        log.warning("generate_test_pack: no valid ideas with requirement_id.")
        return []

    def _idea_sort_key(i: TestIdea) -> tuple[str, str, str]:
        rid = str(_safe_get(i, "requirement_id", "")).strip()
        kind = str(_safe_get(i, "kind", _safe_get(i, "category", "GENERIC"))).strip().upper()
        title = str(_safe_get(i, "title", "")).strip()
        return (rid, kind, _stable_hash(title, n=10))

    normalized_ideas.sort(key=_idea_sort_key)

    out: list[TestCase] = []
    seen_ids: set[str] = set()

    for idea in normalized_ideas:
        rid = str(_safe_get(idea, "requirement_id", "")).strip()
        req = req_by_id.get(rid)

        kind = str(_safe_get(idea, "kind", _safe_get(idea, "category", "GENERIC"))).strip().upper() or "GENERIC"
        idea_title = str(_safe_get(idea, "title", "")).strip() or "Untitled test idea"
        idea_desc = str(_safe_get(idea, "description", "")).strip()

        # Enrich title with req context lightly (recruiter-friendly)
        req_title = str(_safe_get(req, "title", "")).strip() if req else ""
        base_title = idea_title
        if req_title:
            base_title = f"{idea_title} — {req_title}"

        # Deterministic test_id
        rid_slug = _slugify(rid, max_len=24).upper().replace("-", "")
        kind_slug = _slugify(kind, max_len=12).upper().replace("-", "")
        token = _stable_hash(f"{rid}|{kind}|{idea_title}|{idea_desc}", n=8)
        test_id = f"TC-{rid_slug}-{kind_slug}-{token}"

        # Avoid collisions deterministically
        if test_id in seen_ids:
            token2 = _stable_hash(f"{rid}|{kind}|{idea_title}|{idea_desc}|dup", n=8)
            test_id = f"TC-{rid_slug}-{kind_slug}-{token2}"
        seen_ids.add(test_id)

        # Priority heuristics: use idea priority else derive from req criticality
        priority = str(_safe_get(idea, "priority", "")).strip().upper()
        if not priority and req:
            crit = str(_safe_get(req, "criticality", "")).strip().upper()
            priority = "HIGH" if crit in {"HIGH", "SAFETY", "ASIL", "DAL-A", "DALB", "SIL3", "SIL4"} else "MEDIUM"
        if not priority:
            priority = "MEDIUM"

        # Tags aggregation (stable order)
        tags: list[str] = []
        for t in (_safe_get(idea, "tags", []) or []):
            ts = str(t).strip()
            if ts:
                tags.append(ts)
        # Add kind + requirement id tags
        tags.extend([f"KIND:{kind}", f"REQ:{rid}"])
        # Dedup while keeping order
        tags_dedup: list[str] = []
        for t in tags:
            if t not in tags_dedup:
                tags_dedup.append(t)

        # Steps / Expected Results (simple, recruiter-friendly)
        # If TestIdea already contains steps, keep them; else build minimal scaffold.
        steps = _safe_get(idea, "steps", None)
        expected = _safe_get(idea, "expected_results", None)

        if not steps:
            steps = [
                "Prepare the system under test in a known initial state.",
                f"Apply the condition/scenario described in the idea: {idea_title}.",
                "Observe the system behavior and collect evidence (logs, outputs, states).",
            ]
        if not expected:
            expected = [
                "System behavior matches the expected requirement intent.",
                "No unexpected side effects are observed.",
            ]

        # Description (compact but auditable)
        rationale = str(_safe_get(idea, "rationale", "")).strip()
        desc_parts = []
        if idea_desc:
            desc_parts.append(idea_desc)
        if rationale:
            desc_parts.append(f"Rationale: {rationale}")
        if req:
            req_desc = str(_safe_get(req, "description", "")).strip()
            if req_desc:
                desc_parts.append(f"Requirement excerpt: {req_desc[:220]}")

        description = "\n".join(desc_parts).strip() or "Generated from test idea."

        payload: dict[str, Any] = {
            "test_id": test_id,
            "title": base_title,
            "description": description,
            # Keep raw linkage compatible with APP2 style
            "linked_requirements_raw": rid,
            "steps": steps,
            "expected_results": expected,
            "priority": priority,
            "tags": tags_dedup,
        }

        tc = _instantiate_testcase(payload)
        if tc is None:
            # Last-resort fallback: keep going without breaking pipeline
            log.warning("generate_test_pack: failed to instantiate TestCase for idea=%s (rid=%s).", idea_title, rid)
            continue

        out.append(tc)

    log.info("generate_test_pack: generated %s test cases from %s ideas.", len(out), len(normalized_ideas))
    return out
