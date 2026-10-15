# build_oil_drop.py - the execute_blender_code bodies Claude ran through the Blender MCP for oil_drop,
# copied verbatim and in order (A3, 2026-10-15, Blender 5.1.2, mcp-for-blender 2.1.9, add-on 1.8).
#
# Each "STEP n" block below was one execute_blender_code call in Rui's live Blender session. Between calls
# Claude ran get_scene_info (read-only) and, after step 2, look; those calls run no code and are not copied.
#
# Spec: docs/a3/CHANGE-BRIEF.md section 3.2, with one change Rui approved before building (2026-10-15):
# the lower body is a UV sphere squashed to 0.10 m tall instead of a round 0.1375 m sphere, so the 0.15 m
# drop has a real tip (the A2 sprite is a teardrop widest about 40 % up). Overall size, origin and budget
# are unchanged.
#
# Replay without a window (script route):
#   blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_oil_drop.py
# Step 0 saves to an absolute path on Rui's machine; change it (or skip the save) on a replay.


# ---------------------------------------------------------------------------------------------- STEP 0
# Step 0 - switch the open file to blender/oil_drop.blend FIRST (so a later Ctrl+S cannot overwrite
# lamp_post.blend with an empty scene), then empty the scene and set metric units.
import bpy, os

path = r"C:\Users\18500\Desktop\7270\Assignment2\walker-lamplight-rui-sun\blender\oil_drop.blend"
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
# Observed: was ...\blender\lamp_post.blend, now ...\blender\oil_drop.blend; empty; METRIC 1.0 METERS.
# git confirmed lamp_post.blend unchanged.


# ---------------------------------------------------------------------------------------------- STEP 1
# Step 1 - lower body: UV sphere 8 segments x 6 rings, radius 0.06875 m, centre (0, 0, 0.05), squashed in Z
# by 0.05 / 0.06875 so it is 0.1375 wide and 0.10 tall: bottom at z = 0, widest at z = 0.05.
import bpy, math

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

R = 0.06875
bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=6, radius=R, location=(0.0, 0.0, 0.05))
body = bpy.context.active_object
body.name = "od_body"
body.data.name = "od_body"
body.scale = (1.0, 1.0, 0.05 / R)  # scale is applied in step 3
body.data.materials.append(flat_material("od_oil", "f2a93b"))
bpy.context.view_layer.update()

ring_angles = sorted({round(math.degrees(math.atan2(v.co.y, v.co.x)) % 360, 3)
                      for v in body.data.vertices if abs(v.co.z) < 1e-6})
world = [body.matrix_world @ v.co for v in body.data.vertices]
print(body.name, "dims", tuple(round(d, 5) for d in body.dimensions), "loc", tuple(round(v, 5) for v in body.location),
      "scale", tuple(round(s, 5) for s in body.scale))
print("equator vertex angles (deg):", ring_angles)
print("world x %.5f..%.5f y %.5f..%.5f z %.5f..%.5f" % (min(p.x for p in world), max(p.x for p in world),
      min(p.y for p in world), max(p.y for p in world), min(p.z for p in world), max(p.z for p in world)))
print("faces", len(body.data.polygons), "triangles", sum(len(p.vertices) - 2 for p in body.data.polygons))
# Observed: dims (0.1375, 0.1375, 0.1); equator angles 0, 45 ... 315 (so the width is the full 0.1375, not
# 0.127 as it would be with vertices starting at 22.5 deg); z 0 .. 0.1; 48 faces, 80 triangles.


# ---------------------------------------------------------------------------------------------- STEP 2
# Step 2 - tip: cone, 8 vertices, base radius 0.05954 m at z = 0.075, apex at z = 0.15 (depth 0.075, centre z 0.1125),
# NGON base cap so the mesh stays closed. The cone is tangent to the squashed sphere, and its base circle should
# sit exactly on the sphere's second vertex ring (z 0.075, r 0.05954). Its vertices are rotated about Z, if needed,
# to line up with the sphere's (0, 45, 90 ... degrees) so the seam has no step.
import bpy, math

