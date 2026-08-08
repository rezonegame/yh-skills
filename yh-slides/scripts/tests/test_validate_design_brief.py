from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate_design_brief import validate  # noqa: E402


class DesignBriefTests(unittest.TestCase):
    def brief(self) -> dict:
        return {
            "title": "Decision review",
            "objective": "Align leadership",
            "audience": "Executive team",
            "canvas": {"aspect_ratio": "16:9"},
            "visual_system": {"mood": "calm, analytical", "typography": "humanist sans", "colour_roles": {"canvas": "warm white", "accent": "blue"}},
            "layout_principles": ["One claim per page", "Use contrast for hierarchy"],
            "pages": [{"id": "cover", "purpose": "Set decision", "audience_move": "Understand the choice"}, {"id": "evidence", "purpose": "Show evidence", "audience_move": "Trust the recommendation"}],
            "speaker_notes_strategy": "Explain implications, not copied slide text",
        }

    def plan(self) -> dict:
        return {"pages": [{"id": "cover"}, {"id": "evidence"}]}

    def test_valid_brief_matches_plan(self) -> None:
        self.assertEqual(validate(self.brief(), self.plan()), [])

    def test_rejects_drift_and_missing_audience_move(self) -> None:
        brief = self.brief()
        del brief["pages"][1]["audience_move"]
        brief["pages"][1]["id"] = "different"
        errors = validate(brief, self.plan())
        self.assertTrue(any("audience_move" in error for error in errors))
        self.assertTrue(any("exactly match" in error for error in errors))

    def test_requires_ai_image_strategy(self) -> None:
        brief = self.brief()
        brief["pages"][0]["has_ai_images"] = True
        errors = validate(brief)
        self.assertTrue(any("ai_image_strategy" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
