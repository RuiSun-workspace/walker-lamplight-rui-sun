# Sources, credits, and asset log

## Started from

| What | Where | Revision | License / terms |
|---|---|---|---|
| walker-jumpman Godot project (`godot/`: player controller, session, HUD, tests) | https://github.com/nikbearbrown/walker-jumpman | `9387542` | Course-provided starter |

## Tools

| Tool | Version | Role | License |
|---|---|---|---|
| Godot Engine | 4.7.2.stable.official.ed1daf0bf (portable, Windows) | Engine | MIT |
| Claude Code (Claude Opus 5.5, `claude-opus-5-5`) | — | Code, plans, prompt drafts, document drafts. **Not** an image or audio generator. | Anthropic terms; Northeastern access |
| Brutalist (course-provided) | `29ba0e8` | Explainer film workflow | Course-provided |

## Generative models

Each model is added here **when it is first used**.

| Model | Exact version | Where it ran | License / terms | First used |
|---|---|---|---|---|
| Stable Diffusion XL base 1.0 (Stability AI) | `sd_xl_base_1.0.safetensors`, SHA-256 `31e35c80fc4829d14f90153f4c74cd59c90b779f6afe05a74cd6120b893f7e5b` | Locally, RTX 3070 Laptop 8 GB, through ComfyUI 0.39.0 (git `7a5dad69`) | CreativeML Open RAIL++-M (use restrictions; no attribution fee; outputs usable) | 2026-10-06, CHAR-REF |
| MusicGen medium (Meta) | Hugging Face `facebook/musicgen-medium` @ `d3bd7b0` | Locally, same GPU, Hugging Face transformers 5.14.1 | **CC-BY-NC 4.0 — non-commercial, attribution required** (fine for coursework) | downloaded 2026-10-06, not used yet |

Runtime: PyTorch 2.11.0+cu128 reused from an existing local conda environment, in a separate venv on
F: (`F:Ǘ02-genenv`); the original environment was not modified.

## Human / AI contributions

FRICTIONAL.md has the dated detail. In summary:

