#!/usr/bin/env python3
"""apply-structural-pilot.py — Roll the fixed pilot out to structural.

What this ships:
  1. structural added to MEDIA_LAYOUT  → mosaic gallery
  2. structural added to PROJECTS_LAYOUT → hover-reveal tile cards
  3. MEDIA.structural curated 26 → 6 off-project tiles with aspect tags
     (1 wide + 2 tall + 3 sq = 9 cells = 3 perfect mosaic rows)

Lesson learned from fix2: anchor regex to `const MEDIA = {` and
`const PROJECTS=` BEFORE searching for `fixed:` / `structural:` etc.
Otherwise the first match wins and you clobber the wrong array.

Idempotent.
"""
import sys, pathlib, re

HTML = pathlib.Path(__file__).parent / "index.html"
src = HTML.read_text(encoding="utf-8")
changes = 0

def swap(old, new, label, must_exist=True):
    global src, changes
    if new in src and old not in src:
        print(f"✔  {label} — already applied")
        return
    if old not in src:
        if must_exist:
            print(f"❌ {label} — anchor not found")
            sys.exit(1)
        print(f"⚠  {label} — anchor missing, skipping")
        return
    src = src.replace(old, new, 1)
    changes += 1
    print(f"✔  {label}")

# ═══════════════════════════════════════════════════════════════
# 1) Add structural to layout maps
# ═══════════════════════════════════════════════════════════════
swap(
    "const MEDIA_LAYOUT = { fixed: 'mosaic' };",
    "const MEDIA_LAYOUT = { fixed: 'mosaic', structural: 'mosaic' };",
    "MEDIA_LAYOUT += structural",
)
swap(
    "const PROJECTS_LAYOUT = { fixed: 'tiles' };",
    "const PROJECTS_LAYOUT = { fixed: 'tiles', structural: 'tiles' };",
    "PROJECTS_LAYOUT += structural",
)

# ═══════════════════════════════════════════════════════════════
# 2) Curate MEDIA.structural — anchor to const MEDIA first!
# ═══════════════════════════════════════════════════════════════
media_start = src.find('const MEDIA = {')
if media_start == -1:
    print("❌ const MEDIA not found"); sys.exit(1)

# `  structural: [` — the indentation matches the existing format
struct_pos = src.find('  structural: [', media_start)
if struct_pos == -1:
    print("❌ MEDIA.structural: [ not found"); sys.exit(1)

body_start = struct_pos + len('  structural: [\n')
close_offset = src.find('\n  ],', body_start)
if close_offset == -1:
    print("❌ MEDIA.structural closing not found"); sys.exit(1)
body_end = close_offset + 1  # include leading \n before ],

old_body = src[body_start:body_end]
old_count = old_body.count("type:'img'")

NEW_BODY = """    { type:'img', src:'04 — מבנים מרחביים/קשת/סקייליט מקומר בניין עתידים.JPG', cap:'בניין עתידים', aspect:'wide' },
    { type:'img', src:'04 — מבנים מרחביים/פירמידה/Edited-24.jpg', cap:'', aspect:'tall' },
    { type:'img', src:'04 — מבנים מרחביים/כיפה/048.jpeg', cap:'', aspect:'tall' },
    { type:'img', src:'04 — מבנים מרחביים/כיפה/Edited-1.jpg', cap:'' },
    { type:'img', src:'04 — מבנים מרחביים/חרוט/1.jpg', cap:'' },
    { type:'img', src:'04 — מבנים מרחביים/קשת/71.jpg', cap:'' },
"""

if old_body.strip() == NEW_BODY.strip():
    print("✔  MEDIA.structural already curated")
else:
    src = src[:body_start] + NEW_BODY + src[body_end:]
    changes += 1
    print(f"✔  MEDIA.structural curated: {old_count} → 6 off-project tiles")
    print("   Pattern: 1 wide + 2 tall + 3 sq = 3 clean mosaic rows")

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
