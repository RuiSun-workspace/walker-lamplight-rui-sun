"""Write the beat sheet for the Lamplight godot-gamedev (walker) explainer film.

Written by Claude, 2026-10-07. Narration, code excerpts (read verbatim from the repo at the film's
source revision) and Remotion props live here so the film can be rebuilt. Gameplay clip windows are
filled in by cut_clips.py from the measured capture logs; this script only states which take and
which moment each gameplay beat shows.

    python youtube/claude-liam-walker-lamplight-gamedev/build_beats.py  ->  REEL/beat_sheet.json
"""
import base64
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
REEL = Path("F:/7270/reels/claude-liam-walker-lamplight-gamedev")
SLUG = "claude-liam-walker-lamplight-gamedev"
TITLE = "Lamplight: Generated, Then Played."
REV = (REEL / "capture" / "source-commit.txt").read_text().strip()
BUILD = (REEL / "capture" / "build_id.txt").read_text().strip()
SHORT = REV[:7]


def excerpt(path, a, b):
    lines = (REPO / "godot" / path).read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[a - 1:b])


def data_uri(name):
    return "data:image/png;base64," + base64.b64encode((REEL / "assets" / name).read_bytes()).decode()


def narrated(bid, act, text, shot, role):
    return {"beat_id": bid, "act": act, "role_note": role, "narration_text": text, "voice": "am_onyx",
            "engine": "kokoro", "estimated_duration_s": max(4, round(len(text.split()) / 2.5)), "shot": shot}


def code_beat(bid, title, path, a, b, cues, notes, text, role):
    return narrated(bid, "MECHANISM", text, {
        "type": "GRAPHIC", "source": "remotion", "motion": "code-cue",
        "remotion": {"pattern": "GodotDevWorkbench", "props": {
            "mode": "code", "title": title, "project": "walker-lamplight-rui-sun", "path": "godot/" + path,
            "source": f"Verbatim project source at commit {SHORT} · Godot editor reconstruction (teaching view)",
            "code": excerpt(path, a, b), "startLine": a, "cues": cues,
            "inspectorLabel": "Source notes — not Inspector values", "notes": notes}}}, role)


def capture_beat(bid, act, take, moment, text, label, role, evidence_media=False):
    shot = {"type": "CAPTURE", "source": "screen", "take": take, "moment": moment,
            "label": label + f" · scripted-input capture · native 3840x2160 Godot Movie Maker · {take}"}
    if evidence_media:
        shot["evidence_media"] = f"media/{bid}.mp4"
    return narrated(bid, act, text, shot, role)


beats = []
beats.append(narrated("B00", "ASK",
    "Kumusta, this is Liam, in for Bear. The ask, reconstructed: take a one page design about a lantern that is "
    "its own light. Design the look and the sound on paper first. Then make the art, the sound effects and the "
    "music with free local models, and prove they work together in a small playable Godot scene.",
    {"type": "GRAPHIC", "source": "remotion", "motion": "type-on", "remotion": {"pattern": "ClaudeComposerAsk", "props": {
        "greeting": "Kumusta, Liam", "topic": "WALKER · LAMPLIGHT", "segment": "walker-lamplight-rui-sun",
        "command": "Please use Walker to convert my game design document about Wick, a walking lantern spirit escaping a dark "
                   "mine (oil drains every second, the light is the oil gauge, at zero the ember lasts four seconds) into a "
                   "Godot asset slice. Design first: concept, hand-drawn storyboard, character sheet. Then generate the art "
                   "with SDXL and the sounds and music with MusicGen, locally, log every prompt and rejection, and wire them "
                   "in so sound only listens to the game.",
        "runningText": "reading CONCEPT.md, STORYBOARD.md, CHARACTER-SHEET.md, CHANGE-BRIEF.md…",
        "output": ["art: SDXL base 1.0 → pixelised six-colour sprites, 9 states at 64×80",
                   "audio: MusicGen medium → 4 event sounds + an 8-bar loop at 90 bpm, picked by ear",
                   "proof: 99 automated checks, 31 asset checks, 6 playtests by Rui"],
        "folderLabel": "@NikBearBrown", "modelLabel": "Claude", "effortLabel": "Opus"}}},
    "COLD OPEN LAW - Claude UI cold open. The prompt is an ILLUSTRATIVE RECONSTRUCTION of the walker ask, never a transcript."))
