extends RefCounted
## Fixed input route through the real level, driven by the observed player position.
## No position/velocity edits: only the same inputs a player would press.
## lower tunnel -> climb the ladder -> step onto the upper floor -> clear the upper spikes -> exit.
var jump_marks: Array[float] = [250.0, 846.0, 1170.0, 2320.0]
var next_jump: int = 0
var phase: String = "lower"
var ladder_x: float = 1808.0
var ladder_top: float = 360.0

func step(player: CharacterBody2D) -> void:
	player.test_control = true
	player.test_jump_held = false
	player.test_climb_axis = 0.0
	match phase:
		"lower":
			player.test_axis = 1.0
			if player.position.x >= ladder_x - 8.0 and player.is_on_floor() and next_jump >= 3:
				player.test_axis = 0.0
				phase = "climb"
		"climb":
			player.test_axis = 0.0
			player.test_climb_axis = -1.0
			if player.climbing and player.position.y <= ladder_top - 5.0:
				phase = "upper"
		"upper":
			player.test_axis = 1.0
	if next_jump < jump_marks.size() and player.position.x >= jump_marks[next_jump] and player.is_on_floor():
		player.test_jump_pressed = true
		next_jump += 1
