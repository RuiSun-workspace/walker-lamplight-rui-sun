extends RefCounted
## Fixed input route through the real level (v2, three tunnels), driven by the observed player position.
## Only the inputs a player would press: no position or velocity edits.
## Each leg: walk in `dir`, press Jump when passing each mark (on the floor), then hand over to a climb.
const LEGS := [
	{"name": "bottom", "dir": 1.0, "marks": [250.0, 846.0, 1170.0, 1560.0, 1790.0, 2240.0, 2545.0], "ladder": 0},
	{"name": "middle", "dir": -1.0, "marks": [2510.0, 2040.0, 1630.0, 1237.0, 1030.0], "ladder": 1},
	{"name": "top", "dir": 1.0, "marks": [846.0, 1240.0, 1345.0, 1750.0, 2440.0], "ladder": -1},
]
var leg: int = 0
var next_jump: int = 0
var climbing_phase: bool = false
var jumps_pressed: int = 0
var phase: String = "bottom"
var ladders: Array = []

func step(player: CharacterBody2D) -> void:
	player.test_control = true
	player.test_jump_held = false
	player.test_climb_axis = 0.0
	if ladders.is_empty():
		ladders = player.ladders
	var l: Dictionary = LEGS[leg]
	if climbing_phase:
		var lad: Rect2 = ladders[l.ladder]
		player.test_axis = 0.0
		player.test_climb_axis = -1.0
		if player.climbing and player.position.y <= lad.position.y - 5.0:
			climbing_phase = false
			leg += 1
			next_jump = 0
			phase = LEGS[leg].name
			player.test_axis = LEGS[leg].dir
		return
	var dir: float = l.dir
	player.test_axis = dir
	var marks: Array = l.marks
	if next_jump < marks.size() and player.is_on_floor() and (player.position.x - marks[next_jump]) * dir >= 0.0:
		player.test_jump_pressed = true
		next_jump += 1
		jumps_pressed += 1
	if l.ladder >= 0 and next_jump >= marks.size():
		var lad: Rect2 = ladders[l.ladder]
		var centre := lad.position.x + lad.size.x / 2.0
		if absf(player.position.x - centre) <= 8.0 and player.is_on_floor():
			player.test_axis = 0.0
			climbing_phase = true
			phase = l.name + "-climb"