body = bpy.data.objects["od_body"]
ring2 = [body.matrix_world @ v.co for v in body.data.vertices if abs((body.matrix_world @ v.co).z - 0.075) < 1e-4]
print("sphere ring at z 0.075:", len(ring2), "verts, radius",
      round(sum(math.hypot(p.x, p.y) for p in ring2) / max(len(ring2), 1), 5),
      "angles", sorted(round(math.degrees(math.atan2(p.y, p.x)) % 360, 1) for p in ring2))

r_base = 0.05 * math.sqrt(1 - 0.5 ** 2) / 0.05 * 0.06875  # a * sin(60 deg) = 0.05954
bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=r_base, radius2=0.0, depth=0.075,
                                end_fill_type='NGON', location=(0.0, 0.0, 0.1125))
tip = bpy.context.active_object
tip.name = "od_tip"
tip.data.name = "od_tip"
tip.data.materials.append(bpy.data.materials["od_oil"])

base_angles = sorted(round(math.degrees(math.atan2(v.co.y, v.co.x)) % 360, 3)
                     for v in tip.data.vertices if math.hypot(v.co.x, v.co.y) > 1e-6)
print("cone base angles before:", base_angles)
offset = min(base_angles) % 45.0
if offset > 1e-3:
    tip.rotation_euler.z = math.radians(-offset)  # applied in step 3
bpy.context.view_layer.update()

world = [tip.matrix_world @ v.co for v in tip.data.vertices]
base = [p for p in world if abs(p.z - 0.075) < 1e-6]
print("rotation z (deg)", round(math.degrees(tip.rotation_euler.z), 3))
print("cone base angles after:", sorted(round(math.degrees(math.atan2(p.y, p.x)) % 360, 3) for p in base),
      "radius", round(sum(math.hypot(p.x, p.y) for p in base) / len(base), 5))
print(tip.name, "dims", tuple(round(d, 5) for d in tip.dimensions), "z %.5f..%.5f" % (min(p.z for p in world), max(p.z for p in world)))
print("faces", len(tip.data.polygons), "triangles", sum(len(p.vertices) - 2 for p in tip.data.polygons))
# Observed: sphere ring at z 0.075 = 8 verts, r 0.05954, angles 0 ... 315; cone base already at 0 ... 315,
# no rotation needed; cone base r 0.05954 - the cone's base ring lands exactly on the sphere's ring (no step).
# Cone 0.11908 x 0.11908 x 0.075, z 0.075 .. 0.15; 9 faces, 14 triangles. Total so far 94 triangles.


# ------------------------------------------------------------------------------ READ-ONLY: hand changes?
# Rui looked after step 2 and decided: "平滑着色，可以加高光小球试试" ("smooth shading; try adding the
# highlight ball"). Before changing anything, Claude read the scene back:
# Read-only: did anything change by hand since step 2? Transforms, size, shading and colours.
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
# Observed: od_body flat (0 / 48 smooth), od_tip already smooth (9 / 9) - not done by Claude's code, most
# likely Rui's Shade Smooth with only the tip selected (to confirm with Rui). Nothing else changed.


# --------------------------------------------------------------------------------------------- STEP 2b
# Step 2b - smooth shading on both parts (Rui: "平滑着色"). Same as Object > Shade Smooth: it only changes the
# normals used for lighting; no vertices or triangles are added. od_tip was already smooth when read back.
import bpy

for name in ("od_body", "od_tip"):
    mesh = bpy.data.objects[name].data
    before = sum(p.use_smooth for p in mesh.polygons)
    for p in mesh.polygons:
        p.use_smooth = True
    mesh.update()
    print(name, "smooth faces", before, "->", sum(p.use_smooth for p in mesh.polygons), "/", len(mesh.polygons),
          "triangles", sum(len(p.vertices) - 2 for p in mesh.polygons))
# Observed: od_body 0 -> 48 / 48, 80 triangles; od_tip 9 -> 9 / 9, 14 triangles.


# --------------------------------------------------------------------------------------------- STEP 2c
# Step 2c - highlight (Rui: "可以加高光小球试试" - "try adding the highlight ball"): UV sphere 6 segments x 3 rings
# (24 triangles, total 118 of the 120 budget), radius 0.012 m, colour #ffe08a (the sprite's highlight).
# Centre on the body's faceted surface at the front-right (azimuth -45 deg, the camera side in Blender's front view)
# at z 0.07, just above the widest point: there the body's vertex line is at r = 0.0614, so half the ball shows.
import bpy, math

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

