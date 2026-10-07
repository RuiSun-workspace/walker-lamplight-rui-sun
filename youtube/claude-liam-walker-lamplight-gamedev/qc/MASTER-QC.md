# Master QC — claude-liam-walker-lamplight-gamedev (2026-10-07, Claude)

File: `exports/landscape/claude-liam-walker-lamplight-gamedev.mp4`
SHA-256 `00e9e6af92c48b1322d5516826327eadc50bc63ae190cbc61694afbd8058d4f6` · 63.5 MB · not committed (MP4).

| Check | Result |
| --- | --- |
| Streams | H.264 3840×2160 30 fps · AAC 48 kHz stereo · 324.50 s · 22/22 beats filled |
| Gate F (docs) | pass |
| `verify_gamedev.py` | pass — 60 files, 3 exclusions, 5 exact excerpts, 5 code→result pairs |
| Gate V (`final_frame_check`) | 44 frames, **0 BLOCKER, 0 MAJOR** (first compile: 14 BLOCKER, 10 MAJOR; fixes in FRICTIONAL.md 2026-10-07) |
| Frame review by eye | one mid-beat frame per beat taken from the master: one label per gameplay shot, nothing clipped, B18/B19 inside the safe area, end card "YOU ESCAPED" legible |
| Loudness | integrated −23.4 LUFS, LRA 6.1 LU, true peak −0.5 dBFS (Assignment 1 master with the same toolkit: −24.6 LUFS) |
| Narrated beats | mean ≈ −27 dB, max ≈ −7 dB |
| B13 slice audio | mean −17.7 dB, max −0.6 dB: **about 10 dB louder than the narration.** Left unprocessed, as CAPTURE.md says; open for Rui (a single static gain would be the only change) |
| B21 outro | silent 7.0 s. OUTRO-LOCK says the card is silent under a stock jingle from `svg/claude/mp3/`; that folder is not in the local toolkit, so there is no jingle. None was made, since the lock allows only the existing ones |

Not done by Claude: watching the whole film in real time with sound on a human's ears. That is Rui's check.
