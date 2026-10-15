# Assignment 3 — change brief: three 3D assets for Lamplight

Written 2026-10-15, **before any asset was built** (the git timestamp of this file is the evidence).
This file is append-only: later changes go in §9, the text above it stays as first committed.

- **Decisions (Rui Sun, 2026-10-15):** the scale 160 px = 1 m, the three assets (lamp post, oil drop,
  pit prop), and A3 documents living in `docs/a3/`.
- **Drafted by Claude** from those decisions and from numbers read out of the A2 code (cited per row).
  Rui reviews and approves before it is committed.
- Informed by Rui's "learn the window" session ([BLENDER-NOTES.md](BLENDER-NOTES.md)): the default cube is
  2 m with scale 1.000, and the MCP's `get_scene_info` reported it "below ground by 1.0" because its origin
  is its centre. Both are failure modes this brief guards against.

## 1. The game and why it needs 3D assets

Lamplight (repo `walker-lamplight-rui-sun`, A2 submitted at `4cef687`) is a **2D** side-view pixel
platformer: Wick, a small walking brass lantern, climbs out of a dark mine. A3 does not change the 2D game.
It adds a small Godot 3D scene, the **asset room**, with a floor, one light, a camera and the three assets
side by side at game scale (reused in A4–A5). Nothing in A3 connects the 3D scene to the 2D game.

## 2. Scale: 160 px = 1 m

The 2D game measures everything in pixels at a 1280×720 viewport. Blender and Godot 3D both use metres, so
one conversion is fixed here and never changed: **160 px = 1 m** (1 px = 6.25 mm).

| Thing in the A2 game | Pixels (source) | Metres |
|---|---|---|
| Wick's collider (player height) | 36 × 56 (`features/player/player.gd:50`) | 0.225 × 0.35 |
| Tunnel, floor to ceiling | 320 (`levels/lamplight_tunnel.json`: floors y = 1320 / 960, ceilings at 1000 / 640) | 2.0 |
| Rock tile | 64 (`assets/env/tiles_rock.png`) | 0.4 |
| Lamp post, foot to top | 116 (`game/session.gd:358–362`) | 0.725 |
| Oil drop sprite | 22 × 24 (`assets/env/oil_drop.png`) | 0.1375 × 0.15 |

So Wick is a 35 cm hand lantern and the tunnels are 2 m high — the scale the art direction describes
("a tiny character in a big dark space"). A **Wick stand-in box** 0.225 × 0.225 × 0.35 m stands in the
asset room as the size reference. It is labelled as a stand-in and is not one of the three assets.

Axes: Blender is Z-up, so widths are X, depths Y, heights Z. The glTF exporter's **+Y Up** maps Blender
Z → Godot Y and Blender Y → Godot −Z. Godot sizes in §6 are written in Godot axes.

## 3. The three assets

All flat colour, built from Blender primitives, colours taken from the A2 game so the 3D pieces match the
2D palette. Each asset is built around Blender's world origin in its own `.blend` file.

### 3.1 `lamp_post` — the checkpoint (prop)

- **In the game:** the three checkpoint lamp posts (`level.lamp_posts`). Touching one makes it the
  respawn point. A2 draws it in code (`session.gd:_draw_lamp_post`) because no generated post was usable.
- **Look:** a thin timber post, a short crossbar at the top reaching right, and a brass lamp box hanging
  from the crossbar, with a dark glass window and a small flame showing through it. The silhouette (tall
  post + lamp hanging to one side) is what makes it read as a lamp post. It is the same shape as the
  2D one, copied pixel for pixel.
- **Parts (5 cubes):**

| Part | 2D pixels (from the foot) | Blender X | Y (depth) | Z | Colour |
|---|---|---|---|---|---|
| Post | x −5…5, h 0…112 | −0.03125 … 0.03125 | ±0.03125 | 0 … 0.70 | timber `#5a412a` |
| Crossbar | x −5…21, h 110…116 | −0.03125 … 0.13125 | ±0.03125 | 0.6875 … 0.725 | timber `#5a412a` |
| Lamp box | x 12…26, h 92…110 | 0.075 … 0.1625 | ±0.04375 | 0.575 … 0.6875 | brass `#b8863b` |
| Window | x 14…24, h 95…107 | 0.0875 … 0.15 | ±0.04575 (2 mm proud of the box, front and back) | 0.59375 … 0.66875 | dark glass `#241f2c` |
| Flame | x 17…21, h 97…105 (`overlay.gd:32`) | 0.10625 … 0.13125 | ±0.04775 (2 mm proud of the window) | 0.60625 … 0.65625 | flame `#ffcf5a` |