r_surface = 0.0595 + 0.2 * (0.06875 - 0.0595)  # between the vertex rings at z 0.075 and z 0.05
a = math.radians(-45.0)
centre = (r_surface * math.cos(a), r_surface * math.sin(a), 0.07)
bpy.ops.mesh.primitive_uv_sphere_add(segments=6, ring_count=3, radius=0.012, location=centre)
hl = bpy.context.active_object
hl.name = "od_highlight"
hl.data.name = "od_highlight"
hl.data.materials.append(flat_material("od_highlight", "ffe08a"))
for p in hl.data.polygons:
    p.use_smooth = True
bpy.context.view_layer.update()

print(hl.name, "loc", tuple(round(v, 5) for v in hl.location), "dims", tuple(round(d, 5) for d in hl.dimensions),
      "triangles", sum(len(p.vertices) - 2 for p in hl.data.polygons))
pts = [o.matrix_world @ v.co for o in bpy.data.objects for v in o.data.vertices]
print("all parts x %.5f..%.5f y %.5f..%.5f z %.5f..%.5f" % (min(p.x for p in pts), max(p.x for p in pts),
      min(p.y for p in pts), max(p.y for p in pts), min(p.z for p in pts), max(p.z for p in pts)))
print("total triangles", sum(len(p.vertices) - 2 for o in bpy.data.objects for p in o.data.polygons))
# Observed: od_highlight at (0.04338, -0.04338, 0.07), 0.018 x 0.02078 x 0.024, 24 triangles; all parts still
# x/y -0.06875 .. 0.06875, z 0 .. 0.15 (overall size unchanged); total 118 triangles.


# --------------------------------------------------------------------------------------------- STEP 2d
# Rui looked at step 2c (Claude's look: the ball read as a stuck-on bead, not a highlight) and decided against it.
# Step 2d - remove the highlight ball (Rui: "感觉高光球有点丑，不要了吧" - "the highlight ball looks a bit ugly,
# drop it"). Deletes the object, its mesh and its now-unused material.
import bpy

hl = bpy.data.objects["od_highlight"]
mesh = hl.data
bpy.data.objects.remove(hl, do_unlink=True)
if mesh.users == 0:
    bpy.data.meshes.remove(mesh)
mat = bpy.data.materials.get("od_highlight")
if mat and mat.users == 0:
    bpy.data.materials.remove(mat)
bpy.context.view_layer.update()

pts = [o.matrix_world @ v.co for o in bpy.data.objects for v in o.data.vertices]
print("objects", [o.name for o in bpy.data.objects], "materials", [m.name for m in bpy.data.materials],
      "meshes", [m.name for m in bpy.data.meshes])
print("all parts x %.5f..%.5f y %.5f..%.5f z %.5f..%.5f" % (min(p.x for p in pts), max(p.x for p in pts),
      min(p.y for p in pts), max(p.y for p in pts), min(p.z for p in pts), max(p.z for p in pts)))
print("total triangles", sum(len(p.vertices) - 2 for o in bpy.data.objects for p in o.data.polygons))
# Observed: objects ['od_body', 'od_tip'], materials ['od_oil']; x/y -0.06875 .. 0.06875, z 0 .. 0.15; 94 triangles.


# ---------------------------------------------------------------------------------------------- STEP 3
# Claude's look after step 2b: smooth shading left a hard line where the cone meets the body (separate meshes do
# not share normals). Claude proposed welding; Rui: "焊接，消除交界线，然后做第 3 步" ("weld, remove the seam line,
# then do step 3").
# Step 3 - apply all transforms, join, and weld the seam (Rui: "焊接，消除交界线，然后做第 3 步").
# 1. Ctrl+A > All Transforms on both parts (applies the body's 0.727 Z squash; origins go to (0, 0, 0)).
# 2. Join into one object "oil_drop".
# 3. Delete the faces hidden inside the tip: the body's cap above its z 0.075 ring (24 triangles) and the
#    cone's base cap (6 triangles).
# 4. Merge by distance: the cone's 8 base vertices sit exactly on the body's z 0.075 ring, so they weld.
# 5. Smooth shading across the welded mesh, so no line shows at the seam.
import bpy, bmesh