| Who | Contributed |
|---|---|
| **Rui (human)** | Chose the game, tone, hero, ending and rules in the vision intake; **drew the storyboard by hand**; picked the concept and the art style; accepted or rejected every generated image and chose the reference face; **chose every sound and the music loop by listening**; playtested five times and asked for every gameplay revision (ladder descent, ember burn-out 8 s → 4 s, drain 6/s, longer three-tunnel map, jump volume, more oil); decided to keep the SVG character sheet. |
| **Claude (Claude Code, Opus 5.5)** | Wrote the outline, the CONCEPT / CHARACTER-SHEET / CHANGE-BRIEF drafts and the SVG sketches (storyboard v1, character sheet); every prompt and the generation scripts; the post-processing tools (pixelize, face edit, normalise, environment processing, audio cuts and loop); all Godot code, the level layouts and all tests; the asset checks, captures and this documentation. Painted the reference face from Rui's chosen pattern (an edit, not model output). Claude cannot hear, so audio judgements are Rui's. |
| **Stable Diffusion XL base 1.0** | Every generated image: Wick's body and flame in all states, back wall, tiles, spikes, oil drop, ladder (see the asset log for what was kept and edited). |
| **MusicGen medium** | The four sound effects and the music loop (cut and levelled by Claude's tools, chosen by Rui). |
| **Code-drawn (not generated)** | Lamp posts, the exit daylight, the light and darkness, the HUD, the spike flash, the ledge-top rim edit, and the reference face pattern. |

## Asset log

One row per generation that was kept or seriously considered. Rejected outputs are kept as thumbnails in
`design/rejected/`.

Every individual image/clip, with its exact prompt, negative prompt, seed, size and sampler settings, is one
JSON line in [design/generation/gen-log.jsonl](design/generation/gen-log.jsonl), written automatically by
`tools/gen/comfy_generate.py` / `tools/gen/musicgen_generate.py`. Raw outputs live outside the repo in
`F:Ǘ02-gen\gen-raw\<ID>\`; the table below summarises each run and the judgment on it.

Shared SDXL settings unless stated: 1024×1024, 30 steps, CFG 7, `dpmpp_2m` / `karras`, batch 4.

| Asset ID | Model and version | Prompt and settings | Outcome | Edits | Where used |
|---|---|---|---|---|---|
| CHAR-REF | SDXL base 1.0 | Prompt **P1**, txt2img, seed 1001 | **Rejected ×4.** Green background bled into the glass (glass turned green); b1/b2 are many lanterns or a tiled pattern; b3 became a humanoid robot; no flame face in any. | — | `design/rejected/CHAR-REF-round1-contact.png` |
| CHAR-REF | SDXL base 1.0 | Prompt **P2**, txt2img, seed 1002, white background | **Rejected ×4.** Character-sheet and poster layouts with garbled text; human/goblin figures; **b2 closely resembles a well-known copyrighted character (yellow electric mouse with long ears)** — rejected on rights grounds as well as design. | — | contact sheet |
| CHAR-REF | SDXL base 1.0 | P2, **img2img** from `design/generation/init/char-idle-init.png` (character-sheet idle pose, Claude SVG), denoise **0.6**, seed 1003 | **Rejected ×4.** Near-copies of the SVG init; the model added almost nothing, so accepting it would make the "generated" asset Claude's drawing. | — | contact sheet |
| CHAR-REF | SDXL base 1.0 | Prompt **P3**, img2img, denoise **0.75**, seed 1004 | **Rejected ×4.** Real pixel rendering appears, construction kept, but the flame has **one** eye or none (rule 3). | — | contact sheet |
| CHAR-REF | SDXL base 1.0 | P3, img2img, denoise **0.85**, seed 1005 | **Rejected ×4.** b2 the closest so far (pixel shading, handle, cap, face in flame) but one eye, rectangular glass, stray yellow drips; b3 a different object (bottle). | — | contact sheet |
| CHAR-REF | SDXL base 1.0 | Prompt **P4**, img2img, denoise **0.8**, seed 1006 | b0/b2/b3 rejected (no face, or a diamond instead of a flame). **b1 = leading candidate:** two eyes and a smile in a yellow flame, ring handle, cap, slightly tapered glass, arms, legs, pixel style. Problems: a small extra flame on top of the handle (rule 2) and a sly eyebrow expression. | pending Rui's decision | `design/rejected/CHAR-REF-s1006-b1-thumb.png` (thumbnail; rejected by Rui on 2026-10-06 as "a bit ugly") |
| CHAR-REF | SDXL base 1.0 | P4, img2img, denoise 0.8, seed 1007 | **Rejected ×4.** b2 has a face but one eye and a skull-like read; others have no face. | — | contact sheet |

Exact prompts (the negative prompts are in gen-log.jsonl):

- **P1:** "pixel art game sprite of a cute small walking brass lantern character, a lantern with a ring handle on top, tapered dark glass body, a yellow flame inside the glass with two small black eyes as its face, two thin brass legs, two thin brass arms, full body, standing, three-quarter view facing right, simple flat colors, limited palette, clean hard edges, centered, plain solid bright green background"
- **P2:** "pixel art game sprite, a single cute anthropomorphic brass lantern creature, one character only, the lantern has a round ring handle on top, a flat brass cap, a tapered dark glass body with two thin bars, a yellow teardrop flame inside the glass, the flame has two small black dot eyes and is the character's face, two short thin brass stick legs, two thin brass stick arms, full body, standing, three-quarter view facing right, simple flat colors, limited palette, clean hard pixel edges, centered, plain white background"
- **P3:** "pixel art game sprite, 16-bit style, a single cute brass lantern creature, round ring handle on top, flat brass cap, tapered dark glass body, a yellow teardrop flame inside with two small black dot eyes as its face, short thin brass stick legs, thin brass stick arms, full body, standing, three-quarter view facing right, pixel shading on the brass, worn tarnished metal, limited palette, clean hard pixel edges, centered, plain white background"
- **P4:** P3 with "tapered dark glass body narrower at the bottom" and "the flame has a cute face with two round black eyes side by side"; negative adds "one eye, cyclops, dripping".
| CHAR-REF | SDXL base 1.0 | Prompt **P5** (P4 + "highly detailed pixel art, high resolution pixel art sprite with fine small pixels, 128x128 sprite"; negative adds "low resolution, chunky pixels, large pixels, blocky, fire on the handle"), img2img denoise 0.8, seeds 1008 and 1009 | **Rejected ×8** (round 2, after Rui judged 1006-b1 "a bit ugly" and asked for smaller pixel blocks). Asking for finer pixels made the images smoother and vector-like rather than finer-pixelled, and 7 of 8 lost the flame face. | — | `design/rejected/CHAR-REF-round2-contact.png` |
| CHAR-REF | SDXL base 1.0 | P5, img2img denoise **0.9**, seed 1010 | **Rejected ×4.** More freedom gave more pixel texture but no flame face; b2 puts the face on the lantern body (rule 3). | — | contact sheet |
| CHAR-REF | SDXL base 1.0 | **New method (round 3):** prompt **P6** asks for a *flat 2D cartoon illustration* (no "pixel art"); the sprite is made afterwards by `tools/gen/pixelize.py`. P6 txt2img, seed 1011 | **Rejected ×4.** Realistic lantern objects, not a character; grey backgrounds; no faces. | — | `design/rejected/CHAR-REF-round3-contact.png` |
| CHAR-REF | SDXL base 1.0 | P6, img2img from the sheet idle pose, denoise 0.75, seed 1012 | b0/b3 rejected (flame without a proper face). **b1 and b2 = candidates:** cute closed-eye smiling flame faces (b2 with blush), construction matches the sheet. b1: extra small ring on the handle. b2: a smoke wisp above the handle and a stray vertical line in the glass. Both have *closed* happy eyes, not the sheet's dot eyes. | pixelised at 32×40 / 48×60 / 64×80 for review | `design/generation/candidates/round3-pixelized-compare.png` |
| CHAR-REF | SDXL base 1.0 | P6, img2img, denoise 0.85, seed 1013 | **Rejected ×4.** Shinier brass, but: no face (b0); bell-shaped cap (b1); odd mouth (b2); b3 has a big frowning face filling the whole glass, which reads as a face on the body (rule 3). b3 kept in the comparison as the counter-example. | — | contact sheet |

Exact prompt **P6:** "flat 2D cartoon illustration of a single cute brass lantern creature, game character design, bold clean dark outline, flat cel shading with one highlight and one shadow tone, round ring handle on top, flat brass cap, tapered dark glass body narrower at the bottom with two thin cage bars, a big yellow teardrop flame inside the glass, the flame has a cute friendly face with two round black eyes side by side and a small smile, short thin brass stick legs, thin brass stick arms, full body, standing, three-quarter view facing right, simple shapes, centered, plain white background" (negative in gen-log.jsonl; it now *includes* "pixel art, pixelated").
| **CHAR-REF** | SDXL base 1.0 | 1012-b1 (P6, img2img from the sheet idle pose, denoise 0.75, seed 1012, batch index 1) | **Accepted, edited** (Rui, 2026-10-07: chose b1 over b2, then chose face variant 3 "oval" of three). Judged against the sheet: construction (ring handle, flat cap, dark tapered glass, flame inside, brass stick limbs) matches; the generated face did not survive pixelisation, so it was repainted. | `pixelize.py` 64×80, height 66, 6-colour quantise → `face_edit.py --face oval`: removed an extra ring above the handle, cleaned brass specks out of the flame, **replaced the face** with 2×4 oval eyes + 5-px smile (the face is therefore Rui/Claude's edit, not the model's) → `normalize_sprite.py` shift (−6, +5). Every step in `edit-log.jsonl`. | `design/generation/accepted/CHAR-REF.png`; same image is `godot/assets/char/wick_idle.png` (CHAR-IDLE, storyboard P1/P2) |

### Character state poses (round 1, 2026-10-07) — all accepted by Rui

Derived from the CHAR-REF set-up: prompt P6 with the pose sentence swapped
(`tools/gen/poses_round1.sh` has every exact prompt), **seed 1012, denoise 0.75**, img2img from the
character-sheet pose drawn at 1024 px (`design/generation/init/char-<pose>-init.png`). Processed by
`tools/gen/poses_round1_process.sh`: `pixelize.py` (fixed scale 0.07104 = CHAR-REF's, Lab quantise) →
`face_edit.py --auto` (flame clean-up, face pattern) → `normalize_sprite.py` (anchor, trim above handle,
despeckle). All 36 raw outputs: `design/rejected/CHAR-poses-round1-contact.png`.

| Asset ID | Pick | Outcome (judged against CHARACTER-SHEET.md) | Edits | Where used |
|---|---|---|---|---|
| CHAR-WALK | s1012-b3 | **Accepted.** Clear stride, no extra parts; b0–b2 rejected (b0 candle stub in the flame, b1/b2 ring or wisp on the handle). Minor: a few flame pixels outside the flame. | face `oval` | `godot/assets/char/wick_walk.png` (P5) |
| CHAR-JUMP | s1012-b1 | **Accepted.** Arms up, legs tucked. Ring on the handle trimmed. | face `wide` | `godot/assets/char/wick_jump.png` (P3) |
| CHAR-FALL | s1012-b3 | **Accepted with a known flaw:** the flame is narrow and the eyes sit on its right edge. b0 a light bulb, b1 a hanging shape, b2 a crescent above the handle. | face `wide` | `godot/assets/char/wick_fall.png` (P3) |
| CHAR-PICKUP | s1012-b2 | **Accepted.** Big flame through the cap, arm reaching. b3 rejected after pixelising: its strong brass highlights quantised to black. b1 has light rays (rule 5). | face `grin` | `godot/assets/char/wick_pickup.png` (P4) |
| CHAR-EMBER | s1012-b2 | **Accepted.** Small red ember, two cage bars. The face is barely visible at 1×, so the state reads by colour (as predicted on the sheet). | face `lid` | `godot/assets/char/wick_ember.png` (P5) |
| CHAR-HURT | s1014-b1 (round 2) | Round 1 (seed 1012) **rejected ×4**: orange flames quantised to brass. Round 2 prompt asked for "a small deep red flame" (seed 1014); **b1 accepted**, tilted body, red flame. | face `x` | `godot/assets/char/wick_hurt.png` (P6) |
| CHAR-CELEBRATE | s1012-b2 | **Accepted.** Arms high, tall flame. b3 rejected for a grey shadow under the feet. | face `joy` | `godot/assets/char/wick_celebrate.png` (P8) |
| CHAR-CLIMB | s1012-b0 | **Accepted as a stand-in for the back view.** The model drew no back view in 4 tries despite "back view, no face". b0 is front-on with a faceless flame, which is how the back of a glass lantern would look. Not flipped at runtime. | face `none` (flame clean-up only) | `godot/assets/char/wick_climb.png` (P1) |

### Environment round 1 (2026-10-07) — accepted by Rui

txt2img with SDXL base 1.0, 1024×1024 (BG 1344×768), 30 steps, CFG 7, dpmpp_2m/karras, batch 4; exact
prompts in `tools/gen/env_round1.sh` and gen-log.jsonl. Processed by `tools/gen/env_process.py`
(crop, key, area-resize, Lab-quantise to the environment palette in `tools/gen/pixelize.py`). All 28 raw
outputs: `design/rejected/ENV-round1-contact.png`. Composite check: `design/generation/candidates/env-round1-mock.png`.

| Asset ID | Pick | Outcome | Edits | Where used |
|---|---|---|---|---|
| ENV-BG | s2001-b1 | **Accepted, edited.** The only flat back wall; b0/b2/b3 are deep perspective tunnels that fight the side view. | darkened ×0.45 (first mock: brighter and busier than the platforms), 1280×720, quantised | `godot/assets/env/bg_rock.png` |
| ENV-TILE | s2002-b2 | **Accepted, edited.** Regular cold-blue stones. b0 a rock pile on white, b3 warm tan stones (would hurt brass contrast). | central crop, 64×64, quantised | `godot/assets/env/tiles_rock.png` |
| ENV-TILE-TOP | s2003 b0–b3 | **All rejected.** Every output was a whole landscape (waterfall, cliffs, stairs), not a platform edge. | the top edge is a **code edit of ENV-TILE** (rim rows), not model output | `godot/assets/env/tiles_rock_top.png` |
| ENV-SPIKE | s2004-b3 | **Accepted, edited.** Six even spear heads; b0 uneven heights on a white plate, b1/b2 weapons or a falling pattern. | heads cropped, grey keyed, 96×36 (24 px was invisible in the mock) | `godot/assets/env/spikes.png` |
| ENV-OIL | s2005-b3 | **Accepted, edited.** No output was a single drop; the drop hanging on the right of b3 was cropped off its holder. | crop, near-white removed (corner key left a white box), 22×24 | `godot/assets/env/oil_drop.png` |
| ENV-LADDER | s2006-b2 | **Accepted, edited.** A straight front-on run of rungs in the middle of a wooden frame. | crop, 32×32 vertical tile, dark interior → transparent | `godot/assets/env/ladder.png` |
| ENV-LAMPPOST | s2007 b0–b3 | **Not used (pending Rui).** b0 is another lantern (confusable with Wick); b1 reduces to a white smudge; b2/b3 are scenes. | b1 processed to 40×64 for review only | — |

### Sound effects and music (audio round 1, 2026-10-07) — picked by Rui by ear

MusicGen medium (`facebook/musicgen-medium` @ `d3bd7b0`, CC-BY-NC 4.0), local, guidance 3.0, temperature
1.0, top-k 250, fp16; exact prompts and seeds in `tools/gen/audio_round1.json` and gen-log.jsonl.
Edits by `tools/gen/audio_tools.py` (logged in edit-log.jsonl). Waveforms of all 18 raw clips:
`design/rejected/AUDIO-round1-waveforms.png`. Exported files were checked sample-for-sample against
the versions Rui auditioned.

| Asset ID | Pick | Outcome (Rui listened; Claude cannot) | Edits | Where used |
|---|---|---|---|---|
| SFX-JUMP | s3001-b0 | **Accepted** (Rui's pick of 4). | cut from onset, 350 ms, 30 ms fade-out, peak −1 dBFS, OGG q6 | `godot/assets/audio/sfx_jump.ogg` (P3) |
| SFX-PICKUP | s3002-b1 | **Accepted** (Rui's pick of 4). | 600 ms, same chain | `godot/assets/audio/sfx_pickup.ogg` (P4) |
| SFX-HURT | s3003-b0 | **Accepted** (Rui's pick of 4). | 500 ms, same chain | `godot/assets/audio/sfx_hurt.ogg` (P6) |
| SFX-EXIT | s3004-b2 | **Accepted** (Rui's pick of 4). | 2000 ms, same chain | `godot/assets/audio/sfx_exit.ogg` (P8) |
| MUS-LOOP | s3101-b1 | **Accepted.** Rui: seam fine over three repeats. b0 rejected: Rui heard "a slight problem" at its seam. | 8 bars at 90 bpm (measured 90.09) = 21.344 s from 1.899 s, ends on rising zero crossings, seam jump 0.0020 (median step 0.0006), peak −3 dBFS, OGG q6 | `godot/assets/audio/mus_loop.ogg` (P1–P7) |
