"""Cut the gameplay beats from the Movie Maker takes and set every beat's duration (Claude, 2026-10-07).

Timing contract (godot-waikthrough capture reference): each gameplay beat is ONE contiguous interval of a
take at normal speed, never retimed or spliced. Its length is the narration plus a 0.4 s tail, rounded
up to whole frames, and the video and audio are cut to exactly that length. Windows are anchored on
events in the take's input log (physics ticks at 60/s; Movie Maker frames at 30/s, so frame = tick / 2).

Audio: narrated gameplay beats get narration at 0 dB over the take's own game audio at -14 dB (a logged
mix, written to mix/Bxx.wav). B13 gets the take's game audio alone, unprocessed (no narration).
Graphic beats get props.durationSeconds = narration length so Remotion never freezes early.

    python youtube/claude-liam-walker-lamplight-gamedev/cut_clips.py
"""
import hashlib
import json
import math
import shutil
import subprocess
from pathlib import Path

REEL = Path("F:/7270/reels/claude-liam-walker-lamplight-gamedev")
LOGS = Path("F:/7270/capture-build-a2/capture-logs")
FF = "F:/7270/tools/ffmpeg-9.0.1-essentials_build/bin/"
FPS = 30
TAIL = 0.4
GAME_UNDER_DB = -14.0
_HUD = [{"label": "HUD retries and timer", "box": [0.79, 0.025, 0.965, 0.075]},
        {"label": "HUD controls line", "box": [0.012, 0.075, 0.5, 0.115]}]
_LABEL = {"label": "burned-in shot label", "box": [0.028, 0.885, 0.63, 0.945]}
CONTRAST_REGIONS = {"B02": _HUD + [_LABEL], "B08": _HUD + [_LABEL], "B10": _HUD + [_LABEL], "B12": _HUD + [_LABEL],
                    "B15": _HUD + [_LABEL],
                    # B13 ends on the end card: the game dims its HUD under the card's scrim, so only the label is
                    # measured there; the card itself is read by eye in _qc/contact_sheet.png.
                    "B13": [{"label": "burned-in shot label", "box": [0.028, 0.85, 0.49, 0.945]}]}
CONTRAST_REASON = ("The mine is dark by design: lighting.gd darkens the scene with CanvasModulate (0.16, 0.16, 0.22) and "
                   "only Wick's light and the unshaded overlay are bright, so the frame-wide ink/background separation "
                   "reads 0.23-0.29. The text a viewer must read is the HUD (light on dark) and the burned-in shot label, "
                   "so contrast is measured in those regions. On B13 the end card's scrim dims the HUD, so only the label "
                   "is measured; 'YOU ESCAPED' and the card text were checked by eye in _qc/contact_sheet.png.")


def sh(*args):
    subprocess.run([str(a) for a in args], check=True)


