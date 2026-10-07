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

## 2026-10-07 — audio round 1 (MusicGen medium, waiting for Rui's ears)

- **Wanted:** four short event sounds (jump, pickup, hurt, exit) and one tense loop (CONCEPT audio
  direction: steady pulse, "keep going" rather than "panic").
- **Asked:** `tools/gen/audio_round1.json` (MusicGen medium @ `d3bd7b0`, guidance 3, top-k 250): 4
  candidates per sound (2 s; exit 4 s), 2 music clips of 30 s at "90 bpm". Prompts say "no music / no
  melody" for the effects, because MusicGen is a music model.
- **Got (by measurement only, since Claude cannot listen):** every effect clip is a continuous 2-second
  texture, not a one-shot. Only a few have a clear attack at the start (waveforms:
  `design/rejected/AUDIO-round1-waveforms.png`). JUMP-b3 is silence for 0.9 s, then three hits. The
  music came out at 90.09 bpm by autocorrelation, so the prompt's tempo was followed.
- **Claude's edits for listening:** `tools/gen/audio_tools.py`. `sfx` cuts each clip from its onset
  (jump 350 ms, pickup 600 ms, hurt 500 ms, exit 2 s), with a 30 ms fade-out, peak −1 dBFS. `loop`
  cuts 8 bars at 90 bpm (21.33 s), starting on the strongest onset after the first second, both ends on
  rising zero crossings. Seam jump is 0.0016 / 0.0020 against a median sample step of 0.0020 / 0.0006,
  so no sample-level click is expected. Musical continuity across the seam is unknown until a human
  listens.
- **Two of my own bugs, caught:** (1) the first `sfx` pass used −40 dB to find the onset; JUMP-b3's
  noise floor passed that, so its cut was 350 ms of silence. Now −25 dB. (2) the first tempo estimate
  (hop 512) said 89.3 bpm, about 0.2 s of drift over 8 bars; hop 64 gives 90.09.
- **Human / Claude / model:** MusicGen generated; Claude prompted, measured and cut; **Rui listens and
  picks** (listening page `F:\7270\a2-gen\listen\listen.html`, outside the repo).
- **Decided (Rui, by listening):** jump b0, pickup b1, hurt b0, exit b2; music b1. Rui says b1's seam is
  fine over three repeats and **b0 had a slight problem at the seam**. This is the first time the
  numbers and the ear disagreed: b0's seam measured *cleaner* (jump 0.0016 vs its median 0.0020) than
  b1's. The sample check only rules out clicks. It says nothing about whether the music makes sense
  across the cut.
- **Still unresolved:** Rui has not described what each chosen effect sounds like; MusicGen effects
  may sound more "musical" than event-like. To be judged in the running scene (TEST-REPORT).

## 2026-10-07 — slice step 2: level and environment in the engine

- **Built (Claude):** `levels/lamplight_tunnel.json`. Lower tunnel (spawn lamp post, a 56 px teaching
  step, a 140 px spike pit, an 80 px oil ledge) → ladder at x 1792 → upper tunnel (second lamp post, a
  96 px spike strip, a floating oil drop) → code-drawn daylight exit. The sizes come from the ×2 physics:
  rise ~112 px, flat jump ~213 px, so the pit can be cleared but not carelessly.
- **Seen in the first engine screenshots:** the mirrored background copies were missing, because a
  negative rect size does not flip in Godot 4; fixed with a transform. The mirror seam makes a symmetric
  "pillar" in the wall; it reads as part of the mine, so it was left in.
- **Tests:** the inherited full-route test could not pass before climbing exists, so it became
  "lower route reaches the ladder foot with zero deaths" (real inputs only) plus "standing in the exit
  completes". The full route returns in step 3. test_game 26/0, test_keyboard 9/9.
- **Human / Claude / model:** level layout and code are Claude's proposals inside Rui's storyboard;
  Rui has not played it yet.

## 2026-10-07 — slice step 3: Wick's state images and the ladder

- **Built (Claude):** `player.gd` swaps the generated 64×80 image by state (idle / walk / jump / fall
  / climb from movement; hurt / celebrate set by the session on death / exit), flips with facing
  (climb never flips, it is the back view), and climbs ladders: Up grabs, no gravity while climbing,
  stops 6 px above the upper floor, a sideways press steps off at full speed. Jump off a ladder goes
  through the same jump line, so `jumped` still has one emit site.
