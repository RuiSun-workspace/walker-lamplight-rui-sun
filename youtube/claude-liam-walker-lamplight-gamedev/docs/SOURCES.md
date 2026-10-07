# SOURCES — film

| Material | Source | Revision / hash | Terms |
| --- | --- | --- | --- |
| Game source, code excerpts | `walker-lamplight-rui-sun/godot` | commit `a70758d`, build `718aeab3…71e` | the student's project; starter credit: nikbearbrown/walker-jumpman `9387542` |
| Gameplay footage + game audio | Godot 4.7.2 Movie Maker, scripted Input (`capture/run-01..03.mp4/.wav`) | `capture/hashes.txt` | own capture |
| Wick sprites, environment art | Stable Diffusion XL base 1.0, local ComfyUI 0.39.0 | per-asset rows in the project's SOURCES.md | CreativeML Open RAIL++-M |
| Sound effects, music loop | MusicGen medium (`facebook/musicgen-medium` @ `d3bd7b0`), local | project SOURCES.md | CC-BY-NC 4.0 (non-commercial, attribution) |
| Storyboard panels (B04 image) | Rui's hand drawing, photographed 2026-10-06, cropped by `design/storyboard/hand/crop_panels.py` | repo files | the student's own |
| Asset-trace strips (B05, B06 images) | composed by Claude from repo files and raw generations (`assets/b05-*.png`, `b06-*.png`) | this reel | 1002-b2 (a look-alike of a copyrighted character) deliberately not shown |
| Test output (B18) | verbatim stdout of `bash tools/run_tests.sh` and `python tools/check_assets.py`, 2026-10-07 (`capture/test-output.txt`) | `assets/b18-test-output.png` | own |
| Narration | Kokoro v1.0 ONNX, voice `am_onyx` (Liam, in for Bear), local | `mp3/` | toolkit-provided local model |
| Scenes, outro | Brutalist (course-provided) Remotion components: ClaudeComposerAsk, BrutalistHesitantWriter, GodotDesignBoard, GodotDevWorkbench, ClaudeVerdictArtifact, ClaudeTitleOutro | brutalist.art `29ba0e8` | course-provided |
| Outro jingle | `logos/bear-brown/bear-brown-6.mp3`, stock @NikBearBrown jingle; picked by sha256(slug) mod 6 + 1 = 6; −8 dB, otherwise unchanged (`mix/B21-jingle.wav`) | brutalist.art `29ba0e8` | course-provided |

No paid service, API key or network call was used to make this film (models were downloaded once earlier).
