"""Convert LetzAI originals (assets/img-src, git-ignored) into web files under assets/img/ai
and register them in tools/images.json.   python tools/ai_to_web.py"""
import json, os, shutil
from PIL import Image

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lock = json.load(open(f"{R}/tools/ai-media.lock.json"))
images = json.load(open(f"{R}/tools/images.json"))
out = f"{R}/assets/img/ai"
os.makedirs(out, exist_ok=True)
SIZES = {"hero": (2400, 960), "tile": (1600, 720)}

for name, v in lock.items():
    src = f"{R}/{v['file']}"
    if not os.path.exists(src):
        continue
    if v["kind"] == "video":
        shutil.copyfile(src, f"{out}/{name}.mp4")
        print(name, "video", os.path.getsize(src) // 1024, "KB")
        continue
    big, small = SIZES["hero" if name.startswith("hero") else "tile"]
    im = Image.open(src).convert("RGB")
    for w, suffix in ((big, ""), (small, "-s")):
        c = im.copy()
        c.thumbnail((w, w * 2), Image.LANCZOS)
        c.save(f"{out}/{name}{suffix}.webp", "WEBP", quality=82, method=6)
    images[f"ai/{name}"] = {"l": f"assets/img/ai/{name}.webp", "s": f"assets/img/ai/{name}-s.webp"}
    print(name, im.size, "->", big, small)

json.dump(images, open(f"{R}/tools/images.json", "w"), indent=1)
