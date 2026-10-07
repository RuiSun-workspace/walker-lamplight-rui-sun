extends SceneTree
## Evidence captures for TEST-REPORT.md (storyboard vs slice, character states). Must run WITHOUT --headless:
##   godot --fixed-fps 60 --path godot --script res://tests/capture_evidence.gd
## Real play: the route driver presses the same inputs a player would. "staged" in a file name means the
## script set state directly (oil, position) to reach that moment; the report labels those.
## Writes evidence/captures/<name>.png and evidence/captures/wick_positions.json (Wick's screen position).
const Game = preload("res://game/session.gd")
const Route = preload("res://tests/route_driver.gd")
var game: Node2D
var out: String
var wick_at := {}

func _initialize() -> void:
	call_deferred("run")

func steps(n: int) -> void:
	for i in range(n):
		await physics_frame
		await process_frame

func snap(name: String) -> void:
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(out + "/" + name + ".png")
	if is_instance_valid(game) and game.player:
		var s: Vector2 = game.get_viewport().get_canvas_transform() * game.player.global_position
		wick_at[name] = {"x": s.x, "y": s.y, "look": game.player.look, "flip": game.player.sprite.flip_h}
	print("captured ", name)

func fresh() -> void:
	if is_instance_valid(game):
		game.queue_free()
		await process_frame
	game = Game.new()
	game.test_mode = true
	root.add_child(game)
	await steps(3)

func run() -> void:
	out = ProjectSettings.globalize_path("res://../evidence/captures")
	DirAccess.make_dir_recursive_absolute(out)
	# P1: title screen (real)
	await fresh()
	await snap("sb1-title")
	# Real play along the full route, capturing moments as they happen
	game.start_session()
	game.player.test_control = true
	await steps(20)
	await snap("sb2-first-frame")
	await snap("state-idle-right")
	var route = Route.new()
	var got := {}
	var picked := {"n": 0}  # a dictionary: GDScript lambdas capture plain locals by value
	game.oil_collected.connect(func(_i): picked["n"] += 1)
	var t := 0
	while game.state == Game.State.PLAYING and t < 4000:
		route.step(game.player)
		await steps(1)
		t += 1
		var p = game.player
		if not got.has("walk") and p.look == "walk" and p.position.x > 500:
			got["walk"] = 1; await snap("state-walk-right")
		if not got.has("jump") and p.look == "jump" and p.position.x > 880 and p.position.x < 960:
			got["jump"] = 1; await snap("sb3-jump"); await snap("state-jump")
		if not got.has("fall") and p.look == "fall" and p.position.x > 960 and p.position.x < 1060:
			got["fall"] = 1; await snap("state-fall")
		if not got.has("pickup") and picked["n"] >= 1 and p.look == "pickup":
			got["pickup"] = 1; await snap("sb4-pickup"); await snap("state-pickup")
		if not got.has("climb") and p.climbing and p.position.y < 1150:
			got["climb"] = 1; await snap("state-climb")
		if not got.has("left") and p.look == "walk" and p.facing < 0 and p.position.y < 1000 and p.position.x < 2600:
			got["left"] = 1; await snap("state-walk-left")
	for i in range(30):
		await steps(1)
	await snap("sb8-exit-complete")
	await snap("state-celebrate")
	# P5: ember (staged: oil set to 0 in the bottom tunnel)
	await fresh()
	game.start_session()
	game.player.test_control = true
	game.player.test_axis = 1
	await steps(70)
	game.player.test_axis = 0
	game.oil = 0.0
	await steps(90)
	await snap("sb5-staged-ember")
	await snap("state-staged-ember")
	# P6 / P7: death on the pit spikes (staged: placed in the pit), then the real respawn at the lamp post
	game.oil = 100.0
	game.player.position = Vector2(970, 1380)
	await steps(4)
	await snap("sb6-staged-died-flash")
	await snap("state-staged-hurt")
	while game.state == Game.State.DYING:
		await steps(1)
	await steps(20)
	await snap("sb7-restart-at-lamp-post")
	var f := FileAccess.open(out + "/wick_positions.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(wick_at, "  "))
	f.close()
	game.queue_free()
	await process_frame
	quit()
