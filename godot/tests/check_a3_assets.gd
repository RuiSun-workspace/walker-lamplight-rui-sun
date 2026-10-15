extends SceneTree
## A3 headless check: load each imported .glb and the asset room, print what Godot actually has, and compare it
## with docs/a3/CHANGE-BRIEF.md section 6 (+ section 9 revisions: oil_drop x2, pit_prop 0.8 m wide). Tolerance 1 mm.
##   Godot_v4.7.2-stable_win64_console.exe --headless --path godot --script res://tests/check_a3_assets.gd --fixed-fps 60
##
## What it shows: the imported mesh's bounding box (size, lowest Y, X range), every node's scale and rotation,
## which axis is tallest, the triangle count of the base mesh (not Godot's generated LODs), each surface's
## albedo colour, and - in the asset room - each asset's lowest point against the Floor node's height.
## What it does not show: that the assets look right, read as what they are, or suit the game's lighting and
## style. Those are Rui's human checks (TEST-REPORT section 7).

const TOL := 0.001
const ROOM := "res://game3d/asset_room.tscn"
const ASSETS := {
	"lamp_post": {"node": "LampPost", "min": Vector3(-0.03125, 0.0, -0.04775), "max": Vector3(0.1625, 0.725, 0.04775),
		"max_tris": 72, "stands_on_y": true,
		"colours": {"lp_timber": "5a412a", "lp_brass": "b8863b", "lp_glass": "241f2c", "lp_flame": "fdffa6"}},
	"oil_drop": {"node": "OilDrop", "min": Vector3(-0.1375, 0.0, -0.1375), "max": Vector3(0.1375, 0.3, 0.1375),
		"max_tris": 120, "stands_on_y": false,
		"colours": {"od_oil": "f2a93b"}},
	"pit_prop": {"node": "PitProp", "min": Vector3(-0.4, 0.0, -0.06), "max": Vector3(0.4, 2.0, 0.06),
		"max_tris": 60, "stands_on_y": true,
		"colours": {"pp_timber": "5a412a", "pp_timber_dark": "3b2a1c"}},
}

var results: Array[Dictionary] = []
var failures := 0

func _initialize() -> void:
	call_deferred("run")

func check(id: String, passed: bool, observed: Dictionary) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed})
	if not passed:
		failures += 1
	print(JSON.stringify(results.back()))

func meshes_under(node: Node) -> Array[MeshInstance3D]:
	var found: Array[MeshInstance3D] = []
	if node is MeshInstance3D:
		found.append(node)
	for child in node.get_children():
		found.append_array(meshes_under(child))
	return found

func nodes3d_under(node: Node) -> Array[Node3D]:
	var found: Array[Node3D] = []
	if node is Node3D:
		found.append(node)
	for child in node.get_children():
		found.append_array(nodes3d_under(child))
	return found

## Bounding box of every mesh under `node`, in `space`'s coordinates (pass null for global).
func merged_aabb(node: Node, space: Node3D) -> AABB:
	var box := AABB()
	var first := true
	for mi in meshes_under(node):
		var xform: Transform3D = mi.global_transform
		if space != null:
			xform = space.global_transform.affine_inverse() * xform
		var b: AABB = xform * mi.mesh.get_aabb()
		box = b if first else box.merge(b)
		first = false
	return box

func near(a: Vector3, b: Vector3) -> bool:
	return absf(a.x - b.x) <= TOL and absf(a.y - b.y) <= TOL and absf(a.z - b.z) <= TOL

func v(x: Vector3) -> Array:
	return [snappedf(x.x, 0.00001), snappedf(x.y, 0.00001), snappedf(x.z, 0.00001)]

func colour_close(a: Color, hex: String) -> bool:
	var b := Color(hex)
	return absf(a.r - b.r) * 255.0 <= 1.01 and absf(a.g - b.g) * 255.0 <= 1.01 and absf(a.b - b.b) * 255.0 <= 1.01

