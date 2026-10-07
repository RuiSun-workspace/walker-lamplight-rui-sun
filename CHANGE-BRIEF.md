# Change brief — Lamplight asset slice (v1, 2026-10-03)

The plan and the predictions, written before any generation; panel numbers refer to the hand-drawn STORYBOARD.md v2. This file is **append-only** after it is
committed: later changes go in the revision log at the bottom, not into the text above it.

Starting point: walker-jumpman `9387542` `godot/`. Its `session.gd` already has the state machine this
slice hangs everything on: `MENU → PLAYING ⇄ PAUSED`, `PLAYING → DYING → PLAYING` (0.55 s), and
`PLAYING → COMPLETE`. Sounds and music **listen** to those transitions; they never drive them.

## 1. Asset list

"Gen" = made by a generative model (local, logged in SOURCES.md). "Code" = drawn or produced in Godot by
code, which does not count toward the generative-model requirement. **Req** = required for the slice to
meet the assignment; **Want** = used if it passes its check; the slice works without it.

### Character (all from one reference, 32×40 px, palette-quantised — see CHARACTER-SHEET.md)

| ID | What | Source | Panels | Priority | Planned path |
|---|---|---|---|---|---|
| CHAR-REF | Reference image every pose is derived from (not shown in game) | Gen | — | Req | `design/generation/char-ref/` |
| CHAR-IDLE | idle | Gen | P1 P2 | Req | `godot/assets/char/wick_idle.png` |
| CHAR-WALK | walk | Gen | P5 | Req | `godot/assets/char/wick_walk.png` |
| CHAR-JUMP | jump, rising | Gen | P3 | Req | `godot/assets/char/wick_jump.png` |
| CHAR-FALL | fall | Gen | P3 | Req | `godot/assets/char/wick_fall.png` |
| CHAR-PICKUP | oil pickup | Gen | P4 | Req | `godot/assets/char/wick_pickup.png` |
| CHAR-EMBER | ember (oil = 0) | Gen | P5 | Req | `godot/assets/char/wick_ember.png` |
| CHAR-HURT | hurt / fail | Gen | P6 | Req | `godot/assets/char/wick_hurt.png` |
| CHAR-CELEBRATE | celebrate | Gen | P8 | Req | `godot/assets/char/wick_celebrate.png` |
| CHAR-RESPAWN | respawn | Gen | P7 | Want | `godot/assets/char/wick_respawn.png` |
| CHAR-LAND | land | Gen | — | Want | `godot/assets/char/wick_land.png` |
| CHAR-BORED | bored | Gen | — | Want | `godot/assets/char/wick_bored.png` |
| CHAR-CLIMB | climb — back view on a ladder | Gen | P1 | Req | `godot/assets/char/wick_climb.png` |

### Environment

| ID | What | Source | Panels | Priority | Planned path |
|---|---|---|---|---|---|
| ENV-BG | Rock back wall, tiles horizontally, 640×360 | Gen | P1–P7 | Req | `godot/assets/env/bg_rock.png` |
| ENV-TILE | Rock ledge tile set (top edge + fill), 16×16 cells | Gen | P2 P3 P5 P7 | Req | `godot/assets/env/tiles_rock.png` |
| ENV-SPIKE | Spike strip, 8 px wide per spike | Gen | P3 P6 | Req | `godot/assets/env/spikes.png` |
| ENV-OIL | Oil drop pickup, ~12×12 | Gen | P2 P4 | Req | `godot/assets/env/oil_drop.png` |
| ENV-LAMPPOST | Checkpoint lamp post, ~16×48 | Gen | P7 | Want | `godot/assets/env/lamppost.png` |
| ENV-LADDER | Wooden ladder segment that tiles vertically, 16 px wide | Gen | P1 | Req | `godot/assets/env/ladder.png` |
| ENV-TIMBER | Pit-prop timber frame (set dressing; not in the hand-drawn panels) | Gen | — | Want | `godot/assets/env/timber.png` |
| ENV-EXIT | Outdoor daylight end scene: open sky, sun, cloud, ground (storyboard v2 P8) | Gen | P1 P8 | Want | `godot/assets/env/exit_light.png` |

### Code-made (not generated)

