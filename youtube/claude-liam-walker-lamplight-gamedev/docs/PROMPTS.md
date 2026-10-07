# PROMPTS — what was asked, by whom

## The ask (B00, reconstructed — not a transcript)
"Please use Walker to convert my game design document about Wick, a walking lantern spirit escaping a dark mine
(oil drains every second, the light is the oil gauge, at zero the ember lasts four seconds) into a Godot asset
slice. Design first: concept, hand-drawn storyboard, character sheet. Then generate the art with SDXL and the
sounds and music with MusicGen, locally, log every prompt and rejection, and wire them in so sound only listens
to the game."

The real requests were Rui's, in Chinese, across the session ("make the map more complex", "the jump is still
loud", …); they are quoted in TEST-REPORT §9 and FRICTIONAL.md.

## Generation prompts
Exact prompts, negatives, seeds and settings for every image and clip are in the project:
`tools/gen/poses_round1.sh`, `tools/gen/env_round1.sh`, `tools/gen/audio_round1.json`, and one JSON line per
output in `design/generation/gen-log.jsonl`. The film quotes an exact excerpt of P6 (B05).

## Narration
All narration text is in `beat_sheet.json` (`narration_text`), written by Claude from the project's documents
and verified against FACTCHECK.md. Voice: Kokoro `am_onyx`, Liam in for Bear.

## Your Turn (B20)
"Before generating, write the on-screen size this asset must read at. Generate with a local model, reduce to
that exact size, and judge it there. If a detail dies, change the size or edit by hand, and log which. Then wire
one sound to the one line where its event happens, mute that bus, and add a test proving the game's trace is
identical with and without it."
