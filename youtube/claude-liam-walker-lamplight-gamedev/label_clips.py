"""Burn the on-screen provenance label into each gameplay clip (Claude, 2026-10-07).

The toolkit's final compile does not draw shot labels (they appear only in --review cuts), but the brief
requires scripted-input captures and the no-narration audio segment to be labelled on screen. Each label is
a PNG overlay at the bottom-left; nothing else in the frame changes and the timing is untouched.
Run after cut_clips.py and before make_evidence.py (it changes the media hashes).
"""
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path("F:/7270/reels/claude-liam-walker-lamplight-gamedev")
FF = "F:/7270/tools/ffmpeg-9.0.1-essentials_build/bin/ffmpeg.exe"
LABELS = {
    "B02": ("Scripted-input capture · Godot Movie Maker · native 3840×2160 · run-01", None),
    "B08": ("Scripted-input capture · real Input actions · native 4K · run-01", None),
    "B10": ("Scripted-input capture · real Input actions · native 4K · run-01", None),
    "B12": ("Scripted-input capture · an early jump, a real death · run-02", None),
    "B13": ("SLICE AUDIO — the game's own sound, no narration", "Scripted-input capture · native 4K · run-01 · unprocessed game audio"),
    "B15": ("Scripted-input capture · no input pressed · run-03", None),
}
font = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 64)
small = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 46)
for bid, (main, sub) in LABELS.items():
    img = Image.new("RGBA", (3840, 2160), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    w = d.textlength(main, font=font)
    w2 = d.textlength(sub, font=small) if sub else 0
    box_w = int(max(w, w2)) + 96
    box_h = 120 if not sub else 196
    x0, y0 = 120, 2160 - 120 - box_h
    d.rounded_rectangle([x0, y0, x0 + box_w, y0 + box_h], radius=24, fill=(12, 12, 18, 215),
                        outline=(255, 207, 90, 255) if bid == "B13" else (154, 163, 191, 255), width=4)
    d.text((x0 + 48, y0 + 22), main, font=font, fill=(255, 207, 90, 255) if bid == "B13" else (244, 241, 232, 255))
    if sub:
        d.text((x0 + 48, y0 + 112), sub, font=small, fill=(200, 205, 220, 255))
    png = REEL / "assets" / f"label-{bid}.png"
    img.save(png)
    clip = REEL / "media" / f"{bid}.mp4"
    tmp = clip.with_name(f"{bid}.labelled.mp4")
    subprocess.run([FF, "-y", "-v", "error", "-i", str(clip), "-i", str(png), "-filter_complex", "[0:v][1:v]overlay=0:0",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-pix_fmt", "yuv420p", "-an", str(tmp)], check=True)
    tmp.replace(clip)
    print(bid, "labelled:", main)
