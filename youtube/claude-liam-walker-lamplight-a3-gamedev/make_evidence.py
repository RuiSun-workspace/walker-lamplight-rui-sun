"""Write gamedev-evidence.json (schema 1, teaching_contract code-then-result-v1) for the Lamplight A3 film.

Written by Claude, 2026-10-15. Inventories every authored file in godot/ (except .godot/ and .uid), hashes it,
assigns the Assignment 3 files to components and excludes Assignment 2's 2D-slice files with a reason (they are
explained by the A2 film and unchanged by A3), records the verbatim excerpts shown on screen, and pairs each
code beat with the next beat's hashed media. Run AFTER cut_clips.py.

    F:/7270/film-env/Scripts/python.exe make_evidence.py
"""
import hashlib
import json
from pathlib import Path

REEL = Path(__file__).resolve().parent
REPO = Path("C:/Users/18500/Desktop/7270/Assignment2/walker-lamplight-rui-sun")
GAME = REPO / "godot"
A2_FILM = ("Assignment 2's 2D asset slice, unchanged by A3 (only Godot-generated .uid files were added); explained by "
           "the A2 film claude-liam-walker-lamplight-gamedev.mp4 (SHA-256 f0ae6284…41d7); outside this film's scope")

COMPONENTS = {
    "three-assets": (
        "lamp_post, oil_drop and pit_prop: built in Blender through the MCP (tools/blender/build_*.py), all transforms "
        "applied, exported as glTF binary with +Y Up (tools/blender/export_glb.py); Godot imports them with root scale 1.0.",
        ["B06", "B07", "B08", "B09", "B14"],
        [f"assets/models/{a}.glb{x}" for a in ("lamp_post", "oil_drop", "pit_prop") for x in ("", ".import")]),
    "asset-room": (
        "asset_room.tscn: a 4 x 2 m floor at y 0, one DirectionalLight3D plus ambient, the three instanced assets at "
        "height 0 and a Wick-sized stand-in box; orbit_camera.gd lets a viewer (or the capture driver) look from behind "
        "and below; capture_a3_room.gd saves scripted evidence screenshots.",
        ["B10", "B11"],
        ["game3d/asset_room.tscn", "game3d/orbit_camera.gd", "tests/capture_a3_room.gd"]),
    "headless-check": (
        "check_a3_assets.gd loads each imported .glb and the room and checks size, bounds, base at y 0, upright axis, "
        "node scale and rotation, triangles, albedo, and each asset against the Floor node's top (30 checks).",
        ["B12", "B13"],
        ["tests/check_a3_assets.gd"]),
}
EXCERPTS = [("B10", "game3d/asset_room.tscn", 42, 54), ("B12", "tests/check_a3_assets.gd", 154, 158)]
PAIRS = [
    ("B10", "B11", "media/B11.mp4", "The room as saved: floor, light, the three assets at height 0 beside the Wick-sized box; "
     "the scripted camera goes behind (9 s) and below (13 s), where the one-sided floor shows every asset's closed underside."),
    ("B12", "B13", "media/B13.png", "Recorded output: check_a3_assets 30 checks, 0 failed; check_glb 18, 0 failed; and the "
     "three deliberate faults (+Y Up off, drop lifted 0.05 m, stale files) each producing FAIL lines."),
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    files = sorted(p.relative_to(GAME).as_posix() for p in GAME.rglob("*") if p.is_file()
                   and not any(x in (".godot", ".git") for x in p.relative_to(GAME).parts) and p.suffix != ".uid")
    owner = {}
    for cid, (_, _, paths) in COMPONENTS.items():
        for p in paths:
            owner.setdefault(p, []).append(cid)
    unknown = [p for p in owner if p not in files]
    assert not unknown, unknown
    exclusions = {f: A2_FILM for f in files if f not in owner}
    roles = {".gd": "script", ".glb": "3D asset (glTF binary)", ".import": "import settings", ".tscn": "scene"}
    data = {
        "schema_version": 1, "teaching_contract": "code-then-result-v1",
        "source_revision": (REEL / "capture" / "source-commit.txt").read_text().strip(),
        "build_id": (REEL / "capture" / "build_id.txt").read_text().strip(),
        "files": [{"path": f, "sha256": sha(GAME / f), "role": roles.get(Path(f).suffix, "config"), "component_ids": owner[f]}
                  for f in files if f in owner],
        "components": [{"id": cid, "explanation": e, "beat_ids": b, "files": paths} for cid, (e, b, paths) in COMPONENTS.items()],
        "excerpts": [{"beat_id": bid, "path": p, "start_line": a, "end_line": z,
                      "text": "\n".join((GAME / p).read_text(encoding="utf-8").splitlines()[a - 1:z])} for bid, p, a, z in EXCERPTS],
        "exclusions": [{"path": p, "reason": r} for p, r in exclusions.items()],
        "code_result_pairs": [{"code_beat": c, "result_beat": r, "observation": o, "media": {"path": m, "sha256": sha(REEL / m)}}
                              for c, r, m, o in PAIRS],
    }
    (REEL / "gamedev-evidence.json").write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
    print(len(data["files"]), "files,", len(data["exclusions"]), "exclusions,", len(data["excerpts"]), "excerpts,", len(PAIRS), "pairs")


if __name__ == "__main__":
    main()
