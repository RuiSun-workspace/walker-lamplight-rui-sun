# COMPONENTS — what the film explains, and from which files

Inventory of `godot/` at `4b4b77f`: 73 authored files (`.uid` and `.godot/` not counted). 10 belong to Assignment 3
and are explained here. 63 are Assignment 2's 2D slice, listed as exclusions in `gamedev-evidence.json` with one
reason: unchanged by A3 (only Godot `.uid` files were added) and explained by the A2 film.

| Component | Files | Beats | What the film shows |
|---|---|---|---|
| three-assets | `assets/models/{lamp_post,oil_drop,pit_prop}.glb` + `.import` | B06–B09, B14 | Built through the MCP one part per call, Rui's hand edit, the oil drop's shape argument, braces and Apply Transforms, the size revision after Rui's look |
| asset-room | `game3d/asset_room.tscn`, `game3d/orbit_camera.gd`, `tests/capture_a3_room.gd` | B10 → B11 | Code: the four instanced nodes at y = 0 (lines 42–54). Result: the 4K room orbit, from behind and below |
| headless-check | `tests/check_a3_assets.gd` | B12 → B13 | Code: the floor comparison (lines 154–158). Result: the recorded 30/0 output and the three deliberate faults |

Outside `godot/` but shown in stills (not ledger excerpts): `tools/blender/build_*.py` (via MCP read-outs and look
captures), `tools/blender/export_glb.py`, `tools/check_glb.py` (its 18/0 output in B13), `docs/a3/*`.