- **Bugs met on the way (all Claude's):** (1) the ladder-top stop was 1 px above the floor; a slow
  step-off sank into the slab's side, so it is now 6 px with an instant full-speed step. (2) "on the
  ladder" only tolerated 2 px above its top, so at the top Wick let go, fell, re-grabbed and looped;
  the trace showed it and the tolerance is now 10 px. (3) my own test checked the fall image at tick
  17, but the rise lasts ~20 ticks; the test now waits for downward velocity. The assertion itself
  is unchanged.
- **Results:** the full real-input route (lower tunnel → ladder → upper spikes → exit) completes with
  zero deaths again. test_game 26/0, test_keyboard 9/9, new test_wick 15/0 (images 64×80 and anchored,
  looks per state, facing, F8 ladder checks including "one jump sound's worth of jumped per jump-off
  even when mashing Space"). Engine screenshots: `evidence/screens/step3-*.png`.
- **Seen, not fixed yet:** the mirrored background repeat is obvious on the upper level (symmetric
  crates). The darkness in step 4 may hide most of it; to be judged then.

## 2026-10-07 — first human playtest (Rui) → ladder fix

- **Rui played step 3** (Claude launched the game for Rui). Rui's words: facing flip is fine;
  **"coming down from the ladder feels a bit stuck"**.
- **Claude's diagnosis from the code:** (1) the ladder stood 32 px left of the upper floor's edge, so
  from the upper floor there was no way to grab it; you had to walk off the edge and press a direction
  in mid-air, which stops Wick dead in the air; (2) going down was as slow as going up (180 px/s,
  1.5 s for 280 px).
- **Changed:** Down while standing at the ladder top grabs it; climbing down is 1.5× faster
  (270 px/s); the ladder moved next to the edge. The first try (x 1806) put Wick's collider exactly on
  the slab's edge and he got stuck under the slab at y 456. Tests caught it, and the ladder now sits
  3 px clear (x 1803).
- **Checks added:** `down-from-upper-floor` (grab from the top, reach the floor: 61 ticks) and
  `down-faster-than-up`. test_game 26/0, test_wick 17/0, test_keyboard 9/9.
- **Still to confirm by Rui:** whether getting down now feels right.

## 2026-10-07 — slice step 4: oil, light, ember, lamp posts, HUD

- **Built (Claude):** oil drains 4/s; a drop gives +35 (capped at 100), marks itself collected
  *before* emitting `oil_collected`, and shows the pickup image for 0.3 s. Lamp posts save oil and
  which drops are taken; death or R returns to the last post, and drops taken after it come back.
  Darkness is a CanvasModulate. Wick's light follows the oil from 240 px down to a 56 px ring that
  never goes out (Rui's rule). Spikes, oil drops, lamp flames and the exit daylight are drawn
  unshaded, so they stay faintly visible in the dark; the spikes that killed you flash red. The ember
  image shows at zero oil, unless climbing. New HUD: oil gauge (red, blinking outline when empty), run
  timer, retries, controls. Signals for step 5: `oil_collected`, `died`, `respawned`, `completed`,
  `paused_changed`, `run_started`.
- **Caught by tests, fixed:** a real bug. On the tick of a death or exit, the new event-look update
  overwrote hurt / celebrate with the movement image (test_wick went 15→2 failures); the update now
  only runs while still playing. Two of my own test bugs: a check of "starts full" 2 ticks in, after
  drain had begun, now asserts oil = 100 − 4 × elapsed exactly; a `str(100.0)` dictionary key hung the
  run before `quit()`. The respawn-oil check now samples at the respawn signal instead of 6 ticks later.
  Both are stricter than before.
- **Caught by screenshots, fixed:** at ambient 0.09 even full oil hid the ledges ahead (unfair).
  Ambient raised to 0.16. The control hint at the bottom sat on top of the spike pit and moved to the
  top-left. Screens: `evidence/screens/step4-*.png`; files named "staged" had the oil set by the
  capture script, not by play.
- **Results:** test_game 26/0, test_wick 17/0, test_oil 20/0, test_keyboard 9/9.
- **Not yet judged by a human:** whether 4/s drain and 240 → 56 px feel tense but fair.

## 2026-10-07 — second playtest (Rui): "the dark is not risky enough"

- **Rui's observation after playing step 4:** at zero oil the game "can still be played on", and
  "the spikes can be seen in the dark". Rui asked whether this departs from the design's meaning:
  **"the risk is not enough."**
- **Claude's analysis:** a real conflict between two pillars that my implementation settled too far
  toward fairness. "Fair in the dark" made the spike glint visible at any distance, so "Light is life"
  had no cost: oil only changed the mood. Four options were offered (glint fades with distance from
  the light, no glint, flickering glint, ember burns out), plus three drain rates.
- **Decided (Rui):** **the ember burns out after ~8 s at zero oil** (a failure). This changes Rui's own
  2026-10-06 rule "you can keep moving in the dark" into "for a while". Also **drain 6/s**. Claude added
  silent warnings so the rule reads without sound: the ring shrinks 56 → 28 px and the gauge blinks
  faster.
- **Results:** test_oil 23/0 (3 new checks), test_game 26/0, test_wick 17/0, test_keyboard 9/9.
- **Revision records:** appended to CONCEPT.md and CHANGE-BRIEF.md (v1 text untouched).
- **Still unresolved:** whether 8 s is the right length; needs Rui's next playtest.

## 2026-10-07 — slice step 5: sounds and music in the engine

- **Built (Claude):** `audio/audio_director.gd` listens to `jumped`, `oil_collected`, `died` and
  `completed` and plays SFX-JUMP / PICKUP / HURT / EXIT on the SFX bus. MUS-LOOP is imported with
  loop = true (8 bars, 90 bpm) on the Music bus. It plays on the title; a low-pass follows the oil
  (20 kHz full → 800 Hz near empty, exponential); the ember drops it to 400 Hz and −4 dB; it ducks
  −12 dB on death and returns over 0.3 s after respawn; it pauses in place and stops on the end card.
  N mutes music, B mutes effects; the HUD shows MUSIC OFF / EFFECTS OFF.
- **A testing hole found and closed:** a type-inference error in the new script stopped session.gd from
  compiling, yet all three suites still printed "0 failures". `tools/run_tests.sh` now fails a suite on
  any SCRIPT ERROR, a non-zero exit, or zero PASS lines. Earlier step results were checked for script
  errors at the time, so they stand.
- **A flaky check, investigated rather than retried:** F5 (muted run = sound run) failed once and
  passed once. A determinism probe showed the *first* game in a fresh engine process gets 10 physics
  ticks before the route starts, not 3. Runs 2–6 were identical, including two fully muted runs. So
  mute was not the cause. The F5 check now discards a warm-up run; the equality itself is unchanged and
  passed 3/3.
- **Results:** test_audio 23/0 — one sound per jump (5/5 including held and mashed Space), per ladder
  jump-off, per drop, per death (including spike + fall in one tick and a duplicate fatal contact), one
  exit sound with none on replay; music behaviour; mute keys; muted trace = sound trace. All suites:
  26 + 9 + 17 + 23 + 23 checks, 0 failures, 0 script errors.
- **Only a human can check:** whether each sound fits its moment in play, whether the loop seam stays
  clean in the engine, whether the muffling is audible on laptop speakers (F7), and whether the game
  still reads with sound off.

## 2026-10-07 — third playtest (Rui, with sound) → level v2

- **Rui's words:** the jump sound is too loud, make it quieter; "I want the map to be more complex,
  longer, with more things in it"; shorten the ember to four seconds.
- **Claude proposed** building the three-tunnel zig-zag from Rui's own storyboard P1 (the slice had
  only built two of its tunnels) and laid out the contents. Rui's request set the direction, and the
  layout follows Rui's drawing; the details (pit with a pillar, gaps over the spikes below, double strip,
  steps) are Claude's proposals.
- **What broke on the way:** (1) the real-input route died between the double spikes: a platform
  dropped Wick past his take-off point, so it moved right 100 px; (2) a step exactly as high as the
  maximum rise was lowered to 100 px; (3) all tests had v1 coordinates and were moved to v2, and one
  check (spike + fall in one tick) is impossible in the new geometry. It became "spikes + ember
  burn-out in one tick", still two fatal causes and one sound; (4) the F5 muted-vs-sound comparison
  failed again even after the warm-up. The cause: positions were identical, but oil was one 6/s tick
  apart, because a headless run decides from real time how many physics ticks fit in a frame. Fixed at
  the root with `--fixed-fps 60` in `tools/run_tests.sh`; the comparison was not loosened.
- **Results (twice in a row):** test_game 26/0 (full v2 route, zero deaths, ~30 s), test_keyboard 9/9,
  test_wick 17/0, test_oil 24/0, test_audio 23/0. Map: `design/level-v2-overview.png`.
- **Human / Claude / model:** requests and the storyboard route are Rui's; layout details, code and
  tests are Claude's; no new generated assets (v2 reuses the accepted ones).

## 2026-10-07 — fourth playtest (Rui, level v2)

- **Rui's words:** "the jump sound is still loud; everything else is fine; there is a bit too little oil."
- **Changed:** jump to −16 dB (−8 was not enough; the file stays untouched, it is a mix level).
  Rather than lowering the drain again (Rui chose 6/s), there are two more drops, placed where the
  player is already doing something hard: on the pillar in the double-jump pit and on the top step.
  Claude chose the spots. The real-input route now picks up 6 of 6 drops.
- **Results:** all suites 99 checks, 0 failures, 0 script errors.
- **Not yet confirmed by Rui:** whether −16 dB is right.

## 2026-10-07 — step 6: verification and documents

- **Done (Claude):** a fresh `git clone` (no cache) imports and passes every suite. New
  `capture_evidence.gd` records the storyboard moments and each state in real play. Two moments are
  staged and labelled (ember via oil = 0; hurt via placing Wick on spikes). New `check_assets.py`
  covers F1, F2 in-engine, F6 and F4. The comparison sheets are `evidence/states-vs-sheet.png` and
  `evidence/storyboard-vs-slice.png`. TEST-REPORT.md and README written; human/AI table in SOURCES.
- **Surprise worth recording:** the predicted failure F2 (Wick lost against lit rock, 2.1:1 on the
  sheet) did not happen: 4.8–9.6:1 measured on engine captures, because the warm light lifts the brass
  and the generated rock is dark and cold. The prediction was made on flat swatches and did not
  account for lighting.
- **A capture glitch:** the first capture run missed the pickup frame (a GDScript lambda captured a
  counter by value; fixed with a dictionary); a later identical run once still showed 17 files and I
  could not reproduce it; the next full run produced all 18.
- **Still owed by Rui (not invented):** one muted playtest, and the F7 question (is the muffling
  audible on laptop speakers?). The in-engine loop seam has only been judged as part of general play.

## 2026-10-07 — sixth playtest (Rui): muted, then music on

- **Rui's words:** "静音时没问题，音乐有一点区别，没有断拍" (fine when muted; the music has a little
  difference; no broken beat).
