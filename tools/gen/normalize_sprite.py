"""Place a sprite on the common anchor: feet on the bottom row, lantern cap centred. Logged edit.

Written by Claude. Every Wick state image uses the same anchor so swapping images in Godot never makes
him jump sideways or sink: the lowest opaque row goes to the last row of the frame, and the centre of
the cap (the widest brass row in the upper half of the body) goes to the frame's centre column.
Prints the measurements CHARACTER-SHEET.md checks (feet-to-cap, feet-to-handle, cap width).

    python tools/gen/normalize_sprite.py in.png --out out.png
"""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
LOG = REPO / "design" / "generation" / "edit-log.jsonl"
BRASS = (184, 134, 59)


def longest_run(row):
    """(start, end) of the longest contiguous True run in a 1-D bool array, or None."""
    best, start = None, None
    for x, v in enumerate(list(row) + [False]):
        if v and start is None:
            start = x
        elif not v and start is not None:
            if best is None or x - start > best[1] - best[0] + 1:
                best = (start, x - 1)
            start = None
    return best


def measure(a):
    """The cap is the longest contiguous run of brass-or-flame pixels in the upper body that is at least
    30 % brass. Arms are wider but broken by gaps; in pickup / celebrate the tall flame cuts through the
    cap, so flame pixels may sit inside the run; a run of flame alone (inside the glass) is not a cap."""
    op = a[..., 3] > 0
    ys, xs = np.nonzero(op)
    top, bottom = ys.min(), ys.max()
    brass = (a[..., :3] == BRASS).all(axis=2) & op
    solid = brass.copy()
    for c in ((255, 207, 90), (255, 241, 184)):
        solid |= (a[..., :3] == c).all(axis=2) & op
    runs = {}
    for y in range(top, top + (bottom - top) * 6 // 10):
        r = longest_run(solid[y])
        if r and brass[y, r[0]:r[1] + 1].mean() >= 0.3:
            runs[y] = r
    cap_len = max(r[1] - r[0] + 1 for r in runs.values())
    cap_rows = [y for y, r in runs.items() if r[1] - r[0] + 1 >= cap_len - 1]
    cap = runs[cap_rows[0]]
    return {"top": int(top), "bottom": int(bottom), "cap_rows": [int(min(cap_rows)), int(max(cap_rows))],
            "cap_x": [int(cap[0]), int(cap[1])], "cap_width": int(cap_len),
            "feet_to_cap_top": int(bottom - min(cap_rows) + 1), "feet_to_top": int(bottom - top + 1)}


def components(mask):
    """8-connected components of a bool mask -> list of (ys, xs) index arrays."""
    seen = np.zeros_like(mask)
    out = []
    H, W = mask.shape
    for y0, x0 in zip(*np.nonzero(mask)):
        if seen[y0, x0]:
            continue
        stack, ys, xs = [(y0, x0)], [], []
        seen[y0, x0] = True
        while stack:
            y, x = stack.pop()
            ys.append(y); xs.append(x)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
        out.append((np.array(ys), np.array(xs)))
    return out


def despeckle(a):
    """Drop floating opaque bits (< 6 px, e.g. a smoke wisp above the handle) and fill small dark
    specks (<= 3 px of glass / ink) that touch the flame on most sides. 2026-10-07."""
    a = a.copy()
    for ys, xs in components(a[..., 3] > 0):
        if len(ys) < 6:
            a[ys, xs] = 0
    flame = np.zeros(a.shape[:2], bool)
    for c in ((255, 207, 90), (255, 241, 184)):
        flame |= (a[..., :3] == c).all(axis=2) & (a[..., 3] > 0)
    dark = np.zeros_like(flame)
    for c in ((36, 31, 44), (42, 26, 16)):
        dark |= (a[..., :3] == c).all(axis=2) & (a[..., 3] > 0)
    for ys, xs in components(dark):
        if len(ys) <= 3:
            n = sum(flame[max(0, y - 1):y + 2, max(0, x - 1):x + 2].sum() for y, x in zip(ys, xs))
            if n >= 5 * len(ys):
                a[ys, xs, :3] = (255, 207, 90)
    return a


def normalize(a):
    m = measure(a)
    h, w = a.shape[:2]
    dy = (h - 1) - m["bottom"]
    dx = int(round((w - 1) / 2 - (m["cap_x"][0] + m["cap_x"][1]) / 2))
    out = np.zeros_like(a)
    src = a[max(0, -dy):h - max(0, dy), max(0, -dx):w - max(0, dx)]
    out[max(0, dy):max(0, dy) + src.shape[0], max(0, dx):max(0, dx) + src.shape[1]] = src
    # trim extras above the handle (rings, smoke wisps; rule 2): anything within 7 px of the centre
    # column more than 10 rows above the cap top. CHAR-REF's handle top sits 9 rows above its cap.
    m2 = measure(out)
    cx = (m2["cap_x"][0] + m2["cap_x"][1]) // 2
    out[:max(0, m2["cap_rows"][0] - 10), max(0, cx - 7):cx + 8] = 0
    out = despeckle(out)
    return out, dx, dy, measure(out)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    arr = np.asarray(Image.open(a.src).convert("RGBA")).copy()
    out, dx, dy, m = normalize(arr)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(out, "RGBA").save(a.out)
    rec = {"time": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "tool": "tools/gen/normalize_sprite.py",
           "src": Path(a.src).as_posix(), "src_sha256": hashlib.sha256(Path(a.src).read_bytes()).hexdigest(),
           "out": Path(a.out).as_posix(), "shift": [dx, dy], "measure": m}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    print(json.dumps({"shift": [dx, dy], **m}))


if __name__ == "__main__":
    main()
