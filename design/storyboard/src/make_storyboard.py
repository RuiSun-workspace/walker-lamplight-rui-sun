"""Generate the Lamplight storyboard sketches as SVG (16:9, 640x360 viewBox).

Hand-written by Claude (no generative model). Wick is drawn by one function so the
character keeps the same construction in every panel. Run:

    python design/storyboard/src/make_storyboard.py

Writes design/storyboard/NN-name.svg. PNGs are rasterised from these with headless
Chrome (see STORYBOARD.md).
"""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]

DARK = "#0b0b10"
ROCK = "#2a2e3d"
ROCK_EDGE = "#4a5068"
BRASS = "#b8863b"
GLASS = "#241f2c"
FLAME = "#ffcf5a"
FLAME_IN = "#fff1b8"
EMBER = "#e2552f"
SPIKE = "#3a3f4e"
SPIKE_EDGE = "#8f96a8"
GLINT = "#e8f0ff"
DAY = "#dfeaf5"
RED = "#e0483e"
FONT = 'font-family="Consolas, Menlo, monospace"'

LEGS = {
    "idle": [(-4, -6, -5, 0), (4, -6, 5, 0)],
    "walk": [(-4, -6, -8, 0), (4, -6, 7, -1)],
    "jump": [(-4, -6, -7, -2), (4, -6, 2, -1)],
    "hurt": [(-4, -6, -9, -1), (4, -6, 9, -3)],
}
ARMS = {
    "idle": [(-8, -17, -12, -11), (8, -17, 12, -11)],
    "walk": [(-8, -17, -12, -20), (8, -17, 13, -13)],
    "up": [(-8, -18, -14, -25), (8, -18, 14, -25)],
    "hurt": [(-8, -17, -15, -14), (8, -17, 14, -23)],
    "reach": [(-8, -17, -12, -11), (8, -17, 15, -20)],
}
POSES = {  # pose -> (legs, arms)
    "idle": ("idle", "idle"),
    "walk": ("walk", "walk"),
    "jump": ("jump", "up"),
    "hurt": ("hurt", "hurt"),
    "celebrate": ("idle", "up"),
    "pickup": ("idle", "reach"),
    "respawn": ("idle", "idle"),
}


def flame_svg(kind):
    if kind == "big":
        return (f'<path d="M0,-31 C7,-21 6,-11 0,-9 C-6,-11 -7,-21 0,-31Z" fill="{FLAME}"/>'
                f'<path d="M0,-24 C3,-18 3,-12 0,-11 C-3,-12 -3,-18 0,-24Z" fill="{FLAME_IN}"/>'
                '<circle cx="0.3" cy="-16" r="1" fill="#2a1a10"/><circle cx="3" cy="-16" r="1" fill="#2a1a10"/>'
                '<path d="M0.3,-13.6 Q1.7,-12.2 3,-13.6" stroke="#2a1a10" stroke-width="0.7" fill="none"/>')
    if kind == "ember":
        return (f'<path d="M0,-13.5 C2.6,-11.6 2.6,-9.6 0,-9 C-2.6,-9.6 -2.6,-11.6 0,-13.5Z" fill="{EMBER}"/>'
                '<path d="M-0.6,-11 h1.3 M1.6,-11 h1.3" stroke="#2a1a10" stroke-width="0.6"/>')
    if kind == "hurt":
        return (f'<path d="M-3,-22 C5,-17 4,-11 0,-9 C-5,-11 -7,-17 -3,-22Z" fill="#ff8a3d"/>'
                '<path d="M-0.6,-16.4 l1.6,1.6 M1,-16.4 l-1.6,1.6 M2.2,-16.4 l1.6,1.6 M3.8,-16.4 l-1.6,1.6" '
                'stroke="#2a1a10" stroke-width="0.6"/>')
    return (f'<path d="M0,-23 C5,-18 5,-11 0,-9 C-5,-11 -5,-18 0,-23Z" fill="{FLAME}"/>'
            f'<path d="M0,-19 C2.5,-16 2.5,-12 0,-11 C-2.5,-12 -2.5,-16 0,-19Z" fill="{FLAME_IN}"/>'
            '<circle cx="0.3" cy="-15" r="0.95" fill="#2a1a10"/><circle cx="2.9" cy="-15" r="0.95" fill="#2a1a10"/>')


