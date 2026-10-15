"""Read the A3 .glb files directly (no Blender, no Godot) and compare them with the brief.

    python tools/check_glb.py [folder with the three .glb files; default godot/assets/models]

An independent check between the two programs: it reads the glTF JSON chunk inside each .glb and reports
what the file itself says - node transforms (F4), the POSITION accessor's min/max in glTF's Y-up metres
(F1, F2, F3), triangle count from the index accessors (F5) and each material's baseColorFactor converted
back to sRGB hex (F6). glTF stores min/max for POSITION per primitive, so the size is the union of those
boxes. It cannot show how Godot imports the file; check_a3_assets.gd does that.
Expected values: docs/a3/CHANGE-BRIEF.md section 6, plus its section 9 revisions.
"""
import json
import os
import struct
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "godot", "assets", "models")
TOL = 0.001  # metres

# Godot / glTF axes: X width, Y height, Z depth.
EXPECTED = {
    "lamp_post": {"min": (-0.03125, 0.0, -0.04775), "max": (0.1625, 0.725, 0.04775), "max_tris": 72,
                  "colours": {"lp_timber": "#5a412a", "lp_brass": "#b8863b", "lp_glass": "#241f2c",
                              "lp_flame": "#fdffa6"}},
    "oil_drop": {"min": (-0.1375, 0.0, -0.1375), "max": (0.1375, 0.3, 0.1375), "max_tris": 120,  # x2, brief 9
                 "colours": {"od_oil": "#f2a93b"}},
    "pit_prop": {"min": (-0.4, 0.0, -0.06), "max": (0.4, 2.0, 0.06), "max_tris": 60,  # narrowed, brief 9
                 "colours": {"pp_timber": "#5a412a", "pp_timber_dark": "#3b2a1c"}},
}


def read_gltf_json(path):
    with open(path, "rb") as f:
        magic, version, _length = struct.unpack("<4sII", f.read(12))
        if magic != b"glTF" or version != 2:
            raise ValueError("%s is not a glTF 2.0 binary" % path)
        chunk_len, chunk_type = struct.unpack("<I4s", f.read(8))
        if chunk_type != b"JSON":
            raise ValueError("%s: first chunk is not JSON" % path)
        return json.loads(f.read(chunk_len))


def linear_to_srgb_hex(rgb):
    def one(c):
        c = max(0.0, min(1.0, c))
        return c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
    return "#" + "".join("%02x" % round(one(c) * 255) for c in rgb[:3])


results = []


def check(cid, passed, observed):
    results.append({"id": cid, "status": "PASS" if passed else "FAIL", "observed": observed})
    print(json.dumps(results[-1], ensure_ascii=False))


for name, exp in EXPECTED.items():
    g = read_gltf_json(os.path.join(ROOT, name + ".glb"))
    nodes = g.get("nodes", [])
    transforms = [{k: n[k] for k in ("translation", "rotation", "scale", "matrix") if k in n} for n in nodes]
    check(name + ".nodes_untransformed", all(not t for t in transforms),
          {"nodes": [n.get("name") for n in nodes], "transforms": transforms})

    lo, hi, tris = [float("inf")] * 3, [float("-inf")] * 3, 0
    for mesh in g["meshes"]:
        for prim in mesh["primitives"]:
            acc = g["accessors"][prim["attributes"]["POSITION"]]
            lo = [min(a, b) for a, b in zip(lo, acc["min"])]
            hi = [max(a, b) for a, b in zip(hi, acc["max"])]
            count = g["accessors"][prim["indices"]]["count"] if "indices" in prim else acc["count"]
            tris += count // 3
    size = [h - l for h, l in zip(hi, lo)]
    exp_size = [h - l for h, l in zip(exp["max"], exp["min"])]
    check(name + ".size_m", all(abs(a - b) <= TOL for a, b in zip(size, exp_size)),
          {"size_xyz": [round(v, 5) for v in size], "expected": [round(v, 5) for v in exp_size]})
    check(name + ".bounds_m", all(abs(a - b) <= TOL for a, b in zip(lo + hi, list(exp["min"]) + list(exp["max"]))),
          {"min": [round(v, 5) for v in lo], "max": [round(v, 5) for v in hi]})
    check(name + ".base_on_y0", abs(lo[1]) <= TOL, {"min_y": round(lo[1], 6)})
    check(name + ".triangles", tris <= exp["max_tris"], {"triangles": tris, "budget": exp["max_tris"]})

    found = {m.get("name"): linear_to_srgb_hex(m.get("pbrMetallicRoughness", {}).get("baseColorFactor", [1, 1, 1, 1]))
             for m in g.get("materials", [])}
    check(name + ".colours", found == exp["colours"], {"found": found, "expected": exp["colours"]})

failed = sum(r["status"] == "FAIL" for r in results)
print("check_glb: %d checks, %d failed" % (len(results), failed))
sys.exit(1 if failed else 0)
