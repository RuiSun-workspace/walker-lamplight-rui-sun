"""Pilot fix for B10 and B12 (Claude, 2026-10-15), applied in place so the provenance stamps that
remotion_scenes.py wrote into beat_sheet.json are kept. The same change is in build_beats.py and make_evidence.py.
B10: lines 38-54 overflowed the 14-line panel (the OilDrop node was cut off) -> 42-54.
B12: 146-158 wrapped so that the key lines 157-158 fell out of the panel -> 154-158.
"""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parent
REPO = Path("C:/Users/18500/Desktop/7270/Assignment2/walker-lamplight-rui-sun")
FIX = {
    "B10": ("game3d/asset_room.tscn", 42, 54,
            [(42, "each asset is an instanced .glb"), (43, "placed at height 0: no offset, no scale"),
             (45, "a Wick-sized box, 0.35 m, not an asset"), (54, "the oil drop too: y = 0")],
            [{"label": "Floor", "value": "line 38: a 4 × 2 m plane\nat y = 0"},
             {"label": "Light · camera", "value": "one DirectionalLight3D\n+ ambient · orbit camera"}]),
    "B12": ("tests/check_a3_assets.gd", 154, 158,
            [(154, "each asset's box, in world space"), (155, "and it must sit over the floor"),
             (157, "the Floor node's own top, not the asset itself"), (158, "within 1 mm of floor_y")],
            [{"label": "floor_y", "value": "line 148: the Floor\nnode's top (its own box)"},
             {"label": "Also checks", "value": "size · base y 0 · upright\nnode scale · triangles · colour"}]),
}
sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
for b in sheet["beats"]:
    if b["beat_id"] not in FIX:
        continue
    path, a, z, cues, notes = FIX[b["beat_id"]]
    code = "\n".join((REPO / "godot" / path).read_text(encoding="utf-8").splitlines()[a - 1:z])
    lines = code.split("\n")
    p = b["shot"]["remotion"]["props"]
    dur = float(p["durationSeconds"])
    p["code"], p["startLine"], p["notes"] = code, a, notes
    p["codeFontSize"] = 24 if (len(lines) > 14 or max(map(len, lines)) > 100) else 26
    p["cues"] = [{"at": round(dur * (0.08 + 0.8 * i / (len(cues) - 1)), 2), "line": ln, "label": lab}
                 for i, (ln, lab) in enumerate(cues)]
    print(b["beat_id"], path, a, z, len(lines), "lines, font", p["codeFontSize"])
(REEL / "beat_sheet.json").write_text(json.dumps(sheet, indent=1, ensure_ascii=False), encoding="utf-8")