- **Recorded as:** F5 human check passed. F7 only just: the muffling is audible but subtle, and the
  device was not stated. The in-engine loop seam is fine. No change was made; the subtle muffling is
  listed as a limitation and as the first audio change for the full game.

## 2026-10-07 — film capture driver: real Input is one tick late

- **Rui approved** (before going to sleep): local runs (Godot capture, ffmpeg, Python, Remotion,
  Kokoro), writing to F:\7270\reels and a capture copy, local commits without pushing, AI narration
  (Liam / Kokoro am_onyx), keep-awake. For the "slice audio, no narration" segment Rui chose "use the
  toolkit's own mechanism and ask the instructor". The compiler takes a per-beat `audio_file`. Claude
  uses it to put the capture's own game audio on that beat, instead of the `clock: source` /
  `preserve` path that the toolkit reserves for fellows' SOURCE_REPORTs (its docs warn against
  labelling gameplay that way). Rui should still ask the instructor.
- **Found while building `capture_film.gd`** (drives the game through `Input.action_press`, as the
  capture contract requires): the same route that passes with the test hooks died between the middle
  tunnel's two spike strips. With real Input, `is_action_just_pressed` is true on the tick *after* the
  press. At full speed that shifted the previous landing about 5 px left, to 9 px from the next strip,
  and the stop-slide carried the collider in. Two changes: the route's take-off mark for that jump moved
  1237 → 1262 so it lands mid-gap, and the film driver settles 8 ticks after a landing before a chained
  jump, as a person would. The tests still pass with the new mark.
