from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate_deck_plan import validate  # noqa: E402


class DeckPlanTests(unittest.TestCase):
    def valid_plan(self) -> dict:
        return {"title": "Market review", "goal": "Explain the decision", "audience": "Leadership", "route": "2A-S", "pages": [{"id": "cover", "role": "cover", "title": "Decision", "copy": "The recommendation", "layout_id": "cover"}, {"id": "evidence", "role": "evidence", "title": "Evidence", "copy": "Demand increased", "layout_id": "evidence", "chart_data": [1, 2], "insight": "Demand is rising"}]}

    def test_valid_plan(self) -> None:
        self.assertEqual(validate(self.valid_plan(), None), [])

    def test_rejects_template_copy_and_duplicate_layout(self) -> None:
        plan = self.valid_plan()
        plan["pages"][1]["copy"] = "AI Capital roadmap"
        plan["pages"][1]["layout_id"] = "cover"
        errors = validate(plan, None)
        self.assertTrue(any("template marker" in error for error in errors))
        self.assertTrue(any("duplicates cover" in error for error in errors))

    def test_rejects_escaped_media_and_missing_insight(self) -> None:
        plan = self.valid_plan()
        plan["pages"][1]["media"] = [{"path": "../secret.png"}]
        del plan["pages"][1]["insight"]
        errors = validate(plan, None)
        self.assertTrue(any("safe relative" in error for error in errors))
        self.assertTrue(any("no insight" in error for error in errors))

    def test_accepts_capacity_aware_layout_candidates(self) -> None:
        plan = self.valid_plan()
        page = plan["pages"][1]
        page["layout_candidates"] = [
            {"id": "evidence", "family": "chart-led"},
            {"id": "evidence-split", "family": "split"},
        ]
        page["content_package"] = {"required_facts": ["Demand increased"]}
        self.assertEqual(validate(plan, None), [])

    def test_rejects_weak_layout_candidate_set(self) -> None:
        plan = self.valid_plan()
        page = plan["pages"][1]
        page["layout_candidates"] = [
            {"id": "other", "family": "split"},
            {"id": "other-2", "family": "split"},
        ]
        errors = validate(plan, None)
        self.assertTrue(any("at least two" in error for error in errors))
        self.assertTrue(any("must be one of" in error for error in errors))
        self.assertTrue(any("content_package" in error for error in errors))