beats.append(narrated("B01", "BLUF",
    "The design said one short tunnel. The slice you are about to see is three, and that change did not come from "
    "me. It came from Rui playing it. Six playtests made the ember burn out, tripled the map, and pulled the jump "
    "sound down sixteen decibels. Every image and every sound was generated locally, for free, and every "
    "rejection is logged.",
    {"type": "GRAPHIC", "source": "remotion", "motion": "type-on", "remotion": {"pattern": "BrutalistHesitantWriter", "props": {
        "text": "Lamplight\none tunnel.", "triggerWords": "one, tunnel", "replacementWords": "three, tunnels",
        "seed": "lamplight-b01", "face": "serif", "fontSize": 210, "lineSpacing": 2.6, "align": "center",
        "charMs": 26, "jitter": 18, "mistakeRate": 0, "hesitateWithin": 0, "hesitateBetween": 0}}},
    "What was built, with one real correction: CONCEPT v1 scoped one tunnel; Rui's playtests grew it to three."))
beats.append(capture_beat("B02", "GAMEPLAY", "run-01", "title, Enter, the first jumps",
    "This is the running slice. You are Wick, a brass lantern on two legs. The circle of warm light is the only "
    "thing you see by, and it is also the oil gauge. It shrinks every second you do not find more.",
    "Game audio retained quietly under narration", "Real play from the first take; introduces the concept."))
beats.append(narrated("B03", "PILLARS",
    "Four pillars, and each one is a mechanism, not a mood board. Light is life: the light radius is the oil. "
    "Every second burns: six units a second, and at zero you get four seconds of ember. Fair in the dark: spikes "
    "keep a cold glint even outside your light. And the way out glows: the exit is the only cool light in a warm "
    "and black world.",
    {"type": "GRAPHIC", "source": "remotion", "motion": "reveal", "remotion": {"pattern": "GodotDesignBoard", "props": {
        "title": "Four pillars, four mechanisms", "section": "CONCEPT.md · Design pillars",
        "excerpt": "Light is life · Every second burns · Fair in the dark · The way out glows",
        "source": f"CONCEPT.md (v1 + appended revisions) · walker-lamplight-rui-sun @ {SHORT}",
        "status": "IMPLEMENTED · values from session.gd / lighting.gd", "visualLabel": "What each pillar became in code",
        "layout": "cards", "cards": [
            {"label": "Light is life", "text": "light radius follows oil: 240 px full → 56 px ring at zero"},
            {"label": "Every second burns", "text": "oil drains 6/s; at zero the ember lasts 4 s, then a failure"},
            {"label": "Fair in the dark", "text": "spikes keep a cold glint unlit; the ones that killed you flash red"},
            {"label": "The way out glows", "text": "the exit is the only cool, white light in the level"}],
        "cues": [{"at": 4, "card": 0}, {"at": 9, "card": 1}, {"at": 15, "card": 2}, {"at": 20, "card": 3}]}}},
    "Concept and pillars in plain terms, each tied to the value that implements it."))
