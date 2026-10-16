# CAPTURE — A3 explainer

| Field | Value |
| --- | --- |
| Source commit at capture | `4b4b77fe9602b880e79b8ecd1da4c0d93f6e80bf` (working tree clean) |
| `build_id` | `b7d1c7d6b3a8c4b70b8716089fd5a01a09afbb0a77ce0ce6034f193cdafd9c9e` (`capture/source-manifest.txt`, 92 files) |
| Engine | Godot 4.7.2.stable.official.ed1daf0bf, GL Compatibility |
| Isolated copy | `F:/7270/capture-build-a3` = `git archive 4b4b77f godot`, plus a 3840×2160 window override in its `project.godot` |
| Driver | `capture/capture_a3_film.gd` (copied into the copy's `tests/`; moves only the room's camera through fixed keyframes, one step per frame) |

```bash
Godot_v4.7.2-stable_win64_console.exe --path F:/7270/capture-build-a3/godot --disable-vsync --fixed-fps 30 \
  --write-movie REEL/_frames/room-orbit/f.png --script res://tests/capture_a3_film.gd -- --take room-orbit
```

| Take | Frames | Used in |
|---|---|---|
| room-orbit | 600 (20 s): front 0 s → behind 9 s → below 13 s → front 20 s | B11 (frames 150–438) |
| room-front (after) | 60, `capture-build-a3` | B14 (frame 30) |
| room-front (before) | 60, `capture-build-a3-before` = the copy with `oil_drop`/`pit_prop` re-exported from `8d07135`'s `.blend` files by `tools/blender/export_glb.py` | B14 (frame 30) |
| A2 run-01 (reused) | A2 reel `_frames/run-01`, frames 15–420, + `capture/run-01.wav` | B02 |

Movie Maker renders offline, so this is no evidence of real-time frame rate. The room is silent; B11's audio is the
narration alone. The A2 footage is the same 2D game build (`git diff a70758d 4b4b77f -- godot` adds only A3 files
and three `.uid` files).
