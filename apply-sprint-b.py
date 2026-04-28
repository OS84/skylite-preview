#!/usr/bin/env python3
"""apply-sprint-b.py — Roll the proven pilot to all categories.

What ships
==========
penthouse:    mosaic + tiles + projects-first + MEDIA curated (4 vid + 2 still)
walkon:       tiles only (no MEDIA — off-project pool too thin)
retractable:  full pilot + ADD projects-sec DOM section + MEDIA curated (1 wide + 2 tall + 3 sq)
smoke:        full pilot + ADD projects-sec DOM section + MEDIA curated (1 wide + 2 tall + 3 sq)
windows:      skipped (only 6 similar tiles, mosaic doesn't add value)
fixed/structural: already done

After this:
  • All categories with projects render Option C tiles
  • All MEDIA strips are off-project (or hidden where impossible)
  • Projects-first DOM order across all pilot pages

Idempotent.
"""
import sys, pathlib

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
# 1) Layout maps — add all categories
# ═══════════════════════════════════════════════════════════════
swap(
    "const MEDIA_LAYOUT = { fixed: 'mosaic', structural: 'mosaic' };",
    "const MEDIA_LAYOUT = { fixed: 'mosaic', structural: 'mosaic', penthouse: 'mosaic', retractable: 'mosaic', smoke: 'mosaic' };",
    "MEDIA_LAYOUT += penthouse, retractable, smoke",
)
swap(
    "const PROJECTS_LAYOUT = { fixed: 'tiles', structural: 'tiles' };",
    "const PROJECTS_LAYOUT = { fixed: 'tiles', structural: 'tiles', penthouse: 'tiles', walkon: 'tiles', retractable: 'tiles', smoke: 'tiles' };",
    "PROJECTS_LAYOUT += penthouse, walkon, retractable, smoke",
)

# ═══════════════════════════════════════════════════════════════
# 2) MEDIA_HEADERS — add overrides for new pilot categories
# ═══════════════════════════════════════════════════════════════
swap(
    """const MEDIA_HEADERS = {
  fixed:      { eye: 'גלריה', title: 'המוצר במגוון' },
  structural: { eye: 'גלריה', title: 'המוצר במגוון' },
};""",
    """const MEDIA_HEADERS = {
  fixed:       { eye: 'גלריה', title: 'המוצר במגוון' },
  structural:  { eye: 'גלריה', title: 'המוצר במגוון' },
  penthouse:   { eye: 'גלריה', title: 'המוצר במגוון' },
  retractable: { eye: 'גלריה', title: 'המוצר בתנועה' },
  smoke:       { eye: 'גלריה', title: 'המוצר במגוון' },
};""",
    "MEDIA_HEADERS += penthouse, retractable, smoke",
)

# ═══════════════════════════════════════════════════════════════
# 3) Add projects-sec DOM section to retractable + smoke pages
# ═══════════════════════════════════════════════════════════════
swap(
    '<section class="pp-media" id="media-retractable"></section>',
    '<section class="pp-projects-section" id="projects-sec-retractable"></section>\n<section class="pp-media" id="media-retractable"></section>',
    "Retractable: + projects-sec section (projects-first)",
)
swap(
    '<section class="pp-media" id="media-smoke"></section>',
    '<section class="pp-projects-section" id="projects-sec-smoke"></section>\n<section class="pp-media" id="media-smoke"></section>',
    "Smoke: + projects-sec section (projects-first)",
)

# ═══════════════════════════════════════════════════════════════
# 4) Section order swap on penthouse (projects-first)
# ═══════════════════════════════════════════════════════════════
swap(
    '<section class="pp-media" id="media-penthouse"></section>\n<section class="pp-projects-section" id="projects-sec-penthouse"></section>',
    '<section class="pp-projects-section" id="projects-sec-penthouse"></section>\n<section class="pp-media" id="media-penthouse"></section>',
    "Penthouse: swap projects ↔ media (projects-first)",
)

# ═══════════════════════════════════════════════════════════════
# 5) Section order swap on walkon — also REMOVE pp-media (off-project pool too thin)
# ═══════════════════════════════════════════════════════════════
swap(
    '<section class="pp-media" id="media-walkon"></section>\n<section class="pp-projects-section" id="projects-sec-walkon"></section>',
    '<section class="pp-projects-section" id="projects-sec-walkon"></section>',
    "Walkon: hide pp-media (insufficient off-project images), keep projects-only",
)

# ═══════════════════════════════════════════════════════════════
# 6) Init loop — add retractable + smoke to renderProjectsSection calls
# ═══════════════════════════════════════════════════════════════
swap(
    "['penthouse','fixed','walkon','structural'].forEach(renderProjectsSection);",
    "['penthouse','fixed','walkon','structural','retractable','smoke'].forEach(renderProjectsSection);",
    "Init loop: add retractable + smoke",
)

