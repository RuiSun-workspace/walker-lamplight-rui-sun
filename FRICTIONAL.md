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
