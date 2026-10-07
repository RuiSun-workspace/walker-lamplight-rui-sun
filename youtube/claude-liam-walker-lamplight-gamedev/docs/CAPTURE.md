# CAPTURE — walker-lamplight-rui-sun explainer

## Game under capture

| Field | Value |
| --- | --- |
| Project | `walker-lamplight-rui-sun`, CSYE 7270 Assignment 2, started from [nikbearbrown/walker-jumpman](https://github.com/nikbearbrown/walker-jumpman) `9387542` |
| Source commit at capture | `a70758d` (full hash in `capture/source-commit.txt`); working tree clean at capture |
| `build_id` | `718aeab3e08bc7e2bf1882f21ae7f2f84cebf1fe938c7d31cfd736d85a67c71e` |
| Engine | Godot `4.7.2.stable.official.ed1daf0bf`, GL Compatibility |
| GPU / OS | NVIDIA RTX 3070 Laptop (driver 572.16) / Windows 11 Home China |

`build_id` method (same as Assignment 1): `git ls-files godot` at the capture commit, sorted; one line per file
`<sha256 of file bytes>  <path>`; joined with `\n` plus a trailing newline; SHA-256 of that manifest. The
manifest ships as `capture/source-manifest.txt` (76 files).

## Method

An **isolated copy** (`F:/7270/capture-build-a2`, made with `git archive a70758d godot`) with one change to its
`project.godot`, so the submitted source is untouched:

```
; capture build only: 3x the 1280x720 viewport, an exact integer scale (no resampling)
window/size/window_width_override=3840
window/size/window_height_override=2160
```

```bash
Godot_v4.7.2-stable_win64_console.exe --path F:/7270/capture-build-a2/godot --disable-vsync --fixed-fps 30 \
  --write-movie F:/7270/reels/claude-liam-walker-lamplight-gamedev/_frames/<take>/f.png \
  --script res://tests/capture_film.gd -- --take <take>
ffmpeg -framerate 30 -start_number 0 -i f%08d.png -c:v libx264 -preset slow -crf 15 -pix_fmt yuv420p capture/<take>.mp4
```

Movie Maker writes a PNG per frame and the game's own audio as `f.wav`. This is **offline rendering, not
evidence of real-time frame rate** (the laptop GPU was clocking at ~210 MHz; run-01 took 620 s of wall
clock for 34.2 s of footage).

## Driver: real Input, scripted decisions

`godot/tests/capture_film.gd` instantiates the real game and presses keys only through
`Input.action_press` / `Input.action_release` (Enter through `Input.parse_input_event`). It never sets
position, velocity or the player's test fields during a take. *When* to press is decided by the same
position-driven route the tests use (`tests/route_driver.gd`). Every press and release is logged against
the physics tick in `capture/<take>-inputs.jsonl`, and the driver quits non-zero if the take's expected
result does not happen. **These are scripted-input captures, not human play.**

Found while building it: real Input reaches `is_action_just_pressed` one tick after the press, while the
test hooks have no delay. Chained at full speed, the jump between the middle tunnel's spike strips then
died. The route's take-off mark moved 1237 → 1262, and the driver settles 8 ticks after a landing before
a chained jump, as a person would (FRICTIONAL.md, 2026-10-07).

## Takes

| Take | What happens | Result | Frames | SHA-256 (mp4) |
| --- | --- | --- | --- | --- |
| run-01 | title → Enter → the full route through all three tunnels → exit → 3 s end card | complete, 0 deaths, ticks 2052 | 1027 (34.23 s) | `510471dd…f548` |
| run-02 | title → Enter → hop the step → jump too early at x 715 → lands on the pit spikes → respawn | 1 death (spikes), respawned | 174 (5.80 s) | `43b42edb…000c` |
| run-03 | title → Enter → no input: oil drains, ember, burn-out after 4 s → respawn | 1 death ("Your flame went out") | 699 (23.30 s) | `d6a29878…7b33` |

Full hashes and durations: `capture/hashes.txt`. Game audio: `capture/<take>.wav` (same duration as the video).

## How the film uses them

Each gameplay beat is one contiguous interval of a take at normal speed: no retiming, no splicing, no
freeze-padding. Lengths are narration + 0.4 s, rounded up to whole frames (`cut_clips.py`; windows in
`capture/windows.json`). Narrated gameplay beats keep the game audio at −14 dB under Liam (a logged mix in
`mix/`). **B13 is the game's own audio with no narration**, unprocessed, on a plain capture beat whose
`audio_file` is that interval of the take's WAV. It is not presented as a SOURCE_REPORT.
