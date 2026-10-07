"""Measure and edit generated audio (written by Claude, 2026-10-07). Claude cannot listen; these numbers
and pictures support Rui's listening, they do not replace it. Every edit is logged in edit-log.jsonl.

    python tools/gen/audio_tools.py report F:/7270/a2-gen/gen-raw/SFX-JUMP/*.wav --png out.png
    python tools/gen/audio_tools.py sfx  in.wav --max-ms 400 --out godot/assets/audio/sfx_jump.ogg
    python tools/gen/audio_tools.py loop in.wav --bars 8 --out godot/assets/audio/mus_loop.ogg

Run with the a2-gen venv (soundfile). OGG is written by ffmpeg (libvorbis).
"""
import argparse
import datetime as dt
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[2]
LOG = REPO / "design" / "generation" / "edit-log.jsonl"
FFMPEG = "F:/7270/tools/ffmpeg-9.0.1-essentials_build/bin/ffmpeg.exe"


def load(path):
    x, sr = sf.read(path, always_2d=True)
    return x.mean(axis=1), sr


def db(v):
    return 20 * np.log10(max(v, 1e-9))


def lead_silence(x, sr, rel_db=-40):
    thr = np.abs(x).max() * 10 ** (rel_db / 20)
    idx = np.nonzero(np.abs(x) > thr)[0]
    return (idx[0] if len(idx) else 0), thr


def stats(path):
    x, sr = load(path)
    lead, _ = lead_silence(x, sr)
    return {"file": Path(path).name, "seconds": round(len(x) / sr, 3), "lead_silence_ms": round(lead / sr * 1000, 1),
            "peak_dbfs": round(db(np.abs(x).max()), 1), "rms_dbfs": round(db(np.sqrt((x ** 2).mean())), 1)}


