"""Write the beat sheet for the Lamplight A3 godot-gamedev (walker) explainer film.

Written by Claude, 2026-10-15, from the script Rui approved (SCRIPT-DRAFT.md; the only change is the greeting,
"Mingalaba", because "Sawubona" was already used by other toolkit reels). Code excerpts are read verbatim from
the repository at the film's source revision; still images are made by make_assets.py from real files;
capture windows and durations are filled in by cut_clips.py.

    F:/7270/film-env/Scripts/python.exe build_beats.py  ->  REEL/beat_sheet.json
"""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parent
REPO = Path("C:/Users/18500/Desktop/7270/Assignment2/walker-lamplight-rui-sun")
SLUG = "claude-liam-walker-lamplight-a3-gamedev"
TITLE = "Lamplight in 3D: Right Numbers, Wrong Look."
REV = (REEL / "capture" / "source-commit.txt").read_text().strip()
BUILD = (REEL / "capture" / "build_id.txt").read_text().strip()
SHORT = REV[:7]
JINGLE = json.loads((REEL / "jingle.json").read_text())


def excerpt(path, a, b):
    lines = (REPO / "godot" / path).read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[a - 1:b])


def narrated(bid, act, text, shot, role):
    return {"beat_id": bid, "act": act, "role_note": role, "narration_text": text, "voice": "am_onyx",
            "engine": "kokoro", "estimated_duration_s": max(4, round(len(text.split()) / 2.5)), "shot": shot}


def code_beat(bid, title, path, a, b, cues, notes, text, role):
    code = excerpt(path, a, b)
    lines = code.split("\n")
    return narrated(bid, "MECHANISM", text, {
        "type": "GRAPHIC", "source": "remotion", "motion": "code-cue",
        "remotion": {"pattern": "GodotDevWorkbench", "props": {
            "mode": "code", "title": title, "project": "walker-lamplight-rui-sun", "path": "godot/" + path,
            "source": f"Verbatim project source at commit {SHORT} · Godot editor reconstruction (teaching view)",
            "code": code, "startLine": a, "cues": cues,
            "codeFontSize": 24 if (len(lines) > 14 or max(map(len, lines)) > 100) else 26,
            "inspectorLabel": "Source notes — not Inspector values", "notes": notes}}}, role)


def still(bid, act, text, image, label, role, evidence=False):
    shot = {"type": "STILL", "source": "own", "motion": "hold", "label": label}
    if evidence:
        shot["evidence_media"] = f"media/{bid}.png"
    return {**narrated(bid, act, text, shot, role), "image_file": f"assets/{image}"}


def capture(bid, act, text, label, role, evidence=False):
    shot = {"type": "CAPTURE", "source": "screen", "label": label}
    if evidence:
        shot["evidence_media"] = f"media/{bid}.mp4"
    return narrated(bid, act, text, shot, role)


beats = []
beats.append(narrated("B00", "ASK",
    "Mingalaba, this is Liam, in for Bear. The ask, reconstructed: Lamplight is a 2D game about a lantern that is its "
    "own light. Make three simple 3D assets for it in Blender by directing Claude through the Blender MCP, change at "
    "least one thing by hand, and show all three together in Godot at the size the game needs.",
    {"type": "GRAPHIC", "source": "remotion", "motion": "type-on", "remotion": {"pattern": "ClaudeComposerAsk", "props": {
        "greeting": "Mingalaba, Liam", "topic": "WALKER · LAMPLIGHT 3D", "segment": "walker-lamplight-rui-sun",
        "command": "Please use Walker to convert my game design document about Lamplight, a 2D platformer where Wick, a "
                   "walking brass lantern, climbs out of a dark mine, into three simple 3D assets for the game: a lamp post, "
                   "an oil drop and a pit prop. Build each one in my open Blender through the Blender MCP, at the game's "
                   "scale, from basic shapes, then export it and show all three in a Godot 3D scene.",
        "runningText": "reading CHANGE-BRIEF.md, BLENDER-NOTES.md; get_scene_info…",
        "output": ["scale: 160 px = 1 m · Wick 0.35 m · tunnel 2.0 m",
                   "build: one execute_blender_code per part, read back after each",
                   "proof: Godot headless 30/0 + glb 18/0, and Rui's look"],
        "folderLabel": "@NikBearBrown", "modelLabel": "Claude", "effortLabel": "Opus"}}},
    "COLD OPEN LAW - Claude UI cold open. The prompt is an ILLUSTRATIVE RECONSTRUCTION of the walker ask, never a transcript."))
