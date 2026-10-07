extends SceneTree
## CHANGE-BRIEF F3 (one sound per event occurrence), F5 (muting never changes the game) and the music
## behaviour table. Counts come from the audio director's play_counts (every AudioStreamPlayer.play()
## call) compared with the game's own event counts. Scripted inputs, not a listening test: whether the
## sounds are right, and whether the loop seam is clean, is Rui's human check (TEST-REPORT).
const Game = preload("res://game/session.gd")
const Route = preload("res://tests/route_driver.gd")
var game: Node2D
var results: Array[Dictionary] = []
var failures := 0

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

func fresh(at := Vector2.ZERO, start := true) -> void:
	if is_instance_valid(game):
		game.queue_free()
		await process_frame
	game = Game.new()
	game.test_mode = true
	root.add_child(game)
	if start:
		game.start_session()
		game.player.test_control = true
		if at != Vector2.ZERO:
			game.player.position = at
	await steps(2)

func pc(id: String) -> int:
	return game.audio.play_counts[id]

func set_mute(on: bool) -> void:
	for b in [&"Music", &"SFX"]:
		AudioServer.set_bus_mute(AudioServer.get_bus_index(b), on)

func run() -> void:
	set_mute(false)
	# --- F3: jump ---
	await fresh()
	var p = game.player
	for i in range(3):                       # three separate real jumps
		p.test_jump_pressed = true
		await steps(45)
	p.test_jump_held = true                  # hold Space through landings
	p.test_jump_pressed = true
	await steps(120)
	p.test_jump_held = false
	await steps(30)
	for i in range(12):                      # mash Space: only jumps that actually start count
		p.test_jump_pressed = true
		await steps(3)
	await steps(40)
	check("jump-one-sound-per-jump", pc("jump") == p.jumps and p.jumps >= 4, {"jump_sounds": pc("jump"), "jumps": p.jumps})
	await fresh(Vector2(1819, 640))
	p = game.player
	p.test_climb_axis = -1
	await steps(40)
	p.test_climb_axis = 0
	for i in range(10):
		p.test_jump_pressed = true
		await steps(2)
	check("jump-off-ladder-mash-one-sound", pc("jump") == 1 and p.jumps == 1, {"jump_sounds": pc("jump"), "jumps": p.jumps})
	# --- F3: pickup ---
	await fresh(Vector2(1260, 560))
	game.player.test_axis = 1
	await steps(25)
	game.player.test_axis = 0
	await steps(90)                           # stand around on the spot
	check("pickup-one-sound-per-drop", pc("pickup") == 1 and game.collected.count(true) == 1, {"pickup_sounds": pc("pickup")})
	# --- F3: hurt ---
	await fresh(Vector2(970, 700))            # inside the spike pit
	await steps(3)
	game.resolve_contacts(true, true)          # a second fatal contact in the same window is ignored
	await steps(10)
	check("hurt-one-sound-per-death", pc("hurt") == 1 and game.deaths == 1, {"hurt_sounds": pc("hurt"), "deaths": game.deaths})
	await fresh(Vector2(970, 862))            # spike area AND below fall_y in the same tick
	await steps(3)
	check("spike-and-fall-same-tick-one-sound", pc("hurt") == 1 and game.deaths == 1, {"hurt_sounds": pc("hurt"), "deaths": game.deaths})
	await steps(40)
	game.player.position = Vector2(970, 700)
	await steps(50)
	check("hurt-again-after-respawn", pc("hurt") == 2 and game.deaths == 2, {"hurt_sounds": pc("hurt"), "deaths": game.deaths})
	# --- F3: exit ---
	await fresh(Vector2(3120, 360))
	await steps(90)                           # stand in the exit
	check("exit-one-sound", pc("exit") == 1 and game.state == Game.State.COMPLETE, {"exit_sounds": pc("exit")})
	var ev := InputEventAction.new()
	ev.action = "confirm"
	ev.pressed = true
	game._unhandled_input(ev)                  # Enter on the end card starts a new run, no exit sound
	await steps(10)
	check("replay-no-exit-sound", pc("exit") == 1 and game.state == Game.State.PLAYING, {"exit_sounds": pc("exit"), "state": game.state})
	# --- Music behaviour (CHANGE-BRIEF 3) ---
	await fresh(Vector2.ZERO, false)
	check("music-loop-enabled", game.audio.music.stream.loop == true, {"loop": game.audio.music.stream.loop})
	check("music-plays-on-title", game.audio.music.playing and game.state == Game.State.MENU, {"playing": game.audio.music.playing})
	game.start_session()
	game.player.test_control = true
	await steps(30)
	check("music-full-bright-at-start", game.audio.cutoff > 15000.0, {"cutoff": game.audio.cutoff})
	game.set_paused(true)
	await steps(5)
	check("music-pauses", game.audio.music.stream_paused, {"stream_paused": game.audio.music.stream_paused})
	game.set_paused(false)
	await steps(5)
	check("music-resumes", game.audio.music.playing and not game.audio.music.stream_paused, {"playing": game.audio.music.playing})
	game.oil = 20.0
	await steps(60)
	var low_cut: float = game.audio.cutoff
	check("music-muffles-with-low-oil", low_cut < 3000.0 and low_cut > 800.0, {"cutoff_at_20_oil": low_cut})
	game.oil = 0.0
	await steps(60)
	check("music-ember-mostly-pulse", game.audio.cutoff < 500.0 and game.audio.music.volume_db <= -3.9, {"cutoff": game.audio.cutoff, "volume_db": game.audio.music.volume_db})
	game.oil = 100.0
	game.player.position = Vector2(970, 700)
	await steps(8)
	check("music-ducks-on-death", game.audio.music.volume_db < -6.0 and game.audio.music.playing, {"volume_db": game.audio.music.volume_db})
	await steps(60)
	check("music-returns-after-respawn", game.audio.music.volume_db > -1.0 and game.state == Game.State.PLAYING, {"volume_db": game.audio.music.volume_db})
	game.player.position = Vector2(3120, 360)
	await steps(6)
	check("music-stops-at-exit", not game.audio.music.playing and game.state == Game.State.COMPLETE, {"playing": game.audio.music.playing})
	game.start_session()
	await steps(5)
	check("music-restarts-new-run", game.audio.music.playing, {"playing": game.audio.music.playing})
	# --- Mute keys: separate buses, never game state ---
	var before_state = game.state
	var mev := InputEventAction.new()
	mev.action = "mute_music"
	mev.pressed = true
	game.audio._unhandled_input(mev)
	check("n-mutes-music-only", game.audio.is_muted(&"Music") and not game.audio.is_muted(&"SFX") and game.state == before_state, {"music": game.audio.is_muted(&"Music"), "sfx": game.audio.is_muted(&"SFX")})
	var sev := InputEventAction.new()
	sev.action = "mute_sfx"
	sev.pressed = true
	game.audio._unhandled_input(sev)
	check("b-mutes-effects", game.audio.is_muted(&"SFX"), {"sfx": game.audio.is_muted(&"SFX")})
	game.audio._unhandled_input(mev)
	game.audio._unhandled_input(sev)
	check("toggles-back", not game.audio.is_muted(&"Music") and not game.audio.is_muted(&"SFX"), {})
	# --- F5: the same real-input route, sound on vs everything muted, must give identical traces ---
	# The first run in a fresh engine process can get extra physics ticks while the engine catches up at
	# startup (measured: 10 vs 3 ticks before the route starts), which shifts the oil value. A warm-up run
	# is discarded first; runs 2..6 of a determinism probe were identical with and without mute.
	var traces := []
	for muted in [false, false, true]:
		set_mute(muted)
		await fresh()
		var route = Route.new()
		var trace := []
		var t := 0
		while game.state == Game.State.PLAYING and t < 1500:
			route.step(game.player)
			await steps(1)
			t += 1
			if t % 10 == 0:
				trace.append([t, snappedf(game.player.position.x, 0.001), snappedf(game.player.position.y, 0.001), game.state, game.deaths, snappedf(game.oil, 0.001)])
		trace.append(["end", t, game.state, game.deaths, pc("jump"), pc("pickup")])
		traces.append(trace)
	traces.pop_front()  # discard the warm-up run
	set_mute(false)
	for i in range(mini(traces[0].size(), traces[1].size())):
		if traces[0][i] != traces[1][i]:
			print("FIRST DIFF at sample %d: sound=%s muted=%s" % [i, str(traces[0][i]), str(traces[1][i])])
			break
	check("muted-run-identical-to-sound-run", traces[0] == traces[1] and traces[0].back()[2] == Game.State.COMPLETE, {"samples": traces[0].size(), "end_sound": traces[0].back(), "end_muted": traces[1].back()})
	var out := ProjectSettings.globalize_path("res://../evidence")
	DirAccess.make_dir_recursive_absolute(out)
	var file := FileAccess.open(out + "/audio-" + str(Time.get_unix_time_from_system()) + ".json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"scope": "F3 sound-per-event counts, music behaviour, mute keys, F5 muted-trace equality; scripted inputs, not listening", "engine": Engine.get_version_info().string, "results": results, "failures": failures}, "  "))
	file.close()
	print("AUDIO TESTS: %d checks / %d failures" % [results.size(), failures])
	game.queue_free()
	await process_frame
	quit(1 if failures else 0)
