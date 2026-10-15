# export_glb.py - export one A3 asset .blend to binary glTF (.glb) for Godot.
#
#   blender -b blender/<asset>.blend --factory-startup --python-exit-code 1 \
#       --python tools/blender/export_glb.py -- godot/assets/models/<asset>.glb
#
# Run once per asset (lamp_post, oil_drop, pit_prop). Uses Blender's bundled glTF 2.0 exporter
# (io_scene_gltf2 5.1.20 in Blender 5.1.2) with +Y Up on - its default - so Blender's Z-up becomes
# Godot's Y-up. The whole file is exported: each asset .blend holds exactly one mesh object.
# Fails (exit 1 with --python-exit-code 1) if the file does not hold exactly one mesh, or if that
# mesh still has an unapplied transform, so a bad source never reaches Godot.
import os
import sys

import bpy

out = os.path.abspath(sys.argv[sys.argv.index("--") + 1])
objects = list(bpy.data.objects)
meshes = [o for o in objects if o.type == "MESH"]
if len(objects) != 1 or len(meshes) != 1:
    raise SystemExit("expected exactly one mesh object, found %s" % [(o.name, o.type) for o in objects])
obj = meshes[0]
if tuple(obj.location) != (0.0, 0.0, 0.0) or tuple(obj.rotation_euler) != (0.0, 0.0, 0.0) or tuple(obj.scale) != (1.0, 1.0, 1.0):
    raise SystemExit("%s has an unapplied transform: loc %s rot %s scale %s"
                     % (obj.name, tuple(obj.location), tuple(obj.rotation_euler), tuple(obj.scale)))

os.makedirs(os.path.dirname(out), exist_ok=True)
bpy.ops.export_scene.gltf(
    filepath=out,
    export_format='GLB',
    export_yup=True,
    use_selection=False,
    export_apply=True,
    export_materials='EXPORT',
    export_cameras=False,
    export_lights=False,
    export_animations=False,
    export_extras=False,
)
tris = sum(len(p.vertices) - 2 for p in obj.data.polygons)
print("EXPORTED", obj.name, "->", out, os.path.getsize(out), "bytes;", tris, "triangles;",
      "materials", [m.name for m in obj.data.materials])