beats.append(narrated("B01", "BLUF",
    "Three assets: a lamp post, an oil drop and a pit prop. Claude wrote every line of the Blender code, through the MCP. "
    "Rui set the scale, approved every step, made the hand edit, and, after one look in Godot, doubled the oil drop. "
    "The numbers were right. The look was not.",
    {"type": "GRAPHIC", "source": "remotion", "motion": "type-on", "remotion": {"pattern": "BrutalistHesitantWriter", "props": {
        "text": "Lamplight in 3D:\nthe look was right.", "triggerWords": "right", "replacementWords": "wrong",
        "seed": "lamplight-a3-b01", "face": "serif", "fontSize": 190, "lineSpacing": 2.6, "align": "center",
        "charMs": 26, "jitter": 18, "mistakeRate": 0, "hesitateWithin": 0, "hesitateBetween": 0}}},
    "What was built, with one real correction: every number matched the brief, and Rui still found the look wrong."))
beats.append(capture("B02", "GAME",
    "This is the game the assets come from. Wick is a brass lantern, the oil drop refills his light, and the lamp post "
    "is where he comes back to. The game is flat, so these three are its first pieces in 3D, shown in a small room of "
    "their own.",
    "A2 slice footage, reused (same game build) · scripted-input capture run-01",
    "The 2D game, so the viewer knows what the three assets are for."))
beats.append(narrated("B03", "SCALE",
    "Everything starts with one conversion: one hundred sixty pixels is one metre. Wick's collider is fifty six "
    "pixels, so he is thirty five centimetres tall. A tunnel is three hundred twenty pixels, two metres. So the lamp "
    "post is seventy two and a half centimetres, copied from its pixels, and the pit prop is exactly one tunnel high.",
    {"type": "GRAPHIC", "source": "remotion", "motion": "reveal", "remotion": {"pattern": "GodotDesignBoard", "props": {
        "title": "One conversion: 160 px = 1 m", "section": "CHANGE-BRIEF.md §2 · Scale",
        "excerpt": "one conversion is fixed here and never changed: 160 px = 1 m (1 px = 6.25 mm).",
        "source": f"docs/a3/CHANGE-BRIEF.md · values from player.gd, lamplight_tunnel.json, session.gd · @ {SHORT}",
        "status": "DECIDED BY RUI · 2026-10-15", "visualLabel": "What the conversion gives",
        "layout": "cards", "cards": [
            {"label": "Wick", "text": "collider 36 × 56 px → 0.225 × 0.35 m"},
            {"label": "Tunnel", "text": "floor to ceiling 320 px → 2.0 m"},
            {"label": "Lamp post", "text": "116 px, drawn in code → 0.725 m, copied from its pixels"},
            {"label": "Pit prop", "text": "one tunnel high → 2.0 m"}],
        "cues": [{"at": 4, "card": 0}, {"at": 9, "card": 1}, {"at": 14, "card": 2}, {"at": 19, "card": 3}]}}},
    "The scale the brief is written in, each number from a cited line of A2 code."))
