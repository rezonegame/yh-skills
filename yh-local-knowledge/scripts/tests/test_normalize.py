from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import normalize


class NormalizeTests(unittest.TestCase):
    def test_output_paths_do_not_collide(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            a = workspace / "one" / "report.pdf"
            b = workspace / "two" / "report.pdf"
            a.parent.mkdir()
            b.parent.mkdir()
            a.write_bytes(b"a")
            b.write_bytes(b"b")
            self.assertNotEqual(normalize._out_path(workspace, a), normalize._out_path(workspace, b))

    def test_hash_cache_requires_source_match(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            source = workspace / "原始资料" / "report.pdf"
            source.parent.mkdir()
            source.write_bytes(b"v1")
            out = normalize._out_path(workspace, source)
            cache = normalize._cache_path(out)
            normalize._atomic_write_text(out, "converted")
            converter = normalize.Converters()
            expected = normalize._cache_payload(source, normalize._file_sha256(source), converter)
            normalize._atomic_write_text(cache, json.dumps(expected))
            self.assertTrue(normalize._cache_is_valid(out, cache, expected))
            source.write_bytes(b"v2")
            changed = normalize._cache_payload(source, normalize._file_sha256(source), converter)
            self.assertFalse(normalize._cache_is_valid(out, cache, changed))


if __name__ == "__main__":
    unittest.main()