def wick(x, y, s=1.0, pose="idle", flame="full", facing=1, rot=0):
    """Wick, feet at (x, y). At s=1 he is ~36 px tall including the handle."""
    legs, arms = POSES[pose]
    limbs = "".join(
        f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="{BRASS}" stroke-width="2.4" stroke-linecap="round"/>'
        for a, b, c, d in LEGS[legs] + ARMS[arms])
    body = (
        f'<path d="M-5,-27 Q0,-36 5,-27" stroke="{BRASS}" stroke-width="1.8" fill="none"/>'
        f'<polygon points="-8,-24 8,-24 6.5,-7 -6.5,-7" fill="{GLASS}" stroke="{BRASS}" stroke-width="1.6"/>'
        + flame_svg(flame) +
        f'<line x1="-3.4" y1="-24" x2="-2.8" y2="-7" stroke="{BRASS}" stroke-width="0.7" opacity="0.55"/>'
        f'<line x1="3.4" y1="-24" x2="2.8" y2="-7" stroke="{BRASS}" stroke-width="0.7" opacity="0.55"/>'
        f'<rect x="-9.5" y="-27" width="19" height="3.2" rx="1" fill="{BRASS}"/>'
        f'<rect x="-8" y="-7.5" width="16" height="2.6" rx="1" fill="{BRASS}"/>'
    )
    if flame == "big":  # the flame overflows the cap
        body += flame_svg("big")
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s * facing},{s})">'
            f'{limbs}{body}</g>')


def glow(x, y, r, strength=1.0):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#lamp)" opacity="{strength}"/>'


def darkness(holes, opacity=0.9):
    """Black overlay with soft holes punched by light sources (x, y, r)."""
    cut = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#hole)"/>' for x, y, r in holes)
    return (f'<mask id="m"><rect width="640" height="360" fill="white"/>{cut}</mask>'
            f'<rect width="640" height="360" fill="{DARK}" opacity="{opacity}" mask="url(#m)"/>')


def ledge(x, y, w, h=400):
    bricks = "".join(
        f'<line x1="{x}" y1="{yy}" x2="{x + w}" y2="{yy}" stroke="{ROCK_EDGE}" stroke-width="0.6" opacity="0.6"/>'
        for yy in range(int(y) + 14, int(y) + h, 14))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{ROCK}" stroke="{ROCK_EDGE}" stroke-width="1.2"/>'
            f'{bricks}<line x1="{x}" y1="{y}" x2="{x + w}" y2="{y}" stroke="#6a7190" stroke-width="2"/>')


def spikes(x, y, n, w=10, h=12, flash=False):
    out = []
    for i in range(n):
        x0 = x + i * w
        stroke = RED if flash else SPIKE_EDGE
        out.append(f'<polygon points="{x0},{y} {x0 + w / 2},{y - h} {x0 + w},{y}" fill="{SPIKE}" '
                   f'stroke="{stroke}" stroke-width="{2.4 if flash else 1}"/>')
    return "".join(out)


def glints(x, y, n, w=10, h=12):
    return "".join(f'<path d="M{x + i * w + w / 2},{y - h} l-1.5,3 M{x + i * w + w / 2},{y - h} l1.5,3" '
                   f'stroke="{GLINT}" stroke-width="1" opacity="0.85"/>' for i in range(n))


def oil(x, y, s=1.0, halo=True):
    h = f'<circle cx="{x}" cy="{y}" r="{14 * s}" fill="url(#lamp)" opacity="0.55"/>' if halo else ""
    return (h + f'<path transform="translate({x},{y}) scale({s})" d="M0,-8 C5,-1 5,4 0,5 C-5,4 -5,-1 0,-8Z" '
            f'fill="#f2a93b" stroke="#ffe08a" stroke-width="0.8"/>')


def ceiling(points):
    pts = " ".join(f"{x},{y}" for x, y in points)
    return f'<polygon points="0,0 {pts} 640,0" fill="{ROCK}" stroke="{ROCK_EDGE}" stroke-width="1"/>'