beats.append(narrated("B04", "BRIEF",
    "The brief was committed and tagged before anything was built. It fixed every size to the millimetre, put every "
    "origin at the base, set a triangle budget, and predicted nine failures: lying on its side, ten times too big, "
    "floating, scale not applied, colour lost, faces missing.",
    {"type": "GRAPHIC", "source": "remotion", "motion": "reveal", "remotion": {"pattern": "GodotDesignBoard", "props": {
        "title": "Predicted before built", "section": "CHANGE-BRIEF.md · header",
        "excerpt": "Written 2026-10-15, before any asset was built (the git timestamp of this file is the evidence).",
        "source": "git tag a3-brief = 9579486, 2026-10-15 15:23 -04:00 · first asset commit ad1c230 came after",
        "status": "COMMITTED BEFORE ANY ASSET · tag a3-brief", "visualLabel": "What the brief fixed",
        "layout": "cards", "cards": [
            {"label": "Sizes", "text": "lamp post 0.19375 × 0.0955 × 0.725 m · oil drop 0.1375 × 0.15 m · pit prop 1.2 × 2.0 m"},
            {"label": "Origins", "text": "centre of the underside; the lamp post's at its post foot"},
            {"label": "Budgets", "text": "72 / 120 / 60 triangles (course limit 500)"},
            {"label": "9 failures", "text": "on its side · ×10 size · floating · scale not applied · colour lost · faces missing · …"}],
        "cues": [{"at": 4, "card": 0}, {"at": 8, "card": 1}, {"at": 11, "card": 2}, {"at": 14, "card": 3}]}}},
    "Brief-before-build evidence and the predicted failure cases."))
beats.append(still("B05", "SETUP",
    "Rui learned the window first, and wrote the notes in Rui's own words. One line stuck: the default cube is two "
    "metres wide at a scale of one. Then the setup. The chapter's registration line failed as written: the dash e "
    "flag swallowed the server's name. Name first, and it connected.",
    "b05.png", "Screenshot by Rui + Claude's setup log", "Interface notes (Rui's screenshot) and the MCP setup friction."))
beats.append(still("B06", "BUILD",
    "Here is the loop, in Rui's real session. Rui approves a plan, and Claude builds one part per call: post, crossbar, "
    "lamp box, window, flame. Five boxes, sixty triangles. Every size is read back from the vertices, because the "
    "scene report rounds to two decimals.",
    "b06.png", "Screenshot by Rui + MCP look capture", "A real prompt to Claude and what the MCP built."))
beats.append(still("B07", "HAND EDIT",
    "Then Rui's hand edit. The flame looked a little dark, so Rui changed its base colour from amber to a pale yellow, "
    "F D F F A 6. Reading the edit back caught something else: the window glass had changed too, by accident. Rui "
    "said put it back, and it went back.",
    "b07.png", "Screenshot by Rui (after the edit)", "Rui's hand edit and the read-back that caught an accidental change."))
beats.append(still("B08", "OIL DROP",
    "The oil drop shows how a look gets argued. A round sphere at this size reads as a ball, so the body is squashed "
    "and a cone sits on it as the tip. Smooth shading exposed a seam, so the two were welded. Rui tried a highlight "
    "ball, and rejected it as ugly. Sixty four triangles.",
    "b08.png", "MCP look captures + the A2 sprite", "Inspect-and-revise inside Blender: shape, shading, a rejected part."))
beats.append(still("B09", "TRANSFORMS",
    "The pit prop, plain, read like a door frame, so Rui added two braces. Those braces sat at forty five degrees, with "
    "their scale not applied. Exported like that, Godot would get rotated, scaled nodes. Apply all transforms, and "
    "every asset leaves Blender at rotation zero, scale one, origin on the floor.",
    "b09.png", "MCP look captures + get_scene_info", "Why Apply Transforms matters, on a real unapplied state."))
# Pilot fix (2026-10-15): the panel shows 14 lines; lines 38-54 cut off the OilDrop node, so the excerpt is the four
# asset nodes (42-54) and the Floor moves to the notes panel.
beats.append(code_beat("B10", "A plain room, height zero.", "game3d/asset_room.tscn", 42, 54,
    [{"at": 2, "line": 42, "label": "each asset is an instanced .glb"},
     {"at": 6, "line": 43, "label": "placed at height 0: no offset, no scale"},
     {"at": 9, "line": 45, "label": "a Wick-sized box, 0.35 m, not an asset"},
     {"at": 13, "line": 54, "label": "the oil drop too: y = 0"}],
    [{"label": "Floor", "value": "line 38: a 4 × 2 m plane\nat y = 0"},
     {"label": "Light · camera", "value": "one DirectionalLight3D\n+ ambient · orbit camera"}],
    "In Godot, the room is a plain scene: a floor, one light, one camera, and each asset placed at height zero. No "
    "offset, no scale. If an origin were wrong, this is where an asset would float.",
    "Code → result 1: the room scene."))
