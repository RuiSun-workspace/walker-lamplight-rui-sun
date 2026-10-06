"""Cut Rui's hand-drawn storyboard page (one phone photo) into eight panel images.

No drawing is changed. Each panel is cropped (with its handwritten caption), the paper is
flattened by dividing out a heavy blur (removes the shadow and the bed-sheet tint), and the
result is saved as greyscale PNG. Crop boxes were read off the photo by eye.

    python design/storyboard/hand/crop_panels.py
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter, ImageOps

HERE = Path(__file__).resolve().parent
PHOTO = HERE / "storyboard-page-photo-2026-10-06.jpg"

# play order -> (left, top, right, bottom) in the 1080x1920 photo, caption included
PANELS = {
    "01-design-view": (30, 330, 508, 635),
    "02-first-frame": (500, 328, 1060, 630),
    "03-jump": (25, 650, 525, 965),
    "04-oil-absorbed": (565, 660, 1030, 955),
    "05-oil-empty": (20, 1010, 495, 1310),
    "06-died": (12, 1345, 505, 1680),
    "07-restart": (560, 1340, 1018, 1680),
    "08-escape": (552, 995, 1022, 1305),
}


def flatten(img):
    g = ImageOps.grayscale(img)
    bg = g.filter(ImageFilter.GaussianBlur(25))
    a = np.asarray(g, np.float32) / np.maximum(np.asarray(bg, np.float32), 1.0)  # paper -> ~1, ink stays dark
    flat = Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8))
    return ImageOps.autocontrast(flat, cutoff=(1, 0))


if __name__ == "__main__":
    page = Image.open(PHOTO)
    for name, box in PANELS.items():
        out = flatten(page.crop(box))
        out.save(HERE / f"{name}.png")
        print("wrote", name, out.size)
