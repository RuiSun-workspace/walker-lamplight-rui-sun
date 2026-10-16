# FACTCHECK — every narrated claim and where it is proven

Film: `claude-liam-walker-lamplight-a3-gamedev`. Source commit `4b4b77f` (full hash in `capture/source-commit.txt`).
Checked by Claude against the repository and recorded outputs, 2026-10-15. Rui approved the script text
(SCRIPT-DRAFT.md). The only later change is the greeting, Mingalaba instead of Sawubona, because Sawubona was
already used by other reels.

| Beat | Claim | Evidence |
|---|---|---|
| B00 | The ask: three simple 3D assets, built by directing Claude through the Blender MCP, one hand edit, all three in Godot at game size. | Assignment 3 text. The composer prompt is a **reconstruction**, labelled as such. |
| B01 | Claude wrote every line of the Blender code through the MCP. | `tools/blender/build_*.py` hold every `execute_blender_code` body. Rui's only Blender change was the colour hand edit (FRICTIONAL). |
| B01 | Rui set the scale, approved every step, made the hand edit, and doubled the oil drop after one look in Godot. | FRICTIONAL 2026-10-15 entries; brief §9; commits `9579486`, `ad1c230`, `5639322`. |
| B02 | Wick is a brass lantern; oil drops refill his light; lamp posts are where he comes back to. | A2 `CHARACTER-SHEET.md`, `CONCEPT.md`, `session.gd` (`_touch_lamp_posts`, respawn at the post). |
| B02 | The footage is the same game build. | `git diff a70758d 4b4b77f -- godot` touches only A3 files and three `.uid` files. |
| B03 | 160 px = 1 m; Wick's collider is 56 px → 0.35 m; a tunnel is 320 px → 2.0 m; the lamp post is 0.725 m; the pit prop is one tunnel high. | CHANGE-BRIEF §2 (exact excerpt on screen); `player.gd:50` (36×56); level JSON (floors 1320/960, ceilings 1000/640); `session.gd:358–362` (116 px). |
| B04 | The brief was committed and tagged before anything was built. | Tag `a3-brief` → `9579486`, 2026-10-15 15:23:10 −04:00; the first asset commit `ad1c230` came later. |
| B04 | Sizes to the millimetre, origins at the base, a triangle budget, nine predicted failures. | CHANGE-BRIEF §3, §6, §7 (F1–F9). |
| B05 | Rui wrote the interface notes in Rui's own words; the default cube is 2 m wide at scale 1. | `docs/a3/BLENDER-NOTES.md` (commit `1e9bbb8`; Claude added only formatting); Rui's screenshot. |
| B05 | The chapter's `claude mcp add -e DISABLE_TELEMETRY=true blender -- …` failed: `-e` swallowed the name; name first worked. | `F:/7270/a3-setup/setup-log.md`, 2026-10-14 23:49; FRICTIONAL stage 0. The panel abridges the second command with "…". |
| B06 | Rui approves a plan; Claude builds one part per call: post, crossbar, lamp box, window, flame; 5 boxes, 60 triangles. | Rui's screenshot S1 (the real prompt "批准，按方案从第 0 步开始。建完 5 个部件后停下来等我看。"); `build_lamp_post.py` steps 1–5; TEST-REPORT §5. |
| B06 | Sizes are read back from the vertices because the scene report rounds to two decimals. | `build_lamp_post.py` step 6 and its notes; `get_scene_info` printed 0.06 for 0.0625. |
| B07 | Rui changed the flame Base Color `#ffcf5a` → `#fdffa6` because it looked a little dark. | Read-back in `build_lamp_post.py`; Rui: "我认为灯芯之前的颜色有点暗，所以换了一个更明亮的颜色"; S3 shows Hex FDFFA6. |
| B07 | The window glass also changed by accident and went back at Rui's request. | Read-back `#241c54`; Rui: "玻璃窗不是我有意改的，请改回 #241f2c"; step 7a. |
| B08 | Squashed sphere + tangent cone; smooth shading exposed a seam; welded; Rui rejected the highlight ball; 64 triangles. | `build_oil_drop.py` steps 1–3; brief §9; Rui: "感觉高光球有点丑，不要了吧"; TEST-REPORT §5. |
| B09 | Plain pit prop read like a door frame (Claude's description); Rui added two braces. | FRICTIONAL pit_prop entry; Rui: "加两根斜撑试试". |
| B09 | Braces at 45° with scale not applied; after Apply: rotation 0, scale 1, origin on the floor. | `get_scene_info` before step 4: rot (0, ±45, 0), scale (0.5, 0.12, 0.08); step 4 output. |
| B10 | The room has a floor, one light, one camera, each asset at height 0, no offset, no scale. | `asset_room.tscn` lines 42–54 (exact excerpt; the Floor, line 38, is in the notes panel); `room.one_light` / `room.one_camera` PASS. "One light" = one Light3D node; ambient comes from WorldEnvironment (said on the code panel's note). |
| B11 | At game scale beside a Wick-sized box; behind and under; the floor is one-sided. | `media/B11.mp4` (frames 150–438 of room-orbit: behind at 9 s, below at 13 s); PlaneMesh is single-sided by default. |
| B12 | The headless check measures each asset against the Floor node, not against itself. | `check_a3_assets.gd` lines 154–158 (exact excerpt; floor_y, line 148, in the notes panel). |
| B13 | 30 checks, 0 failures, every size within 1 mm; three deliberate faults each failed. | `capture/test-output.txt` (re-run 2026-10-15 in the isolated copy). |
| B14 | Rui's words; the drop's 0.15 m was the exact pixel conversion; drop ×2; frame narrower and thinner, still 2 m. | TEST-REPORT §7; brief §9; before image re-rendered from `8d07135` sources (re-exported files fail the new size checks, recorded in test-output fault 3). |
| B15 | 48 checks passing (30 + 18). | test-output.txt. A2's 99 checks also pass (`run_tests.sh`, 2026-10-15), but are not counted in the 48. |
| B15 | Colours render brighter than their hex values; the room is not lit like the game; Wick is a box. | TEST-REPORT §6 limitation; README A3 limitations. Rui did not comment on colour, so this stays "uncertain". |
| B15 | Claude wrote all the Blender and Godot code; Rui chose the assets and scale, made the hand edit and the size call. | docs/a3/SOURCES.md contributions table. |

Not claimed: that the assets look right in Lamplight's real lighting, that the colours are right on screen, or
that the room is connected to the 2D game.
