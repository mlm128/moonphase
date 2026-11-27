#!/usr/bin/env python3
"""moonphase_img.py — photographic moon phase images for any date.

Modes:
    python3 moonphase_img.py [YYYY-MM-DD]                 single moon PNG
    python3 moonphase_img.py [YYYY-MM-DD] --card          vertical poster card
    python3 moonphase_img.py [YYYY-MM-DD] --cycle         12-moon cycle chart

Technique: a real full-moon texture (Wikimedia Commons, photo by Luc
Viatour — auto-downloaded on first run if moon_texture.jpg is absent),
shaded per-pixel by the terminator geometry implied by the moon's age,
on a starry black sky. Numbers match moonphase.py (same anchor & cycle).
"""
import io
import math
import os
import random
import sys
import urllib.request
from datetime import date, datetime, time, timedelta, timezone

import numpy as np
from PIL import Image, ImageDraw, ImageFont

SYNODIC = 29.530588853
NEW_MOON_UTC = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
TEXTURE_URL = ("https://upload.wikimedia.org/wikipedia/commons/d/dd/"
               "Full_Moon_Luc_Viatour.jpg")
HERE = os.path.dirname(os.path.abspath(__file__))
TEXTURE_PATH = os.path.join(HERE, "moon_texture.jpg")

PHASES = [
    ("新月", "New Moon"),
    ("娥眉月", "Waxing Crescent"),
    ("上弦月", "First Quarter"),
    ("盈凸月", "Waxing Gibbous"),
    ("满月", "Full Moon"),
    ("亏凸月", "Waxing Gibbous".replace("Waxing", "Waning")),
    ("下弦月", "Last Quarter"),
    ("残月", "Waning Crescent"),
]
EVENTS = [(0.0, "新月"), (SYNODIC / 4, "上弦月"),
          (SYNODIC / 2, "满月"), (3 * SYNODIC / 4, "下弦月")]

FONT_SANS = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_SERIF_B = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


# ---------------------------------------------------------------- math
def moon_age(d: date) -> float:
    dt = datetime.combine(d, time(12, 0), tzinfo=timezone.utc)
    return (dt - NEW_MOON_UTC).total_seconds() / 86400.0 % SYNODIC


def phase_info(age: float):
    idx = int(((age + SYNODIC / 16) % SYNODIC) / (SYNODIC / 8))
    theta = 2 * math.pi * age / SYNODIC
    illum = (1 - math.cos(theta)) / 2
    return PHASES[idx], illum


def next_events(d: date, age: float, count=3):
    out = []
    for target, name in EVENTS:
        delta = (target - age) % SYNODIC
        if delta < 0.5:
            delta += SYNODIC
        out.append((d + timedelta(days=round(delta)), name))
    return sorted(out)[:count]


# ---------------------------------------------------------------- texture
def load_texture() -> Image.Image:
    if not os.path.exists(TEXTURE_PATH):
        req = urllib.request.Request(TEXTURE_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        with open(TEXTURE_PATH, "wb") as f:
            f.write(data)
    tex = Image.open(TEXTURE_PATH).convert("L")
    w, h = tex.size
    s = min(w, h)
    return tex.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))


_TEX_CACHE = {}


def render_moon(age: float, diameter: int) -> Image.Image:
    """One moon disc (RGB, black background) at the given age."""
    ss = 2  # supersample
    D = diameter * ss
    if D not in _TEX_CACHE:
        _TEX_CACHE[D] = np.asarray(
            load_texture().resize((D, D), Image.LANCZOS), dtype=np.float32) / 255.0
    tex = _TEX_CACHE[D]
    yy, xx = np.mgrid[0:D, 0:D]
    x = (xx - D / 2) / (D / 2)
    y = (yy - D / 2) / (D / 2)
    r2 = x * x + y * y
    inside = r2 <= 1.0
    z = np.sqrt(np.clip(1.0 - r2, 0, 1))
    theta = 2 * math.pi * age / SYNODIC
    v = x * math.sin(theta) - z * math.cos(theta)
    light = np.clip(0.5 + v / (2 * 0.055), 0, 1)
    moon = tex * (0.03 + 0.97 * light)
    moon = np.where(inside, moon, 0.0)
    img = Image.fromarray((np.clip(moon, 0, 1) * 255).astype(np.uint8), "L").convert("RGB")
    return img.resize((diameter, diameter), Image.LANCZOS)


