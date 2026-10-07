extends Node2D
## Darkness and lights (CONCEPT pillar "Light is life"). Wick's light radius follows the oil:
## ~240 px at full, never below a ~56 px ring at zero (Rui, 2026-10-06: a small ring stays when the oil
## runs out). Lamp posts, uncollected oil drops and the exit carry their own small lights.
const RADIUS_FULL := 240.0
const RADIUS_EMBER := 56.0
const RADIUS_OUT := 28.0  # the ember ring keeps shrinking toward this as it burns out (silent warning)
const EASE := 8.0  # how fast the radius follows a change (pickup opens it up over ~0.3 s)

var game: Node2D
var wick_light: PointLight2D
var oil_lights: Array[PointLight2D] = []
var wick_radius: float = RADIUS_FULL

static func radial_texture() -> GradientTexture2D:
	var g := Gradient.new()
	g.set_color(0, Color(1, 1, 1, 1))
	g.set_color(1, Color(1, 1, 1, 0))
	g.add_point(0.55, Color(1, 1, 1, 0.55))
	var t := GradientTexture2D.new()
	t.gradient = g
	t.fill = GradientTexture2D.FILL_RADIAL
	t.fill_from = Vector2(0.5, 0.5)
	t.fill_to = Vector2(1.0, 0.5)
	t.width = 256
	t.height = 256
	return t

func _light(pos: Vector2, radius: float, colour: Color, energy: float) -> PointLight2D:
	var l := PointLight2D.new()
	l.texture = radial_texture()
	l.texture_scale = radius / 128.0
	l.color = colour
	l.energy = energy
	l.position = pos
	add_child(l)
	return l

func target_radius() -> float:
	if game.oil <= 0.0:
		return lerpf(RADIUS_EMBER, RADIUS_OUT, clampf(game.ember_time / game.EMBER_LIMIT, 0.0, 1.0))
	return lerpf(RADIUS_EMBER, RADIUS_FULL, clampf(game.oil / game.OIL_MAX, 0.0, 1.0))

func _ready() -> void:
	var dark := CanvasModulate.new()
	dark.color = Color(0.16, 0.16, 0.22)  # first value 0.09 hid the ledges ahead even at full oil (screenshot review)
	add_child(dark)
	wick_light = _light(Vector2.ZERO, RADIUS_FULL, Color(1.0, 0.82, 0.55), 1.35)
	for post in game.level.lamp_posts:
		_light(Vector2(post[0] + 19, post[1] - 100), 110.0, Color(1.0, 0.8, 0.5), 0.9)
	for drop in game.level.oil:
		oil_lights.append(_light(Vector2(drop[0], drop[1]), 44.0, Color(1.0, 0.7, 0.3), 0.8))
	var f: Array = game.level.finish
	_light(Vector2(f[0] + 40, f[1] + 40), 320.0, Color(0.85, 0.92, 1.0), 1.4)
	wick_radius = target_radius()

func _process(delta: float) -> void:
	wick_radius = lerpf(wick_radius, target_radius(), clampf(EASE * delta, 0.0, 1.0))
	wick_light.texture_scale = wick_radius / 128.0
	wick_light.position = game.player.position + Vector2(0, -40)  # at the flame
	for i in range(oil_lights.size()):
		oil_lights[i].visible = not game.collected[i]

func snap_radius() -> void:
	## Tests and respawn: jump straight to the target instead of easing.
	wick_radius = target_radius()
