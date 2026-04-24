#!/usr/bin/env python3
"""apply-about-page.py — Build dedicated About page at /#about.

Changes:
  1. Re-add .why-us CSS (was parked when we pulled the section off home)
  2. Insert new <div id="page-about" class="pp"> HTML before STRUCTURAL marker
  3. Update home-nav link: <a href="#about"> → onclick go('about')
  4. Add 'about' to pages array

Page structure (short, per user):
  - Hero
  - pp-content: two columns (about + activity)
  - why-us: Right First Time block
  - CTA
  - Footer

No materials/standards section (moved to tech page).
No named-project list (per user — many projects lack images).

Idempotent.
"""
import sys, pathlib

HTML = pathlib.Path(__file__).parent / "index.html"
src = HTML.read_text(encoding="utf-8")
changes = 0

def swap(old, new, label):
    global src, changes
    if new in src:
        print(f"✔  {label} — already applied")
        return
    if old not in src:
        print(f"❌ {label} — anchor not found")
        sys.exit(1)
    src = src.replace(old, new, 1)
    changes += 1
    print(f"✔  {label}")

# ═══════════════════════════════════════════════════════════════
# 1. Re-add .why-us CSS (parked in .agents/parked-copy-blocks.md)
# ═══════════════════════════════════════════════════════════════
WHYUS_CSS = """
    /* ── WHY US: Right First Time block (used on About page) ── */
    .why-us{background:var(--linen);padding:128px 48px 120px;text-align:center;position:relative;border-top:1px solid var(--warm-gray);border-bottom:1px solid var(--warm-gray)}
    .why-us-inner{max-width:820px;margin:0 auto}
    .why-us-title{font-weight:900;font-size:clamp(30px,4vw,52px);line-height:1.18;color:var(--dark);margin-bottom:44px;letter-spacing:-.005em}
    .why-us-title em{font-style:normal;color:var(--accent)}
    .why-us-body p{font-size:17px;font-weight:300;line-height:1.9;color:var(--stone);margin-bottom:22px}
    .why-us-body p:last-child{margin-bottom:0}
    .why-us-body strong{color:var(--dark);font-weight:500}
    @media(max-width:1024px){.why-us{padding:88px 40px 88px}}
    @media(max-width:600px){.why-us{padding:64px 24px 64px}.why-us-title{margin-bottom:32px}.why-us-body p{font-size:16px;line-height:1.85}}
"""

STYLE_CLOSE = "</style>"
SIGNATURE = "/* ── WHY US: Right First Time block"
if SIGNATURE in src:
    print("✔  .why-us CSS already present")
elif STYLE_CLOSE in src:
    src = src.replace(STYLE_CLOSE, WHYUS_CSS + "  " + STYLE_CLOSE, 1)
    changes += 1
    print("✔  Added .why-us CSS")
else:
    print("❌ </style> not found")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════
# 2. Insert new About page HTML before the STRUCTURAL marker
# ═══════════════════════════════════════════════════════════════
ABOUT_NAV = '<nav class="nav scrolled"><div class="nav-logo"><svg viewBox="0 0 50 50" width="36" height="36" fill="none"><rect width="50" height="50" fill="#E9EEF2"/><path d="M26,0 L50,0 L50,50 L0,50 L0,40 C3,30 18,10 26,0Z" fill="#1A1E24"/></svg><span class="nav-wordmark">SKYLITE</span></div><a href="#" class="nav-back" onclick="home();return false"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M13 8H3M7 12l-4-4 4-4"/></svg>חזרה לדף הבית</a><a href="#" class="nav-cta" onclick="openCM();return false">צור קשר</a></nav>'

ABOUT_FOOTER = '<footer><div class="f-brand"><svg viewBox="0 0 50 50" width="32" fill="none"><rect width="50" height="50" fill="#1A1E24"/><path d="M26,0 L50,0 L50,50 L0,50 L0,40 C3,30 18,10 26,0Z" fill="#E9EEF2"/></svg><div class="f-name">Skylite</div><div class="f-tag">הנדסת הטבע<br>האור שחותך את החלל — מ-1986</div></div><div class="f-links"><a href="#" onclick="home();return false">← חזרה לדף הבית</a><a href="#" onclick="go(\'retractable\');return false">סקיילייט נוסע</a><a href="#" onclick="go(\'fixed\');return false">סקיילייט קבוע</a><a href="#" onclick="go(\'smoke\');return false">מערכות שחרור עשן</a><a href="#" onclick="go(\'tech\');return false">מידע טכני</a></div><div class="f-contact"><p><strong>סקיילייט בע"מ</strong></p><p>אלכסנדר ינאי 8, א.ת סגולה, פתח תקווה</p><p>טל: <a href="tel:+97239343159" dir="ltr" style="color:inherit;text-decoration:none;border-bottom:1px solid currentColor">03-9343159</a> | פקס: <span dir="ltr">03-9311921</span></p><p><a href="mailto:skylite@skylite.co.il" style="color:inherit;text-decoration:none;border-bottom:1px solid currentColor">skylite@skylite.co.il</a></p><p style="margin-top:8px">שעות פעילות: ראשון–חמישי 9:00–18:00</p><p>שישי–שבת: סגור | הגעה בתיאום מראש</p><p style="margin-top:10px"><a href="https://instagram.com/skyliteisrael/" target="_blank" rel="noopener" style="color:var(--accent-pale);text-decoration:none;font-size:12px;letter-spacing:.06em">Instagram — @skyliteisrael</a></p></div></footer>'

