extends RefCounted
## Fixed input route through the real level. No position/velocity edits.
## Lower tunnel (step 2): hop onto the step, clear the spike pit, hop onto the oil ledge, walk to the ladder.
var jump_marks: Array[float] = [250.0, 846.0, 1170.0]
var next_jump: int = 0
var stop_x: float = 1790.0

func step(player: CharacterBody2D) -> void:
	player.test_control = true
	player.test_axis = 1.0 if player.position.x < stop_x else 0.0
	player.test_jump_held = false
	if next_jump < jump_marks.size() and player.position.x >= jump_marks[next_jump] and player.is_on_floor():
		player.test_jump_pressed = true
		next_jump += 1