# ═══════════════════════════════════════════════════════════════
# 7) MEDIA.penthouse — curate to 6 off-project tiles (4 vid + 2 still + aspects)
# ═══════════════════════════════════════════════════════════════
import re
media_start = src.find('const MEDIA = {')
penthouse_pos = src.find('  penthouse: [\n', media_start)
if penthouse_pos == -1:
    print("❌ MEDIA.penthouse anchor not found")
    sys.exit(1)
body_start = penthouse_pos + len('  penthouse: [\n')
close_offset = src.find('\n  ],', body_start)
body_end = close_offset + 1

old_body = src[body_start:body_end]
old_count = old_body.count("type:")

NEW_PENTHOUSE = """    { type:'vid', src:'06 — יציאה לגג/17.mp4', vidbase:'img', cap:'', aspect:'wide' },
    { type:'img', src:'06 — יציאה לגג/Edited-8.jpg', cap:'', aspect:'tall' },
    { type:'vid', src:'06 — יציאה לגג/23.mp4', vidbase:'img', cap:'' },
    { type:'img', src:'06 — יציאה לגג/חדר שמש, הרצליה פיתוח.JPG', cap:'חדר שמש — הרצליה', aspect:'tall' },
    { type:'vid', src:'06 — יציאה לגג/3c.mp4', vidbase:'img', cap:'' },
    { type:'vid', src:'06 — יציאה לגג/33.mp4', vidbase:'img', cap:'' },
"""

if old_body.strip() == NEW_PENTHOUSE.strip():
    print("✔  MEDIA.penthouse already curated")
else:
    src = src[:body_start] + NEW_PENTHOUSE + src[body_end:]
    changes += 1
    print(f"✔  MEDIA.penthouse curated: {old_count} → 6 off-project tiles (4 vid + 2 still)")

# ═══════════════════════════════════════════════════════════════
# 8) MEDIA.retractable — curate to 6 off-project tiles
# ═══════════════════════════════════════════════════════════════
retract_pos = src.find('  retractable: [\n', media_start)
if retract_pos == -1:
    print("❌ MEDIA.retractable anchor not found")
    sys.exit(1)
body_start = retract_pos + len('  retractable: [\n')
close_offset = src.find('\n  ],', body_start)
body_end = close_offset + 1

old_body = src[body_start:body_end]
old_count = old_body.count("type:")

NEW_RETRACT = """    { type:'img', src:'01 — סקיילייט נוסע/חד שיפועי/DOR_6758-HDR.jpg', cap:'', aspect:'wide' },
    { type:'vid', src:'01 — סקיילייט נוסע/1.mp4', vidbase:'img', cap:'' },
    { type:'img', src:'01 — סקיילייט נוסע/דו שיפועי/Edited-21.jpg', cap:'', aspect:'tall' },
    { type:'vid', src:'01 — סקיילייט נוסע/11a.mp4', vidbase:'img', cap:'' },
    { type:'img', src:'01 — סקיילייט נוסע/63.jpg', cap:'קירוי בריכה', aspect:'tall' },
    { type:'vid', src:'01 — סקיילייט נוסע/24.mp4', vidbase:'img', cap:'' },
"""

if old_body.strip() == NEW_RETRACT.strip():
    print("✔  MEDIA.retractable already curated")
else:
    src = src[:body_start] + NEW_RETRACT + src[body_end:]
    changes += 1
    print(f"✔  MEDIA.retractable curated: {old_count} → 6 tiles (3 vid + 3 still)")

# ═══════════════════════════════════════════════════════════════
# 9) MEDIA.smoke — curate to 6 off-project tiles with aspects
# ═══════════════════════════════════════════════════════════════
smoke_pos = src.find('  smoke: [\n', media_start)
if smoke_pos == -1:
    print("❌ MEDIA.smoke anchor not found")
    sys.exit(1)
body_start = smoke_pos + len('  smoke: [\n')
close_offset = src.find('\n  ],', body_start)
body_end = close_offset + 1

old_body = src[body_start:body_end]
old_count = old_body.count("type:")

NEW_SMOKE = """    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/בית פרטי חד שיפועי שחרור עשן.jpg', cap:'', aspect:'wide' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/AlfVjy-ryenVRYXksChGM_1Zu0pUByH44zoXInIzwZqq.jpg', cap:'', aspect:'tall' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/גפני1.jpg', cap:'' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/213.jpg', cap:'', aspect:'tall' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/251.jpg', cap:'' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/130.jpg', cap:'' },
"""

if old_body.strip() == NEW_SMOKE.strip():
    print("✔  MEDIA.smoke already curated")
else:
    src = src[:body_start] + NEW_SMOKE + src[body_end:]
    changes += 1
    print(f"✔  MEDIA.smoke curated: {old_count} → 6 tiles (1 wide + 2 tall + 3 sq)")

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
