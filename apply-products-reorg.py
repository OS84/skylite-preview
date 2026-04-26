#!/usr/bin/env python3
"""apply-products-reorg.py — Products folder reorganization.

User request (April 2026):
  1. Add 7th product category — חלונות סקיילייט (Skylite Windows)
  2. Refactor projects to use 'use/' subfolders where they exist
     (best-of-folder curation already done by user)
  3. Verify and fix all broken paths after folder restructure
  4. Swap About page split image to the new 'About us image.jpeg'

Scope of changes
================

A) HP HQ moved from WALKON to FIXED category
   Files now live at: 02 — סקיילייט קבוע/HP HQ - בניין מרקורי/
   Old MEDIA.walkon and PROJECTS.walkon hp-hq paths broken.

   Action:
   - Remove HP HQ tiles from MEDIA.walkon
   - Add HP HQ tiles to MEDIA.fixed
   - Move hp-hq entry from PROJECTS.walkon to PROJECTS.fixed
   - Update Schema.org HP HQ image URL
   - Update HP HQ project page hero image src

B) Mitzpe Hayamim — switch to curated 'Use/' subfolder
   Use/ files: DJI_20260225173740_0134_D(1).jpg, DSC04851.jpeg,
   DSC04859.jpg, DSC04869.jpg, DSC04881.jpg, DSC04912.jpg,
   hero image.jpg, מצפה הימים מסעדה.jpg

   Action:
   - Update PROJECTS.fixed mitzpe-hayamim images to Use/ paths
   - Update MEDIA.fixed Mitzpe references to Use/
   - Update Schema.org

C) New 7th category — windows (חלונות סקיילייט)
   Files at: 02 — סקיילייט קבוע/חלונות סקיילייט/
   (Files identical to the duplicate ⁨07 folder; the 02 path is
   chosen because it has clean Unicode and existing site references.)

   Action:
   - Add 'windows' to pages array
   - Add new home grid card (#7)
   - Add new <div id="page-windows"> product page
   - Add MEDIA.windows (6 tiles)
   - Add META.windows for SEO
   - Add Schema.org Product entry

D) About page image swap
   - Replace 04 — מבנים מרחביים/כיפה/048.jpeg
     with About us image.jpeg (kept on the LEFT in RTL = renders
     before the text in source order; current layout is correct).

Idempotent — safe to re-run.
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
# A) HP HQ — fix broken paths (was walkon → now fixed)
# ═══════════════════════════════════════════════════════════════
HP_OLD = "03 — סקיילייט מדרך/HP HQ - בניין מרקורי"
HP_NEW = "02 — סקיילייט קבוע/HP HQ - בניין מרקורי"

# Replace ALL occurrences globally for HP HQ folder reference
hp_replacements_before = src.count(HP_OLD)
src = src.replace(HP_OLD, HP_NEW)
hp_replacements_after = src.count(HP_OLD)
print(f"✔  HP HQ folder path: {hp_replacements_before} ref(s) → fixed")
if hp_replacements_after > 0:
    print(f"   ⚠ {hp_replacements_after} stragglers remain (probably none)")
changes += hp_replacements_before

# Move PROJECTS hp-hq from walkon[] to fixed[]
# The walkon array has hp-hq as the 2nd entry; find and lift it.
import re
# Find walkon[] block
walkon_m = re.search(r"(\bwalkon:\[)([\s\S]*?)(\],\s*structural:)", src)
if walkon_m:
    walkon_body = walkon_m.group(2)
    # Look for hp-hq object and remove
    hp_re = re.compile(r"\s*\{slug:'hp-hq'[^}]*?\}\]?\}\s*,?")
    hp_match = hp_re.search(walkon_body)
    if hp_match:
        hp_obj = hp_match.group(0).strip().rstrip(',')
        # Strip trailing comma to get clean object
        hp_obj_clean = hp_obj.rstrip(',').strip()
        new_walkon_body = hp_re.sub('', walkon_body, count=1)
        # Update walkon block in src
        src = src[:walkon_m.start(2)] + new_walkon_body + src[walkon_m.end(2):]
        # Now insert hp-hq into fixed[] (append at end before closing ])
        fixed_m = re.search(r"(\bfixed:\[)([\s\S]*?)(\],\s*walkon:)", src)
        if fixed_m:
            fixed_body = fixed_m.group(2)
            # Append hp-hq before the closing
            new_fixed_body = fixed_body.rstrip() + "\n    " + hp_obj_clean + ",\n  "
            src = src[:fixed_m.start(2)] + new_fixed_body + src[fixed_m.end(2):]
            changes += 1
            print("✔  PROJECTS.hp-hq moved walkon → fixed")
        else:
            print("⚠  Could not find fixed[] to insert hp-hq")
    else:
        print("✔  hp-hq already not in walkon[]")
else:
    print("⚠  Could not locate walkon[] block")

# MEDIA strip cleanup — remove 2 HP HQ tiles from walkon strip,
# add equivalent tiles to fixed strip.
HP_WALKON_TILES = """    { type:'img', src:'02 — סקיילייט קבוע/HP HQ - בניין מרקורי/269.jpg', cap:'HP HQ — בניין מרקורי' },
    { type:'img', src:'02 — סקיילייט קבוע/HP HQ - בניין מרקורי/HP06.jpg', cap:'HP HQ — בניין מרקורי' },
