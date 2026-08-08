from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from artifact_contract import candidate_path, discard_candidate, promote_candidate, validate_delivery_brief, validate_required_files
from release_gate import validate_manifest


class ArtifactContractTests(unittest.TestCase):
    def test_complete_brief_and_assets_pass(self):
        brief = {"audience":"leaders","language":"zh-CN","template":"report","output_format":"pdf","acceptance_check":"render","capabilities":{"weasyprint":True}}
        self.assertEqual(validate_delivery_brief(brief), [])
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "asset.txt").write_text("ok", encoding="utf-8")
            self.assertEqual(validate_required_files(root, ["asset.txt"]), [])

    def test_missing_asset_and_path_escape_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            errors = validate_required_files(Path(tmp), ["missing.txt", "missing-screenshot.png", "../escape.txt"])
            self.assertTrue(any("missing" in item for item in errors))
            self.assertTrue(any("escapes" in item for item in errors))

    def test_failed_render_preserves_last_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            final = Path(tmp) / "report.pdf"
            final.write_bytes(b"last-good")
            candidate = candidate_path(final)
            candidate.write_bytes(b"bad")
            with self.assertRaises(ValueError):
                promote_candidate(candidate, final, validator=lambda _: ["render failed"])
            discard_candidate(candidate)
            self.assertEqual(final.read_bytes(), b"last-good")

    def test_successful_candidate_is_atomic_replacement(self):
        with tempfile.TemporaryDirectory() as tmp:
            final = Path(tmp) / "report.pdf"
            final.write_bytes(b"old")
            candidate = candidate_path(final)
            candidate.write_bytes(b"new")
            promote_candidate(candidate, final)
            self.assertEqual(final.read_bytes(), b"new")
            self.assertFalse(candidate.exists())

    def test_release_identity_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            (root / "SKILL.md").write_text("skill", encoding="utf-8")
            (root / "evidence.txt").write_text("ok", encoding="utf-8")
            with zipfile.ZipFile(root / "package.zip", "w") as archive:
                archive.writestr("SKILL.md", "skill")
            package_hash = hashlib.sha256((root / "package.zip").read_bytes()).hexdigest()
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "fixture"], check=True)
            manifest = {"identity":{"name":"wrong-name","version":"1","git_sha":"0"*40},"package":{"path":"package.zip","sha256":package_hash,"required_members":["SKILL.md"]},"required_files":["SKILL.md"],"validation_evidence":["evidence.txt"]}
            errors = validate_manifest(manifest, root)
            self.assertTrue(any("name mismatch" in item for item in errors))
            self.assertTrue(any("Git SHA mismatch" in item for item in errors))

    def test_release_identity_package_and_evidence_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            (root / "SKILL.md").write_text("skill", encoding="utf-8")
            (root / "evidence.txt").write_text("ok", encoding="utf-8")
            with zipfile.ZipFile(root / "package.zip", "w") as archive:
                archive.writestr("SKILL.md", "skill")
            package_hash = hashlib.sha256((root / "package.zip").read_bytes()).hexdigest()
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "fixture"], check=True)
            commit = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=True, capture_output=True, text=True,
            ).stdout.strip()
            manifest = {
                "identity": {"name": "yh-document-studio", "version": "1", "git_sha": commit},
                "package": {"path": "package.zip", "sha256": package_hash, "required_members": ["SKILL.md"]},
                "required_files": ["SKILL.md"],
                "validation_evidence": ["evidence.txt"],
            }
            self.assertEqual(validate_manifest(manifest, root), [])


if __name__ == "__main__":
    unittest.main()
