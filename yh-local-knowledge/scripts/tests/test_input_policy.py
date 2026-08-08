from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import input_policy  # noqa: E402


class InputPolicyTests(unittest.TestCase):
    def test_rejects_escape_and_nested_archive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "inbox"
            root.mkdir()
            outside = Path(tmp) / "outside.pdf"
            outside.write_bytes(b"x")
            self.assertIn("escapes", input_policy.reject_reason(outside, root) or "")
            archive = root / "nested.zip"
            with zipfile.ZipFile(archive, "w") as zf:
                zf.writestr("/".join(["d"] * 9) + "/file.txt", "x")
            self.assertIn("nesting", input_policy.reject_reason(archive, root) or "")

    def test_allows_regular_local_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "inbox"
            root.mkdir()
            source = root / "note.pdf"
            source.write_bytes(b"x")
            self.assertIsNone(input_policy.reject_reason(source, root))

    def test_checks_zip_based_document_formats(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "inbox"
            root.mkdir()
            source = root / "oversized.docx"
            with zipfile.ZipFile(source, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("word/document.xml", b"x" * (2 * 1024 * 1024))
            self.assertIn("compression ratio", input_policy.reject_reason(source, root) or "")

    def test_rejects_archive_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "inbox"
            root.mkdir()
            source = root / "escape.epub"
            with zipfile.ZipFile(source, "w") as zf:
                zf.writestr("../outside.txt", "x")
            self.assertIn("path escape", input_policy.reject_reason(source, root) or "")
