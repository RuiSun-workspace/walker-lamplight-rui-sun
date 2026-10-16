# Master QC — claude-liam-walker-lamplight-a3-gamedev (2026-10-15, Claude; first master)

File: `exports/landscape/claude-liam-walker-lamplight-a3-gamedev.mp4`
SHA-256 `78d42317c8f59a1ff1cf25bad6637178802ae50fd5ba39585e9d6aedb7baadd3` · 37,415,469 bytes · not committed (MP4).

| Check | Result |
| --- | --- |
| Streams | H.264 3840×2160 30 fps · AAC 48 kHz stereo · 265.03 s · 18/18 beats filled |
| Gate F (docs) | pass (after the docs were placed at the reel root; the first compile refused: "missing or empty FACTCHECK.md") |
| Slots | the second compile refused six slates: the stills must be `media/Bxx.png`, not only `assets/`; copied, third compile clean |
| `verify_gamedev.py` | pass — 10 files, 63 exclusions (A2 slice), 2 exact excerpts, 2 code→result pairs |
| Pilot fix | B10 and B12 code panels overflowed (OilDrop node and the key floor lines cut off); excerpts changed to 42–54 and 154–158, re-rendered, re-verified |
| Gate V (`final_frame_check`) | 36 frames, **0 BLOCKER, 0 MAJOR** on the first master |
| Contact sheet by eye | `_qc/contact_sheet.png`: every beat shows its intended picture; labels legible; nothing clipped |
| Loudness | integrated −24.4 LUFS, LRA 5.5 LU (A2 master: −23.4 LUFS) |
| B02 (narration + A2 game audio at −14 dB) | mean −26.4 dB, max −8.1 dB |
| B11 (narration only) | mean −26.9 dB, max −5.4 dB |
| B17 outro | stock jingle `bear-brown-3.mp3` at −8 dB, 9.36 s: mean −23.9 dB, max −8.4 dB |

Not done by Claude: watching the whole film in real time with sound on a human's ears. That is Rui's check.
