"""Clean up a pixelised Wick sprite and paint a readable face into the flame. Logged, repeatable edit.

Written by Claude after Rui's review of CHAR-REF-s1012-b1 (2026-10-07): "make the eye and mouth lines
thicker and the shapes nicer". After pixelisation the generated face had dissolved into brass-coloured
smudges, so the face is repainted here from fixed pixel patterns. Body, flame outline and colours stay
as the model produced them. Steps:

  1. drop stray opaque pixels above `--top` (remnant of an extra ring on the handle, rule 2);
  2. inside the flame zone, brass pixels left by area-averaging become flame if they touch >= 2 flame
     pixels, otherwise glass;
  3. old face pixels inside the face box become flame;
  4. paint eyes + mouth from the chosen pattern in ink (#2a1a10), with a 1 px core-colour highlight.

    python tools/gen/face_edit.py design/generation/pixelized/CHAR-REF-s1012-b1-64x80.png \
        --face round --out design/generation/edited/CHAR-REF-s1012-b1-64x80-round.png
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
BRASS, GLASS, FLAME, CORE, INK = (184, 134, 59), (36, 31, 44), (255, 207, 90), (255, 241, 184), (42, 26, 16)
EMBER_RGB = (226, 85, 47)

# Patterns: 'X' ink, 'h' highlight (core colour), '.' leave. Eyes are given for the LEFT eye; the right
# eye is the same pattern. Coordinates are the top-left of each pattern in the 64x80 frame.
FACES = {  # revised 2026-10-07 after the first preview: corner highlight read as a frown, mouth too wide
    "round": {  # open round eyes with an inner highlight - the sheet's neutral idle face
        "eye": [".XX.", "XXhX", "XXXX", ".XX."], "left": [34, 44], "right": [40, 44],
        "mouth": ["X...X", "XX.XX", ".XXX."], "mouth_at": [36, 50],
    },
    "happy": {  # closed happy arcs, like the generated face but 2 px thick
        "eye": [".XXX.", "XX.XX", "X...X"], "left": [33, 45], "right": [39, 45],
        "mouth": ["X...X", "XX.XX", ".XXX."], "mouth_at": [36, 50],
    },
    "oval": {  # tall oval eyes, a little more expressive  <- chosen for CHAR-REF / idle (Rui)
        "eye": ["hX", "XX", "XX", "XX"], "left": [35, 44], "right": [40, 44],
        "mouth": ["X...X", "XX.XX", ".XXX."], "mouth_at": [36, 50],
    },
    # State faces (2026-10-07). Placed with --auto relative to the flame, same rule as CHAR-REF.
    "grin": {"eye": ["hX", "XX", "XX", "XX"], "mouth": ["X.....X", "XX...XX", ".XXXXX."]},  # pickup
    "wide": {"eye": ["hX", "XX", "XX", "XX"], "mouth": [".X.", "X.X", ".X."]},               # fall / jump
    "x": {"eye": ["X.X", ".X.", "X.X"], "mouth": [".X.", "X.X", ".X."]},                     # hurt
    "lid": {"eye": ["XX"], "mouth": []},                                                     # ember
    "joy": {"eye": [".XX.", "X..X"], "mouth": ["X.....X", "XX...XX", ".XXXXX."]},           # celebrate
    "none": {"eye": [], "mouth": []},                                                        # climb (back view)
}
FLAMES = (FLAME, CORE, (226, 85, 47), (255, 138, 61))  # flame, core, ember, hurt-orange


def auto_anchor(a, face):
    """Place the face like CHAR-REF: flame bbox (x 26-37, y 40-61) -> eyes at x 29 / 34, y 49; mouth x 30, y 55."""
    fl = np.zeros(a.shape[:2], bool)
    for c in FLAMES:
        fl |= (a[..., :3] == c).all(axis=2) & (a[..., 3] > 0)
    ys, xs = np.nonzero(fl)
    fx0, fx1, fy0, fy1 = xs.min(), xs.max(), ys.min(), ys.max()
    cx, h = (fx0 + fx1) / 2, fy1 - fy0 + 1
    f = FACES[face]
    w = len(f["eye"][0]) if f["eye"] else 0
    left = [int(cx - 1.5 - w + 1), fy0 + round(0.41 * h)]
    right = [left[0] + w + 3, left[1]]
    mw = len(f["mouth"][0]) if f["mouth"] else 0
    mouth = [int(cx - mw / 2 + 1), fy0 + round(0.68 * h)]
    H, W = a.shape[:2]
    zone = [max(1, int(fx0) - 1), max(1, int(fy0) - 1), min(W - 1, int(fx1) + 2), min(H - 1, int(fy1) + 2)]
    return left, right, mouth, zone, zone


def paint(arr, pattern, x0, y0):
    for dy, row in enumerate(pattern):
        for dx, ch in enumerate(row):
            if ch == "X":
                arr[y0 + dy, x0 + dx] = (*INK, 255)
            elif ch == "h":
                arr[y0 + dy, x0 + dx] = (*CORE, 255)


def edit(src, face, top, zone, face_box, left_eye, right_eye, mouth):
    a = np.asarray(Image.open(src).convert("RGBA")).copy()
    a[:top, :, :] = 0                                    # 1
    x0, y0, x1, y1 = zone
    is_flame = lambda p: tuple(p[:3]) in FLAMES
    snapshot = a.copy()
    for y in range(y0, y1):                              # 2
        for x in range(x0, x1):
            if tuple(snapshot[y, x, :3]) == BRASS and snapshot[y, x, 3]:
                n = sum(is_flame(snapshot[yy, xx]) for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)))
                a[y, x, :3] = FLAME if n >= 2 else GLASS
    # 2b. fill holes inside the flame: any non-flame pixel between the leftmost and rightmost flame pixel
    #     of its row (and between the top and bottom flame pixel of its column) becomes flame. Removes
    #     generated face lines and shading that quantised to glass / ink (poses round 1, 2026-10-07).
    fl = np.zeros(a.shape[:2], bool)
    for c in FLAMES:
        fl |= (a[..., :3] == c).all(axis=2) & (a[..., 3] > 0)
    fill = np.zeros_like(fl)
    for y in range(y0, y1):
        xs_ = np.nonzero(fl[y, x0:x1])[0]
        if len(xs_) >= 2:
            fill[y, x0 + xs_[0]:x0 + xs_[-1] + 1] = True
    colfill = np.zeros_like(fl)
    for x in range(x0, x1):
        ys_ = np.nonzero(fl[y0:y1, x])[0]
        if len(ys_) >= 2:
            colfill[y0 + ys_[0]:y0 + ys_[-1] + 1, x] = True
    holes = fill & colfill & ~fl & (a[..., 3] > 0)
    main_flame = EMBER_RGB if (fl & (a[..., :3] == EMBER_RGB).all(axis=2)).sum() > fl.sum() / 2 else FLAME
    a[holes, :3] = main_flame
    fx0, fy0, fx1, fy1 = face_box                        # 3
    for y in range(fy0, fy1):
        for x in range(fx0, fx1):
            if a[y, x, 3] and tuple(a[y, x, :3]) in (INK, BRASS):
                a[y, x, :3] = FLAME if not any(tuple(a[yy, xx, :3]) == (226, 85, 47) for yy, xx in ((y, x - 1), (y, x + 1))) else (226, 85, 47)
    f = FACES[face]                                      # 4
    paint(a, f["eye"], *left_eye)
    paint(a, f["eye"], *right_eye)
    if f["mouth"]:
        paint(a, f["mouth"], *mouth)
    return Image.fromarray(a, "RGBA")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("--face", choices=FACES, required=True)
    p.add_argument("--top", type=int, default=19)
    p.add_argument("--zone", type=int, nargs=4, default=[30, 34, 47, 57], help="flame zone x0 y0 x1 y1")
    p.add_argument("--face-box", type=int, nargs=4, default=[32, 44, 46, 54])
    p.add_argument("--left-eye", type=int, nargs=2, default=None)
    p.add_argument("--right-eye", type=int, nargs=2, default=None)
    p.add_argument("--mouth", type=int, nargs=2, default=None)
    p.add_argument("--auto", action="store_true", help="place face relative to the flame (state poses)")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    if a.auto:
        src = np.asarray(Image.open(a.src).convert("RGBA"))
        a.left_eye, a.right_eye, a.mouth, a.zone, a.face_box = auto_anchor(src, a.face)
    left = a.left_eye or FACES[a.face]["left"]
    right = a.right_eye or FACES[a.face]["right"]
    mouth = a.mouth or FACES[a.face].get("mouth_at")
    img = edit(a.src, a.face, a.top, a.zone, a.face_box, left, right, mouth)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    rec = {"time": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "tool": "tools/gen/face_edit.py",
           "src": Path(a.src).as_posix(), "src_sha256": hashlib.sha256(Path(a.src).read_bytes()).hexdigest(),
           "out": out.as_posix(), "face": a.face, "pattern": FACES[a.face], "top": a.top, "zone": [int(v) for v in a.zone],
           "face_box": [int(v) for v in a.face_box], "auto": a.auto, "left_eye": [int(v) for v in left], "right_eye": [int(v) for v in right],
           "mouth": [int(v) for v in mouth] if mouth else None}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    print(out)


if __name__ == "__main__":
    main()
