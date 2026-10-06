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
    "oval": {  # tall oval eyes, a little more expressive
        "eye": ["hX", "XX", "XX", "XX"], "left": [35, 44], "right": [40, 44],
        "mouth": ["X...X", "XX.XX", ".XXX."], "mouth_at": [36, 50],
    },
}


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
    is_flame = lambda p: tuple(p[:3]) in (FLAME, CORE)
    snapshot = a.copy()
    for y in range(y0, y1):                              # 2
        for x in range(x0, x1):
            if tuple(snapshot[y, x, :3]) == BRASS and snapshot[y, x, 3]:
                n = sum(is_flame(snapshot[yy, xx]) for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)))
                a[y, x, :3] = FLAME if n >= 2 else GLASS
    fx0, fy0, fx1, fy1 = face_box                        # 3
    for y in range(fy0, fy1):
        for x in range(fx0, fx1):
            if a[y, x, 3] and tuple(a[y, x, :3]) in (INK, BRASS):
                a[y, x, :3] = FLAME
    f = FACES[face]                                      # 4
    paint(a, f["eye"], *left_eye)
    paint(a, f["eye"], *right_eye)
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
    p.add_argument("--out", required=True)
    a = p.parse_args()
    left = a.left_eye or FACES[a.face]["left"]
    right = a.right_eye or FACES[a.face]["right"]
    mouth = a.mouth or FACES[a.face]["mouth_at"]
    img = edit(a.src, a.face, a.top, a.zone, a.face_box, left, right, mouth)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    rec = {"time": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "tool": "tools/gen/face_edit.py",
           "src": Path(a.src).as_posix(), "src_sha256": hashlib.sha256(Path(a.src).read_bytes()).hexdigest(),
           "out": out.as_posix(), "face": a.face, "pattern": FACES[a.face], "top": a.top, "zone": a.zone,
           "face_box": a.face_box, "left_eye": left, "right_eye": right, "mouth": mouth}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    print(out)


if __name__ == "__main__":
    main()
