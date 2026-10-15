# Test report — Assignment 3, three 3D assets

Versions: **Blender 5.1.2** (build 2026-05-19, portable, Windows 11), **Godot 4.7.2**
(`4.7.2.stable.official.ed1daf0bf`), **mcp-for-blender 2.1.9** (add-on 1.8, protocol 13).
Spec: [CHANGE-BRIEF.md](CHANGE-BRIEF.md) (`9579486`, tag `a3-brief`) plus its §9 revisions.

Status: **in progress.** All three assets are built, exported and checked in Blender and Godot, and revised once
after Rui's human check (§9, cycle 4). Empty cells mean not measured yet, not passed.

Commands (Windows; Git Bash provides `timeout`):

```bash
for a in lamp_post oil_drop pit_prop; do blender -b blender/$a.blend --factory-startup --python-exit-code 1 --python tools/blender/export_glb.py -- godot/assets/models/$a.glb; done
python tools/check_glb.py
Godot_v4.7.2-stable_win64_console.exe --headless --path godot --import
timeout 120 Godot_v4.7.2-stable_win64_console.exe --headless --path godot --script res://tests/check_a3_assets.gd --fixed-fps 60
bash tools/run_tests.sh
```

## 1. Interface notes

The six parts are in Rui's own words in [BLENDER-NOTES.md](BLENDER-NOTES.md), with Rui's own screenshot
`blender-session.png` (`1e9bbb8`). Claude checked the notes against the screenshot (facts only). The first
screenshot disagreed with two statements, so Rui retook it. See FRICTIONAL, 2026-10-15.

## 2. Size — Blender vs brief vs Godot

Blender numbers are read from the mesh's vertex coordinates after Apply, because `get_scene_info` and the
sidebar round. Godot numbers come from `check_a3_assets.gd` (AABB of the imported meshes, Godot axes X × Y × Z,
so height is the middle number). Rows show the **revised** sizes; the originals are in brackets.

| Asset | Brief W × D × H (m) | Blender W × D × H (m) | Godot AABB X × Y × Z (m) | Result |
|---|---|---|---|---|
| lamp_post | 0.19375 × 0.0955 × 0.725 | **0.19375 × 0.0955 × 0.725** | **0.19375 × 0.725 × 0.0955** | match (±1 mm) |
| oil_drop | 0.275 × 0.275 × 0.30 (×2, brief §9; was 0.1375 × 0.1375 × 0.15) | **0.275 × 0.275 × 0.3** (was 0.1375 × 0.1375 × 0.15) | **0.275 × 0.3 × 0.275** (was 0.1375 × 0.15 × 0.1375) | match (±1 mm) |
| pit_prop | 0.8 × 0.12 × 2.0 (brief §9; was 1.2 × 0.16 × 2.0) | **0.8 × 0.12 × 2.0** (was 1.2 × 0.16 × 2.0) | **0.8 × 2.0 × 0.12** (was 1.2 × 2.0 × 0.16) | match (±1 mm) |

## 3. Upright and scale

| Asset | Blender rotation / scale after Apply | Godot node scale | Stands upright in Godot |
|---|---|---|---|
| lamp_post | (0, 0, 0) / (1, 1, 1) | 1, 1, 1 on every node; rotation 0 | yes — tallest axis Y |
| oil_drop | (0, 0, 0) / (1, 1, 1) | 1, 1, 1 on every node; rotation 0 | yes (by the size match; its X and Y differ by 25 mm) |
| pit_prop | (0, 0, 0) / (1, 1, 1) — the braces' ±45° rotation was baked in by Apply | 1, 1, 1 on every node; rotation 0 | yes — tallest axis Y |

## 4. Origin

| Asset | Brief origin | Blender | Sits on the Godot floor |
|---|---|---|---|
| lamp_post | foot of the post; X range −0.03125 … 0.1625 | origin (0, 0, 0); z min 0.000000; X −0.03125 … 0.1625; `get_scene_info` "on ground" | yes — `rests_on_floor`: min Y 0.0 vs Floor node top 0.0, gap 0 |
| oil_drop | centre of the underside | origin (0, 0, 0); z min 0.000000; X/Y −0.1375 … 0.1375 after ×2 (was ±0.06875); "on ground" | yes — gap 0 |
| pit_prop | centre of the underside, midway between the posts | origin (0, 0, 0); z min 0.000000; X −0.4 … 0.4 after revision (was ±0.6); "on ground" | yes — gap 0 |

## 5. Triangle count

| Asset | Budget | Blender | Godot |
|---|---|---|---|
| lamp_post | ≤ 72 | **60** (30 quads, counted from the mesh by code) | 60 |
| oil_drop | ≤ 120 | **64** (24 quads + 16 tris; was 94 before the weld, 118 with the rejected highlight) | 64 |
| pit_prop | ≤ 60 | **60** (30 quads: 3 timbers + 2 braces; unchanged by the revision) | 60 |

*Rui to confirm in Blender's status bar (right-click → Scene Statistics).*

## 6. Imports and appears in the 3D scene

