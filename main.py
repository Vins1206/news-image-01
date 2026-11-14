#!/usr/bin/env python3
"""news-image-01 entry: THE WORLD TODAY, Friday 13 November 2026.

The artwork lives next to this file as ``art.png``: a one-page newspaper
front page that sums up the world news of Friday 13 November 2026 in six
illustrated panels plus a footer strip.

This program is deliberately boring. It validates the bundled image
against the competition gate (a whole PNG or JPEG, at most 1 MiB, at
most 1024 x 1024 pixels) and then copies it byte-for-byte to
``entry.png`` inside the output directory. The output directory is
``$MAKEFUN_OUTPUT_DIR`` when that variable is set, otherwise
``/output``. Running the program twice produces byte-identical output,
because the copy is exact and nothing is re-encoded.

Standard library only. No network access is needed or used.
"""

import os
import struct
import sys
import zlib
from pathlib import Path

MAX_BYTES = 1_048_576  # 1 MiB hard limit from the competition gate
MAX_WIDTH = 1024
MAX_HEIGHT = 1024

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_SOI = b"\xff\xd8"

# JPEG markers that carry no length field of their own.
JPEG_STANDALONE = {0x01, 0xD8, 0xD9} | set(range(0xD0, 0xD8))
# Start-of-frame markers whose segment holds the picture dimensions.
JPEG_SOF = {
    0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
    0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
}


def fail(message):
    """Print an error to stderr and exit nonzero."""
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_png(data):
    """Walk every PNG chunk, verify each CRC, return (width, height)."""
    pos = len(PNG_SIGNATURE)
    width = None
    height = None
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            fail("art.png: truncated PNG chunk header")
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        chunk_type = data[pos + 4:pos + 8]
        chunk_end = pos + 8 + length + 4
        if chunk_end > len(data):
            fail("art.png: PNG chunk overruns the file")
        body = data[pos + 8:pos + 8 + length]
        stored_crc = struct.unpack(
            ">I", data[pos + 8 + length:chunk_end]
        )[0]
        actual_crc = zlib.crc32(chunk_type + body) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            fail(f"art.png: bad CRC in PNG chunk {chunk_type!r}")
        if chunk_type == b"IHDR":
            if length != 13:
                fail("art.png: IHDR chunk is not 13 bytes")
            width, height = struct.unpack(">II", body[0:8])
        if chunk_type == b"IEND":
            seen_iend = True
            pos = chunk_end
            break
        pos = chunk_end
    if width is None:
        fail("art.png: no IHDR chunk found")
    if not seen_iend:
        fail("art.png: no IEND chunk found")
    if pos != len(data):
        fail("art.png: trailing bytes after the IEND chunk")
    return width, height


def check_jpeg(data):
    """Walk JPEG segments to the end marker, return (width, height)."""
    if not data.endswith(b"\xff\xd9"):
        fail("art.png: JPEG does not end with the EOI marker")
    pos = 2
    width = None
    height = None
    while pos < len(data):
        if data[pos] != 0xFF:
            fail("art.png: JPEG segment does not start with 0xFF")
        marker = data[pos + 1]
        pos += 2
        if marker in JPEG_STANDALONE:
            continue
        if pos + 2 > len(data):
            fail("art.png: truncated JPEG segment")
        seg_len = struct.unpack(">H", data[pos:pos + 2])[0]
        if seg_len < 2 or pos + seg_len > len(data):
            fail("art.png: JPEG segment overruns the file")
        if marker in JPEG_SOF and width is None:
            if seg_len < 7:
                fail("art.png: short JPEG frame header")
            height = struct.unpack(">H", data[pos + 3:pos + 5])[0]
            width = struct.unpack(">H", data[pos + 5:pos + 7])[0]
        if marker == 0xDA:
            break
        pos += seg_len
    if width is None:
        fail("art.png: no JPEG frame header found")
    return width, height


def validate(data):
    """Enforce the gate limits on the raw bytes; return a summary."""
    if len(data) == 0:
        fail("art.png: file is empty")
    if len(data) > MAX_BYTES:
        fail(f"art.png: {len(data)} bytes exceeds the 1 MiB limit")
    if data.startswith(PNG_SIGNATURE):
        width, height = check_png(data)
        kind = "PNG"
    elif data.startswith(JPEG_SOI):
        width, height = check_jpeg(data)
        kind = "JPEG"
    else:
        fail("art.png: not a PNG or JPEG (bad magic bytes)")
    if not (1 <= width <= MAX_WIDTH and 1 <= height <= MAX_HEIGHT):
        fail(f"art.png: dimensions {width}x{height} exceed 1024x1024")
    return kind, width, height


def main():
    here = Path(__file__).resolve().parent
    source = here / "art.png"
    if not source.is_file():
        fail(f"art.png not found next to main.py in {here}")
    data = source.read_bytes()
    kind, width, height = validate(data)

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(data)

    if target.read_bytes() != data:
        fail("entry.png: written bytes differ from art.png")
    print(
        f"wrote {target} ({len(data)} bytes, {kind} {width}x{height}, "
        "byte-for-byte copy of art.png)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