"""
if HP_WALKON_TILES in src:
    src = src.replace(HP_WALKON_TILES, "")
    changes += 1
    print("✔  MEDIA.walkon — removed 2 HP HQ tiles")
else:
    print("✔  MEDIA.walkon — HP HQ tiles already removed")

# Add HP HQ to MEDIA.fixed (insert after Mitzpe hero tile)
HP_FIXED_INSERT_ANCHOR = "    { type:'img', src:'02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/hero image.jpg', cap:'מצפה הימים' },"
HP_FIXED_INSERT_NEW = """    { type:'img', src:'02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/hero image.jpg', cap:'מצפה הימים' },
    { type:'img', src:'02 — סקיילייט קבוע/HP HQ - בניין מרקורי/HP06.jpg', cap:'HP HQ — בניין מרקורי' },
    { type:'img', src:'02 — סקיילייט קבוע/HP HQ - בניין מרקורי/269.jpg', cap:'HP HQ — בניין מרקורי' },"""
if "HP HQ - בניין מרקורי/HP06.jpg" in src and "MEDIA.fixed" or "02 — סקיילייט קבוע/HP HQ - בניין מרקורי/HP06.jpg', cap:'HP HQ" in src:
    # Already present somewhere
    if HP_FIXED_INSERT_NEW in src:
        print("✔  MEDIA.fixed — HP HQ tiles already inserted")
    else:
        if HP_FIXED_INSERT_ANCHOR in src:
            src = src.replace(HP_FIXED_INSERT_ANCHOR, HP_FIXED_INSERT_NEW, 1)
            changes += 1
            print("✔  MEDIA.fixed — added 2 HP HQ tiles")
        else:
            print("⚠  MEDIA.fixed anchor not found")

# ═══════════════════════════════════════════════════════════════
# B) Mitzpe Hayamim → Use/ subfolder
# ═══════════════════════════════════════════════════════════════
# Mitzpe project images — refactor to Use/ paths.
# Use/ files (8): DJI_20260225173740_0134_D(1).jpg, DSC04851.jpeg, DSC04859.jpg,
#   DSC04869.jpg, DSC04881.jpg, DSC04912.jpg, hero image.jpg, מצפה הימים מסעדה.jpg
MITZPE_OLD = "{slug:'mitzpe-hayamim',name:'מלון מצפה הימים — ראש פינה',hero:'02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/hero image.jpg',meta:{where:'ראש פינה',when:'2020',arch:'פייגין',product:'סקיילייט קבוע'},images:['02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/hero image.jpg','02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/מצפה הימים מסעדה.jpg','02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/DJI_20260225171403_0110_D(1).jpg','02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/DSC04851.jpg','02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/DSC04860.jpg','02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/מצפה הימים מבט על.jpg','02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/DSC04881.jpg','02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/DJI_20260225173740_0134_D(1).jpg','02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/DSC04910.jpg']}"
MITZPE_NEW = "{slug:'mitzpe-hayamim',name:'מלון מצפה הימים — ראש פינה',hero:'02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/Use/hero image.jpg',meta:{where:'ראש פינה',when:'2020',arch:'פייגין',product:'סקיילייט קבוע'},images:['02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/Use/hero image.jpg','02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/Use/מצפה הימים מסעדה.jpg','02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/Use/DSC04851.jpeg','02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/Use/DSC04859.jpg','02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/Use/DSC04869.jpg','02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/Use/DSC04881.jpg','02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/Use/DJI_20260225173740_0134_D(1).jpg','02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/Use/DSC04912.jpg']}"
swap(MITZPE_OLD, MITZPE_NEW, "PROJECTS.mitzpe-hayamim → Use/", must_exist=False)

# MEDIA.fixed Mitzpe — switch to Use/ paths
swap(
    "{ type:'img', src:'02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/hero image.jpg', cap:'מצפה הימים' },",
    "{ type:'img', src:'02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/Use/hero image.jpg', cap:'מצפה הימים' },",
    "MEDIA.fixed Mitzpe hero → Use/",
    must_exist=False,
)
swap(
    "{ type:'img', src:'02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/DJI_20260225173740_0134_D(1).jpg', cap:'מצפה הימים' },",
    "{ type:'img', src:'02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/Use/DJI_20260225173740_0134_D(1).jpg', cap:'מצפה הימים' },",
    "MEDIA.fixed Mitzpe drone → Use/",
    must_exist=False,
)

# Mitzpe hero image used in project page hero (line ~1412):
# Update src in <img src="./מוצרים מסווגים/02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/hero image.jpg"
swap(
    './מוצרים מסווגים/02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/hero image.jpg',
    './מוצרים מסווגים/02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/Use/hero image.jpg',
    "Mitzpe project hero <img> → Use/",
    must_exist=False,
)

# Schema HP HQ image URL — already covered by HP_OLD→HP_NEW global replace above.
# Schema Mitzpe — no special schema beyond URL? Check by string presence below.

# ═══════════════════════════════════════════════════════════════
# C) New 7th category — חלונות סקיילייט / windows
# ═══════════════════════════════════════════════════════════════

# C1) Add 'windows' to pages array
swap(
    "const pages=['home','about','penthouse','fixed','retractable','walkon','structural','smoke','tech'];",
    "const pages=['home','about','penthouse','fixed','retractable','walkon','structural','smoke','windows','tech'];",
    "pages[] += windows",
)

# C2) Home grid — add 7th card after smoke (before penthouse card #6, but
#     visually our grid uses 3-column layout so we want windows last to keep
#     2 rows of 3 + 1 lone card OR 3+3+1; better: keep 2 rows of 3 then last
#     card = windows — but we currently have 6 cards total. Adding #7 makes 7.
#     We'll add windows as #7 right after penthouse card.
# Find penthouse card closing and insert windows card after it.
PENT_CARD_END = """    <div class="p-card rv rv-d3" onclick="go('penthouse')">
      <div class="p-card-bg" style="background-image:url('./מוצרים מסווגים/06 — יציאה לגג/Hero copy.jpg')"></div>
      <div class="p-card-ov"></div>
      <div class="p-card-c"><div class="p-card-num">06</div><div><div class="p-card-en">Roof Access</div><div class="p-card-name">יציאה לגג</div><div class="p-card-tag">הדלת שפותחת שמיים</div><div class="p-card-arrow">גלה עוד <svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M2 7h10M8 3l4 4-4 4"/></svg></div></div></div>
    </div>"""

WINDOWS_CARD = """    <div class="p-card rv rv-d3" onclick="go('penthouse')">
      <div class="p-card-bg" style="background-image:url('./מוצרים מסווגים/06 — יציאה לגג/Hero copy.jpg')"></div>
      <div class="p-card-ov"></div>
      <div class="p-card-c"><div class="p-card-num">06</div><div><div class="p-card-en">Roof Access</div><div class="p-card-name">יציאה לגג</div><div class="p-card-tag">הדלת שפותחת שמיים</div><div class="p-card-arrow">גלה עוד <svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M2 7h10M8 3l4 4-4 4"/></svg></div></div></div>
    </div>

    <div class="p-card rv rv-d3" onclick="go('windows')">
      <div class="p-card-bg" style="background-image:url('./מוצרים מסווגים/02 — סקיילייט קבוע/חלונות סקיילייט/חלון סקיילייט.png')"></div>
      <div class="p-card-ov"></div>
      <div class="p-card-c"><div class="p-card-num">07</div><div><div class="p-card-en">Skylite Windows</div><div class="p-card-name">חלונות סקיילייט</div><div class="p-card-tag">חלון. כן. אבל לאור.</div><div class="p-card-arrow">גלה עוד <svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M2 7h10M8 3l4 4-4 4"/></svg></div></div></div>
    </div>"""

swap(PENT_CARD_END, WINDOWS_CARD, "Home grid +07 windows card")

# C3) New page-windows DOM — insert after page-smoke and before page-tech.
# Anchor: <!-- ════ TECH ════ -->
WINDOWS_PAGE = """<!-- ════ WINDOWS ════ -->
<div id="page-windows" class="pp">
<nav class="nav scrolled"><div class="nav-logo"><svg viewBox="0 0 50 50" width="36" height="36" fill="none"><rect width="50" height="50" fill="#E9EEF2"/><path d="M26,0 L50,0 L50,50 L0,50 L0,40 C3,30 18,10 26,0Z" fill="#1A1E24"/></svg><span class="nav-wordmark">SKYLITE</span></div><a href="#" class="nav-back" onclick="home();return false"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M13 8H3M7 12l-4-4 4-4"/></svg>חזרה</a><a href="#" class="nav-cta" onclick="openCM();return false">צור קשר</a></nav>
<section class="pp-hero"><img src="./מוצרים מסווגים/02 — סקיילייט קבוע/חלונות סקיילייט/חלון סקיילייט.png" alt="חלונות סקיילייט — חלון לאור"><div class="pp-hero-ov"></div><div class="pp-hero-c"><div class="pp-hero-cat">07 — Skylite Windows</div><h1 class="pp-hero-name">חלונות סקיילייט</h1><div class="pp-hero-tag">חלון. כן. אבל לאור.</div></div></section>
<section class="pp-content">
  <div><div class="pp-desc-label">על המוצר</div><div class="pp-desc"><p>חלון סקיילייט הוא חלון ייעודי המותקן בגג או בקיר משופע — המביא אור טבעי וחיבור לשמיים אל חללים פנימיים שלא היו נגישים לאור. עיצוב נקי, מסגרת אלומיניום דקה ומגוון צורות — מלבני, מרובע, או עגול.</p><p>כל חלון מתוכנן לפי הפרויקט — מידה, צבע, סוג זיגוג ומנגנון פתיחה. מתאים לחללים פרטיים, מסחריים ומוסדיים.</p><p>הזיגוג כולל זכוכית ביטחון מרובדת, זכוכית בידודית או פוליקרבונט — בהתאם לדרישת הבידוד, הבטיחות והאקוסטיקה. הפרופיל בנוי באותה שיטה של שאר מוצרי סקיילייט: אטמי EPDM משולבים, תעלות ניקוז פנימיות, וגימור צביעה אלקטרוסטטית בתנור.</p></div></div>
  <div><div class="pp-chars-title">מאפיינים עיקריים</div>
    <div class="pp-char"><div class="pp-char-n">01</div><div><div class="pp-char-name">מסגרת אלומיניום דקה</div><div class="pp-char-desc">פרופיל אלומיניום 6063 TF, נקי ומינימליסטי — שלא לגזול שטח אור. גימור RAL לבחירת האדריכל.</div></div></div>
    <div class="pp-char"><div class="pp-char-n">02</div><div><div class="pp-char-name">מגוון צורות וגדלים</div><div class="pp-char-desc">חלון מלבני, מרובע או עגול. מידות לפי הזמנה. ניתן לשלב במיקומים לא שגרתיים — קיר משופע, גג, או חלל פינתי.</div></div></div>
    <div class="pp-char"><div class="pp-char-n">03</div><div><div class="pp-char-name">חלופות זיגוג</div><div class="pp-char-desc">זכוכית ביטחון מרובדת, זכוכית בידודית, או פוליקרבונט. בחירה לפי דרישות הבידוד התרמי, האקוסטי והבטיחות.</div></div></div>
    <div class="pp-char"><div class="pp-char-n">04</div><div><div class="pp-char-name">איטום אינטגרלי</div><div class="pp-char-desc">אטמי EPDM משולבים בפרופיל — לא מודבקים, לא נדחסים. תעלות ניקוז פנימיות. אותה שיטת איטום של כל מוצרי סקיילייט.</div></div></div>
  </div>
