#!/usr/bin/env python3
"""apply-penthouse-copy.py — Rewrite the "על המוצר" block on the penthouse page.

Replaces the utilitarian 2-paragraph description with a 4-paragraph version
that leads with experience, keeps the technical anchors, and closes on brand
scope. Conservative on claims — dropped specific voltage, EN 12101 cert, and
rain/wind sensor language pending product-variant verification.
"""
import sys, pathlib

HTML = pathlib.Path(__file__).parent / "index.html"
src  = HTML.read_text(encoding="utf-8")

OLD = '<div><div class="pp-desc-label rv">על המוצר</div><div class="pp-desc rv rv-d1"><p>חלונות סקיילייט המשמשים ליציאה לגג, לסוכה, לאיוורור ושחרור עשן. מופעלים באמצעות מפסק חשמלי, שלט או רכזת הפעלה. החלון בנוי ממערכת אלומיניום בעלת דופן כפולה ייעודית, צירים אטמים ומנוע.</p><p>מידות לפי הזמנה — לפרויקטים ויישומים מיוחדים ולבתים פרטיים. התקנה מתבצעת על ידי חברת סקיילייט.</p></div></div>'

NEW = '<div><div class="pp-desc-label rv">על המוצר</div><div class="pp-desc rv rv-d1"><p>בית שנפתח לשמיים. לוחצים על הכפתור — והתקרה נעה הצידה. לא דלת לגג, אלא הגג עצמו שהופך להמשך של הבית. אור שמש ממלא את החלל; ערב קיצי נכנס פנימה; בחג הסוכות, הארוחה מתחת לשמיים — בלב הסלון.</p><p>הפתיחה חלקה, שקטה ומבוקרת — בשלט, במפסק או דרך רכזת ההפעלה. אפשר לשלוט מהספה.</p><p>המערכת בנויה ממסגרת אלומיניום בעלת דופן כפולה, אטמים אינטגרליים, צירים אטומים ומנוע חשמלי ייעודי.</p><p>מידות לפי הזמנה. תכנון, ייצור והתקנה על ידי חברת סקיילייט — בפנטהאוזים, בווילות ובפרויקטים מוסדיים בישראל, מאז 1986.</p></div></div>'

if NEW in src:
    print("✔  Penthouse copy already applied")
    sys.exit(0)
if OLD not in src:
    print("❌ Anchor not found — current penthouse 'על המוצר' copy doesn't match expected original")
    sys.exit(1)

src = src.replace(OLD, NEW, 1)
HTML.write_text(src, encoding="utf-8")
print("✅ Penthouse 'על המוצר' copy updated")
print("   Preview: http://localhost:8100/#penthouse")