def star_canvas(w: int, h: int, seed=42, n=320) -> Image.Image:
    img = Image.new("RGB", (w, h), (0, 0, 0))
    px = img.load()
    rnd = random.Random(seed)
    for _ in range(n):
        sx, sy = rnd.randrange(w), rnd.randrange(h)
        b = rnd.choice([60, 90, 120, 160, 200])
        px[sx, sy] = (b, b, min(255, int(b * 1.06)))
    return img


def centered(draw, cx, y, text, fnt, fill):
    box = draw.textbbox((0, 0), text, font=fnt)
    draw.text((cx - (box[2] - box[0]) / 2, y), text, font=fnt, fill=fill)
    return y + (box[3] - box[1])


# ---------------------------------------------------------------- modes
def mode_single(d: date, out: str):
    age = moon_age(d)
    size, disc = 900, 760
    img = star_canvas(size, size)
    img.paste(render_moon(age, disc), ((size - disc) // 2, (size - disc) // 2))
    img.save(out)
    return age


def mode_card(d: date, out: str):
    age = moon_age(d)
    (cn, en), illum = phase_info(age)
    W, H, disc = 1080, 1520, 820
    img = star_canvas(W, H, n=420)
    img.paste(render_moon(age, disc), ((W - disc) // 2, 90))
    dr = ImageDraw.Draw(img)
    cx = W // 2
    y = centered(dr, cx, 960, cn, font(FONT_SERIF_B, 120), (245, 243, 235))
    y = centered(dr, cx, y + 26, en.upper(), font(FONT_SANS, 40), (168, 172, 185))
    y = centered(dr, cx, y + 58, d.strftime("%Y 年 %-m 月 %-d 日"), font(FONT_SANS, 44), (225, 227, 232))
    y = centered(dr, cx, y + 30, f"照亮 {illum * 100:.1f}%  ·  月龄 {age:.1f} 天",
                 font(FONT_SANS, 44), (225, 227, 232))
    ev = next_events(d, age)
    ev_txt = "  ·  ".join(f"{name} {dt.month}月{dt.day}日" for dt, name in ev)
    centered(dr, cx, y + 64, ev_txt, font(FONT_SANS, 36), (150, 155, 168))
    img.save(out)
    return age


def mode_cycle(d: date, out: str):
    age0 = moon_age(d)
    start = d - timedelta(days=int(age0))
    cols, rows = 3, 4
    cell_w, cell_h, disc = 500, 560, 400
    W, H = cols * cell_w, rows * cell_h + 150
    img = star_canvas(W, H, n=700)
    dr = ImageDraw.Draw(img)
    centered(dr, W // 2, 42, "月 相 周 期", font(FONT_SERIF_B, 64), (245, 243, 235))
    for i in range(cols * rows):
        a = i * SYNODIC / 12
        (cn, _), illum = phase_info(a)
        r, c = divmod(i, cols)
        x0, y0 = c * cell_w, 150 + r * cell_h
        img.paste(render_moon(a, disc), (x0 + (cell_w - disc) // 2, y0))
        dt = start + timedelta(days=round(a))
        centered(dr, x0 + cell_w // 2, y0 + disc + 14, cn, font(FONT_SANS, 40), (235, 236, 240))
        centered(dr, x0 + cell_w // 2, y0 + disc + 68,
                 f"{dt.month}月{dt.day}日 · {illum * 100:.0f}%", font(FONT_SANS, 30), (150, 155, 168))
    img.save(out)
    return age0


if __name__ == "__main__":
    argv = sys.argv[1:]
    mode = "single"
    if "--card" in argv:
        mode, argv = "card", [a for a in argv if a != "--card"]
    if "--cycle" in argv:
        mode, argv = "cycle", [a for a in argv if a != "--cycle"]
    if argv and "-" in argv[0]:
        d = datetime.strptime(argv[0], "%Y-%m-%d").date()
    else:
        d = datetime.now(timezone(timedelta(hours=8))).date()
    suffix = {"single": "", "card": "-card", "cycle": "-cycle"}[mode]
    out = argv[1] if len(argv) > 1 else f"moon-{d.isoformat()}{suffix}.png"
    fn = {"single": mode_single, "card": mode_card, "cycle": mode_cycle}[mode]
    age = fn(d, out)
    (cn, en), illum = phase_info(age)
    print(f"{d}  {cn} {en}  age={age:.2f}d  illumination={illum * 100:.1f}%  -> {out}")
