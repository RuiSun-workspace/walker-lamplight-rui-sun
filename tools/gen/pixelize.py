"""Turn one generated illustration into a pixel-art sprite. Every step is a logged, repeatable edit.

Written by Claude. Steps, in order:
  1. background removal: every near-white pixel is background (the prompt asks for a plain white
     background). Global, not a flood fill from the border: the first version only removed white
     connected to the border and left the hole inside the handle ring as a pale blob (2026-10-07).
     The flame core (#fff1b8, blue channel ~184) is not near-white, so it survives;
  2. crop to the character's bounding box;
  3. scale (area average) so the character is `--height` px tall, feet on the bottom row of a
     `--frame W H` canvas, centred horizontally;
  4. alpha threshold at 50% (hard pixel edges, no semi-transparent fringe);
  5. quantise every opaque pixel to the nearest colour of the CHARACTER-SHEET.md palette.

    python tools/gen/pixelize.py F:/7270/a2-gen/gen-raw/CHAR-REF/CHAR-REF-s1011-b0.png \
        --frame 64 80 --height 66 --out design/generation/pixelized/CHAR-REF-s1011-b0-64x80.png

A JSON line per output is appended to design/generation/edit-log.jsonl.
"""
import argparse
import datetime as dt
import hashlib
import json
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
LOG = REPO / "design" / "generation" / "edit-log.jsonl"
PALETTE = {  # CHARACTER-SHEET.md
    "brass": "#b8863b", "glass": "#241f2c", "flame": "#ffcf5a",
    "core": "#fff1b8", "ember": "#e2552f", "ink": "#2a1a10",
}


def hex_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def remove_background(rgb, tol):
    """Mask of background pixels: near-white and connected to the border."""
    h, w, _ = rgb.shape
    near_white = (rgb.astype(int) >= 255 - tol).all(axis=2)
    bg = np.zeros((h, w), bool)
    q = deque((y, x) for y in range(h) for x in (0, w - 1) if near_white[y, x])
    q.extend((y, x) for x in range(w) for y in (0, h - 1) if near_white[y, x])
    for y, x in q:
        bg[y, x] = True
    while q:
        y, x = q.popleft()
        for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if 0 <= ny < h and 0 <= nx < w and near_white[ny, nx] and not bg[ny, nx]:
                bg[ny, nx] = True
                q.append((ny, nx))
    return bg


def quantise(rgba, palette):
    cols = np.array([hex_rgb(c) for c in palette.values()], float)
    px = rgba[..., :3].reshape(-1, 3).astype(float)
    idx = ((px[:, None, :] - cols[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
    out = rgba.copy()
    out[..., :3] = cols[idx].reshape(rgba.shape[0], rgba.shape[1], 3).astype(np.uint8)
    return out


def pixelize(src, frame_w, frame_h, height, tol=18, palette=PALETTE):
    rgb = np.asarray(Image.open(src).convert("RGB"))
    alpha = np.where((rgb.astype(int) >= 255 - tol).all(axis=2), 0, 255).astype(np.uint8)
    rgba = np.dstack([rgb, alpha])
    ys, xs = np.nonzero(alpha)
    crop = Image.fromarray(rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1], "RGBA")
    scale = height / crop.height
    w = max(1, round(crop.width * scale))
    if w > frame_w:  # never exceed the frame; shrink to fit the width instead
        scale = frame_w / crop.width
        w, height = frame_w, max(1, round(crop.height * scale))
    small = crop.resize((w, height), Image.BOX)
    canvas = Image.new("RGBA", (frame_w, frame_h), (0, 0, 0, 0))
    canvas.paste(small, ((frame_w - w) // 2, frame_h - height), small)
    arr = np.asarray(canvas).copy()
    arr[..., 3] = np.where(arr[..., 3] >= 128, 255, 0)
    arr = quantise(arr, palette) if palette else arr
    arr[arr[..., 3] == 0] = 0
    return Image.fromarray(arr, "RGBA"), {"crop_box": [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1],
                                         "scaled_to": [w, height]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("--frame", nargs=2, type=int, required=True, metavar=("W", "H"))
    p.add_argument("--height", type=int, required=True, help="character height in sprite pixels")
    p.add_argument("--tol", type=int, default=18, help="near-white tolerance for background removal")
    p.add_argument("--no-quantise", action="store_true")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    img, info = pixelize(a.src, *a.frame, a.height, a.tol, None if a.no_quantise else PALETTE)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    rec = {"time": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "tool": "tools/gen/pixelize.py",
           "src": str(a.src), "src_sha256": hashlib.sha256(Path(a.src).read_bytes()).hexdigest(),
           "out": out.as_posix(), "frame": a.frame, "height": a.height, "tol": a.tol,
           "palette": None if a.no_quantise else PALETTE, **info}
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    print(out)


if __name__ == "__main__":
    main()
