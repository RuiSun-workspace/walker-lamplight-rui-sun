"""Generate Wick's character-sheet images (SVG, rasterised to PNG with headless Chrome).

Hand-written by Claude (no generative model). This is the *contract* the generated pixel
sprites are judged against, so every number here is also written into CHARACTER-SHEET.md.

Units: 1 unit = 1 on-screen pixel in the 640x360 game viewport. Origin = Wick's feet,
centred, y up is negative (same convention as the Godot player, whose collider is the
18x28 rectangle (-9,-28)-(9,0) inherited from walker-jumpman).

    python design/character/src/make_character_sheet.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]

# ---- palette (the six character colours) --------------------------------------------
BRASS = "#b8863b"    # frame, cap, base, handle, limbs
GLASS = "#241f2c"    # dark glass behind the flame
FLAME = "#ffcf5a"    # flame body
CORE = "#fff1b8"     # flame core
EMBER = "#e2552f"    # low-oil coal / hurt flame
INK = "#2a1a10"      # eyes and mouth
CHARACTER = [("brass", BRASS), ("glass", GLASS), ("flame", FLAME),
             ("core", CORE), ("ember", EMBER), ("ink", INK)]
# ---- environment colours Wick must stay visible against ------------------------------
ENVIRONMENT = [("cave dark", "#0b0b10"), ("rock", "#2a2e3d"), ("rock edge", "#4a5068"),
               ("lit rock", "#6b5a44"), ("timber", "#3b2a1c"), ("daylight", "#dfeaf5")]

COLLIDER = (-9, -28, 18, 28)
FONT = 'font-family="Consolas, Menlo, monospace"'

# legs/arms are polylines from fixed attachment points: legs (±4,-6), arms (±8,-17/-18)
LEGS = {
    "idle": [[(-4, -6), (-5, 0)], [(4, -6), (5, 0)]],
    "walk": [[(-4, -6), (-8, 0)], [(4, -6), (7, -1)]],
    "jump": [[(-4, -6), (-7, -2)], [(4, -6), (2, -1)]],
    "fall": [[(-4, -6), (-6, 1)], [(4, -6), (6, 1)]],
    "land": [[(-4, -6), (-8, -3), (-6, 0)], [(4, -6), (8, -3), (6, 0)]],
    "hurt": [[(-4, -6), (-9, -1)], [(4, -6), (9, -3)]],
    "climb": [[(-4, -6), (-5, 0)], [(4, -6), (6, -4)]],
    "side": [[(-1, -6), (-3, 0)], [(1, -6), (3, 0)]],
}
ARMS = {
    "idle": [[(-8, -17), (-12, -11)], [(8, -17), (12, -11)]],
    "walk": [[(-8, -17), (-12, -20)], [(8, -17), (13, -13)]],
    "up": [[(-8, -18), (-14, -25)], [(8, -18), (14, -25)]],
    "out": [[(-8, -18), (-15, -21)], [(8, -18), (15, -21)]],
    "hurt": [[(-8, -17), (-15, -14)], [(8, -17), (14, -23)]],
    "reach": [[(-8, -17), (-12, -11)], [(8, -17), (15, -20)]],
    "hip": [[(-8, -17), (-11, -11)], [(8, -17), (12, -14), (8, -11)]],
    "side": [[(1, -17), (4, -11)]],
}
# pose -> legs, arms, flame, view
POSES = {
    "idle": ("idle", "idle", "full", "three"),
    "bored": ("idle", "hip", "bored", "three"),
    "walk": ("walk", "walk", "full", "three"),
    "jump": ("jump", "up", "full", "three"),
    "fall": ("fall", "out", "stretch", "three"),
    "land": ("land", "idle", "squash", "three"),
    "pickup": ("idle", "reach", "big", "three"),
    "ember": ("walk", "idle", "ember", "three"),
    "hurt": ("hurt", "hurt", "hurt", "three"),
    "respawn": ("idle", "idle", "kindle", "three"),
    "celebrate": ("idle", "up", "joy", "three"),
    "climb": ("climb", "up", "full", "back"),  # added 2026-10-06: ladder is in the slice
}


def eyes(view, y=-15.0, style="dot"):
    xs = {"front": (-1.3, 1.3), "three": (0.3, 2.9), "side": (2.6,)}.get(view, ())
    out = []
    for x in xs:
        if style == "dot":
            out.append(f'<circle cx="{x}" cy="{y}" r="0.95" fill="{INK}"/>')
        elif style == "lid":
            out.append(f'<path d="M{x - 0.8},{y} h1.6" stroke="{INK}" stroke-width="0.7"/>')
        elif style == "x":
            out.append(f'<path d="M{x - 0.8},{y - 0.8} l1.6,1.6 M{x + 0.8},{y - 0.8} l-1.6,1.6" '
                       f'stroke="{INK}" stroke-width="0.6"/>')
        elif style == "wide":
            out.append(f'<circle cx="{x}" cy="{y}" r="1.25" fill="{INK}"/>'
                       f'<circle cx="{x + 0.35}" cy="{y - 0.35}" r="0.4" fill="{CORE}"/>')
        elif style == "joy":
            out.append(f'<path d="M{x - 0.9},{y + 0.4} Q{x},{y - 1} {x + 0.9},{y + 0.4}" '
                       f'stroke="{INK}" stroke-width="0.7" fill="none"/>')
        elif style == "up":
            out.append(f'<circle cx="{x + 0.3}" cy="{y - 0.5}" r="0.8" fill="{INK}"/>'
                       f'<path d="M{x - 0.9},{y - 1.2} h1.8" stroke="{INK}" stroke-width="0.6"/>')
    return "".join(out)


def flame(kind, view):
    face = view != "back"
    def body(d_out, d_in, col=FLAME):
        return f'<path d="{d_out}" fill="{col}"/>' + (f'<path d="{d_in}" fill="{CORE}"/>' if d_in else "")
    full_o = "M0,-23 C5,-18 5,-11 0,-9 C-5,-11 -5,-18 0,-23Z"
    full_i = "M0,-19 C2.5,-16 2.5,-12 0,-11 C-2.5,-12 -2.5,-16 0,-19Z"
    if kind == "full":
        return body(full_o, full_i) + (eyes(view) if face else "")
    if kind == "big" or kind == "joy":
        s = body("M0,-31 C7,-21 6,-11 0,-9 C-6,-11 -7,-21 0,-31Z", "M0,-24 C3,-18 3,-12 0,-11 C-3,-12 -3,-18 0,-24Z")
        mouth = (f'<path d="M0.3,-13.6 Q1.7,-12.2 3,-13.6" stroke="{INK}" stroke-width="0.7" fill="none"/>')
        return s + eyes(view, -16, "joy" if kind == "joy" else "dot") + mouth
    if kind == "stretch":
        return body("M0,-26 C4,-19 4,-11 0,-9 C-4,-11 -4,-19 0,-26Z", "M0,-21 C2,-17 2,-12 0,-11 C-2,-12 -2,-17 0,-21Z") \
            + eyes(view, -15, "wide")
    if kind == "squash":
        return body("M0,-19 C6,-16 6,-11 0,-9 C-6,-11 -6,-16 0,-19Z", "M0,-16 C3,-14 3,-12 0,-11 C-3,-12 -3,-14 0,-16Z") \
            + eyes(view, -13.5, "lid")
    if kind == "ember":
        return body("M0,-13.5 C2.6,-11.6 2.6,-9.6 0,-9 C-2.6,-9.6 -2.6,-11.6 0,-13.5Z", None, EMBER) \
            + eyes(view, -11, "lid")
    if kind == "hurt":
        return body("M-3,-22 C5,-17 4,-11 0,-9 C-5,-11 -7,-17 -3,-22Z", None, "#ff8a3d") + eyes(view, -15.5, "x")
    if kind == "kindle":
        return body("M0,-18 C3.5,-15 3.5,-11 0,-9 C-3.5,-11 -3.5,-15 0,-18Z", "M0,-15 C1.8,-13 1.8,-11.5 0,-11 C-1.8,-11.5 -1.8,-13 0,-15Z") \
            + eyes(view, -13.5, "wide")
    if kind == "bored":
        return body("M2,-22 C6,-17 5,-11 0,-9 C-5,-11 -4,-17 2,-22Z", "M1.5,-18 C3,-15 2.5,-12 0,-11 C-2.5,-12 -1.5,-15 1.5,-18Z") \
            + eyes(view, -15, "up")
    raise ValueError(kind)


def poly(points, colour=BRASS, w=2.4):
    pts = " ".join(f"{x},{y}" for x, y in points)
    return (f'<polyline points="{pts}" fill="none" stroke="{colour}" stroke-width="{w}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def wick(x, y, s=1.0, pose="idle", view=None, facing=1, rot=0):
    legs, arms, fl, v = POSES[pose]
    view = view or v
    if view == "side":
        legs, arms = "side", "side"
    half_top, half_bot, cap = (6, 5, 7) if view == "side" else (8, 6.5, 9)
    limbs = "".join(poly(p) for p in LEGS[legs] + ARMS[arms])
    bars = ""
    if view in ("front", "back"):
        bars = "".join(f'<line x1="{bx}" y1="-24" x2="{bx * 0.82}" y2="-7" stroke="{BRASS}" stroke-width="0.7" opacity="0.55"/>'
                       for bx in (-3.4, 3.4))
    elif view == "three":  # bars slide toward the facing side with the eyes
        bars = "".join(f'<line x1="{bx}" y1="-24" x2="{bx * 0.82}" y2="-7" stroke="{BRASS}" stroke-width="0.7" opacity="0.55"/>'
                       for bx in (-2.2, 4.6))
    back = ""
    if view == "back":  # latch and hinge mark the back door
        back = (f'<rect x="-0.6" y="-23" width="1.2" height="15" fill="{BRASS}"/>'
                f'<rect x="-2" y="-17" width="4" height="2" fill="{BRASS}"/>')
    handle = (f'<path d="M-5,-27 Q0,-36 5,-27" stroke="{BRASS}" stroke-width="1.8" fill="none"/>'
              if view != "side" else
              f'<path d="M-1,-27 Q0,-36 1,-27" stroke="{BRASS}" stroke-width="1.8" fill="none"/>')
    fl_svg = flame(fl, view)
    body = (handle
            + f'<polygon points="{-half_top},-24 {half_top},-24 {half_bot},-7 {-half_bot},-7" fill="{GLASS}" '
              f'stroke="{BRASS}" stroke-width="1.6"/>'
            + fl_svg + bars + back
            + f'<rect x="{-cap}" y="-27" width="{2 * cap}" height="3.2" rx="1" fill="{BRASS}"/>'
            + f'<rect x="{-half_top}" y="-7.5" width="{2 * half_top}" height="2.6" rx="1" fill="{BRASS}"/>')
    if fl in ("big", "joy"):
        body += fl_svg  # the flame rises over the cap
    back_limbs = limbs if view != "side" else limbs
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s * facing},{s})">'
            f'{back_limbs}{body}</g>')


def svg(w, h, body, extra_defs="", bg="#191b24", crisp=False, scale=1):
    cr = ' shape-rendering="crispEdges"' if crisp else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w * scale}" height="{h * scale}" '
            f'viewBox="0 0 {w} {h}"{cr}><defs>{extra_defs}'
            '<filter id="sil"><feFlood flood-color="#000"/><feComposite in2="SourceAlpha" operator="in"/></filter>'
            f'</defs><rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>\n')


def text(x, y, s, size=12, fill="#f4f1e8", anchor="start"):
    return f'<text x="{x}" y="{y}" {FONT} font-size="{size}" fill="{fill}" text-anchor="{anchor}">{s}</text>'


# ---------------------------------------------------------------- sheets

def turnaround():
    S = 6
    views = [("front", "front"), ("three", "three-quarter (game view)"), ("side", "side"), ("back", "back")]
    body = ""
    ground = 300
    for name, y in [("handle top -32", -32), ("collider top -28 (cap top -27)", -28), ("eye line -15", -15),
                    ("base -7", -7), ("feet 0", 0)]:
        yy = ground + y * S
        body += (f'<line x1="70" y1="{yy}" x2="800" y2="{yy}" stroke="#4a5068" stroke-width="1" stroke-dasharray="4 4"/>'
                 + text(806, yy + 4, name, 11, "#9aa3bf"))
    # height bar, one tick per pixel, label every 4
    for px in range(0, 33):
        yy = ground - px * S
        w = 14 if px % 4 == 0 else 7
        body += f'<line x1="{52 - w}" y1="{yy}" x2="52" y2="{yy}" stroke="#f4f1e8" stroke-width="1"/>'
        if px % 4 == 0:
            body += text(30 - (6 if px >= 10 else 0), yy + 4, str(px), 10, "#f4f1e8", "end")
    body += f'<line x1="52" y1="{ground}" x2="52" y2="{ground - 32 * S}" stroke="#f4f1e8" stroke-width="1.5"/>'
    body += text(8, 96, "px", 11)
    for i, (v, label) in enumerate(views):
        cx = 150 + i * 175
        body += wick(cx, ground, S, "idle", view=v) + text(cx, ground + 34, label, 12, anchor="middle")
    body += text(70, 30, "Wick — neutral turnaround · 1 unit = 1 on-screen px · drawn at 6x", 14)
    return svg(1010, 360, body)


def ladder(cx, gy):
    rails = "".join(f'<rect x="{cx + dx}" y="{gy - 165}" width="6" height="165" fill="#3b2a1c" stroke="#5a412a"/>' for dx in (-46, 40))
    rungs = "".join(f'<rect x="{cx - 46}" y="{y}" width="92" height="5" fill="#3b2a1c" stroke="#5a412a"/>' for y in range(gy - 155, gy, 30))
    return rails + rungs


def poses():
    S = 4
    order = [("idle", "1 idle"), ("bored", "2 bored (idle > 4 s)"), ("walk", "3 walk"),
             ("jump", "4 jump (rising)"), ("fall", "5 fall"), ("land", "6 land"),
             ("pickup", "7 oil pickup"), ("ember", "8 ember (oil = 0)"), ("hurt", "9 hurt / fail"),
             ("respawn", "10 respawn"), ("celebrate", "11 celebrate (exit)"),
             ("climb", "12 climb (on ladder)")]
    body = text(20, 28, "Wick — poses (right-facing; left = runtime flip) · drawn at 4x, feet on the line", 14)
    for i, (p, label) in enumerate(order):
        col, row = i % 4, i // 4
        cx, gy = 110 + col * 200, 210 + row * 210
        body += f'<line x1="{cx - 80}" y1="{gy}" x2="{cx + 80}" y2="{gy}" stroke="#6a7190" stroke-width="2"/>'
        lift = -24 if p in ("jump", "fall") else (-28 if p == "climb" else 0)
        rot = -10 if p == "hurt" else 0
        if p == "climb":
            body += ladder(cx, gy)
        body += wick(cx, gy + lift, S, p, rot=rot)
        if p == "respawn":
            body += f'<circle cx="{cx}" cy="{gy - 60}" r="70" fill="none" stroke="#ffe08a" stroke-width="2" stroke-dasharray="3 9"/>'
        body += text(cx, gy + 26, label, 12, anchor="middle")
    body += text(20, 704, "13 turnaround → turnaround.png · climb is the back view, seen while on a ladder", 12, "#9aa3bf")
    return svg(820, 720, body)


def collision():
    S = 4
    order = ["idle", "bored", "walk", "jump", "fall", "land", "pickup", "ember", "hurt", "respawn", "celebrate", "climb"]
    x0, y0, w, h = COLLIDER
    body = text(20, 28, "Collision overlay · RectangleShape2D 18 x 28 px, bottom-centre on the feet · 4x", 14)
    for i, p in enumerate(order):
        col, row = i % 4, i // 4
        cx, gy = 110 + col * 200, 210 + row * 210
        lift = -24 if p in ("jump", "fall") else (-28 if p == "climb" else 0)
        rot = -10 if p == "hurt" else 0
        if p == "climb":
            body += ladder(cx, gy)
        body += wick(cx, gy + lift, S, p, rot=rot)
        body += (f'<rect x="{cx + x0 * S}" y="{gy + lift + y0 * S}" width="{w * S}" height="{h * S}" '
                 f'fill="#ff3b3b" fill-opacity="0.18" stroke="#ff3b3b" stroke-width="2" stroke-dasharray="6 4"/>')
        body += text(cx, gy + 26, p, 12, anchor="middle")
    body += text(20, 704, "red = collider · outside it: handle, arms, tall flame", 12, "#ff8a8a")
    return svg(820, 720, body)


def silhouette_1x():
    """Black silhouettes at true on-screen size inside a 640x360 viewport."""
    order = ["idle", "walk", "jump", "fall", "hurt", "ember", "celebrate"]
    body = '<rect y="300" width="640" height="60" fill="#c9c4b8"/>'
    for i, p in enumerate(order):
        x = 60 + i * 80
        lift = -24 if p in ("jump", "fall") else 0
        body += f'<g filter="url(#sil)">{wick(x, 300 + lift, 1, p)}</g>'
    body += text(10, 20, "silhouette test · 1x · 640x360 viewport", 11, "#333")
    return svg(640, 360, body, bg="#f4f1e8")


def palette():
    def lum(hexc):
        r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5))
        f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

    def ratio(a, b):
        la, lb = sorted((lum(a), lum(b)), reverse=True)
        return (la + 0.05) / (lb + 0.05)

    body = text(20, 28, "Palette · character (top) checked against environment (columns)", 14)
    for i, (n, c) in enumerate(CHARACTER):
        y = 60 + i * 44
        body += f'<rect x="20" y="{y}" width="36" height="36" fill="{c}" stroke="#666"/>'
        body += text(64, y + 16, n, 12) + text(64, y + 31, c, 11, "#9aa3bf")
    for j, (n, c) in enumerate(ENVIRONMENT):
        x = 180 + j * 100
        body += f'<rect x="{x}" y="44" width="92" height="12" fill="{c}" stroke="#666"/>'
        body += text(x + 46, 40, n, 10, "#9aa3bf", "middle")
        for i, (_, cc) in enumerate(CHARACTER):
            y = 60 + i * 44
            r = ratio(cc, c)
            col = "#7ee08a" if r >= 3 else ("#ffd27a" if r >= 1.8 else "#ff8a8a")
            body += f'<rect x="{x}" y="{y}" width="92" height="36" fill="{c}"/>'
            body += f'<rect x="{x + 6}" y="{y + 8}" width="20" height="20" fill="{cc}"/>'
            body += text(x + 86, y + 23, f"{r:.1f}:1", 11, col, "end")
    # Wick at 1x and 3x on each environment colour
    for j, (n, c) in enumerate(ENVIRONMENT):
        x = 180 + j * 100
        body += f'<rect x="{x}" y="330" width="92" height="120" fill="{c}"/>'
        body += wick(x + 20, 440, 1, "idle") + wick(x + 60, 440, 3, "idle")
    body += text(20, 350, "Wick at 1x and 3x", 12) + text(20, 368, "on each colour", 12)
    body += text(20, 476, "green >= 3:1 · amber >= 1.8:1 · red below — the brass frame must be green or amber on every cave colour", 11, "#9aa3bf")
    return svg(800, 490, body), {(cn, en): ratio(cc, ec) for cn, cc in CHARACTER for en, ec in ENVIRONMENT}


if __name__ == "__main__":
    files = {"turnaround": turnaround(), "poses": poses(), "collision": collision(),
             "silhouette-1x": silhouette_1x()}
    pal, ratios = palette()
    files["palette"] = pal
    for name, content in files.items():
        (OUT / f"{name}.svg").write_text(content, encoding="utf-8")
        print("wrote", name)
    for (cn, en), r in ratios.items():
        if cn == "brass":
            print(f"contrast brass vs {en}: {r:.2f}")
