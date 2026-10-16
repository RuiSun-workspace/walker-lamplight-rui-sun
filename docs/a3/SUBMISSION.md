# SUBMISSION

**Assignment:** Assignment 3 - Your First 3D Game Assets with Claude, the Blender MCP, and Blender

**Student:** Rui Sun

**Project name:** Lamplight (`walker-lamplight-rui-sun`)

**GitHub repository URL:** https://github.com/RuiSun-workspace/walker-lamplight-rui-sun

**Git tag and submitted commit SHA:** tag `a3`. The submitted commit is the one that adds this file; its full SHA is
in the Canvas note, because a commit cannot contain its own SHA.

**Game-source revision shown in the film:** `4b4b77fe9602b880e79b8ecd1da4c0d93f6e80bf` (build_id
`b7d1c7d6b3a8c4b70b8716089fd5a01a09afbb0a77ce0ce6034f193cdafd9c9e`). The submitted commit adds only the film's
documentation and this file. `git diff 4b4b77f a3 -- godot` is empty.

**Godot version, Blender version, and operating system:** Godot 4.7.2.stable.official.ed1daf0bf (GL Compatibility);
Blender 5.1.2; Windows 11 Home China. The assignment's commands are written for macOS; this repository uses the
Windows console executables and Git Bash's `timeout` (README).

**The three assets and what each is for:**
- `lamp_post` (0.19375 × 0.0955 × 0.725 m, 60 triangles): the checkpoint lamp post Wick respawns at.
- `oil_drop` (0.275 × 0.275 × 0.30 m, 64 triangles): the oil pickup that refills Wick's light.
- `pit_prop` (0.8 × 0.12 × 2.0 m, 60 triangles): mine-tunnel timber support, set dressing.

All three are in the asset room `godot/game3d/asset_room.tscn` at 160 px = 1 m. The oil drop is deliberately 2× that
conversion after Rui's human check.

**MCP project and version, or "script route":** MCP route for all three assets: MCP for Blender
(https://github.com/ahujasid/blender-mcp), PyPI `mcp-for-blender` 2.1.9, add-on 1.8, through Claude Code 2.1.295. Asset
libraries and generators were off and never called; telemetry was off. Every `execute_blender_code` body is in
`tools/blender/build_*.py`. Export used a saved headless script (`tools/blender/export_glb.py`).

**My hand edit in Blender:** the lamp post's flame colour, Base Color `#ffcf5a` → `#fdffa6`, because it looked a little
dark. Reading the edit back found that the window glass had also changed by accident (`#241c54`); I had it reverted to
`#241f2c`. Brief §9, TEST-REPORT §8.

**Checks run (command and result):**
- `timeout 120 godot --headless --path godot --script res://tests/check_a3_assets.gd --fixed-fps 60`: 30 checks,
  0 failed. Size, bounds, base at y 0, upright axis, node scale/rotation, triangles, colours, and each asset against
  the Floor node.
- `python tools/check_glb.py`: 18 checks, 0 failed. Reads each .glb's own glTF JSON.
- `bash tools/run_tests.sh`: A2's 99 checks and A3's 30, all passing.
- `godot --headless --path godot --import`: no error or warning.
- Deliberate faults, each shown to fail: export with +Y Up off (3 FAIL), the oil drop lifted 0.05 m (1 FAIL), stale
  files after the revision (4 FAIL).
- The fresh-clone verification of tag `a3` is recorded in the Canvas note.

**Final film URL and filename:**
https://northeastern-my.sharepoint.com/:v:/g/personal/sun_r3_northeastern_edu/IQADTR_nhidsQYwsMixaW2lRAcvRoMJdoghbNIagW1P0Vv4?e=OLJ7D5
— `claude-liam-walker-lamplight-a3-gamedev.mp4` (3840×2160, 265.03 s, 37.4 MB; Northeastern sign-in required)

**Final film SHA-256:** `78d42317c8f59a1ff1cf25bad6637178802ae50fd5ba39585e9d6aedb7baadd3`

**Summary of my changes:**
- Interface notes in my own words with my screenshot.
- A brief committed and tagged (`a3-brief`) before any asset was built: scale 160 px = 1 m, sizes, origins,
  budgets, nine predicted failures.
- Three low-poly assets built through the Blender MCP, with my hand edit, and with my choices on shape, shading and
  braces (one highlight rejected).
- `.glb` exports, a Godot asset room, a headless check and an independent file check.
- One inspect-and-revise cycle from my look in Godot (oil drop ×2, frame narrower and thinner).
- The Brutalist explainer film.

**Known limitations:**
- On screen the colours render lighter and more saturated than their hex values. I did not judge colour separately.
- The room uses one neutral directional light plus ambient, not Lamplight's dark scene with a warm point light.
- Wick is a box stand-in.
- The oil drop no longer follows 160 px = 1 m, and the pit prop does not exist in the 2D game yet.
- `lamp_post`'s build script does not replay my colour edit (the `.blend` is the source).
- The film shows my screenshots, not screen recordings.
- Two FRICTIONAL questions (what the hand edit taught me; whether I clicked Shade Smooth on the cone) are unanswered.

**Changed games since Assignment 2 (yes/no; if yes, FRICTIONAL.md entry):** No. Same game and repository
(`walker-lamplight-rui-sun`); A3 documents are in `docs/a3/`.
