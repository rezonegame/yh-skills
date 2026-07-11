from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg_finalize.path_safety import resolve_image_path


class SvgPathSafetyTests(unittest.TestCase):
    def test_allows_project_local_parent_image(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            svg_dir = root / "svg_output"
            image = root / "images" / "chart.png"
            svg_dir.mkdir()
            image.parent.mkdir()
            image.write_bytes(b"png")
            self.assertEqual(resolve_image_path("../images/chart.png", svg_dir, root), image)

    def test_blocks_absolute_and_escape_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            svg_dir = root / "svg_output"
            svg_dir.mkdir()
            outside = root.parent / "outside.png"
            outside.write_bytes(b"png")
            self.assertIsNone(resolve_image_path(str(outside), svg_dir, root))
            self.assertIsNone(resolve_image_path("../../outside.png", svg_dir, root))
            outside.unlink()


if __name__ == "__main__":
    unittest.main()
