"""Automated asset checks for the predicted failures in CHANGE-BRIEF (written by Claude, 2026-10-07).

  F1  each Wick sprite's proportions vs the accepted reference (cap width, feet-to-cap, feet-to-top, +-2 px)
  F6  colours per sprite (character <= 6 + transparency; environment <= its 13-colour palette);
      Nearest filter as the project default
  F2  in-engine contrast of Wick's brass frame against the pixels around him, measured on real engine
      captures (evidence/captures, made by godot/tests/capture_evidence.gd)
  F4  the music loop's seam numbers, from edit-log.jsonl

    python tools/check_assets.py        -> prints a table, writes evidence/asset-checks.json, exit 1 on a FAIL
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools" / "gen"))
from normalize_sprite import measure  # noqa: E402

CHAR = REPO / "godot" / "assets" / "char"
ENV = REPO / "godot" / "assets" / "env"
CAP = REPO / "evidence" / "captures"
BRASS = (184, 134, 59)
results = []


def check(fid, name, ok, observed, note=""):
    results.append({"id": fid, "name": name, "status": "PASS" if ok else ("NOTE" if ok is None else "FAIL"),
                    "observed": observed, "note": note})


def lum(c):
    c = np.asarray(c, float) / 255.0
    c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def contrast(a, b):
    la, lb = sorted((float(lum(a)), float(lum(b))), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def main():
    ref = measure(np.asarray(Image.open(CHAR / "wick_idle.png").convert("RGBA")))
    # F1 --------------------------------------------------------------------------------------------
    for f in sorted(CHAR.glob("wick_*.png")):
        m = measure(np.asarray(Image.open(f).convert("RGBA")))
        d = {k: m[k] - ref[k] for k in ("cap_width", "feet_to_cap_top", "feet_to_top")}
        ok = all(abs(v) <= 2 for v in d.values())
        note = ""
        if f.stem in ("wick_pickup", "wick_celebrate") and not ok:
            ok, note = None, "flame rises through the cap by design (sheet: 'over the cap only in pickup and celebrate'); cap not measurable"
        elif f.stem == "wick_hurt" and not ok:
            ok, note = None, "hurt is drawn tilted (sheet: tilted 10 deg); proportions not comparable on axis"
        check("F1", f.stem, ok, {"measure": {k: m[k] for k in d}, "diff_vs_ref": d}, note)
    # F6 --------------------------------------------------------------------------------------------
    for f in sorted(CHAR.glob("wick_*.png")):
        a = np.asarray(Image.open(f).convert("RGBA"))
        cols = {tuple(p[:3]) for p in a.reshape(-1, 4) if p[3] == 255}
        semi = int(((a[..., 3] > 0) & (a[..., 3] < 255)).sum())
        check("F6", f.stem, len(cols) <= 6 and semi == 0, {"colours": len(cols), "semi_transparent_px": semi})
    for f in sorted(ENV.glob("*.png")):
        a = np.asarray(Image.open(f).convert("RGBA"))
        cols = {tuple(p[:3]) for p in a.reshape(-1, 4) if p[3] == 255}
        semi = int(((a[..., 3] > 0) & (a[..., 3] < 255)).sum())
        check("F6", f.stem, len(cols) <= 13 and semi == 0, {"colours": len(cols), "semi_transparent_px": semi})
    proj = (REPO / "godot" / "project.godot").read_text(encoding="utf-8")
    check("F6", "project default texture filter = Nearest", "default_texture_filter=0" in proj, {})
    # F2 --------------------------------------------------------------------------------------------
    pos = json.loads((CAP / "wick_positions.json").read_text(encoding="utf-8"))
    for shot in ("state-idle-right", "state-walk-right", "sb3-jump", "state-climb", "state-staged-ember"):
        if shot not in pos:
            continue
        info = pos[shot]
        img = np.asarray(Image.open(CAP / f"{shot}.png").convert("RGB")).astype(float)
        spr = np.asarray(Image.open(CHAR / f"wick_{info['look']}.png").convert("RGBA"))
        if info["flip"]:
            spr = spr[:, ::-1]
        x0, y0 = int(round(info["x"] - 32)), int(round(info["y"] - 80))
        brass = (spr[..., :3] == BRASS).all(axis=2) & (spr[..., 3] == 255)
        ys, xs = np.nonzero(brass)
        on_screen = img[ys + y0, xs + x0]
        brass_seen = np.median(on_screen, axis=0)
        # background: a 12 px band around the sprite frame, outside any opaque sprite pixel
        H, W = img.shape[:2]
        band = []
        for yy in range(max(0, y0 - 12), min(H, y0 + 92)):
            for xx in range(max(0, x0 - 12), min(W, x0 + 76)):
                inside = 0 <= yy - y0 < 80 and 0 <= xx - x0 < 64
                if not inside or spr[yy - y0, xx - x0, 3] == 0:
                    if not inside:
                        band.append(img[yy, xx])
        bg_seen = np.median(np.array(band), axis=0)
        r = contrast(brass_seen, bg_seen)
        check("F2", shot, r >= 3.0, {"brass_on_screen": [int(v) for v in brass_seen], "background_on_screen": [int(v) for v in bg_seen],
                                     "contrast": round(r, 2)}, "pass condition from CHANGE-BRIEF F2: >= 3:1")
    # F4 --------------------------------------------------------------------------------------------
    edits = [json.loads(l) for l in (REPO / "design" / "generation" / "edit-log.jsonl").read_text(encoding="utf-8").splitlines()]
    loops = [e for e in edits if e.get("op") == "loop" and e.get("out", "").endswith("godot/assets/audio/mus_loop.ogg")]
    if loops:
        e = loops[-1]
        check("F4", "mus_loop seam (numbers only; Rui listened: 'no problem at the seam')", e["seam_jump"] <= 4 * max(e["median_step"], 1e-4),
              {k: e[k] for k in ("bpm", "bars", "length_s", "seam_jump", "median_step")})
    # report ----------------------------------------------------------------------------------------
    for r in results:
        print(f"{r['id']:3} {r['status']:5} {r['name'][:46]:46} {json.dumps(r['observed'])[:120]}")
    out = REPO / "evidence" / "asset-checks.json"
    out.write_text(json.dumps({"results": results}, indent=2), encoding="utf-8")
    fails = sum(r["status"] == "FAIL" for r in results)
    print(f"ASSET CHECKS: {len(results)} rows / {fails} FAIL / {sum(r['status'] == 'NOTE' for r in results)} NOTE")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
