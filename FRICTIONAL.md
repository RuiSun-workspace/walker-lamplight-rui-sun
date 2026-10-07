# Frictional — design log

Dated, in order. Entries are written on the day unless marked **(retrospective)**.
Each entry separates what Rui decided, what Claude proposed or wrote, and what a generative model produced.

## 2026-10-03 — choosing the game and the art style

- **Wanted:** a game I actually want to build this semester, small enough that a playable asset slice
  fits in one 10-day assignment.
- **Asked (Claude, no generative model):** for an outline of Assignment 2, then a visual comparison of
  pixel art vs flat vector, then several game concepts.
- **Got:**
  - A side-by-side mockup of one scene drawn both ways. The mockup is SVG written by Claude; it is a style
    illustration only, not a game asset, and does not count toward the generative-model requirement.
  - Four concepts: A "lamp-carrying miner" side-view platformer, B rooftop-cat stealth, C warehouse
    push-crate robot (grid puzzle), D greenhouse gardener (top-down). Claude recommended A.
- **Decided (Rui):** pixel art; concept A. Started from the walker-jumpman Godot structure
  (commit `9387542`), copying only `godot/`.
- **Claude's stated reasons for recommending A and pixel art** (Claude's argument, recorded so it can be
  checked later): one oil value can drive lamp radius, music density, and failure, which gives a clear
  cause-and-effect chain; side view needs only right-facing art with left flipped at runtime; pixel art
  survives the silhouette test at small size, and quantising every pose to one palette doubles as a
  consistency rule; 640×360 × 6 = 3840×2160 reuses the Assignment 1 capture recipe.
- **My own reasons (Rui):** I choose this scheme mainly because it has some similarities with the previous task 1, and can easily complete all the requirements in the task book.
- **Human / Claude / model:** Rui chose concept and style. Claude wrote the outline, the SVG mockup, the
  four concepts, the repo scaffold, and this entry's draft. No generative model has been run.
- **Still unresolved:** which local image / audio models to use on an RTX 3070 (8 GB); the walker asset
  helpers `rembg_matting.py` and `grid_slice.py` are not in my local Brutalist (`29ba0e8`) or
  walker-jumpman checkouts, so I need the course copy or an equivalent I log myself.

## 2026-10-03 — vision intake for CONCEPT.md

- **Asked (Claude → Rui):** four multiple-choice questions before drafting the concept.
- **Decided (Rui):**
  - Tone: **tense survival escape** (not quiet exploration, not cute adventure).
  - Oil at zero: **the lamp goes out but you can keep moving in the dark** (not instant failure).
    Failure comes from spikes and falls.
  - Main character: **a walking lantern spirit** (not a young miner, not an old miner).
  - Session end: **reach the mine exit and see daylight**.
- **Claude drafted** CONCEPT.md v1 from these answers: the name "Wick", the four pillars, the music
  behavior table, and the slice scope are Claude's proposals awaiting Rui's review.
- **Noted risk (Claude):** a lantern spirit has an unusual body, so a diffusion model may drift between
  poses more than it would for a humanoid. The character sheet's consistency rules need to be strict.
- **Still unresolved:** whether jumping should also cost oil; how fast oil drains (needs playtest).

## 2026-10-03 — storyboard sketches

- **Wanted:** eight moments of play, in order, that fix what each asset has to do, with at least three
  shot sizes and three angles.
- **Asked (Rui → Claude):** draw the storyboard as SVG sketches instead of hand-drawn photos.
- **Got (Claude, no generative model):** `design/storyboard/src/make_storyboard.py`, which draws all
  eight panels from one Wick-drawing function so his construction (lantern body, handle ring, flame
  face, brass limbs) is identical in every panel. PNGs rasterised with headless Chrome.
- **First render problem (Claude caught on review):** in P2, P5 and P7 the spike pit sat under the
  caption strip, so the hazard was half hidden — the opposite of "Fair in the dark". Pit floors raised
  by about 20 px and re-rendered.
- **Design choices made in the sketches (Claude proposed, for Rui to accept or change):** spikes and oil
  drops stay faintly visible outside the light (glint / halo); respawn refills oil only to the
  checkpoint's level; P6's Dutch angle is a design view because the slice camera stays level.