beats.append(narrated("B04", "DESIGN",
    "The design came first, and it is dated. Rui drew the storyboard by hand: eight panels, three shot sizes, "
    "three camera angles. The character sheet set the contract: the collider, a six colour palette, and the rule "
    "that the face lives in the flame. All of it was committed and tagged design v1 before a single image was "
    "generated.",
    {"type": "GRAPHIC", "source": "remotion", "motion": "reveal", "remotion": {"pattern": "GodotDesignBoard", "props": {
        "title": "Designed before generated", "section": "STORYBOARD.md v2 (hand-drawn) · CHARACTER-SHEET.md",
        "excerpt": "8 panels · wide / medium / close-up · high / eye level / Dutch\nCollider 18×28 (later ×2) · palette of 6 · face lives in the flame",
        "source": "design/storyboard/hand/*.png (photo of Rui's sheet, cropped only) · git tag design-v1 = 6b5d099, 2026-10-06 01:52 -04:00",
        "status": "COMMITTED BEFORE ANY GENERATION · tag design-v1", "visualLabel": "Rui's hand-drawn storyboard, all eight panels",
        "layout": "image", "image": data_uri("b04-storyboard.png"),
        "cards": [{"label": "Character sheet", "text": "drawn as SVG by Claude (Rui's choice); the storyboard is Rui's hand"}]}}},
    "Design-before-generation evidence: the hand-drawn storyboard and the design-v1 tag."))
beats.append(narrated("B05", "TRACE",
    "Now one asset all the way through: Wick himself. SDXL made fifty two candidates, and fifty one were "
    "rejected. Green glass, a pile of lanterns, a robot, faces with one eye, and one image that "
    "looked like a famous copyrighted character, rejected on the spot. The fix was to stop asking for pixel art. "
    "Prompt six asks for a flat cartoon, starts from the character sheet pose, and keeps seed ten twelve.",
    {"type": "GRAPHIC", "source": "remotion", "motion": "reveal", "remotion": {"pattern": "GodotDesignBoard", "props": {
        "title": "One asset, design → prompt → raw output", "section": "SOURCES.md asset log · CHAR-REF",
        "excerpt": "P6 (abridged): flat 2D cartoon illustration of a single cute brass lantern creature … a big yellow "
                   "teardrop flame inside the glass, the flame has a cute friendly face … full body, standing, "
                   "three-quarter view facing right, plain white background\nimg2img from the sheet pose · denoise 0.75 · seed 1012",
        "source": "Exact prompts: tools/gen/*.sh and design/generation/gen-log.jsonl · SDXL base 1.0, CreativeML Open RAIL++-M · the copyrighted look-alike is not shown",
        "status": "ROUNDS 1–3 · 51 OF 52 REJECTED · 1012-b1 ACCEPTED BY RUI", "visualLabel": "Character-sheet pose → rejected outputs → the accepted raw image",
        "layout": "image", "image": data_uri("b05-prompt-to-raw.png"),
        "cards": [{"label": "Why rejected", "text": "green background leaked into the glass; one-eyed faces; a robot; near-copies of the SVG"}]}}},
    "Asset trace part 1: character sheet → prompt → raw output, with the rejections."))
beats.append(narrated("B06", "TRACE",
    "Pixelising is where a design decision showed up. Reduced to thirty two by forty, the generated face "
    "dissolved into a smudge, so Rui chose sixty four by eighty and the whole game doubled to match. The face "
    "still did not survive, so it is an edit, not model output: Rui picked oval eyes from three painted patterns. "
    "Body, flame and colours are SDXL. The face is a logged hand edit. And that is the sprite, in the engine.",
    {"type": "GRAPHIC", "source": "remotion", "motion": "reveal", "remotion": {"pattern": "GodotDesignBoard", "props": {
        "title": "Raw output → edits → in engine", "section": "edit-log.jsonl · pixelize.py · face_edit.py · normalize_sprite.py",
        "excerpt": "pixelize: remove white, area-scale, hard alpha, Lab-quantise to 6 colours\nface_edit: clean the flame, paint the chosen face (oval)\nnormalize: feet on the last row, cap centred\nresult: 64×80, 5 colours, Nearest filter",
        "source": "design/generation/* and evidence/captures/state-idle-right.png (engine capture) · every edit logged with input and output hashes",
        "status": "EDITED · FACE IS A HAND EDIT, NOT MODEL OUTPUT", "visualLabel": "Raw → 32×40 vs 64×80 → three faces → accepted sprite → engine",
        "layout": "image", "image": data_uri("b06-raw-to-engine.png"),
        "cards": [{"label": "Decision", "text": "Rui: 64×80 and the oval face. Viewport 1280×720, collider 36×56, tuning ×2"}]}}},
    "Asset trace part 2: edits and the in-engine result."))