| ID | What | Panels |
|---|---|---|
| LIGHT | Wick's light: a `PointLight2D` whose texture scale follows oil, over a `CanvasModulate` darkness | all gameplay |
| UI-GAUGE | Oil gauge (flame icon + bar; red outline at 0) | P2 P5 |
| UI-TEXT | Title, pause, end card text and the mute indicators | P1 P8 |
| FX-FLASH | Red flash on the spike that killed you | P6 |

### Sound and music

| ID | What | Source | Panels | Priority | Planned path |
|---|---|---|---|---|---|
| SFX-JUMP | Short, dry, light "hop" with a small metal clink | Gen | P3 | Req | `godot/assets/audio/sfx_jump.ogg` |
| SFX-PICKUP | Bright liquid "gulp" + flame flare, rising | Gen | P4 | Req | `godot/assets/audio/sfx_pickup.ogg` |
| SFX-HURT | Sharp metallic hit + hiss of the flame | Gen | P6 | Req | `godot/assets/audio/sfx_hurt.ogg` |
| SFX-EXIT | Open, airy resolve — wind and a soft chime | Gen | P8 | Req | `godot/assets/audio/sfx_exit.ogg` |
| MUS-LOOP | Tense, steady pulse loop with a warm melodic layer, cut at a bar boundary | Gen | P1–P7 | Req | `godot/assets/audio/mus_loop.ogg` |

## 2. Event-to-sound map

Each sound is played by a small `Audio` node that connects to a **signal emitted at the one line where
the event already happens**. The signal is emitted after the state change, and nothing reads back from
the audio node, so a missing file, a muted bus or a failed load cannot change what happens.

| Sound | Exact game event (existing code) | Why it can only fire once | Double-trigger risk we will test |
|---|---|---|---|
| SFX-JUMP | `player.gd` `_physics_process`, the branch that sets `velocity.y = jump_velocity` and `jumps += 1`. New signal `jumped`. Jumping off a ladder goes through the **same** branch (being on a ladder counts as a jump opportunity), so there is still one emit site. | That branch sets `opportunity_consumed = true`; it cannot run again until Wick is on the floor or grabs a ladder again. Jump uses `is_action_just_pressed`, so holding Space does not repeat. | Holding Space through a landing; mashing Space during coyote time; jump-buffer press just before landing; mashing Space while on a ladder. |
| SFX-PICKUP | New: oil drop `Area2D` overlap, checked in `session.gd` `_physics_process` next to the hazard check. Signal `oil_collected`. | The drop is marked `collected`, hidden and its monitoring disabled **before** the signal is emitted; collected drops are skipped. | Standing on a drop for many frames; touching two drops in one frame (two sounds is correct there — one per drop). |
| SFX-HURT | `session.gd` `resolve_contacts`, `fatal` branch (`PLAYING → DYING`). Signal `died`. Covers spikes and falling out. | The function returns early unless `state == PLAYING`, and the branch leaves `PLAYING`. Spike and fall in the same tick are OR-ed into one `fatal`. | Landing on two spike areas at once; spike + fall in one tick; the starter's phantom-contact case after respawn (`contact_settle_ticks`). |
| SFX-EXIT | `session.gd` `resolve_contacts`, `finished` branch (`PLAYING → COMPLETE`). Signal `completed`. | Same guard: only from `PLAYING`, and the branch leaves it. | Standing inside the exit area for many frames; pressing Enter on the end card (starts a new session, no exit sound). |

Not sounds in this slice (by decision, to keep four clear events): landing, footsteps, climbing, oil
running out, respawn, menu clicks.

## 3. Music behavior

`MUS-LOOP` runs on its own **Music** bus with an `AudioEffectLowPassFilter`; the four sounds run on an
**SFX** bus. Mute keys toggle `AudioServer.set_bus_mute` only.

| Situation | Music does | Implemented as |
|---|---|---|
| Title (MENU) | Plays at full brightness | stream playing, cutoff 20 kHz |
| Playing, oil healthy → low | Same loop, increasingly muffled as oil drops | cutoff follows oil: about 20 kHz at full, ~800 Hz near zero (curve to tune by ear) |
| Ember (oil = 0) | Muffled to mostly the low pulse, slightly quieter | cutoff ~400 Hz, −4 dB |
| Oil pickup | Opens back up over ~0.3 s | cutoff eased toward the new target |
| **Pause** (Esc/P, or window loses focus) | Pauses; resumes from the same position | `stream_paused = true / false` |
| **Failure** (DYING, 0.55 s) | Dips; keeps its position; comes back on respawn | volume ducked −12 dB, restored over 0.3 s in `restart_attempt` |
| **Success / end of slice** (COMPLETE) | Stops and stays stopped on the end card; SFX-EXIT plays alone | `stop()`; Enter starts a new session and the loop from its start |
| Back to menu (M) | Starts again at full brightness | `play()` from the start |

