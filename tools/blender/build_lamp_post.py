# build_lamp_post.py - the execute_blender_code bodies Claude ran through the Blender MCP for lamp_post,
# copied verbatim and in order (A3, 2026-10-15, Blender 5.1.2, mcp-for-blender 2.1.9, add-on 1.8).
#
# Each "STEP n" block below was one execute_blender_code call in Rui's live Blender session. Between calls
# Claude ran get_scene_info (read-only) and, after step 5, look; those calls run no code and are not copied.
# The repeated helper functions are kept because each call was sent as its own self-contained body.
#
# Spec: docs/a3/CHANGE-BRIEF.md section 3.1. Steps 6+ (apply transforms, join, origin) and any hand edit
# by Rui come later; the .blend file (blender/lamp_post.blend) is the source of truth after the hand edit.
#
# Replay without a window (script route):
#   blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_lamp_post.py


# ---------------------------------------------------------------------------------------------- STEP 0
# Step 0 - empty the scene (no file reload, so the MCP add-on keeps running) and set metric units.
import bpy

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

print("objects:", [o.name for o in bpy.data.objects])
print("meshes:", [m.name for m in bpy.data.meshes], "materials:", [m.name for m in bpy.data.materials],
      "lights:", [l.name for l in bpy.data.lights], "cameras:", [c.name for c in bpy.data.cameras])
print("units:", units.system, units.scale_length, units.length_unit)


# ---------------------------------------------------------------------------------------------- STEP 1
# Step 1 - Post: timber, 0.0625 x 0.0625 x 0.70 m, centre (0, 0, 0.35) so its underside sits on z = 0.
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
    obj.scale = dims  # a 1 m cube scaled to the part's size; scale is applied in step 6
    obj.data.materials.append(mat)
    return obj

post = box_part("lp_post", (0.0, 0.0, 0.35), (0.0625, 0.0625, 0.70), flat_material("lp_timber", "5a412a"))
print(post.name, "dims", tuple(round(d, 5) for d in post.dimensions), "loc", tuple(post.location),
      "scale", tuple(round(s, 5) for s in post.scale), "mat", post.data.materials[0].name)
# Observed: printed dims (1.0, 1.0, 1.0) - stale, the view layer had not been updated after the scale
# change. get_scene_info showed the real size. Steps 2-5 call view_layer.update() before printing.


# ---------------------------------------------------------------------------------------------- STEP 2
# Step 2 - Crossbar: timber, 0.1625 x 0.0625 x 0.0375 m, centre (0.05, 0, 0.70625); spans x -0.03125 ... 0.13125, z 0.6875 ... 0.725.
import bpy

def box_part(name, centre, dims, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=centre)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.name = name
    obj.scale = dims
    obj.data.materials.append(mat)
    return obj

bar = box_part("lp_crossbar", (0.05, 0.0, 0.70625), (0.1625, 0.0625, 0.0375), bpy.data.materials["lp_timber"])
bpy.context.view_layer.update()  # refresh so dimensions reflect the new scale before printing
print(bar.name, "dims", tuple(round(d, 5) for d in bar.dimensions), "loc", tuple(round(v, 5) for v in bar.location),
      "mat", bar.data.materials[0].name)


# ---------------------------------------------------------------------------------------------- STEP 3
# Step 3 - Lamp box: brass, 0.0875 x 0.0875 x 0.1125 m, centre (0.11875, 0, 0.63125); hangs under the crossbar, x 0.075 ... 0.1625, z 0.575 ... 0.6875.
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

box = box_part("lp_lamp_box", (0.11875, 0.0, 0.63125), (0.0875, 0.0875, 0.1125), flat_material("lp_brass", "b8863b"))
bpy.context.view_layer.update()
print(box.name, "dims", tuple(round(d, 5) for d in box.dimensions), "loc", tuple(round(v, 5) for v in box.location),
      "mat", box.data.materials[0].name)


# ---------------------------------------------------------------------------------------------- STEP 4
# Step 4 - Window: dark glass, 0.0625 x 0.0915 x 0.075 m, centre (0.11875, 0, 0.63125); 2 mm proud of the lamp box front and back, x 0.0875 ... 0.15, z 0.59375 ... 0.66875.
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