- `godot --headless --path godot --import`: no error or warning. `.glb.import` files use Godot's defaults (root scale 1.0, LODs generated; the triangle counts above are the base mesh).
- `godot/game3d/asset_room.tscn`: Floor (4 × 2 m, `#2a2e3d`), one DirectionalLight3D ("Sun") + WorldEnvironment ambient 0.35 (not a light node), one Camera3D with orbit controls, the three assets and a labelled Wick stand-in box (0.225 × 0.35 × 0.225 m, not an asset). `room.one_light`, `room.one_camera`, `room.has_floor` pass.
- Colours in Godot (albedo, from the check): lamp_post `5a412a / b8863b / 241f2c / fdffa6`, oil_drop `f2a93b`, pit_prop `5a412a / 3b2a1c`. All match the brief and §9.
- Independent file check `tools/check_glb.py` (reads the .glb's own JSON): 18/0. Nodes carry no transform; Y-up bounds as above.
- Claude's scripted screenshots: `evidence/room_*.png` (front, back, below, three close-ups). They show that the scene renders; they are not the human check.
- **What these checks do not show:** that the assets look right. On screen the colours render lighter and more saturated than their hex values under this light (the oil drop reads lemon-yellow); the numbers only prove the stored albedo.

### Checks proven able to fail

| Deliberate fault | Check | Result |
|---|---|---|
| pit_prop exported with +Y Up off | `check_glb.py` | 3 FAIL (size, bounds, base) |
| oil_drop lifted 0.05 m in a copy of the room | `check_a3_assets.gd` `rests_on_floor` | FAIL, gap 0.05 |
| stale .glb files after the size revision | `check_glb.py` | 4 FAIL until re-exported |

## 7. HUMAN CHECK — look

| Asset | When | Rui's observation |
|---|---|---|
| lamp_post (Blender viewport) | 2026-10-15, after steps 1–5 | Rui looked and changed the flame's colour: "我认为灯芯之前的颜色有点暗，所以换了一个更明亮的颜色" ("I thought the flame's previous colour was a little dark, so I changed it to a brighter one"). |
| asset room (Godot, Rui orbiting the camera) | 2026-10-15, first look | "我检查完了，出现在游戏中的油滴不可能这么小，我感觉木架有点偏大" ("I've checked it: the oil drop in the game can't be this small, and I feel the frame is a bit too big") → revision cycle 4. |
| asset room after the revision (Godot, Rui orbiting the camera) | 2026-10-15, second look | "看完了，没问题了" ("I've looked, no problems now"). Rui accepted the revised sizes. Rui made no separate comment on the brighter on-screen colours or on the 6 cm post (F9). |
| oil_drop (Blender, Material Preview) | 2026-10-15, after steps 1–2 | Rui chose smooth shading and to try a highlight ball. |
| oil_drop (Blender, with highlight) | 2026-10-15 | "感觉高光球有点丑，不要了吧" ("the highlight ball looks a bit ugly, drop it") — removed. |
| pit_prop (Blender, Material Preview) | 2026-10-15, after steps 1–3 | Rui: "加两根斜撑试试" ("try adding two braces"), then "斜撑可以" ("the braces are fine"). |

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
3. **pit_prop braces (2026-10-15).** Observation (Claude's look): the plain frame could read as a door frame.
   Revision (Rui's choice): two 45° corner braces, 60 triangles. Inspection: look images show the braces
   meeting post and beam with no gap; Rui accepted them.
4. **Sizes after the human check in Godot (2026-10-15).** Observation (Rui): the oil drop is too small, the frame a
   bit too big. Inspection (Claude): the drop's 0.15 m was exactly the 160 px = 1 m conversion; the numbers were
   right and the look was not. Revision (Rui's choice, Claude via MCP): oil_drop ×2 (0.275 × 0.275 × 0.3 m);
   pit_prop 0.8 m wide with 0.12 m timbers, still 2.0 m high. Check: re-exported; the stale files had failed the
   new expectations; after re-export check_glb 18/0, check_a3_assets 30/0, suite green. Rui's look at the revised
   room: "看完了，没问题了" ("I've looked, no problems now").

## 10. What Claude got wrong

- **A wrong scale reference before the brief.** Claude proposed a "miner's lantern" and a 1.75 m miner,
  from a wrong memory note. The A2 hero is Wick, a lantern. Claude caught it by reading `CHARACTER-SHEET.md`
  before the brief was written.
- **A check that printed stale numbers.** Step 1 printed `dims (1.0, 1.0, 1.0)` for a part that was
  already 0.0625 × 0.0625 × 0.70. The scene had not been refreshed. `get_scene_info` showed the truth.

## 11. Predicted failures (brief §7) — what actually happened so far

| # | Prediction | lamp_post so far |
|---|---|---|
| F1 | lying on its side | did not happen: tallest axis Y in Godot for lamp_post and pit_prop; a deliberate +Y-Up-off export was caught |
| F2 | ×10 / ×100 size | lamp_post and oil_drop: did not happen in Blender (exact match); the 22.5° vertex-start width error checked on oil_drop, did not happen |
| F3 | origin in the middle | did not happen (z min 0); the default cube showed the failure before we started |
| F4 | scale/rotation not applied | all three were built with unapplied scale (pit_prop's braces also with ±45° rotation) and then applied: every asset has rotation 0 and scale 1 in Blender; Godot node scale pending |
| F5 | more detail than asked | did not happen: lamp_post 60 / 72, oil_drop 64 / 120, pit_prop 60 / 60 |
| F6 | colour lost at export | did not happen: every albedo matches in the .glb and in Godot. But the colours render brighter than their hex on screen, a look issue the check cannot see |
| F7 | missing faces / flipped normals | lamp_post: 0 inward-facing faces, closed bottom; oil_drop: 0 inward, positive volume, 0 boundary edges after the weld; pit_prop: 0 inward, 0 boundary edges. Godot look pending |
| F8 | MCP drops mid-build | did not happen: every call returned, including a file load through the MCP |
| F9 | 6 cm post too thin at game size | not observed: Rui raised no problem with the lamp post in either Godot look |