- **Human / Claude / model:** Rui chose SVG sketches. Claude wrote the script, the panel text and the
  asset IDs. No generative model.
- **Still unresolved:** whether the exit's pale edge on the right of every gameplay frame is too strong
  a hint; needs a playtest.

## 2026-10-03 — character sheet

- **Wanted:** a contract precise enough that I can reject a generated pose by measuring it, not by taste.
- **Asked (Rui → Claude):** draw the character sheet in the same SVG style as the storyboard.
- **Got (Claude, no generative model):** `design/character/src/make_character_sheet.py` → turnaround,
  11 poses, 1× silhouette, collision overlay, palette contrast table. Wick's numbers were fitted to the
  18 × 28 collider kept from walker-jumpman, so the jump tuning does not change.
- **Found while checking the sheet (Claude's checks, written down for Rui to verify in the engine):**
  - Silhouette: ember is identical to idle in black. Ember must be told apart by colour and the light
    radius, not by outline.
  - Palette: the brass frame is only 2.1:1 against lit rock (`#6b5a44`) — the colour right around Wick
    inside his own light. Either the generated rock stays darker/bluer there, or the sprite needs a dark
    1 px outline. Not decided yet; it goes into CHANGE-BRIEF as a predicted failure.
  - Collision: arms, handle and the tall flame stand outside the box; the fall pose's feet are 1 px
    below it; the tilted hurt pose leaves it. Recorded as fair or harmless in CHARACTER-SHEET.md.
  - First render had the three-quarter view nearly identical to the front view (only the eyes moved);
    the cage bars now shift toward the facing side too. A label and a caption were cut off and moved.
- **Human / Claude / model:** Rui asked for the SVG approach; Claude drew, measured and wrote the sheet.
  No generative model.
- **Still unresolved:** whether 8 required + 3 optional poses is too many to keep consistent with a
  diffusion model on an 8 GB card.

## 2026-10-03 — change brief (drafted, waiting for Rui's review before commit)

- **Wanted:** the last design document before generation: what assets, which events make which
  sound, what the music does, and what I expect to go wrong.
- **Asked (Rui → Claude):** write CHANGE-BRIEF.md but do not commit it yet.
- **Got (Claude, no generative model):** CHANGE-BRIEF.md v1 draft — 12 character IDs, 7 environment
  IDs, 4 code-made items, 4 sounds + 1 music loop; each sound tied to the exact existing line in
  `player.gd` / `session.gd` where its event already happens; music table for title / oil level /
  ember / pickup / pause / failure / success / menu; seven predicted failures F1–F7 with checks.
- **Choices in the draft that are Claude's proposals, for Rui to accept or change:** mute keys `N`
  (music) and `B` (effects) because `M` is already the menu key; oil numbers (drain 4/s, drop +35,
  light 120 → 28 px) marked as first guesses; landing / footsteps / respawn deliberately have no sound.
- **Human / Claude / model:** Claude drafted; Rui reviews before it is committed.
- **Still unresolved:** _Rui's review notes._

## 2026-10-05 / 2026-10-06 — storyboard redrawn by hand

- **What changed:** on 2026-10-05 Rui reported that the instructor said in class the storyboard must be
  hand-drawn. The Claude-written SVG storyboard (v1, `96abb60`) is kept as `STORYBOARD-v1-svg.md`;
  it is no longer the deliverable.
- **Drawn (Rui, by hand):** first six panels on 2026-10-06. Claude checked them against the assignment
  and found three gaps: no failure panel, no recovery panel, and only two camera angles (high + eye
  level). Rui added **died** (drawn with the ground tilted, a Dutch angle) and **restart** (lamp post) in
  the empty bottom row. Both photos are kept in `design/storyboard/hand/`.
- **Rui's own design changes against v1 (visible in the drawings):** the ending is **outdoors** under
  sun and cloud, not a shaft of light; the route map has a **ladder** between tunnels; the oil pickup
  close-up is at eye level; the oil-empty panel shows **no light at all**.
- **Claude did:** cropped the photo into eight panels and evened out the shadow with `crop_panels.py`
  (lines untouched); wrote STORYBOARD.md v2 from what the drawings show; updated the uncommitted
  CHANGE-BRIEF (ENV-EXIT is now an outdoor scene; timber is not in any panel).
- **Open questions recorded in STORYBOARD.md for Rui:** is "no light" in panel 5 literal, or the tiny
  ember radius from the concept? The ladder is treated as full-game only (no climbing in the slice).
- **Human / Claude / model:** drawings and the design changes are Rui's; crops and text are Claude's.
  No generative model.

## 2026-10-06 — three decisions after the storyboard

- **Decided (Rui):**
  1. The character sheet stays as Claude's SVG drawings (option A). Claude had pointed out the risk: if
     the instructor's "hand-drawn" rule also covers the character sheet, that criterion may lose points.
     Rui accepted the risk.
  2. **The ladder goes into the slice.** Climbing becomes a verb.
  3. When the oil runs out, **a very small ring of light stays around Wick's body**. It is not fully
     dark. (Answer to the panel 5 "no light" question.)
- **Claude did:** added pose 12 "climb" (back view on a ladder) to the sheet script and re-rendered
  `poses.png` / `collision.png`; added CHAR-CLIMB, ENV-LADDER, ladder rules (§4b) and failure case F8 to
  the uncommitted CHANGE-BRIEF; resolved the two open notes in STORYBOARD.md; appended revision logs to
  CONCEPT.md and CHARACTER-SHEET.md without changing their v1 text.
- **Consequence noted by Claude:** climbing is new movement code on top of the walker-jumpman controller,
  so it is the riskiest part of the slice to build (see F8). The four sound events stay the same;
  climbing has no sound.
- **Human / Claude / model:** decisions Rui's; edits Claude's. No generative model.

## 2026-10-06 — local models installed; first character reference attempts (CHAR-REF)

- **Setup:** ComfyUI 0.39.0 + SDXL base 1.0 and MusicGen medium on F:, reusing Rui's existing PyTorch
  2.11 + CUDA 12.8 from a D: conda environment (Rui pointed it out; it saved a 2.7 GB download). Rui
  chose MusicGen only for all audio, so no Hugging Face account or gated license is needed.
- **Wanted:** one reference image of Wick that meets CHARACTER-SHEET.md, so every pose can be derived
  from it.
- **Asked / got (SDXL, 28 images in 7 runs, all in gen-log.jsonl and the asset log):**
  - txt2img with a green background (seed 1001) → green glass, piles of lanterns, a robot. The key
    colour leaked into the design.
  - txt2img with white background (1002) → poster / character-sheet layouts with fake text, and one
    image that looked like a famous copyrighted character. Rejected on rights grounds too; added
    "animal, ears, text" to the negative prompt.
  - img2img from the sheet's idle pose: at denoise 0.6 (1003) the model returned the SVG almost
    unchanged; that would be Claude's drawing, not a generated asset. At 0.75–0.85 (1004–1005) real pixel
    rendering appeared, but the flame face kept coming out with **one** eye. At 0.8 with "two round
    black eyes side by side" (1006–1007) one image, **1006-b1**, has the right face.
- **Judgment so far (Claude's check against the sheet, for Rui to decide):** 1006-b1 passes rules 1,
  3, 4, 5-ish and 7; fails rule 2 because of a small extra flame on top of the handle (removable by hand),
  and its eyebrows read as "sly" rather than neutral.
- **Human / Claude / model:** SDXL made the images; Claude wrote the prompts, the scripts and the
  checks; **Rui decides whether 1006-b1 becomes CHAR-REF.**
- **Still unresolved:** _Rui's decision on 1006-b1._

## 2026-10-06 — CHAR-REF round 2: "make the pixel blocks smaller"

- **Rui's judgment on 1006-b1:** "a bit ugly"; wants smaller pixel blocks. Not accepted.
- **Asked (Claude's prompt P5):** the same img2img set-up with "highly detailed pixel art, fine small
  pixels, 128x128 sprite" and "chunky / large pixels" in the negative; denoise 0.8 (seeds 1008, 1009)
  and 0.9 (1010).
- **Got:** 12 images, none usable. The prompt did not make the pixels finer; it made the images smoother
  and less pixel-like, and the flame face disappeared in almost all of them.
- **What this showed (Claude's analysis):** the block size in the *game* is not set by the generated
  image at all. It is set by the sprite size the image is reduced to. Reducing 1006-b1 to the sheet's
  32 × 40 frame (`design/generation/candidates/sprite-size-demo-1006-b1.png`) turns the face into a
  smudge, so the eyes do not read. At 64 × 80 they do. This is a problem with the character sheet's size
  decision. Prompting will not fix it.
- **Human / Claude / model:** Rui judged and asked; Claude prompted and analysed; SDXL generated.
- **Still unresolved:** _Rui to choose the sprite / viewport size._

## 2026-10-07 — CHAR-REF round 3: new method (illustrate, then pixelise ourselves)

- **Decided (Rui):** change the generation method. SDXL no longer draws pixel art. It draws a flat
  cartoon illustration, and `tools/gen/pixelize.py` (Claude) makes the sprite: remove background, scale
  to the sprite size, hard alpha, quantise to the six sheet colours. Rui has **not** chosen the sprite
  size yet, so every candidate is shown at 32×40, 48×60 and 64×80.
- **Got:** txt2img (1011) produced realistic lantern objects, not a character. img2img at denoise 0.75
  (1012) produced two cute candidates with closed-eye smiling flames. At 0.85 (1013) the brass got
  shinier but the faces went wrong.
- **Bug found in my own tool (Claude):** the first pixelise pass only removed white that touched the
  image border, so the hole inside the handle ring stayed as a pale blob. Fixed to remove all near-white
  pixels; the flame core is pale yellow, not white, so it survives. Logged in the script's docstring.
- **What the pixelised comparison shows:** the lantern body now reads well as clean pixel art at
  every size. The **thin face lines dissolve**: area averaging mixes the 2–3 px dark eye lines with the
  yellow flame, and quantisation then turns them into brass-coloured smudges. Only 1013-b3's huge face
  survives, and that one breaks rule 3.
- **Human / Claude / model:** method choice is Rui's; prompts, pixeliser and analysis are Claude's;
  images are SDXL's.
- **Still unresolved:** _Rui: sprite size, which candidate, and how to keep the face (see options in chat)._

## 2026-10-07 — CHAR-REF accepted (1012-b1, oval face)

- **Decided (Rui):** 1012-b1 over 1012-b2. Asked for the eye and mouth lines to be thicker and the
  shapes nicer, because the face "looks awkward". Then chose **variant 3, oval eyes**, out of three.
- **What Claude did:** wrote `face_edit.py`. It removes the leftover ring pixels above the handle,
  turns the brass specks that pixelisation left inside the flame back into flame, and paints the face
  from fixed pixel patterns in 2 px ink. The first preview put the eye highlight in a corner, which read
  as a frown, and the mouth was too wide. Claude revised both before showing Rui the three variants.
  Claude also wrote `normalize_sprite.py` so every state image shares one anchor (feet on the last row,
  cap centred). Its first version measured the arms as the cap, because the arms are the widest brass
  row. Fixed to use the longest *continuous* brass run.
- **Honest authorship note:** body, flame outline and colours come from SDXL (after quantisation). The
  **face is a hand-specified edit**: Rui chose it, Claude's script painted it. It is not model output.
- **Consequence:** the sprite is 64×80 in a 1280×720 viewport; collider and tuning ×2 (revisions
  appended to CHARACTER-SHEET.md and CHANGE-BRIEF.md). The proportions contract is now the measured
  reference: cap 30, feet-to-cap 47, feet-to-handle 56 px.
- **Next:** derive the other poses from this reference with the same pipeline.

## 2026-10-07 — state poses round 1 (8 states derived from CHAR-REF)

- **Wanted:** the eight required state images (walk, jump, fall, pickup, ember, hurt, celebrate,
  climb), consistent with CHAR-REF.
- **Asked:** `tools/gen/poses_round1.sh`. Same prompt P6, **same seed 1012** and denoise 0.75 as
  CHAR-REF; only the pose sentence and the init image (the sheet pose) change. 32 images.
- **Got:** all 32 share CHAR-REF's look (brass frame, dark glass, flat cel shading). This is the first
  time the model was consistent without a fight. The model did **not** draw a back view for climb, even
  with "back view, no face" (all four are front views). Claude picked one per state for Rui to review:
  walk b3, jump b1, fall b3, pickup b2 (b3's strong brass highlights quantised to black), ember b2,
  celebrate b2, climb b0. climb b0 is a front view with a faceless flame. Through a glass lantern the
  back view would look the same, so it stands in for the back view.
- **Hurt needed a round 2:** the model painted the hurt flame orange (~230,135,55). In Lab that is nearer
  the brass than the sheet's ember red, so the whole flame quantised to brass. Re-prompted for "a small
  deep red flame" (seed 1014); all four then quantised to ember red; picked b1.
- **Bugs in Claude's own pipeline, found by looking at the outputs and fixed one at a time:**
  1. RGB nearest-colour quantising turned shaded brass to glass and orange to brass → switched to Lab.
  2. The cap detector broke when the tall flame cut through the cap (pickup / celebrate): pickup was
     shifted 20 px sideways, then the handle was trimmed off as an "extra above the handle". The cap is
     now a run that is at least 30 % brass.
  3. Generated face lines and shading inside the flame survived as dark specks → hole-fill inside the
     flame, plus a despeckle step (floating bits < 6 px removed, dark specks ≤ 3 px inside flame filled).
  4. One stray pixel at the image edge had stretched CHAR-REF's crop box → opening filter before
     cropping; all poses use CHAR-REF's scale (0.07104) so bodies stay the same size.
- **Known defects Claude can still see:** fall's flame is narrow and the wide eyes sit on its right
  edge; walk has a few flame pixels outside the flame; pickup and celebrate cannot be measured by the
  F1 cap check, because the flame really does cover the cap in those poses.
- **Human / Claude / model:** SDXL drew the bodies; Claude picked candidates, wrote and fixed the tools,
  and painted the faces from patterns; **Rui has not reviewed this set yet.**
- **Decided (Rui, 2026-10-07):** all nine state images accepted as they are, including fall's
  off-centre eyes and climb's faceless front view standing in for the back view. Fall can be revisited
  if it reads badly in the engine.

## 2026-10-07 — environment round 1

- **Wanted:** the tunnel world (back wall, platform tiles, spikes, oil drop, ladder, a lamp post),
  dark and cold so Wick's warm brass stays the brightest mid-tone (CHANGE-BRIEF F2).
- **Asked:** `tools/gen/env_round1.sh`, txt2img in the same flat cartoon style, 7 assets × 4.
- **Got:** usable back walls and stone textures. **Every "rock ledge top" came back as a whole
  landscape** (waterfalls, cliffs). Spikes came back as spears. No single oil drop (a lamp, a bottle, a
  wallpaper of drops). One "lamp post" was simply another lantern, which would be confused with Wick.
- **Claude's picks and edits** (`tools/gen/env_process.py`, logged per step): BG b1 (the only flat wall;
  the others are deep perspective tunnels that fight a side view); TILE b2 (regular blue stones); the top
  edge is a **code edit** of the tile (light rim rows), since no top generation was usable; spike heads
  cropped from b3; the oil drop cropped off the holder in b3; a straight run of rungs cropped from b2 with
  the dark box interior made transparent.
- **First mock (no in-game darkness yet) showed:** the wall was far brighter and busier than the
  platforms and had its own floor; the oil drop kept a white box (corner key failed); spikes at 24 px
  were almost invisible; the lamp post read as a white smudge. Fixes: wall darkened to 45 % before
  quantising, oil keyed by near-white, spikes 36 px tall. Lamp post left out pending Rui.
- **Human / Claude / model:** SDXL drew; Claude picked, cropped, keyed, darkened and composed the mock;
  **Rui has not reviewed yet.**
- **Decided (Rui):** environment round 1 accepted. The lamp post and the outdoor exit scene are still
  open (asked, not answered yet); the slice can run without them.
