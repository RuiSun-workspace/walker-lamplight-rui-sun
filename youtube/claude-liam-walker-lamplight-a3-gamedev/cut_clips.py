"""Cut the two moving-picture beats, burn their labels, and set every beat's duration (Claude, 2026-10-15).

Timing contract (godot-waikthrough capture reference, as in A2): each capture beat is ONE contiguous interval of
a take at normal speed, never retimed or spliced; its length is the narration plus a 0.4 s tail, rounded up to
whole frames.
- B02: A2's scripted-input take run-01 (same 2D game build: only Godot .uid metadata changed since a70758d).
  Window chosen to contain the oil pickup in the bottom tunnel and the walk past the middle-tunnel lamp post.
  Game audio at -14 dB under the narration, as in A2.
- B11: this film's room-orbit take. Window chosen to contain the view from behind (9 s) and from below (13 s).
  The room has no sound, so the audio is the narration alone.
Graphic beats get props.durationSeconds = narration length; their highlight cues are spread over 8-88 %.

    F:/7270/film-env/Scripts/python.exe cut_clips.py
"""
import hashlib
import json
import math
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parent
A2 = Path("F:/7270/reels/claude-liam-walker-lamplight-gamedev")
FF = "F:/7270/tools/ffmpeg-9.0.1-essentials_build/bin/"
FPS, TAIL, GAME_UNDER_DB = 30, 0.4, -14.0
LABELS = {
    "B02": ("A2 slice footage, reused · same game build", "scripted-input capture run-01 (A2 reel) · native 4K · game audio under narration"),
    "B11": ("Godot 4.7.2 · asset room · scripted camera orbit", f"Claude's capture · native 3840×2160 Movie Maker · source {(REEL / 'capture/source-commit.txt').read_text()[:7]}"),
}


def sh(*args):
    subprocess.run([str(a) for a in args], check=True)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def frames_for(seconds):
    return math.ceil((seconds + TAIL) * FPS - 1e-9)


def label_png(bid):
    main, sub = LABELS[bid]
    font = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 64)
    small = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 46)
    img = Image.new("RGBA", (3840, 2160), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    w = max(d.textlength(main, font=font), d.textlength(sub, font=small))
    x0, y0, bw, bh = 120, 2160 - 120 - 196, int(w) + 96, 196
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=24, fill=(12, 12, 18, 215), outline=(154, 163, 191, 255), width=4)
    d.text((x0 + 48, y0 + 22), main, font=font, fill=(244, 241, 232, 255))
    d.text((x0 + 48, y0 + 112), sub, font=small, fill=(200, 205, 220, 255))
    p = REEL / "assets" / f"label-{bid}.png"
    img.save(p)
    return p


def cut(bid, frames_dir, start, n, narration, game_wav=None):
    total = len(list(frames_dir.glob("f*.png")))
    assert 0 <= start and start + n <= total, (bid, start, n, total)
    media = REEL / "media" / f"{bid}.mp4"
    media.parent.mkdir(exist_ok=True)
    sh(FF + "ffmpeg.exe", "-y", "-v", "error", "-framerate", FPS, "-start_number", start, "-i", frames_dir / "f%08d.png",
       "-i", label_png(bid), "-filter_complex", "[0:v][1:v]overlay=0:0", "-frames:v", n,
       "-c:v", "libx264", "-preset", "slow", "-crf", 15, "-pix_fmt", "yuv420p", "-an", media)
    dur, t0 = n / FPS, start / FPS
    (REEL / "mix").mkdir(exist_ok=True)
    audio = REEL / "mix" / f"{bid}.wav"
    if game_wav:
        game = REEL / "mix" / f"{bid}-game.wav"
        sh(FF + "ffmpeg.exe", "-y", "-v", "error", "-ss", f"{t0:.6f}", "-t", f"{dur:.6f}", "-i", game_wav,
           "-af", "apad", "-t", f"{dur:.6f}", "-ar", 48000, "-ac", 2, "-c:a", "pcm_s16le", game)
        sh(FF + "ffmpeg.exe", "-y", "-v", "error", "-i", REEL / narration, "-i", game, "-filter_complex",
           f"[0:a]aresample=48000,aformat=channel_layouts=stereo,apad[n];[1:a]volume={GAME_UNDER_DB}dB[g];"
           f"[n][g]amix=inputs=2:duration=longest:normalize=0[m]", "-map", "[m]", "-t", f"{dur:.6f}",
           "-ar", 48000, "-ac", 2, "-c:a", "pcm_s16le", audio)
    else:
        sh(FF + "ffmpeg.exe", "-y", "-v", "error", "-i", REEL / narration, "-af", "aresample=48000,aformat=channel_layouts=stereo,apad",
           "-t", f"{dur:.6f}", "-ar", 48000, "-ac", 2, "-c:a", "pcm_s16le", audio)
    return {"media": f"media/{bid}.mp4", "audio_file": audio.relative_to(REEL).as_posix(), "duration": dur,
            "start_s": round(t0, 4), "end_s": round(t0 + dur, 4), "frames": [start, start + n]}


