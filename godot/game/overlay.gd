extends Node2D
## Things drawn UNSHADED, so the darkness never hides them completely (pillar "Fair in the dark"):
## spikes keep a faint cold glint, uncollected oil drops and the lamp flames glow, the exit daylight is
## real light, and the spikes that just killed Wick flash red during the 0.55 s failure window (FX-FLASH).
const SPIKES := preload("res://assets/env/spikes.png")
const OIL := preload("res://assets/env/oil_drop.png")
const FLAME := Color("ffcf5a")
const DAYLIGHT := Color("dfeaf5")
const GLINT := Color(0.42, 0.47, 0.62)   # spikes outside the light: dim and cold, but readable
const FLASH := Color(1.0, 0.25, 0.2)

var game: Node2D

func _ready() -> void:
	var m := CanvasItemMaterial.new()
	m.light_mode = CanvasItemMaterial.LIGHT_MODE_UNSHADED
	material = m
	texture_repeat = CanvasItem.TEXTURE_REPEAT_ENABLED

func _draw() -> void:
	var level: Dictionary = game.level
	for i in range(level.hazards.size()):
		var h: Array = level.hazards[i]
		var tint := GLINT
		if game.state == game.State.DYING and i == game.killer_hazard and int(game.retry_remaining * 10.0) % 2 == 0:
			tint = FLASH
		draw_texture_rect(SPIKES, Rect2(h[0], h[1], h[2], h[3]), true, tint)
	for i in range(level.oil.size()):
		if not game.collected[i]:
			draw_texture(OIL, Vector2(level.oil[i][0], level.oil[i][1]) - OIL.get_size() / 2.0)
	for post in level.lamp_posts:
		draw_rect(Rect2(post[0] + 17, post[1] - 105, 4, 8), FLAME)
	var f: Array = level.finish
	var x0: float = f[0] - 40.0
	var floor_y: float = f[1] + f[3]
	draw_polygon(PackedVector2Array([Vector2(x0 + 40, 0), Vector2(level.width, 0), Vector2(level.width, floor_y), Vector2(x0 - 60, floor_y)]),
		PackedColorArray([Color(DAYLIGHT, 0.85), Color(DAYLIGHT, 0.85), Color(DAYLIGHT, 0.35), Color(DAYLIGHT, 0.0)]))
	draw_rect(Rect2(x0 + 40, 0, level.width - x0 - 40, 24), DAYLIGHT)