beats.append(code_beat("B07", "Nine images, one state each.", "features/player/player.gd", 137, 150,
    [{"at": 2, "line": 138, "label": "an event look (pickup, ember, hurt, celebrate) wins"},
     {"at": 7, "line": 140, "label": "on a ladder: the back-view image"},
     {"at": 11, "line": 143, "label": "rising or falling, read from velocity"},
     {"at": 16, "line": 150, "label": "left is a runtime flip, except the back view"}],
    [{"label": "Images", "value": "9 generated PNGs, 64×80\nfeet on the bottom row"},
     {"label": "Animation", "value": "none: one static image\nper state (allowed)"}],
    "That sprite is swapped, not animated. Update look picks one of nine generated images from the player's "
    "state: climbing, rising, falling, walking. An event look like pickup or hurt wins first. Then it flips the "
    "image when Wick faces left, except on the ladder, because that image is the back view.",
    "Code → result 1: the state-image swap."))
beats.append(capture_beat("B08", "RESULT", "run-01", "pillar jumps and the first ladder",
    "Watch the image change: walking, arms up on the rise, arms out on the fall, then the back view on the ladder.",
    "Game audio retained quietly under narration", "Visible result of B07.", evidence_media=True))
beats.append(code_beat("B09", "Marked first, then announced.", "game/session.gd", 275, 285,
    [{"at": 2, "line": 281, "label": "Wick's 36×56 box touches a 24×24 drop"},
     {"at": 6, "line": 282, "label": "collected BEFORE the signal: one drop, one event"},
     {"at": 11, "line": 283, "label": "+35 oil, capped at 100"},
     {"at": 16, "line": 285, "label": "only now: oil_collected (the pickup sound listens)"}],
    [{"label": "Drops", "value": "6 in level v2\n(Rui: 'oil a bit scarce')"}],
    "Oil is where the rules and the sound meet. When Wick's box touches a drop, the drop is marked collected first, "
    "the oil goes up by thirty five, the pickup image is scheduled, and only then does the session announce it. "
    "Marked first, so one drop can never fire twice.",
    "Code → result 2: oil pickup."))
beats.append(capture_beat("B10", "RESULT", "run-01", "oil pickup on the middle-tunnel platform",
    "There. The flame flares over the cap, the gauge jumps, and the light opens up.",
    "Game audio retained quietly under narration", "Visible result of B09.", evidence_media=True))
beats.append(code_beat("B11", "Sound only listens.", "audio/audio_director.gd", 43, 55,
    [{"at": 2, "line": 43, "label": "jump: the one line where a jump starts"},
     {"at": 6, "line": 44, "label": "pickup, after the drop is marked"},
     {"at": 10, "line": 45, "label": "death: hurt sound + the music dips"},
     {"at": 15, "line": 53, "label": "play and count; nothing writes back"}],
    [{"label": "Buses", "value": "Music (low-pass) · SFX\nN / B mute them separately"},
     {"label": "Jump", "value": "-16 dB, Rui's ears,\nfile unchanged"}],
    "Here is the whole contract for sound. The audio director only listens: jumped, oil collected, died, "
    "completed. Each handler plays one file and counts it. Nothing writes back into the game, so a missing file or "
    "a muted bus changes what you hear, and nothing else.",
    "Code → result 3: sound events."))
beats.append(capture_beat("B12", "RESULT", "run-02", "an early jump into the pit, death, respawn",
    "Too early. The hurt sound, red spikes, back to the lamp post.",
    "Game audio retained quietly under narration", "Visible and audible result of B11.", evidence_media=True))
b13 = {"beat_id": "B13", "act": "SLICE AUDIO", "narration_text": "",
       "role_note": "SLICE AUDIO - the game's own sound with NO narration (assignment requirement). A plain CAPTURE beat whose "
                    "audio_file is this capture's own Movie Maker WAV interval, unprocessed. Not a SOURCE_REPORT.",
       "shot": {"type": "CAPTURE", "source": "screen", "take": "run-01", "moment": "top tunnel to the exit and the end card",
                "label": "SLICE AUDIO — the game's own sound, no narration · scripted-input capture · native 3840x2160 · run-01"}}
