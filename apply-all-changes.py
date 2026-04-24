#!/usr/bin/env python3
"""Apply all design consistency + content enrichment changes."""
import os, sys, re

FILE = os.path.expanduser("~/Downloads/skylite-github/index.html")
if not os.path.exists(FILE): print("❌ not found"); sys.exit(1)
with open(FILE, "r", encoding="utf-8") as f: html = f.read()
changes = 0

# ── 1. Label font sizes: 9px → 10px ──
if "p-card-en{font-size:9px" in html:
    html = html.replace("p-card-en{font-size:9px", "p-card-en{font-size:10px")
    changes += 1; print("✅ .p-card-en 9px → 10px")

if "p-card-badge{" in html and "font-size:9px" in html:
    html = html.replace(
        "p-card-badge{display:inline-block;padding:4px 14px;background:var(--accent-deep);font-size:9px;font-weight:500;letter-spacing:.2em",
        "p-card-badge{display:inline-block;padding:4px 14px;background:var(--accent-deep);font-size:10px;font-weight:500;letter-spacing:.22em"
    )
    changes += 1; print("✅ .p-card-badge 9px → 10px")

# ── 2. Normalize label letter-spacing to .30em ──
if "proc-num{" in html and "letter-spacing:.28em" in html:
    html = html.replace(
        ".proc-num{font-size:10px;font-weight:400;letter-spacing:.28em",
        ".proc-num{font-size:10px;font-weight:400;letter-spacing:.30em"
    )
    changes += 1; print("✅ .proc-num letter-spacing → .30em")

if "pp-hero-cat{" in html and "letter-spacing:.32em" in html:
    html = html.replace(
        ".pp-hero-cat{font-size:10px;font-weight:400;letter-spacing:.32em",
        ".pp-hero-cat{font-size:10px;font-weight:400;letter-spacing:.30em"
    )
    changes += 1; print("✅ .pp-hero-cat letter-spacing → .30em")

# ── 3. Opacity fixes ──
if "p-card-tag{" in html and "color:rgba(255,255,255,.48)" in html:
    html = html.replace("color:rgba(255,255,255,.48);margin-top:8px;letter-spacing:.015em", "color:rgba(255,255,255,.6);margin-top:8px;letter-spacing:.02em")
    changes += 1; print("✅ .p-card-tag opacity .48 → .6")

if "scrolled .nav-links a{color:rgba(28,26,22,.5)}" in html:
    html = html.replace("scrolled .nav-links a{color:rgba(28,26,22,.5)}", "scrolled .nav-links a{color:rgba(28,26,22,.6)}")
    changes += 1; print("✅ Scrolled nav links opacity .5 → .6")

# ── 4. Process header body text 15px → 14px ──
if 'font-size:15px;font-weight:300;color:var(--stone);line-height:1.75;max-width:320px' in html:
    html = html.replace(
        'font-size:15px;font-weight:300;color:var(--stone);line-height:1.75;max-width:320px',
        'font-size:14px;font-weight:300;color:var(--stone);line-height:1.75;max-width:320px'
    )
    changes += 1; print("✅ Process header text 15px → 14px")

# ── 5. Enrich Fixed page ──
old_fixed_desc = 'מגיע בתצורה חד-שיפועית לגגות שטוחים ודו-שיפועית לגגות בעלי מרכז. מתאים למגורים ולמסחרי כאחד.</p></div></div>'
new_fixed_desc = 'מגיע בתצורה חד-שיפועית לגגות שטוחים ודו-שיפועית לגגות בעלי מרכז. מתאים למגורים ולמסחרי כאחד.</p><p>מערכות הזיגוג מותקנות בשיטת FLUSH GLAZING — הזכוכית מהודקת אך ורק באמצעות פרופילי האלומיניום, ללא מגע ישיר בין חומר הזיגוג לאלומיניום. הפרופילים כוללים תעלות ניקוז פנימי המונעות חדירת מים לחלל המבנה.</p></div></div>'
if old_fixed_desc in html and 'FLUSH GLAZING' not in html.split('page-fixed')[1].split('page-retractable')[0]:
    html = html.replace(old_fixed_desc, new_fixed_desc, 1)
    changes += 1; print("✅ Enriched Fixed page description")

old_fixed_chars = 'קונסטרוקציית אלומיניום</div><div class="pp-char-desc">מסגרת אלומיניום עם זיגוג זכוכית'
new_fixed_chars = 'פרופילי אלומיניום 6063 TF</div><div class="pp-char-desc">פרופילים קונסטרוקטיביים עם איטום ומירזוב עצמיים. אטמי EPDM משולבים כחלק אינטגרלי — לא מודבקים, לא נדחסים.'
if old_fixed_chars in html:
    # Replace the full characteristics section for fixed page
    html = html.replace(old_fixed_chars, new_fixed_chars)
    changes += 1; print("✅ Enriched Fixed page characteristics")

# ── 6. Enrich Walk-On page ──
old_walkon = 'מיוחד לחצרות פנימיות, אתרי מורשת, גשרים מזוגגים ומרחבים אדריכליים ייחודיים.</p></div></div>'
if old_walkon in html and 'עומסי דריכה' not in html.split('page-walkon')[1].split('page-structural')[0]:
    new_walkon = 'מיוחד לחצרות פנימיות, אתרי מורשת, גשרים מזוגגים ומרחבים אדריכליים ייחודיים.</p><p>הזיגוג עשוי זכוכית ביטחון מרובדת המתאימה לעומסי דריכה — בשום נקודה חומר הזיגוג לא בא במגע ישיר עם האלומיניום. תעלות ניקוז פנימיות בפרופילים מונעות הצטברות מים מתחת למשטח ההליכה.</p></div></div>'
    html = html.replace(old_walkon, new_walkon, 1)
    changes += 1; print("✅ Enriched Walk-On page description")

# ── 7. Enrich Structural page ──
old_struct = 'אנחנו עובדים צמוד לאדריכל ולמהנדס הקונסטרוקציה — ומספקים פתרון מלא.</p></div></div>'
if old_struct in html and 'יקב רקנאטי' not in html.split('page-structural')[1].split('page-smoke')[0][:500]:
    new_struct = 'אנחנו עובדים צמוד לאדריכל ולמהנדס הקונסטרוקציה — ומספקים פתרון מלא. 40 שנה של ניסיון בפרויקטים מורכבים — מיקב רקנאטי ועד אוניברסיטת בר אילן — מאפשרים לנו להתמודד עם כל אתגר גיאומטרי.</p><p>הקונסטרוקציה בנויה מפרופילי אלומיניום 6063 TF עם איטום ומירזוב עצמיים, מערכות זיגוג בשיטת FLUSH GLAZING, ותעלות ניקוז פנימיות. כל חלקי האלומיניום החשופים בגימור צביעה אלקטרוסטטית בתנור — צבע RAL לבחירת האדריכל.</p></div></div>'
    html = html.replace(old_struct, new_struct, 1)
    changes += 1; print("✅ Enriched Structural page description")

if changes > 0:
    with open(FILE, "w", encoding="utf-8") as f: f.write(html)
    print(f"\n🎉 Applied {changes} change(s). Hard refresh.")
else:
    print("✅ All changes already applied.")
