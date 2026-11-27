# moonphase 🌙

Moon phase tools: a text CLI and a photographic image renderer.

- `moonphase.py` — text output: moon age, illumination, phase name
  (Chinese + English) and a small ASCII moon.
- `moonphase_img.py` — photographic output: renders the moon for any
  date from a real full-moon texture, shaded per-pixel by the true
  terminator geometry. Three modes below.

Both share the same math: synodic month 29.530588853 days, anchored at
the new moon of 2000-01-06 18:14 UTC.

## Text version

```bash
python3 moonphase.py            # today (Asia/Shanghai)
python3 moonphase.py 2026-11-24 # any date, YYYY-MM-DD
```

## Image version

```bash
python3 moonphase_img.py                    # single moon PNG (today)
python3 moonphase_img.py 2026-11-24         # single moon PNG (that date)
python3 moonphase_img.py 2026-11-27 --card  # vertical poster card:
                                            # phase name, date,
                                            # illumination, moon age,
                                            # next quarter events
python3 moonphase_img.py 2026-11-27 --cycle # 12-moon chart of the
                                            # whole lunar cycle
```

Requires Python 3 with Pillow and numpy. On first run it downloads the
full-moon texture (`moon_texture.jpg`, Wikimedia Commons, photo by
Luc Viatour, CC BY-SA) next to the script and reuses it afterwards.

History: the text version was built by DeepSeek Harness (DeepSeek-V3.2
via SiliconFlow); the image version was written by Camus after studying
how GitHub projects such as MoonTex render phase images.