beats.append(b13)
beats.append(code_beat("B14", "A playtest, as a constant.", "game/session.gd", 249, 258,
    [{"at": 2, "line": 250, "label": "6 oil per second (was 4)"},
     {"at": 6, "line": 252, "label": "at zero oil the ember starts counting"},
     {"at": 11, "line": 256, "label": "EMBER_LIMIT: 8 s, then Rui cut it to 4"},
     {"at": 16, "line": 258, "label": "a death with its own reason"}],
    [{"label": "Rui, playtest 2", "value": "'the risk is not enough'"},
     {"label": "Before", "value": "zero oil = darkness,\nwalk on forever"}],
    "One cause and effect from a playtest. In version one, zero oil just meant darkness, and Rui could walk on "
    "forever. Rui's note: the risk is not enough. So the ember now counts. At zero, ember time grows every tick, "
    "and at the limit it is a death with its own reason. Eight seconds first, then Rui cut it to four.",
    "Code → result 4: the source change behind the ember burn-out."))
beats.append(capture_beat("B15", "RESULT", "run-03", "no input: the ember shrinks and goes out",
    "No input at all. The ring shrinks, the empty gauge blinks faster, and four seconds later the flame goes out.",
    "Game audio retained quietly under narration", "Visible result of B14.", evidence_media=True))
beats.append(narrated("B16", "PLAYTESTS",
    "Every gameplay change in this slice traces to something Rui said while playing. Coming down the ladder felt "
    "stuck: grab it from the top, climb down faster. The risk is not enough: the ember burns out. Make the map "
    "longer: three tunnels, from Rui's own storyboard. And the jump is too loud, twice: minus sixteen decibels.",
    {"type": "GRAPHIC", "source": "remotion", "motion": "reveal", "remotion": {"pattern": "GodotDesignBoard", "props": {
        "title": "Six playtests, quoted", "section": "TEST-REPORT.md §9 · Rui's words (translated)",
        "excerpt": "\"coming down the ladder feels a bit stuck\"\n\"the risk is not enough\"\n\"make the map more complex, longer\"\n\"the jump is still loud\" · \"a bit too little oil\"\n\"fine when muted; no broken beat\"",
        "source": f"FRICTIONAL.md and TEST-REPORT.md · commits b72a749, 0295499, d195a92, 77d0573 · @ {SHORT}",
        "status": "HUMAN JUDGEMENT · RUI · 6 SESSIONS (ONE FULLY MUTED)", "visualLabel": "What each sentence changed",
        "layout": "flow", "cards": [
            {"label": "Ladder", "text": "Down grabs from the top; descend 1.5× faster"},
            {"label": "Risk", "text": "ember burns out (8 s → 4 s); drain 4 → 6/s"},
            {"label": "Map", "text": "three tunnels from storyboard P1; +2 oil drops"},
            {"label": "Jump", "text": "−8 dB, then −16 dB"}],
        "cues": [{"at": 6, "card": 0}, {"at": 11, "card": 1}, {"at": 15, "card": 2}, {"at": 21, "card": 3}]}}},
    "Inspect-and-revise: Rui's playtest notes and the changes they caused."))
beats.append(code_beat("B17", "Mute must not change the game.", "tests/test_audio.gd", 161, 176,
    [{"at": 2, "line": 162, "label": "warm-up, sound on, everything muted"},
     {"at": 7, "line": 166, "label": "the same real-input route each time"},
     {"at": 12, "line": 172, "label": "every 10 ticks: position, state, deaths, oil"},
     {"at": 17, "line": 176, "label": "the warm-up is discarded (engine start-up ticks)"}],
    [{"label": "Runner", "value": "--fixed-fps 60\nfails on any SCRIPT ERROR"}],
    "Then the tests. This one plays the full route with real physics, once with sound and once with both buses "
    "muted, and demands identical traces every ten ticks: position, state, deaths and oil. If muting ever changed "
    "the game, this fails.",
    "Code → result 5: an automated check."))
