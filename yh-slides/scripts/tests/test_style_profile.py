from __future__ import annotations

import sys
import unittest
import json
import os
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate_style_profile import validate  # noqa: E402
from load_style_profile import load  # noqa: E402


class StyleProfileTests(unittest.TestCase):
    def profile(self) -> dict:
        return {"palette": {"canvas": "warm white", "accent": "ink blue"}, "typography": "editorial serif title", "density": "calm", "preferred_route": "2A"}

    def test_valid_profile(self) -> None:
        self.assertEqual(validate(self.profile()), [])

    def test_rejects_secret_and_conflict(self) -> None:
        profile = self.profile()
        profile["api_key"] = "nope"
        errors = validate(profile, "2C")
        self.assertTrue(any("forbidden" in error for error in errors))
        self.assertTrue(any("conflicts" in error for error in errors))

    def test_loader_requires_explicit_absolute_environment_path(self) -> None:
        previous = os.environ.get("YH_SLIDES_STYLE_PROFILE")
        try:
            os.environ["YH_SLIDES_STYLE_PROFILE"] = "relative.json"
            with self.assertRaises(ValueError):
                load()
            with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
                json.dump(self.profile(), handle)
                profile_path = handle.name
            os.environ["YH_SLIDES_STYLE_PROFILE"] = profile_path
            self.assertEqual(load()["preferred_route"], "2A")
        finally:
            if previous is None:
                os.environ.pop("YH_SLIDES_STYLE_PROFILE", None)
            else:
                os.environ["YH_SLIDES_STYLE_PROFILE"] = previous
            if 'profile_path' in locals():
                Path(profile_path).unlink(missing_ok=True)
