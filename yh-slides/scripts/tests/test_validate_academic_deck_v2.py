from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate_academic_deck import validate  # noqa: E402


def content(page_id: str, role: str, title: str) -> dict:
    return {
        "id": page_id,
        "role": role,
        "title": title,
        "purpose": f"Explain {role}",
        "audience_move": f"Understand {role}",
        "body_word_count": 20,
        "body_font_pt": 22,
        "estimated_seconds": 50,
    }


def v2_deck(mode: str = "structured_argument") -> dict:
    pages = [
        {"id": "cover", "role": "cover", "estimated_seconds": 20},
        content("context", "context", "Current onboarding loses one in three participants before week two."),
        content("question", "research_question", "We test whether a short intervention improves week-two retention."),
        content("finding", "results", "The intervention improved retention by 18 percentage points."),
        content("conclusion", "conclusions", "A short intervention is a low-cost way to retain more participants."),
        {"id": "refs", "role": "references", "estimated_seconds": 0},
        content("appendix-power", "appendix", "The study was powered to detect a ten-point retention change."),
    ]
    pages[1]["evidence"] = [{"kind": "claim", "original": False, "citation": "Lee, 2025"}]
    pages[3].update({
        "exhibits": ["retention chart"],
        "insight": "The effect survives cohort adjustment.",
        "annotation": "+18 pp after adjustment",
        "evidence": [{"kind": "data", "original": True}],
    })
    deck = {
        "schema": "yh_slides_academic_deck.v2",
        "mode": mode,
        "talk_type": "conference",
        "talk_minutes": 12,
        "narrative_spine": "scr",
        "main_claim": "A short intervention improves retention without increasing workload.",
        "accessibility": {
            "high_contrast": True,
            "color_independent": True,
            "acronyms_defined": True,
        },
        "pages": pages,
    }
    if mode == "structured_argument":
        deck["research_question"] = "Does a short intervention improve week-two retention?"
    return deck


class AcademicDeckV2Tests(unittest.TestCase):
    def test_valid_structured_deck(self) -> None:
        self.assertEqual(validate(v2_deck()), [])

    def test_visual_narrative_does_not_require_question_page(self) -> None:
        deck = v2_deck("visual_narrative")
        deck["pages"] = [page for page in deck["pages"] if page["role"] != "research_question"]
        self.assertEqual(validate(deck), [])

    def test_rejects_missing_question_and_result_annotation(self) -> None:
        deck = v2_deck()
        deck["pages"] = [page for page in deck["pages"] if page["role"] != "research_question"]
        next(page for page in deck["pages"] if page["role"] == "results").pop("annotation")
        errors = validate(deck)
        self.assertTrue(any("research_question page" in error for error in errors))
        self.assertTrue(any("so-what annotation" in error for error in errors))

    def test_rejects_uncited_evidence_and_references_after_appendix(self) -> None:
        deck = v2_deck()
        deck["pages"][1]["evidence"][0].pop("citation")
        refs = deck["pages"].pop(-2)
        deck["pages"].append(refs)
        errors = validate(deck)
        self.assertTrue(any("citation is required" in error for error in errors))
        self.assertTrue(any("before the appendix" in error for error in errors))

    def test_rejects_text_accessibility_and_timing_overruns(self) -> None:
        deck = v2_deck()
        deck["talk_minutes"] = 3
        deck["pages"][1].update({"body_word_count": 41, "body_font_pt": 18, "estimated_seconds": 200})
        errors = validate(deck)
        for fragment in ("40-word", "at least 20", "one-slide-per-minute", "speaking time"):
            self.assertTrue(any(fragment in error for error in errors), fragment)

    def test_rejects_generic_ending(self) -> None:
        deck = v2_deck()
        deck["pages"].append({"id": "thanks", "role": "contact", "title": "Thank You"})
        self.assertTrue(any("generic thank-you" in error for error in validate(deck)))
