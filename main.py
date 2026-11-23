#!/usr/bin/env python3
"""Deliver the 23 November 2026 front page to the runner's output folder.

The finished newspaper image lives in this repository as ``entry.png``
(it was drawn in this session by ``render_frontpage.py``). This script
only moves it: it reads the file, checks that it is a whole PNG inside
the competition's limits (at most 1024x1024 pixels, at most 1 MiB), and
writes an exact copy to ``/output/entry.png`` (or to the directory named
by ``MAKEFUN_OUTPUT_DIR`` when that is set).

Nothing is re-encoded, resized, or redrawn, so the page the judge sees
is byte for byte the page that was laid out here. The script uses only
the Python standard library and touches no network.
"""

import os
import shutil
import struct
import sys
from pathlib import Path

SOURCE = "entry.png"
OUTPUT_DIR = "/output"
MAX_BYTES = 1_048_576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"main.py: ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_png(path):
    """Confirm path holds a complete PNG within the size limits."""
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        fail(f"{path} is {len(data)} bytes, over the 1 MiB limit")
    if not data.startswith(PNG_MAGIC):
        fail(f"{path} does not start with the PNG signature")
    if len(data) < 24 or data[12:16] != b"IHDR":
        fail(f"{path} has no IHDR chunk where one belongs")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        fail(f"{path} is {width}x{height}, over the 1024x1024 limit")
    if not data.endswith(b"\x00\x00\x00\x00IEND\xaeB`\x82"):
        fail(f"{path} does not end with a proper IEND chunk")
    return len(data), width, height


def main():
    here = Path(__file__).resolve().parent
    source = here / SOURCE
    if not source.is_file():
        fail(f"cannot find {SOURCE} next to main.py")

    size, width, height = check_png(source)

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", OUTPUT_DIR))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / SOURCE
    shutil.copyfile(source, target)

    copied = target.stat().st_size
    if copied != size:
        fail(f"copy is {copied} bytes but the source is {size} bytes")
    print(f"main.py: wrote {target} ({width}x{height}, {size} bytes)")


if __name__ == "__main__":
    main()