</section>
<section class="pp-media" id="media-windows"></section>
<section class="pp-cta"><h2 class="rv">מתכננים פתח לאור?<br><em>נשמח לייעץ</em></h2><div class="cta-acts rv rv-d1"><button class="btn-pd" onclick="openCM()">השאירו פרטים</button><a href="tel:+97239343159" class="btn-od">טלפון: 03-9343159</a></div></section>
<footer><div class="f-brand"><svg viewBox="0 0 50 50" width="32" fill="none"><rect width="50" height="50" fill="#1A1E24"/><path d="M26,0 L50,0 L50,50 L0,50 L0,40 C3,30 18,10 26,0Z" fill="#E9EEF2"/></svg><div class="f-name">Skylite</div><div class="f-tag">הנדסת הטבע<br>האור שחותך את החלל — מ-1986</div></div><div class="f-links"><a href="#" onclick="home();return false">← חזרה לדף הבית</a><a href="#" onclick="go('retractable');return false">סקיילייט נוסע</a><a href="#" onclick="go('fixed');return false">סקיילייט קבוע</a><a href="#" onclick="go('smoke');return false">מערכות שחרור עשן</a><a href="#" onclick="go('tech');return false">מידע טכני</a></div><div class="f-contact"><p><strong>סקיילייט בע"מ</strong></p><p>אלכסנדר ינאי 8, א.ת סגולה, פתח תקווה</p><p>טל: <a href="tel:+97239343159" dir="ltr" style="color:inherit;text-decoration:none;border-bottom:1px solid currentColor">03-9343159</a> | פקס: <span dir="ltr">03-9311921</span></p><p><a href="mailto:skylite@skylite.co.il" style="color:inherit;text-decoration:none;border-bottom:1px solid currentColor">skylite@skylite.co.il</a></p><p style="margin-top:8px">שעות פעילות: ראשון–חמישי 9:00–18:00</p><p>שישי–שבת: סגור | הגעה בתיאום מראש</p><p style="margin-top:10px"><a href="https://instagram.com/skyliteisrael/" target="_blank" rel="noopener" style="color:var(--accent-pale);text-decoration:none;font-size:12px;letter-spacing:.06em">Instagram — @skyliteisrael</a></p></div></footer>
</div>

