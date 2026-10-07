# Master QC — claude-liam-walker-lamplight-gamedev (2026-10-07, Claude; third compile: outro jingle, B07/B08 climb-image wording)

File: `exports/landscape/claude-liam-walker-lamplight-gamedev.mp4`
SHA-256 `f0ae62846568d6013f68f96b63f891486d3302910da23aca04f36d2bd12c41d7` · 64.7 MB · not committed (MP4).

| Check | Result |
| --- | --- |
| Streams | H.264 3840×2160 30 fps · AAC 48 kHz stereo · 329.93 s · 22/22 beats filled |
| Gate F (docs) | pass |
| `verify_gamedev.py` | pass — 60 files, 3 exclusions, 5 exact excerpts, 5 code→result pairs |
| Gate V (`final_frame_check`) | 44 frames, **0 BLOCKER, 0 MAJOR** (first compile: 14 BLOCKER, 10 MAJOR; fixes in FRICTIONAL.md 2026-10-07) |
| Frame review by eye | one mid-beat frame per beat taken from the master: one label per gameplay shot, nothing clipped, B18/B19 inside the safe area, end card "YOU ESCAPED" legible |
| Loudness | integrated −23.4 LUFS, LRA 6.1 LU, true peak −0.6 dBFS (Assignment 1 master with the same toolkit: −24.6 LUFS) |
| Narrated beats | mean ≈ −27 dB, max ≈ −7 dB |
| B13 slice audio | mean −17.7 dB, max −0.6 dB: **about 10 dB louder than the narration.** Left unprocessed, as CAPTURE.md says. Rui, 2026-10-07: "一不用改" (no change) |
| B21 outro | 9.37 s, stock jingle `bear-brown-6.mp3` at −8 dB: mean −24.0 dB, max −8.4 dB. First compile had a silent outro because OUTRO-LOCK's `svg/claude/mp3/` is not in the toolkit; Rui: "2配一下吧", so the stock @NikBearBrown set in `logos/bear-brown/` is used, picked by the slug as the lock says |

Not done by Claude: watching the whole film in real time with sound on a human's ears. That is Rui's check.

## Third compile (2026-10-07)

Found while drafting SUBMISSION.md: B07 and B08 said the ladder image "is the back view". TEST-REPORT §3 says it
is a front view with a faceless flame standing in for one (the model drew no back view in four tries). Rui chose
to fix the film. B07 and B08 were re-narrated; B08's line was also reordered to the order on screen (walk, ladder,
rise, fall) and its lead-in shortened, so "the faceless climb image" is spoken at 2.07–3.90 s of B08 while the
climb is on screen at 2.07–4.12 s. Every gameplay clip was re-cut from the frames and re-labelled once; B07 was
re-rendered. B13 is now 8.47 s (it starts where B08 ends). The comment in `player.gd` line 150 still says
"climb is the back view": it is the source shown in the film, unchanged since `a70758d`.