beats.append(capture("B11", "RESULT",
    "And there they are at game scale, beside a box the size of Wick. The camera goes behind and under. The floor is "
    "one sided, so every bottom face can be checked.",
    "Godot 4.7.2 · asset room · scripted camera orbit (Claude's capture) · native 3840×2160",
    "Visible result of B10.", evidence=True))
# Pilot fix (2026-10-15): with 146-158 the wrapped long lines pushed the key lines 157-158 out of the panel.
beats.append(code_beat("B12", "Measured against the floor.", "tests/check_a3_assets.gd", 154, 158,
    [{"at": 2, "line": 154, "label": "each asset's box, in world space"},
     {"at": 4, "line": 155, "label": "and it must sit over the floor"},
     {"at": 6, "line": 157, "label": "the Floor node's own top, not the asset itself"},
     {"at": 8, "line": 158, "label": "within 1 mm of floor_y"}],
    [{"label": "floor_y", "value": "line 148: the Floor\nnode's top (its own box)"},
     {"label": "Also checks", "value": "size · base y 0 · upright\nnode scale · triangles · colour"}],
    "The headless check measures each asset against the floor node, not against itself. A check that only measured "
    "the asset would prove nothing about the floor.",
    "Code → result 2: the headless check."))
beats.append(still("B13", "RESULT",
    "Headless: thirty checks, zero failures, every size within a millimetre of the brief. And each kind of check was "
    "broken on purpose, to see it fail: export without Y up, lift the drop five centimetres, keep a stale file. Each "
    "one failed.",
    "b13.png", "Headless output, verbatim (capture/test-output.txt)",
    "Visible result of B12: actual recorded output, including the deliberate failures.", evidence=True))
beats.append(still("B14", "HUMAN CHECK",
    "Then the check no script can run. Rui walked the camera around and said: the oil drop can't be this small, and "
    "the frame is a bit too big. The drop's fifteen centimetres was the exact pixel conversion. The numbers were right; "
    "the look was not. So the drop doubled, and the frame got narrower and thinner, still two metres tall.",
    "b14.png", "Before re-rendered from 8d07135 · after from the current build",
    "Rui's human check and the revision it caused."))
beats.append(narrated("B15", "VERDICT",
    "The verdict. Shown working: three assets built through the MCP, exported upright, at the brief's size, standing "
    "on the floor, with forty eight checks passing. Still uncertain: the colours render brighter than their hex "
    "values, the room is not lit like the game, and Wick is still a box. Next: light the room the way the game is lit. "
    "Claude wrote every line of Blender and Godot code. Rui chose the assets and the scale, made the hand edit, and made "
    "the call that changed two sizes.",
    {"type": "GRAPHIC", "source": "remotion", "motion": "reveal", "remotion": {"pattern": "ClaudeVerdictArtifact", "props": {
        "artifactTitle": "Verdict",
        "artifactHeading": f"walker-lamplight-rui-sun @ {SHORT} · shown, checked, still open",
        "artifactLines": [
            "shown working — lamp post, oil drop, pit prop: built through the Blender MCP, exported as glTF, upright, at the brief's size, on the floor.",
            "checked — Godot headless 30/0 and glb file check 18/0; each kind of check broken on purpose and seen to fail; A2's 99 still pass.",
            "uncertain — colours render brighter than their hex values; the room is not lit like the game; Wick is a box stand-in.",
            "next step — light the room the way Lamplight is lit (dark, one warm point light) and look again.",
            "who made what — Claude: all Blender and Godot code, checks, this film · Rui: scale, assets, approvals, the hand edit, the two size changes.",
            f"source shown — commit {SHORT} · build {BUILD[:12]} · Godot 4.7.2 · Blender 5.1.2 · mcp-for-blender 2.1.9."]}}},
    "Verdict: checked, uncertain, next step, contributions, source revision."))