win = box_part("lp_window", (0.11875, 0.0, 0.63125), (0.0625, 0.0915, 0.075), flat_material("lp_glass", "241f2c"))
bpy.context.view_layer.update()
print(win.name, "dims", tuple(round(d, 5) for d in win.dimensions), "loc", tuple(round(v, 5) for v in win.location),
      "mat", win.data.materials[0].name)


# ---------------------------------------------------------------------------------------------- STEP 5
# Step 5 - Flame: flame yellow, 0.025 x 0.0955 x 0.05 m, centre (0.11875, 0, 0.63125); 2 mm proud of the window front and back, x 0.10625 ... 0.13125, z 0.60625 ... 0.65625.
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

flame = box_part("lp_flame", (0.11875, 0.0, 0.63125), (0.025, 0.0955, 0.05), flat_material("lp_flame", "ffcf5a"))
bpy.context.view_layer.update()
print(flame.name, "dims", tuple(round(d, 5) for d in flame.dimensions), "loc", tuple(round(v, 5) for v in flame.location),
      "mat", flame.data.materials[0].name)
print("materials:", {m.name: m.users for m in bpy.data.materials})


# ---------------------------------------------------------------------------------------- RUI'S HAND EDIT
# Not code. Between step 5 and step 6 Rui changed colours by hand in Blender's window (Rui: "我手动修改了
# 灯芯的颜色" - "I changed the flame's colour by hand"). The read-only call below recorded the result:
#   lp_flame  Base Color #ffcf5a -> #fdffa6 (viewport colour left at #ffcf5a)
#   lp_glass  Base Color #241f2c -> #241c54 (viewport colour left at #241f2c) - not mentioned by Rui; asked.
# Geometry was unchanged. Replaying this script therefore gives the PRE-edit colours; blender/lamp_post.blend
# holds the edited ones.


# ------------------------------------------------------------------------------ READ-ONLY: record the edit
# Read-only: record Rui's hand edit - compare every part and material with the step 1-5 values.
import bpy

def linear_to_srgb(c):
    c = max(0.0, min(1.0, c))
    return c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

def hexof(rgba):
    return "#" + "".join("%02x" % round(linear_to_srgb(v) * 255) for v in rgba[:3])

planned = {"lp_timber": "#5a412a", "lp_brass": "#b8863b", "lp_glass": "#241f2c", "lp_flame": "#ffcf5a"}
for mat in bpy.data.materials:
    bsdf = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None) if mat.use_nodes else None
    base = bsdf.inputs["Base Color"] if bsdf else None
    linked = base.is_linked if base else None
    print(mat.name, "users", mat.users, "| base", hexof(base.default_value) if base else None,
          "linked" if linked else "", "| viewport", hexof(mat.diffuse_color), "| planned", planned.get(mat.name),
          "| emission", tuple(round(v, 3) for v in bsdf.inputs["Emission Color"].default_value[:3]) if bsdf else None,
          round(bsdf.inputs["Emission Strength"].default_value, 3) if bsdf else None)
bpy.context.view_layer.update()
for obj in bpy.data.objects:
    print(obj.name, obj.type, "loc", tuple(round(v, 5) for v in obj.location), "rot", tuple(round(v, 5) for v in obj.rotation_euler),
          "dims", tuple(round(v, 5) for v in obj.dimensions), "mats", [m.name for m in obj.data.materials] if obj.type == "MESH" else None)


# ---------------------------------------------------------------------------------------------- STEP 6
# Step 6 - apply all transforms (Ctrl+A > All Transforms), join the five parts into one object "lamp_post",
# origin at the world origin = centre of the post's underside. Materials (incl. Rui's hand edit) are untouched.
import bpy

parts = [bpy.data.objects[n] for n in ("lp_post", "lp_crossbar", "lp_lamp_box", "lp_window", "lp_flame")]
post = parts[0]
for obj in bpy.data.objects:
    obj.select_set(obj in parts)
bpy.context.view_layer.objects.active = post

with bpy.context.temp_override(selected_editable_objects=parts, selected_objects=parts, active_object=post, object=post):
    # location too: every part's origin moves to (0, 0, 0), which is where the joined object's origin must be
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.join()

