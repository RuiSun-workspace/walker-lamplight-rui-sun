extends CharacterBody2D

## Emitted from the one line where a jump actually starts (ground, coyote, buffer or off a ladder).
## Sound listens to this; nothing reads it back (CHANGE-BRIEF section 2).
signal jumped

const Tuning = preload("res://features/player/tuning.gd")
# Generated state images (SOURCES.md): 64x80, feet on the bottom row, cap centred (CHARACTER-SHEET rev. 2026-10-07).
const LOOKS := {
	"idle": preload("res://assets/char/wick_idle.png"),
	"walk": preload("res://assets/char/wick_walk.png"),
	"jump": preload("res://assets/char/wick_jump.png"),
	"fall": preload("res://assets/char/wick_fall.png"),
	"climb": preload("res://assets/char/wick_climb.png"),
	"pickup": preload("res://assets/char/wick_pickup.png"),
	"ember": preload("res://assets/char/wick_ember.png"),
	"hurt": preload("res://assets/char/wick_hurt.png"),
	"celebrate": preload("res://assets/char/wick_celebrate.png"),
}
const CLIMB_SPEED := 180.0  # CHANGE-BRIEF 4b: ~90 px/s at 640x360, x2
const CLIMB_DOWN_SPEED := 270.0  # Rui playtest 2026-10-07: coming down felt stuck; down is 1.5x faster

var tuning = Tuning.new()
var enabled: bool = false
var tick: int = 0
var last_floor_tick: int = -1000
var jump_request_tick: int = -1000
var opportunity_consumed: bool = false
var require_jump_release: bool = true
var facing: float = 1.0
var jumps: int = 0
var climbing: bool = false
var ladders: Array[Rect2] = []
var look: String = "idle"
## Set by the session for event looks (hurt, celebrate, pickup, ember); "" = follow movement.
var look_override: String = ""
var sprite: Sprite2D
var test_control: bool = false
var test_axis: float = 0.0
var test_climb_axis: float = 0.0
var test_jump_pressed: bool = false
var test_jump_held: bool = false

func _ready() -> void:
	name = "Player"
	collision_layer = 2
	collision_mask = 1
	floor_snap_length = 1.0
	var shape := RectangleShape2D.new()
	shape.size = Vector2(36, 56)  # CHARACTER-SHEET revision 2026-10-07: x2 of the inherited 18x28
	var collider := CollisionShape2D.new()
	collider.shape = shape
	collider.position = Vector2(0, -28)
	add_child(collider)
	sprite = Sprite2D.new()
	sprite.centered = false
	sprite.position = Vector2(-32, -80)  # bottom row on the feet, frame centre on the collider centre
	add_child(sprite)
	_update_look()

func reset_at(spawn: Vector2) -> void:
	position = spawn
	velocity = Vector2.ZERO
	last_floor_tick = -1000
	jump_request_tick = -1000
	opportunity_consumed = false
	require_jump_release = true
	test_jump_pressed = false
	jumps = 0
	climbing = false
	facing = 1.0
	_update_look()

func ladder_at() -> Variant:
	for r in ladders:
		var centre := r.position.x + r.size.x / 2.0
		if absf(position.x - centre) <= 20.0 and position.y > r.position.y - 10.0 and position.y - 56.0 < r.end.y:
			return r
	return null

func _physics_process(delta: float) -> void:
	if not enabled:
		return
	tick += 1
	var axis := test_axis if test_control else Input.get_axis("move_left", "move_right")
	var climb_axis := test_climb_axis if test_control else Input.get_axis("climb_up", "climb_down")
	var held := test_jump_held if test_control else Input.is_action_pressed("jump")
	var pressed := test_jump_pressed if test_control else Input.is_action_just_pressed("jump")
	test_jump_pressed = false
	if not held:
		require_jump_release = false
	var ladder = ladder_at()
	# Grab: Up anywhere on the ladder; Down while airborne on it or while standing at its top (Rui playtest
	# 2026-10-07: getting down from the upper floor meant falling off the edge and grabbing in mid-air).
	# Standing at the foot + Down does nothing.
	var at_top: bool = ladder != null and is_on_floor() and absf(position.y - ladder.position.y) < 2.0
	if not climbing and ladder != null and (climb_axis < 0.0 or (climb_axis > 0.0 and (not is_on_floor() or at_top))):
		climbing = true
		position.x = ladder.position.x + ladder.size.x / 2.0
		velocity = Vector2.ZERO
	if climbing and ladder == null:
		climbing = false
	if (is_on_floor() and velocity.y >= 0.0) or climbing:
		last_floor_tick = tick  # a ladder counts as footing, so a jump off it uses the same jump line below
		opportunity_consumed = false
	if pressed and not require_jump_release:
		jump_request_tick = tick
	if climbing:
		velocity.x = 0.0
		velocity.y = climb_axis * (CLIMB_SPEED if climb_axis < 0.0 else CLIMB_DOWN_SPEED)
		var top: float = ladder.position.y - 6.0
		if position.y + velocity.y * delta <= top:  # stop a little above the floor the ladder leads to
			position.y = top
			velocity.y = 0.0
		if not is_zero_approx(axis):  # step off sideways at full speed (onto the upper floor at the top)
			climbing = false
			velocity.x = axis * tuning.speed
		elif is_on_floor() and climb_axis > 0.0:  # reached the foot
			climbing = false
	if not climbing:
		var rate: float = tuning.acceleration if not is_zero_approx(axis) else tuning.deceleration
		velocity.x = move_toward(velocity.x, axis * tuning.speed, rate * delta)
		velocity.y = minf(velocity.y + tuning.gravity * delta, tuning.terminal_velocity)
	if not is_zero_approx(axis):
		facing = signf(axis)
	if not opportunity_consumed and tick - last_floor_tick <= tuning.coyote_ticks and tick - jump_request_tick <= tuning.buffer_ticks:
		climbing = false
		velocity.y = tuning.jump_velocity
		opportunity_consumed = true
		jump_request_tick = -1000
		jumps += 1
		jumped.emit()
	move_and_slide()
	position.x = maxf(position.x, 20.0)
	_update_look()

func _update_look() -> void:
	if look_override != "":
		look = look_override
	elif climbing:
		look = "climb"
	elif not is_on_floor():
		look = "jump" if velocity.y < 0.0 else "fall"
	elif absf(velocity.x) > 8.0:
		look = "walk"
	else:
		look = "idle"
	if sprite:
		sprite.texture = LOOKS[look]
		sprite.flip_h = facing < 0.0 and look != "climb"  # climb is the back view: never mirrored
