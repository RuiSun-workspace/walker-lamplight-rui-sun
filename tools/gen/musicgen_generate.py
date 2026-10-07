"""Generate audio locally with MusicGen (facebook/musicgen-medium) and log it reproducibly.

Written by Claude. Used for both music and sound effects (Rui chose MusicGen only, 2026-10-06).

    python tools/gen/musicgen_generate.py --id MUS-LOOP --prompt "..." --seed 2001 --seconds 30 --batch 2

Raw WAVs (32 kHz mono) go to F:/7270/a2-gen/gen-raw/<ID>/; one JSON line per clip is appended to
design/generation/gen-log.jsonl.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path

os.environ.setdefault("HF_HOME", "F:/7270/a2-gen/hf-cache")

import numpy as np
import soundfile as sf
import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration

REPO = Path(__file__).resolve().parents[2]
LOG = REPO / "design" / "generation" / "gen-log.jsonl"
RAW = Path("F:/7270/a2-gen/gen-raw")
MODEL_ID = "facebook/musicgen-medium"
REVISION = "d3bd7b00761b78ad7a8a05145ee31e7832e9916c"  # pinned Hugging Face commit
MODEL = "MusicGen medium (Meta, facebook/musicgen-medium), weights CC-BY-NC 4.0, run locally with transformers"


def run(model, processor, device, job, defaults):
    """One generation job: {id, prompt, seed, seconds, batch, guidance, temperature, top_k, note}."""
    a = {**defaults, **job}
    rate = model.config.audio_encoder.sampling_rate
    tokens = int(a["seconds"] * model.config.audio_encoder.frame_rate)
    torch.manual_seed(a["seed"])
    inputs = processor(text=[a["prompt"]] * a["batch"], padding=True, return_tensors="pt").to(device)
    with torch.no_grad():
        audio = model.generate(**inputs, do_sample=True, guidance_scale=a["guidance"], temperature=a["temperature"],
                               top_k=a["top_k"], max_new_tokens=tokens)
    audio = audio.float().cpu().numpy()[:, 0, :]
    out_dir = RAW / a["id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    with LOG.open("a", encoding="utf-8") as log:
        for i, clip in enumerate(audio):
            name = f"{a['id']}-s{a['seed']}-b{i}.wav"
            sf.write(out_dir / name, clip / max(1e-9, np.abs(clip).max()) * 0.9, rate, subtype="PCM_16")
            digest = hashlib.sha256((out_dir / name).read_bytes()).hexdigest()
            rec = {"time": stamp, "asset_id": a["id"], "file": f"gen-raw/{a['id']}/{name}", "model": MODEL,
                   "model_revision": REVISION, "prompt": a["prompt"], "seed": a["seed"], "batch_index": i,
                   "batch": a["batch"], "seconds": a["seconds"], "guidance": a["guidance"],
                   "temperature": a["temperature"], "top_k": a["top_k"], "sample_rate": rate,
                   "postprocess": "peak-normalised to 0.9 at export", "output_sha256": digest, "note": a.get("note", "")}
            log.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(out_dir / name, flush=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jobs", help="JSON file with a list of jobs (model is loaded once)")
    p.add_argument("--id")
    p.add_argument("--prompt")
    p.add_argument("--seed", type=int)
    p.add_argument("--seconds", type=float, default=8.0)
    p.add_argument("--guidance", type=float, default=3.0)
    p.add_argument("--temperature", type=float, default=1.0)
    p.add_argument("--top_k", type=int, default=250)
    p.add_argument("--batch", type=int, default=1)
    p.add_argument("--note", default="")
    a = p.parse_args()
    defaults = {"seconds": a.seconds, "guidance": a.guidance, "temperature": a.temperature, "top_k": a.top_k,
                "batch": a.batch, "note": a.note}
    jobs = json.loads(Path(a.jobs).read_text(encoding="utf-8")) if a.jobs else         [{"id": a.id, "prompt": a.prompt, "seed": a.seed}]

    device = "cuda" if torch.cuda.is_available() else "cpu"
    processor = AutoProcessor.from_pretrained(MODEL_ID, revision=REVISION)
    model = MusicgenForConditionalGeneration.from_pretrained(MODEL_ID, revision=REVISION, torch_dtype=torch.float16).to(device)
    for job in jobs:
        run(model, processor, device, job, defaults)


if __name__ == "__main__":
    main()
