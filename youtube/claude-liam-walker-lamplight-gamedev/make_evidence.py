"""Write gamedev-evidence.json (schema 1, teaching_contract code-then-result-v1) for the Lamplight film.

Written by Claude, 2026-10-07. Inventories every authored file in godot/ (except .godot/ and .uid), hashes it,
assigns it to a component or excludes it with a reason, records the verbatim code excerpts shown on screen,
and pairs each code beat with the next beat's hashed media. Run AFTER cut_clips.py (media must exist).

    python youtube/claude-liam-walker-lamplight-gamedev/make_evidence.py
"""
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GAME = REPO / "godot"
REEL = Path("F:/7270/reels/claude-liam-walker-lamplight-gamedev")

COMPONENTS = {
    "wick-state-images": (
        "Nine generated 64x80 state images; player.gd swaps one per state (movement or event look) and flips for "
        "facing, never animating. tuning.gd holds the x2-scaled walker-jumpman movement values.",
        ["B06", "B07", "B08"],
        ["features/player/player.gd", "features/player/tuning.gd"] + [f"assets/char/wick_{s}.png{x}" for s in
         ("idle", "walk", "jump", "fall", "climb", "pickup", "ember", "hurt", "celebrate") for x in ("", ".import")]),
    "oil-and-rules": (
        "session.gd owns the state machine, oil drain (6/s), pickups (+35, marked before the signal), lamp-post "
        "checkpoints, the 4 s ember burn-out and the signals sound listens to; the v2 level data is the three tunnels.",
        ["B02", "B09", "B10", "B14", "B15"],
        ["game/session.gd", "levels/lamplight_tunnel.json", "game/main.tscn"]),
    "light-and-overlay": (
        "lighting.gd darkens the scene and sizes Wick's light from the oil (240 px -> 56 px ring -> 28 px as the ember "
        "burns out); overlay.gd draws spikes, drops, lamp flames and the exit unshaded, and the red death flash.",
        ["B03", "B15"],
        ["game/lighting.gd", "game/overlay.gd"]),
    "sound": (
        "audio_director.gd only listens to game signals, plays one sound per event and counts it; the music loop "
        "follows oil through a low-pass, ducks on death, pauses and stops; N/B mute separate buses.",
        ["B11", "B12"],
        ["audio/audio_director.gd", "audio/default_bus_layout.tres"] + [f"assets/audio/{n}.ogg{x}" for n in
         ("sfx_jump", "sfx_pickup", "sfx_hurt", "sfx_exit", "mus_loop") for x in ("", ".import")]),
    "environment-art": (
        "Generated back wall, rock tiles, ledge-top edit, spikes, oil drop and ladder, drawn by session.gd and overlay.gd.",
        ["B02", "B05"],
        [f"assets/env/{n}.png{x}" for n in ("bg_rock", "tiles_rock", "tiles_rock_top", "spikes", "oil_drop", "ladder")
         for x in ("", ".import")]),
    "hud": (
        "hud.gd draws the oil gauge (red and blinking faster as the ember burns out), timer, retries, controls, mute "
        "indicators and the title / pause / end cards.",
        ["B02", "B15"],
        ["ui/hud.gd"]),
    "project-config": (
        "project.godot: 1280x720 viewport (doubled when the sprite became 64x80), Nearest texture filter, audio bus "
        "layout; .gitignore keeps the engine cache out.",
        ["B06"],
        ["project.godot", ".gitignore"]),
    "tests": (
        "Headless suites run by tools/run_tests.sh at --fixed-fps 60, plus the evidence and film capture drivers that "
        "press real Input actions along the route.",
        ["B17", "B18"],
        ["tests/test_game.gd", "tests/test_keyboard.gd", "tests/test_wick.gd", "tests/test_oil.gd", "tests/test_audio.gd",
         "tests/route_driver.gd", "tests/capture_evidence.gd", "tests/capture_film.gd"]),
}
EXCLUSIONS = {
    "levels/first_steps.json": "walker-jumpman's starter level, scaled x2 in step 1; the slice no longer loads it",
    "levels/lamplight_tunnel_v1_two_tunnels.json": "level v1 kept as the record of the two-tunnel slice; not loaded",
    "tests/capture_game.gd": "walker-jumpman's original screenshot script; superseded by capture_evidence.gd, not run",
}
EXCERPTS = [("B07", "features/player/player.gd", 137, 150), ("B09", "game/session.gd", 275, 285),
            ("B11", "audio/audio_director.gd", 43, 55), ("B14", "game/session.gd", 249, 258),
            ("B17", "tests/test_audio.gd", 161, 176)]
PAIRS = [
    ("B07", "B08", "media/B08.mp4", "The image changes with the state in real play: walk, then the faceless climb image on the ladder (a front view standing in for the back view), then arms up rising and arms out falling."),
    ("B09", "B10", "media/B10.mp4", "Landing on the middle-tunnel platform takes the drop: pickup image, flame over the cap, gauge up, light opens."),
    ("B11", "B12", "media/B12.mp4", "An early jump lands on the pit spikes: hurt sound (game audio under the narration), red spike flash, respawn at the lamp post."),
    ("B14", "B15", "media/B15.mp4", "With no input the ember ring shrinks, the gauge blinks faster, and after 4 s the flame goes out: 'Your flame went out'."),
    ("B17", "B18", "media/B18.png", "Recorded output of tools/run_tests.sh: five suites, 99 checks, 0 failures; check_assets.py 31 rows, 0 FAIL."),
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
    missing = [f for f in files if f not in owner and f not in EXCLUSIONS]
    extra = [p for p in list(owner) + list(EXCLUSIONS) if p not in files]
    assert not missing and not extra, ("unassigned", missing, "unknown", extra)
    roles = {".gd": "script", ".json": "level data", ".png": "generated image", ".ogg": "generated audio",
             ".import": "import settings", ".tres": "resource", ".tscn": "scene", ".godot": "project settings"}
    data = {
        "schema_version": 1, "teaching_contract": "code-then-result-v1",
        "source_revision": (REEL / "capture" / "source-commit.txt").read_text().strip(),
        "build_id": (REEL / "capture" / "build_id.txt").read_text().strip(),
        "files": [{"path": f, "sha256": sha(GAME / f), "role": roles.get(Path(f).suffix, "config"), "component_ids": owner[f]}
                  for f in files if f in owner],
        "components": [{"id": cid, "explanation": e, "beat_ids": b, "files": paths} for cid, (e, b, paths) in COMPONENTS.items()],
        "excerpts": [{"beat_id": bid, "path": p, "start_line": a, "end_line": z,
                      "text": "\n".join((GAME / p).read_text(encoding="utf-8").splitlines()[a - 1:z])} for bid, p, a, z in EXCERPTS],
        "exclusions": [{"path": p, "reason": r} for p, r in EXCLUSIONS.items()],
        "code_result_pairs": [{"code_beat": c, "result_beat": r, "observation": o, "media": {"path": m, "sha256": sha(REEL / m)}}
                              for c, r, m, o in PAIRS],
    }
    (REEL / "gamedev-evidence.json").write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
    print(len(data["files"]), "files,", len(data["exclusions"]), "exclusions,", len(data["excerpts"]), "excerpts,", len(PAIRS), "pairs")


if __name__ == "__main__":
    main()
