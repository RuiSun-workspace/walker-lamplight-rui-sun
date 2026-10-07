extends SceneTree
## Film capture driver (explainer film, 2026-10-07). Drives the REAL game through Godot's Input actions,
## exactly the path a keyboard takes (Input.action_press / action_release); nothing sets the player's
## position, velocity or test fields during a take. The decisions (when to jump / climb) come from the
## same position-driven route the tests use (tests/route_driver.gd); this driver only turns them into
## Input actions. Every press/release is logged against the physics tick.
##
## Run on an ISOLATED copy whose project.godot overrides the window to 3840x2160 (3x the 1280x720 viewport):
##   godot --path <copy>/godot --disable-vsync --fixed-fps 30 --write-movie <dir>/f.png \
##         --script res://tests/capture_film.gd -- --take run-01
## Takes:
##   run-01  title -> Enter -> full route through all three tunnels -> exit -> end card
##   run-02  title -> Enter -> walk right and jump LATE at the first spike pit -> real death -> respawn
##   run-03  title -> Enter -> stand still: oil drains, ember, burn-out after 4 s -> respawn
## The script quits non-zero if the take's expected result does not happen.
const Game = preload("res://game/session.gd")
const Route = preload("res://tests/route_driver.gd")
var game: Node2D
var take: String = "run-01"
var log_lines: Array[String] = []
var tick: int = 0
var held := {}

func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var i := args.find("--take")
	if i >= 0 and i + 1 < args.size():
		take = args[i + 1]
	call_deferred("run")

func press(action: String) -> void:
	if not held.get(action, false):
		Input.action_press(action)
		held[action] = true
		log_lines.append(JSON.stringify({"tick": tick, "press": action, "x": game.player.position.x, "y": game.player.position.y}))

func release(action: String) -> void:
	if held.get(action, false):
		Input.action_release(action)
		held[action] = false
		log_lines.append(JSON.stringify({"tick": tick, "release": action}))

func set_axis(neg: String, pos: String, v: float) -> void:
	if v > 0.0:
		release(neg); press(pos)
	elif v < 0.0:
		release(pos); press(neg)
	else:
		release(neg); release(pos)

func tap_key(code: Key) -> void:
	var e := InputEventKey.new()
	e.keycode = code
	e.physical_keycode = code
	e.pressed = true
	Input.parse_input_event(e)
	log_lines.append(JSON.stringify({"tick": tick, "key": OS.get_keycode_string(code)}))
	await physics_frame
	tick += 1
	e = e.duplicate()
	e.pressed = false
	Input.parse_input_event(e)

func ticks(n: int) -> void:
	for k in range(n):
		await physics_frame
		tick += 1

func release_all() -> void:
	for a in held.keys():
		release(a)

func run() -> void:
	game = Game.new()
	root.add_child(game)
	await ticks(60)                       # title screen, 1 s
	await tap_key(KEY_ENTER)
	var ok := false
	if take == "run-01":
		var route = Route.new()
		# Like a person: real Input arrives one tick late (is_action_just_pressed is true on the tick after
		# the press). Chaining a jump straight off a landing at full speed then needs frame-perfect timing
		# between the middle tunnel's two spike strips (found 2026-10-07: the test hooks have no such delay).
		# So after a landing, a requested jump waits until Wick has settled for SETTLE ticks with no
		# horizontal input, then jumps in the route's direction.
		const SETTLE := 8
		var was_floor := true
		var landed_at := -100
		var pending := false
		while game.state == Game.State.PLAYING and tick < 6000:
			await physics_frame
			tick += 1
			var p = game.player
			if p.is_on_floor() and not was_floor:
				landed_at = tick
			was_floor = p.is_on_floor()
			route.step(p)                     # decides; writes intents into the player's test fields
			p.test_control = false            # ...but the player reads real Input, not those fields
			var axis: float = p.test_axis
			if p.test_jump_pressed and tick - landed_at < SETTLE:
				pending = true
			if pending and tick - landed_at < SETTLE:
				axis = 0.0
			var jump_now: bool = (p.test_jump_pressed and not pending) or (pending and tick - landed_at >= SETTLE)
			if jump_now:
				pending = false
			set_axis("move_left", "move_right", axis)
			set_axis("climb_up", "climb_down", p.test_climb_axis)
			if jump_now:
				press("jump")
			else:
				release("jump")
			p.test_jump_pressed = false
		release_all()
		ok = game.state == Game.State.COMPLETE and game.deaths == 0
		await ticks(180)                   # end card, 3 s, music stopped, exit sound plays out
	elif take == "run-02":
		press("move_right")
		while game.player.position.x < 250 and tick < 2000:   # hop the teaching step, like run-01
			await ticks(1)
		press("jump")
		await ticks(2)
		release("jump")
		while not game.player.is_on_floor() and tick < 2000:
			await ticks(1)
		while game.player.position.x < 715 and tick < 2000:   # jump too EARLY: lands inside the pit (~x 938)
			await ticks(1)
		press("jump")
		await ticks(2)
		release("jump")
		while game.state == Game.State.PLAYING and tick < 2000:
			await ticks(1)
		release_all()
		ok = game.state == Game.State.DYING and game.deaths == 1
		while game.state == Game.State.DYING and tick < 3000:
			await ticks(1)
		await ticks(90)                    # back at the lamp post, 1.5 s
		ok = ok and game.state == Game.State.PLAYING
	elif take == "run-03":
		while game.state == Game.State.PLAYING and tick < 4000:   # no input at all: oil drains, ember, burn-out
			await ticks(1)
		ok = game.state == Game.State.DYING and game.death_reason == "Your flame went out"
		while game.state == Game.State.DYING and tick < 5000:
			await ticks(1)
		await ticks(60)
	var out := ProjectSettings.globalize_path("res://../capture-logs")
	DirAccess.make_dir_recursive_absolute(out)
	var f := FileAccess.open(out + "/" + take + "-inputs.jsonl", FileAccess.WRITE)
	for line in log_lines:
		f.store_line(line)
	f.store_line(JSON.stringify({"tick": tick, "result_ok": ok, "state": game.state, "deaths": game.deaths, "oil": game.oil, "elapsed": game.elapsed}))
	f.close()
	print("TAKE %s ok=%s ticks=%d deaths=%d" % [take, ok, tick, game.deaths])
	quit(0 if ok else 1)
