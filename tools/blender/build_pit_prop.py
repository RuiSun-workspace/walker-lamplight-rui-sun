# build_pit_prop.py - the execute_blender_code bodies Claude ran through the Blender MCP for pit_prop,
# copied verbatim and in order (A3, 2026-10-15, Blender 5.1.2, mcp-for-blender 2.1.9, add-on 1.8).
#
# Each "STEP n" block below was one execute_blender_code call in Rui's live Blender session. Between calls
# Claude ran get_scene_info (read-only) and, after step 3, look; those calls run no code and are not copied.
#
# Spec: docs/a3/CHANGE-BRIEF.md section 3.3.
#
# Replay without a window (script route):
#   blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_pit_prop.py
# Step 0 saves to an absolute path on Rui's machine; change it (or skip the save) on a replay.


# ---------------------------------------------------------------------------------------------- STEP 0
# Step 0 - switch the open file to blender/pit_prop.blend FIRST (so a later Ctrl+S cannot overwrite
# oil_drop.blend with an empty scene), then empty the scene and set metric units.
import bpy, os

path = r"C:\Users\18500\Desktop\7270\Assignment2\walker-lamplight-rui-sun\blender\pit_prop.blend"
print("was", bpy.data.filepath)
bpy.ops.wm.save_as_mainfile(filepath=path)

for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras):
    for block in list(coll):
        if block.users == 0:
            coll.remove(block)

units = bpy.context.scene.unit_settings
units.system = 'METRIC'
units.scale_length = 1.0
units.length_unit = 'METERS'

print("now", bpy.data.filepath)
print("objects:", [o.name for o in bpy.data.objects], "meshes:", [m.name for m in bpy.data.meshes],
      "materials:", [m.name for m in bpy.data.materials])
print("units:", units.system, units.scale_length, units.length_unit)
# Observed: was ...\blender\oil_drop.blend, now ...\blender\pit_prop.blend; empty; METRIC 1.0 METERS.
# git confirmed oil_drop.blend and lamp_post.blend unchanged.


# ---------------------------------------------------------------------------------------------- STEP 1
# Step 1 - left post: timber, 0.16 x 0.16 x 1.84 m, centre (-0.52, 0, 0.92); spans x -0.6 ... -0.44, z 0 ... 1.84.
import bpy

def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def flat_material(name, hex_srgb):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    rgb = [srgb_to_linear(int(hex_srgb[i:i + 2], 16) / 255) for i in (0, 2, 4)]
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.8
    bsdf.inputs["Metallic"].default_value = 0.0
    mat.diffuse_color = (*rgb, 1.0)  # viewport (Solid) colour only; the export reads Base Color
    return mat

def box_part(name, centre, dims, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=centre)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.name = name
    obj.scale = dims  # a 1 m cube scaled to the part's size; scale is applied in step 4
    obj.data.materials.append(mat)
    return obj

left = box_part("pp_post_left", (-0.52, 0.0, 0.92), (0.16, 0.16, 1.84), flat_material("pp_timber", "5a412a"))
bpy.context.view_layer.update()
print(left.name, "dims", tuple(round(d, 5) for d in left.dimensions), "loc", tuple(round(v, 5) for v in left.location),
      "mat", left.data.materials[0].name)
# Observed: dims (0.16, 0.16, 1.84) loc (-0.52, 0, 0.92) mat pp_timber; get_scene_info "on ground".


# ---------------------------------------------------------------------------------------------- STEP 2
# Step 2 - right post: timber, 0.16 x 0.16 x 1.84 m, centre (0.52, 0, 0.92); spans x 0.44 ... 0.6, z 0 ... 1.84.
import bpy

def box_part(name, centre, dims, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=centre)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.name = name
    obj.scale = dims
    obj.data.materials.append(mat)
    return obj

right = box_part("pp_post_right", (0.52, 0.0, 0.92), (0.16, 0.16, 1.84), bpy.data.materials["pp_timber"])
bpy.context.view_layer.update()
print(right.name, "dims", tuple(round(d, 5) for d in right.dimensions), "loc", tuple(round(v, 5) for v in right.location),
      "mat", right.data.materials[0].name)
# Observed: dims (0.16, 0.16, 1.84) loc (0.52, 0, 0.92) mat pp_timber; get_scene_info "on ground".


# ---------------------------------------------------------------------------------------------- STEP 3
# Step 3 - cap beam: dark timber, 1.2 x 0.16 x 0.16 m, centre (0, 0, 1.92); spans x -0.6 ... 0.6, z 1.84 ... 2.0,
# resting on both posts.
import bpy

def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def flat_material(name, hex_srgb):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    rgb = [srgb_to_linear(int(hex_srgb[i:i + 2], 16) / 255) for i in (0, 2, 4)]
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.8
    bsdf.inputs["Metallic"].default_value = 0.0
    mat.diffuse_color = (*rgb, 1.0)
    return mat

