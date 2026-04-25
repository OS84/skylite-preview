#!/usr/bin/env python3
"""apply-smoke-curate.py — Curate MEDIA.smoke after visual review.

Visual audit of all 19 images in 05 — כיפות תאורה ושחרור עשן revealed:

DUPLICATES (drop the dup):
  • 118.jpg = 252.jpg (identical TA rooftop) — keep 252, drop 118
  • 13 (1).jpg ≈ 253.jpg (same hilltop dome) — keep 253, drop 13 (1)

POOR QUALITY / WEAK SCENES (drop):
  • 22.jpg — palm tree obscures, awkward composition
  • 18.jpg — construction debris, feels unfinished
  • 255.jpg — generic institutional, low-res
  • 254.jpg — small interior, weaker than 9.jpg
  • שחרור עשן.jpg — close-up no context, low-res

ADD MISSING STRONG TILE:
  • 9.jpg — only good interior shot in folder (grid ceiling)

Result: 18 → 12 tiles, no dups, all strong, better diversity (residential,
commercial, hospitality, heritage, atmospheric, interior).
"""
import sys, pathlib, re

HTML = pathlib.Path(__file__).parent / "index.html"
src = HTML.read_text(encoding="utf-8")

NEW_BODY = """    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/בית פרטי חד שיפועי שחרור עשן.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/גפני1.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/AlfVjy-ryenVRYXksChGM_1Zu0pUByH44zoXInIzwZqq.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/251.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/252.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/213.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/142.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/130.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/262.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/253.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/265.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/9.jpg' },"""

# Find MEDIA.smoke array body and replace contents
m = re.search(r"const MEDIA\s*=\s*\{", src)
if not m:
    print("❌ const MEDIA not found"); sys.exit(1)
ms = re.search(r"smoke:\s*\[", src[m.end():])
if not ms:
    print("❌ smoke: [ not found"); sys.exit(1)
body_start = m.end() + ms.end()
close = re.search(r"\n\s*\],", src[body_start:])
if not close:
    print("❌ closing for MEDIA.smoke not found"); sys.exit(1)
body_end = body_start + close.start()

old_body = src[body_start:body_end]
old_count = len(re.findall(r"src:'", old_body))

if old_body.strip() == NEW_BODY.strip():
    print("✔  MEDIA.smoke already curated — no changes")
else:
    src = src[:body_start] + "\n" + NEW_BODY + src[body_end:]
    HTML.write_text(src, encoding="utf-8")
    print(f"✅ MEDIA.smoke curated: {old_count} → 12 tiles")
    print("   Dropped: 22, 18, 13 (1), 118, 254, 255, שחרור עשן")
    print("   Added:   9.jpg (only good interior)")
    print("   Reordered for visual impact")