def main():
    sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
    beats = {b["beat_id"]: b for b in sheet["beats"]}
    timings = json.loads((REEL / "mp3" / "timings.json").read_text())
    windows = {}
    # B02: ends just after Wick walks left past lamp post 2 (move_left at tick 705 -> frame ~352; post at x 2700)
    n = frames_for(float(timings["B02"]))
    end = 420
    windows["B02"] = cut("B02", A2 / "_frames/run-01", max(0, end - n), n, "mp3/beat-B02.mp3", A2 / "capture/run-01.wav")
    windows["B02"]["take"] = "A2 run-01"
    assert windows["B02"]["frames"][0] <= 263 and windows["B02"]["frames"][1] >= 400, "B02 must contain the pickup and the post"
    # B11: contains behind (frame 270) and below (frame 390)
    n = frames_for(float(timings["B11"]))
    windows["B11"] = cut("B11", REEL / "_frames/room-orbit", 150, n, "mp3/beat-B11.mp3")
    windows["B11"]["take"] = "room-orbit"
    assert windows["B11"]["frames"][0] <= 270 and windows["B11"]["frames"][1] >= 400, "B11 must contain behind and below"
    for bid, w in windows.items():
        b = beats[bid]
        b["audio_file"] = w["audio_file"]
        b["actual_duration_s"] = round(w["duration"], 4)
        b["render_duration_s"] = w["duration"]
        b["shot"]["clip_file"] = w["media"]
        b["shot"]["capture_window"] = {k: w[k] for k in ("take", "start_s", "end_s", "frames")}
        b["shot"]["capture_window"]["media_sha256"] = sha(REEL / w["media"])
        b.setdefault("qc", {})["full_bleed"] = True
        b["qc"]["full_bleed_reason"] = "Native 3840x2160 engine capture fills the frame by design."
        b["qc"]["contrast_regions"] = [{"label": "burned-in shot label", "box": [0.028, 0.85, 0.66, 0.945]}]
        b["qc"]["contrast_reason"] = ("Dark engine footage by design (the mine, and the asset room's near-black background); "
                                      "the text a viewer must read is the burned-in label, so contrast is measured there.")
    for b in sheet["beats"]:
        rem = b.get("shot", {}).get("remotion")
        if rem and b.get("actual_duration_s"):
            dur = float(b["actual_duration_s"])
            rem["props"]["durationSeconds"] = dur
            cues = rem["props"].get("cues") or []
            for i, c in enumerate(cues):
                c["at"] = round(dur * (0.08 + 0.8 * i / max(1, len(cues) - 1)), 2)
    shutil.copy(REEL / "assets" / "b13.png", REEL / "media" / "B13.png")
    (REEL / "beat_sheet.json").write_text(json.dumps(sheet, indent=1, ensure_ascii=False), encoding="utf-8")
    (REEL / "capture" / "windows.json").write_text(json.dumps(windows, indent=1), encoding="utf-8")
    for bid, w in windows.items():
        print(bid, w["take"], f"{w['start_s']:.2f}-{w['end_s']:.2f}s", f"{w['duration']:.2f}s", w["audio_file"])


if __name__ == "__main__":
    main()
