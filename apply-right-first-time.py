#!/usr/bin/env python3
"""apply-right-first-time.py — Add the "Right First Time" positioning section.

Inserts a centered single-column section between the stats and products on the
home page. Hebrew copy chosen by user (April 2026) — Option 2, legally-safe
aspirational framing (no "אחריות", no "ערובה", no future-tense "no leaks" promise).

Adds:
  • CSS: .why-us / .why-us-inner / .why-us-title / .why-us-body  (light-linen bg,
    centered column, typographic rhythm matching .statement section)
  • HTML: new <section class="why-us"> between stats and products

Idempotent: skipped if already applied.
"""
import sys, pathlib

HTML = pathlib.Path(__file__).parent / "index.html"
src  = HTML.read_text(encoding="utf-8")
changes = 0

def swap(old, new, label):
    global src, changes
    if new in src:
        print(f"✔  {label} — already applied, skipping")
        return
    if old not in src:
        print(f"❌ {label} — anchor not found; aborting")
        sys.exit(1)
    src = src.replace(old, new, 1)
    changes += 1
    print(f"✔  {label}")

# ══════════════════════════════════════════════════════════════════
# 1. CSS — centered single-column "why us" section
# ══════════════════════════════════════════════════════════════════
CSS_ANCHOR = "    .stat-n sup{font-size:28px;color:var(--accent)}"
CSS_ADD = CSS_ANCHOR + """
    .stat-l{font-size:13px;font-weight:300;letter-spacing:.08em;color:var(--stone);line-height:1.5}

    /* ── WHY US: Right First Time positioning ── */
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

# The existing src has `.stat-l{...}` on the same logical block as `.stat-n`,
# but they may be on different lines. Find the exact contiguous pair.
STAT_L_LINE = "    .stat-l{font-size:13px;font-weight:300;letter-spacing:.08em;color:var(--stone);line-height:1.5}"
OLD_PAIR = CSS_ANCHOR + "\n" + STAT_L_LINE
swap(OLD_PAIR, CSS_ADD, "CSS: .why-us section")

# ══════════════════════════════════════════════════════════════════
# 2. HTML — insert the section between stats and products
# ══════════════════════════════════════════════════════════════════
OLD_HTML = """  <div class="stat"><div class="stat-n">100<sup>%</sup></div><div class="stat-l">תכנון, ייצור והרכבה<br>מקומיים, בתוך הבית</div></div>
</section>

<section class="products" id="products">"""

NEW_HTML = """  <div class="stat"><div class="stat-n">100<sup>%</sup></div><div class="stat-l">תכנון, ייצור והרכבה<br>מקומיים, בתוך הבית</div></div>
</section>

<section class="why-us" id="why-skylite">
  <div class="why-us-inner">
    <h2 class="why-us-title rv">נכון מהפעם הראשונה. בזמן. <em>בשלמות.</em></h2>
    <div class="why-us-body rv rv-d1">
      <p>בפרויקט בנייה, כל עיכוב בגג עולה זמן וכסף. לכן אנחנו מלווים כל שלב — מהסקיצה, דרך ההנדסה והייצור, ועד ההתקנה בשטח.</p>
      <p>כל פרויקט שונה. חלקם מורכבים במיוחד — גיאומטריות חריגות, עומסי רוח, שילוב עם קונסטרוקציה קיימת. אנחנו לא מתחמקים מהמורכבות; אנחנו מתכננים סביבה.</p>
      <p>40 שנה של ניסיון, בקרת איכות קפדנית וצוות הנדסה בתוך הבית — זה הסטנדרט שלנו, ולזה אנחנו שואפים בכל פרויקט: סקיילייט שיוצא נכון מהפעם הראשונה, מגיע בזמן, ונמסר במלואו.</p>
    </div>
  </div>
</section>

<section class="products" id="products">"""

swap(OLD_HTML, NEW_HTML, "HTML: why-us section between stats and products")

# ══════════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — everything already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
    print("   Preview: python3 -m http.server 8080 → http://localhost:8080/#why-skylite")
