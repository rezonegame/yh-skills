from pathlib import Path
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from template_specs import PRIORITY_LOW_TO_HIGH, build_spec_stack, effective_text


class TemplateSpecTests(unittest.TestCase):
    def test_priority_and_source_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = {}
            for role in PRIORITY_LOW_TO_HIGH:
                path = root / f"{role}.md"
                path.write_text(role, encoding="utf-8")
                paths[role] = path
            stack = build_spec_stack(
                upstream_default=paths["upstream-default"],
                style=paths["style"],
                layout=paths["layout"],
                brand=paths["brand"],
                project_explicit=paths["project-explicit"],
            )
            self.assertEqual([layer.role for layer in stack], list(PRIORITY_LOW_TO_HIGH))
            text = effective_text(stack)
            self.assertEqual(text.count("spec-layer:"), 5)
            self.assertGreater(text.index("project-explicit"), text.index("brand"))

    def test_missing_spec_fails_closed(self):
        with self.assertRaises(FileNotFoundError):
            build_spec_stack(style=Path("missing-style.md"))


if __name__ == "__main__":
    unittest.main()