beats.append({**narrated("B18", "RESULT",
    "Ninety nine checks, zero failures, and thirty one asset checks. Two honest notes. This runner once printed "
    "zero failures over a script that did not compile, so it now fails on any script error. And a flaky trace "
    "turned out to be the engine, not the sound, fixed by running at a fixed sixty frames.",
    {"type": "STILL", "source": "own", "motion": "hold", "evidence_media": "media/B18.png",
     "label": "Recorded tool output, verbatim (capture/test-output.txt)"},
    "Visible result of B17: actual recorded output, not an invented success line."), "image_file": "assets/b18-test-output.png"})
beats.append(narrated("B19", "VERDICT",
    "The verdict. Shown working: nine generated states, a generated world, four event sounds and a loop, all in "
    "the running slice, readable with sound off. Tested: ninety nine automated checks and six playtests by Rui. "
    "Still uncertain: the music's muffling is subtle, the effects are cut from a music model, and one jump between "
    "two spike strips needs near perfect timing at full speed. Next: a wider gap there and a stronger muffling "
    "curve. SDXL made every image, MusicGen every sound. Rui made the design, the storyboard and every choice. "
    "I wrote the prompts, the tools, the code and the tests.",
    {"type": "GRAPHIC", "source": "remotion", "motion": "reveal", "remotion": {"pattern": "ClaudeVerdictArtifact", "props": {
        "artifactTitle": "Verdict",
        "artifactHeading": f"walker-lamplight-rui-sun @ {SHORT} · shown, tested, still open",
        "artifactLines": [
            "shown working — 9 generated Wick states swapped by state, left by flip; generated wall, tiles, spikes, oil, ladder; 4 event sounds + an 8-bar loop; N/B mute; readable muted.",
            "tested — 99 automated checks (0 failures) + 31 asset checks; 6 playtests by Rui, one fully muted; muted and sound traces identical.",
            "uncertain — oil-to-music muffling is subtle (Rui: 'a little difference'); effects are cuts of MusicGen output; the double-spike gap needs near frame-perfect timing at full speed.",
            "next step — widen that gap and strengthen the muffling curve: the first two changes for the full game.",
            "who made what — SDXL base 1.0: every image · MusicGen medium: every sound · Rui: concept, hand-drawn storyboard, every accept/reject and sound pick, every gameplay change · Claude: prompts, tools, code, tests, this film.",
            f"source shown — commit {SHORT} · build {BUILD[:12]} · Godot 4.7.2.stable · captures are scripted input, not human play."]}}},
    "Verdict: tested, uncertain, next step, contributions, models, source revision."))
beats.append(narrated("B20", "HANDOFF",
    "Your turn. Here is the paste ready prompt. Pick one asset, and before you generate anything, write down the "
    "on screen size it has to read at. Generate, then shrink it to that size, and judge it there, not in the "
    "image folder. If a detail dies, change the size or edit by hand, and log which one it was. Then wire one sound "
    "to one signal, mute it, and prove the game did not notice. Liam, in for Bear.",
    {"type": "GRAPHIC", "source": "remotion", "motion": "type-on", "remotion": {"pattern": "ClaudeComposerAsk", "props": {
        "greeting": "Your turn.", "topic": "WALKER · LAMPLIGHT", "segment": "your turn",
        "command": "Before generating, write the on-screen size this asset must read at. Generate with a local model, reduce "
                   "to that exact size, and judge it there. If a detail dies, change the size or edit by hand, and log which. "
                   "Then wire one sound to the one line where its event happens, mute that bus, and add a test proving the "
                   "game's trace is identical with and without it.",
        "runningText": "reducing to game size; comparing muted and unmuted traces…",
        "output": ["judge art at game size: the 32×40 face died, 64×80 survived",
                   "sound listens, never decides: a muted run must be the same run",
                   "a green test over a script error is not green"],
        "folderLabel": "@NikBearBrown", "modelLabel": "Claude", "effortLabel": "Opus"}}},
    "Your Turn - a paste-ready Walker prompt; Liam signs off here, before the final card."))
