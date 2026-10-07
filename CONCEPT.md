# Lamplight — concept (v1, 2026-10-03)

## The game in two sentences

You are **Wick**, a small walking lantern spirit lost deep in an abandoned mine, and your flame is both your
life and your only light. Run and jump through the dark tunnels toward the daylight at the mine's exit,
grabbing oil drops to keep burning before the dark swallows what you can see.

## Core loop

- **Repeat:** move to the edge of what your light shows → read the next stretch of tunnel → jump.
- **Decide each time:** take the detour to an oil drop (costs time, which costs oil) or push straight on
  toward the exit with less light.
- **Risk:** oil drains every second. As it drops, your light radius shrinks; at zero your flame becomes an
  ember and you can still move, but you can barely see the spikes and gaps. Touching spikes or falling
  sends you back to the last lamp post (checkpoint).

## Design pillars

| Pillar | What it means for the player | Visual choice that honors it | Sound choice that honors it |
|---|---|---|---|
| **Light is life** | How much you can see *is* how much oil you have. | The light radius around Wick shrinks with oil; Wick's own flame is drawn smaller in the low-oil state image. | The music loses brightness (low-pass) as oil drops. |
| **Every second burns** | There is always a quiet pressure to keep moving. | A flame-shaped oil gauge in the corner that visibly shortens. | A low pulse layer in the music that the player hears under everything. |
| **Fair in the dark** | When you fail, it is because you misjudged, not because something was invisible. | Spikes carry a faint cold glint that shows even outside the light; the hazard that killed you flashes on death. | The spike hit sound is sharp and different from every other sound, so failure is never ambiguous. |
| **The way out glows** | You always know which way is forward. | The exit is a shaft of pale daylight, the only cool-white light in a warm-and-black world. | At the exit the music resolves and stops. |

## Art direction

Pixel art at a 640×360 viewport, a deliberately small palette, and hard pixel edges imported with the
Nearest filter. A tiny character in a big dark space is the whole feeling of the game, and pixel art keeps
Wick readable at about 24×32 on-screen pixels where a smooth illustration would turn to mush; one shared
palette across every pose also keeps the generated images consistent.

Reference notes (words, not artists):
- **Materials:** wet slate-blue rock, rotten timber pit props, tarnished brass lantern, thick amber oil.
- **Lighting:** a single warm point light in near-black; the only other light is cold, pale daylight at
  the exit.
- **Era and mood:** an old hand-dug mine abandoned long ago; damp, cramped, quiet, slightly dangerous.

## Audio direction

The player should feel **tense but in control**: a steady pulse that says "keep going" rather than
"panic". Sound effects are short and dry so each one lands on its event.

| Moment | Music |
|---|---|
| Normal play, oil healthy | Loop plays at full brightness. |
| Oil getting low | Same loop, increasingly muffled (low-pass) — the world closes in. |
| Ember (oil empty) | Muffled down to almost only the pulse. |
| Failure (spikes / fall) | Music dips for the respawn and returns on retry. |
| Pause | Music pauses; resumes from the same point. |
| Exit reached (end of session) | Music stops; the success sound plays on its own. |

## Scope of the Assignment 2 slice

One short tunnel: start, a few jumps, at least one oil drop, one spike hazard, one checkpoint lamp post,
and the exit. Controllable Wick with static state images, one looping music track, four event sounds,
and separate music / effects mute keys. The full game (more tunnels, more hazard types) is out of scope here.

## Revision log

- **2026-10-06 (Rui):** the slice scope grows from "one short tunnel" to a lower and an upper tunnel
  joined by a **ladder** (from the hand-drawn storyboard P1); climbing becomes a verb. When the oil runs out
  the light shrinks to **a very small ring around Wick's body**, never fully dark. The ending is
  **outdoors** in daylight (storyboard P8). The text above is the v1 record and is left unchanged.
- **2026-10-07 (Rui, after playtesting step 4):** the ember was too safe. Rui still saw every spike
  in the dark and could keep playing indefinitely at zero oil, so darkness carried no risk. **At zero
  oil the ember now burns out after 8 seconds (a failure, back to the last lamp post)**, and oil drains
  at 6/s instead of 4/s. The spikes' faint glint stays, so "Fair in the dark" is kept; the risk now
  comes from time ("Every second burns") instead of from hiding the hazards.