body, tip = bpy.data.objects["od_body"], bpy.data.objects["od_tip"]
parts = [body, tip]
for obj in bpy.data.objects:
    obj.select_set(obj in parts)
bpy.context.view_layer.objects.active = body
with bpy.context.temp_override(selected_editable_objects=parts, selected_objects=parts, active_object=body, object=body):
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.join()

drop = bpy.context.view_layer.objects.active
drop.name = "oil_drop"
drop.data.name = "oil_drop"

eps = 1e-5
bm = bmesh.new()
bm.from_mesh(drop.data)
tris_before = sum(len(f.verts) - 2 for f in bm.faces)
hidden = [f for f in bm.faces
          if min(v.co.z for v in f.verts) > 0.075 - eps and max(v.co.z for v in f.verts) < 0.10 + eps]
removed = sum(len(f.verts) - 2 for f in hidden)
bmesh.ops.delete(bm, geom=hidden, context='FACES')
loose = [v for v in bm.verts if not v.link_faces]
bmesh.ops.delete(bm, geom=loose, context='VERTS')
verts_before = len(bm.verts)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=eps)
welded = verts_before - len(bm.verts)
for f in bm.faces:
    f.smooth = True
bm.to_mesh(drop.data)
bm.free()
drop.data.update()
bpy.context.view_layer.update()

print("objects", [o.name for o in bpy.data.objects], "| triangles", tris_before, "-", removed, "->",
      sum(len(p.vertices) - 2 for p in drop.data.polygons), "| loose verts removed", len(loose), "| welded", welded)
print(drop.name, "loc", tuple(drop.location), "rot", tuple(drop.rotation_euler), "scale", tuple(drop.scale))
xs = [v.co.x for v in drop.data.vertices]; ys = [v.co.y for v in drop.data.vertices]; zs = [v.co.z for v in drop.data.vertices]
print("dims", tuple(round(d, 6) for d in drop.dimensions))
print("x %.6f .. %.6f | y %.6f .. %.6f | z %.6f .. %.6f" % (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))
print("faces", len(drop.data.polygons), "verts", len(drop.data.vertices), "materials", [m.name for m in drop.data.materials],
      "smooth", sum(p.use_smooth for p in drop.data.polygons))
# Observed: triangles 94 - 30 -> 64; welded 8 (the FACES delete had already dropped the 9 orphaned verts);
# loc (0,0,0) rot (0,0,0) scale (1,1,1); dims (0.1375, 0.1375, 0.15); x/y -0.06875 .. 0.06875, z 0 .. 0.15;
# 40 faces (24 quads + 16 tris), 34 verts, all smooth. get_scene_info: on ground, 0 non-manifold, 0 boundary edges.


# ------------------------------------------------------------------------- READ-ONLY: F7 normals check
# Read-only check (F7): the welded drop is one closed convex shape, so every face normal must point away
# from its centre; a positive signed volume also means the normals face outward.
import bpy, bmesh
from mathutils import Vector

drop = bpy.data.objects["oil_drop"]
bm = bmesh.new()
bm.from_mesh(drop.data)
bmesh.ops.triangulate(bm, faces=bm.faces)
centre = sum((v.co for v in bm.verts), Vector()) / len(bm.verts)
inward = sum(1 for f in bm.faces if f.normal.dot(f.calc_center_median() - centre) <= 0)
volume = sum(f.verts[0].co.dot(f.verts[1].co.cross(f.verts[2].co)) for f in bm.faces) / 6.0
boundary = sum(1 for e in bm.edges if len(e.link_faces) != 2)
print("triangles", len(bm.faces), "inward-facing", inward, "signed volume %.7f m3" % volume, "non-2-face edges", boundary)
bm.free()
# Observed: triangles 64, inward-facing 0, signed volume +0.0009579 m3, non-2-face edges 0.


# ---------------------------------------------------------------------------------------------- STEP 4
# Step 4 - save the live scene to the oil_drop source file (already the open file since step 0).
import bpy, os