beats.append({"beat_id": "B21", "act": "OUTRO", "audio_policy": "silence",
              "audio_policy_note": "Intentional. OUTRO-LOCK.md: the outro card is silent under the jingle; no narration, no game audio.",
              "role_note": "OUTRO LOCK - ClaudeTitleOutro, exact title, @NikBearBrown, slug-seeded mascot/jingle.",
              "narration_text": "", "estimated_duration_s": 7, "actual_duration_s": 7.0,
              "shot": {"type": "GRAPHIC", "source": "remotion", "motion": "reveal",
                       "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG}}}})

# Design-board excerpts must be EXACT text (the component labels them "Exact excerpt"): excerpts.json holds
# verified substrings of the named documents (markdown emphasis removed). Code font sized to fit the panel.
_ex = json.loads((Path(__file__).parent / "excerpts.json").read_text(encoding="utf-8"))
for _b in beats:
    _rem = _b.get("shot", {}).get("remotion") or {}
    if _b["beat_id"] in _ex:
        _rem["props"]["section"] = _ex[_b["beat_id"]]["section"]
        _rem["props"]["excerpt"] = _ex[_b["beat_id"]]["excerpt"]
    if _rem.get("pattern") == "GodotDevWorkbench":
        _code = _rem["props"]["code"].split("
")
        _rem["props"]["codeFontSize"] = 24 if (len(_code) > 14 or max(map(len, _code)) > 100) else 26

# Gate V fixes (2026-10-07): one-line board sources and a compact verdict, so nothing crosses title-safe.
_qc = json.loads((Path(__file__).parent / "qc_fixes.json").read_text(encoding="utf-8"))
for _b in beats:
    _p = (_b.get("shot", {}).get("remotion") or {}).get("props", {})
    if _b["beat_id"] in _qc["source"]:
        _p["source"] = _qc["source"][_b["beat_id"]]
    if _b["beat_id"] == "B19":
        _p["artifactLines"] = _qc["B19_artifactLines"]

sheet = {"metadata": {
    "title": TITLE, "slug": SLUG, "topic": "WALKER · LAMPLIGHT", "kind": "gamedev", "playlist": "Brutalist",
    "brand": "claude-liam", "audience": "CSYE 7270 reviewers and Walker readers", "register": "Teardown",
    "engine": "kokoro", "voice": "am_onyx", "voice_kokoro": "am_onyx", "palette": "claude", "style_preset": "claude",
    "ground": "#FAF9F5", "aspect_ratio": "16:9", "fit": "contain", "captions": False, "channel": "@NikBearBrown",
    "channel_title": "@NikBearBrown", "folderLabel": "@NikBearBrown", "greeting": "Kumusta, Liam",
    "greeting_note": "hello lexicon: Kumusta (Filipino, one word), not used by any reel in this toolkit's youtube/ or examples/.",
    "persona": "Liam (in for Bear)", "presenter": "Liam (in for Bear)", "in_for_bear": True,
    "episode_id": "walker-lamplight-gamedev",
    "note": f"godot-gamedev in walker mode over walker-lamplight-rui-sun (CSYE 7270 Assignment 2). Source commit {REV}, "
            f"build_id {BUILD}, Godot 4.7.2.stable.official.ed1daf0bf. Gameplay beats are native 3840x2160 Godot Movie Maker "
            "output from scripted-input takes (capture/run-01..03.mp4) driven through Input actions; not human play. "
            "B13 carries the game's own audio with no narration; other gameplay beats keep the game audio quietly under narration."},
    "beats": beats}
(REEL / "beat_sheet.json").write_text(json.dumps(sheet, indent=1, ensure_ascii=False), encoding="utf-8")
print(len(beats), "beats ->", REEL / "beat_sheet.json")