def timber(x, ground, top):
    return (f'<rect x="{x}" y="{top}" width="6" height="{ground - top}" fill="#3b2a1c" stroke="#5a412a" stroke-width="1"/>'
            f'<rect x="{x - 14}" y="{top - 6}" width="34" height="7" fill="#3b2a1c" stroke="#5a412a" stroke-width="1"/>')


def exit_hint(x=618):
    return (f'<rect x="{x}" y="0" width="{640 - x}" height="360" fill="url(#dayside)"/>')


def gauge(level, warn=False):
    col = RED if warn else BRASS
    return (f'<g transform="translate(14,14)">'
            f'<path d="M6,0 C11,6 10,13 6,15 C2,13 1,6 6,0Z" fill="{FLAME if level > 0.15 else EMBER}"/>'
            f'<rect x="18" y="4" width="84" height="8" fill="none" stroke="{col}" stroke-width="1.4"/>'
            f'<rect x="20" y="6" width="{80 * level:.1f}" height="4" fill="{FLAME if level > 0.15 else EMBER}"/></g>')


def arrow_path(d, dashed=True):
    dash = 'stroke-dasharray="6 5"' if dashed else ""
    return (f'<path d="{d}" fill="none" stroke="#ffffff" stroke-width="1.6" {dash} opacity="0.8" '
            f'marker-end="url(#arr)"/>')


def label(text):
    return (f'<rect x="0" y="336" width="640" height="24" fill="#000" opacity="0.72"/>'
            f'<text x="10" y="352" {FONT} font-size="12" fill="#f4f1e8">{text}</text>')


