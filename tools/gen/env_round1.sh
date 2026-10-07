#!/usr/bin/env bash
# Environment assets, round 1 (written by Claude, 2026-10-07). txt2img with SDXL base 1.0, same flat
# cartoon style as Wick. Rock is asked to be dark and cold blue so Wick's brass frame stays readable
# (CHANGE-BRIEF F2: brass is only 2.1:1 against warm lit rock).
#   bash tools/gen/env_round1.sh
set -euo pipefail
for i in $(seq 1 60); do curl -s -o /dev/null http://127.0.0.1:8188/system_stats && break; sleep 3; done  # wait for ComfyUI
PY=F:/7270/a2-gen/venv/Scripts/python.exe
STYLE="flat 2D cartoon illustration, game art, bold clean dark outline, flat cel shading with one highlight and one shadow tone, simple shapes"
NEG="photo, realistic, 3d render, blurry, gradient, text, letters, watermark, signature, people, character, creature, face, lantern, light rays, glow, bloom, pixel art, frame, border"

gen() {  # id seed width height prompt [extra-negative]
  "$PY" tools/gen/comfy_generate.py --id "$1" --seed "$2" --batch 4 --width "$3" --height "$4" \
    --prompt "$STYLE, $5" --negative "$NEG${6:+, $6}" --note "environment round 1" | tail -1
}

gen ENV-BG       2001 1344 768  "game background, inside a dark abandoned mine tunnel, rough wet slate-blue rock wall, a few old wooden pit props and beams, deep shadows, cold dark blue palette, side view, wide horizontal composition, empty scene" "sky, bright, sunlight"
gen ENV-TILE     2002 1024 1024 "texture of rough dark slate-blue rock, cracked stone blocks, flat even lighting, uniform pattern filling the whole image, seamless tileable texture, no objects" "perspective, horizon, white background"
gen ENV-TILE-TOP 2003 1024 1024 "side view of the top edge of a rock ledge in a mine, a flat walkable top surface with a lighter worn stone rim, dark slate-blue rock below, game platform, plain white background" "perspective, grass"
gen ENV-SPIKE    2004 1024 1024 "game hazard, a row of four sharp steel spikes pointing straight up on a dark metal base, side view, cold grey steel with a bright edge highlight, plain white background" "blood, rust"
gen ENV-OIL      2005 1024 1024 "game pickup item, a single drop of thick golden amber lamp oil, teardrop shape with a small white highlight, centered, plain white background" "many drops, splash, bottle"
gen ENV-LADDER   2006 1024 1024 "game prop, an old wooden mine ladder, straight front view, two vertical rails and evenly spaced rungs, plain white background" "perspective, wall"
gen ENV-LAMPPOST 2007 1024 1024 "game prop, an old iron mine lamp post with a small hanging oil lamp at the top, side view, tall and thin, plain white background" "light rays, character"