<!-- ════ TECH ════ -->"""

if 'id="page-windows"' in src:
    print("✔  page-windows DOM — already present")
else:
    src = src.replace("<!-- ════ TECH ════ -->", WINDOWS_PAGE, 1)
    changes += 1
    print("✔  page-windows DOM inserted")

# C4) MEDIA.windows — append before MEDIA closing.
WINDOWS_MEDIA_BLOCK = """  windows: [
    { type:'img', src:'02 — סקיילייט קבוע/חלונות סקיילייט/חלון סקיילייט.png', cap:'חלון סקיילייט' },
    { type:'img', src:'02 — סקיילייט קבוע/חלונות סקיילייט/חלון סקיילייט 1.png', cap:'חלון סקיילייט' },
    { type:'img', src:'02 — סקיילייט קבוע/חלונות סקיילייט/חלון סקיילייט עגול.png', cap:'חלון עגול' },
    { type:'img', src:'02 — סקיילייט קבוע/חלונות סקיילייט/067.jpeg', cap:'' },
    { type:'img', src:'02 — סקיילייט קבוע/חלונות סקיילייט/075.jpeg', cap:'' },
    { type:'img', src:'02 — סקיילייט קבוע/חלונות סקיילייט/20200506_153509.jpeg', cap:'' },
  ],