def box_part(name, centre, dims, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=centre)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.name = name
    obj.scale = dims
    obj.data.materials.append(mat)
    return obj

cap = box_part("pp_cap", (0.0, 0.0, 1.92), (1.2, 0.16, 0.16), flat_material("pp_timber_dark", "3b2a1c"))
bpy.context.view_layer.update()
print(cap.name, "dims", tuple(round(d, 5) for d in cap.dimensions), "loc", tuple(round(v, 5) for v in cap.location),
      "mat", cap.data.materials[0].name)
pts = [o.matrix_world @ v.co for o in bpy.data.objects for v in o.data.vertices]
print("all parts x %.5f..%.5f y %.5f..%.5f z %.5f..%.5f" % (min(p.x for p in pts), max(p.x for p in pts),
      min(p.y for p in pts), max(p.y for p in pts), min(p.z for p in pts), max(p.z for p in pts)))
print("total triangles", sum(len(p.vertices) - 2 for o in bpy.data.objects for p in o.data.polygons),
      "materials", {m.name: m.users for m in bpy.data.materials})
# Observed: dims (1.2, 0.16, 0.16) loc (0, 0, 1.92) mat pp_timber_dark; all parts x -0.6 .. 0.6,
# y -0.08 .. 0.08, z 0 .. 2.0; 36 triangles; materials pp_timber x2, pp_timber_dark x1.


# ------------------------------------------------------------------------------ READ-ONLY: hand changes?
# Rui looked after step 3 (Claude's description: it could read as a door frame or a goal) and decided:
# "加两根斜撑试试" ("try adding two braces"). Before changing anything, Claude read the scene back:
# Read-only: did anything change by hand since step 3? Transforms, size, shading and colours.
import bpy

def linear_to_srgb(c):
    c = max(0.0, min(1.0, c))
    return c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

def hexof(rgba):
    return "#" + "".join("%02x" % round(linear_to_srgb(v) * 255) for v in rgba[:3])

bpy.context.view_layer.update()
for obj in bpy.data.objects:
    smooth = sum(p.use_smooth for p in obj.data.polygons) if obj.type == "MESH" else None
    print(obj.name, "loc", tuple(round(v, 5) for v in obj.location), "rot", tuple(round(v, 5) for v in obj.rotation_euler),
          "scale", tuple(round(v, 5) for v in obj.scale), "dims", tuple(round(v, 5) for v in obj.dimensions),
          "smooth faces", smooth, "/", len(obj.data.polygons), "mods", [m.type for m in obj.modifiers])
for mat in bpy.data.materials:
    b = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    print(mat.name, "users", mat.users, "base", hexof(b.inputs["Base Color"].default_value), "viewport", hexof(mat.diffuse_color))
print("file", bpy.data.filepath)
# Observed: the three parts exactly as steps 1-3 left them; colours as planned. No hand change.


# --------------------------------------------------------------------------------------------- STEP 3b
# Step 3b - two corner braces (Rui: "加两根斜撑试试" - "try adding two braces"). Timber, cross-section 0.08 (in the
# frame's plane) x 0.12 (depth), at 45 degrees, each joining a post's inner face 0.3 m below the beam to the beam's
# underside 0.3 m in from the post. The contact points are 0.3 * sqrt(2) = 0.4243 m apart; each end is pushed 0.04 m
# further into the post / beam (half the 0.08 thickness), so no triangular gap shows where the 45-degree end meets
# the face: length 0.5043 m. Rotation about Y is left unapplied until step 4 (where F4 is checked).
import bpy, math

def box_part(name, centre, dims, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=centre)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.name = name
    obj.scale = dims
    obj.data.materials.append(mat)
    return obj

leg = 0.3
length = leg * math.sqrt(2) + 2 * 0.04
timber = bpy.data.materials["pp_timber"]
# left: from (-0.44, 1.54) on the post to (-0.14, 1.84) under the beam; right is the mirror image
left = box_part("pp_brace_left", (-0.44 + leg / 2, 0.0, 1.84 - leg / 2), (length, 0.12, 0.08), timber)
left.rotation_euler.y = math.radians(-45.0)
right = box_part("pp_brace_right", (0.44 - leg / 2, 0.0, 1.84 - leg / 2), (length, 0.12, 0.08), timber)
right.rotation_euler.y = math.radians(45.0)
bpy.context.view_layer.update()

for b in (left, right):
    w = [b.matrix_world @ v.co for v in b.data.vertices]
    print(b.name, "loc", tuple(round(v, 5) for v in b.location), "rot y", round(math.degrees(b.rotation_euler.y), 3),
          "x %.5f..%.5f y %.5f..%.5f z %.5f..%.5f" % (min(p.x for p in w), max(p.x for p in w), min(p.y for p in w),
          max(p.y for p in w), min(p.z for p in w), max(p.z for p in w)))
