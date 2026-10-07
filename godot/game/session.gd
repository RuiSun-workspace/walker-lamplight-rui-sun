extends Node2D

const Player = preload("res://features/player/player.gd")
const Hud = preload("res://ui/hud.gd")
# Generated environment art (SOURCES.md, environment round 1). Lamp posts and the exit light are code-drawn.
const BG := preload("res://assets/env/bg_rock.png")
const TILE := preload("res://assets/env/tiles_rock.png")
const TILE_TOP := preload("res://assets/env/tiles_rock_top.png")
const SPIKES := preload("res://assets/env/spikes.png")
const LADDER := preload("res://assets/env/ladder.png")
const OIL := preload("res://assets/env/oil_drop.png")
const BRASS := Color("b8863b")
const FLAME := Color("ffcf5a")
const TIMBER := Color("5a412a")
const TIMBER_DARK := Color("3b2a1c")
const DAYLIGHT := Color("dfeaf5")
enum State { MENU, PLAYING, PAUSED, DYING, COMPLETE }
var state: State = State.MENU
var player: CharacterBody2D
var camera: Camera2D
var hud: Control
var level: Dictionary
var hazard_areas: Array[Area2D] = []
var goal: Area2D
var deaths: int = 0
var elapsed: float = 0.0
var retry_remaining: float = 0.0
var death_reason: String = ""
var last_finish_time: float = 0.0
var test_mode: bool = false
var contact_settle_ticks: int = 0

func _ready() -> void:
	process_physics_priority = 10
	level = JSON.parse_string(FileAccess.get_file_as_string("res://levels/lamplight_tunnel.json"))
	texture_repeat = CanvasItem.TEXTURE_REPEAT_ENABLED  # tiles, spikes and ladder are drawn as repeating textures
	_setup_input()
	for entry in level.solids:
		_add_solid(Rect2(entry[0], entry[1], entry[2], entry[3]))
	_add_solid(Rect2(-64, 0, 64, 860))
	_add_solid(Rect2(level.width, 0, 64, 860))
	for entry in level.hazards:
		hazard_areas.append(_add_area(Rect2(entry[0], entry[1], entry[2], entry[3]), 8, true))
	var f: Array = level.finish
	goal = _add_area(Rect2(f[0], f[1], f[2], f[3]), 16, false)
	player = Player.new()
	add_child(player)
	player.reset_at(Vector2(level.spawn[0], level.spawn[1]))
	camera = Camera2D.new()
	camera.position = Vector2(640, 360)
	add_child(camera)
	var layer := CanvasLayer.new()
	add_child(layer)
	hud = Hud.new()
	hud.game = self
	hud.scale = Vector2(2, 2)  # placeholder HUD drawn in 640x360 units until the HUD step
	layer.add_child(hud)
	get_window().focus_exited.connect(_on_focus_lost)
	queue_redraw()

func _setup_input() -> void:
	var actions := {"move_left": [KEY_A, KEY_LEFT], "move_right": [KEY_D, KEY_RIGHT], "jump": [KEY_SPACE], "pause": [KEY_ESCAPE, KEY_P], "restart": [KEY_R], "confirm": [KEY_ENTER], "menu": [KEY_M]}
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

func start_session() -> void:
	if state == State.PLAYING:
		return
	deaths = 0
	restart_attempt()

func restart_attempt() -> void:
	state = State.PLAYING
	elapsed = 0.0
	retry_remaining = 0.0
	# Area2D overlaps are physics-step snapshots. Discard pre-teleport contacts
	# until the broadphase has observed the reset, preventing a phantom second death.
	contact_settle_ticks = 2
	player.reset_at(Vector2(level.spawn[0], level.spawn[1]))
	player.enabled = true
	camera.position = Vector2(640, 360)

func set_paused(value: bool) -> void:
	if value and state == State.PLAYING:
		state = State.PAUSED
		player.enabled = false
	elif not value and state == State.PAUSED:
		state = State.PLAYING
		player.enabled = true
		player.require_jump_release = true
		player.jump_request_tick = -1000

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
	elif finished:
		state = State.COMPLETE
		last_finish_time = elapsed
		player.enabled = false
		player.velocity = Vector2.ZERO

func _physics_process(delta: float) -> void:
	if state == State.DYING:
		retry_remaining -= delta
		if retry_remaining <= 0:
			restart_attempt()
	elif state == State.PLAYING:
		elapsed += delta
		var fatal := player.position.y > float(level.fall_y)
		death_reason = "Missed the landing" if fatal else "Watch the spikes"
		for hazard in hazard_areas:
			fatal = fatal or hazard.overlaps_body(player)
		if contact_settle_ticks > 0:
			contact_settle_ticks -= 1
		else:
			resolve_contacts(fatal, goal.overlaps_body(player))
		camera.position.x = clampf(player.position.x + 200, 640, float(level.width) - 640)
	if is_instance_valid(hud):
		hud.queue_redraw()

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
		restart_attempt()
	elif event.is_action_pressed("menu") and state in [State.PAUSED, State.COMPLETE]:
		state = State.MENU
		player.enabled = false
	elif event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		if Rect2(220, 215, 200, 34).has_point(hud.get_local_mouse_position()):
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
	for entry in level.hazards:
		draw_texture_rect(SPIKES, Rect2(entry[0], entry[1], entry[2], entry[3]), true)
	for entry in level.ladders:
		draw_texture_rect(LADDER, Rect2(entry[0], entry[1], entry[2], entry[3]), true)
	for entry in level.oil:
		draw_texture(OIL, Vector2(entry[0], entry[1]) - OIL.get_size() / 2.0)
	for entry in level.lamp_posts:
		_draw_lamp_post(Vector2(entry[0], entry[1]))
	_draw_exit_light()

func _draw_lamp_post(foot: Vector2) -> void:
	# Code-drawn checkpoint (Rui, 2026-10-07: no generated lamp post was usable). Timber post, brass lamp.
	draw_rect(Rect2(foot.x - 5, foot.y - 112, 10, 112), TIMBER)
	draw_rect(Rect2(foot.x - 5, foot.y - 112, 3, 112), TIMBER_DARK)
	draw_rect(Rect2(foot.x - 5, foot.y - 116, 26, 6), TIMBER)
	draw_rect(Rect2(foot.x + 12, foot.y - 110, 14, 18), BRASS)
	draw_rect(Rect2(foot.x + 14, foot.y - 107, 10, 12), Color("241f2c"))
	draw_rect(Rect2(foot.x + 17, foot.y - 105, 4, 8), FLAME)

func _draw_exit_light() -> void:
	# Code-drawn daylight at the exit (Rui, 2026-10-07). The only cool light in the level (pillar "The way out glows").
	var f: Array = level.finish
	var x0: float = f[0] - 40.0
	var floor_y: float = f[1] + f[3]
	draw_polygon(PackedVector2Array([Vector2(x0 + 40, 0), Vector2(level.width, 0), Vector2(level.width, floor_y), Vector2(x0 - 60, floor_y)]),
		PackedColorArray([Color(DAYLIGHT, 0.85), Color(DAYLIGHT, 0.85), Color(DAYLIGHT, 0.35), Color(DAYLIGHT, 0.0)]))
	draw_rect(Rect2(x0 + 40, 0, level.width - x0 - 40, 24), DAYLIGHT)
