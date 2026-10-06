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
    """The cap is the longest *contiguous* brass run in the upper body (arms are wider but broken)."""
    op = a[..., 3] > 0
    ys, xs = np.nonzero(op)
    top, bottom = ys.min(), ys.max()
    brass = (a[..., :3] == BRASS).all(axis=2) & op
    runs = {y: longest_run(brass[y]) for y in range(top, top + (bottom - top) * 6 // 10)}
    runs = {y: r for y, r in runs.items() if r}
    cap_len = max(r[1] - r[0] + 1 for r in runs.values())
    cap_rows = [y for y, r in runs.items() if r[1] - r[0] + 1 >= cap_len - 1]
    cap = runs[cap_rows[0]]
    return {"top": int(top), "bottom": int(bottom), "cap_rows": [int(min(cap_rows)), int(max(cap_rows))],
            "cap_x": [int(cap[0]), int(cap[1])], "cap_width": int(cap_len),
            "feet_to_cap_top": int(bottom - min(cap_rows) + 1), "feet_to_top": int(bottom - top + 1)}


def normalize(a):
    m = measure(a)
    h, w = a.shape[:2]
    dy = (h - 1) - m["bottom"]
    dx = int(round((w - 1) / 2 - (m["cap_x"][0] + m["cap_x"][1]) / 2))
    out = np.zeros_like(a)
    src = a[max(0, -dy):h - max(0, dy), max(0, -dx):w - max(0, dx)]
    out[max(0, dy):max(0, dy) + src.shape[0], max(0, dx):max(0, dx) + src.shape[1]] = src
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
