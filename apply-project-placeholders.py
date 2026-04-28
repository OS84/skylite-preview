#!/usr/bin/env python3
"""apply-project-placeholders.py — Phase 2: project content placeholders.

Audit before writing
====================
Of the 6 fixed projects, content-completeness varied:
  HP HQ              full description ✓
  Beit Gil HaZahav   full description ✓
  Mitzpe Hayamim     metadata only, no description (only article links)
  Mishya             metadata only, no description block
  Bar-Ilan           NO intro section at all
  Beit Zait          NO intro section at all

This script adds:
  • description placeholder to Mitzpe (above the existing article links)
  • year row to Mitzpe (data has 2020, page didn't show it)
  • description placeholder to Mishya
  • full intro section + description placeholder to Bar-Ilan
  • full intro section + description placeholder to Beit Zait

Placeholder format: italic stone-colored text in a clear bracket-tag so it
stands out visually as "fill this in later" — no risk of shipping unnoticed.
The tag `[תיאור הפרויקט — להשלים]` will be searchable in the file.

Idempotent.
"""
import sys, pathlib

HTML = pathlib.Path(__file__).parent / "index.html"
src = HTML.read_text(encoding="utf-8")
changes = 0

PLACEHOLDER = (
    '<p style="color:var(--stone);font-style:italic;border-right:3px solid var(--accent-pale);'
    'padding-right:14px;margin:0">'
    '[תיאור הפרויקט — להשלים: אתגר אדריכלי, פתרון סקיילייט, פרט מבדיל]'
    '</p>'
)

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
# 1) Mitzpe Hayamim — add year row + description placeholder
# ═══════════════════════════════════════════════════════════════
swap(
    """  <dl class="pp-project-intro-meta rv">
    <dt>מיקום</dt><dd>ראש פינה</dd>
    <dt>אדריכל</dt><dd>פייגין</dd>
    <dt>מוצר</dt><dd>סקיילייט קבוע</dd>
  </dl>
  <div class="pp-project-intro-desc rv rv-d1">
    <p style="margin-top:0"><a href="https://www.ynet.co.il/vacation/flights/article/B1pTyqhxI\"""",
    f"""  <dl class="pp-project-intro-meta rv">
    <dt>מיקום</dt><dd>ראש פינה</dd>
    <dt>שנה</dt><dd>2020</dd>
    <dt>אדריכל</dt><dd>פייגין</dd>
    <dt>מוצר</dt><dd>סקיילייט קבוע</dd>
  </dl>
  <div class="pp-project-intro-desc rv rv-d1">
    {PLACEHOLDER}
    <p style="margin-top:14px"><a href="https://www.ynet.co.il/vacation/flights/article/B1pTyqhxI\"""",
    "Mitzpe Hayamim: + year 2020, + description placeholder",
)

# ═══════════════════════════════════════════════════════════════
# 2) Mishya — add description placeholder (intro has metadata but no desc)
# ═══════════════════════════════════════════════════════════════
swap(
    """<section class="pp-project-intro" style="grid-template-columns:auto;max-width:520px">
  <dl class="pp-project-intro-meta rv">
    <dt>מיקום</dt><dd>תל אביב</dd>
    <dt>אדריכל</dt><dd>ברנוביץ'-קרוננברג</dd>
    <dt>מוצר</dt><dd>סקיילייט קבוע, חד שיפועי</dd>
  </dl>
</section>""",
    f"""<section class="pp-project-intro">
  <dl class="pp-project-intro-meta rv">
    <dt>מיקום</dt><dd>תל אביב</dd>
    <dt>אדריכל</dt><dd>ברנוביץ'-קרוננברג</dd>
    <dt>מוצר</dt><dd>סקיילייט קבוע, חד שיפועי</dd>
  </dl>
  <div class="pp-project-intro-desc rv rv-d1">
    {PLACEHOLDER}
  </div>
</section>""",
    "Mishya: + description placeholder (and removed override style — uses default 2-col)",
)

# ═══════════════════════════════════════════════════════════════
# 3) Bar-Ilan — add full intro section after hero
# ═══════════════════════════════════════════════════════════════
swap(
    """<section class="pp-hero"><img src="./מוצרים מסווגים/02 — סקיילייט קבוע/דו שיפועי/6ב - מנהלה בר אילן.jpg" alt="מנהלה — אוניברסיטת בר אילן"><div class="pp-hero-ov"></div><div class="pp-hero-c"><div class="pp-hero-cat">Project · Fixed Skylight</div><h1 class="pp-hero-name">מנהלה — אוניברסיטת בר אילן</h1><div class="pp-hero-tag">רמת גן · דו שיפועי</div></div></section>
<section class="pp-project-gallery" id="project-gal-bar-ilan"></section>""",
    f"""<section class="pp-hero"><img src="./מוצרים מסווגים/02 — סקיילייט קבוע/דו שיפועי/6ב - מנהלה בר אילן.jpg" alt="מנהלה — אוניברסיטת בר אילן"><div class="pp-hero-ov"></div><div class="pp-hero-c"><div class="pp-hero-cat">Project · Fixed Skylight</div><h1 class="pp-hero-name">מנהלה — אוניברסיטת בר אילן</h1><div class="pp-hero-tag">רמת גן · דו שיפועי</div></div></section>
<section class="pp-project-intro">
  <dl class="pp-project-intro-meta rv">
    <dt>מיקום</dt><dd>רמת גן</dd>
    <dt>מוצר</dt><dd>סקיילייט קבוע, דו שיפועי</dd>
  </dl>
  <div class="pp-project-intro-desc rv rv-d1">
    {PLACEHOLDER}
  </div>
</section>
<section class="pp-project-gallery" id="project-gal-bar-ilan"></section>""",
    "Bar-Ilan: + full intro section + description placeholder",
)

# ═══════════════════════════════════════════════════════════════
# 4) Beit Zait — add full intro section after hero
# ═══════════════════════════════════════════════════════════════
swap(
    """<section class="pp-hero"><img src="./מוצרים מסווגים/02 — סקיילייט קבוע/חצר אנגלית/בית זית/DJI_20260311194246_0277_D.jpg" alt="בית זית"><div class="pp-hero-ov"></div><div class="pp-hero-c"><div class="pp-hero-cat">Project · Fixed Skylight</div><h1 class="pp-hero-name">בית זית</h1><div class="pp-hero-tag">בית זית · חצר אנגלית</div></div></section>
<section class="pp-project-gallery" id="project-gal-beit-zait"></section>""",
    f"""<section class="pp-hero"><img src="./מוצרים מסווגים/02 — סקיילייט קבוע/חצר אנגלית/בית זית/DJI_20260311194246_0277_D.jpg" alt="בית זית"><div class="pp-hero-ov"></div><div class="pp-hero-c"><div class="pp-hero-cat">Project · Fixed Skylight</div><h1 class="pp-hero-name">בית זית</h1><div class="pp-hero-tag">בית זית · חצר אנגלית</div></div></section>
<section class="pp-project-intro">
  <dl class="pp-project-intro-meta rv">
    <dt>מיקום</dt><dd>בית זית</dd>
    <dt>מוצר</dt><dd>סקיילייט קבוע, חצר אנגלית</dd>
  </dl>
  <div class="pp-project-intro-desc rv rv-d1">
    {PLACEHOLDER}
  </div>
</section>
<section class="pp-project-gallery" id="project-gal-beit-zait"></section>""",
    "Beit Zait: + full intro section + description placeholder",
)

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