pts = [o.matrix_world @ v.co for o in bpy.data.objects for v in o.data.vertices]
print("all parts x %.5f..%.5f y %.5f..%.5f z %.5f..%.5f" % (min(p.x for p in pts), max(p.x for p in pts),
      min(p.y for p in pts), max(p.y for p in pts), min(p.z for p in pts), max(p.z for p in pts)))
print("objects", len(bpy.data.objects), "total triangles", sum(len(p.vertices) - 2 for o in bpy.data.objects for p in o.data.polygons))
# Observed: left brace (-0.29, 0, 1.69) rot y -45, x -0.49657 .. -0.08343, z 1.48343 .. 1.89657; right brace mirrored;
# all parts still x -0.6 .. 0.6, y -0.08 .. 0.08, z 0 .. 2.0; 5 objects, 60 triangles (= the 60 budget).


# ---------------------------------------------------------------------------------------------- STEP 4
# Rui: "斜撑可以，继续第 4 步" ("the braces are fine, go on to step 4"). A read-only get_scene_info first showed no
# hand change: braces at rot (0, -45, 0) / (0, 45, 0), scale (0.5, 0.12, 0.08) - the unapplied state F4 is about.
# Step 4 - apply all transforms (Ctrl+A > All Transforms: bakes the posts' and beam's scale and the braces'
# +/-45 degree rotation into the mesh), join the five parts into one object "pit_prop", origin at the world
# origin = centre of the underside, midway between the posts.
import bpy

names = ("pp_post_left", "pp_post_right", "pp_cap", "pp_brace_left", "pp_brace_right")
parts = [bpy.data.objects[n] for n in names]
active = parts[0]
for obj in bpy.data.objects:
    obj.select_set(obj in parts)
bpy.context.view_layer.objects.active = active
with bpy.context.temp_override(selected_editable_objects=parts, selected_objects=parts, active_object=active, object=active):
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.join()

frame = bpy.context.view_layer.objects.active
frame.name = "pit_prop"
frame.data.name = "pit_prop"
bpy.context.view_layer.update()

xs = [v.co.x for v in frame.data.vertices]; ys = [v.co.y for v in frame.data.vertices]; zs = [v.co.z for v in frame.data.vertices]
print("objects:", [o.name for o in bpy.data.objects])
print(frame.name, "loc", tuple(frame.location), "rot", tuple(frame.rotation_euler), "scale", tuple(frame.scale))
print("dims", tuple(round(d, 6) for d in frame.dimensions))
print("x %.6f .. %.6f | y %.6f .. %.6f | z %.6f .. %.6f" % (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))
print("faces", len(frame.data.polygons), "triangles", sum(len(p.vertices) - 2 for p in frame.data.polygons),
      "materials", [m.name for m in frame.data.materials])
# Observed: objects ['pit_prop']; loc (0,0,0) rot (0,0,0) scale (1,1,1); dims (1.2, 0.16, 2.0);
# x -0.6 .. 0.6 | y -0.08 .. 0.08 | z 0 .. 2.0; 30 faces, 60 triangles; get_scene_info: on ground,
# 0 non-manifold, 0 boundary edges, 0 loose verts.


# ------------------------------------------------------------------------- READ-ONLY: F7 normals check
# Read-only check (F7): every face normal must point away from its own part's centre (no flipped faces);
# the braces were rotated, so this also confirms the rotation was baked without mirroring anything.
import bpy, bmesh
from mathutils import Vector

frame = bpy.data.objects["pit_prop"]
bm = bmesh.new()
bm.from_mesh(frame.data)
islands, seen = [], set()
for f in bm.faces:
    if f.index in seen:
        continue
    stack, isl = [f], []
    while stack:
        g = stack.pop()
        if g.index in seen:
            continue
        seen.add(g.index); isl.append(g)
        for e in g.edges:
            stack.extend(lf for lf in e.link_faces if lf.index not in seen)
    islands.append(isl)
inward = 0
for isl in islands:
    centre = sum((f.calc_center_median() for f in isl), Vector()) / len(isl)
    inward += sum(1 for f in isl if f.normal.dot(f.calc_center_median() - centre) <= 0)
print("parts", len(islands), "faces", len(bm.faces), "inward-facing", inward)
bm.free()
# Observed: parts 5, faces 30, inward-facing 0.


# ---------------------------------------------------------------------------------------------- STEP 5
# Step 5 - save the live scene to the pit_prop source file (already the open file since step 0).
import bpy, os

path = r"C:\Users\18500\Desktop\7270\Assignment2\walker-lamplight-rui-sun\blender\pit_prop.blend"
bpy.ops.wm.save_as_mainfile(filepath=path)
print("saved", bpy.data.filepath, os.path.getsize(path), "bytes; objects", [o.name for o in bpy.data.objects])
# Observed: 98,664 bytes; objects ['pit_prop']. Reopened headless: pit_prop at (0,0,0), rot 0, scale 1,
# 1.2 x 0.16 x 2.0 m, x -0.6 .. 0.6, z min 0, 60 triangles, pp_timber #5a412a, pp_timber_dark #3b2a1c, METRIC 1.0.
