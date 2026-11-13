#!/usr/bin/env python3
"""news-image-01 entry: validate art.png, then copy it byte-for-byte.

The image is a one-page editorial front page that sums up the world
news of Friday 13 November 2026. This program is the delivery vehicle:
it checks that the bundled image is a whole PNG or JPEG within the
competition limits (at most 1 MiB, at most 1024 x 1024 pixels) and
writes it, unchanged, to the output directory as ``entry.png``.

Standard library only. No network. Deterministic: the same input
bytes always produce the same output bytes.
"""

import os
import struct
import sys
import zlib
from pathlib import Path

MAX_BYTES = 1_048_576  # 1 MiB
MAX_WIDTH = 1024
MAX_HEIGHT = 1024

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_SOI = b"\xff\xd8"
JPEG_EOI = b"\xff\xd9"

# JPEG markers that carry a frame header with the image dimensions.
SOF_MARKERS = {0xC0, 0xC1, 0xC2}
# JPEG markers with no length field and no payload.
STANDALONE_MARKERS = {0x01, 0xD8, 0xD9} | set(range(0xD0, 0xD8))


def fail(message):
    """Abort with a clear error message."""
    raise SystemExit(f"error: {message}")


def check_png(data):
    """Validate a whole PNG and return (width, height).

    Walks every chunk, verifies each chunk's CRC, reads the dimensions
    from IHDR, and requires the file to end exactly at IEND.
    """
    if not data.startswith(PNG_SIGNATURE):
        fail("art.png: bad PNG signature")
    pos = len(PNG_SIGNATURE)
    width = height = None
    seen_idat = False
    while pos < len(data):
        if pos + 8 > len(data):
            fail("art.png: truncated chunk header")
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        chunk_type = data[pos + 4:pos + 8]
        end = pos + 8 + length + 4
        if end > len(data):
            fail(f"art.png: truncated {chunk_type!r} chunk")
        payload = data[pos + 8:pos + 8 + length]
        stored_crc = struct.unpack(">I", data[pos + 8 + length:end])[0]
        actual_crc = zlib.crc32(chunk_type + payload) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            fail(f"art.png: CRC mismatch in {chunk_type!r} chunk")
        if width is None:
            if chunk_type != b"IHDR" or length != 13:
                fail("art.png: first chunk is not a 13-byte IHDR")
            width, height = struct.unpack(">II", payload[:8])
            bit_depth, color_type = payload[8], payload[9]
            if color_type not in (0, 2, 3, 4, 6):
                fail(f"art.png: invalid PNG color type {color_type}")
            if bit_depth not in (1, 2, 4, 8, 16):
                fail(f"art.png: invalid PNG bit depth {bit_depth}")
            if payload[10] != 0 or payload[11] != 0 or payload[12] not in (0, 1):
                fail("art.png: invalid PNG compression/filter/interlace bytes")
        if chunk_type == b"IDAT":
            seen_idat = True
        pos = end
        if chunk_type == b"IEND":
            break
    else:
        fail("art.png: no IEND chunk")
    if pos != len(data):
        fail("art.png: trailing bytes after IEND")
    if not seen_idat:
        fail("art.png: no IDAT chunk")
    return width, height


def check_jpeg(data):
    """Validate a whole JPEG and return (width, height).

    Walks the marker segments until the end marker, reading the
    dimensions from the first start-of-frame segment on the way.
    """
    if not data.startswith(JPEG_SOI):
        fail("art.png: bad JPEG start marker")
    if not data.endswith(JPEG_EOI):
        fail("art.png: missing JPEG end marker")
    pos = 2
    width = height = None
    while pos + 1 < len(data):
        if data[pos] != 0xFF:
            fail(f"art.png: expected JPEG marker at offset {pos}")
        marker = data[pos + 1]
        pos += 2
        if marker in STANDALONE_MARKERS:
            if marker == 0xD9:
                break
            continue
        if pos + 2 > len(data):
            fail("art.png: truncated JPEG segment")
        seg_len = struct.unpack(">H", data[pos:pos + 2])[0]
        if seg_len < 2 or pos + seg_len > len(data):
            fail("art.png: JPEG segment overruns the file")
        if marker in SOF_MARKERS and width is None:
            if seg_len < 7:
                fail("art.png: short JPEG frame header")
            height = struct.unpack(">H", data[pos + 3:pos + 5])[0]
            width = struct.unpack(">H", data[pos + 5:pos + 7])[0]
        if marker == 0xDA:  # start of scan: entropy data runs to EOI
            break
        pos += seg_len
    if width is None:
        fail("art.png: no JPEG frame header found")
    return width, height


def validate(data):
    """Check the competition gate limits; return the image kind."""
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
