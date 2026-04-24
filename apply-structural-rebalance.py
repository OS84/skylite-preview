#!/usr/bin/env python3
"""apply-structural-rebalance.py — Rebalance MEDIA.structural.

Replaces the current 14-tile strip with an 18-tile curated selection:
  - Lead with highest-quality shots (multiple files >500KB were missing)
  - Better shape balance (7 dome, 4 pyramid, 3 cone, 2 arch, 2 project teasers)
  - Add missing hero-rank: כיפה/049.jpeg (1MB), קשת/סקייליט מקומר בניין
    עתידים.JPG (1MB, named project), כיפה/048.jpeg (710KB)
  - Swap weak cone files (4.jpg, 110.jpg) for stronger (1.jpg, 2.jpg, 5.jpg)
  - Project teasers stay at the end (unchanged)

Idempotent (re-run safe).
"""
import sys, pathlib, re

HTML = pathlib.Path(__file__).parent / "index.html"
src = HTML.read_text(encoding="utf-8")

NEW_BODY = """    { type:'img', src:'04 — מבנים מרחביים/כיפה/049.jpeg' },
    { type:'img', src:'04 — מבנים מרחביים/קשת/סקייליט מקומר בניין עתידים.JPG', cap:'בניין עתידים' },
    { type:'img', src:'04 — מבנים מרחביים/כיפה/048.jpeg' },
    { type:'img', src:'04 — מבנים מרחביים/פירמידה/Edited-24.jpg' },
    { type:'img', src:'04 — מבנים מרחביים/כיפה/Edited-22.jpg' },
    { type:'img', src:'04 — מבנים מרחביים/פירמידה/Edited-6.jpg' },
    { type:'img', src:'04 — מבנים מרחביים/קשת/71.jpg' },
    { type:'img', src:'04 — מבנים מרחביים/חרוט/1.jpg' },
    { type:'img', src:'04 — מבנים מרחביים/כיפה/Edited-1.jpg' },
    { type:'img', src:'04 — מבנים מרחביים/פירמידה/Edited-14.jpg' },
    { type:'img', src:'04 — מבנים מרחביים/חרוט/2.jpg' },
    { type:'img', src:'04 — מבנים מרחביים/חרוט/5.jpg' },
    { type:'img', src:'04 — מבנים מרחביים/כיפה/046.jpg' },
    { type:'img', src:'04 — מבנים מרחביים/כיפה/034.jpg' },
    { type:'img', src:'04 — מבנים מרחביים/כיפה/035.jpg' },
    { type:'img', src:'04 — מבנים מרחביים/פירמידה/025.jpg' },
    { type:'img', src:'04 — מבנים מרחביים/כיפה/בית כנסת יגדיל תורה - אור יהודה/M53_0154-.jpg-main.jpg', cap:'בית כנסת יגדיל תורה' },
    { type:'img', src:'04 — מבנים מרחביים/פירמידה/מרכז מבקרים יקב רקנאטי - פארק תעשיות רמת דלתון/DJI_20260225203307_0163_D.jpg', cap:'יקב רקנאטי' },"""

# Fingerprint of the new body — if already applied, bail.
SIGNATURE = "04 — מבנים מרחביים/כיפה/049.jpeg"
if SIGNATURE in src:
    print("✔  Already applied — MEDIA.structural contains 049.jpeg")
    sys.exit(0)

# Locate MEDIA={...}, then structural: [ ... ] within it, and replace the array body.
m = re.search(r"const MEDIA\s*=\s*\{", src)
if not m:
    print("❌ const MEDIA not found"); sys.exit(1)
media_start = m.end()

# From media_start, find structural: [
ms = re.search(r"structural:\s*\[", src[media_start:])
if not ms:
    print("❌ structural: [ not found inside MEDIA"); sys.exit(1)
body_start = media_start + ms.end()

# Find the matching closing "  ],"  (the line with just "  ]," after the array body)
close_match = re.search(r"\n\s*\],", src[body_start:])
if not close_match:
    print("❌ closing '  ],' not found for MEDIA.structural"); sys.exit(1)
body_end = body_start + close_match.start()

old_body = src[body_start:body_end]
new_src = src[:body_start] + "\n" + NEW_BODY + src[body_end:]

HTML.write_text(new_src, encoding="utf-8")
print(f"✅ MEDIA.structural rebuilt (18 tiles)")
print(f"   Replaced {len(old_body.strip().splitlines())} lines of tile entries")