def waveform(x, w=600, h=70, colour=(60, 90, 160)):
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    n = len(x)
    for i in range(w):
        seg = x[i * n // w:(i + 1) * n // w]
        if len(seg):
            lo, hi = seg.min(), seg.max()
            d.line([(i, h / 2 - hi * h / 2), (i, h / 2 - lo * h / 2)], fill=colour)
    return img


def log(rec):
    rec = {"time": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "tool": "tools/gen/audio_tools.py", **rec}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")


def write_ogg(x, sr, out):
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    wav = out.with_suffix(".edit.wav")
    sf.write(wav, x, sr, subtype="PCM_16")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", str(wav), "-c:a", "libvorbis", "-q:a", "6", str(out)], check=True)
    wav.unlink()


def cmd_report(a):
    rows = [stats(p) for p in a.files]
    for r in rows:
        print(json.dumps(r))
    if a.png:
        img = Image.new("RGB", (760, 80 * len(a.files)), "white")
        d = ImageDraw.Draw(img)
        for k, p in enumerate(a.files):
            x, sr = load(p)
            img.paste(waveform(x / max(1e-9, np.abs(x).max())), (150, k * 80 + 5))
            d.text((4, k * 80 + 30), Path(p).stem[-14:], fill="black")
            d.text((4, k * 80 + 45), f"{len(x) / sr:.2f}s", fill="black")
        img.save(a.png)


def cmd_sfx(a):
    x, sr = load(a.src)
    # onset at -25 dB below peak: at -40 dB the noise floor before JUMP-b3's hit counted as sound and the
    # first cut was 350 ms of silence (2026-10-07)
    lead, thr = lead_silence(x, sr, a.onset_db)
    start = max(0, lead - int(0.002 * sr))                     # keep 2 ms before the onset
    y = x[start:start + int(a.max_ms / 1000 * sr)].copy()
    fade = min(len(y), int(a.fade_ms / 1000 * sr))
    y[-fade:] *= np.linspace(1, 0, fade)                        # fade out so the cut never clicks
    y *= 10 ** (a.peak_db / 20) / max(1e-9, np.abs(y).max())
    write_ogg(y, sr, a.out)
    log({"op": "sfx", "src": Path(a.src).as_posix(), "src_sha256": hashlib.sha256(Path(a.src).read_bytes()).hexdigest(),
         "out": Path(a.out).as_posix(), "trim_start_ms": round(start / sr * 1000, 1), "length_ms": round(len(y) / sr * 1000, 1),
         "fade_out_ms": a.fade_ms, "peak_dbfs": a.peak_db, "onset_db": a.onset_db})
    print(json.dumps({"out": a.out, "trim_start_ms": round(start / sr * 1000, 1), "length_ms": round(len(y) / sr * 1000, 1)}))


def onset_env(x, sr, hop=512):
    frames = len(x) // hop
    e = np.array([np.sqrt((x[i * hop:(i + 1) * hop] ** 2).mean()) for i in range(frames)])
    return np.maximum(0, np.diff(e, prepend=e[0])), hop


def tempo(x, sr, lo=60, hi=160, hop=64):
    """Autocorrelation of the onset envelope. hop 64 (2 ms at 32 kHz) so an 8-bar loop is accurate to a
    few ms; the first version used hop 512, too coarse (89.3 vs ~90 bpm = 0.2 s drift over 8 bars)."""
    env, hop = onset_env(x, sr, hop)
    env = env - env.mean()
    ac = np.correlate(env, env, "full")[len(env) - 1:]
    fps = sr / hop
    lags = np.arange(int(fps * 60 / hi), int(fps * 60 / lo))
    best = lags[np.argmax(ac[lags])]
    return 60 * fps / best


def cmd_loop(a):
    x, sr = load(a.src)
    bpm = a.bpm or tempo(x, sr)
    bar = 4 * 60 / bpm
    length = int(round(a.bars * bar * sr))
    env, hop = onset_env(x, sr)
    # start on the strongest onset after the first second (generated intros are often unsettled)
    first = int(sr / hop)
    beat = int(60 / bpm * sr / hop)
    start_f = first + int(np.argmax(env[first:first + 4 * beat]))
    start = start_f * hop
    if start + length > len(x):
        raise SystemExit(f"clip too short for {a.bars} bars at {bpm:.1f} bpm")
    # move both ends to nearby rising zero crossings so the seam joins cleanly
    def zc(i):
        w = x[i - 200:i + 200]
        z = np.nonzero((w[:-1] <= 0) & (w[1:] > 0))[0]
        return i - 200 + z[np.argmin(np.abs(z - 200))] + 1 if len(z) else i
    s, e = zc(start), zc(start + length)
    y = x[s:e].copy()
    seam = abs(y[-1] - y[0])
    neighbour = np.median(np.abs(np.diff(y)))
    y *= 10 ** (a.peak_db / 20) / max(1e-9, np.abs(y).max())
    write_ogg(y, sr, a.out)
    preview = Path(a.out).with_name(Path(a.out).stem + "-x3-preview.wav")
    sf.write(preview, np.tile(y, 3), sr, subtype="PCM_16")
    rec = {"op": "loop", "src": Path(a.src).as_posix(), "src_sha256": hashlib.sha256(Path(a.src).read_bytes()).hexdigest(),
           "out": Path(a.out).as_posix(), "bpm": round(bpm, 2), "bars": a.bars, "start_s": round(s / sr, 4),
           "end_s": round(e / sr, 4), "length_s": round(len(y) / sr, 4),
           "seam_jump": float(round(seam, 5)), "median_step": float(round(neighbour, 5)), "preview_x3": preview.as_posix()}
    log(rec)
    print(json.dumps(rec))


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("report"); r.add_argument("files", nargs="+"); r.add_argument("--png")
    s = sub.add_parser("sfx"); s.add_argument("src"); s.add_argument("--out", required=True)
    s.add_argument("--max-ms", type=float, default=500); s.add_argument("--fade-ms", type=float, default=30)
    s.add_argument("--peak-db", type=float, default=-1.0)
    s.add_argument("--onset-db", type=float, default=-25.0)
    l = sub.add_parser("loop"); l.add_argument("src"); l.add_argument("--out", required=True)
    l.add_argument("--bars", type=int, default=8); l.add_argument("--bpm", type=float)
    l.add_argument("--peak-db", type=float, default=-3.0)
    a = p.parse_args()
    {"report": cmd_report, "sfx": cmd_sfx, "loop": cmd_loop}[a.cmd](a)


if __name__ == "__main__":
    main()