- **What it says about the level:** chaining that section at full speed is close to frame-perfect. Rui
  got through it (probably by stopping in the gap). Worth a wider gap in the full game; recorded as a
  limitation.

## 2026-10-07 — building the explainer film: what the toolkit's gates caught

- **A wrong count on screen.** B05's first narration miscounted the character rejections; the script
  now says fifty-two candidates, fifty-one rejected. Caught by re-reading the asset log against the
  script, not by a gate; B05 was re-narrated (21.50 s) and re-rendered.
- **A look-alike in the rejected strip.** The seed-1002 b2 thumbnail (the copyrighted look-alike already
  logged in SOURCES.md) was in the first B05 strip. It is no longer shown; the narration still says one
  rejection was for that reason.
- **Labels were not burned by the compiler.** The final compile does not draw shot labels on gameplay
  beats, so `label_clips.py` burns them into the cut clips once, after `cut_clips.py` (it is not
  idempotent; re-cut first if it must run again).
- **Gate F wanted a SHOTLIST.md**, which had not been written; written from the beat sheet.
- **Gate V refused the first compile.** Two kinds of defect:
  - *Edge-bleed* on every GodotDesignBoard beat (B03–B06, B16). Not our text: the component draws its
    own `@NikBearBrown` handle at 4 % from the bottom, below the title-safe line its own QC enforces.
    Toolkit defect; the local copy now places it at 6.2 % (one-line change in
    `GodotDesignBoard.tsx`, not upstreamed). The board sources were also cut to one line. B19's verdict
    card was too tall (six long lines) and B18's terminal image started inside the left margin; both
    redone (B18 now starts at x 380 of 3840, larger type).
  - *Low contrast* on the gameplay beats (0.23–0.29 < 0.30). The mine is dark on purpose, so the game
    footage was not brightened. Following the Assignment 1 film, each gameplay beat declares
    `contrast_regions` (the HUD and the burned label) with a written reason; on B13 the end card's scrim
    dims the HUD, so only the label is measured there and the card is checked by eye.
