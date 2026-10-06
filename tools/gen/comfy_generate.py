"""Run one SDXL generation through a local ComfyUI server and log it reproducibly.

Written by Claude. ComfyUI must already be running locally, e.g.

    F:/7270/a2-gen/venv/Scripts/python.exe F:/7270/a2-gen/ComfyUI/main.py --listen 127.0.0.1 --port 8188

Example (txt2img):

    python tools/gen/comfy_generate.py --id CHAR-REF --prompt "..." --negative "..." \
        --seed 1001 --width 1024 --height 1024 --batch 4

Example (img2img from an init image):

    python tools/gen/comfy_generate.py --id CHAR-WALK --init path/to/init.png --denoise 0.55 ...

Raw images go to F:/7270/a2-gen/gen-raw/<ID>/ (outside the repo). Every image gets one JSON line
in design/generation/gen-log.jsonl with everything needed to reproduce it.
"""
import argparse
import datetime as dt
import hashlib
import json
import shutil
import time
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LOG = REPO / "design" / "generation" / "gen-log.jsonl"
RAW = Path("F:/7270/a2-gen/gen-raw")
COMFY = Path("F:/7270/a2-gen/ComfyUI")
SERVER = "http://127.0.0.1:8188"
CKPT = "sd_xl_base_1.0.safetensors"
MODEL = "Stable Diffusion XL base 1.0 (stabilityai), CreativeML Open RAIL++-M, run locally in ComfyUI"


def post(path, payload):
    req = urllib.request.Request(SERVER + path, json.dumps(payload).encode(), {"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req).read())


def get(path):
    return urllib.request.urlopen(SERVER + path).read()


def workflow(a, init_name):
    wf = {
        "ckpt": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CKPT}},
        "pos": {"class_type": "CLIPTextEncode", "inputs": {"text": a.prompt, "clip": ["ckpt", 1]}},
        "neg": {"class_type": "CLIPTextEncode", "inputs": {"text": a.negative, "clip": ["ckpt", 1]}},
        "sample": {"class_type": "KSampler", "inputs": {
            "model": ["ckpt", 0], "positive": ["pos", 0], "negative": ["neg", 0],
            "seed": a.seed, "steps": a.steps, "cfg": a.cfg, "sampler_name": a.sampler,
            "scheduler": a.scheduler, "denoise": a.denoise, "latent_image": ["latent", 0]}},
        "decode": {"class_type": "VAEDecode", "inputs": {"samples": ["sample", 0], "vae": ["ckpt", 2]}},
        "save": {"class_type": "SaveImage", "inputs": {"images": ["decode", 0], "filename_prefix": a.id}},
    }
    if init_name:
        wf["load"] = {"class_type": "LoadImage", "inputs": {"image": init_name}}
        wf["enc"] = {"class_type": "VAEEncode", "inputs": {"pixels": ["load", 0], "vae": ["ckpt", 2]}}
        wf["latent"] = {"class_type": "RepeatLatentBatch", "inputs": {"samples": ["enc", 0], "amount": a.batch}}
    else:
        wf["latent"] = {"class_type": "EmptyLatentImage",
                        "inputs": {"width": a.width, "height": a.height, "batch_size": a.batch}}
    return wf


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--id", required=True, help="asset ID, e.g. CHAR-REF")
    p.add_argument("--prompt", required=True)
    p.add_argument("--negative", default="")
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--width", type=int, default=1024)
    p.add_argument("--height", type=int, default=1024)
    p.add_argument("--steps", type=int, default=30)
    p.add_argument("--cfg", type=float, default=7.0)
    p.add_argument("--sampler", default="dpmpp_2m")
    p.add_argument("--scheduler", default="karras")
    p.add_argument("--denoise", type=float, default=1.0)
    p.add_argument("--batch", type=int, default=1)
    p.add_argument("--init", help="init image for img2img")
    p.add_argument("--note", default="", help="why this run was made")
    a = p.parse_args()

    init_name = None
    if a.init:
        init_name = f"{a.id}-init-{Path(a.init).name}"
        shutil.copy(a.init, COMFY / "input" / init_name)

    pid = post("/prompt", {"prompt": workflow(a, init_name)})["prompt_id"]
    while True:
        hist = json.loads(get(f"/history/{pid}"))
        if pid in hist and hist[pid].get("outputs"):
            break
        time.sleep(1)

    out_dir = RAW / a.id
    out_dir.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    images = hist[pid]["outputs"]["save"]["images"]
    stamp = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    with LOG.open("a", encoding="utf-8") as log:
        for i, im in enumerate(images):
            q = urllib.parse.urlencode({"filename": im["filename"], "subfolder": im["subfolder"], "type": im["type"]})
            name = f"{a.id}-s{a.seed}-b{i}.png"
            (out_dir / name).write_bytes(get(f"/view?{q}"))
            rec = {"time": stamp, "asset_id": a.id, "file": f"gen-raw/{a.id}/{name}", "model": MODEL,
                   "checkpoint": CKPT, "prompt": a.prompt, "negative": a.negative, "seed": a.seed,
                   "batch_index": i, "batch": a.batch, "width": a.width, "height": a.height,
                   "steps": a.steps, "cfg": a.cfg, "sampler": a.sampler, "scheduler": a.scheduler,
                   "denoise": a.denoise, "init": str(a.init) if a.init else None,
                   "init_sha256": sha256(a.init) if a.init else None,
                   "output_sha256": sha256(out_dir / name), "note": a.note}
            log.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(out_dir / name)


if __name__ == "__main__":
    main()
