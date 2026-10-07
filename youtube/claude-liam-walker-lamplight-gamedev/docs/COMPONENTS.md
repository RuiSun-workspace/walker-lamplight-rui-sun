# COMPONENTS — what the film explains, and where

Ledger: `gamedev-evidence.json` (schema 1, `code-then-result-v1`), checked by `verify_gamedev.py`.

| Component | Files | Beats | Taught as |
| --- | --- | --- | --- |
| wick-state-images | player.gd, tuning.gd, 9 sprites + imports | B06 B07 B08 | asset trace → `_update_look` (player.gd 137–150) → real play |
| oil-and-rules | session.gd, lamplight_tunnel.json, main.tscn | B02 B09 B10 B14 B15 | `_collect_oil` (275–285) → pickup; ember lines (249–258) → burn-out |
| light-and-overlay | lighting.gd, overlay.gd | B03 B15 | pillar values; ring shrinking in run-03 |
| sound | audio_director.gd, bus layout, 5 OGG + imports | B11 B12 (+B13 unnarrated) | listeners (43–55) → hurt sound in run-02; slice audio in B13 |
| environment-art | 6 environment PNG + imports | B02 B05 | seen in play; generation logged in the project's SOURCES.md |
| hud | hud.gd | B02 B15 | gauge and blinking ember warning in play |
| project-config | project.godot, .gitignore | B06 | 1280×720 after the 64×80 decision; Nearest |
| tests | 8 test/capture scripts | B17 B18 | F5 trace check (test_audio.gd 161–176) → recorded output |

Exclusions (in the ledger with reasons): `levels/first_steps.json` (starter level, not loaded),
`levels/lamplight_tunnel_v1_two_tunnels.json` (v1 record, not loaded), `tests/capture_game.gd` (starter
screenshot script, not run).
