from pathlib import Path
import json
import sys
import unittest


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
from validate_presenter_mode import validate_presenter


def html(notes, ids=("opening", "evidence"), budget=120, runtime=True, recovery=True):
    contract = {
        "talk_budget_seconds": budget,
        "runtime_features": ["audience-connection", "heartbeat-timeout", "recovery", "end-mask", "notes-persistence"] if runtime else [],
        "recovery": {"heartbeat_seconds": 2, "timeout_seconds": 8, "resume_token": "deck-session"} if recovery else {},
        "notes": notes,
    }
    slides = "".join(f'<section data-slide-id="{value}"></section>' for value in ids)
    return slides + '<script id="speaker-notes" type="application/json">' + json.dumps(contract) + '</script>'


def note(id, talk=50):
    return {"id":id,"title":id,"purpose":"explain","talking_points":["one"],"transition":"next","talk_seconds":talk,"interaction":[],"fallback":"short version","pronunciation":[]}


class PresenterModeTests(unittest.TestCase):
    def test_valid_contract(self):
        errors, _ = validate_presenter(html([note("opening"), note("evidence")]))
        self.assertEqual(errors, [])

    def test_duplicate_id(self):
        errors, _ = validate_presenter(html([note("opening"), note("opening")], ids=("opening", "opening")))
        self.assertTrue(any("duplicate" in item for item in errors))

    def test_missing_notes_and_order(self):
        errors, _ = validate_presenter(html([note("evidence")]))
        self.assertTrue(any("count/order" in item for item in errors))

    def test_budget_and_auto_advance_confusion(self):
        bad = note("opening", talk=130)
        bad["duration"] = 10
        errors, _ = validate_presenter(html([bad, note("evidence")], budget=120))
        self.assertTrue(any("ambiguous" in item for item in errors))
        self.assertTrue(any("exceeds budget" in item for item in errors))

    def test_missing_runtime_recovery(self):
        errors, _ = validate_presenter(html([note("opening"), note("evidence")], runtime=False, recovery=False))
        self.assertTrue(any("runtime contract" in item for item in errors))
        self.assertTrue(any("recovery" in item for item in errors))

    def test_low_budget_warning(self):
        errors, warnings = validate_presenter(html([note("opening", 10), note("evidence", 10)], budget=120))
        self.assertEqual(errors, [])
        self.assertTrue(warnings)


if __name__ == "__main__":
    unittest.main()
