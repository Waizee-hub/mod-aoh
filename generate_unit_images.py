#!/usr/bin/env python3
"""
Generate placeholder PNG unit images for the Maritime Combat Units mod.
Run this script from the mod root directory to create all required images.

Images are created in:
  game/units/unitsImages/H/    (16x16)
  game/units/unitsImages/XH/   (32x32)
  game/units/unitsImages/XXH/  (48x48)
"""

import zlib
import struct
import os

# ---------------------------------------------------------------------------
# Minimal pure-stdlib PNG encoder
# ---------------------------------------------------------------------------

def _make_chunk(chunk_type: bytes, data: bytes) -> bytes:
    crc = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", crc)


def create_png(pixels: list[list[tuple[int, int, int, int]]]) -> bytes:
    """
    Encode a 2-D list of (R, G, B, A) tuples as a PNG bytestring.
    pixels[y][x] = (r, g, b, a)
    """
    height = len(pixels)
    width  = len(pixels[0])

    # Signature
    sig = b"\x89PNG\r\n\x1a\n"

    # IHDR  – 8-bit RGBA (colour type 6)
    ihdr = _make_chunk(
        b"IHDR",
        struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0),
    )

    # IDAT
    raw = bytearray()
    for row in pixels:
        raw.append(0)  # filter = None
        for r, g, b, a in row:
            raw += bytes([r, g, b, a])
    idat = _make_chunk(b"IDAT", zlib.compress(bytes(raw), 9))

    # IEND
    iend = _make_chunk(b"IEND", b"")

    return sig + ihdr + idat + iend


# ---------------------------------------------------------------------------
# Ship pixel-art templates  (16×16 canonical, will be scaled up)
# ---------------------------------------------------------------------------

T = (0, 0, 0, 0)        # transparent

def _ship_template(hull: tuple, deck: tuple, flag: tuple) -> list[list]:
    """16×16 generic top-down ship silhouette."""
    H, D, F = hull, deck, flag
    return [
        [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],
        [T, T, T, T, T, T, T, H, H, T, T, T, T, T, T, T],
        [T, T, T, T, T, T, H, H, H, H, T, T, T, T, T, T],
        [T, T, T, T, T, H, H, D, D, H, H, T, T, T, T, T],
        [T, T, T, T, H, H, D, D, D, D, H, H, T, T, T, T],
        [T, T, T, H, H, D, D, F, F, D, D, H, H, T, T, T],
        [T, T, H, H, D, D, D, D, D, D, D, D, H, H, T, T],
        [T, H, H, D, D, D, D, D, D, D, D, D, D, H, H, T],
        [T, H, H, D, D, D, D, D, D, D, D, D, D, H, H, T],
        [T, T, H, H, D, D, D, D, D, D, D, D, H, H, T, T],
        [T, T, T, H, H, D, D, D, D, D, D, H, H, T, T, T],
        [T, T, T, T, H, H, D, D, D, D, H, H, T, T, T, T],
        [T, T, T, T, T, H, H, H, H, H, H, T, T, T, T, T],
        [T, T, T, T, T, T, H, H, H, H, T, T, T, T, T, T],
        [T, T, T, T, T, T, T, H, H, T, T, T, T, T, T, T],
        [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],
    ]


def _battleship_template(hull: tuple, deck: tuple, turret: tuple) -> list[list]:
    """16×16 larger-looking battleship silhouette."""
    H, D, Tu = hull, deck, turret
    return [
        [T, T, T, T, T, T, T, H, H, T, T, T, T, T, T, T],
        [T, T, T, T, T, T, H, H, H, H, T, T, T, T, T, T],
        [T, T, T, T, T, H, H, D, D, H, H, T, T, T, T, T],
        [T, T, T, T, H, H, D, Tu, Tu, D, H, H, T, T, T, T],
        [T, T, T, H, H, D, D, Tu, Tu, D, D, H, H, T, T, T],
        [T, T, H, H, D, D, D, D, D, D, D, D, H, H, T, T],
        [T, H, H, D, D, D, D, D, D, D, D, D, D, H, H, T],
        [H, H, D, D, D, D, Tu, Tu, Tu, Tu, D, D, D, D, H, H],
        [H, H, D, D, D, D, Tu, Tu, Tu, Tu, D, D, D, D, H, H],
        [T, H, H, D, D, D, D, D, D, D, D, D, D, H, H, T],
        [T, T, H, H, D, D, D, D, D, D, D, D, H, H, T, T],
        [T, T, T, H, H, D, D, Tu, Tu, D, D, H, H, T, T, T],
        [T, T, T, T, H, H, D, Tu, Tu, D, H, H, T, T, T, T],
        [T, T, T, T, T, H, H, D, D, H, H, T, T, T, T, T],
        [T, T, T, T, T, T, H, H, H, H, T, T, T, T, T, T],
        [T, T, T, T, T, T, T, H, H, T, T, T, T, T, T, T],
    ]


