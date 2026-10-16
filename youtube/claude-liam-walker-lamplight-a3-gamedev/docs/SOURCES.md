# SOURCES — media in the A3 film

Source revision shown: `4b4b77fe9602b880e79b8ecd1da4c0d93f6e80bf`, build_id
`b7d1c7d6b3a8c4b70b8716089fd5a01a09afbb0a77ce0ce6034f193cdafd9c9e` (manifest `capture/source-manifest.txt`, 92 files,
same method as A1/A2). SHA-256 of every still's source picture: `assets/sources.json`.

| Media | What it is | Made by | Label in frame |
|---|---|---|---|
| B02 clip | A2 reel `capture/run-01` frames 15–420 + `run-01.wav` at −14 dB | Claude (A2 capture driver, real Input actions) | "A2 slice footage, reused · same game build" |
| B11 clip | `_frames/room-orbit` frames 150–438, native 3840×2160 Movie Maker, isolated copy `F:/7270/capture-build-a3` | Claude (`capture/capture_a3_film.gd`, camera only) | "Godot 4.7.2 · asset room · scripted camera orbit" |
| B05 | `docs/a3/blender-session.png` | **Rui** (screenshot) | "Screenshot by Rui, 2026-10-15" |
| B05 | setup-log text (`F:/7270/a3-setup/setup-log.md`) | Claude's commands, 2026-10-14 | "Claude's run, 2026-10-14 · setup log" |
| B06 | `屏幕截图 2026-10-15 194200.png` (Claude app, the real prompt) | **Rui** | "Screenshot by Rui, 2026-10-15" |
| B06–B09 | MCP `look` images saved by Claude Code (`tool-results/mcp-blender-blob-*.png`) | Claude, through the MCP, from Rui's live Blender | "MCP look capture from Rui's Blender session" |
| B07 | `屏幕截图 2026-10-15 194826.png` (lp_flame Base Color picker) | **Rui** | "Screenshot by Rui, 2026-10-15 (after the edit)" |
| B08 | `godot/assets/env/oil_drop.png` (A2 sprite, ×20 nearest) | SDXL output edited in A2 (A2 SOURCES) | caption under the image |
| B13 | Verbatim lines of `capture/test-output.txt` | recorded tool output | "Headless output · verbatim lines" |
| B14 | `_frames/room-front-before/f00000030.png` (copy with `8d07135`'s oil_drop/pit_prop re-exported) and `_frames/room-front-after/f00000030.png` | Claude (same driver) | "Before · re-rendered from commit 8d07135 sources" / "After" |
| Narration | Kokoro v1.0 ONNX, voice `am_onyx` ("Liam"), local | Brutalist toolkit | — |
| Outro jingle | `logos/bear-brown/bear-brown-3.mp3`, −8 dB; pick = sha256(slug) mod 6 + 1 = 3 | stock @NikBearBrown | — |
| Graphics | Brutalist Remotion components (ClaudeComposerAsk, BrutalistHesitantWriter, GodotDesignBoard, GodotDevWorkbench, ClaudeVerdictArtifact, ClaudeTitleOutro) | toolkit `29ba0e8` | code panels: "Godot editor reconstruction" |

No paid service, no network call, no generated image, mesh or music in this film. Rui did not record video (the
assignment allows screenshots); the hand edit itself has no footage, so B07 shows Rui's screenshot of the result
plus the read-back values.
