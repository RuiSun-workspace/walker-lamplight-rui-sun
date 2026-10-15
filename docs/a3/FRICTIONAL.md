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
- **What the hand edit taught me about the interface (Rui):** *Rui to add.*
- **Saved:** `blender/lamp_post.blend` (step 7b, by code at Rui's request). Claude reopened it headless:
  the numbers and colours above are what the file holds. `.blend1` backups are git-ignored.
- **Human / AI:** Rui chose the assets and scale, approved the plan, looked in the viewport, made the
  colour edit and rejected the accidental window change. Claude wrote and ran all the code, read the edit
  back, and wrote this entry.
- **Open:**
  - Does the 6 cm post read at game size beside Wick (F9)? That needs the Godot scene.
  - Should the flame's viewport colour also be updated? It does not affect the export.
