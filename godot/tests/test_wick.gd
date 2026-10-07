extends SceneTree
## Wick's state images, facing and ladder (CHANGE-BRIEF F8). Inputs go through the player's test hooks;
## positions are only set to start a fixture, never during the behaviour under test.
const Game = preload("res://game/session.gd")
var game: Node2D
var results: Array[Dictionary] = []
var failures := 0
var jumped_count := 0

func _initialize() -> void:
	call_deferred("run")

func steps(n: int) -> void:
	for i in range(n):
		await physics_frame
		await process_frame

func check(id: String, passed: bool, observed: Dictionary) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed})
	if not passed:
		failures += 1
	print(JSON.stringify(results.back()))

func on_jumped() -> void:
	jumped_count += 1

func fresh(at := Vector2.ZERO) -> void:
	if is_instance_valid(game):
		game.queue_free()
		await process_frame
	game = Game.new()
	game.test_mode = true
	root.add_child(game)
	game.start_session()
	game.player.test_control = true
	game.player.jumped.connect(on_jumped)
	jumped_count = 0
	if at != Vector2.ZERO:
		game.player.position = at
	await steps(3)

func run() -> void:
	await fresh()
	var p = game.player
	var sizes_ok := true
	for k in p.LOOKS:
		sizes_ok = sizes_ok and p.LOOKS[k].get_size() == Vector2(64, 80)
	check("sprites-64x80-anchored", sizes_ok and p.sprite.position == Vector2(-32, -80) and not p.sprite.centered, {"sprite_position": str(p.sprite.position)})
	check("look-idle", p.look == "idle", {"look": p.look})
	p.test_axis = 1
	await steps(6)
	check("look-walk-right", p.look == "walk" and not p.sprite.flip_h, {"look": p.look, "flip": p.sprite.flip_h})
	p.test_axis = -1
	await steps(6)
	check("facing-left-flips", p.sprite.flip_h and p.facing < 0, {"flip": p.sprite.flip_h})
	p.test_axis = 0
	await steps(10)
	p.test_jump_pressed = true
	await steps(3)
	check("look-jump-rising", p.look == "jump" and p.velocity.y < 0, {"look": p.look, "vy": p.velocity.y})
	# rise lasts ~20 ticks (640 / 1920 s); the first version checked at tick 17, while still rising
	var w := 0
	while p.velocity.y <= 0 and w < 40:
		await steps(1)
		w += 1
	await steps(1)
	check("look-fall", p.look == "fall" and p.velocity.y > 0, {"look": p.look, "vy": p.velocity.y, "ticks_to_apex": w})
	# Ladder (F8)
	await fresh(Vector2(2852, 1320))
	p = game.player
	p.test_axis = -1
	await steps(2)
	p.test_axis = 0
	p.test_climb_axis = -1
	await steps(4)
	check("grab-ladder", p.climbing and p.look == "climb" and not p.sprite.flip_h, {"climbing": p.climbing, "look": p.look, "flip": p.sprite.flip_h})
	var t := 0
	while p.position.y > 956 and t < 300:
		await steps(1)
		t += 1
	var up_ticks := t
	await steps(10)
	check("climb-to-top-holds", p.climbing and absf(p.position.y - 954) < 3, {"y": p.position.y, "ticks": t})
	p.test_climb_axis = 0
	p.test_axis = -1  # v2: the middle tunnel is to the LEFT of the first ladder
	await steps(20)
	check("step-onto-upper-floor", not p.climbing and p.is_on_floor() and absf(p.position.y - 960) < 1 and p.position.x < 2848, {"pos": str(p.position)})
	await fresh(Vector2(2852, 1320))
	p = game.player
	p.test_climb_axis = -1
	await steps(40)
	p.test_climb_axis = 0
	var jumps_before: int = p.jumps
	p.test_jump_pressed = true
	await steps(2)
	check("jump-off-ladder-once", not p.climbing and p.jumps == jumps_before + 1 and jumped_count == 1, {"jumps": p.jumps, "jumped_signals": jumped_count})
	for i in range(10):
		p.test_jump_pressed = true
		await steps(2)
	check("mash-jump-on-ladder-no-extra", jumped_count == 1, {"jumped_signals": jumped_count})
	await fresh(Vector2(2852, 1320))
	p = game.player
	p.test_climb_axis = -1
	await steps(40)
	p.test_climb_axis = 1
	t = 0
	while p.climbing and t < 300:
		await steps(1)
		t += 1
	check("climb-down-to-floor", not p.climbing and p.is_on_floor() and absf(p.position.y - 1320) < 1, {"pos": str(p.position), "ticks": t})
	# Rui playtest 2026-10-07: getting down felt stuck. Down at the ladder top grabs; down is faster than up.
	await fresh(Vector2(2840, 960))  # standing on the middle floor's right edge, next to ladder 1
	p = game.player
	await steps(3)
	p.test_climb_axis = 1
	await steps(3)
	var grabbed_from_top: bool = p.climbing
	t = 0
	while p.climbing and t < 300:
		await steps(1)
		t += 1
	check("down-from-upper-floor", grabbed_from_top and not p.climbing and p.is_on_floor() and absf(p.position.y - 1320) < 1, {"grabbed": grabbed_from_top, "ticks_down": t, "pos": str(p.position)})
	check("down-faster-than-up", t > 0 and t < up_ticks, {"ticks_down_360px": t, "ticks_up": up_ticks, "up_speed": p.CLIMB_SPEED, "down_speed": p.CLIMB_DOWN_SPEED})
	# Event looks
	await fresh(Vector2(970, 1380))
	await steps(2)
	check("look-hurt-on-death", game.state == Game.State.DYING and game.player.look == "hurt", {"state": game.state, "look": game.player.look})
	await steps(40)
	check("look-cleared-on-respawn", game.state == Game.State.PLAYING and game.player.look == "idle", {"look": game.player.look})
	await fresh(Vector2(3100, 600))
	await steps(3)
	check("look-celebrate-on-exit", game.state == Game.State.COMPLETE and game.player.look == "celebrate", {"look": game.player.look})
	var out := ProjectSettings.globalize_path("res://../evidence")
	DirAccess.make_dir_recursive_absolute(out)
	var file := FileAccess.open(out + "/wick-" + str(Time.get_unix_time_from_system()) + ".json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"scope": "Wick state images, facing and ladder (F8); scripted inputs, not human playtesting", "engine": Engine.get_version_info().string, "results": results, "failures": failures}, "  "))
	file.close()
	print("WICK TESTS: %d checks / %d failures" % [results.size(), failures])
	game.queue_free()
	await process_frame
	quit(1 if failures else 0)
