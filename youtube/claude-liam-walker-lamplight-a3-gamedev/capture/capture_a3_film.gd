extends SceneTree
## A3 film capture driver (Claude, 2026-10-15). Lives in the reel, copied into the isolated capture build's
## godot/tests/ only; the repository is not changed. Drives the asset room's own orbit camera through fixed
## keyframes, one step per rendered frame, so the take is identical on every run (Movie Maker, --fixed-fps 30).
## It moves only the camera: the assets, floor and light are exactly as saved in game3d/asset_room.tscn.
##   Godot_v4.7.2-stable_win64_console.exe --path <capture-build>/godot --disable-vsync --fixed-fps 30 \
##     --write-movie <reel>/_frames/<take>/f.png --script res://tests/capture_a3_film.gd -- --take <take>
## Takes: room-orbit (front -> behind -> below -> front, 20 s), room-front (front overview held, 2 s).

const FPS := 30.0
const OVERVIEW := Vector3(0.05, 0.7, 0.0)
# [seconds, target, distance, yaw_deg, pitch_deg]; pitch < 0 is above the target, > 0 below (the floor is
# single-sided, so from below it is see-through and the assets' undersides show).
const ORBIT := [
	[0.0, OVERVIEW, 4.2, 0.0, -12.0],
	[4.0, OVERVIEW, 3.6, -35.0, -15.0],
	[9.0, OVERVIEW, 4.0, -180.0, -12.0],
	[13.0, OVERVIEW, 3.6, -205.0, 30.0],
	[17.0, OVERVIEW, 3.8, -330.0, -8.0],
	[20.0, OVERVIEW, 4.2, -360.0, -12.0],
]
const FRONT := [
	[0.0, OVERVIEW, 4.2, 0.0, -12.0],
	[2.0, OVERVIEW, 4.2, 0.0, -12.0],
]

func _initialize() -> void:
	call_deferred("run")

func take_name() -> String:
	var args := OS.get_cmdline_user_args()
	var i := args.find("--take")
	return args[i + 1] if i >= 0 and i + 1 < args.size() else "room-orbit"

func sample(keys: Array, t: float) -> Array:
	for k in range(keys.size() - 1):
		var a: Array = keys[k]
		var b: Array = keys[k + 1]
		if t <= b[0]:
			var u: float = clampf((t - a[0]) / maxf(b[0] - a[0], 0.0001), 0.0, 1.0)
			u = u * u * (3.0 - 2.0 * u)  # smoothstep: no jolt at the keyframes
			return [a[1].lerp(b[1], u), lerpf(a[2], b[2], u), lerpf(a[3], b[3], u), lerpf(a[4], b[4], u)]
	var last: Array = keys[-1]
	return [last[1], last[2], last[3], last[4]]

func run() -> void:
	var take := take_name()
	var keys: Array = ORBIT if take == "room-orbit" else FRONT
	var room := (load("res://game3d/asset_room.tscn") as PackedScene).instantiate()
	root.add_child(room)
	var hint := room.get_node_or_null("Hint")
	if hint:
		hint.visible = false
	var cam := room.get_node("Camera") as Camera3D
	var total := int(round(keys[-1][0] * FPS))
	print("TAKE ", take, " frames ", total)
	for f in range(total):
		var s := sample(keys, f / FPS)
		cam.target = s[0]
		cam.distance = s[1]
		cam.yaw_deg = s[2]
		cam.pitch_deg = s[3]
		cam.apply_view()
		await process_frame
	quit(0)