- **A race to remember:** `remotion_scenes.py` rewrites `beat_sheet.json` when it stamps provenance, so
  edits made to the sheet while a render runs are lost. The contrast fields had to be applied again.

## 2026-10-07 — film master review (Rui): the outro jingle

- **Claude reported two things:** B13's slice audio is about 10 dB louder than the narration, and B21 was
  silent because the jingle folder OUTRO-LOCK names (`svg/claude/mp3/`) is not in the toolkit.
- **Rui's words:** "一不用改，2配一下吧" (1: no change; 2: add it).
- **Done:** the toolkit does ship stock @NikBearBrown jingles in `logos/bear-brown/` (six files, three
  distinct tunes). OUTRO-LOCK says the jingle is picked by the reel slug, but no picker code exists, so
  the pick is `sha256(slug) mod 6 + 1` = `bear-brown-6.mp3` (9.36 s), at −8 dB so it sits just above
  the narration instead of 11 dB over it. The outro card now runs for the jingle's length (9.37 s), and
  the film is 326.9 s. B13 is unchanged.

## 2026-10-07 — the film said "back view"; it is a stand-in

- **Found by Claude** while writing SUBMISSION.md: B07 and B08 said the ladder image "is the back view".
  TEST-REPORT §3 says otherwise: the model drew no back view in four tries, so a front view with a
  faceless flame stands in for it. The README's limitations say the same. The film contradicted the
  report.
- **Rui chose** to re-narrate and re-render rather than only note it.
- **A second fault, found while fixing the first:** B08's line named the states in the order walk,
  rise, fall, ladder, but on screen the ladder comes second. Spoken "ladder" came after Wick had left
  it. The line now follows the screen. The lead-in was shortened because the clip could not start
  earlier without reusing B10's footage. "The faceless climb image" is now spoken at 2.07–3.90 s while
  the climb is on screen at 2.07–4.12 s.
- **Left as is:** the comment on `player.gd` line 150 still says "climb is the back view". It is the
  source the film shows verbatim, and `godot/` has not changed since `a70758d`. The game treats that
  image as the back view (it is never mirrored); the comment describes the role, not the drawing.
- Film: 329.9 s, SHA-256 `f0ae6284…41d7`. Gate V 0 / 0, loudness −23.4 LUFS.
