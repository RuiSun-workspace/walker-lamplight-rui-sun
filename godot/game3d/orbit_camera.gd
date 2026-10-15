extends Camera3D
## Orbit camera for the A3 asset room, so every asset can be looked at from all sides, including behind and
## below (the floor is single-sided, so it is see-through from underneath).
##   right-drag: orbit    wheel: zoom    middle-drag: pan
##   0: overview   1: lamp post   2: pit prop   3: oil drop   4: Wick stand-in

@export var target := Vector3(0.05, 0.7, 0.0)
@export var distance := 4.2
@export var yaw_deg := 0.0
@export var pitch_deg := -12.0  # negative = camera above the target

const FOCUS := {
	KEY_0: [Vector3(0.05, 0.7, 0.0), 4.2],
	KEY_1: [Vector3(-1.34, 0.4, 0.0), 1.3],
	KEY_2: [Vector3(0.3, 1.0, 0.0), 3.0],
	KEY_3: [Vector3(1.5, 0.15, 0.0), 1.0],
	KEY_4: [Vector3(-0.8, 0.18, 0.0), 0.9],
}

func _ready() -> void:
	apply_view()

func apply_view() -> void:
	pitch_deg = clampf(pitch_deg, -85.0, 85.0)
	distance = clampf(distance, 0.2, 12.0)
	var offset := Basis(Vector3.UP, deg_to_rad(yaw_deg)) * Basis(Vector3.RIGHT, deg_to_rad(pitch_deg)) * Vector3(0, 0, distance)
	position = target + offset
	look_at(target, Vector3.UP)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion:
		var motion := event as InputEventMouseMotion
		if motion.button_mask & MOUSE_BUTTON_MASK_RIGHT:
			yaw_deg -= motion.relative.x * 0.3
			pitch_deg -= motion.relative.y * 0.3
			apply_view()
		elif motion.button_mask & MOUSE_BUTTON_MASK_MIDDLE:
			var pan := (-global_basis.x * motion.relative.x + global_basis.y * motion.relative.y) * distance * 0.0015
			target += pan
			apply_view()
	elif event is InputEventMouseButton and event.pressed:
		var button := event as InputEventMouseButton
		if button.button_index == MOUSE_BUTTON_WHEEL_UP:
			distance *= 0.9
			apply_view()
		elif button.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			distance /= 0.9
			apply_view()
	elif event is InputEventKey and event.pressed and not event.echo:
		var key := (event as InputEventKey).physical_keycode
		if FOCUS.has(key):
			target = FOCUS[key][0]
			distance = FOCUS[key][1]
			apply_view()
