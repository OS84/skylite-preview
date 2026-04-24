#!/usr/bin/env python3
"""apply-opener-swaps.py — Swap weak opener tiles for stronger alternatives.

Per audit Agent 4's critique — top tile of each product strip sets the tone.

  • Fixed:      Edited-2.jpg (clinical look-up) → DSC05064.jpg (20MB pro shot)
  • Structural: swap positions 1↔2 so "בניין עתידים" leads over 049.jpeg
  • Smoke:      swap positions 1↔2 so "בית פרטי חד שיפועי שחרור עשן" leads
                over the 22.jpg rooftop shot

Walk-on left unchanged per user decision.

Idempotent.
"""
import sys, pathlib

HTML = pathlib.Path(__file__).parent / "index.html"
src = HTML.read_text(encoding="utf-8")
changes = 0

def swap(old, new, label):
    global src, changes
    if new in src:
        print(f"✔  {label} — already applied")
        return
    if old not in src:
        print(f"❌ {label} — anchor not found")
        sys.exit(1)
    src = src.replace(old, new, 1)
    changes += 1
    print(f"✔  {label}")

# ═══════════════════════════════════════════════════════════════
# Fixed — replace opener with DSC05064 (20MB pro photography)
# ═══════════════════════════════════════════════════════════════
swap(
    "{ type:'img', src:'02 — סקיילייט קבוע/חד שיפועי/Edited-2.jpg', cap:'' },",
    "{ type:'img', src:'02 — סקיילייט קבוע/חד שיפועי/DSC05064.jpg', cap:'' },",
    "Fixed: swap Edited-2.jpg → DSC05064.jpg"
)

# ═══════════════════════════════════════════════════════════════
# Structural — swap positions 1 and 2 (Atidim leads over 049.jpeg)
# ═══════════════════════════════════════════════════════════════
STRUCT_OLD = """    { type:'img', src:'04 — מבנים מרחביים/כיפה/049.jpeg' },
    { type:'img', src:'04 — מבנים מרחביים/קשת/סקייליט מקומר בניין עתידים.JPG', cap:'בניין עתידים' },"""
STRUCT_NEW = """    { type:'img', src:'04 — מבנים מרחביים/קשת/סקייליט מקומר בניין עתידים.JPG', cap:'בניין עתידים' },
    { type:'img', src:'04 — מבנים מרחביים/כיפה/049.jpeg' },"""
swap(STRUCT_OLD, STRUCT_NEW, "Structural: swap positions 1↔2 (Atidim leads)")

# ═══════════════════════════════════════════════════════════════
# Smoke — swap positions 1 and 2 (בית פרטי leads over 22.jpg)
# ═══════════════════════════════════════════════════════════════
SMOKE_OLD = """    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/22.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/בית פרטי חד שיפועי שחרור עשן.jpg' },"""
SMOKE_NEW = """    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/בית פרטי חד שיפועי שחרור עשן.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/22.jpg' },"""
swap(SMOKE_OLD, SMOKE_NEW, "Smoke: swap positions 1↔2 (בית פרטי leads)")

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — everything already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
