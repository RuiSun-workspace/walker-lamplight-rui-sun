"""Compose the 4K still images for the A3 film (Claude, 2026-10-15).

Every picture placed here is a real file with a recorded SHA-256 (assets/sources.json): Rui's own screenshots,
MCP `look` images Claude took from Rui's Blender session, Godot frames from the isolated capture build, the
A2 oil-drop sprite, and verbatim lines of capture/test-output.txt. Nothing is redrawn. Each panel carries a
burned-in provenance label.

    F:/7270/film-env/Scripts/python.exe make_assets.py
"""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parent
REPO = Path("C:/Users/18500/Desktop/7270/Assignment2/walker-lamplight-rui-sun")
SHOTS = Path("C:/Users/18500/Pictures/Screenshots")
LOOKS = Path("C:/Users/18500/.claude/projects/C--Users-18500-Desktop-7270-Assignment1/"
             "730d3bcf-f7af-4d79-a291-8251757baafd/tool-results")
W, H = 3840, 2160
GROUND, INK, MUTED, ACCENT = (250, 249, 245), (20, 20, 19), (94, 93, 89), (217, 119, 87)
F = "C:/Windows/Fonts/"
bold = lambda s: ImageFont.truetype(F + "segoeuib.ttf", s)
reg = lambda s: ImageFont.truetype(F + "segoeui.ttf", s)
mono = lambda s: ImageFont.truetype(F + "consola.ttf", s)
cjk = lambda s: ImageFont.truetype(F + "msyh.ttc", s)