def frame(body, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 640 360">
<title>{title}</title>
<defs>
<radialGradient id="lamp"><stop offset="0" stop-color="#ffc861" stop-opacity="0.55"/>
<stop offset="0.45" stop-color="#ffb347" stop-opacity="0.2"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>
<radialGradient id="hole"><stop offset="0" stop-color="#000"/><stop offset="0.55" stop-color="#000"/>
<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<linearGradient id="dayside" x1="0" x2="1"><stop offset="0" stop-color="{DAY}" stop-opacity="0"/>
<stop offset="1" stop-color="{DAY}" stop-opacity="0.45"/></linearGradient>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{DAY}" stop-opacity="0.85"/>
<stop offset="1" stop-color="{DAY}" stop-opacity="0.08"/></linearGradient>
<marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
<path d="M1,1 L9,5 L1,9" fill="none" stroke="#ffffff" stroke-width="1.6"/></marker>
</defs>
<rect width="640" height="360" fill="#191b24"/>
{body}
{label(title)}
</svg>
'''


# ---------------------------------------------------------------- panels

def p1():
    tunnel = "M50,318 H280 L320,250 H520 L556,184 H300 L268,122 H560 V60"
    body = (
        '<rect width="640" height="62" fill="#cfdbe8"/>'
        '<rect y="60" width="640" height="6" fill="#4f6b3c"/>'
        '<rect y="66" width="640" height="294" fill="#14151d"/>'
        f'<path d="{tunnel}" fill="none" stroke="#2c3042" stroke-width="28" stroke-linejoin="round" stroke-linecap="round"/>'
        + "".join(f'<line x1="{x}" y1="{y - 12}" x2="{x}" y2="{y + 12}" stroke="#5a412a" stroke-width="2"/>'
                  for x, y in [(140, 318), (230, 318), (400, 250), (470, 250), (380, 184), (440, 122)])
        + '<polygon points="548,60 572,60 590,140 530,140" fill="url(#beam)"/>'
        + glow(68, 312, 34) + wick(68, 326, 0.55, "idle")
        + arrow_path("M92,306 H272 L308,240 H508 L540,196 H312 L282,134 H540 L548,76")
        + f'<text x="24" y="40" {FONT} font-size="26" font-weight="700" fill="#14151d">LAMPLIGHT</text>'
        + f'<text x="26" y="54" {FONT} font-size="11" fill="#14151d">press Enter</text>'
        + f'<text x="584" y="52" {FONT} font-size="11" fill="#14151d">exit</text>'
    )
    return frame(body, "P1 · WIDE · HIGH ANGLE (cross-section) · DESIGN VIEW — title / establishing")


def p2():
    body = (
        ceiling([(0, 46), (60, 58), (130, 40), (210, 62), (300, 44), (380, 66), (470, 42), (560, 60), (640, 48)])
        + ledge(0, 290, 300) + ledge(380, 270, 260) + ledge(300, 324, 80)
        + spikes(302, 324, 7, 11, 13)
        + timber(196, 290, 92) + timber(520, 270, 92)
        + oil(470, 250)
        + exit_hint()
        + glow(100, 270, 130)
        + wick(100, 290, 1.0, "idle")
        + darkness([(100, 272, 150), (470, 250, 30)], 0.9)
        + glints(302, 324, 7, 11, 13) + oil(470, 250, halo=False) + exit_hint()
        + gauge(1.0)
    )
    return frame(body, "P2 · WIDE · EYE LEVEL · GAMEPLAY VIEW — first frame of play (true 640×360 scale)")


def p3():
    body = (
        ceiling([(0, 30), (120, 46), (260, 26), (420, 50), (560, 30), (640, 40)])
        + ledge(0, 260, 230) + ledge(410, 250, 230) + ledge(230, 340, 180)
        + spikes(232, 340, 16, 11, 14)
        + glow(320, 160, 220)
        + wick(320, 182, 2.3, "jump")
        + arrow_path("M206,250 Q320,70 432,238")
        + darkness([(320, 165, 250)], 0.88)
        + glints(232, 340, 16, 11, 14)
        + gauge(0.8)
    )
    return frame(body, "P3 · MEDIUM · EYE LEVEL · GAMEPLAY VIEW (2× crop of camera) — core action: jump")


def p4():
    rays = "".join(
        f'<line x1="{320 + 70 * c}" y1="{150 + 70 * s}" x2="{320 + 150 * c}" y2="{150 + 150 * s}" '
        f'stroke="#ffd27a" stroke-width="2" opacity="0.6"/>'
        for c, s in [(1, 0), (0.7, -0.7), (0, -1), (-0.7, -0.7), (-1, 0), (0.7, 0.7), (-0.7, 0.7)])
    body = (
        '<polygon points="20,360 92,360 250,0 228,0" fill="#3b2a1c" stroke="#5a412a"/>'
        '<polygon points="548,360 620,360 412,0 390,0" fill="#3b2a1c" stroke="#5a412a"/>'
        '<polygon points="160,40 480,40 470,58 170,58" fill="#3b2a1c" stroke="#5a412a"/>'
        f'<rect y="326" width="640" height="34" fill="{ROCK}" stroke="{ROCK_EDGE}"/>'
        + glow(320, 160, 330, 1.0) + rays
        + wick(320, 330, 8.4, "pickup", "big")
        + '<path d="M470,175 Q430,150 380,170" fill="none" stroke="#ffe08a" stroke-width="1.5" stroke-dasharray="3 4"/>'
        + oil(492, 186, 2.2)
        + "".join(f'<circle cx="{x}" cy="{y}" r="2" fill="#ffe08a"/>' for x, y in [(450, 160), (420, 152), (398, 160)])
        + darkness([(320, 170, 420)], 0.6)
    )
    return frame(body, "P4 · CLOSE-UP · LOW ANGLE · DESIGN VIEW — success: oil drop absorbed, flame flares")


def p5():
    body = (
        ceiling([(0, 40), (150, 56), (300, 38), (450, 60), (640, 44)])
        + ledge(0, 280, 400) + ledge(470, 280, 170) + ledge(400, 322, 70)
        + spikes(402, 322, 6, 11, 13)
        + timber(120, 280, 80)
        + glow(250, 262, 70)
        + wick(250, 280, 2.2, "walk", "ember")
        + darkness([(250, 262, 80)], 0.95)
        + glints(402, 322, 6, 11, 13) + exit_hint(600)
        + gauge(0.05, warn=True)
    )
    return frame(body, "P5 · MEDIUM · EYE LEVEL · GAMEPLAY VIEW (2× crop) — risk: oil empty, ember")


def p6():
    impact = "".join(
        f'<line x1="{330 + 30 * c}" y1="{250 + 30 * s}" x2="{330 + 52 * c}" y2="{250 + 52 * s}" '
        f'stroke="{RED}" stroke-width="2.4"/>'
        for c, s in [(1, 0), (0.7, -0.7), (0, -1), (-0.7, -0.7), (-1, 0)])
    scene = (
        ledge(-80, 230, 250) + ledge(480, 230, 260) + ledge(170, 300, 310)
        + spikes(172, 300, 28, 11, 14, flash=True)
        + glow(330, 250, 180)
        + wick(330, 300, 2.8, "hurt", "hurt", rot=-18)
        + impact
        + darkness([(330, 250, 200)], 0.85)
        + glints(172, 300, 28, 11, 14)
    )
    body = f'<g transform="rotate(-11 320 180) translate(-30 -20) scale(1.1)">{scene}</g>'
    return frame(body, "P6 · MEDIUM · DUTCH ANGLE · DESIGN VIEW — failure: spikes (in game: eye level + flash)")


def p7():
    body = (
        ceiling([(0, 46), (90, 60), (200, 40), (320, 64), (450, 44), (640, 56)])
        + ledge(0, 290, 330) + ledge(400, 280, 240) + ledge(330, 324, 70)
        + spikes(332, 324, 6, 11, 13, flash=True)
        + f'<rect x="118" y="200" width="5" height="90" fill="#3b2a1c" stroke="#5a412a"/>'
        + f'<rect x="110" y="190" width="21" height="14" fill="{GLASS}" stroke="{BRASS}" stroke-width="1.5"/>'
        + f'<path d="M120.5,192 C124,196 124,200 120.5,202 C117,200 117,196 120.5,192Z" fill="{FLAME}"/>'
        + glow(120, 197, 90)
        + glow(160, 272, 110)
        + '<circle cx="160" cy="272" r="26" fill="none" stroke="#ffe08a" stroke-width="1.4" stroke-dasharray="2 5"/>'
        + wick(160, 290, 1.25, "respawn")
        + arrow_path("M364,304 Q260,200 178,262")
        + darkness([(160, 272, 125), (120, 197, 70)], 0.9)
        + glints(332, 324, 6, 11, 13) + exit_hint()
        + gauge(0.6)
    )
    return frame(body, "P7 · WIDE · EYE LEVEL · GAMEPLAY VIEW — recovery: respawn at the lamp post")


def p8():
    body = (
        f'<rect width="640" height="360" fill="{DAY}"/>'
        f'<polygon points="0,360 214,360 270,0 0,0" fill="{ROCK}" stroke="{ROCK_EDGE}"/>'
        f'<polygon points="426,360 640,360 640,0 370,0" fill="{ROCK}" stroke="{ROCK_EDGE}"/>'
        + "".join(f'<line x1="{214 + (270 - 214) * t}" y1="{360 * (1 - t)}" x2="{426 - (426 - 370) * t}" '
                  f'y2="{360 * (1 - t)}" stroke="#5a412a" stroke-width="{3 - 2 * t:.1f}"/>'
                  for t in (0.25, 0.5, 0.7, 0.85))
        + '<polygon points="270,0 370,0 440,330 200,330" fill="url(#beam)"/>'
        + f'<rect y="326" width="640" height="34" fill="{ROCK}" stroke="{ROCK_EDGE}"/>'
        + glow(320, 300, 70)
        + wick(320, 330, 3.0, "celebrate", "big")
        + '<rect x="420" y="20" width="200" height="52" fill="#000" opacity="0.7"/>'
        + f'<text x="432" y="42" {FONT} font-size="14" fill="#f4f1e8">YOU ESCAPED · 1:42</text>'
        + f'<text x="432" y="60" {FONT} font-size="11" fill="#f4f1e8">Enter: play again</text>'
    )
    return frame(body, "P8 · WIDE · LOW ANGLE · DESIGN VIEW — end of session: daylight at the exit")


PANELS = {
    "01-title": p1, "02-first-frame": p2, "03-jump": p3, "04-oil-pickup": p4,
    "05-ember": p5, "06-failure": p6, "07-respawn": p7, "08-exit": p8,
}

if __name__ == "__main__":
    for name, fn in PANELS.items():
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
        print("wrote", name)
