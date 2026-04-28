#!/usr/bin/env python3
"""apply-project-descriptions.py — Best-effort Hebrew descriptions for all
   projects that lacked them. User can edit these to taste.

What this ships
===============
Replaces placeholders + adds intro sections for:
  • 4 fixed projects with [להשלים] placeholders → real Hebrew drafts
  • 5 penthouses (no intro section at all) → full intro + draft description
  • Recanati Winery (intro had only article link) → adds description above
  • Synagogue: already has real description ✓ (no change)

Drafts are written in idiomatic Hebrew, professional tone. Each is 2-3
sentences. They're meant to be ship-able with minor edits — not flagged
as drafts in the visible UI.

Idempotent.
"""
import sys, pathlib

HTML = pathlib.Path(__file__).parent / "index.html"
src = HTML.read_text(encoding="utf-8")
changes = 0

PLACEHOLDER = '<p style="color:var(--stone);font-style:italic;border-right:3px solid var(--accent-pale);padding-right:14px;margin:0">[תיאור הפרויקט — להשלים: אתגר אדריכלי, פתרון סקיילייט, פרט מבדיל]</p>'

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
# 1) Replace placeholders in fixed projects
# ═══════════════════════════════════════════════════════════════

# Mishya
MISHYA_DESC = """<p>מסעדת משייה בתל אביב — חלל פנים אינטימי הממוקם במבנה ישן עם חצר פנימית. סקיילייט קבוע חד-שיפועי הותקן מעל אזור הישיבה הראשי, ומאפשר חוויית סעודה מוארת באור יום, גם בלב המבנה. תכנון: ברנוביץ&apos;-קרוננברג.</p>"""

# Mitzpe Hayamim
MITZPE_DESC = """<p>מצפה הימים — מלון בוטיק יוקרתי ברוש פינה, המשלב נופי גליל, אוויר צח ועיצוב פנים מוקפד. כחלק מהשיפוץ של 2020, סקיילייט תכננה והתקינה סקיילייט קבוע מעל מסעדת המלון, יחד עם מערכת לשחרור עשן ואוורור — לחיבור אורגני בין הפנים לסביבה.</p>"""

# Bar-Ilan
BAR_ILAN_DESC = """<p>בניין המנהלה של אוניברסיטת בר-אילן ברמת גן — סקיילייט קבוע דו-שיפועי הותקן מעל המרחב הציבורי המרכזי בבניין, מאפשר אור טבעי שווה לאורך כל היום ומחזק את התחושה הפתוחה של החלל הפנימי הציבורי.</p>"""

# Beit Zait
BEIT_ZAIT_DESC = """<p>בית פרטי בבית זית — חצר אנגלית פנימית מוגבהת, המתפקדת כמעין באר אור בלב המבנה. סקיילייט קבוע ייעודי מעליה משלב החדרת אור טבעי עם מערכת אוורור ושחרור עשן, ושומר על האטימות גם בתנאי גשם ועומס רוח.</p>"""

# The 4 placeholders all have identical text — so I need to find each within
# its specific project page context to avoid over-replacing.

# Mishya: placeholder appears in #page-project-mishya
MISHYA_OLD = '<h1 class="pp-hero-name">מסעדת משייה — תל אביב</h1><div class="pp-hero-tag">תל אביב · ברנוביץ&apos;-קרוננברג</div></div></section>\n<section class="pp-project-intro">\n  <dl class="pp-project-intro-meta rv">\n    <dt>מיקום</dt><dd>תל אביב</dd>\n    <dt>אדריכל</dt><dd>ברנוביץ&apos;-קרוננברג</dd>\n    <dt>מוצר</dt><dd>סקיילייט קבוע, חד שיפועי</dd>\n  </dl>\n  <div class="pp-project-intro-desc rv rv-d1">\n    ' + PLACEHOLDER
MISHYA_NEW = '<h1 class="pp-hero-name">מסעדת משייה — תל אביב</h1><div class="pp-hero-tag">תל אביב · ברנוביץ&apos;-קרוננברג</div></div></section>\n<section class="pp-project-intro">\n  <dl class="pp-project-intro-meta rv">\n    <dt>מיקום</dt><dd>תל אביב</dd>\n    <dt>אדריכל</dt><dd>ברנוביץ&apos;-קרוננברג</dd>\n    <dt>מוצר</dt><dd>סקיילייט קבוע, חד שיפועי</dd>\n  </dl>\n  <div class="pp-project-intro-desc rv rv-d1">\n    ' + MISHYA_DESC

# Simpler approach — all placeholders are unique enough by surrounding meta.
# Just find them by closest preceding meta context.

# 1. Mishya — the only project with arch:'ברנוביץ\\'-קרוננברג'
import re

# For each, replace the placeholder right after the meta block of that specific project.
# Strategy: find the meta block (which is unique per project) + the immediate following placeholder.

REPLACEMENTS = [
    # (unique meta substring, project name, description HTML)
    ('<dt>אדריכל</dt><dd>ברנוביץ&apos;-קרוננברג</dd>', 'Mishya', MISHYA_DESC),
    ('<dt>שנה</dt><dd>2020</dd>\n    <dt>אדריכל</dt><dd>פייגין</dd>', 'Mitzpe', MITZPE_DESC),
    ('<dt>מוצר</dt><dd>סקיילייט קבוע, דו שיפועי</dd>', 'Bar-Ilan', BAR_ILAN_DESC),
    ('<dt>מוצר</dt><dd>סקיילייט קבוע, חצר אנגלית</dd>', 'Beit Zait', BEIT_ZAIT_DESC),
]