beats.append(narrated("B16", "HANDOFF",
    "Your turn. Here is the paste ready prompt. Pick one asset from your game and write its size in metres from "
    "something the player already knows. Predict the one way it will go wrong, and the check that would catch it. "
    "Build it through the MCP, put it in Godot, and look at it beside your character before you trust the numbers. "
    "Liam, in for Bear.",
    {"type": "GRAPHIC", "source": "remotion", "motion": "type-on", "remotion": {"pattern": "ClaudeComposerAsk", "props": {
        "greeting": "Your turn.", "topic": "WALKER · LAMPLIGHT 3D", "segment": "your turn",
        "command": "Use Walker with the Blender MCP. Pick one asset from my game and write its size in metres from something "
                   "the player already knows. Before building, predict one way it will fail and the check that would catch it. "
                   "Build it one part per call, apply transforms, export glTF with +Y up, and place it in Godot beside my "
                   "character. Show me the numbers, then let me look before we trust them.",
        "runningText": "reading the brief; get_scene_info; checking against the floor…",
        "output": ["size in metres, from the player's own scale",
                   "one predicted failure, one check that can fail",
                   "a human look beside the character, then revise"],
        "folderLabel": "@NikBearBrown", "modelLabel": "Claude", "effortLabel": "Opus"}}},
    "Your Turn - a paste-ready Walker prompt; Liam signs off here, before the final card."))
beats.append({"beat_id": "B17", "act": "OUTRO",
              "role_note": "OUTRO LOCK - ClaudeTitleOutro, exact title, @NikBearBrown, slug-seeded mascot/jingle.",
              "narration_text": "", "audio_file": JINGLE["audio_file"],
              "jingle": {k: JINGLE[k] for k in ("source", "pick", "gain_db")},
              "estimated_duration_s": JINGLE["duration_s"], "actual_duration_s": JINGLE["duration_s"],
              "shot": {"type": "GRAPHIC", "source": "remotion", "motion": "reveal",
                       "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG,
                                                                             "durationSeconds": JINGLE["duration_s"]}}}})

sheet = {"metadata": {
    "title": TITLE, "slug": SLUG, "topic": "WALKER · LAMPLIGHT 3D", "kind": "gamedev", "playlist": "Brutalist",
    "brand": "claude-liam", "audience": "CSYE 7270 reviewers and Walker readers", "register": "Teardown",
    "engine": "kokoro", "voice": "am_onyx", "voice_kokoro": "am_onyx", "palette": "claude", "style_preset": "claude",
    "ground": "#FAF9F5", "aspect_ratio": "16:9", "fit": "contain", "captions": False, "channel": "@NikBearBrown",
    "channel_title": "@NikBearBrown", "folderLabel": "@NikBearBrown", "greeting": "Mingalaba, Liam",
    "greeting_note": "hello lexicon: Mingalaba (Burmese, one word), not used by any reel in this toolkit's youtube/, examples/ "
                     "or the A1/A2 reels (Sawubona, the draft's choice, was already used).",
    "persona": "Liam (in for Bear)", "presenter": "Liam (in for Bear)", "in_for_bear": True,
    "episode_id": "walker-lamplight-a3-gamedev",
    "note": f"godot-gamedev in walker mode over walker-lamplight-rui-sun (CSYE 7270 Assignment 3). Source commit {REV}, "
            f"build_id {BUILD}, Godot 4.7.2.stable.official.ed1daf0bf, Blender 5.1.2, mcp-for-blender 2.1.9. B02 reuses A2's "
            "scripted-input footage of the same 2D game build (A2 reel, run-01). B11 is native 3840x2160 Godot Movie Maker "
            "output of the asset room with a scripted camera. Stills are Rui's screenshots, MCP look captures from Rui's "
            "Blender session, and recorded tool output; all labelled in frame."},
    "beats": beats}
(REEL / "beat_sheet.json").write_text(json.dumps(sheet, indent=1, ensure_ascii=False), encoding="utf-8")
print(len(beats), "beats ->", REEL / "beat_sheet.json")
