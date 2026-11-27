# moonphase 🌙

A tiny CLI tool that tells you the moon phase for any date.

Built by DeepSeek Harness (DeepSeek-V3.2 via SiliconFlow) as a first
playground project, with the phase-name mapping fixed on the second pass.

## Usage

```bash
python3 moonphase.py            # today (Asia/Shanghai)
python3 moonphase.py 2026-11-24 # any date, YYYY-MM-DD
```

## Output

- Moon age (days into the synodic cycle, 29.530588853 days,
  anchored at the new moon of 2000-01-06 18:14 UTC)
- Illumination percentage
- Phase name in English and Chinese (8 standard phases)
- A small ASCII moon, lit from the correct side

Standard library only. No dependencies.
