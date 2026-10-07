# FACTCHECK — every claim in the narration, and its evidence

| Beat | Claim | Evidence |
| --- | --- | --- |
| B00 | design first, then local generation, wired so sound only listens | CONCEPT/STORYBOARD/CHARACTER-SHEET/CHANGE-BRIEF committed before generation (tag `design-v1` = `6b5d099`); audio_director.gd |
| B01 | design said one tunnel; slice is three; change came from Rui's playtests | CONCEPT.md v1 "One short tunnel"; revision log 2026-10-07 (third playtest); commit `d195a92` |
| B01 | six playtests; ember burns out; jump −16 dB | TEST-REPORT §9 (6 rows); `0295499`; `77d0573` |
| B01 | generated locally, for free; every rejection logged | SOURCES.md models table; design/generation/gen-log.jsonl; design/rejected/ |
| B02 | light circle = oil gauge; shrinks without oil | lighting.gd `target_radius()`; run-01 footage |
| B03 | 6/s; 4 s ember; glint outside light; exit only cool light | session.gd `OIL_DRAIN`, `EMBER_LIMIT`; overlay.gd `GLINT`; lighting.gd exit light colour |
| B04 | storyboard hand-drawn, 8 panels, 3 sizes, 3 angles; committed and tagged before any image | STORYBOARD.md v2 coverage table; `git tag design-v1` 2026-10-06 01:52 −04:00; first generation logged 2026-10-06 later |
| B05 | 52 candidates, 51 rejected; green glass, pile, robot, one eye, copyrighted look-alike rejected | gen-log.jsonl (52 CHAR-REF lines, seeds 1001–1013); SOURCES.md CHAR-REF rows |
| B05 | prompt 6, flat cartoon, sheet pose init, seed 1012 | gen-log.jsonl entry s1012-b1 |
| B06 | face dissolved at 32×40; 64×80 chosen; game doubled | design/generation/candidates/sprite-size-demo-1006-b1.png; CHARACTER-SHEET revision 2026-10-07; commit `d0185ae` |
| B06 | face is an edit; oval chosen from three | face_edit.py; edit-log.jsonl; FRICTIONAL 2026-10-07 |
| B07 | swapped, not animated; 9 images; event look first; flip except ladder | player.gd 137–150 (shown verbatim) |
| B09 | marked first, +35, then emit | session.gd 275–285 (shown verbatim) |
| B11 | only listens; plays one file and counts; nothing writes back | audio_director.gd 43–55 (shown); test_audio F3 + F5 |
| B14 | v1 zero oil = darkness forever; Rui "risk is not enough"; 8 s then 4 s | TEST-REPORT §9 row 2–3; session.gd 249–258; CONCEPT revision log |
| B16 | four quoted changes | TEST-REPORT §9; commits `b72a749`, `0295499`, `d195a92`, `77d0573` |
| B17 | full route twice, with sound and muted, identical traces every 10 ticks | test_audio.gd 161–176 (shown); evidence/runs/audio-*.json |
| B18 | 99 checks 0 failures; 31 asset checks; runner fails on script error; fixed 60 fps fix | capture/test-output.txt; tools/run_tests.sh; FRICTIONAL step 5 and level-v2 entries |
| B19 | uncertainties: subtle muffling (Rui), MusicGen effects, near-frame-perfect gap | TEST-REPORT §5, §10; CAPTURE.md "Driver" |
| B19 | model per asset; contributions; source a70758d | SOURCES.md; capture/source-commit.txt |

**Note on the count (B05), found and fixed before the final render:** CHAR-REF was generated in 13 runs of 4
images (seeds 1001–1013) = 52 images; one (1012-b1) was accepted, so **51 were rejected**. The first narration
said "fifty two images came back wrong" and the status line said "52 REJECTED". Both were corrected ("SDXL made
fifty two candidates, and fifty one were rejected"; "51 OF 52 REJECTED"), the narration regenerated and B05
re-rendered.

**Note on excerpts:** design-board excerpts are exact substrings of the named documents with markdown
emphasis (`**`, `*`) removed; verified by script (`youtube/.../excerpts.json`).