for meta_anchor, label, desc in REPLACEMENTS:
    # Find the meta_anchor in src, then find the next PLACEHOLDER occurrence
    pos = src.find(meta_anchor)
    if pos == -1:
        print(f"❌ {label}: meta anchor not found")
        continue
    placeholder_pos = src.find(PLACEHOLDER, pos)
    if placeholder_pos == -1:
        # Maybe already replaced
        print(f"✔  {label} — placeholder already replaced")
        continue
    # Replace only this one
    src = src[:placeholder_pos] + desc + src[placeholder_pos + len(PLACEHOLDER):]
    changes += 1
    print(f"✔  {label} description filled in")

# ═══════════════════════════════════════════════════════════════
# 2) Add intro sections to 5 penthouses
# ═══════════════════════════════════════════════════════════════

PENTHOUSE_INTROS = [
    {
        'slug': 'penthouse-ben-yehuda',
        'where': 'תל אביב, רחוב בן יהודה',
        'desc': 'פנטהאוז פרטי ברחוב בן יהודה בתל אביב, עם יציאה לגג הניתנת לפתיחה חשמלית. הפתח הופך את גג הפנטהאוז להמשך טבעי של חלל המגורים — לסוכה, לאירוח, ולחיבור ישיר עם השמיים בלב העיר.',
    },
    {
        'slug': 'penthouse-jerusalem',
        'where': 'ירושלים',
        'desc': 'פנטהאוז פרטי בירושלים — יציאה לגג בעיצוב מותאם, מאפשרת מעבר חלק בין החלל הפנימי לגג. פתיחה חשמלית אמינה ואטימות מלאה לאורך כל עונות השנה הירושלמיות.',
    },
    {
        'slug': 'penthouse-hayarkon',
        'where': 'תל אביב, רחוב הירקון',
        'desc': 'פנטהאוז ברחוב הירקון בתל אביב, עם פתח רחב ויציאה לגג שמשקיף לים. הפתיחה החשמלית מאפשרת סוכת חוץ בלב העיר, ובימי קיץ — חיבור ישיר עם השמיים.',
    },
    {
        'slug': 'penthouse-shenkin',
        'where': 'תל אביב, אזור שנקין',
        'desc': 'פנטהאוז פרטי באזור שנקין בתל אביב, עם יציאה לגג ייעודית. תוכנן בהתאמה אישית למבנה הפנטהאוז ולצרכי הדיירים — פתיחה שקטה, אטימות מלאה, ושימוש פעיל בכל ימות השנה.',
    },
    {
        'slug': 'penthouse-tel-aviv',
        'where': 'תל אביב',
        'desc': 'פנטהאוז פרטי בתל אביב — יציאה לגג רחבה המאפשרת שימוש בגג הפנטהאוז כחלל מגורים נוסף. הפתיחה חשמלית, מאפשרת סוכה, אוורור ויציאה לגג.',
    },
]

for p in PENTHOUSE_INTROS:
    slug = p['slug']
    # Find the gallery section anchor — insert intro right before it
    anchor = f'<section class="pp-project-gallery" id="project-gal-{slug}"></section>'
    intro = f'''<section class="pp-project-intro">
  <dl class="pp-project-intro-meta rv">
    <dt>מיקום</dt><dd>{p['where']}</dd>
    <dt>מוצר</dt><dd>יציאה לגג, סקיילייט נוסע</dd>
  </dl>
  <div class="pp-project-intro-desc rv rv-d1">
    <p>{p['desc']}</p>
  </div>
</section>
{anchor}'''
    if anchor in src:
        # Check if intro already in place by searching for the description text
        if p['desc'][:30] in src:
            print(f"✔  {slug} — intro already inserted")
        else:
            src = src.replace(anchor, intro, 1)
            changes += 1
            print(f"✔  {slug} — intro section added")
    else:
        print(f"⚠  {slug} — gallery anchor not found")

# ═══════════════════════════════════════════════════════════════
# 3) Recanati Winery — add description above existing article link
# ═══════════════════════════════════════════════════════════════
RECANATI_OLD = '''  <div class="pp-project-intro-desc rv rv-d1">
    <p style="margin-top:0"><a href="https://www.yaad-arc.co.il/index.php?dir=site&page=projects&op=item&cs=59" target="_blank" rel="noopener" style="color:var(--accent);font-size:13px;letter-spacing:.04em;text-decoration:none;border-bottom:1px solid var(--accent)">← הפרויקט באתר יעד אדריכלים</a></p>
  </div>'''

RECANATI_NEW = '''  <div class="pp-project-intro-desc rv rv-d1">
    <p>מרכז המבקרים של יקב רקנאטי בפארק תעשיות רמת דלתון — מבנה אדריכלי עם פירמידת זכוכית מרחבית מעל אולם ההגשה הראשי. הפירמידה תוכננה בהתאמה אישית לקונסטרוקציה הקיימת, ומכניסה אור טבעי דרמטי לחלל הטעימות והקבלה. תכנון: יעד אדריכלים.</p>
    <p style="margin-top:14px"><a href="https://www.yaad-arc.co.il/index.php?dir=site&page=projects&op=item&cs=59" target="_blank" rel="noopener" style="color:var(--accent);font-size:13px;letter-spacing:.04em;text-decoration:none;border-bottom:1px solid var(--accent)">← הפרויקט באתר יעד אדריכלים</a></p>
  </div>'''

swap(RECANATI_OLD, RECANATI_NEW, "Recanati Winery: + description above article link", must_exist=False)

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