path = r"C:\Users\18500\Desktop\7270\Assignment2\walker-lamplight-rui-sun\blender\oil_drop.blend"
bpy.ops.wm.save_as_mainfile(filepath=path)
print("saved", bpy.data.filepath, os.path.getsize(path), "bytes; objects", [o.name for o in bpy.data.objects])
# Observed: 97,913 bytes; objects ['oil_drop']. Reopened headless: oil_drop at (0,0,0), scale 1,
# 0.1375 x 0.1375 x 0.15 m, z min 0, 64 triangles, 40/40 smooth, od_oil #f2a93b, METRIC 1.0.


# =============================================================================== REVISION R2 (2026-10-15)
# Rui's human check of the asset room in Godot: "出现在游戏中的油滴不可能这么小" ("the oil drop in the game can't be
# this small"). Claude showed that 0.15 m is the exact 160 px = 1 m conversion of the 24 px sprite (43 % of Wick's
# height) and offered x2, x1.5 or no change; Rui chose x2, done by Claude through the MCP. This deliberately breaks
# the 160 px = 1 m conversion for this one asset (brief section 9).
# On a headless replay of this whole file, SKIP STEP R2a: it opens the saved, already-revised oil_drop.blend, and R2b
# would then double it again. Replaying steps 0-4 and R2b gives the revised drop.

# --------------------------------------------------------------------------------------------- STEP R2a
# (pit_prop.blend was saved first; Rui's live session had it open.)
# Revision R2a - open blender/oil_drop.blend in the live session (pit_prop.blend was saved just before).
# Nothing runs after the load, because loading a file replaces all Blender data the script could hold.
import bpy
bpy.ops.wm.open_mainfile(filepath=r"C:\Users\18500\Desktop\7270\Assignment2\walker-lamplight-rui-sun\blender\oil_drop.blend")
# Observed: returned normally and the MCP connection survived the file load (get_scene_info then showed oil_drop.blend).


# --------------------------------------------------------------------------------------------- STEP R2b
# Revision R2b - oil_drop x2 (Rui's human check in Godot: "出现在游戏中的油滴不可能这么小" - "the oil drop in the
# game can't be this small"; Rui chose x2). Scale is about the object's origin (centre of the underside), so the
# base stays on z = 0. Then Apply Scale (Ctrl+A) so the node scale is 1 again, verify, and save.
import bpy, os

drop = bpy.data.objects["oil_drop"]
drop.scale = (2.0, 2.0, 2.0)
bpy.context.view_layer.update()
print("before apply: scale", tuple(drop.scale), "dims", tuple(round(d, 6) for d in drop.dimensions))
for o in bpy.data.objects:
    o.select_set(o is drop)
bpy.context.view_layer.objects.active = drop
with bpy.context.temp_override(selected_editable_objects=[drop], selected_objects=[drop], active_object=drop, object=drop):
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.context.view_layer.update()

xs = [v.co.x for v in drop.data.vertices]; ys = [v.co.y for v in drop.data.vertices]; zs = [v.co.z for v in drop.data.vertices]
print("after apply: loc", tuple(drop.location), "rot", tuple(drop.rotation_euler), "scale", tuple(drop.scale))
print("dims", tuple(round(d, 6) for d in drop.dimensions))
print("x %.6f .. %.6f | y %.6f .. %.6f | z %.6f .. %.6f" % (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))
print("faces", len(drop.data.polygons), "triangles", sum(len(p.vertices) - 2 for p in drop.data.polygons),
      "smooth", sum(p.use_smooth for p in drop.data.polygons))

path = r"C:\Users\18500\Desktop\7270\Assignment2\walker-lamplight-rui-sun\blender\oil_drop.blend"
bpy.ops.wm.save_as_mainfile(filepath=path)
print("saved", bpy.data.filepath, os.path.getsize(path), "bytes")
# Observed: before apply scale (2,2,2) dims (0.275, 0.275, 0.3); after apply loc/rot 0, scale 1, dims (0.275, 0.275, 0.3),
# x/y -0.1375 .. 0.1375, z 0 .. 0.3; 40 faces, 64 triangles, 40 smooth. Saved 97,430 bytes.
