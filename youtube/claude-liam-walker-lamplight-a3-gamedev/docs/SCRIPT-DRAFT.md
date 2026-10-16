# A3 film — beat sheet draft for Rui's review (v1, 2026-10-15)

Working title: **"Lamplight in 3D: Right Numbers, Wrong Look."**
Slug: `claude-liam-walker-lamplight-a3-gamedev`. Brutalist `godot-gamedev`, **walker** mode. 4K landscape.
Narrator: Liam (in for Bear), Kokoro `am_onyx`. Narration is English. About 640 words, so roughly 4 to 4½
minutes once measured. Pronouns: Rui is never "he" or "she" in the narration.

Labels are burned into the picture wherever a beat shows something that is not live footage made by the
engine for this film:
- **"Screenshot by Rui, 2026-10-15"**
- **"MCP look capture from Rui's Blender session, 2026-10-15"** (Blender viewport images Claude took
  through the MCP while building)
- **"A2 slice footage, reused (same game build)"**
- **"Godot editor reconstruction"** (code panels)
- **"Headless output"**
- **"Re-rendered from commit 8d07135 sources"** (the "before" room)

| # | Visual (what is on screen) | Narration (Liam) | Evidence / label |
|---|---|---|---|
| **B00** | Claude composer with the reconstructed ask: *"Please use Walker to convert my game design document about Lamplight, a 2D lantern platformer, into three simple 3D assets…"* | Sawubona, this is Liam, in for Bear. The ask, reconstructed: Lamplight is a 2D game about a lantern that is its own light. Make three simple 3D assets for it in Blender by directing Claude through the Blender MCP, change at least one thing by hand, and show all three together in Godot at the size the game needs. | "Reconstructed prompt" |
| **B01** | Hesitant-writer summary (one-word correction on screen) | Three assets: a lamp post, an oil drop and a pit prop. Claude wrote every line of the Blender code, through the MCP. Rui set the scale, approved every step, made the hand edit, and, after one look in Godot, doubled the oil drop. The numbers were right. The look was not. | — |
| **B02** | A2 gameplay clip: Wick walking past a lamp post, picking up an oil drop | This is the game the assets come from. Wick is a brass lantern, the oil drop refills his light, and the lamp post is where he comes back to. The game is flat, so these three are its first pieces in 3D, shown in a small room of their own. | "A2 slice footage, reused (same game build)" + hash |
| **B03** | Design board: Wick 56 px → 0.35 m, tunnel 320 px → 2.0 m, lamp post 116 px → 0.725 m | Everything starts with one conversion: one hundred sixty pixels is one metre. Wick's collider is fifty six pixels, so he is thirty five centimetres tall. A tunnel is three hundred twenty pixels, two metres. So the lamp post is seventy two and a half centimetres, copied from its pixels, and the pit prop is exactly one tunnel high. | Source lines in `player.gd`, the level JSON, `session.gd` |
| **B04** | Design board: the brief, with the `a3-brief` tag time, sizes, origins, budgets, the nine predicted failures | The brief was committed and tagged before anything was built. It fixed every size to the millimetre, put every origin at the base, set a triangle budget, and predicted nine failures: lying on its side, ten times too big, floating, scale not applied, colour lost, faces missing. | `git` tag time 15:23 −04:00 |
| **B05** | Rui's interface screenshot (left) + the failing `claude mcp add` output (right) | Rui learned the window first, and wrote the notes in Rui's own words. One line stuck: the default cube is two metres wide at a scale of one. Then the setup. The chapter's registration line failed as written: the dash e flag swallowed the server's name. Name first, and it connected. | "Screenshot by Rui"; the real error text from the setup log |
| **B06** | Rui's screenshot S1 (the real prompt "批准，按方案从第 0 步开始…" + Claude's step replies) beside the MCP look capture of the five lamp-post parts | Here is the loop, in Rui's real session. Rui approves a plan, and Claude builds one part per call: post, crossbar, lamp box, window, flame. Five boxes, sixty triangles. Every size is read back from the vertices, because the scene report rounds to two decimals. | "Screenshot by Rui"; "MCP look capture" |
| **B07** | Rui's S3 (lp_flame Base Color picker, Hex FDFFA6) + the read-back table `#ffcf5a → #fdffa6`, `glass #241c54 → #241f2c` | Then Rui's hand edit. The flame looked a little dark, so Rui changed its base colour from amber to a pale yellow, F D F F A 6. Reading the edit back caught something else: the window glass had changed too, by accident. Rui said put it back, and it went back. | "Screenshot by Rui (after the edit)"; values from the read-back |
| **B08** | Four MCP look captures of the oil drop: flat → smooth with highlight ball → welded (and the sprite as text art) | The oil drop shows how a look gets argued. A round sphere at this size reads as a ball, so the body is squashed and a cone sits on it as the tip. Smooth shading exposed a seam, so the two were welded. Rui tried a highlight ball, and rejected it as ugly. Sixty four triangles. | "MCP look capture" ×3 |
| **B09** | MCP looks: plain pit prop → braced; `get_scene_info` line showing the braces at rotation ±45 and scale (0.5, 0.12, 0.08) → after Apply: 0 / 1 | The pit prop, plain, read like a door frame, so Rui added two braces. Those braces sat at forty five degrees, with their scale not applied. Exported like that, Godot would get rotated, scaled nodes. Apply all transforms, and every asset leaves Blender at rotation zero, scale one, origin on the floor. | "MCP look capture"; MCP read-out |
| **B10** | **Code** (Godot editor reconstruction): `godot/game3d/asset_room.tscn`, the Floor / LampPost / PitProp / OilDrop node lines | In Godot, the room is a plain scene: a floor, one light, one camera, and each asset placed at height zero. No offset, no scale. If an origin were wrong, this is where an asset would float. | Exact excerpt, hashed |
| **B11** | **Result**: Godot room, 4K, scripted camera orbit, including from behind and from below | And there they are at game scale, beside a box the size of Wick. The camera goes behind and under. The floor is one sided, so every bottom face can be checked. | "Godot 4.7.2, scripted camera orbit (Claude's capture)" |
| **B12** | **Code**: `godot/tests/check_a3_assets.gd`, the `rests_on_floor` lines | The headless check measures each asset against the floor node, not against itself. A check that only measured the asset would prove nothing about the floor. | Exact excerpt, hashed |
| **B13** | **Result**: the real headless output (30 checks, 0 failed) + the three deliberate faults and their FAILs | Headless: thirty checks, zero failures, every size within a millimetre of the brief. And each kind of check was broken on purpose, to see it fail: export without Y up, lift the drop five centimetres, keep a stale file. Each one failed. | "Headless output" |
| **B14** | Before / after room: before re-rendered from `8d07135` sources, after from the current build; Rui's words on screen | Then the check no script can run. Rui walked the camera around and said: the oil drop can't be this small, and the frame is a bit too big. The drop's fifteen centimetres was the exact pixel conversion. The numbers were right; the look was not. So the drop doubled, and the frame got narrower and thinner, still two metres tall. | "Re-rendered from commit 8d07135 sources"; Rui's quote with translation |
| **B15** | Verdict artifact | The verdict. Shown working: three assets built through the MCP, exported upright, at the brief's size, standing on the floor, with forty eight checks passing. Still uncertain: the colours render brighter than their hex values, the room is not lit like the game, and Wick is still a box. Next: light the room the way the game is lit. Claude wrote every line of Blender and Godot code. Rui chose the assets and the scale, made the hand edit, and made the call that changed two sizes. | Source revision shown on screen |
| **B16** | Claude composer: the paste-ready "Your Turn" prompt | Your turn. Here is the paste ready prompt. Pick one asset from your game and write its size in metres from something the player already knows. Predict the one way it will go wrong, and the check that would catch it. Build it through the MCP, put it in Godot, and look at it beside your character before you trust the numbers. Liam, in for Bear. | — |
| **B17** | Locked `ClaudeTitleOutro`, stock jingle, no narration | — | — |