def probe(path):
    out = subprocess.run([FF + "ffprobe.exe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def events(take):
    return [json.loads(l) for l in (LOGS / f"{take}-inputs.jsonl").read_text().splitlines() if l.strip()]


def frames(take):
    return len(list((REEL / "_frames" / take).glob("f*.png")))


def encode_take(take):
    """Full take as evidence: capture/<take>.mp4 + .wav + the input log."""
    src = REEL / "_frames" / take
    out = REEL / "capture" / f"{take}.mp4"
    if not out.exists():
        sh(FF + "ffmpeg.exe", "-y", "-v", "error", "-framerate", FPS, "-start_number", 0, "-i", src / "f%08d.png",
           "-c:v", "libx264", "-preset", "slow", "-crf", 15, "-pix_fmt", "yuv420p", out)
    shutil.copy(src / "f.wav", REEL / "capture" / f"{take}.wav")
    shutil.copy(LOGS / f"{take}-inputs.jsonl", REEL / "capture" / f"{take}-inputs.jsonl")
    return out


def cut(bid, take, start_frame, n_frames, narration, game_only=False):
    src = REEL / "_frames" / take
    total = frames(take)
    assert 0 <= start_frame and start_frame + n_frames <= total, (bid, start_frame, n_frames, total)
    media = REEL / "media" / f"{bid}.mp4"
    media.parent.mkdir(exist_ok=True)
    sh(FF + "ffmpeg.exe", "-y", "-v", "error", "-framerate", FPS, "-start_number", start_frame, "-i", src / "f%08d.png",
       "-frames:v", n_frames, "-c:v", "libx264", "-preset", "slow", "-crf", 15, "-pix_fmt", "yuv420p", media)
    dur = n_frames / FPS
    t0 = start_frame / FPS
    (REEL / "mix").mkdir(exist_ok=True)
    game = REEL / "mix" / f"{bid}-game.wav"
    sh(FF + "ffmpeg.exe", "-y", "-v", "error", "-ss", f"{t0:.6f}", "-t", f"{dur:.6f}", "-i", src / "f.wav",
       "-af", "apad", "-t", f"{dur:.6f}", "-ar", 48000, "-ac", 2, "-c:a", "pcm_s16le", game)
    if game_only:
        audio = game
    else:
        audio = REEL / "mix" / f"{bid}.wav"
        sh(FF + "ffmpeg.exe", "-y", "-v", "error", "-i", REEL / narration, "-i", game, "-filter_complex",
           f"[0:a]aresample=48000,aformat=channel_layouts=stereo,apad[n];[1:a]volume={GAME_UNDER_DB}dB[g];"
           f"[n][g]amix=inputs=2:duration=longest:normalize=0[m]", "-map", "[m]", "-t", f"{dur:.6f}",
           "-ar", 48000, "-ac", 2, "-c:a", "pcm_s16le", audio)
    return {"media": f"media/{bid}.mp4", "audio_file": audio.relative_to(REEL).as_posix(), "duration": dur,
            "take": take, "start_s": round(t0, 4), "end_s": round(t0 + dur, 4), "frames": [start_frame, start_frame + n_frames]}


def frames_for(seconds):
    return math.ceil((seconds + TAIL) * FPS - 1e-9)


def main():
    sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
    beats = {b["beat_id"]: b for b in sheet["beats"]}
    for take in ("run-01", "run-02", "run-03"):
        encode_take(take)
    e1, e2, e3 = events("run-01"), events("run-02"), events("run-03")
    jumps1 = [e for e in e1 if e.get("press") == "jump"]

    def first_jump(xlo, xhi, ylo, yhi):
        return next(e for e in jumps1 if xlo <= e["x"] <= xhi and ylo <= e["y"] <= yhi)

    # always from the Kokoro outputs, never from fields this script rewrites (so a re-run is idempotent)
    timings = json.loads((REEL / "mp3" / "timings.json").read_text())

    def nar(bid):
        return float(timings[bid])

    windows = {}
    T = lambda e: e["tick"] / 60.0                     # seconds into the take
    F = lambda sec: int(round(sec * FPS))
    climb2 = next(e for e in e1 if e.get("press") == "climb_up" and e["y"] < 1000)
    plat = first_jump(1580, 1680, 900, 1000)
    # run-01 windows do NOT overlap, so no footage is shown twice:
    #   B02 0 .. title + bottom tunnel | B10 middle-platform pickup | B08 walk left, ladder 2, top jump | B13 top tunnel to end card
    windows["B02"] = cut("B02", "run-01", 0, frames_for(nar("B02")), "mp3/beat-B02.mp3")
    b10_start = F(T(plat) - 2.95)
    assert b10_start >= windows["B02"]["frames"][1], "B10 overlaps B02"
    windows["B10"] = cut("B10", "run-01", b10_start, frames_for(nar("B10")), "mp3/beat-B10.mp3")
    b08_start = F(T(climb2) - 2.07)
    assert b08_start >= windows["B10"]["frames"][1], "B08 overlaps B10"
    windows["B08"] = cut("B08", "run-01", b08_start, frames_for(nar("B08")), "mp3/beat-B08.mp3")
    b13_start = windows["B08"]["frames"][1] + 2
    windows["B13"] = cut("B13", "run-01", b13_start, frames("run-01") - b13_start, None, game_only=True)
    # B12: run-02 ending on the respawn, long enough for the narration (the whole take is 5.8 s)
    n = frames_for(nar("B12"))
    windows["B12"] = cut("B12", "run-02", frames("run-02") - n, n, "mp3/beat-B12.mp3")
    # B15: run-03, the last seconds of the ember to the burn-out and the start of the respawn
    n = frames_for(nar("B15"))
    windows["B15"] = cut("B15", "run-03", frames("run-03") - n - 5, n, "mp3/beat-B15.mp3")

    for bid, w in windows.items():
        b = beats[bid]
        b["audio_file"] = w["audio_file"]
        b["actual_duration_s"] = round(w["duration"], 4)
        b["render_duration_s"] = w["duration"]
        b["shot"]["capture_window"] = {k: w[k] for k in ("take", "start_s", "end_s", "frames")}
        b["shot"]["capture_window"]["media_sha256"] = sha(REEL / w["media"])
        b.setdefault("qc", {})["full_bleed"] = True
        b["qc"]["full_bleed_reason"] = ("Gameplay capture: the 1280x720 viewport (x3, native 3840x2160) fills the frame; "
                                        "the HUD sits at the top edge by design.")
        # Gate V (2026-10-07): the mine is dark by design (CanvasModulate 0.16), so whole-frame ink/background
        # separation reads 0.23-0.29. Measure contrast where the text is instead.
        b["qc"]["contrast_regions"] = CONTRAST_REGIONS[bid]
        b["qc"]["contrast_reason"] = CONTRAST_REASON
    # graphic beats: Remotion duration = narration; highlight cues spread over 8-88 % of the real length
    for b in sheet["beats"]:
        rem = b.get("shot", {}).get("remotion")
        if rem and b.get("actual_duration_s"):
            dur = float(b["actual_duration_s"])
            rem["props"]["durationSeconds"] = dur
            cues = rem["props"].get("cues") or []
            for i, c in enumerate(cues):
                c["at"] = round(dur * (0.08 + 0.8 * i / max(1, len(cues) - 1)), 2)
    # B18 still: the recorded output image
    shutil.copy(REEL / "assets" / "b18-test-output.png", REEL / "media" / "B18.png")
    (REEL / "beat_sheet.json").write_text(json.dumps(sheet, indent=1, ensure_ascii=False), encoding="utf-8")
    (REEL / "capture" / "windows.json").write_text(json.dumps(windows, indent=1), encoding="utf-8")
    for bid, w in windows.items():
        print(bid, w["take"], f"{w['start_s']:.2f}-{w['end_s']:.2f}s", f"{w['duration']:.2f}s", w["audio_file"])


if __name__ == "__main__":
    main()