The loop itself must repeat with no click or gap: it is cut at a bar boundary and imported with
`loop = true` in the OGG import settings.

**Controls added by the slice:** `N` = mute / unmute music, `B` = mute / unmute effects (the starter
already uses `M` for menu). Both show a small on-screen indicator.

## 4. Oil rules (needed to wire the light and the music; numbers are first guesses)

- Oil 0–100, drains 4 per second (25 s from full to empty). Oil drop: +35, capped at 100.
- Light radius from about 120 px at full to about 28 px (ember) at zero. **The light never goes fully
  out:** at zero oil a small ring stays around Wick's body (Rui, 2026-10-06), so nearby hazards stay
  faintly readable.
- Lamp post: touching it saves the current oil; respawn restores that saved value (P7).
- These numbers are predictions, to be revised by playtest and recorded in the revision log.

## 4b. Ladder rules (added 2026-10-06 — the ladder from storyboard P1 is in the slice)

- The slice has a lower tunnel and an upper tunnel joined by one ladder.
- Overlapping the ladder and pressing Up (`W` / `↑`) grabs it: gravity off, Up / Down move at about
  90 px/s, `CHAR-CLIMB` shows. Oil keeps draining.
- Leaving the top steps onto the upper floor; pressing Down at the bottom, or Jump at any point, lets go.
- New input actions: `climb_up` (`W`, `↑`), `climb_down` (`S`, `↓`). The walker-jumpman jump tuning
  is unchanged.

## 5. Readable without sound

Every sound event has a visual twin, so muted play loses mood but not information:

| Sound | Visual twin |
|---|---|
| SFX-JUMP | jump pose |
| SFX-PICKUP | pickup pose, light grows, gauge rises |
| SFX-HURT | hurt pose, spike flashes red, existing failure text |
| SFX-EXIT | celebrate pose, end card |
| Music muffling | light radius and gauge |

## 6. Predicted failure cases and how each will be checked

| # | Prediction | How I will check it | Pass condition |
|---|---|---|---|
| F1 | **Generated poses drift from the reference** — body taller or wider, eyes on the brass instead of the flame, a third limb, a different handle. | A script measures each quantised 32×40 sprite: brass bounding box, cap width, feet-to-cap height; plus an overlay of each sprite on `design/character/collision.png`; plus the 8 consistency rules by eye. | Cap 18 ± 1 px, feet-to-cap 27 ± 1 px, rules 1–8 hold. Failing poses are regenerated, not stretched to fit. |
| F2 | **Wick disappears against the lit rock** (brass vs lit rock is only 2.1:1 on the sheet). | In-engine screenshot at full oil standing on the generated tiles; sample the background ring around Wick and compute contrast with the brass frame; look at 1× with eyes. | Brass ≥ 3:1 against the actual pixels around Wick, or a 1 px dark outline is added and logged as an edit. |
| F3 | **A sound fires twice on one event** (held jump, spike+fall same tick, standing in the exit). | Automated test: scripted input sequence that counts each signal and each `AudioStreamPlayer.play()` call per event (rapid presses, held input, two hazards at once, idle inside the exit). | Exactly one sound per event occurrence for all four sounds. |
| F4 | **The music loop clicks or gaps at the seam.** Generated music rarely ends on a bar line. | Cut at a bar boundary from the measured tempo; script checks the sample jump and RMS change across the seam; then I listen to at least three repetitions on headphones. | No audible click in three repeats; seam sample jump within the normal range of neighbouring samples. |
| F5 | **Muting changes the game, or muted play is unreadable** (e.g. ember only "heard" through the music). | Automated: run the same input sequence with both buses muted and unmuted and compare the state trace. Human: play once fully muted. | Identical state traces; I can tell jump, pickup, death, ember and exit apart with sound off. |
| F6 | **"Pixel art" from the model is not on a pixel grid** — soft edges, half-pixels, extra colours, a drawn checkerboard instead of transparency. | Prompt for a solid flat background; downscale with nearest-neighbour to the sprite size; quantise to the six-colour palette; count unique colours; check Godot import filter = Nearest. | ≤ 6 colours + transparency per character sprite; no blur in an in-engine screenshot at 6×. |
| F8 | **The ladder breaks the old movement** — Wick sticks at the top, falls through the upper floor, or a jump off the ladder fires `jumped` twice. | Automated: scripted climb up, climb down, jump off mid-ladder, mash Space on the ladder; count `jumped` and check final positions. Human: climb with keyboard both ways. | Reaches the upper floor every time; one jump sound per jump-off; the walker-jumpman tests still pass. |
| F7 | **The low-pass "muffling" is too subtle to hear** on laptop speakers, so the music state carries no information. | Listen at full / half / zero oil on laptop speakers and headphones. | The three levels are distinguishable by ear; if not, add the −4 dB volume step earlier. |