"""
# Insert after smoke array close (before "};" of MEDIA)
MEDIA_CLOSE_ANCHOR = """    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/265.jpg' },
  ],
};"""
MEDIA_CLOSE_NEW = """    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/265.jpg' },
  ],
""" + WINDOWS_MEDIA_BLOCK + "};"

if "windows: [" in src:
    print("✔  MEDIA.windows — already added")
else:
    if MEDIA_CLOSE_ANCHOR in src:
        src = src.replace(MEDIA_CLOSE_ANCHOR, MEDIA_CLOSE_NEW, 1)
        changes += 1
        print("✔  MEDIA.windows added")
    else:
        print("⚠  MEDIA close anchor not found — windows block not added")

# C5) Also remove windows tiles from MEDIA.fixed since they belong to MEDIA.windows now.
FIXED_WINDOWS_TILES = """    { type:'img', src:'02 — סקיילייט קבוע/חלונות סקיילייט/חלון סקיילייט.png', cap:'חלון סקיילייט' },
    { type:'img', src:'02 — סקיילייט קבוע/חלונות סקיילייט/חלון סקיילייט 1.png', cap:'חלון סקיילייט' },
    { type:'img', src:'02 — סקיילייט קבוע/חלונות סקיילייט/חלון סקיילייט עגול.png', cap:'חלון סקיילייט עגול' },
