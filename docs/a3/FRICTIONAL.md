# Frictional — Assignment 3 log (3D assets with the Blender MCP)

Dated, in order. Entries are written on the day unless marked **(retrospective)**.
Each entry separates what Rui did or decided, what Claude (Claude Code, Opus 5.5) did, and what is still open.
Rui's own words are quoted exactly. Where an entry has no words from Rui yet, it says *Rui to add*; Claude
does not write Rui's reasons or learning.

Raw timestamped install log (Claude's, kept outside the repo): `F:\7270\a3-setup\setup-log.md`.

## 2026-10-14 23:42 → 2026-10-15 00:02 — stage 0: installing Blender, uv and the MCP

- **Asked (Rui):** "先执行阶段0，把需要的东西装好" ("do stage 0 first, install what is needed").
  The MCP two-hour time box starts here (23:42 −04:00).
- **Done (Claude):**
  - **Blender 5.1.2** (the chapter's version). Portable zip on F:, because C: has about 19 GB free.
    `download.blender.org` answered **HTTP 403** with a Cloudflare challenge page, so Claude downloaded from
    the official mirror `mirror.clarkson.edu`. The SHA-256 matches the mirror's own list. It could **not**
    be checked against blender.org: the browser got a human-verification page there, which Claude must not
    complete.
  - **uv 0.13.1.** The README's Windows line pipes an install script into PowerShell. Claude downloaded the
    same official release zip instead, checked its published SHA-256 and unzipped it to `F:\7270\tools\uv`.
    Then Claude added that folder to the user PATH and pointed uv's cache and Python directories to F:.
  - **The add-on.** `uvx mcp-for-blender@2.1.9 addon-paths` said **"No Blender addons directories
    found."** A portable Blender is not detected. The README's documented override
    `BLENDERMCP_ADDONS_DIR=…\Blender\5.1\scripts\addons` worked.
  - **Read the add-on's source before enabling it.** It binds `localhost:9876`. Every service and
    download toggle defaults to off, and telemetry consent is off. The start button's label in the code is
    **"Connect to Claude"**: the assignment says "Connect to MCP server", the README says "Start MCP Server".
    On every start it **fetches `addon.py` from GitHub** to check for updates (no install without a click).
    Claude wrote a launcher, `F:\7270\tools\blender-a3.cmd`, that sets `BLENDERMCP_NO_UPDATE_CHECK=1` so the
    add-on stays at one version for the whole assignment.
  - **Registration.** `claude` is not on PATH in the desktop app, so Claude used the app's bundled
    `claude.exe` 2.1.295. **The chapter's line fails as written:**
    `claude mcp add -e DISABLE_TELEMETRY=true blender -- uvx mcp-for-blender` → exit 1, `Invalid environment
    variable format: blender …`. `-e` takes several values and swallowed the server name. With the name
    first it worked: `claude mcp add blender -s user -e DISABLE_TELEMETRY=true … -- F:\7270\tools\uv\uvx.exe
    mcp-for-blender@2.1.9`. Claude pinned 2.1.9 and used the absolute `uvx.exe` path, because the running
    app does not see the new PATH. `claude mcp get blender` reported "Connected". That only proves the
    server process starts, not that Blender is reachable.
- **Done (Rui):** enabled the add-on. First try: Rui typed "add-on" into the Preferences window's
  top-left search box and got nothing ("找不到", "can't find it"). That box searches settings, not the
  add-on list. Rui then used the Add-ons section's own search box and ticked **Interface: MCP for Blender**
  ("完成了", "done").
- **Checked (Claude):** port 9876 listens on **127.0.0.1 only** (owner `blender.exe`, PID 44204). No
  firewall rule was created. A raw socket `ping` → `pong`, and `get_scene_info` returned the default scene.
  This proves the add-on answers. It does not prove Claude Code's MCP client reaches it.
- **Open:** `BLENDER_MCP_SAFE_MODE=1` (README: blocks file, network and process access in generated
  code) was left off to match the chapter's setup.

## 2026-10-15 — learn the window (Rui)

- **Done (Rui):** a look-only session, then wrote the six interface parts in Rui's own words
  ([BLENDER-NOTES.md](BLENDER-NOTES.md)) and took a screenshot of Rui's own session.
- **Checked (Claude, facts only, no rewording):** the first screenshot did not match two statements in the
  notes. The active tool was Move, not Select Box (the header's "Drag: Select Box" is a Move-tool setting),
  and the Cube had been dragged to (−0.54, 1.72, 0.51), not (0, 0, 0). Rui restarted the PC, and the moved
  cube was not saved (it did not need to be).
- **Decided (Rui):** retake the screenshot instead of rewriting the notes. The new screenshot (2551×1527,
  default scene, Select Box active, Cube at 0, 0, 0) matches the notes word for word.
- **Committed:** `1e9bbb8`. Claude added only Markdown formatting.

## 2026-10-15 15:10 — the MCP route works (first tool calls from Claude Code)

- After the restart, the Claude Code session loaded the `blender` tools. Claude called three read-only
  tools:
  - `get_addon_status`: protocol 13/13, add-on (1, 8), Blender 5.1.2; every library and generator is off;
    `telemetry_consent: false`.
  - `get_scene_info`: the default cube is 2.0 × 2.0 × 2.0 and **"below ground by 1.0"**.
  - `look`: returned a viewport image.
- One more naming mismatch: `get_addon_status` calls the add-on "Interface: Blender MCP", while Preferences
  shows "Interface: MCP for Blender".
- **Time box:** connected. The wall-clock gap from 23:42 is about 15 h, but that includes the night. Active
  setup time was about 20 minutes. Nothing needed the script-route fallback.

## 2026-10-15 — the brief, and a wrong assumption caught before it was written down

- **Claude's mistake, caught by reading the code:** Claude's plan (2026-10-14) proposed a "miner's
  lantern" and a 1.75 m miner as the scale reference. It came from a wrong note in Claude's memory. The
  A2 hero is **Wick, a walking brass lantern** (`CHARACTER-SHEET.md`), so a lantern asset would have
  duplicated the player. Claude measured the A2 level instead: tunnel 320 px floor to ceiling, tile 64 px,
  Wick's collider 36×56, lamp post 116 px, oil drop 22×24.
- **Decided (Rui), from Claude's options:**
  - scale **160 px = 1 m** (Wick 0.35 m, tunnel 2.0 m);
  - assets **lamp post, oil drop, pit prop**;
  - A3 docs in **`docs/a3/`**, so the A2 files at the root stay as submitted.
- **Done (Claude):** drafted [CHANGE-BRIEF.md](CHANGE-BRIEF.md): every size from a cited line of A2 code,
  origins, colours from the game's palette, budgets 72 / 120 / 60, nine predicted failures with their
  checks, and the Godot numbers the check must report.
- **Approved (Rui):** "我看过 docs/a3/CHANGE-BRIEF.md 了，可以" ("I've read it, it's fine").
  Committed `9579486` and tagged `a3-brief` before any asset was built.

## 2026-10-15 — lamp_post, built through the MCP

- **Plan (Claude) → approved (Rui):** step 0 empties the scene without reloading the file (a reload could
  drop the add-on's server). Steps 1–5 add one 1 m cube per part, moved to its centre and scaled to the
  brief. Colours go on the Principled BSDF Base Color, converted from sRGB hex to linear. Then Rui looks.
  Step 6 applies all transforms and joins the parts.
- **What happened (Claude's calls, all recorded in `tools/blender/build_lamp_post.py`):**
  - Steps 0–5 ran without an error.
  - **Claude's own check proved less than it claimed.** Step 1 printed `dims (1.0, 1.0, 1.0)` for the post,
    because the view layer had not updated after the scale change. `get_scene_info` showed the real size.
    Steps 2–5 call `view_layer.update()` before printing.
  - `get_scene_info` rounds to two decimals (0.0625 → 0.06), so it cannot confirm the brief's millimetres.
    Step 6 read the vertex coordinates instead.
  - **Step 6:** one object `lamp_post` at (0, 0, 0), rotation 0, scale 1. Size 0.19375 × 0.0955 × 0.725 m,
    X range −0.03125 … 0.1625, 60 triangles, 0 inward-facing faces, 0 non-manifold edges. All as the brief.
  - **Replay:** the saved script replays in a headless Blender with exit 0 and gives the same numbers, but
    the **pre-edit** colours. After the hand edit, `blender/lamp_post.blend` is the source of truth, not the
    script.
- **Hand edit (Rui):** changed the flame's colour in Blender's window. Rui's reason: "我认为灯芯之前的颜色有点
  暗，所以换了一个更明亮的颜色" ("I thought the flame's previous colour was a little dark, so I changed it
  to a brighter one"). Recorded value: Base Color `#ffcf5a` → `#fdffa6`.
- **Caught by reading back the edit (Claude):** the window's Base Color had also changed, `#241f2c` →
  `#241c54`. Rui: "玻璃窗不是我有意改的，请改回 #241f2c" ("the window change was not intentional, please
  change it back"). Claude reverted only that input (step 7a). Without the read-back, the accidental colour
  would have shipped.
- **Observed (Claude):** Rui's edit changed the Base Color (what glTF exports), not the material's
  viewport colour, which is still `#ffcf5a`. In Solid shading the flame therefore still looks like the old
  colour; Material Preview shows the new one.
- **What the hand edit taught me about the interface (Rui):** *Rui did not add this (asked 2026-10-15).*
- **Saved:** `blender/lamp_post.blend` (step 7b, by code at Rui's request). Claude reopened it headless:
  the numbers and colours above are what the file holds. `.blend1` backups are git-ignored.
- **Human / AI:** Rui chose the assets and scale, approved the plan, looked in the viewport, made the
  colour edit and rejected the accidental window change. Claude wrote and ran all the code, read the edit
  back, and wrote this entry.
- **Open:**
  - Does the 6 cm post read at game size beside Wick (F9)? That needs the Godot scene.
  - Should the flame's viewport colour also be updated? It does not affect the export.

## 2026-10-15 — oil_drop, built through the MCP

- **Looked at the A2 sprite first (Claude):** printed `oil_drop.png` as text. It is a teardrop, pointed at
  the top and widest about 40 % up. Taken literally, the brief's round 0.1375 m sphere plus a cone to
  0.15 m would read as a ball with a bump. **Claude proposed** a sphere squashed to 0.10 m plus a cone tangent
  to it. **Rui approved** before anything was built ("批准压扁球加圆锥的方案"). Brief §9.
- **Protecting the first asset (Claude):** step 0 first did *Save As* `oil_drop.blend`, then emptied
  the scene. Emptying the open `lamp_post.blend` first would let a later Ctrl+S overwrite it with an empty
  scene. git confirmed `lamp_post.blend` unchanged.
- **A predicted hidden size error that did not happen:** an 8-segment sphere is only 0.127 m wide if its
  vertices start at 22.5°. Claude printed the vertex angles: 0°, 45° … so the width is the full 0.1375 m.
  The cone's base ring landed exactly on the sphere's z 0.075 ring (radius 0.05954, same angles), so no
  rotation was needed.
- **Looking and deciding (Rui):**
  - After steps 1–2, Rui chose **smooth shading** and to **try the highlight ball**.
  - Read-back before changing anything: the cone was **already smooth-shaded** and the body was not.
    Claude's code had not done that. Its source is **unconfirmed**: Claude asked whether Rui clicked Shade
    Smooth with the cone selected, and the answer did not come through. *Rui did not add this (asked again
    2026-10-15); it stays unconfirmed.*
  - Claude added the highlight ball (24 triangles, `#ffe08a`, total 118 of 120). Claude's description of
    the look: it read as a stuck-on bead, not a highlight. **Rui rejected it:** "感觉高光球有点丑，不要了吧"
    ("the highlight ball looks a bit ugly, drop it").
- **A side effect of smooth shading, caught by looking (Claude):** a hard line where the cone met the body.
  Separate meshes do not share normals. Claude proposed welding. **Rui:** "焊接，消除交界线，然后做第 3 步"
  ("weld, remove the seam line, then do step 3").
- **Step 3 result:** one object `oil_drop`, transforms applied, 0.1375 × 0.1375 × 0.15 m, z min 0,
  **64 triangles** (94 − 30 hidden), 0 inward-facing faces, positive volume, 0 boundary or non-manifold
  edges. The seam line is gone in the look images. Saved, reopened headless and confirmed. Unlike lamp_post,
  the whole script replays to the same final mesh (there was no hand edit on this asset).
- **Human / AI:** Rui approved the shape change, chose smooth shading, and rejected the highlight. Claude
  read the sprite, proposed the shape and the weld, wrote and ran all the code, and wrote this entry.
- **Open:**
  - The amber looks paler under Blender's Material Preview light than on the dark game background. Judge
    it in Godot.
  - The cone's smooth shading source: unconfirmed (Rui did not add it).

## 2026-10-15 — pit_prop, built through the MCP

- **Plan (Claude) → approved (Rui):** brief §3.3 as written. Step 0 again did *Save As* `pit_prop.blend`
  before emptying the scene; git confirmed both earlier `.blend` files unchanged. Steps 1–3 built two
  posts (0.16 × 0.16 × 1.84) and the dark cap beam (1.2 × 0.16 × 0.16): 36 triangles, every number as
  planned on the first try.
- **Looking (Claude's description, then Rui's decision):** plain, the frame could read as a door frame or
  a goal. Nothing in three straight timbers says "mine". Rui: "加两根斜撑试试" ("try adding two braces").
  Read-back first: no hand change.
- **The braces (Claude):** 45°, 0.3 m legs, 0.08 × 0.12 m section. Each end runs 0.04 m into the post and
  the beam, so the square end of a tilted box leaves no triangular gap at the joint. Total 60 triangles,
  exactly the budget. **Rui:** "斜撑可以，继续第 4 步" ("the braces are fine, go on to step 4").
- **F4 seen for real:** before step 4, `get_scene_info` showed the braces at rotation (0, ±45, 0) and scale
  (0.5, 0.12, 0.08). Exported like that, Godot would get rotated, scaled nodes. Step 4 applied all
  transforms: one object `pit_prop` with rotation 0 and scale 1, 1.2 × 0.16 × 2.0 m, X −0.6 … 0.6, z min 0,
  60 triangles, 0 inward-facing faces, 0 boundary edges. Saved, reopened headless and confirmed. The whole
  script replays to the same mesh.
- **Human / AI:** Rui approved the plan, chose to add the braces and accepted them. Claude wrote and ran
  all the code, described the looks, and wrote this entry.
- **Open:** do flat-colour timbers read as old mine timber at game size? That is a human check in Godot.

## 2026-10-15 — export, Godot import, checks, asset room

- **Plan (Claude) → approved (Rui):**
  - Export with a saved headless script (`tools/blender/export_glb.py`, glTF binary, +Y Up), not through the
    MCP. Switching files in Rui's live session could have dropped the add-on's server.
  - Check each `.glb` file directly before Godot (`tools/check_glb.py`), then check it in Godot
    (`godot/tests/check_a3_assets.gd`).
  - Build the asset room with one neutral DirectionalLight3D plus ambient (a WorldEnvironment, not a light
    node), an orbit camera, and a Wick stand-in box.
- **What happened (Claude):**
  - Export exit 0 for all three. `check_glb.py` 18/0. Godot `--import` printed no error or warning.
    `check_a3_assets.gd` 30/0. The whole suite (`tools/run_tests.sh`, A2's 99 checks + A3's 30) passed.
  - The Godot import also created `.uid` files for three A2 test scripts (Godot metadata; no behaviour change).
- **Proving the checks can fail (Claude):** a passing check proves nothing if it cannot fail. Three tests:
  - A pit_prop exported with +Y Up **off** → `check_glb.py` failed 3 checks (height on Z).
  - A copy of the room with oil_drop lifted 5 cm → `rests_on_floor` failed, "gap_m": 0.05. That check
    compares each asset with the **Floor node's** top, not with the asset itself, which was the trap in the
    Module 3 example.
  - After the size revision below, the **stale** `.glb` files failed the new expectations (4 checks) until
    they were re-exported.
- **Claude's own look at scripted screenshots** (`docs/a3/evidence/`, labelled as Claude's captures): the
  colours render lighter and more saturated than their hex values under this light (the oil drop looks
  lemon-yellow). The checks only prove that the stored albedo numbers match.
- **Human check (Rui, orbiting the camera in the running scene):** "我检查完了，出现在游戏中的油滴不可能这么小，
  我感觉木架有点偏大" ("I've checked it: the oil drop in the game can't be this small, and I feel the frame is a
  bit too big").
- **Revision (the inspect-and-revise cycle):**
  - Claude showed that the drop's 0.15 m is the exact 160 px = 1 m conversion of its sprite, so the
    numbers were right and the look was not. Then Claude offered options.
  - **Rui chose:** oil drop ×2; pit prop keeps its 2.0 m height but is narrower and thinner (0.8 m, 0.12 m
    timber); Claude makes the change through the MCP.
  - Before rebuilding, Claude found pit_prop in **Edit Mode** in Rui's session. Claude compared a
    fingerprint of the edit-mode vertices with the saved file (identical: `6a1a6c09fb6fd367`), so no
    edit of Rui's was overwritten.
  - **Opening `oil_drop.blend` through the MCP** (`wm.open_mainfile`) worked, and the connection survived
    the file load. Claude saved pit_prop first in case it did not.
  - The rebuild also exposed leftover orphan meshes in the session, which forced `.001` names. Claude
    purged them.
  - Result: oil_drop 0.275 × 0.275 × 0.30 m, pit_prop 0.8 × 0.12 × 2.0 m. Re-exported, `check_glb.py`
    18/0, suite all green. Both build scripts replay to the revised meshes.
  - The 160 px = 1 m conversion is now deliberately broken for the oil drop (brief §9).
- **Human / AI:** Rui did the human check and chose both revisions. Claude proposed the options, made the
  changes, ran every check and wrote this entry.
- **Second look (Rui), revised room:** "看完了，没问题了" ("I've looked, no problems now"). Revision cycle closed.
- **Open:** Rui did not comment on the colours rendering brighter than their hex values. That is recorded
  as a known limitation, not as a confirmed pass. The room's neutral light is not the game's dark, warm
  lighting either.

## 2026-10-15 — the explainer film

- **Plan (Claude) → approved (Rui):** Brutalist `godot-gamedev`, walker mode, about 4 minutes. A2's game files are
  listed as exclusions in the evidence ledger, because the checker inventories all of `godot/`. Blender code is
  shown in stills, because code panels may only quote `godot/` files.
- **Rui's footage:** Claude first prepared scratch files for two screen recordings. **Rui:** "我不想录视频，要求里说了截图也行"
  ("I don't want to record video; the assignment says screenshots are fine"). Rui took three screenshots instead:
  - S1: the real prompt in the Claude app;
  - S2: lamp_post with its Dimensions;
  - S3: the flame's Base Color at FDFFA6.
  Skipping video meant the film shows the real prompt from the real session, not a re-run.
- **Script:** Claude drafted the 18-beat script with narration and labels; Rui approved it. One change before
  rendering: the greeting "Sawubona" was already used by other toolkit reels, so it became "Mingalaba".
- **What the pipeline caught (Claude):**
  - The first code-panel renders overflowed. B10 lost the OilDrop node, and B12's wrapped lines pushed out the
    two lines the narration is about. Both excerpts were shortened and re-rendered.
  - Gate F refused the first compile because the docs were not at the reel root.
  - The second compile refused six slates, because the stills must be `media/Bxx.png`.
  - Gate V then passed with 0 BLOCKER and 0 MAJOR. `verify_gamedev.py` passed. The master is −24.4 LUFS.
- **Evidence re-run for the film:** in throw-away copies, the three deliberate faults were run again (3, 1 and 4
  FAIL lines). The "before" room was re-rendered from `8d07135`'s `.blend` files. Its re-exported files fail the new
  size checks, which proves they are the old sizes.
- **Rui watched the whole master:** "成片我完整看过了，没问题" ("I watched the whole film; no problems"). Rui uploaded it
  to Northeastern OneDrive. Master SHA-256 `78d42317c8f59a1ff1cf25bad6637178802ae50fd5ba39585e9d6aedb7baadd3`, 265.03 s, source `4b4b77f`.
- **Human / AI:** Rui chose screenshots over video, took S1–S3, approved the script and accepted the master. Claude
  wrote the script, made the captures, stills and evidence, rendered the film and wrote this entry. The narration
  is Kokoro TTS.
