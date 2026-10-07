extends Node2D

## Game rules for the Lamplight asset slice. Sound never decides anything here: the signals below are
## emitted after the state change they describe, and nothing reads back from the audio side
## (CHANGE-BRIEF section 2).
signal oil_collected(index: int)
signal died
signal respawned
signal completed
signal paused_changed(paused: bool)
signal run_started

const Player = preload("res://features/player/player.gd")
const Hud = preload("res://ui/hud.gd")
const Lighting = preload("res://game/lighting.gd")
const Overlay = preload("res://game/overlay.gd")
# Generated environment art (SOURCES.md, environment round 1). Lamp posts and the exit light are code-drawn.
const BG := preload("res://assets/env/bg_rock.png")
const TILE := preload("res://assets/env/tiles_rock.png")
const TILE_TOP := preload("res://assets/env/tiles_rock_top.png")
const LADDER := preload("res://assets/env/ladder.png")
const TIMBER := Color("5a412a")
const TIMBER_DARK := Color("3b2a1c")
const BRASS := Color("b8863b")
# CHANGE-BRIEF section 4 (first guesses, to be tuned by playtest)
const OIL_MAX := 100.0
const OIL_DRAIN := 4.0         # per second
const OIL_DROP := 35.0
const PICKUP_LOOK_TIME := 0.3  # seconds the pickup image shows

enum State { MENU, PLAYING, PAUSED, DYING, COMPLETE }
var state: State = State.MENU
var player: CharacterBody2D
var camera: Camera2D
var hud: Control
var lighting: Node2D
var overlay: Node2D
var level: Dictionary
var hazard_areas: Array[Area2D] = []
var goal: Area2D
var deaths: int = 0
var elapsed: float = 0.0
var retry_remaining: float = 0.0
var death_reason: String = ""
var killer_hazard: int = -1
var last_finish_time: float = 0.0
var test_mode: bool = false
var contact_settle_ticks: int = 0
var oil: float = OIL_MAX
var collected: Array[bool] = []
var pickup_until: float = -1.0
var checkpoint: int = 0                 # index into level.lamp_posts
var checkpoint_oil: float = OIL_MAX
var checkpoint_collected: Array[bool] = []

func _ready() -> void:
	process_physics_priority = 10
	level = JSON.parse_string(FileAccess.get_file_as_string("res://levels/lamplight_tunnel.json"))
	texture_repeat = CanvasItem.TEXTURE_REPEAT_ENABLED  # tiles and ladder are drawn as repeating textures
	_setup_input()
	for entry in level.solids:
		_add_solid(Rect2(entry[0], entry[1], entry[2], entry[3]))
	_add_solid(Rect2(-64, 0, 64, 860))
	_add_solid(Rect2(level.width, 0, 64, 860))
	for entry in level.hazards:
		hazard_areas.append(_add_area(Rect2(entry[0], entry[1], entry[2], entry[3]), 8, true))
	var f: Array = level.finish
	goal = _add_area(Rect2(f[0], f[1], f[2], f[3]), 16, false)
	_reset_run()
	overlay = Overlay.new()
	overlay.game = self
	add_child(overlay)
	player = Player.new()
	for entry in level.ladders:
		player.ladders.append(Rect2(entry[0], entry[1], entry[2], entry[3]))
	add_child(player)
	player.reset_at(_checkpoint_position())
	lighting = Lighting.new()
	lighting.game = self
	add_child(lighting)
	camera = Camera2D.new()
	camera.position = Vector2(640, 360)
	add_child(camera)
	var layer := CanvasLayer.new()
	add_child(layer)
	hud = Hud.new()
	hud.game = self
	layer.add_child(hud)
	get_window().focus_exited.connect(_on_focus_lost)
	queue_redraw()

func _setup_input() -> void:
	var actions := {"move_left": [KEY_A, KEY_LEFT], "move_right": [KEY_D, KEY_RIGHT], "jump": [KEY_SPACE], "pause": [KEY_ESCAPE, KEY_P], "restart": [KEY_R], "confirm": [KEY_ENTER], "menu": [KEY_M], "climb_up": [KEY_W, KEY_UP], "climb_down": [KEY_S, KEY_DOWN]}
	for action in actions:
		if InputMap.has_action(action):
			continue
		InputMap.add_action(action)
		for key in actions[action]:
			var event := InputEventKey.new()
			event.physical_keycode = key
			InputMap.action_add_event(action, event)

