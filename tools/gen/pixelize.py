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
from PIL import Image, ImageFilter

REPO = Path(__file__).resolve().parents[2]
LOG = REPO / "design" / "generation" / "edit-log.jsonl"
PALETTE = {  # CHARACTER-SHEET.md
    "brass": "#b8863b", "glass": "#241f2c", "flame": "#ffcf5a",
    "core": "#fff1b8", "ember": "#e2552f", "ink": "#2a1a10",
}

# Environment palette (Claude's proposal, 2026-10-07): cold, dark rock so Wick's brass stays the warmest
# mid-tone on screen; timber, steel and oil get two tones each.
ENV_PALETTE = {
    "cave dark": "#0b0b10", "deep rock": "#161822", "rock": "#2a2e3d", "rock mid": "#3a3f52",
    "rock edge": "#4a5068", "rock light": "#5d6480", "timber dark": "#3b2a1c", "timber": "#5a412a",
    "steel": "#8f96a8", "steel light": "#c9cdd6", "oil": "#f2a93b", "oil light": "#ffe08a",
    "highlight": "#f4f1e8",
}
PALETTES = {"char": PALETTE, "env": ENV_PALETTE}


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


def to_lab(rgb):
    """sRGB (0-255, ..., 3) -> CIE Lab (D65)."""
    c = rgb / 255.0
    c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    xyz = c @ np.array([[0.4124, 0.2126, 0.0193], [0.3576, 0.7152, 0.1192], [0.1805, 0.0722, 0.9505]])
    xyz /= np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], axis=-1)


def quantise(rgba, palette, space="lab"):
    """Nearest palette colour. 'lab' (default since 2026-10-07) matches what the eye sees: with plain RGB
    distance the hurt pose's orange flame became brass and shaded brass became glass."""
    cols = np.array([hex_rgb(c) for c in palette.values()], float)
    px = rgba[..., :3].reshape(-1, 3).astype(float)
    if space == "lab":
        px, ref = to_lab(px), to_lab(cols)
    else:
        ref = cols
    idx = ((px[:, None, :] - ref[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
    out = rgba.copy()
    out[..., :3] = cols[idx].reshape(rgba.shape[0], rgba.shape[1], 3).astype(np.uint8)
    return out


def pixelize(src, frame_w, frame_h, height, tol=18, palette=PALETTE, scale=None, space="lab"):
    rgb = np.asarray(Image.open(src).convert("RGB"))
    alpha = np.where((rgb.astype(int) >= 255 - tol).all(axis=2), 0, 255).astype(np.uint8)
    # opening (min then max filter) drops specks smaller than ~5 px, so a stray pixel at the image edge
    # no longer stretches the bounding box (CHAR-REF's crop started at x = 0 because of one, 2026-10-07)
    alpha = np.asarray(Image.fromarray(alpha).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(5)))
    rgba = np.dstack([rgb, alpha])
    ys, xs = np.nonzero(alpha)
    crop = Image.fromarray(rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1], "RGBA")
    scale = scale or height / crop.height  # --scale keeps every pose at the reference's scale
    w, height = max(1, round(crop.width * scale)), max(1, round(crop.height * scale))
    if height > frame_h:
        raise SystemExit(f"{src}: {height} px tall at this scale, frame is {frame_h}")
    if w > frame_w:  # never exceed the frame; shrink to fit the width instead
        scale = frame_w / crop.width
        w, height = frame_w, max(1, round(crop.height * scale))
    small = crop.resize((w, height), Image.BOX)
    canvas = Image.new("RGBA", (frame_w, frame_h), (0, 0, 0, 0))
    canvas.paste(small, ((frame_w - w) // 2, frame_h - height), small)
    arr = np.asarray(canvas).copy()
    arr[..., 3] = np.where(arr[..., 3] >= 128, 255, 0)
    arr = quantise(arr, palette, space) if palette else arr
    arr[arr[..., 3] == 0] = 0
    return Image.fromarray(arr, "RGBA"), {"crop_box": [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1],
                                         "scaled_to": [w, height], "scale": scale}


def exact(src, w, h, palette, space="lab"):
    """Background / tile mode: no background removal, no anchoring; area-resize to w x h and quantise."""
    img = Image.open(src).convert("RGB").resize((w, h), Image.BOX)
    arr = np.dstack([np.asarray(img), np.full((h, w), 255, np.uint8)])
    return Image.fromarray(quantise(arr, palette, space), "RGBA"), {"mode": "exact"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("--frame", nargs=2, type=int, required=True, metavar=("W", "H"))
    p.add_argument("--height", type=int, default=0, help="character height in sprite pixels")
    p.add_argument("--scale", type=float, default=None, help="fixed scale instead of --height")
    p.add_argument("--tol", type=int, default=18, help="near-white tolerance for background removal")
    p.add_argument("--no-quantise", action="store_true")
    p.add_argument("--palette", choices=list(PALETTES), default="char")
    p.add_argument("--exact", action="store_true", help="resize the whole image to --frame (backgrounds, tiles)")
    p.add_argument("--space", choices=["lab", "rgb"], default="lab", help="colour distance for quantising (CHAR-REF used rgb)")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    pal = PALETTES[a.palette]
    if a.exact:
        img, info = exact(a.src, *a.frame, pal, a.space)
    else:
        img, info = pixelize(a.src, *a.frame, a.height, a.tol, None if a.no_quantise else pal, a.scale, a.space)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    rec = {"time": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "tool": "tools/gen/pixelize.py",
           "src": str(a.src), "src_sha256": hashlib.sha256(Path(a.src).read_bytes()).hexdigest(),
           "out": out.as_posix(), "frame": a.frame, "height": a.height, "scale_arg": a.scale, "tol": a.tol,
           "palette": None if a.no_quantise else PALETTES[a.palette], "palette_name": a.palette, "space": a.space, **info}
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    print(out)


if __name__ == "__main__":
    main()
