# BUILD-PROMPT — how this reel was produced

Local only: no paid service, no API key, no network call (models downloaded earlier).

| Tool | Version | Where |
| --- | --- | --- |
| Godot | 4.7.2.stable.official.ed1daf0bf | `C:/Users/18500/Desktop/7270/godot-4.7.2/` (portable) |
| Python | 3.11 venv | `F:/7270/film-env/` |
| ffmpeg | 9.0.1 essentials | `F:/7270/tools/ffmpeg-9.0.1-essentials_build/bin/` |
| Remotion | toolkit's `runtime/remotion` | `F:/7270/brutalist.art` (`29ba0e8`) |
| Kokoro | v1.0 ONNX, `am_onyx` | `F:/7270/brutalist.art/runtime/models/kokoro/` |

## Steps

```bash
# 1. capture (isolated copy, see CAPTURE.md)
Godot_v4.7.2-stable_win64_console.exe --path F:/7270/capture-build-a2/godot --disable-vsync --fixed-fps 30 \
  --write-movie REEL/_frames/<take>/f.png --script res://tests/capture_film.gd -- --take <take>
# 2. beat sheet, narration
python youtube/claude-liam-walker-lamplight-gamedev/build_beats.py
python runtime/scripts/generate_audio_kokoro.py REEL
# 3. graphic scenes (from PowerShell, see deviation 2)
python runtime/scripts/remotion_scenes.py REEL
# 4. gameplay cuts, durations, game-audio mixes
python youtube/claude-liam-walker-lamplight-gamedev/cut_clips.py
# 5. evidence ledger and check
python youtube/claude-liam-walker-lamplight-gamedev/make_evidence.py
python skills/make/godot-gamedev/scripts/verify_gamedev.py REEL --game <repo>/godot
# 6. master
python runtime/scripts/compile.py REEL --height 2160 --fps 30 --out REEL/exports/landscape
```

## Deviations, and why (the toolkit itself was not edited)

1. `./art …` entry points were not used; the scripts they dispatch to were called directly (same known
   defects as Assignment 1: `./setup`/`./art doctor` guard, recorded in A1's BUILD-PROMPT).
2. **Remotion from Git Bash failed** ("'node' is not recognized" inside npx's nested cmd.exe even though
   node.exe is on PATH). Rendering from PowerShell with the same PATH works; `remotion_scenes.py` was run from
   PowerShell. The script's own error handler then crashed on `r.stderr` being `None`, which hid the cause.
3. **Game audio without narration (B13)** uses an ordinary capture beat whose per-beat `audio_file` is the
   take's own WAV interval (a supported compiler input), not the `clock: source` / `preserve` path that the
   toolkit reserves for fellows' SOURCE_REPORT beats. Rui approved "use the toolkit's mechanism and ask the
   instructor"; the instructor has not been asked yet at render time.
4. Narrated gameplay beats keep the game audio at −14 dB under the narration (mix files in `mix/`), the
   capture reference's "retain it quietly under narration" option, decided explicitly.
5. Design-board excerpts were rewritten to exact document text after a pilot showed the component labels
   its left panel "Exact excerpt" (FACTCHECK note).