lamp = bpy.context.view_layer.objects.active
lamp.name = "lamp_post"
lamp.data.name = "lamp_post"
bpy.context.view_layer.update()

xs = [v.co.x for v in lamp.data.vertices]; ys = [v.co.y for v in lamp.data.vertices]; zs = [v.co.z for v in lamp.data.vertices]
tris = sum(len(p.vertices) - 2 for p in lamp.data.polygons)
print("objects:", [o.name for o in bpy.data.objects])
print(lamp.name, "loc", tuple(lamp.location), "rot", tuple(lamp.rotation_euler), "scale", tuple(lamp.scale))
print("dims", tuple(round(d, 6) for d in lamp.dimensions))
print("x %.6f .. %.6f | y %.6f .. %.6f | z %.6f .. %.6f" % (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))
print("faces", len(lamp.data.polygons), "triangles", tris, "materials", [m.name for m in lamp.data.materials])
# Observed: loc (0,0,0) rot (0,0,0) scale (1,1,1); dims (0.19375, 0.0955, 0.725);
# x -0.03125 .. 0.1625 | y -0.04775 .. 0.04775 | z 0 .. 0.725; 30 faces, 60 triangles - all as the brief.


# ------------------------------------------------------------------------- READ-ONLY: F7 normals check
# Read-only check (F7): every face normal must point away from its own part's centre (no flipped faces).
import bpy, bmesh
from mathutils import Vector

lamp = bpy.data.objects["lamp_post"]
bm = bmesh.new()
bm.from_mesh(lamp.data)
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


# --------------------------------------------------------------------------------------------- STEP 7a
# Rui confirmed the lp_glass change was NOT intended ("玻璃窗不是我有意改的，请改回 #241f2c" - "the window
# change was not intentional, please change it back to #241f2c"). The flame edit (#fdffa6) is intended and kept.
# Step 7a - revert the accidental change to lp_glass (Rui: "玻璃窗不是我有意改的，请改回 #241f2c").
# Only lp_glass's Base Color is touched; Rui's intended flame edit (#fdffa6) stays.
import bpy

def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def linear_to_srgb(c):
    c = max(0.0, min(1.0, c))
    return c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

def hexof(rgba):
    return "#" + "".join("%02x" % round(linear_to_srgb(v) * 255) for v in rgba[:3])

glass = bpy.data.materials["lp_glass"]
bsdf = next(n for n in glass.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
before = hexof(bsdf.inputs["Base Color"].default_value)
rgb = [srgb_to_linear(int("241f2c"[i:i + 2], 16) / 255) for i in (0, 2, 4)]
bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
print("lp_glass base", before, "->", hexof(bsdf.inputs["Base Color"].default_value))

for mat in bpy.data.materials:
    b = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    print(mat.name, "base", hexof(b.inputs["Base Color"].default_value), "viewport", hexof(mat.diffuse_color))
# Observed in Rui's session: lp_glass base #241c54 -> #241f2c; final Base Colors: brass #b8863b,
# flame #fdffa6 (Rui's hand edit), glass #241f2c, timber #5a412a. Viewport colour of lp_flame still #ffcf5a.


# --------------------------------------------------------------------------------------------- STEP 7b
# Step 7b - save the live scene as the lamp_post source file (Rui: "请用代码把当前场景存到 blender/lamp_post.blend").
import bpy, os

path = r"C:\Users\18500\Desktop\7270\Assignment2\walker-lamplight-rui-sun\blender\lamp_post.blend"
os.makedirs(os.path.dirname(path), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=path)
print("saved", bpy.data.filepath, os.path.getsize(path), "bytes", "dirty" if bpy.data.is_dirty else "clean")
print("objects", [o.name for o in bpy.data.objects])
# Observed: saved 106,376 bytes; objects ['lamp_post']. The printed "dirty" flag was stale; reopening the
# file headless showed lamp_post at (0,0,0), scale 1, 0.19375 x 0.0955 x 0.725 m, 60 triangles, flame #fdffa6,
# glass #241f2c, METRIC 1.0. NOTE: the absolute path is Rui's machine; on a replay change it or skip this step.
