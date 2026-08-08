#!/usr/bin/env python3
"""Validate the optional evidence-led yh-slides academic-deck contract."""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path


SCHEMA_V2 = "yh_slides_academic_deck.v2"
MODES = {"structured_argument", "visual_narrative"}
NARRATIVE_SPINES = {"scr", "funnel_answer", "answer_first"}
TALK_TYPES = {
    "conference", "seminar", "thesis_defense", "grant", "lab_meeting",
    "invited_lecture", "policy_briefing", "public_engagement",
}
NON_SUBSTANTIVE = {"cover", "section", "references", "contact", "closing"}
V2_ROLES = NON_SUBSTANTIVE | {
    "context", "research_question", "methods", "results", "discussion",
    "implications", "conclusions", "appendix",
}
TOPIC_LABELS = {
    "background", "method", "methods", "results", "discussion", "conclusion",
    "conclusions", "references", "参考文献", "背景", "方法", "结果", "讨论", "结论",
}
EMPTY_ENDINGS = {
    "thank you", "thank you!", "thanks", "q&a", "questions?",
    "谢谢", "谢谢！", "感谢聆听", "问答",
}


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _action_title(value: str) -> bool:
    title = value.strip()
    if title.lower() in TOPIC_LABELS or title in TOPIC_LABELS:
        return False
    return bool(re.search(r"[。！？.!?]$", title)) or len(re.sub(r"\s+", "", title)) >= 10


