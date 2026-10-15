# Test report — Assignment 3, three 3D assets

Versions: **Blender 5.1.2** (build 2026-05-19, portable, Windows 11), **Godot 4.7.2**
(`4.7.2.stable.official.ed1daf0bf`), **mcp-for-blender 2.1.9** (add-on 1.8, protocol 13).
Spec: [CHANGE-BRIEF.md](CHANGE-BRIEF.md) (`9579486`, tag `a3-brief`) plus its §9 revisions.

Status: **in progress.** lamp_post and oil_drop are built and checked in Blender. pit_prop is not built
yet. Nothing has been exported or checked in Godot. Empty cells mean not measured yet, not passed.

## 1. Interface notes

The six parts are in Rui's own words in [BLENDER-NOTES.md](BLENDER-NOTES.md), with Rui's own screenshot
`blender-session.png` (`1e9bbb8`). Claude checked the notes against the screenshot (facts only). The first
screenshot disagreed with two statements, so Rui retook it. See FRICTIONAL, 2026-10-15.

## 2. Size — Blender vs brief vs Godot

Blender numbers are read from the mesh's vertex coordinates after Apply, because `get_scene_info` and the
sidebar round. Godot numbers come from the headless check (not written yet).

| Asset | Brief W × D × H (m) | Blender W × D × H (m) | Godot AABB X × Y × Z (m) | Result |
|---|---|---|---|---|
| lamp_post | 0.19375 × 0.0955 × 0.725 | **0.19375 × 0.0955 × 0.725** | | Blender matches; Godot pending |
| oil_drop | 0.1375 × 0.1375 × 0.15 | **0.1375 × 0.1375 × 0.15** | | Blender matches; Godot pending |
| pit_prop | 1.2 × 0.16 × 2.0 | | | not built |

## 3. Upright and scale

| Asset | Blender rotation / scale after Apply | Godot node scale | Stands upright in Godot |
|---|---|---|---|
| lamp_post | (0, 0, 0) / (1, 1, 1) | | |
| oil_drop | (0, 0, 0) / (1, 1, 1) | | |

## 4. Origin

| Asset | Brief origin | Blender | Sits on the Godot floor |
|---|---|---|---|
| lamp_post | foot of the post; X range −0.03125 … 0.1625 | origin (0, 0, 0); z min 0.000000; X −0.03125 … 0.1625; `get_scene_info` "on ground" | |
| oil_drop | centre of the underside | origin (0, 0, 0); z min 0.000000; X/Y −0.06875 … 0.06875; "on ground" | |

## 5. Triangle count

| Asset | Budget | Blender | Godot |
|---|---|---|---|
| lamp_post | ≤ 72 | **60** (30 quads, counted from the mesh by code) | |
| oil_drop | ≤ 120 | **64** (24 quads + 16 tris; was 94 before the weld, 118 with the rejected highlight) | |

*Rui to confirm in Blender's status bar (right-click → Scene Statistics).*

## 6. Imports and appears in the 3D scene

Not yet.

## 7. HUMAN CHECK — look

| Asset | When | Rui's observation |
|---|---|---|
| lamp_post (Blender viewport) | 2026-10-15, after steps 1–5 | Rui looked and changed the flame's colour: "我认为灯芯之前的颜色有点暗，所以换了一个更明亮的颜色" ("I thought the flame's previous colour was a little dark, so I changed it to a brighter one"). |
| lamp_post (Godot, from all sides, beside the Wick stand-in) | | |
| oil_drop (Blender, Material Preview) | 2026-10-15, after steps 1–2 | Rui chose smooth shading and to try a highlight ball. |
| oil_drop (Blender, with highlight) | 2026-10-15 | "感觉高光球有点丑，不要了吧" ("the highlight ball looks a bit ugly, drop it") — removed. |
| oil_drop (Godot, from all sides, beside the Wick stand-in) | | |

## 8. Hand edit in Blender

| Asset | Part | Before | After | By | Note |
|---|---|---|---|---|---|
| lamp_post | flame (`lp_flame` Base Color) | `#ffcf5a` | `#fdffa6` | Rui, by hand | intended; brief §9 |
| lamp_post | window (`lp_glass` Base Color) | `#241f2c` | `#241c54` → back to `#241f2c` | changed by accident during the hand edit; reverted by Claude's code at Rui's request | caught by reading the edit back |

## 9. Inspect-and-revise cycles

1. **lamp_post colours (2026-10-15).** Observation: Rui found the flame too dark in the viewport. Revision:
   the flame became `#fdffa6`. Inspection: Claude read every material back, found an unintended window
   change and reverted it. The saved file was re-opened headless to confirm the final colours.
2. **oil_drop shape and shading (2026-10-15).** Observation (Claude, from the sprite): a literal round
   sphere would read as a ball, so Rui approved a squashed sphere plus a tangent cone. Observation (Rui,
   viewport): try smooth shading and a highlight. Revision: smooth on, highlight added. Observation (Rui):
   the highlight looked ugly, so it was removed. Observation (Claude, look images): a seam line where the
   cone met the body. Revision (Rui approved): welded, 64 triangles. Inspection: the look images show no
   seam; 0 boundary edges, normals outward.

## 10. What Claude got wrong

- **A wrong scale reference before the brief.** Claude proposed a "miner's lantern" and a 1.75 m miner,
  from a wrong memory note. The A2 hero is Wick, a lantern. Claude caught it by reading `CHARACTER-SHEET.md`
  before the brief was written.
- **A check that printed stale numbers.** Step 1 printed `dims (1.0, 1.0, 1.0)` for a part that was
  already 0.0625 × 0.0625 × 0.70. The scene had not been refreshed. `get_scene_info` showed the truth.

## 11. Predicted failures (brief §7) — what actually happened so far

| # | Prediction | lamp_post so far |
|---|---|---|
| F1 | lying on its side | not testable until Godot |
| F2 | ×10 / ×100 size | lamp_post and oil_drop: did not happen in Blender (exact match); the 22.5° vertex-start width error checked on oil_drop, did not happen |
| F3 | origin in the middle | did not happen (z min 0); the default cube showed the failure before we started |
| F4 | scale/rotation not applied | parts were built with unapplied scale on purpose; step 6 applied all transforms (scale 1, rotation 0) |
| F5 | more detail than asked | did not happen: lamp_post 60 / 72, oil_drop 64 / 120 |
| F6 | colour lost at export | not testable until Godot; the colours are on Base Color, which glTF exports |
| F7 | missing faces / flipped normals | lamp_post: 0 inward-facing faces, closed bottom; oil_drop: 0 inward, positive volume, 0 boundary edges after the weld. Godot look pending |
| F8 | MCP drops mid-build | did not happen: every call returned |
| F9 | 6 cm post too thin at game size | Godot look pending |
