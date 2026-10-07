#!/usr/bin/env bash
# Turn the picked pose outputs into 64x80 state sprites with the CHAR-REF pipeline (Claude, 2026-10-07).
# Scale 0.07104 = 66 / 929, the scale CHAR-REF was reduced with, so every body matches the reference.
#   bash tools/gen/poses_round1_process.sh
set -euo pipefail
PY=F:/7270/film-env/Scripts/python.exe
RAW=F:/7270/a2-gen/gen-raw
SCALE=0.07104

# id            pick  face   (face pattern per CHARACTER-SHEET state)
while read -r ID PICK FACE; do
  low=$(echo "${ID#CHAR-}" | tr 'A-Z' 'a-z')
  "$PY" tools/gen/pixelize.py "$RAW/$ID/$ID-s1012-$PICK.png" --frame 64 80 --scale $SCALE \
      --out "design/generation/pixelized/$ID-s1012-$PICK-64x80.png" >/dev/null
  "$PY" tools/gen/face_edit.py "design/generation/pixelized/$ID-s1012-$PICK-64x80.png" --face "$FACE" --auto --top 0 \
      --out "design/generation/edited/$ID-s1012-$PICK-64x80-$FACE.png" >/dev/null
  "$PY" tools/gen/normalize_sprite.py "design/generation/edited/$ID-s1012-$PICK-64x80-$FACE.png" \
      --out "design/generation/accepted/$ID.png" | sed "s/^/$ID /"
done < <(grep -v "^#" <<'EOF'
CHAR-WALK      b3 oval
CHAR-JUMP      b1 wide
CHAR-FALL      b3 wide
CHAR-PICKUP    b2 grin
CHAR-EMBER     b2 lid
#CHAR-HURT      b1 x   # round 1: orange flame quantises to brass; see HURT round 2 below
CHAR-CELEBRATE b2 joy
CHAR-CLIMB     b0 none
EOF
)

# HURT round 2 (seed 1014, red flame): pick b1
"$PY" tools/gen/face_edit.py design/generation/pixelized/CHAR-HURT-s1014-b1-64x80.png --face x --auto --top 0 \
    --out design/generation/edited/CHAR-HURT-s1014-b1-64x80-x.png >/dev/null
"$PY" tools/gen/normalize_sprite.py design/generation/edited/CHAR-HURT-s1014-b1-64x80-x.png \
    --out design/generation/accepted/CHAR-HURT.png | sed "s/^/CHAR-HURT /"