ABOUT_PAGE = f'''
<!-- ════ ABOUT ════ -->
<div id="page-about" class="pp">
{ABOUT_NAV}
<section class="pp-hero"><img src="./מוצרים מסווגים/03 — סקיילייט מדרך/Hero Banner .jpg" alt="סקיילייט — הנדסת האור מאז 1986"><div class="pp-hero-ov"></div><div class="pp-hero-c"><div class="pp-hero-cat">About</div><h1 class="pp-hero-name">הנדסת האור.<br>מאז 1986.</h1><div class="pp-hero-tag">פתרונות גגות שקופים — קרוב ל-40 שנות ניסיון</div></div></section>
<section class="pp-content">
  <div><div class="pp-desc-label rv">אודות החברה</div><div class="pp-desc rv rv-d1"><p>חברת סקיילייט מתמחה בפתרונות למערכות גגות שקופים, בעיקר מזכוכית, עם ניסיון ומוניטין של איכות ושירות קרוב ל-40 שנים.</p><p>החברה הוקמה על ידי אהרון שמיר ופועלת בסקטור הציבורי, המסחרי והפרטי. סקיילייט מבצעת את כל שלבי הפרויקט — תכנון, ייצור, התקנה ושירות.</p><p>החברה פועלת בשיתוף פעולה מלא עם אדריכלים, יזמים, קבלנים ולקוחות פרטיים, ומציבה סטנדרט גבוה של מקצועיות, חדשנות ושירות אישי בכל פרויקט.</p></div></div>
  <div class="rv rv-d1"><div class="pp-chars-title">פעילות מקיפה</div><div class="pp-desc"><p>פעילות החברה לפתרון מקיף כוללת גם ייעוץ, יבוא, שיווק וביצוע של מגוון מוצרים בתחום הקירוי השקוף, וכן פתרונות אוורור ושחרור עשן משולבים.</p><p>אנחנו מייצרים את מגוון סוגי הסקיילייטים המרכזיים — קבועים, נוסעים, מדרך, וחלונות ליציאה לגג — וכן מבנים מרחביים מורכבים: כיפות, פירמידות, קשתות וחרוטים.</p><p>כל פרויקט מתוכנן ומיוצר בהתאמה אישית לפי הדרישות הספציפיות.</p></div></div>
</section>
<section class="why-us" id="about-why-us">
  <div class="why-us-inner">
    <h2 class="why-us-title rv">נכון מהפעם הראשונה. בזמן. <em>בשלמות.</em></h2>
    <div class="why-us-body rv rv-d1">
      <p>בפרויקט בנייה, כל עיכוב בגג עולה זמן וכסף. לכן אנחנו מלווים כל שלב — מהסקיצה, דרך ההנדסה והייצור, ועד ההתקנה בשטח.</p>
      <p>כל פרויקט שונה. חלקם מורכבים במיוחד — גיאומטריות חריגות, עומסי רוח, שילוב עם קונסטרוקציה קיימת. אנחנו לא מתחמקים מהמורכבות; אנחנו מתכננים סביבה.</p>
      <p>40 שנה של ניסיון, בקרת איכות קפדנית וצוות הנדסה בתוך הבית — זה הסטנדרט שלנו, ולזה אנחנו שואפים בכל פרויקט: סקיילייט שיוצא נכון מהפעם הראשונה, מגיע בזמן, ונמסר במלואו.</p>
    </div>
  </div>
</section>
<section class="pp-cta"><h2 class="rv">מתכננים פרויקט?<br><em>נשמח להיפגש</em></h2><div class="cta-acts rv rv-d1"><button class="btn-pd" onclick="openCM()">השאירו פרטים</button><a href="tel:+97239343159" class="btn-od">טלפון: 03-9343159</a></div></section>
{ABOUT_FOOTER}
</div>

<!-- ════ STRUCTURAL ════ -->'''

swap("\n<!-- ════ STRUCTURAL ════ -->", ABOUT_PAGE, "Insert About page HTML")

# ═══════════════════════════════════════════════════════════════
# 3. Update home nav link to call go('about')
# ═══════════════════════════════════════════════════════════════
swap(
    '<li><a href="#about">עלינו</a></li>',
    '<li><a href="#" onclick="go(\'about\');return false">עלינו</a></li>',
    "Nav: עלינו now routes via go('about')"
)

# ═══════════════════════════════════════════════════════════════
# 4. Add 'about' to pages array
# ═══════════════════════════════════════════════════════════════
swap(
    "const pages=['home','penthouse','fixed','retractable','walkon','structural','smoke','tech'];",
    "const pages=['home','about','penthouse','fixed','retractable','walkon','structural','smoke','tech'];",
    "pages array: add 'about'"
)

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
    print("   Preview: http://localhost:8100/#about")
