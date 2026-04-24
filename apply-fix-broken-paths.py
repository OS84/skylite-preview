#!/usr/bin/env python3
"""apply-fix-broken-paths.py — Repair image references broken by folder reorgs.

Audit found 4 broken image paths:
  1. Pool images (63, 65, Edited-27) — moved from "קירוי בריכה/" subfolder
     up to "01 — סקיילייט נוסע/" root.
  2. Dome file "049.jpeg" — actual file is "049.jpg" (extension changed).
"""
import sys, pathlib

HTML = pathlib.Path(__file__).parent / "index.html"
src = HTML.read_text(encoding="utf-8")
changes = 0

def swap_all(old, new, label):
    global src, changes
    count = src.count(old)
    if count == 0:
        new_count = src.count(new)
        if new_count:
            print(f"✔  {label} — already fixed ({new_count} already uses new path)")
            return
        print(f"⚠  {label} — anchor not found; skipping")
        return
    src = src.replace(old, new)
    changes += count
    print(f"✔  {label} ({count} replaced)")

swap_all(
    "01 — סקיילייט נוסע/קירוי בריכה/63.jpg",
    "01 — סקיילייט נוסע/63.jpg",
    "Pool: 63.jpg → root"
)
swap_all(
    "01 — סקיילייט נוסע/קירוי בריכה/65.jpg",
    "01 — סקיילייט נוסע/65.jpg",
    "Pool: 65.jpg → root"
)
swap_all(
    "01 — סקיילייט נוסע/קירוי בריכה/Edited-27.jpg",
    "01 — סקיילייט נוסע/Edited-27.jpg",
    "Pool: Edited-27.jpg → root"
)
swap_all(
    "04 — מבנים מרחביים/כיפה/049.jpeg",
    "04 — מבנים מרחביים/כיפה/049.jpg",
    "Dome: 049.jpeg → 049.jpg (extension fix)"
)

if changes == 0:
    print("\n(No changes — already fixed.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} reference(s) repaired)")
