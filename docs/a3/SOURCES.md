# Sources and credits — Assignment 3 (three 3D assets)

Assignment 2's sources, models and asset log stay in the root [SOURCES.md](../../SOURCES.md). This file
covers what Assignment 3 added.

## Started from

| What | Where | Revision |
|---|---|---|
| The Lamplight game (A2 asset slice, submitted) | this repository, `main` | `4cef687` (A2's submitted commit) |
| Sizes and colours of the three assets | A2's own code and art: `godot/features/player/player.gd` (Wick's collider), `godot/levels/lamplight_tunnel.json` (tunnel height), `godot/game/session.gd` and `overlay.gd` (lamp post shape and colours `#5a412a`, `#3b2a1c`, `#b8863b`, `#241f2c`, `#ffcf5a`), `godot/assets/env/oil_drop.png` (sprite shape and `#f2a93b`, `#ffe08a`) | `4cef687` |

No colour palette, model, texture or reference image from outside this repository was used.

## Tools

| Tool | Version | Role | License |
|---|---|---|---|
| Blender | **5.1.2** (build 2026-05-19, portable zip for Windows x64, SHA-256 `345bedea7b0acf7cc9666423d8553f9129622aea34ded65c23e8cb70f83f14ff`, from the official mirror `mirror.clarkson.edu`) | Modelling, through the MCP and by hand | GPL-3.0-or-later |
| Blender glTF 2.0 exporter | `io_scene_gltf2` **5.1.20** (bundled with Blender 5.1.2) | `.glb` export (`tools/blender/export_glb.py`) | Apache-2.0 |
| MCP for Blender (community project) | PyPI **`mcp-for-blender` 2.1.9**; Blender add-on `blender_mcp.py` **bl_info 1.8**, protocol 13; https://github.com/ahujasid/blender-mcp | Lets Claude Code drive Rui's live Blender (`execute_blender_code`, `get_scene_info`, `look`, `get_addon_status`) | MIT |
| uv | **0.13.1** (official release zip) | Runs the MCP server (`uvx mcp-for-blender@2.1.9`) | MIT / Apache-2.0 |
| Godot Engine | **4.7.2.stable.official.ed1daf0bf** | Import, asset room, headless checks | MIT |
| Claude Code | **2.1.295** (bundled with the Claude desktop app), model Claude Opus 5.5 (`claude-opus-5-5`) | Plans, all Blender and Godot code, checks, document drafts | Anthropic terms; Northeastern access |
| Python | 3.14.0 (system) | `tools/check_glb.py` (standard library only) | PSF |

**Switched off and never called:** MCP for Blender's asset libraries and generators. `get_addon_status`
reported Poly Haven, Sketchfab and Poly Pizza **off**, and Hyper3D, Hunyuan3D and Tripo **off**.
`generate_3d`, `search_assets` and `import_asset` were never called. Telemetry: `DISABLE_TELEMETRY=true` on the
server, add-on `telemetry_consent: false`. Nothing paid was used. No credentials exist in the repository.

The film's tools (Brutalist and Kokoro narration) will be added here when the film is made.

## The three assets

All geometry is built from Blender primitives by code Claude ran through the MCP, plus Rui's hand edit. No
downloaded or AI-generated mesh is used.

| Asset | Source file | Build code | Export | Hand edit |
|---|---|---|---|---|
| lamp_post | `blender/lamp_post.blend` | `tools/blender/build_lamp_post.py` | `godot/assets/models/lamp_post.glb` | **Rui**: flame colour `#ffcf5a` → `#fdffa6` |
| oil_drop | `blender/oil_drop.blend` | `tools/blender/build_oil_drop.py` | `godot/assets/models/oil_drop.glb` | — |
| pit_prop | `blender/pit_prop.blend` | `tools/blender/build_pit_prop.py` | `godot/assets/models/pit_prop.glb` | — |

## Human / AI contributions

Dated detail with commits: [FRICTIONAL.md](FRICTIONAL.md).

| Who | Contributed |
|---|---|
| **Rui (human)** | Wrote [BLENDER-NOTES.md](BLENDER-NOTES.md) in Rui's own words and took the screenshot (retook it so it matched the notes). Enabled the MCP add-on in Blender. Chose the scale (160 px = 1 m), the three assets and the docs layout, and approved the brief. Approved every build plan. Looked in Blender's viewport after each build. **Hand edit:** changed the lamp post's flame colour (and rejected an accidental window-colour change). Approved the oil drop's squashed-sphere shape. Chose smooth shading. **Rejected** the highlight ball. Chose the weld and the pit prop's braces. **Human check in Godot:** found the oil drop too small and the frame too big, and chose both revisions (drop ×2; frame 0.8 m wide, 0.12 m timber). Accepted the revised room. |
| **Claude (Claude Code, Opus 5.5)** | Installed Blender, uv and the MCP, and registered the server. Read the add-on's source before it was enabled. Measured the A2 game and drafted the brief's numbers. Proposed every build plan and wrote and ran **all Blender code** through the MCP (kept verbatim in `tools/blender/build_*.py`). Read every hand edit back. Wrote the export script, `tools/check_glb.py`, `godot/tests/check_a3_assets.gd`, the asset room scene and orbit camera, and the scripted captures in `evidence/`. Tested that each check can fail. Wrote the drafts of every A3 document. |
| **Generative models** | None. A3 used no image, mesh, audio or text generator for any asset. |

**What Claude got wrong**, and how it was caught:
- The first plan used a "miner's lantern" and a 1.75 m miner from a wrong memory note. Caught by reading
  `CHARACTER-SHEET.md` before the brief was written.
- A stale `dims` printout (1.0 for a 0.0625 m part) in lamp_post step 1. `get_scene_info` showed the truth.
