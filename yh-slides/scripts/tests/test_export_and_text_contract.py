from pathlib import Path
import sys
import tempfile
import unittest
from xml.etree import ElementTree as ET


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from export_contract import inspect_svg_sources, promote_export, resolve_output
from svg_to_pptx.drawingml_context import ConvertContext
from svg_to_pptx.drawingml_elements import convert_text
from svg_to_pptx.text_contract import text_direction, text_flow_mode, validate_bcp47
from validate_svg_text_contract import validate_file


class ExportAndTextContractTests(unittest.TestCase):
    def test_output_containment(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(resolve_output(root, "exports/deck.pptx"), (root / "exports/deck.pptx").resolve())
            with self.assertRaises(ValueError):
                resolve_output(root, "../deck.pptx")

    def test_image_provenance_and_remote_rejection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "image.png").write_bytes(b"png")
            svg = root / "slide.svg"
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg"><image href="image.png"/></svg>', encoding="utf-8")
            records = inspect_svg_sources(root, [svg])
            self.assertEqual(records[0]["images"][0]["source"], "image.png")
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg"><image href="https://example.com/a.png"/></svg>', encoding="utf-8")
            with self.assertRaises(ValueError):
                inspect_svg_sources(root, [svg])

    def test_transaction_rollback_and_valid_promotion(self):
        import zipfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            final = root / "deck.pptx"
            final.write_bytes(b"last-good")
            invalid = root / "invalid.pptx"
            invalid.write_bytes(b"not-a-zip")
            with self.assertRaises(ValueError):
                promote_export(invalid, final)
            self.assertEqual(final.read_bytes(), b"last-good")
            valid = root / "valid.pptx"
            with zipfile.ZipFile(valid, "w") as archive:
                archive.writestr("[Content_Types].xml", "types")
                archive.writestr("ppt/presentation.xml", "presentation")
            promote_export(valid, final)
            self.assertTrue(zipfile.is_zipfile(final))

    def test_bcp47_rtl_and_flow_modes(self):
        self.assertEqual(validate_bcp47("zh-hans-cn"), "zh-Hans-CN")
        self.assertEqual(text_direction("ar-SA"), "rtl")
        self.assertEqual(text_flow_mode(None), "preserve")
        self.assertEqual([text_flow_mode(x) for x in ("preserve", "reflow", "split")], ["preserve", "reflow", "split"])
        with self.assertRaises(ValueError):
            validate_bcp47("not_a_tag")

    def test_drawingml_emits_language_font_slots_rtl_and_reflow(self):
        element = ET.fromstring(
            '<text x="80" y="120" font-size="24" lang="ar-SA" dir="rtl" '
            'data-pptx-text-flow="reflow" data-pptx-font-latin="Arial" '
            'data-pptx-font-ea="Microsoft YaHei" '
            'data-pptx-font-cs="Traditional Arabic">مرحبا</text>'
        )
        result = convert_text(element, ConvertContext())
        self.assertIsNotNone(result)
        xml = result.xml
        self.assertIn('lang="ar-SA"', xml)
        self.assertIn('rtl="1"', xml)
        self.assertIn('wrap="square"', xml)
        self.assertIn('<a:latin typeface="Arial"/>', xml)
        self.assertIn('<a:ea typeface="Microsoft YaHei"/>', xml)
        self.assertIn('<a:cs typeface="Traditional Arabic"/>', xml)

    def test_cross_text_box_consistency(self):
        with tempfile.TemporaryDirectory() as tmp:
            svg = Path(tmp) / "slide.svg"
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg"><text data-pptx-flow-group="g" lang="ar" dir="rtl" data-pptx-text-flow="preserve">a</text><text data-pptx-flow-group="g" lang="en" data-pptx-text-flow="reflow">b</text></svg>', encoding="utf-8")
            self.assertTrue(any("inconsistent" in item for item in validate_file(svg)))


if __name__ == "__main__":
    unittest.main()
