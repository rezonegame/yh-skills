from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate_academic_deck import validate  # noqa: E402


class AcademicDeckTests(unittest.TestCase):
    def deck(self) -> dict:
        return {"pages": [
            {"id": "cover", "role": "cover"},
            {"id": "finding", "role": "results", "title": "The intervention improved retention by 18 percentage points.", "purpose": "Show the result", "audience_move": "Trust the effect", "exhibits": ["retention chart"], "insight": "The effect persists after cohort adjustment.", "borrowed_figure": True, "sources": ["doi:10/example"]},
            {"id": "refs", "role": "references"}
        ]}

    def test_valid_research_deck(self) -> None:
        plan = {"pages": [{"id": "cover"}, {"id": "finding"}, {"id": "refs"}]}
        self.assertEqual(validate(self.deck(), plan), [])

    def test_rejects_topic_title_and_missing_source(self) -> None:
        deck = self.deck()
        deck["pages"][1]["title"] = "Results"
        deck["pages"][1]["sources"] = []
        errors = validate(deck)
        self.assertTrue(any("action title" in error for error in errors))
        self.assertTrue(any("sources" in error for error in errors))

    def test_rejects_multiple_exhibits_and_plan_drift(self) -> None:
        deck = self.deck()
        deck["pages"][1]["exhibits"].append("table")
        errors = validate(deck, {"pages": [{"id": "cover"}]})
        self.assertTrue(any("exactly one" in error for error in errors))
        self.assertTrue(any("must match" in error for error in errors))