func run() -> void:
	# --- each .glb on its own, at the origin ---
	for asset in ASSETS:
		var spec: Dictionary = ASSETS[asset]
		var packed := load("res://assets/models/%s.glb" % asset) as PackedScene
		check(asset + ".loads", packed != null, {"path": "res://assets/models/%s.glb" % asset})
		if packed == null:
			continue
		var inst := packed.instantiate() as Node3D
		root.add_child(inst)
		await process_frame

		var box := merged_aabb(inst, inst)
		var exp_size: Vector3 = spec["max"] - spec["min"]
		check(asset + ".size_m", near(box.size, exp_size), {"aabb_size_xyz": v(box.size), "expected": v(exp_size)})
		check(asset + ".bounds_m", near(box.position, spec["min"]) and near(box.end, spec["max"]),
			{"min": v(box.position), "max": v(box.end), "x_range": [snappedf(box.position.x, 0.00001), snappedf(box.end.x, 0.00001)]})
		check(asset + ".origin_at_base", absf(box.position.y) <= TOL, {"aabb_min_y": snappedf(box.position.y, 0.000001)})
		var tallest := 0 if box.size.x >= box.size.y and box.size.x >= box.size.z else (1 if box.size.y >= box.size.z else 2)
		if spec["stands_on_y"]:
			check(asset + ".upright_tallest_axis_y", tallest == 1, {"tallest_axis": ["X", "Y", "Z"][tallest]})

		var transforms := []
		var all_identity := true
		for n in nodes3d_under(inst):
			var s := n.scale
			var r := n.rotation_degrees
			var t := n.position
			transforms.append({"node": String(n.name), "scale": v(s), "rotation_deg": v(r), "position": v(t)})
			if not (near(s, Vector3.ONE) and near(r, Vector3.ZERO) and near(t, Vector3.ZERO)):
				all_identity = false
		check(asset + ".node_scale_1_rotation_0", all_identity, {"nodes": transforms})

		var tris := 0
		var found := {}
		var colours_ok := true
		for mi in meshes_under(inst):
			for i in range(mi.mesh.get_surface_count()):
				var arrays: Array = mi.mesh.surface_get_arrays(i)
				var idx: PackedInt32Array = arrays[Mesh.ARRAY_INDEX] if arrays[Mesh.ARRAY_INDEX] != null else PackedInt32Array()
				var verts: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
				tris += (idx.size() if idx.size() > 0 else verts.size()) / 3
				var mat := mi.get_active_material(i)
				var albedo := Color.MAGENTA
				if mat is BaseMaterial3D:
					albedo = (mat as BaseMaterial3D).albedo_color
				found[mat.resource_name if mat else "<none>"] = albedo.to_html(false)
				var want = spec["colours"].get(mat.resource_name if mat else "", null)
				if want == null or not colour_close(albedo, want):
					colours_ok = false
		check(asset + ".triangles", tris <= spec["max_tris"], {"triangles": tris, "budget": spec["max_tris"]})
		check(asset + ".colours", colours_ok and found.size() == spec["colours"].size(),
			{"found": found, "expected": spec["colours"]})
		inst.queue_free()
		await process_frame

	# --- the asset room: one light, one camera, every asset resting on the Floor node ---
	var room_packed := load(ROOM) as PackedScene
	check("room.loads", room_packed != null, {"path": ROOM})
	if room_packed != null:
		var room := room_packed.instantiate() as Node3D
		root.add_child(room)
		await process_frame
		var lights := room.find_children("*", "Light3D", true, false)
		var cameras := room.find_children("*", "Camera3D", true, false)
		check("room.one_light", lights.size() == 1, {"lights": lights.map(func(n): return String(n.name))})
		check("room.one_camera", cameras.size() == 1, {"cameras": cameras.map(func(n): return String(n.name))})
		var floor := room.get_node_or_null("Floor") as MeshInstance3D
		check("room.has_floor", floor != null, {})
		if floor != null:
			var floor_box := merged_aabb(floor, null)
			var floor_y := floor_box.end.y
			for asset in ASSETS:
				var node := room.get_node_or_null(ASSETS[asset]["node"]) as Node3D
				if node == null:
					check(asset + ".in_room", false, {"missing_node": ASSETS[asset]["node"]})
					continue
				var b := merged_aabb(node, null)
				var over_floor := b.position.x >= floor_box.position.x and b.end.x <= floor_box.end.x \
					and b.position.z >= floor_box.position.z and b.end.z <= floor_box.end.z
				# measured against the Floor node's own top, not against the asset itself
				check(asset + ".rests_on_floor", absf(b.position.y - floor_y) <= TOL and over_floor,
					{"asset_min_y": snappedf(b.position.y, 0.000001), "floor_top_y": snappedf(floor_y, 0.000001),
					 "gap_m": snappedf(b.position.y - floor_y, 0.000001), "inside_floor_xz": over_floor,
					 "node_scale": v(node.scale), "global_position": v(node.global_position)})
		room.queue_free()
		await process_frame

	print("check_a3_assets: %d checks, %d failed" % [results.size(), failures])
	quit(1 if failures > 0 else 0)