def _scale(pixels: list, factor: int) -> list:
    """Nearest-neighbour upscale."""
    result = []
    for row in pixels:
        scaled_row = []
        for pixel in row:
            scaled_row.extend([pixel] * factor)
        for _ in range(factor):
            result.append(list(scaled_row))
    return result


# ---------------------------------------------------------------------------
# Unit image definitions
# ---------------------------------------------------------------------------

# colour palette
HULL_BLUE    = (30,  90, 160, 255)   # medium navy hull
DECK_BLUE    = (70, 140, 200, 255)   # deck highlight
FLAG_YELLOW  = (230, 200,  50, 255)  # flag/pennant

HULL_DKBLUE  = (20,  55, 110, 255)   # Ship of the Line hull
DECK_DKBLUE  = (50, 100, 160, 255)
FLAG_RED     = (200,  40,  40, 255)

HULL_GRAY    = (100, 110, 120, 255)  # Ironclad hull
DECK_GRAY    = (150, 160, 170, 255)
TURRET_GRAY  = ( 70,  75,  80, 255)

HULL_DKGRAY  = ( 60,  65,  70, 255)  # Battleship hull
DECK_DKGRAY  = (100, 105, 110, 255)
TURRET_DKGRAY= ( 35,  38,  42, 255)


UNIT_IMAGES = {
    # id  : (template_fn, arg1,         arg2,         arg3)
    100: (_ship_template,        HULL_BLUE,   DECK_BLUE,   FLAG_YELLOW),
    101: (_ship_template,        HULL_BLUE,   (90, 160, 220, 255),  FLAG_YELLOW),
    102: (_ship_template,        HULL_BLUE,   (110,180,240,255),    (240,210,60,255)),
    110: (_ship_template,        HULL_DKBLUE, DECK_DKBLUE, FLAG_RED),
    111: (_ship_template,        HULL_DKBLUE, (70,110,170,255),     FLAG_RED),
    112: (_ship_template,        HULL_DKBLUE, (80,120,180,255),     (220,50,50,255)),
    120: (_battleship_template,  HULL_GRAY,   DECK_GRAY,   TURRET_GRAY),
    121: (_battleship_template,  HULL_GRAY,   (160,170,180,255),    TURRET_GRAY),
    122: (_battleship_template,  HULL_GRAY,   (170,180,190,255),    (60,65,70,255)),
    130: (_battleship_template,  HULL_DKGRAY, DECK_DKGRAY, TURRET_DKGRAY),
    131: (_battleship_template,  HULL_DKGRAY, (110,115,120,255),    TURRET_DKGRAY),
    132: (_battleship_template,  HULL_DKGRAY, (120,125,130,255),    (25,28,32,255)),
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

SIZES = {
    "H":   1,   # 16×16
    "XH":  2,   # 32×32
    "XXH": 3,   # 48×48
}

BASE_DIR = os.path.join(os.path.dirname(__file__), "game", "units", "unitsImages")


def main():
    created = 0
    for folder, scale_factor in SIZES.items():
        out_dir = os.path.join(BASE_DIR, folder)
        os.makedirs(out_dir, exist_ok=True)
        for img_id, (fn, *args) in UNIT_IMAGES.items():
            pixels_16 = fn(*args)
            pixels    = _scale(pixels_16, scale_factor)
            png_bytes  = create_png(pixels)
            out_path   = os.path.join(out_dir, f"{img_id}.png")
            with open(out_path, "wb") as f:
                f.write(png_bytes)
            created += 1
    print(f"Generated {created} PNG files in {BASE_DIR}/{{H,XH,XXH}}/")


if __name__ == "__main__":
    main()