## Facts each line rests on (to be re-checked in FACTCHECK.md before rendering)

- 160 px = 1 m; Wick 36 × 56 px (`player.gd:50`); tunnel 320 px (level JSON); lamp post 116 px
  (`session.gd:358–362`). The oil drop was 24 px = 0.15 m, and is now 0.30 m (brief §9).
- The brief was tagged `a3-brief` at `9579486`, 2026-10-15 15:23 −04:00, before `ad1c230` (first asset).
- Hand edit: `lp_flame` `#ffcf5a → #fdffa6`. Rui: "我认为灯芯之前的颜色有点暗…". Accidental glass change
  `#241c54` reverted to `#241f2c` at Rui's request.
- Triangles: lamp_post 60, oil_drop 64, pit_prop 60. Checks: Godot 30/0 + glb 18/0 = 48. A2 suites 99/0.
- Deliberate faults: +Y Up off (3 FAIL), drop lifted 0.05 m (FAIL), stale files after revision (4 FAIL).
- Rui's human check: "出现在游戏中的油滴不可能这么小，我感觉木架有点偏大". Second look: "看完了，没问题了".
- Rui has not commented on the colours, so the verdict lists them as uncertain, not as a pass.

## What is still to be made after you approve

1. A 4K Godot capture of the room (scripted orbit) from an isolated copy at a fixed source commit.
2. The "before" room, re-rendered from the `8d07135` `.blend` sources in a separate copy (the repository is
   not touched).
3. `beat_sheet.json`, the evidence ledger (A2 files excluded with reasons), FACTCHECK, SOURCES, PROMPTS,
   narration audio, the Remotion scenes, the cut, the QC gates. Then you watch the master.
