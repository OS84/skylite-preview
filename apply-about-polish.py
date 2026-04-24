#!/usr/bin/env python3
"""apply-about-polish.py — About page design polish from audit agent.

Changes:
  1. Remove <br> from H1 (let CSS clamp handle mobile wrap)
  2. Rewrite hero tagline: About-voiced instead of product-generic
  3. Bump .why-us-body p font 17px/300 → 18px/400 (gravitas)
  4. Global .pp-desc typography alignment: 18px/300/1.82 → 15px/400/1.75
     (aligns with CLAUDE.md typeset spec; affects all product pages)
  5. Convert About's Right First Time block to 2-column split:
     text on right (RTL native), image on left
     — uses modifier class .why-us--split scoped to About page only
     — mobile: single column, image first
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
# 1. Remove <br> from About H1
# ═══════════════════════════════════════════════════════════════
swap(
    '<h1 class="pp-hero-name">הנדסת האור.<br>מאז 1986.</h1>',
    '<h1 class="pp-hero-name">הנדסת האור. מאז 1986.</h1>',
    "H1: remove <br> (CSS clamp handles mobile wrap)"
)

# ═══════════════════════════════════════════════════════════════
# 2. New hero tagline
# ═══════════════════════════════════════════════════════════════
swap(
    '<div class="pp-hero-tag">פתרונות גגות שקופים — קרוב ל-40 שנות ניסיון</div>',
    '<div class="pp-hero-tag">הסיפור של סקיילייט — 40 שנה של הנדסת אור</div>',
    "Hero tagline: About-voiced"
)

# ═══════════════════════════════════════════════════════════════
# 3. .why-us-body font bump (17 → 18, weight 300 → 400)
# ═══════════════════════════════════════════════════════════════
swap(
    ".why-us-body p{font-size:17px;font-weight:300;line-height:1.9;color:var(--stone);margin-bottom:22px}",
    ".why-us-body p{font-size:18px;font-weight:400;line-height:1.85;color:var(--stone);margin-bottom:22px}",
    ".why-us-body p: 17→18 / 300→400"
)

# ═══════════════════════════════════════════════════════════════
# 4. Global .pp-desc typography alignment with CLAUDE.md spec
# ═══════════════════════════════════════════════════════════════
swap(
    ".pp-desc{font-size:18px;font-weight:300;line-height:1.82;color:var(--dark)}",
    ".pp-desc{font-size:15px;font-weight:400;line-height:1.75;color:var(--dark)}",
    ".pp-desc: 18/300/1.82 → 15/400/1.75 (aligns typeset spec, affects all product pages)"
)

# ═══════════════════════════════════════════════════════════════
# 5. Add .why-us--split CSS (2-column variant)
# ═══════════════════════════════════════════════════════════════
SPLIT_CSS = """
    /* About page: Right First Time as 2-column split with image.
       HTML order = image first then text. In RTL, first child renders on
       the right, so image ends up on the right and text on the left. */
    .why-us--split{text-align:right}
    .why-us--split .why-us-inner{max-width:1160px;display:grid;grid-template-columns:1fr 1.5fr;gap:72px;align-items:start;text-align:right}
    .why-us--split .why-us-title{text-align:right;margin-bottom:36px}
    .why-us--split .why-us-body{text-align:right}
    .why-us--split-img{aspect-ratio:3/4;border-radius:6px;overflow:hidden;background:var(--dark)}
    .why-us--split-img img{width:100%;height:100%;object-fit:cover;filter:brightness(.95) saturate(1.04);transition:transform 1.2s var(--spring)}
    .why-us--split-img:hover img{transform:scale(1.03)}
    @media(max-width:1024px){
      .why-us--split .why-us-inner{grid-template-columns:1fr;gap:40px;max-width:640px}
      .why-us--split-img{aspect-ratio:16/10}
    }
    @media(max-width:600px){
      .why-us--split .why-us-inner{gap:28px}
    }
"""

WHYUS_MOBILE_ANCHOR = '    @media(max-width:600px){.why-us{padding:64px 24px 64px}.why-us-title{margin-bottom:32px}.why-us-body p{font-size:16px;line-height:1.85}}'
if ".why-us--split" in src:
    print("✔  .why-us--split CSS already present")
else:
    src = src.replace(WHYUS_MOBILE_ANCHOR, WHYUS_MOBILE_ANCHOR + SPLIT_CSS, 1)
    changes += 1
    print("✔  Added .why-us--split CSS (2-column with image)")

# ═══════════════════════════════════════════════════════════════
# 6. Update About page: why-us section → split variant with image
# ═══════════════════════════════════════════════════════════════
OLD_WHYUS_HTML = '''<section class="why-us" id="about-why-us">
  <div class="why-us-inner">
    <h2 class="why-us-title rv">נכון מהפעם הראשונה. בזמן. <em>בשלמות.</em></h2>
    <div class="why-us-body rv rv-d1">
      <p>בפרויקט בנייה, כל עיכוב בגג עולה זמן וכסף. לכן אנחנו מלווים כל שלב — מהסקיצה, דרך ההנדסה והייצור, ועד ההתקנה בשטח.</p>
      <p>כל פרויקט שונה. חלקם מורכבים במיוחד — גיאומטריות חריגות, עומסי רוח, שילוב עם קונסטרוקציה קיימת. אנחנו לא מתחמקים מהמורכבות; אנחנו מתכננים סביבה.</p>
      <p>40 שנה של ניסיון, בקרת איכות קפדנית וצוות הנדסה בתוך הבית — זה הסטנדרט שלנו, ולזה אנחנו שואפים בכל פרויקט: סקיילייט שיוצא נכון מהפעם הראשונה, מגיע בזמן, ונמסר במלואו.</p>
    </div>
  </div>
</section>'''

NEW_WHYUS_HTML = '''<section class="why-us why-us--split" id="about-why-us">
  <div class="why-us-inner">
    <div class="why-us--split-img rv">
      <img src="./מוצרים מסווגים/04 — מבנים מרחביים/כיפה/048.jpeg" alt="סקיילייט — כיפה מרחבית" loading="lazy">
    </div>
    <div>
      <h2 class="why-us-title rv rv-d1">נכון מהפעם הראשונה. בזמן. <em>בשלמות.</em></h2>
      <div class="why-us-body rv rv-d2">
        <p>בפרויקט בנייה, כל עיכוב בגג עולה זמן וכסף. לכן אנחנו מלווים כל שלב — מהסקיצה, דרך ההנדסה והייצור, ועד ההתקנה בשטח.</p>
        <p>כל פרויקט שונה. חלקם מורכבים במיוחד — גיאומטריות חריגות, עומסי רוח, שילוב עם קונסטרוקציה קיימת. אנחנו לא מתחמקים מהמורכבות; אנחנו מתכננים סביבה.</p>
        <p>40 שנה של ניסיון, בקרת איכות קפדנית וצוות הנדסה בתוך הבית — זה הסטנדרט שלנו, ולזה אנחנו שואפים בכל פרויקט: סקיילייט שיוצא נכון מהפעם הראשונה, מגיע בזמן, ונמסר במלואו.</p>
      </div>
    </div>
  </div>
</section>'''
swap(OLD_WHYUS_HTML, NEW_WHYUS_HTML, "About: why-us section → split with image")

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
