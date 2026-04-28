#!/usr/bin/env python3
"""apply-swap-sections.py — Move projects above gallery on fixed + structural.

Information-architecture change. After our curation, the MEDIA strip is
"product variations / off-project shots" — supporting texture. The PROJECTS
section is the credibility payoff (named clients, architects, locations).
Trust beats atmosphere; named projects belong above the gallery.

This is also a mobile win: every section is one screen on mobile, so the
section that needs to land first must come first in DOM order.

What this ships
===============
1. Swap the order of <section pp-media> and <section pp-projects-section>
   on fixed and structural product pages. (penthouse, walkon untouched —
   not in pilot yet.)

2. Differentiate the section eyebrows so they don't read as duplicate
   showcases:
     - Projects:  eyebrow "מבחר עבודות"  → "פרויקטים"   (was bumping with
                                                          "עבודות נבחרות"
                                                          in gallery)
                  h2      "פרויקטים"     → "היכן בנינו"  (clearer story)
     - Gallery:   eyebrow "גלריה"        unchanged
                  h2      "עבודות נבחרות" → "המוצר במגוון" (pilot categories
                                                            only, via
                                                            MEDIA_HEADERS map)

3. Add MEDIA_HEADERS map so non-pilot categories (penthouse, walkon, smoke,
   retractable) keep their original gallery h2.

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
# 1) HTML — swap section order on fixed page
# ═══════════════════════════════════════════════════════════════
swap(
    '<section class="pp-media" id="media-fixed"></section>\n<section class="pp-projects-section" id="projects-sec-fixed"></section>',
    '<section class="pp-projects-section" id="projects-sec-fixed"></section>\n<section class="pp-media" id="media-fixed"></section>',
    "fixed: swap projects ↔ gallery section order",
)

# ═══════════════════════════════════════════════════════════════
# 2) HTML — swap section order on structural page
# ═══════════════════════════════════════════════════════════════
swap(
    '<section class="pp-media" id="media-structural"></section>\n<section class="pp-projects-section" id="projects-sec-structural"></section>',
    '<section class="pp-projects-section" id="projects-sec-structural"></section>\n<section class="pp-media" id="media-structural"></section>',
    "structural: swap projects ↔ gallery section order",
)

# ═══════════════════════════════════════════════════════════════
# 3) JS — update renderProjectsSection eyebrow + h2 (applies globally,
#    but only categories with PROJECTS data render this section so it's
#    safe — non-pilot categories with cards see the same friendlier copy)
# ═══════════════════════════════════════════════════════════════
swap(
    '<div class="pp-projects-section-h"><div class="pp-projects-section-eye">מבחר עבודות</div><h2 class="pp-projects-section-t">פרויקטים</h2></div>',
    '<div class="pp-projects-section-h"><div class="pp-projects-section-eye">פרויקטים</div><h2 class="pp-projects-section-t">היכן בנינו</h2></div>',
    "renderProjectsSection: eyebrow → 'פרויקטים', h2 → 'היכן בנינו'",
)

# ═══════════════════════════════════════════════════════════════
# 4) JS — add MEDIA_HEADERS map and use it in renderMedia
# ═══════════════════════════════════════════════════════════════

# Insert MEDIA_HEADERS just before MEDIA_LAYOUT
swap(
    "// Pilot: per-pid mosaic layout map. 'mosaic' enables varied aspect ratios\n// driven by `aspect:'wide'|'tall'` on each MEDIA item (default = square).\nconst MEDIA_LAYOUT = { fixed: 'mosaic', structural: 'mosaic' };",
    """// Pilot: per-pid mosaic layout map. 'mosaic' enables varied aspect ratios
// driven by `aspect:'wide'|'tall'` on each MEDIA item (default = square).
const MEDIA_LAYOUT = { fixed: 'mosaic', structural: 'mosaic' };

// Per-pid header copy override for the gallery section. When a category has
// projects above (pilot categories), the gallery is a "product variations"
// strip — its h2 should reflect that. Other categories keep "עבודות נבחרות".
const MEDIA_HEADERS = {
  fixed:      { eye: 'גלריה', title: 'המוצר במגוון' },
  structural: { eye: 'גלריה', title: 'המוצר במגוון' },
};""",
    "Add MEDIA_HEADERS map (pilot-scoped overrides)",
)

# Update renderMedia to use MEDIA_HEADERS
swap(
    'const out = [`<div class="pp-media-h"><div class="pp-projects-section-eye">גלריה</div><h2 class="pp-projects-section-t">עבודות נבחרות</h2></div>`, `<div class="${gridClass}">`];',
    '''const hdr = MEDIA_HEADERS[pid] || { eye: 'גלריה', title: 'עבודות נבחרות' };
  const out = [`<div class="pp-media-h"><div class="pp-projects-section-eye">${hdr.eye}</div><h2 class="pp-projects-section-t">${hdr.title}</h2></div>`, `<div class="${gridClass}">`];''',
    "renderMedia: read header from MEDIA_HEADERS map",
)

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
