# walker-lamplight-rui-sun

> **Status: scaffold (2026-10-03).** Design documents are being written; no asset has been generated yet.
> Sections marked _TBD_ are filled in as the work lands, not in advance.

**Lamplight** (working title) — a small side-view pixel-art platformer for CSYE 7270 Fall 2026,
Assignment 2 "Generate Art, Sound, and Music for Your Game". You are a lamp-carrying miner descending
a dark mine; the lamp's oil keeps draining, so you pick up oil drops while looking for the way out.

## Started from

The Godot project structure (`godot/`) was imported from
[nikbearbrown/walker-jumpman](https://github.com/nikbearbrown/walker-jumpman) at commit `9387542`
("Add Walker Jumpman playable First Steps prototype"). Only the engine project was copied; the starter's
design documents describe a different game and are not included. See [SOURCES.md](SOURCES.md).

## Engine

Godot **4.7.2.stable.official.ed1daf0bf**, GDScript, Compatibility renderer, 640×360 viewport.

## Run

```
godot --path godot
```

Or import `godot/project.godot` in the Godot editor and press F5.

Tests (headless):

```
godot --headless --path godot --script res://tests/test_game.gd
godot --headless --path godot --script res://tests/test_keyboard.gd
```

## Controls

_TBD — the slice's controls, including separate music / effects mute keys._

## What the slice demonstrates

_TBD._

## Design documents

| Document | Purpose |
|---|---|
| CONCEPT.md | _TBD_ — the game in one page |
| STORYBOARD.md | _TBD_ — the play experience, panel by panel |
| CHARACTER-SHEET.md | _TBD_ — the contract the generated character must meet |
| CHANGE-BRIEF.md | _TBD_ — asset list, event-to-sound map, predicted failures |
| [SOURCES.md](SOURCES.md) | Credits, models and licenses, asset log |
| [FRICTIONAL.md](FRICTIONAL.md) | Dated log of design decisions |
| TEST-REPORT.md | _TBD_ |

## Known limitations

_TBD._

## Final film

_TBD — filename, link to course media storage, SHA-256._