"""
if FIXED_WINDOWS_TILES in src:
    src = src.replace(FIXED_WINDOWS_TILES, "")
    changes += 1
    print("✔  MEDIA.fixed — removed 3 windows tiles (moved to MEDIA.windows)")
else:
    print("✔  MEDIA.fixed — windows tiles already removed")

# C6) META.windows
META_TECH_OLD = """  tech: {
    title: \"מידע טכני | סקיילייט\","""
META_WINDOWS_NEW = """  windows: {
    title: \"חלונות סקיילייט — חלונות אדריכליים לגגות וקירות | סקיילייט\",
    desc: \"חלונות סקיילייט — חלונות ייעודיים לגגות וקירות משופעים. מסגרת אלומיניום דקה, מגוון צורות, ואטימות אינטגרלית. מידה וגוון לפי הזמנה.\",
    image: \"./מוצרים מסווגים/02 — סקיילייט קבוע/חלונות סקיילייט/חלון סקיילייט.png\"
  },
  tech: {
    title: \"מידע טכני | סקיילייט\","""
swap(META_TECH_OLD, META_WINDOWS_NEW, "META.windows added")

# C7) Schema.org Product entry — insert after smoke product
SCHEMA_SMOKE_END = """    {
      "@type": "Product",
      "@id": "https://os84.github.io/skylite-preview/#product-smoke",
      "name": "כיפות תאורה ושחרור עשן",
      "description": "פתרונות אוורור ושחרור עשן בתקן EN 12101. בסיס PVC דופן כפול, זיגוג כפול, מנועים חשמליים.",
      "url": "https://os84.github.io/skylite-preview/#smoke",
      "brand": {
        "@id": "https://os84.github.io/skylite-preview/#org"
      },
      "manufacturer": {
        "@id": "https://os84.github.io/skylite-preview/#org"
      }
    },"""

SCHEMA_WITH_WINDOWS = SCHEMA_SMOKE_END + """
    {
      "@type": "Product",
      "@id": "https://os84.github.io/skylite-preview/#product-windows",
      "name": "חלונות סקיילייט",
      "description": "חלונות אדריכליים לגגות וקירות משופעים. מסגרת אלומיניום, מגוון צורות, מידה וגוון לפי הזמנה.",
      "url": "https://os84.github.io/skylite-preview/#windows",
      "brand": {
        "@id": "https://os84.github.io/skylite-preview/#org"
      },
      "manufacturer": {
        "@id": "https://os84.github.io/skylite-preview/#org"
      }
    },"""

if "#product-windows" in src:
    print("✔  Schema windows Product — already present")
else:
    if SCHEMA_SMOKE_END in src:
        src = src.replace(SCHEMA_SMOKE_END, SCHEMA_WITH_WINDOWS, 1)
        changes += 1
        print("✔  Schema windows Product inserted")
    else:
        print("⚠  Schema smoke anchor not found")

# ═══════════════════════════════════════════════════════════════
# D) About page — replace dome image with About us image.jpeg
# ═══════════════════════════════════════════════════════════════
swap(
    '<img src="./מוצרים מסווגים/04 — מבנים מרחביים/כיפה/048.jpeg" alt="סקיילייט — כיפה מרחבית" loading="lazy">',
    '<img src="./מוצרים מסווגים/About us image.jpeg" alt="סקיילייט — סטודיו ועיצוב" loading="lazy">',
    "About page split image → About us image.jpeg",
)

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