## 7. What the slice is not

One short stretch — a lower tunnel and an upper tunnel joined by a ladder — not the full mine. No new jump physics (the walker-jumpman tuning is kept). No
animation: each state is one static image swapped in. No voice.

## 8. Revision log

_Append dated entries here after this file is first committed._

- **2026-10-07 — resolution, sprite size and pipeline (follows Rui's choice of CHAR-REF).**
  - Viewport 640×360 → **1280×720**; Wick sprite 32×40 → **64×80**; collider 18×28 → **36×56**.
  - All walker-jumpman tuning in pixels is scaled ×2 so jump feel is unchanged: speed 320,
    acceleration 2560, deceleration 3840, jump velocity −640, gravity 1920, terminal velocity 960 (frame
    counts — coyote 6, buffer 6 — unchanged). Level geometry and the oil light radius (now ~240 → ~56 px)
    scale ×2 too.
  - **F1 check now measures against `design/generation/accepted/CHAR-REF.png`:** cap 30 ± 2,
    feet-to-cap-top 47 ± 2, feet-to-handle-top 56 ± 2 px.
  - **F6 pipeline changed:** SDXL draws a flat illustration (not "pixel art") → `pixelize.py` (remove
    white, scale, hard alpha, 6-colour quantise) → `face_edit.py` (clean flame, paint face pattern) →
    `normalize_sprite.py` (feet / cap anchor). Every step is logged in `design/generation/edit-log.jsonl`.

- **2026-10-07 — ember burn-out and faster drain (Rui's playtest decision).** Section 4 changes: drain
  **6/s** (was 4); at zero oil an **8 s ember limit** — the light ring shrinks 56 → 28 px and the empty
  gauge blinks faster (1.5 → 6 per second) as it runs out, then the failure "Your flame went out" (same
  `died` signal and SFX-HURT as spikes / falls; no spike flash). Any drop resets the timer. Options Rui
  did not choose: glint fading with distance, no glint at all, flickering glint. New checks:
  `ember-ring-shrinks`, `ember-burns-out-after-8s`, `drop-in-time-saves-the-ember`.

- **2026-10-07 — level v2, ember 4 s, quieter jump (Rui's third playtest).** `lamplight_tunnel.json`
  v2 (v1 kept as `lamplight_tunnel_v1_two_tunnels.json`): 3200×1440, three tunnels in storyboard-P1
  order, ladders at x 2836 and 260 (3–6 px clear of the slabs), camera follows y as well and looks
  ahead in the facing direction (smoothed). Ember limit 8 → **4 s**. **SFX-JUMP plays at −8 dB**: Rui
  found it too loud; a mixing decision in `audio_director.gd`, the file is unchanged. Spacing was
  checked against the ×2 physics (213 px jump, 36 px collider). Two placements failed the real-input
  route and were moved: the oil platform sat too close to the double spikes, and a 112 px step equalled
  the maximum rise. The tests now run at `--fixed-fps 60`; without it the number of physics ticks per
  frame varied, which broke the F5 trace comparison by one tick of oil.
- **2026-10-07 — fourth playtest (Rui):** jump still too loud → SFX-JUMP **−16 dB** (was −8). "Oil is a
  bit scarce" → **two more drops** (6 total), placed as rewards on the route: on the pit-B pillar
  (landing the double jump) and on the top tunnel's second step. The real-input route now collects
  all 6 (was 4). Everything else in level v2 was fine for Rui.
