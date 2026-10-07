#!/usr/bin/env bash
# Derive Wick's state poses from the accepted reference set-up (written by Claude, 2026-10-07).
# Same prompt P6 as CHAR-REF 1012, same seed 1012, same denoise 0.75; only the pose sentence and the
# init image (the character-sheet pose, design/generation/init/char-<pose>-init.png) change.
# Run from the repo root with ComfyUI up:  bash tools/gen/poses_round1.sh
set -euo pipefail
PY=F:/7270/a2-gen/venv/Scripts/python.exe
HEAD="flat 2D cartoon illustration of a single cute brass lantern creature, game character design, bold clean dark outline, flat cel shading with one highlight and one shadow tone, round ring handle on top, flat brass cap, tapered dark glass body narrower at the bottom with two thin cage bars"
TAIL="short thin brass stick legs, thin brass stick arms, full body, simple shapes, centered, plain white background"
NEG="pixel art, pixelated, realistic, photo, 3d render, blurry, gradient, drop shadow, text, letters, watermark, signature, multiple objects, many lanterns, character sheet, pattern, human, animal, ears, robot, armor, helmet, face on the lantern body, one eye, cyclops, angry, green glass, extra limbs, dripping, fire on the handle, glow, bloom, checkerboard"
FLAME="a big yellow teardrop flame inside the glass, the flame has a cute friendly face with two round black eyes side by side and a small smile"

run() {  # id pose-file pose-sentence flame-sentence
  "$PY" tools/gen/comfy_generate.py --id "$1" --seed 1012 --batch 4 --denoise 0.75 \
    --init "design/generation/init/char-$2-init.png" \
    --prompt "$HEAD, $4, $TAIL, $3, three-quarter view facing right" --negative "$NEG" \
    --note "poses round 1: P6 + pose sentence, seed/denoise as CHAR-REF 1012, init = sheet pose '$2'" | tail -1
}

run CHAR-WALK      walk      "walking mid stride, one leg forward and one back, one arm swinging"              "$FLAME"
run CHAR-JUMP      jump      "jumping upward, both arms raised, legs tucked up"                                 "$FLAME"
run CHAR-FALL      fall      "falling down, both arms spread out to the sides, legs dangling, surprised"        "a tall stretched yellow flame inside the glass with two wide round black eyes"
run CHAR-PICKUP    pickup    "reaching forward with one arm to grab something, delighted"                       "a big bright yellow flame rising up above the cap, the flame has a happy face with two black eyes and a wide smile"
run CHAR-EMBER     ember     "walking slowly, tired"                                                            "only a tiny dim red-orange ember at the bottom of the glass instead of a flame, the ember has two sleepy half-closed eyes"
run CHAR-HURT      hurt      "knocked backwards and tilted, arms flailing, hurt"                                "an orange flame blown to one side inside the glass, the flame has dizzy cross-shaped eyes"
run CHAR-CELEBRATE celebrate "both arms raised high in celebration, joyful"                                     "a big tall yellow flame rising above the cap, the flame has happy closed eyes and a big smile"
"$PY" tools/gen/comfy_generate.py --id CHAR-CLIMB --seed 1012 --batch 4 --denoise 0.75 \
  --init design/generation/init/char-climb-init.png \
  --prompt "$HEAD, a yellow flame inside the glass, $TAIL, seen from behind, back view, no face visible, both arms raised as if climbing a ladder, one leg raised" \
  --negative "$NEG, face, eyes" --note "poses round 1: climb is the back view (sheet pose 12); face/eyes in the negative" | tail -1

# HURT round 2 (2026-10-07): round-1 flames were orange (~230,135,55), which is nearer brass than the
# sheet's ember red in Lab, so the whole flame quantised to brass. Ask for a red flame instead.
"$PY" tools/gen/comfy_generate.py --id CHAR-HURT --seed 1014 --batch 4 --denoise 0.75 \
  --init design/generation/init/char-hurt-init.png \
  --prompt "$HEAD, a small deep red flame blown to one side inside the glass, the red flame has dizzy cross-shaped eyes, $TAIL, knocked backwards and tilted, arms flailing, hurt, three-quarter view facing right" \
  --negative "$NEG, orange flame, yellow flame" --note "HURT round 2: red flame so it quantises to the ember colour, new seed 1014" | tail -1
