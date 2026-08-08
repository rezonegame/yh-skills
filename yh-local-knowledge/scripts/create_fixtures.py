#!/usr/bin/env python3
"""Generate adversarial test fixtures for scan_input_policy.py."""
import os
import zipfile
import tarfile
import io
import struct

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fixtures", "security")
os.makedirs(FIXTURES_DIR, exist_ok=True)

# 1. zip-nesting.zip: 4 levels deep (exceeds limit of 3)
def make_nested_zip():
    # Create innermost zip
    buf4 = io.BytesIO()
    with zipfile.ZipFile(buf4, 'w') as zf:
        zf.writestr("deep/file.txt", "I am very deep")
    data4 = buf4.getvalue()

    # Wrap level 3
    buf3 = io.BytesIO()
    with zipfile.ZipFile(buf3, 'w') as zf:
        zf.writestr("level3.zip", data4)
    data3 = buf3.getvalue()

    # Wrap level 2
    buf2 = io.BytesIO()
    with zipfile.ZipFile(buf2, 'w') as zf:
        zf.writestr("level2.zip", data3)
    data2 = buf2.getvalue()

    # Wrap level 1 (outermost)
    path = os.path.join(FIXTURES_DIR, "zip-nesting.zip")
    with zipfile.ZipFile(path, 'w') as zf:
        zf.writestr("level1.zip", data2)
    print(f"Created {path} (4 nested levels)")

# 2. excessive-files.zip: >500 files
def make_excessive_files_zip():
    path = os.path.join(FIXTURES_DIR, "excessive-files.zip")
    with zipfile.ZipFile(path, 'w') as zf:
        for i in range(501):
            zf.writestr(f"file_{i:04d}.txt", f"content of file {i}")
    print(f"Created {path} (501 files)")

# 3. path-escape.tar.gz: contains ../../etc/passwd
def make_path_escape_tar():
    path = os.path.join(FIXTURES_DIR, "path-escape.tar.gz")
    with tarfile.open(path, 'w:gz') as tf:
        data = b"root:x:0:0:root:/root:/bin/bash\n"
        info = tarfile.TarInfo(name="../../etc/passwd")
        info.size = len(data)
        tf.addfile(info, io.BytesIO(data))
    print(f"Created {path} (path traversal)")

# 4. unsupported-binary.bin: OLE compound document (magic bytes)
def make_ole_binary():
    path = os.path.join(FIXTURES_DIR, "unsupported-binary.bin")
    # OLE magic + padding
    ole_magic = b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1'
    with open(path, 'wb') as f:
        f.write(ole_magic)
        f.write(b'\x00' * 512)  # padding to look like a real file
    print(f"Created {path} (OLE magic bytes)")

if __name__ == "__main__":
    make_nested_zip()
    make_excessive_files_zip()
    make_path_escape_tar()
    make_ole_binary()
    print("All fixtures created.")