func _add_solid(rect: Rect2) -> void:
	var body := StaticBody2D.new()
	body.position = rect.position + rect.size / 2
	body.collision_layer = 1
	body.collision_mask = 2
	var shape := RectangleShape2D.new()
	shape.size = rect.size
	var collision := CollisionShape2D.new()
	collision.shape = shape
	body.add_child(collision)
	add_child(body)

func _add_area(rect: Rect2, layer: int, spikes: bool) -> Area2D:
	var area := Area2D.new()
	area.position = rect.position
	area.collision_layer = layer
	area.collision_mask = 2
	if spikes:
		# One exact triangular trigger per drawn spike (16 px each, matching spikes.png); no oversized box.
		for i in range(maxi(1, roundi(rect.size.x / 16.0))):
			var triangle := CollisionPolygon2D.new()
			var x := float(i) * 16.0
			triangle.polygon = PackedVector2Array([Vector2(x, rect.size.y), Vector2(x + 8, 0), Vector2(x + 16, rect.size.y)])
			area.add_child(triangle)
	else:
		var collision := CollisionShape2D.new()
		var shape := RectangleShape2D.new()
		shape.size = rect.size
		collision.shape = shape
		collision.position = rect.size / 2.0
		area.add_child(collision)
	add_child(area)
	return area

func _reset_run() -> void:
	## A whole new run: first lamp post, full oil, every drop back.
	collected.clear()
	for i in range(level.oil.size()):
		collected.append(false)
	checkpoint = 0
	checkpoint_oil = OIL_MAX
	checkpoint_collected = collected.duplicate()

func _checkpoint_position() -> Vector2:
	if checkpoint == 0:
		return Vector2(level.spawn[0], level.spawn[1])
	var post: Array = level.lamp_posts[checkpoint]
	return Vector2(post[0] + 40, post[1])

func start_session() -> void:
	if state == State.PLAYING:
		return
	deaths = 0
	elapsed = 0.0  # the run timer keeps counting through deaths; only a new run resets it
	_reset_run()
	restart_attempt()
	run_started.emit()

func restart_attempt() -> void:
	## Back to the last lamp post with the oil and drops it saved (storyboard P7). Not a death.
	var was_dying := state == State.DYING
	state = State.PLAYING
	retry_remaining = 0.0
	killer_hazard = -1
	oil = checkpoint_oil
	collected = checkpoint_collected.duplicate()
	pickup_until = -1.0
	# Area2D overlaps are physics-step snapshots. Discard pre-teleport contacts
	# until the broadphase has observed the reset, preventing a phantom second death.
	contact_settle_ticks = 2
	player.look_override = ""
	player.reset_at(_checkpoint_position())
	player.enabled = true
	camera.position.x = clampf(player.position.x + 200, 640, float(level.width) - 640)
	if is_instance_valid(lighting):
		lighting.snap_radius()
	if was_dying:
		respawned.emit()

func set_paused(value: bool) -> void:
	if value and state == State.PLAYING:
		state = State.PAUSED
		player.enabled = false
		paused_changed.emit(true)
	elif not value and state == State.PAUSED:
		state = State.PLAYING
		player.enabled = true
		player.require_jump_release = true
		player.jump_request_tick = -1000
		paused_changed.emit(false)

func _on_focus_lost() -> void:
	if not test_mode:
		set_paused(true)

func resolve_contacts(fatal: bool, finished: bool) -> void:
	if state != State.PLAYING:
		return
	if fatal:
		state = State.DYING
		deaths += 1
		retry_remaining = 0.55
		player.enabled = false
		player.velocity = Vector2.ZERO
		player.look_override = "hurt"  # storyboard P6
		player._update_look()
		died.emit()
	elif finished:
		state = State.COMPLETE
		last_finish_time = elapsed
		player.enabled = false
		player.velocity = Vector2.ZERO
		player.look_override = "celebrate"  # storyboard P8
		player._update_look()
		completed.emit()

func player_rect() -> Rect2:
	return Rect2(player.position.x - 18, player.position.y - 56, 36, 56)

func _physics_process(delta: float) -> void:
	if state == State.DYING:
		retry_remaining -= delta
		if retry_remaining <= 0:
			restart_attempt()
	elif state == State.PLAYING:
		elapsed += delta
		oil = maxf(0.0, oil - OIL_DRAIN * delta)
		_collect_oil()
		_touch_lamp_posts()
		var fatal := player.position.y > float(level.fall_y)
		death_reason = "Missed the landing" if fatal else "Watch the spikes"
		for i in range(hazard_areas.size()):
			if hazard_areas[i].overlaps_body(player):
				fatal = true
				killer_hazard = i
		if contact_settle_ticks > 0:
			contact_settle_ticks -= 1
		else:
			resolve_contacts(fatal, goal.overlaps_body(player))
		camera.position.x = clampf(player.position.x + 200, 640, float(level.width) - 640)
		if state == State.PLAYING:  # a death / exit this tick already set hurt / celebrate; keep it
			_update_event_look()
	if is_instance_valid(hud):
		hud.queue_redraw()
	if is_instance_valid(overlay):
		overlay.queue_redraw()

