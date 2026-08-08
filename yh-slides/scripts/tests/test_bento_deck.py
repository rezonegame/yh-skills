from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
from create_bento_deck import DOC_RE, to_bento_document  # noqa: E402
from extract_bento_comments import extract  # noqa: E402
from validate_bento_deck import validate  # noqa: E402


def plan() -> dict:
    return {
        "schema": "yh_slides_bento_deck.v1",
        "title": "Test deck",
        "slides": [
            {
                "id": "one",
                "name": "One",
                "notes": "Say hello.",
                "elements": [{"id": "title", "type": "text", "x": 20, "y": 20, "w": 800, "h": 100, "html": "<b>Hello</b>"}],
            },
            {
                "id": "two",
                "name": "Two",
                "notes": "Explain the change.",
                "transition": "morph",
                "elements": [{"id": "title", "type": "text", "x": 20, "y": 60, "w": 800, "h": 100, "html": "<b>Changed</b>"}],
            },
        ],
    }


class BentoDeckTests(unittest.TestCase):
    def test_valid_plan_and_deck_plan_alignment(self) -> None:
        self.assertEqual(validate(plan(), {"pages": [{"id": "one"}, {"id": "two"}]}), [])

    def test_rejects_remote_image_and_invalid_morph(self) -> None:
        invalid = plan()
        invalid["slides"][1]["elements"][0]["id"] = "new-title"
        invalid["slides"][0]["elements"].append({"id": "image", "type": "image", "x": 1, "y": 1, "w": 10, "h": 10, "src": "https://example.test/a.png"})
        errors = validate(invalid)
        self.assertTrue(any("remote src" in error for error in errors))
        self.assertTrue(any("morph transition" in error for error in errors))

    def test_serialized_doc_escapes_script_breakout_and_comments_extract(self) -> None:
        doc = to_bento_document(plan())
        doc["slides"][0]["comments"] = [{"body": "tighten opening"}]
        encoded = json.dumps(doc, ensure_ascii=False).replace("<", "\\u003c")
        self.assertNotIn("</script>", encoded.lower())
        shell = '<script type="application/bento+json" id="bento-doc"></script>'
        rendered, count = DOC_RE.subn(lambda m: f"{m.group(1)}{encoded}{m.group(3)}", shell)
        self.assertEqual(count, 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "deck.bento.html"
            path.write_text(rendered, encoding="utf-8")
            result = extract(path)
        self.assertEqual(result["comments"][0]["slide_id"], "one")
        self.assertEqual(result["comments"][0]["comment"]["body"], "tighten opening")
