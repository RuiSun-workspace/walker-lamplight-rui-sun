extends Control
## Lamplight HUD at 1280x720 (UI-GAUGE, UI-TEXT; code-drawn, not generated).
var game: Node2D
const TEXT := Color("f4f1e8")
const DIM := Color("9aa3bf")
const BRASS := Color("b8863b")
const FLAME := Color("ffcf5a")
const EMBER := Color("e2552f")
const PANEL := Color(0.04, 0.04, 0.07, 0.82)
const DAY := Color("dfeaf5")

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

func text_at(text: String, pos: Vector2, size_px: int = 20, color: Color = TEXT) -> void:
	draw_string(ThemeDB.fallback_font, pos, text, HORIZONTAL_ALIGNMENT_LEFT, -1, size_px, color)

func centered(text: String, y: float, size_px: int, color: Color = TEXT) -> void:
	var w := ThemeDB.fallback_font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, size_px).x
	text_at(text, Vector2((1280 - w) / 2, y), size_px, color)

func button_rect() -> Rect2:
	return Rect2(520, 440, 240, 56)

func gauge() -> void:
	## Flame icon + oil bar. Empty: the outline turns ember red and blinks (P5).
	var level: float = clampf(game.oil / game.OIL_MAX, 0.0, 1.0)
	var empty := level <= 0.0
	var low := level <= 0.15
	var col := EMBER if low else FLAME
	draw_colored_polygon(PackedVector2Array([Vector2(36, 18), Vector2(48, 38), Vector2(36, 50), Vector2(24, 38)]), col)
	# blink speeds up from 1.5 to 6 per second as the ember burns out (readable with sound off)
	var rate := lerpf(3.0, 12.0, clampf(game.ember_time / game.EMBER_LIMIT, 0.0, 1.0))
	var outline := EMBER if empty and int(game.elapsed * rate) % 2 == 0 else BRASS
	draw_rect(Rect2(60, 24, 248, 20), outline, false, 3.0)
	draw_rect(Rect2(64, 28, 240 * level, 12), col)

func _draw() -> void:
	if not is_instance_valid(game):
		return
	gauge()
	text_at("RETRIES %02d     %05.1fs" % [game.deaths, game.elapsed], Vector2(1030, 44), 20, DIM)
	text_at("A/D move   Space jump   W/S climb   R last lamp post   Esc pause", Vector2(24, 74), 15, DIM)  # was at the bottom, over the spike pit
	if game.state == game.State.PLAYING:
		return
	if game.state == game.State.DYING:
		draw_rect(Rect2(440, 250, 400, 96), PANEL)
		centered(game.death_reason, 292, 32, EMBER)
		centered("Back to the last lamp post.", 328, 18, DIM)
		return
	draw_rect(Rect2(0, 0, 1280, 720), Color(0, 0, 0, 0.45))
	draw_rect(Rect2(340, 190, 600, 330), PANEL)
	var title := "LAMPLIGHT"
	var detail := "Your flame is your light. Find the daylight before it burns out."
	var button := "ENTER  /  START"
	var title_col := FLAME
	if game.state == game.State.PAUSED:
		title = "PAUSED"
		detail = "R: back to the last lamp post     M: main menu"
		button = "ENTER  /  RESUME"
	elif game.state == game.State.COMPLETE:
		title = "YOU ESCAPED"
		title_col = DAY
		detail = "%.1f seconds   /   %d %s" % [game.last_finish_time, game.deaths, "retry" if game.deaths == 1 else "retries"]
		button = "ENTER  /  PLAY AGAIN"
	centered(title, 280, 48, title_col)
	centered(detail, 340, 20)
	centered("Oil drains every second. At zero your ember lasts 8 seconds.", 380, 16, DIM)
	var b := button_rect()
	draw_rect(b, BRASS)
	centered(button, b.position.y + 36, 22, Color("14151c"))
