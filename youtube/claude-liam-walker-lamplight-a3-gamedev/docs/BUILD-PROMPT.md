# BUILD-PROMPT — how the A3 reel was produced

Local only: no paid service, no API key, no network call.

| Tool | Version | Where |
| --- | --- | --- |
| Godot | 4.7.2.stable.official.ed1daf0bf | `C:/Users/18500/Desktop/7270/godot-4.7.2/` (portable) |
| Blender | 5.1.2 | `F:/7270/blender-5.1.2-windows-x64/` (only for re-exporting the "before" assets) |
| Python | 3.11 venv | `F:/7270/film-env/` |
| ffmpeg | 9.0.1 essentials | `F:/7270/tools/ffmpeg-9.0.1-essentials_build/bin/` |
| Remotion / Kokoro | toolkit `runtime/` | `F:/7270/brutalist.art` (`29ba0e8`), Kokoro v1.0 `am_onyx` |

## Steps

```bash
# 0. isolated 4K copy (repository untouched)
git archive 4b4b77f godot | tar -x -C F:/7270/capture-build-a3   # + window override 3840x2160 in its project.godot
# 1. captures (camera-only driver, capture/capture_a3_film.gd copied into the copy's tests/)
Godot_v4.7.2-stable_win64_console.exe --path F:/7270/capture-build-a3/godot --disable-vsync --fixed-fps 30 \
  --write-movie REEL/_frames/room-orbit/f.png --script res://tests/capture_a3_film.gd -- --take room-orbit
#    "before": F:/7270/capture-build-a3-before = the same copy with oil_drop/pit_prop re-exported from 8d07135's .blend
#    takes room-front (before and after)
# 2. recorded test output -> capture/test-output.txt (check_a3_assets in the copy, check_glb, three deliberate faults
#    in F:/7270/capture-build-a3-neg and -before)
# 3. stills, beat sheet, narration
python make_assets.py
python build_beats.py
python runtime/scripts/generate_audio_kokoro.py REEL
# 4. capture cuts (+ burned labels), durations
python cut_clips.py
# 5. evidence ledger and check
python make_evidence.py
python skills/make/godot-gamedev/scripts/verify_gamedev.py REEL --game <repo>/godot
# 6. graphic scenes (from PowerShell), master
python runtime/scripts/remotion_scenes.py REEL
python runtime/scripts/compile.py REEL --height 2160 --fps 30 --out REEL/exports/landscape
```

## Deviations, and why (the toolkit itself was not edited)

1. `./art …` entry points were not used; their scripts were called directly (the same known `./setup` /
   `./art doctor` guard defect as A1 and A2).
2. Remotion was run from PowerShell (Git Bash's npx cannot find node), as in A2.
3. Stills are full-frame `STILL` beats composed by `make_assets.py` from real files, so Rui's screenshots stay
   readable at 4K; their provenance labels are burned into the image.
4. The code panels show only `godot/` files (the checker's scope). Blender code is shown in the stills as MCP
   output and is kept verbatim in the repository's `tools/blender/build_*.py`.
5. A2's 63 game files are listed as exclusions in `gamedev-evidence.json` with one shared reason: they are the A2
   slice, unchanged by A3, and explained by the A2 film.
