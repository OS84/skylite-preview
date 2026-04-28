#!/usr/bin/env python3
"""apply-fixed-pilot-fix2.py — Deduplicate MEDIA.fixed strip.

Principle: the strip is the "atmosphere reel" of off-project product shots.
Named projects (Mitzpe, HP HQ, Mishya, Beit Zait, Beit Yokra, Bar-Ilan,
Beit Gil HaZahav) already get their own dedicated detail pages with full
galleries. Showing those same hero images twice on the fixed page (strip
+ project tile) makes both feel redundant and dilutes impact.

Result
======
15 tiles → 6 tiles, all off-project, all generic product shots:
  1. DSC05064  — single-slope hero    (wide)
  2. סקיילייט דו שיפועי על גג רעפים — dual-slope tile roof
  3. Edited-10 — single-slope vertical  (tall)
  4. 217      — dual-slope detail        (tall)
  5. חצר אנגלית — English courtyard
  6. בית פרטי 2 — private dual-slope home

3-col mosaic math: 1×2 wide + 2×2 tall + 3×1 sq = 9 cells = 3 perfect rows.
No gaps, every tile pulls weight, all show product variations rather than
named project repeats.

Idempotent.
"""
import sys, pathlib, re

HTML = pathlib.Path(__file__).parent / "index.html"
src = HTML.read_text(encoding="utf-8")

# ═══════════════════════════════════════════════════════════════
# Locate MEDIA.fixed array body and rewrite it.
# ═══════════════════════════════════════════════════════════════

NEW_BODY = """    { type:'img', src:'02 — סקיילייט קבוע/חד שיפועי/DSC05064.jpg', cap:'', aspect:'wide' },
    { type:'img', src:'02 — סקיילייט קבוע/דו שיפועי/סקיילייט דו שיפועי על גג רעפים.jpg', cap:'' },
    { type:'img', src:'02 — סקיילייט קבוע/חד שיפועי/Edited-10.jpg', cap:'', aspect:'tall' },
    { type:'img', src:'02 — סקיילייט קבוע/דו שיפועי/217.jpg', cap:'', aspect:'tall' },
    { type:'img', src:'02 — סקיילייט קבוע/חצר אנגלית/חצר אנגלית.jpeg', cap:'' },
    { type:'img', src:'02 — סקיילייט קבוע/דו שיפועי/בית פרטי 2.jpg', cap:'' },"""

# Find the start of MEDIA.fixed array body
m = re.search(r"\bfixed:\s*\[\n", src)
if not m:
    print("❌ MEDIA.fixed: anchor not found"); sys.exit(1)
body_start = m.end()

# Find matching closing `  ],\n` for THIS array — first one after body_start.
close = re.search(r"\n  \],\n", src[body_start:])
if not close:
    print("❌ MEDIA.fixed: closing not found"); sys.exit(1)
body_end = body_start + close.start() + 1  # include the leading \n

old_body = src[body_start:body_end]
old_count = len(re.findall(r"src:'", old_body))

if old_body.strip() == NEW_BODY.strip():
    print("✔  MEDIA.fixed already curated — no changes")
else:
    src = src[:body_start] + NEW_BODY + "\n" + src[body_end:]
    HTML.write_text(src, encoding="utf-8")
    print(f"✅ MEDIA.fixed curated: {old_count} → 6 tiles (off-project only)")
    print("   Dropped: 9 named-project repeats (Mitzpe, HP HQ, Mishya,")
    print("            Beit Zait, Beit Yokra, Bar-Ilan)")
    print("   Kept:    1 wide + 2 tall + 3 square — 3 clean mosaic rows")
