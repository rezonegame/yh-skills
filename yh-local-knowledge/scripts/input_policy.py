"""Local-only screening policy for untrusted knowledge inputs."""
from __future__ import annotations

import zipfile
from pathlib import Path, PurePosixPath


MAX_ARCHIVE_MEMBERS = 500
MAX_ARCHIVE_BYTES = 250 * 1024 * 1024
MAX_ARCHIVE_DEPTH = 8
MAX_ARCHIVE_MEMBER_BYTES = 100 * 1024 * 1024
MAX_COMPRESSION_RATIO = 200
ARCHIVE_EXTENSIONS = {".zip", ".docx", ".pptx", ".xlsx", ".epub"}


def _within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _zip_error(path: Path) -> str | None:
    try:
        with zipfile.ZipFile(path) as archive:
            members = archive.infolist()
            if len(members) > MAX_ARCHIVE_MEMBERS:
                return f"archive has more than {MAX_ARCHIVE_MEMBERS} members"
            if sum(member.file_size for member in members) > MAX_ARCHIVE_BYTES:
                return f"archive expands beyond {MAX_ARCHIVE_BYTES} bytes"
            for member in members:
                member_path = PurePosixPath(member.filename.replace("\\", "/"))
                if member_path.is_absolute() or ".." in member_path.parts:
                    return "archive contains a path escape"
                if len(member_path.parts) > MAX_ARCHIVE_DEPTH:
                    return f"archive exceeds nesting depth {MAX_ARCHIVE_DEPTH}"
                if member.file_size > MAX_ARCHIVE_MEMBER_BYTES:
                    return f"archive member expands beyond {MAX_ARCHIVE_MEMBER_BYTES} bytes"
                if member.flag_bits & 0x1:
                    return "encrypted archive members are not permitted"
                compressed = max(member.compress_size, 1)
                if member.file_size > 1024 * 1024 and member.file_size / compressed > MAX_COMPRESSION_RATIO:
                    return f"archive member compression ratio exceeds {MAX_COMPRESSION_RATIO}:1"
    except (OSError, zipfile.BadZipFile) as exc:
        return f"invalid archive: {exc}"
    return None


def reject_reason(path: Path, source_root: Path) -> str | None:
    """Return a bounded rejection reason, or None when conversion may continue."""
    raw = str(path)
    if "://" in raw:
        return "remote URL inputs are not permitted"
    if not _within(path, source_root):
        return "path escapes the declared source root"
    if path.is_symlink():
        return "symlink inputs are not permitted"
    if path.suffix.lower() in ARCHIVE_EXTENSIONS:
        return _zip_error(path)
    return None
