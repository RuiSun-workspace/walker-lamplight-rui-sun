extends SceneTree
## Oil, light, ember and lamp-post rules (CHANGE-BRIEF section 4, storyboard P2, P4, P5, P7).
## Positions are only set to start a fixture; behaviour is driven by test inputs and real physics ticks.
const Game = preload("res://game/session.gd")
var game: Node2D
var results: Array[Dictionary] = []
var failures := 0
var counts := {"oil_collected": 0, "died": 0, "respawned": 0}
var oil_at_respawn: float = -1.0

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

func fresh(at := Vector2.ZERO) -> void:
	if is_instance_valid(game):
		game.queue_free()
		await process_frame
	game = Game.new()
	game.test_mode = true
	root.add_child(game)
	game.start_session()
	game.player.test_control = true
	for k in counts:
		counts[k] = 0
	game.oil_collected.connect(func(_i): counts["oil_collected"] += 1)
	game.died.connect(func(): counts["died"] += 1)
	game.respawned.connect(func():
		counts["respawned"] += 1
		oil_at_respawn = game.oil)
	if at != Vector2.ZERO:
		game.player.position = at
	await steps(2)

func run() -> void:
	await fresh()
	# drains from the first tick, so "full" means exactly 100 - 4 x elapsed (the first version checked == 100 two ticks in)
	check("oil-starts-full", absf(game.oil - (100.0 - game.OIL_DRAIN * game.elapsed)) < 0.001, {"oil": game.oil, "elapsed": game.elapsed})
	var before: float = game.oil
	await steps(60)
	check("drain-6-per-second", absf((before - game.oil) - 6.0) < 0.3, {"drained_in_60_ticks": before - game.oil})
	game.set_paused(true)
	var paused_oil: float = game.oil
	await steps(60)
	check("no-drain-while-paused", game.oil == paused_oil, {"oil": game.oil})
	game.set_paused(false)
	# Pickup on the oil ledge (drop 0 at 1320,520; ledge top y 560)
	await fresh(Vector2(1260, 560))
	game.oil = 50.0
	game.player.test_axis = 1
	var t := 0
	while counts["oil_collected"] == 0 and t < 60:
		await steps(1)
		t += 1
	game.player.test_axis = 0
	check("pickup-adds-35", counts["oil_collected"] == 1 and game.collected[0] and absf(game.oil - 85.0) < 1.0, {"oil": game.oil, "signals": counts["oil_collected"]})
	await steps(1)
	check("pickup-look", game.player.look == "pickup", {"look": game.player.look})
	await steps(40)
	check("pickup-look-ends", game.player.look != "pickup", {"look": game.player.look})
	await steps(30)
	check("standing-on-drop-no-repeat", counts["oil_collected"] == 1, {"signals": counts["oil_collected"]})
	await fresh(Vector2(1260, 560))
	game.player.test_axis = 1
	await steps(30)
	check("pickup-capped-at-100", counts["oil_collected"] == 1 and game.oil <= 100.0, {"oil": game.oil})
	# Light follows the oil; never fully dark (Rui 2026-10-06)
	var radii := {}
	for o in [100, 50, 0]:
		game.oil = float(o)
		game.lighting.snap_radius()
		radii[o] = game.lighting.wick_radius
	check("light-radius-follows-oil", radii[100] > radii[50] and radii[50] > radii[0] and absf(radii[0] - 56.0) < 0.5 and absf(radii[100] - 240.0) < 0.5, {"radii": radii})
	# Ember image at zero oil, on the ground; climb image wins on a ladder
	await fresh()
	game.oil = 0.0
	await steps(3)
	check("ember-look-at-zero", game.player.look == "ember" and game.state == Game.State.PLAYING, {"look": game.player.look, "state": game.state})
	check("still-playing-at-zero", game.state == Game.State.PLAYING, {"state": game.state})
	await fresh(Vector2(1819, 640))
	game.oil = 0.0
	game.player.test_climb_axis = -1
	await steps(6)
	check("climb-look-beats-ember", game.player.look == "climb", {"look": game.player.look})
	# Ember burns out (Rui playtest 2026-10-07): 8 s at zero oil is a failure; a drop in time resets it
	await fresh()
	game.oil = 0.0
	await steps(60 * 5)
	var r_mid: float = game.lighting.wick_radius
	check("ember-ring-shrinks", r_mid < 56.0 and r_mid > 28.0 and game.state == Game.State.PLAYING, {"radius_after_5s": r_mid})
	await steps(60 * 3 + 5)
	check("ember-burns-out-after-8s", game.state == Game.State.DYING and counts["died"] == 1 and game.death_reason == "Your flame went out" and game.killer_hazard == -1, {"state": game.state, "reason": game.death_reason})
	await fresh(Vector2(1260, 560))
	game.oil = 0.0
	await steps(60 * 5)
	game.player.test_axis = 1
	t = 0
	while counts["oil_collected"] == 0 and t < 60:
		await steps(1)
		t += 1
	game.player.test_axis = 0
	await steps(60 * 4)
	check("drop-in-time-saves-the-ember", game.state == Game.State.PLAYING and counts["died"] == 0 and game.ember_time == 0.0, {"state": game.state, "oil": game.oil})
	# Lamp post checkpoint (P7): touch post 2, collect drop 1, die on the upper spikes, come back
	await fresh(Vector2(1980, 360))
	game.player.test_axis = 1
	await steps(4)
	game.player.test_axis = 0
	check("lamp-post-saves", game.checkpoint == 1, {"checkpoint": game.checkpoint, "saved_oil": game.checkpoint_oil})
	var saved: float = game.checkpoint_oil
	game.player.position = Vector2(2650, 360)
	await steps(2)
	game.player.test_jump_pressed = true
	t = 0
	while counts["oil_collected"] == 0 and t < 40:
		await steps(1)
		t += 1
	check("floating-drop-reachable-by-jump", counts["oil_collected"] == 1 and game.collected[1], {"signals": counts["oil_collected"], "ticks": t})
	await steps(40)
	game.player.position = Vector2(2448, 350)
	await steps(3)
	check("killer-hazard-recorded", game.state == Game.State.DYING and game.killer_hazard == 1, {"state": game.state, "killer": game.killer_hazard})
	await steps(40)
	check("respawn-at-lamp-post", game.state == Game.State.PLAYING and game.player.position.distance_to(Vector2(2040, 360)) < 1.0, {"pos": str(game.player.position)})
	# measured at the moment of respawn (the first version compared after ~6 more ticks of normal drain)
	check("respawn-restores-saved-oil-and-drop", oil_at_respawn == saved and not game.collected[1], {"oil_at_respawn": oil_at_respawn, "saved": saved, "drop1_collected": game.collected[1]})
	check("died-and-respawned-once", counts["died"] == 1 and counts["respawned"] == 1, {"counts": counts})
	game.restart_attempt()
	check("r-restart-is-not-death", game.deaths == 1 and counts["died"] == 1 and game.checkpoint == 1, {"deaths": game.deaths})
	# A new run resets everything
	game.player.position = Vector2(3120, 360)
	await steps(3)
	game.start_session()
	check("new-run-resets", game.checkpoint == 0 and is_equal_approx(game.oil, 100.0) and not game.collected.has(true) and game.player.position.distance_to(Vector2(128, 640)) < 1.0, {"checkpoint": game.checkpoint, "oil": game.oil})
	var out := ProjectSettings.globalize_path("res://../evidence")
	DirAccess.make_dir_recursive_absolute(out)
	var file := FileAccess.open(out + "/oil-" + str(Time.get_unix_time_from_system()) + ".json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"scope": "Oil, light, ember, lamp posts; scripted inputs, not human playtesting", "engine": Engine.get_version_info().string, "results": results, "failures": failures}, "  "))
	file.close()
	print("OIL TESTS: %d checks / %d failures" % [results.size(), failures])
	game.queue_free()
	await process_frame
	quit(1 if failures else 0)