def _valid_sources(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(_text(item) for item in value)


def _validate_v2_top_level(data: dict, errors: list[str]) -> None:
    if data.get("mode") not in MODES:
        errors.append(f"mode must be one of: {', '.join(sorted(MODES))}")
    if data.get("narrative_spine") not in NARRATIVE_SPINES:
        errors.append(f"narrative_spine must be one of: {', '.join(sorted(NARRATIVE_SPINES))}")
    if data.get("talk_type") not in TALK_TYPES:
        errors.append(f"talk_type must be one of: {', '.join(sorted(TALK_TYPES))}")
    if not _number(data.get("talk_minutes")) or data["talk_minutes"] <= 0:
        errors.append("talk_minutes must be a positive number")
    if not _text(data.get("main_claim")):
        errors.append("main_claim must be a non-empty string")
    if data.get("mode") == "structured_argument" and not _text(data.get("research_question")):
        errors.append("structured_argument mode requires research_question")

    accessibility = data.get("accessibility")
    if not isinstance(accessibility, dict):
        errors.append("accessibility must be an object")
    else:
        for field in ("high_contrast", "color_independent", "acronyms_defined"):
            if accessibility.get(field) is not True:
                errors.append(f"accessibility.{field} must be true")


def validate(data: object, deck_plan: object | None = None) -> list[str]:
    if not isinstance(data, dict):
        return ["academic deck must be a JSON object"]
    errors: list[str] = []
    is_v2 = data.get("schema") == SCHEMA_V2
    if data.get("schema") not in (None, SCHEMA_V2):
        errors.append(f"schema must be {SCHEMA_V2}")
    if is_v2:
        _validate_v2_top_level(data, errors)

    pages = data.get("pages")
    if not isinstance(pages, list) or not pages:
        return errors + ["pages must be a non-empty list"]

    ids: list[str] = []
    saw_source = False
    timed_seconds = 0.0
    research_question_indices: list[int] = []
    conclusion_indices: list[int] = []
    reference_indices: list[int] = []
    appendix_indices: list[int] = []
    live_slide_count = 0

    for number, page in enumerate(pages, 1):
        prefix = f"pages[{number}]"
        if not isinstance(page, dict):
            errors.append(f"{prefix} must be an object")
            continue
        role = page.get("role")
        if not _text(page.get("id")):
            errors.append(f"{prefix}.id must be a non-empty string")
        else:
            if page["id"] in ids:
                errors.append(f"{prefix}.id duplicates {page['id']}")
            ids.append(page["id"])
        if not _text(role):
            errors.append(f"{prefix}.role must be a non-empty string")
            continue
        if is_v2 and role not in V2_ROLES:
            errors.append(f"{prefix}.role is not supported by academic deck v2: {role}")

        if role not in NON_SUBSTANTIVE:
            for field in ("title", "purpose", "audience_move"):
                if not _text(page.get(field)):
                    errors.append(f"{prefix}.{field} must be a non-empty string")
            if _text(page.get("title")) and not _action_title(page["title"]):
                errors.append(f"{prefix}.title must be an action title, not a topic label")

        if role == "research_question":
            research_question_indices.append(number - 1)
        elif role == "conclusions":
            conclusion_indices.append(number - 1)
        elif role == "references":
            reference_indices.append(number - 1)
        elif role == "appendix":
            appendix_indices.append(number - 1)

        if role not in {"references", "appendix"}:
            live_slide_count += 1

        if role == "results":
            exhibits = page.get("exhibits")
            if not isinstance(exhibits, list) or len(exhibits) != 1:
                errors.append(f"{prefix}.results requires exactly one primary exhibit")
            if not _text(page.get("insight")):
                errors.append(f"{prefix}.results requires a concrete insight")
            if is_v2 and not _text(page.get("annotation")):
                errors.append(f"{prefix}.results requires a so-what annotation")

        borrowed_flags = any(
            page.get(field) is True
            for field in ("borrowed_figure", "borrowed_claim", "borrowed_data")
        )
        if borrowed_flags:
            if not _valid_sources(page.get("sources")):
                errors.append(f"{prefix}.borrowed content requires non-empty sources")
            saw_source = True

        evidence = page.get("evidence")
        if evidence is not None:
            if not isinstance(evidence, list):
                errors.append(f"{prefix}.evidence must be a list")
            else:
                for evidence_number, item in enumerate(evidence, 1):
                    evidence_prefix = f"{prefix}.evidence[{evidence_number}]"
                    if not isinstance(item, dict):
                        errors.append(f"{evidence_prefix} must be an object")
                        continue
                    if item.get("original") is False:
                        saw_source = True
                        if not _text(item.get("citation")):
                            errors.append(f"{evidence_prefix}.citation is required for non-original evidence")

        if page.get("sources"):
            saw_source = True

        if is_v2:
            if "body_word_count" in page:
                count = page.get("body_word_count")
                if not isinstance(count, int) or isinstance(count, bool) or count < 0:
                    errors.append(f"{prefix}.body_word_count must be a non-negative integer")
                elif count > 40:
                    errors.append(f"{prefix}.body_word_count exceeds the 40-word academic budget")
            if "body_font_pt" in page:
                font_size = page.get("body_font_pt")
                if not _number(font_size) or font_size < 20:
                    errors.append(f"{prefix}.body_font_pt must be at least 20")
            if "estimated_seconds" in page:
                seconds = page.get("estimated_seconds")
                if not _number(seconds) or seconds < 0:
                    errors.append(f"{prefix}.estimated_seconds must be a non-negative number")
                else:
                    timed_seconds += float(seconds)

    if saw_source:
        if not reference_indices:
            errors.append("a sourced deck must include a references page")
        elif appendix_indices and max(reference_indices) > min(appendix_indices):
            errors.append("the references page must appear before the appendix")

    if is_v2:
        if len(reference_indices) > 1:
            errors.append("academic deck v2 allows only one references page")
        if appendix_indices:
            first_appendix = min(appendix_indices)
            if any(
                isinstance(page, dict) and page.get("role") != "appendix"
                for page in pages[first_appendix:]
            ):
                errors.append("appendix pages must form the final contiguous block")
        if len(conclusion_indices) != 1:
            errors.append("academic deck v2 requires exactly one conclusions page")
        elif any(
            isinstance(page, dict) and page.get("role") not in {"contact", "references", "appendix"}
            for page in pages[conclusion_indices[0] + 1:]
        ):
            errors.append("conclusions must be the last argumentative page")
        if data.get("mode") == "structured_argument":
            if len(research_question_indices) != 1:
                errors.append("structured_argument mode requires exactly one research_question page")
            else:
                substantive = [
                    index for index, page in enumerate(pages)
                    if isinstance(page, dict) and page.get("role") not in NON_SUBSTANTIVE
                ]
                if research_question_indices[0] not in substantive[:3]:
                    errors.append("research_question must appear within the first three substantive pages")
        if pages and isinstance(pages[-1], dict):
            ending = str(pages[-1].get("title", "")).strip().lower()
            if ending in EMPTY_ENDINGS:
                errors.append("do not end an academic deck with a generic thank-you or Q&A slide")
        talk_minutes = data.get("talk_minutes")
        if _number(talk_minutes) and talk_minutes > 0:
            if live_slide_count > math.ceil(float(talk_minutes)):
                errors.append("live slide count exceeds the one-slide-per-minute ceiling")
            if timed_seconds > float(talk_minutes) * 60:
                errors.append("estimated speaking time exceeds talk_minutes")

    if deck_plan is not None:
        plan_pages = deck_plan.get("pages") if isinstance(deck_plan, dict) else None
        plan_ids = [
            page.get("id") for page in plan_pages
            if isinstance(page, dict) and _text(page.get("id"))
        ] if isinstance(plan_pages, list) else []
        if ids != plan_ids:
            errors.append("academic deck page IDs must match deck-plan IDs and order")
    return errors


def _read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="validate yh-slides academic-deck.json")
    parser.add_argument("deck", type=Path)
    parser.add_argument("--deck-plan", type=Path)
    args = parser.parse_args()
    try:
        errors = validate(_read(args.deck), _read(args.deck_plan) if args.deck_plan else None)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read contract: {exc}")
        return 2
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK: academic deck contract validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