- **Size:** W × D × H = **0.19375 × 0.0955 × 0.725 m**.
- **Origin:** the **foot of the post**, at the centre of the post's underside (0, 0, 0). This is *not* the
  centre of the bounding box (the lamp hangs to +X), on purpose: the A2 level places lamp posts by that
  foot point, so the 3D asset uses the same anchor. Expected X range −0.03125 … 0.1625.
- **Budget:** **72 triangles** (5 cubes × 12 = 60, leaving room for one more part). A 0.725 m post is
  116 px tall on screen; nothing finer than a box would be visible.

### 3.2 `oil_drop` — the pickup (collectible)

- **In the game:** the six oil drops (`level.oil`). Touching one adds 35 oil.
- **Look:** a fat amber teardrop with the point up. The round bottom and point make it read as a drop
  and not a ball. Body amber `#f2a93b` (the sprite's main colour). Optional small highlight `#ffe08a`
  (the sprite's highlight) if it reads better. Decide by looking, then record which.
- **Parts (2, at most 3):** a UV sphere with **8 segments × 6 rings** (radius 0.06875 m), and a cone
  with **8 vertices** pointing up. Its top is the tip at 0.15 m and its base sits inside the sphere.
  Optional third part: a small highlight sphere (4–6 segments).
- **Size:** W × D × H = **0.1375 × 0.1375 × 0.15 m** (the sprite's 22 × 24 px; depth = width).
- **Origin:** **centre of the underside** (the bottom of the sphere at z = 0). In the 2D game a drop is
  drawn by its centre and floats (`overlay.gd:30`). The 3D asset still follows the course rule (base on
  the floor at the world origin), so in the asset room it rests on the floor. A game that hovers it would
  lift it by 0.075 m. This is a deliberate difference, recorded here.
- **Budget:** **120 triangles** (sphere 8×6 ≈ 80, cone ≈ 14, highlight ≈ 20). On screen the drop is
  24 px tall, so a smoother sphere could not be seen.

### 3.3 `pit_prop` — the timber support frame (environment)

- **In the game:** the "rotten timber pit props" named in the A2 art direction (`CONCEPT.md`). A2 does
  not draw them yet. They are background set dressing: a frame standing against the tunnel wall every few
  metres, holding up the roof.
- **Look:** two square timber posts and a cap beam across their tops — a doorway-shaped frame. Posts
  timber `#5a412a`, cap beam dark timber `#3b2a1c` so the beam separates from the posts.
- **Parts (3 cubes):** posts 0.16 × 0.16 × 1.84 m with centres at X = ±0.52. The cap beam is
  1.2 × 0.16 × 0.16 m, from Z 1.84 to 2.0.
- **Size:** W × D × H = **1.2 × 0.16 × 2.0 m**. Height = the tunnel's 2.0 m floor-to-ceiling, so it holds
  the roof. Width = 3 rock tiles (1.2 m). The opening is 0.88 m wide and 1.84 m high, so Wick (0.35 m) walks
  through it easily.
- **Origin:** **centre of the underside**, midway between the two posts (0, 0, 0).
- **Budget:** **60 triangles** (3 cubes = 36; room for two diagonal corner braces if the frame looks too
  plain — at most 5 shapes).

Total budget: 252 triangles across the three, each well under the course's 500.

## 4. Where things go

| What | Path |
|---|---|
| Blender sources | `blender/lamp_post.blend`, `blender/oil_drop.blend`, `blender/pit_prop.blend` — **outside** `godot/`, because Godot 4 tries to import `.blend` files it finds inside the project |
| Code Claude ran | `tools/blender/build_<asset>.py` (every `execute_blender_code` body, in order) |
| Exports | `godot/assets/models/<asset>.glb` (+ Godot's `.import`) |
| 3D scene | `godot/game3d/asset_room.tscn` — floor, one light, one camera, the three assets, the Wick stand-in |
| Headless check | `godot/tests/check_a3_assets.gd` |
| Docs | `docs/a3/` (this file, BLENDER-NOTES, TEST-REPORT, FRICTIONAL, SOURCES) |

## 5. Workflow

Brief → build (MCP, one asset per request, Rui approves each plan) → Rui looks in the viewport after each
step → at least one hand edit by Rui → apply rotation and scale → export glTF binary, +Y Up → import
headless → check script → asset room → Rui's human look → revise → export again.

## 6. Predicted numbers the check must report

Godot axes (X width, Y height, Z depth). Tolerance ±1 mm on every size, ±1 mm on the floor contact.

| Asset | AABB size X × Y × Z (m) | AABB min Y | AABB X range | Node scale | Triangles |
|---|---|---|---|---|---|
| lamp_post | 0.19375 × 0.725 × 0.0955 | 0 | −0.03125 … 0.1625 | 1, 1, 1 | ≤ 72 |
| oil_drop | 0.1375 × 0.15 × 0.1375 | 0 | −0.06875 … 0.06875 | 1, 1, 1 | ≤ 120 |
| pit_prop | 1.2 × 2.0 × 0.16 | 0 | −0.6 … 0.6 | 1, 1, 1 | ≤ 60 |

The tallest axis must be Godot **Y** for lamp_post and pit_prop (for oil_drop height and width differ by
only 12.5 mm, so its check is the size match itself).

## 7. Predicted failure cases and how each is checked

| # | Prediction | Check |
|---|---|---|
| F1 | **Arrives lying on its side** (Z-up vs Y-up confusion, or the +Y Up option off). | Check script: tallest AABB axis is Y; human look in the asset room. |
| F2 | **Wrong size by ×10 or ×100** (centimetre thinking, or built from the 2 m default cube without halving). | Check script: every AABB size within ±1 mm of §6; Blender sidebar Dimensions written next to the brief. |
| F3 | **Origin in the middle, so it floats or sinks** (exactly what the default cube does: "below ground by 1.0"). | Check script: AABB min Y = 0 ± 1 mm; in the asset room each asset at Y = 0 must sit on the floor. For lamp_post also the X range, because its origin is deliberately off-centre. |
| F4 | **Scale or rotation not applied**, so Godot gets a node scale ≠ 1 or a rotated root. | Blender: `get_scene_info` scale (1, 1, 1) and rotation (0, 0, 0) before export; check script prints every node's scale and rotation in the imported scene. |
| F5 | **Claude builds more detail than asked** (default 32-segment sphere ≈ 960 triangles; bevels; extra parts). | Blender Scene Statistics triangle count per file vs §3 budgets; check script counts triangles from the imported meshes. |
| F6 | **A colour does not survive the export** — set on `material.diffuse_color` (viewport only) instead of the Principled BSDF Base Color, or lost to a missing material. | Check script prints each surface material's albedo as hex next to §3; human look under the room's light. |
| F7 | **Missing faces / flipped normals** — faces that vanish from behind or below once Godot culls back faces. | Human check: orbit each asset in Godot including from behind and below; in Blender, the Face Orientation overlay before export. |
| F8 | **The MCP connection drops mid-build** (Blender busy, socket timeout, add-on restarted). | Every call's result is read before the next; if a call fails, `get_scene_info` to see what state Blender is in, and log the exact error in FRICTIONAL. Fallback: the same code as a headless script. |
| F9 | **The lamp post's 6 cm post reads as a stick or vanishes at game size** next to a 0.35 m Wick. | Human check only — a size match cannot show it. |

## 8. What the checks cannot show

A passing headless check proves the sizes, origin, orientation, node scale, triangle count and material
colour numbers that Godot imported. It does not prove the assets read as a lamp post, an oil drop and a
pit prop, that they look right under the room's light, or that they suit Lamplight's style. Those are Rui's
human checks, recorded in TEST-REPORT.

## 9. Revision log (append-only)

*(empty at first commit)*

- **2026-10-15 — lamp_post flame colour `#ffcf5a` → `#fdffa6` (Rui's hand edit in Blender).** Rui's
  reason: "我认为灯芯之前的颜色有点暗，所以换了一个更明亮的颜色" ("I thought the flame's previous colour
  was a little dark, so I changed it to a brighter one"). This changes §3.1's flame row and the colour the
  Godot check expects for `lp_flame`. Sizes, origin and budget are unchanged. The window colour was also
  changed by accident during the same edit (`#241f2c` → `#241c54`). Rui said it was not intended, so it
  was reverted to `#241f2c`; §3.1 stands for the window.
