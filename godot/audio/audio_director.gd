extends Node
## Plays the four event sounds and the music loop by LISTENING to game signals (CHANGE-BRIEF 2 and 3).
## Nothing here changes game state; a missing file or a muted bus changes nothing but what you hear.
## N mutes music, B mutes effects (separate buses).
const STREAMS := {
	"jump": preload("res://assets/audio/sfx_jump.ogg"),
	"pickup": preload("res://assets/audio/sfx_pickup.ogg"),
	"hurt": preload("res://assets/audio/sfx_hurt.ogg"),
	"exit": preload("res://assets/audio/sfx_exit.ogg"),
}
const MUSIC := preload("res://assets/audio/mus_loop.ogg")  # imported with loop=true, 8 bars at 90 bpm
const CUTOFF_FULL := 20000.0
const CUTOFF_LOW := 800.0     # oil nearly empty
const CUTOFF_EMBER := 400.0   # oil empty: mostly the low pulse
const EMBER_DB := -4.0
const DUCK_DB := -12.0        # failure window
const JUMP_DB := -16.0        # Rui playtests 2026-10-07: jump too loud; -8 dB was still too loud, now -16 (mix only; file unchanged)

var game: Node2D
var sfx: Dictionary = {}
var music: AudioStreamPlayer
var lowpass: AudioEffectLowPassFilter
var play_counts := {"jump": 0, "pickup": 0, "hurt": 0, "exit": 0}
var duck_db: float = 0.0
var duck_target: float = 0.0
var cutoff: float = CUTOFF_FULL

func _ready() -> void:
	for id in STREAMS:
		var p := AudioStreamPlayer.new()
		p.stream = STREAMS[id]
		p.bus = &"SFX"
		if id == "jump":
			p.volume_db = JUMP_DB
		add_child(p)
		sfx[id] = p
	music = AudioStreamPlayer.new()
	music.stream = MUSIC
	music.bus = &"Music"
	add_child(music)
	var bus := AudioServer.get_bus_index(&"Music")
	lowpass = AudioServer.get_bus_effect(bus, 0) as AudioEffectLowPassFilter
	game.player.jumped.connect(_play.bind("jump"))
	game.oil_collected.connect(func(_i): _play("pickup"))
	game.died.connect(_on_died)
	game.respawned.connect(func(): duck_target = 0.0)
	game.completed.connect(_on_completed)
	game.paused_changed.connect(func(paused): music.stream_paused = paused)
	game.run_started.connect(_on_run_started)
	game.returned_to_menu.connect(_on_run_started)
	music.play()  # title screen: full brightness

func _play(id: String) -> void:
	play_counts[id] += 1
	sfx[id].play()

func _on_died() -> void:
	_play("hurt")
	duck_target = DUCK_DB   # music dips but keeps its place

func _on_completed() -> void:
	_play("exit")
	music.stop()            # stays stopped on the end card; the exit sound plays alone

func _on_run_started() -> void:
	duck_target = 0.0
	music.stream_paused = false
	if not music.playing:
		music.play()        # after the end card the loop starts again from its beginning

func target_cutoff() -> float:
	if game.state == game.State.MENU or game.state == game.State.COMPLETE:
		return CUTOFF_FULL
	if game.oil <= 0.0:
		return CUTOFF_EMBER
	var t := clampf(game.oil / game.OIL_MAX, 0.0, 1.0)
	return CUTOFF_LOW * pow(CUTOFF_FULL / CUTOFF_LOW, t)  # exponential: equal steps sound equal

func _process(delta: float) -> void:
	cutoff = lerpf(cutoff, target_cutoff(), clampf(delta / 0.3, 0.0, 1.0))  # ~0.3 s to open up after a pickup
	if lowpass:
		lowpass.cutoff_hz = cutoff
	var ember: bool = game.state == game.State.PLAYING and game.oil <= 0.0
	duck_db = move_toward(duck_db, duck_target, absf(DUCK_DB) * delta / (0.1 if duck_target < duck_db else 0.3))
	music.volume_db = duck_db + (EMBER_DB if ember else 0.0)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.echo:
		return
	if event.is_action_pressed("mute_music"):
		toggle_mute(&"Music")
	elif event.is_action_pressed("mute_sfx"):
		toggle_mute(&"SFX")

func toggle_mute(bus_name: StringName) -> void:
	var i := AudioServer.get_bus_index(bus_name)
	AudioServer.set_bus_mute(i, not AudioServer.is_bus_mute(i))

static func is_muted(bus_name: StringName) -> bool:
	return AudioServer.is_bus_mute(AudioServer.get_bus_index(bus_name))
