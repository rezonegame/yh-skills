from __future__ import annotations
import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_asset_intent import validate

class AssetIntentTests(unittest.TestCase):
    def test_edit_requires_invariants(self):
        self.assertTrue(any("immutable" in x for x in validate({"operation":"edit","consumer":"deck","destination":"assets/a-v2.png","inputs":["a.png"]})))
    def test_valid_generate(self):
        self.assertEqual(validate({"operation":"generate","consumer":"deck","destination":"assets/a-v2.png"}), [])
