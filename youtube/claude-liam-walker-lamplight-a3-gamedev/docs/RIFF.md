# RIFF — what the commentary rests on (inspected output, not imagined play)

- "The numbers were right. The look was not." The oil drop's 0.15 m is exactly 24 px at 160 px/m and passed every
  check; Rui still found it too small in the room (TEST-REPORT §7, cycle 4).
- "Every size is read back from the vertices, because the scene report rounds to two decimals." `get_scene_info`
  printed 0.06 for a 0.0625 m post (build_lamp_post.py, step 1 notes).
- "Reading the edit back caught something else." The read-back found `lp_glass` at `#241c54`; Rui had not meant it.
- "A check that only measured the asset would prove nothing about the floor." The Module 3 example; here the
  check reads the Floor node's own box, and a 5 cm lift was shown to fail it.
- "Each one failed." Recorded in `capture/test-output.txt`, re-run in throw-away copies for this film.
