# SUBMISSION — CSYE 7270 Assignment 2

**Assignment:** Assignment 2 - Generate Art, Sound, and Music for Your Game

**Student:** Rui Sun (`sun.r3@northeastern.edu`)

**Project name:** `walker-lamplight-rui-sun` (game: *Lamplight*)

**Game concept in one sentence:** You are Wick, a small walking lantern spirit lost in an abandoned mine,
whose flame is both life and the only light: oil drains every second, oil drops refill it, and at zero the
ember lasts four seconds, so you climb through three dark tunnels to the daylight before it goes out.

**GitHub repository URL:** https://github.com/RuiSun-workspace/walker-lamplight-rui-sun

**Started from:** walker-jumpman ([nikbearbrown/walker-jumpman](https://github.com/nikbearbrown/walker-jumpman)
`9387542`). Only its Godot project structure was imported; the game is new.

**Submitted commit SHA:** *the commit that adds this file. A commit cannot contain its own SHA; run
`git rev-parse HEAD` on the pushed `main`, and see the Canvas note.*

**Source revision shown in the film:** `a70758da954068bafc3de1058f9eaebff318b16a`

> The film was captured from `a70758d`. Commits after it add only documentation and the film's build
> scripts and records (`youtube/`, FRICTIONAL, TEST-REPORT, SOURCES, README, this file). **No file under
> `godot/` changed after `a70758d`**:
>
> ```bash
> git diff --stat a70758d..HEAD -- godot/     # expect empty output
> ```

**Godot version and operating system:** Godot `4.7.2.stable.official.ed1daf0bf` (GL Compatibility) on
Windows 11 Home China, RTX 3070 Laptop GPU 8 GB.

**Generative models used (name, version, where run, license):**

| Model | Version | Where run | License | Used for |
| --- | --- | --- | --- | --- |
| Stable Diffusion XL base 1.0 (Stability AI) | `sd_xl_base_1.0.safetensors`, SHA-256 `31e35c80…7e5b` | Locally on the RTX 3070, ComfyUI 0.39.0 | CreativeML Open RAIL++-M | Every generated image: Wick's nine states, back wall, rock tiles, spikes, oil drop, ladder |
| MusicGen medium (Meta) | `facebook/musicgen-medium` @ `d3bd7b0` | Locally on the same GPU, Hugging Face transformers 5.14.1 | CC-BY-NC 4.0 (non-commercial, attribution) | The four sound effects and the music loop |
| Kokoro TTS | `kokoro-v1.0.onnx`, voice `am_onyx` | Locally, Brutalist toolkit | Apache-2.0 | Film narration only |

No paid service was used. Claude Code (Claude Opus 5.5) wrote code, prompts, tools and drafts; it
generated no image or sound. Full asset log, kept and rejected outputs: [SOURCES.md](SOURCES.md).

**Final film URL and filename:**
https://northeastern-my.sharepoint.com/:v:/g/personal/sun_r3_northeastern_edu/IQApLUVOtRgNSa8IJEat3WgqAatgl7QkgIaf07zQCJS8u24?e=Lqm1EB
— `claude-liam-walker-lamplight-gamedev.mp4`

**Final film SHA-256:** `f0ae62846568d6013f68f96b63f891486d3302910da23aca04f36d2bd12c41d7`

*(3840×2160 H.264, 30 fps, AAC 48 kHz stereo, 329.93 s, 64.7 MB. Northeastern OneDrive, link scope
"People in Northeastern University with the link", view-only. MP4 and MP3 are kept out of the repository.)*

---

## Summary of my work

**Designed before generating.** CONCEPT, a hand-drawn STORYBOARD (eight panels, drawn by me on paper),
CHARACTER-SHEET and CHANGE-BRIEF were committed and tagged `design-v1` (`6b5d099`) before any model ran.
Later changes are appended as dated revisions, never rewritten.

**Generated art.** SDXL produced Wick and the environment. Prompts, seeds and every rejection are logged
(51 of 52 character candidates rejected, with reasons and thumbnails in `design/rejected/`). The images
were pixelised to a fixed six-colour palette. Wick has nine states (idle, walk, jump, fall, climb, pickup,
ember, hurt, celebrate) at 64×80, swapped by game state and flipped for facing. The face is a logged hand
edit, not model output.

**Generated sound and music.** MusicGen produced four event sounds (jump, oil pickup, hurt, exit) and an
8-bar loop at 90 bpm. I picked each one by ear. The audio code only listens to game signals: one sound per
event, the music muffles as oil drops, dips on death, pauses and stops at the exit. N and B mute music and
effects separately, and the game is readable muted.

**Playable slice.** Three tunnels with a ladder, spikes, six oil drops, lamp-post checkpoints and a daylight
exit. Darkness and the light ring follow the oil. I playtested six times (once fully muted), and those
sessions caused every gameplay revision: ladder descent, ember burn-out 8 s → 4 s, drain 6/s, the longer
map, the jump volume and more oil.

**Verification.** `tools/run_tests.sh` runs five headless suites (99 checks, 0 failures) and fails on any
script error. `tools/check_assets.py` checks 31 rows (sprite proportions, palette, in-engine contrast, loop
seam): 0 FAIL. Both pass on a fresh clone of the pushed repository.

**Film.** A 4K Brutalist `godot-gamedev` explainer that shows code and then its result in the game. The
gameplay is scripted input through real `Input` actions, labelled as such. One segment plays the game's own
audio with no narration. Every shown code excerpt is verified verbatim against `a70758d`.

## Known limitations

From [TEST-REPORT.md §10](TEST-REPORT.md):

1. The oil-to-music muffling is subtle (my words: "a little difference").
2. The effects are cuts from a music model, not designed one-shots.
3. The jump between the middle tunnel's two spike strips needs near-frame-perfect timing at full speed;
   stopping in the gap works.
4. Climb uses a front view standing in for the back view (the model drew none); the fall image's eyes are
   off-centre; there is no animation.
5. The mirrored back wall repeat is visible; the outdoor exit scene was not generated.
6. The character-sheet drawings are SVG; the storyboard is hand-drawn.
7. One playtester (me). The film's gameplay is scripted input, not human play.
8. Film audio: segment B13 uses the toolkit's per-beat `audio_file` for the game's own sound, not the
   toolkit's source-report mechanism. I am asking the instructor whether that is the intended method.

## Where to look

| Document | What it answers |
| --- | --- |
| [README.md](README.md) | Run instructions, controls (including mute), what the slice shows, the film link |
| [CONCEPT.md](CONCEPT.md) · [STORYBOARD.md](STORYBOARD.md) · [CHARACTER-SHEET.md](CHARACTER-SHEET.md) · [CHANGE-BRIEF.md](CHANGE-BRIEF.md) | The design, committed before generation, with dated revisions |
| [SOURCES.md](SOURCES.md) | Models, licenses, the full asset log, the human/AI split |
| [TEST-REPORT.md](TEST-REPORT.md) | Character and storyboard checks, sound events, muted play, automated results, playtests, limitations |
| [FRICTIONAL.md](FRICTIONAL.md) | What went wrong, what surprised us, what was rejected |
| [youtube/claude-liam-walker-lamplight-gamedev/](youtube/claude-liam-walker-lamplight-gamedev/) | Film beat sheet, prompts, fact-check, shot list, capture hashes, input logs, evidence ledger, QC |

## Verifying this submission

```bash
git clone https://github.com/RuiSun-workspace/walker-lamplight-rui-sun.git
cd walker-lamplight-rui-sun
godot --headless --path godot --import    # first run only: builds the import cache
GODOT=<path to Godot 4.7.2> bash tools/run_tests.sh    # 5 suites, 99 checks, 0 failures
python tools/check_assets.py              # 31 rows, 0 FAIL
godot --path godot                        # play it
git diff --stat a70758d..HEAD -- godot/   # empty: the film shows this exact game source
```