SRC = {
    "rui_blender_notes": REPO / "docs/a3/blender-session.png",
    "rui_s1_prompt": SHOTS / "屏幕截图 2026-10-15 194200.png",
    "rui_s2_lamp_post": SHOTS / "屏幕截图 2026-10-15 194558.png",
    "rui_s3_flame_hex": SHOTS / "屏幕截图 2026-10-15 194826.png",
    "look_lamp_parts": LOOKS / "mcp-blender-blob-1792092756211-4flx8f.png",
    "look_lamp_joined": LOOKS / "mcp-blender-blob-1792093396538-ukgtpm.png",
    "look_drop_flat": LOOKS / "mcp-blender-blob-1792094391108-nzl577.png",
    "look_drop_highlight": LOOKS / "mcp-blender-blob-1792094615303-s7tsgs.png",
    "look_drop_welded": LOOKS / "mcp-blender-blob-1792094812484-s523tk.png",
    "look_pit_plain": LOOKS / "mcp-blender-blob-1792095126521-mto7tw.png",
    "look_pit_braced": LOOKS / "mcp-blender-blob-1792095356581-othnmp.png",
    "sprite_oil_drop": REPO / "godot/assets/env/oil_drop.png",
    "room_before": REEL / "_frames/room-front-before/f00000030.png",
    "room_after": REEL / "_frames/room-front-after/f00000030.png",
    "test_output": REEL / "capture/test-output.txt",
}
sources = {k: {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for k, p in SRC.items()}


def canvas(title, kicker):
    img = Image.new("RGB", (W, H), GROUND)
    d = ImageDraw.Draw(img)
    d.text((200, 150), kicker.upper(), font=bold(54), fill=ACCENT)
    d.text((200, 220), title, font=bold(104), fill=INK)
    return img, d


def label(d, x, y, text, gold=False):
    f = reg(46)
    w = d.textlength(text, font=f)
    d.rounded_rectangle([x, y, x + w + 64, y + 84], radius=20, fill=(12, 12, 18),
                        outline=(255, 207, 90) if gold else (154, 163, 191), width=4)
    d.text((x + 32, y + 12), text, font=f, fill=(255, 207, 90) if gold else (244, 241, 232))


def paste_fit(img, path, box, crop=None, nearest=False):
    """Fit an image inside box=(x, y, w, h), keep aspect, thin frame; returns the placed rectangle."""
    im = Image.open(path).convert("RGB")
    if crop:
        im = im.crop(crop)
    x, y, w, h = box
    s = min(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.NEAREST if nearest else Image.LANCZOS)
    px, py = x + (w - im.width) // 2, y + (h - im.height) // 2
    img.paste(im, (px, py))
    ImageDraw.Draw(img).rectangle([px - 3, py - 3, px + im.width + 2, py + im.height + 2], outline=(200, 198, 190), width=3)
    return px, py, im.width, im.height


def text_box(d, x, y, w, lines, size=50, font=None, line_h=None, fill=(30, 30, 34), ink=(236, 233, 224)):
    font = font or mono(size)
    line_h = line_h or int(size * 1.45)
    h = 70 + line_h * len(lines)
    d.rounded_rectangle([x, y, x + w, y + h], radius=24, fill=fill)
    for i, (t, c) in enumerate(lines):
        d.text((x + 44, y + 36 + i * line_h), t, font=font, fill=c or ink)
    return h


RED, GREEN, GOLD = (255, 120, 110), (120, 220, 140), (255, 207, 90)
out = REEL / "assets"
out.mkdir(exist_ok=True)

# B05 - Rui's interface screenshot + the registration line that failed as written
img, d = canvas("Learn the window, then connect", "B05 · Blender interface and MCP setup")
r = paste_fit(img, SRC["rui_blender_notes"], (200, 400, 2050, 1400))
label(d, r[0], r[1] + r[3] + 30, "Screenshot by Rui, 2026-10-15 · docs/a3/blender-session.png")
text_box(d, 2380, 430, 1260, [
    ("$ claude mcp add -e DISABLE_TELEMETRY=true \\", None),
    ("    blender -- uvx mcp-for-blender", None),
    ("Invalid environment variable format:", RED),
    ("blender, environment variables should", RED),
    ("be added as: -e KEY1=value1 ...", RED),
    ("exit=1", RED),
    ("", None),
    ("$ claude mcp add blender -s user \\", None),
    ("    -e DISABLE_TELEMETRY=true ... --", None),
    ("    uvx.exe mcp-for-blender@2.1.9", None),
    ("Added stdio MCP server blender", GREEN),
], size=40)
label(d, 2380, 1330, "Claude's run, 2026-10-14 · setup log", False)
img.save(out / "b05.png")

# B06 - Rui's real prompt in the Claude app + what the MCP built in Rui's Blender
img, d = canvas("One plan, one part per call", "B06 · prompt → build")
r = paste_fit(img, SRC["rui_s1_prompt"], (200, 400, 2000, 1440))
label(d, r[0], r[1] + r[3] + 30, "Screenshot by Rui, 2026-10-15 · the real prompt and Claude's replies")
r = paste_fit(img, SRC["look_lamp_parts"], (2330, 400, 1310, 1310))
label(d, r[0], r[1] + r[3] + 30, "MCP look capture from Rui's Blender session")
img.save(out / "b06.png")

# B07 - Rui's hand edit: the flame's Base Color, and the read-back
img, d = canvas("The hand edit, read back", "B07 · Rui's change in Blender's window")
r = paste_fit(img, SRC["rui_s3_flame_hex"], (200, 400, 2200, 1400), crop=(1000, 0, 2557, 1525))
label(d, r[0], r[1] + r[3] + 30, "Screenshot by Rui, 2026-10-15 (after the edit) · lp_flame Base Color, Hex FDFFA6")
text_box(d, 2560, 460, 1080, [
    ("read back, Base Color (sRGB)", (180, 180, 190)),
    ("", None),
    ("lp_flame  #ffcf5a -> #fdffa6", GOLD),
    ("  intended (Rui's edit)", (180, 180, 190)),
    ("", None),
    ("lp_glass  #241f2c -> #241c54", RED),
    ("  not intended -> reverted", (180, 180, 190)),
    ("  to #241f2c at Rui's request", (180, 180, 190)),
], size=44)
d.text((2560, 1230), "Rui: “我认为灯芯之前的颜色有点暗，", font=cjk(46), fill=INK)
d.text((2560, 1300), "所以换了一个更明亮的颜色”", font=cjk(46), fill=INK)
d.text((2560, 1380), "“The flame's colour was a little dark,", font=reg(44), fill=MUTED)
d.text((2560, 1440), "so I changed it to a brighter one.”", font=reg(44), fill=MUTED)
img.save(out / "b07.png")

# B08 - the oil drop argued into shape
img, d = canvas("The oil drop, argued into shape", "B08 · sprite → squash + cone → weld")
cols = [("sprite_oil_drop", "A2 sprite, 22×24 px (×20, nearest)", True),
        ("look_drop_flat", "squashed sphere + cone, flat · 94 tris", False),
        ("look_drop_highlight", "smooth + highlight ball · rejected by Rui", False),
        ("look_drop_welded", "welded, no seam · 64 tris", False)]
for i, (k, cap, nn) in enumerate(cols):
    x = 200 + i * 870
    r = paste_fit(img, SRC[k], (x, 420, 800, 1100), nearest=nn)
    d.text((x, 1560), cap, font=reg(42), fill=INK)
label(d, 200, 1680, "Images 2–4: MCP look captures from Rui's Blender session, 2026-10-15")
img.save(out / "b08.png")

# B09 - pit prop braces and Apply transforms
img, d = canvas("Braces, then Apply All Transforms", "B09 · pit prop")
r = paste_fit(img, SRC["look_pit_plain"], (200, 420, 1150, 1150))
d.text((200, 1600), "plain: reads like a door frame", font=reg(44), fill=INK)
r = paste_fit(img, SRC["look_pit_braced"], (1420, 420, 1150, 1150))
d.text((1420, 1600), "two 45° braces (Rui's choice)", font=reg(44), fill=INK)
text_box(d, 2680, 460, 960, [
    ("before Apply", (180, 180, 190)),
    ("pp_brace_left", None),
    ("  rot (0, -45, 0)", RED),
    ("  scale (0.5, 0.12, 0.08)", RED),
    ("", None),
    ("after Ctrl+A > All", (180, 180, 190)),
    ("pit_prop", None),
    ("  rot (0, 0, 0)", GREEN),
    ("  scale (1, 1, 1)", GREEN),
    ("  origin (0, 0, 0), on ground", GREEN),
], size=44)
label(d, 200, 1700, "MCP look captures + get_scene_info read-outs, Rui's Blender session, 2026-10-15")
img.save(out / "b09.png")

# B13 - verbatim headless output (selected lines, long lines cut at the right edge)
lines = (REEL / "capture/test-output.txt").read_text(encoding="utf-8").splitlines()
pick = [l for l in lines if l.startswith("check_a3_assets:") or l.startswith("check_glb:")]
rest = [l for l in lines if '"rests_on_floor"' in l or "rests_on_floor" in l and "PASS" in l]
fails = [l for l in lines if '"FAIL"' in l]
img, d = canvas("Headless: thirty checks, then three faults", "B13 · recorded output")
show = []
show.append(("$ godot --headless ... check_a3_assets.gd --fixed-fps 60", None))
for l in lines:
    if l.startswith('{"id":"lamp_post.size_m"') or l.startswith('{"id":"oil_drop.rests_on_floor"') and '"PASS"' in l:
        show.append((l[:118] + ("…" if len(l) > 118 else ""), GREEN))
show.append((pick[0], GREEN))
show.append(("$ python tools/check_glb.py", None))
show.append((pick[1], GREEN))
show.append(("", None))
show.append(("# deliberate faults, each in a throw-away copy", (180, 180, 190)))
f1 = next(l for l in lines if '"pit_prop.size_m"' in l and '"FAIL"' in l)
f2 = next(l for l in lines if '"oil_drop.rests_on_floor"' in l and '"FAIL"' in l)
f3 = next(l for l in lines if '"oil_drop.size_m"' in l and '"FAIL"' in l)
show.append(("1 +Y Up off:   " + f1[:100] + "…", RED))
show.append(("2 lifted 5 cm: " + f2[:100] + "…", RED))
show.append(("3 stale files: " + f3[:100] + "…", RED))
text_box(d, 200, 400, 3440, show, size=40)
label(d, 200, 1820, "Headless output · verbatim lines of capture/test-output.txt (long lines cut with …)", True)
img.save(out / "b13.png")

# B14 - before / after the human check
img, d = canvas("Right numbers, wrong look", "B14 · Rui's human check in Godot")
r = paste_fit(img, SRC["room_before"], (200, 520, 1680, 945))
label(d, r[0], r[1] + r[3] + 30, "Before · re-rendered from commit 8d07135 sources")
r = paste_fit(img, SRC["room_after"], (1960, 520, 1680, 945))
label(d, r[0], r[1] + r[3] + 30, "After · Godot 4.7.2, source 4b4b77f")
d.text((200, 380), "Rui: “出现在游戏中的油滴不可能这么小，我感觉木架有点偏大”", font=cjk(54), fill=INK)
d.text((200, 1700), "“The oil drop in the game can't be this small, and I feel the frame is a bit too big.”",
       font=reg(50), fill=MUTED)
d.text((200, 1790), "oil_drop 0.1375 × 0.15 m → 0.275 × 0.30 m (×2) · pit_prop 1.2 → 0.8 m wide, timber 0.16 → 0.12 m",
       font=reg(48), fill=INK)
img.save(out / "b14.png")

(out / "sources.json").write_text(json.dumps(sources, indent=1, ensure_ascii=False), encoding="utf-8")
print("wrote", sorted(p.name for p in out.glob("b*.png")))