func _collect_oil() -> void:
	var body := player_rect()
	for i in range(level.oil.size()):
		if collected[i]:
			continue
		var drop := Rect2(level.oil[i][0] - 12, level.oil[i][1] - 12, 24, 24)
		if body.intersects(drop):
			collected[i] = true  # marked before the signal, so one drop can only ever fire once
			oil = minf(OIL_MAX, oil + OIL_DROP)
			pickup_until = elapsed + PICKUP_LOOK_TIME
			oil_collected.emit(i)

func _touch_lamp_posts() -> void:
	for i in range(checkpoint + 1, level.lamp_posts.size()):
		var post: Array = level.lamp_posts[i]
		if absf(player.position.x - post[0]) < 48 and absf(player.position.y - post[1]) < 8 and player.is_on_floor():
			checkpoint = i
			checkpoint_oil = oil
			checkpoint_collected = collected.duplicate()

func _update_event_look() -> void:
	## Event images override movement images: pickup (0.3 s) > ember (oil empty). Hurt / celebrate are set
	## on the state change itself.
	if elapsed < pickup_until:
		player.look_override = "pickup"
	elif oil <= 0.0 and not player.climbing:
		player.look_override = "ember"
	else:
		player.look_override = ""
	player._update_look()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.echo:
		return
	if event.is_action_pressed("confirm"):
		if state in [State.MENU, State.COMPLETE]:
			start_session()
		elif state == State.PAUSED:
			set_paused(false)
	elif event.is_action_pressed("pause"):
		set_paused(state != State.PAUSED)
	elif event.is_action_pressed("restart") and state in [State.PLAYING, State.PAUSED, State.DYING]:
		if state == State.PAUSED:
			paused_changed.emit(false)
		restart_attempt()
	elif event.is_action_pressed("menu") and state in [State.PAUSED, State.COMPLETE]:
		state = State.MENU
		player.enabled = false
	elif event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		if hud.button_rect().has_point(hud.get_local_mouse_position()):
			if state in [State.MENU, State.COMPLETE]:
				start_session()
			elif state == State.PAUSED:
				set_paused(false)

func _draw() -> void:
	if level.is_empty():
		return
	# Back wall: the generated 1280x720 rock, every other copy mirrored so the repeat seam matches.
	for i in range(int(ceil(float(level.width) / 1280.0)) + 1):
		var x := float(i) * 1280.0
		if i % 2 == 0:
			draw_texture(BG, Vector2(x, 0))
		else:  # a negative rect size does not flip in Godot 4; mirror with a transform instead
			draw_set_transform(Vector2(x + 1280, 0), 0.0, Vector2(-1, 1))
			draw_texture(BG, Vector2.ZERO)
			draw_set_transform(Vector2.ZERO)
	for entry in level.solids:
		var r := Rect2(entry[0], entry[1], entry[2], entry[3])
		draw_texture_rect(TILE, r, true)
		var top_h := minf(64.0, r.size.y)
		draw_texture_rect_region(TILE_TOP, Rect2(r.position, Vector2(r.size.x, top_h)), Rect2(0, 0, r.size.x, top_h))
	for entry in level.ladders:
		draw_texture_rect(LADDER, Rect2(entry[0], entry[1], entry[2], entry[3]), true)
	for entry in level.lamp_posts:
		_draw_lamp_post(Vector2(entry[0], entry[1]))

func _draw_lamp_post(foot: Vector2) -> void:
	# Code-drawn checkpoint (Rui, 2026-10-07: no generated lamp post was usable). Timber post, brass lamp;
	# the lamp's flame is drawn unshaded by overlay.gd.
	draw_rect(Rect2(foot.x - 5, foot.y - 112, 10, 112), TIMBER)
	draw_rect(Rect2(foot.x - 5, foot.y - 112, 3, 112), TIMBER_DARK)
	draw_rect(Rect2(foot.x - 5, foot.y - 116, 26, 6), TIMBER)
	draw_rect(Rect2(foot.x + 12, foot.y - 110, 14, 18), BRASS)
	draw_rect(Rect2(foot.x + 14, foot.y - 107, 10, 12), Color("241f2c"))
