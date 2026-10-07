"""Process environment round-1 picks into game-size pixel art (written by Claude, 2026-10-07).

Every step is a logged edit (design/generation/edit-log.jsonl). Crop boxes are in the 1024-px source
image, read off the outputs by eye. Sizes are in game pixels at the 1280x720 viewport.

    python tools/gen/env_process.py
"""
import datetime as dt
import hashlib
import json
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

from pixelize import ENV_PALETTE, quantise, hex_rgb

REPO = Path(__file__).resolve().parents[2]
LOG = REPO / "design" / "generation" / "edit-log.jsonl"
RAW = Path("F:/7270/a2-gen/gen-raw")
OUT = REPO / "design" / "generation" / "accepted"


def load(asset, seed, b):
    return Image.open(RAW / asset / f"{asset}-s{seed}-b{b}.png").convert("RGB")


def corner_key(img, dist):
    """Alpha mask: background = pixels within `dist` (RGB) of the mean corner colour, connected to the border."""
    a = np.asarray(img).astype(int)
    h, w, _ = a.shape
    ref = np.mean([a[0, 0], a[0, -1], a[-1, 0], a[-1, -1]], axis=0)
    near = np.sqrt(((a - ref) ** 2).sum(axis=2)) <= dist
    bg = np.zeros((h, w), bool)
    q = deque([(y, x) for y in range(h) for x in (0, w - 1)] + [(y, x) for x in range(w) for y in (0, h - 1)])
    while q:
        y, x = q.popleft()
        if 0 <= y < h and 0 <= x < w and near[y, x] and not bg[y, x]:
            bg[y, x] = True
            q.extend(((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)))
    m = np.where(bg, 0, 255).astype(np.uint8)
    return np.asarray(Image.fromarray(m).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(5)))


def to_sprite(img, alpha, size):
    """Area-resize RGB + alpha to `size`, hard alpha, quantise to the environment palette."""
    rgb = img.resize(size, Image.BOX)
    al = Image.fromarray(alpha).resize(size, Image.BOX)
    arr = np.dstack([np.asarray(rgb), np.where(np.asarray(al) >= 128, 255, 0).astype(np.uint8)])
    arr = quantise(arr, ENV_PALETTE)
    arr[arr[..., 3] == 0] = 0
    return arr


def log(asset, src, out, steps):
    rec = {"time": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "tool": "tools/gen/env_process.py",
           "asset_id": asset, "src": src.as_posix(), "src_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
           "out": out.relative_to(REPO).as_posix(), "steps": steps}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")


def save(asset, arr, src, steps):
    out = OUT / f"{asset}.png"
    Image.fromarray(arr, "RGBA").save(out)
    log(asset, src, out, steps)
    print(asset, arr.shape[1], "x", arr.shape[0])


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # ENV-BG: whole image -> 1280x720, quantised. b1: flat rock wall with a beam (others are deep perspective).
    src = RAW / "ENV-BG" / "ENV-BG-s2001-b1.png"
    img = Image.open(src).convert("RGB")
    # round-1 mock: the wall was far brighter and busier than the platforms, so it is darkened to 45 %
    # before quantising; it is a backdrop, the lit platforms must win.
    img = Image.fromarray((np.asarray(img).astype(float) * 0.45).astype(np.uint8))
    save("ENV-BG", to_sprite(img, np.full(img.size[::-1], 255, np.uint8), (1280, 720)), src,
         ["darken x0.45 (backdrop must sit behind the platforms)", "resize 1344x768 -> 1280x720 (area)", "quantise Lab to ENV_PALETTE"])

    # ENV-TILE: central 768 px of b2 (regular blue stones) -> 64x64 texture (2x2 cells of 32 px).
    src = RAW / "ENV-TILE" / "ENV-TILE-s2002-b2.png"
    img = Image.open(src).convert("RGB").crop((128, 128, 896, 896))
    tile = to_sprite(img, np.full((768, 768), 255, np.uint8), (64, 64))
    save("ENV-TILE", tile, src, ["crop (128,128,896,896)", "resize -> 64x64 (area)", "quantise Lab to ENV_PALETTE"])

    # ENV-TILE-TOP: every TILE-TOP output was a whole scene, so the top edge is an edit of ENV-TILE:
    # rows 0-1 'rock light', row 2 'rock edge', row 3 'deep rock' shadow line. (Claude's code, not the model.)
    top = tile.copy()
    for y, name in ((0, "rock light"), (1, "rock light"), (2, "rock edge"), (3, "deep rock")):
        top[y, :, :3] = hex_rgb(ENV_PALETTE[name])
    save("ENV-TILE-TOP", top, src, ["copy ENV-TILE", "paint rows 0-1 rock light, row 2 rock edge, row 3 deep rock (code edit; all ENV-TILE-TOP generations rejected)"])

    # ENV-SPIKE: b3 spear heads only (crop), grey background keyed from the corners -> 96x24 strip of 6.
    src = RAW / "ENV-SPIKE" / "ENV-SPIKE-s2004-b3.png"
    img = Image.open(src).convert("RGB").crop((100, 30, 880, 330))
    save("ENV-SPIKE", to_sprite(img, corner_key(img, 40), (96, 36)), src,
         ["crop spear heads (100,30,880,330)", "key out grey background from corners (dist 40)", "resize -> 96x36 (24 px read too thin in the mock)", "quantise Lab to ENV_PALETTE"])

    # ENV-OIL: the hanging drop on the right of b3, cropped away from the holder -> 24x24.
    src = RAW / "ENV-OIL" / "ENV-OIL-s2005-b3.png"
    img = Image.open(src).convert("RGB").crop((740, 290, 1010, 590))
    near_white = (np.asarray(img).astype(int) >= 225).all(axis=2)  # corner key left a white box (round-1 mock)
    save("ENV-OIL", to_sprite(img, np.where(near_white, 0, 255).astype(np.uint8), (22, 24)), src,
         ["crop the single drop (740,290,1010,590)", "remove all near-white (>=225) pixels", "resize -> 22x24", "quantise Lab to ENV_PALETTE"])

    # ENV-LADDER: a straight run of rungs from the middle of b2 -> 32x32 tile, dark gaps made transparent.
    src = RAW / "ENV-LADDER" / "ENV-LADDER-s2006-b2.png"
    img = Image.open(src).convert("RGB").crop((330, 380, 690, 740))
    arr = to_sprite(img, np.full((360, 360), 255, np.uint8), (32, 32))
    for name in ("cave dark", "deep rock"):
        arr[(arr[..., :3] == hex_rgb(ENV_PALETTE[name])).all(axis=2)] = 0
    save("ENV-LADDER", arr, src, ["crop rungs (330,380,690,740)", "resize -> 32x32", "quantise Lab to ENV_PALETTE",
                                  "cave dark / deep rock -> transparent (the box interior behind the rungs)"])

    # ENV-LAMPPOST (want): b1 post with a bell lamp, small props at the foot cropped off -> 32x80.
    src = RAW / "ENV-LAMPPOST" / "ENV-LAMPPOST-s2007-b1.png"
    img = Image.open(src).convert("RGB").crop((150, 60, 760, 1000))
    save("ENV-LAMPPOST", to_sprite(img, corner_key(img, 40), (40, 64)), src,
         ["crop post (150,60,760,1000)", "key out white from corners (dist 40)", "resize -> 40x64", "quantise Lab to ENV_PALETTE"])


if __name__ == "__main__":
    main()
