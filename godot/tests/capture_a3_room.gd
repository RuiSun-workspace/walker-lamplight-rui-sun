extends SceneTree
## Screenshots of the A3 asset room from fixed camera views, saved to docs/a3/evidence/room_<view>.png.
## Needs a window (rendering), so run WITHOUT --headless:
##   Godot_v4.7.2-stable_win64_console.exe --path godot --script res://tests/capture_a3_room.gd
## These are Claude's evidence captures from scripted views. They are not Rui's human check, which is done
## by orbiting the camera by hand in the running scene.

const VIEWS := {
	"overview_front": {"target": Vector3(0.05, 0.7, 0.0), "distance": 4.2, "yaw": 0.0, "pitch": -12.0},
	"overview_back": {"target": Vector3(0.05, 0.7, 0.0), "distance": 4.2, "yaw": 180.0, "pitch": -12.0},
	"overview_below": {"target": Vector3(0.05, 0.4, 0.0), "distance": 3.6, "yaw": 20.0, "pitch": 40.0},
	"lamp_post_close": {"target": Vector3(-1.1, 0.4, 0.0), "distance": 1.5, "yaw": 25.0, "pitch": -10.0},
	"oil_drop_close": {"target": Vector3(1.5, 0.15, 0.0), "distance": 1.0, "yaw": -30.0, "pitch": -15.0},
	"pit_prop_close": {"target": Vector3(0.3, 1.0, 0.0), "distance": 2.8, "yaw": 35.0, "pitch": -10.0},
}

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	var room := (load("res://game3d/asset_room.tscn") as PackedScene).instantiate()
	root.add_child(room)
	var hint := room.get_node_or_null("Hint")
	if hint:
		hint.visible = false
	var cam := room.get_node("Camera") as Camera3D
	var out_dir := ProjectSettings.globalize_path("res://").path_join("../docs/a3/evidence").simplify_path()
	DirAccess.make_dir_recursive_absolute(out_dir)
	for view in VIEWS:
		var v: Dictionary = VIEWS[view]
		cam.target = v["target"]
		cam.distance = v["distance"]
		cam.yaw_deg = v["yaw"]
		cam.pitch_deg = v["pitch"]
		cam.apply_view()
		for i in range(6):
			await process_frame
		await RenderingServer.frame_post_draw
		var img := root.get_texture().get_image()
		var path := out_dir.path_join("room_%s.png" % view)
		var err := img.save_png(path)
		print("CAPTURE ", view, " ", img.get_width(), "x", img.get_height(), " -> ", path, " err=", err)
	quit(0)
