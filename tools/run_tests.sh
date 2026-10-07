#!/usr/bin/env bash
# Run every headless test suite and fail on ANY script error, not only on failed checks.
# Written 2026-10-07 after a compile error in audio_director.gd still printed "0 failures":
# when a script fails to load, Godot keeps going and the suites' own counters can look green.
#   bash tools/run_tests.sh
set -u
G="${GODOT:-/c/Users/18500/Desktop/7270/godot-4.7.2/Godot_v4.7.2-stable_win64_console.exe}"
cd "$(dirname "$0")/../godot"
status=0
for t in test_game test_keyboard test_wick test_oil test_audio; do
  [ -f "tests/$t.gd" ] || continue
  # --fixed-fps 60: exactly one physics tick per frame. Without it a fast headless run decides from real
  # time how many physics ticks fit in a frame, so "wait 2 frames" was sometimes 1 extra tick (found by
  # the F5 muted-vs-sound trace check: same positions, oil 0.1 apart = one 6/s tick).
  out=$(timeout 600 "$G" --headless --fixed-fps 60 --path . --script "res://tests/$t.gd" 2>&1); code=$?
  pass=$(grep -c '"status":"PASS"' <<<"$out"); fail=$(grep -c '"status":"FAIL"' <<<"$out")
  errs=$(grep -c 'SCRIPT ERROR' <<<"$out")
  verdict=OK
  if [ "$code" -ne 0 ] || [ "$fail" -ne 0 ] || [ "$errs" -ne 0 ] || [ "$pass" -eq 0 ]; then verdict=FAILED; status=1; fi
  printf '%-14s pass=%-3s fail=%-3s script_errors=%-3s exit=%-3s %s\n' "$t" "$pass" "$fail" "$errs" "$code" "$verdict"
  if [ "$verdict" = FAILED ]; then grep -E '"status":"FAIL"|SCRIPT ERROR|at: res' <<<"$out" | head -8; fi
done
exit $status
