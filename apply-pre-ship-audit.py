#!/usr/bin/env python3
"""apply-pre-ship-audit.py — Consolidated pre-ship fixes.

Landing all decisions from the 4-agent audit in a single script:

DATA / CONTENT
  1. Hero statement: "המלון באילת" → "המלון במצפה הימים" (fabricated claim fix)
  2. Synagogue metadata: blank year + arch (unverifiable)
  3. HP HQ: add when:'2012' (verified via ArchDaily + Mann-Shinar portfolio)
  4. Mitzpe Hayamim: add when:'2020' (verified via hospitalitynet.org)

UX COPY
  5. Form success message: add SLA + phone fallback

CODE CLEANUP
  6. Delete SELECTED_WORK.retractable leftover entry
  7. Delete `['retractable'].forEach(renderSelectedWork)` init line

MOBILE READINESS
  8. Footer phone → <a href="tel:">
  9. Footer email → <a href="mailto:">
  10. Modal scroll-lock (body overflow toggle on open/close)
  11. .pp-hero min-height reduced on mobile (< 600px)
  12. .form-field input padding bumped on mobile (tap target)
  13. .lb-close repositioned for mobile

Idempotent (re-run safe).
"""
import sys, pathlib, re

HTML = pathlib.Path(__file__).parent / "index.html"
src = HTML.read_text(encoding="utf-8")
changes = 0

def swap(old, new, label):
    global src, changes
    if new in src:
        print(f"✔  {label} — already applied")
        return
    if old not in src:
        print(f"❌ {label} — anchor not found; aborting")
        sys.exit(1)
    src = src.replace(old, new, 1)
    changes += 1
    print(f"✔  {label}")

def swap_any(pairs, label):
    """Try multiple (old, new) alternatives until one matches. Used when the
    anchor text might vary slightly in whitespace/quoting."""
    global src, changes
    for old, new in pairs:
        if new in src:
            print(f"✔  {label} — already applied")
            return
        if old in src:
            src = src.replace(old, new, 1)
            changes += 1
            print(f"✔  {label}")
            return
    print(f"❌ {label} — no anchor variant matched; aborting")
    sys.exit(1)

# ══════════════════════════════════════════════════════════════════
# 1. Eilat hotel → Mitzpe Hayamim in hero statement
# ══════════════════════════════════════════════════════════════════
swap(
    "המלון באילת",
    "המלון במצפה הימים",
    "Hero: replace fabricated Eilat reference with Mitzpe Hayamim"
)

# ══════════════════════════════════════════════════════════════════
# 2. Synagogue: blank year + arch
# ══════════════════════════════════════════════════════════════════
swap(
    "meta:{where:'אור יהודה',when:'2007',arch:'אילן פילוסוף',product:'מבנים מרחביים, כיפה'}",
    "meta:{where:'אור יהודה',when:'—',arch:'—',product:'מבנים מרחביים, כיפה'}",
    "Synagogue: blank unverifiable year/arch"
)

# ══════════════════════════════════════════════════════════════════
# 3. HP HQ: add when='2012'
# ══════════════════════════════════════════════════════════════════
swap(
    "meta:{where:'יהוד',when:'—',arch:'אמיר מן, עמי שנער אדריכלים'",
    "meta:{where:'יהוד',when:'2012',arch:'אמיר מן, עמי שנער אדריכלים'",
    "HP HQ: add when='2012'"
)

# ══════════════════════════════════════════════════════════════════
# 4. Mitzpe Hayamim: add when='2020'
# ══════════════════════════════════════════════════════════════════
swap(
    "meta:{where:'ראש פינה',when:'—',arch:'פייגין'",
    "meta:{where:'ראש פינה',when:'2020',arch:'פייגין'",
    "Mitzpe Hayamim: add when='2020'"
)

# ══════════════════════════════════════════════════════════════════
# 5. Form success message: add SLA + phone fallback
# Both the main form and modal form can share the same success block — check
# how many instances exist. Current text: "קיבלנו את הפרטים שלכם ונחזור אליכם בהקדם."
# ══════════════════════════════════════════════════════════════════
OLD_SUCCESS = "<p>קיבלנו את הפרטים שלכם ונחזור אליכם בהקדם.</p>"
NEW_SUCCESS = '<p>קיבלנו את פרטיכם — נחזור אליכם תוך יום עסקים אחד. לפנייה דחופה, חייגו <a href="tel:+97239343159" style="color:var(--accent);text-decoration:none;border-bottom:1px solid var(--accent)">03-9343159</a>.</p>'
# There may be more than one occurrence (main + modal); replace all
count_success = src.count(OLD_SUCCESS)
count_new = src.count(NEW_SUCCESS)
if count_new > 0 and count_success == 0:
    print(f"✔  Form success message — already applied ({count_new} instance(s))")
elif count_success > 0:
    src = src.replace(OLD_SUCCESS, NEW_SUCCESS)
    changes += 1
    print(f"✔  Form success message — rewrote {count_success} instance(s) with SLA + phone fallback")
else:
    print("❌ Form success message anchor not found; aborting")
    sys.exit(1)

# ══════════════════════════════════════════════════════════════════
# 6. Delete SELECTED_WORK.retractable entry (dead data)
# ══════════════════════════════════════════════════════════════════
# The retractable entry is the only one likely still in SELECTED_WORK. Try to
# match the entire const SELECTED_WORK = {...} block and see what's left.
m = re.search(r"const SELECTED_WORK\s*=\s*\{([\s\S]*?)\n\};", src)
if m:
    body = m.group(1)
    # Is there a retractable entry?
    retr_match = re.search(r"\s*retractable:\[[^\]]*\],?\n", body)
    if retr_match:
        old_block = "const SELECTED_WORK={" + body + "\n};"
        new_body = body.replace(retr_match.group(0), "\n")
        # Collapse multiple consecutive newlines
        new_body = re.sub(r"\n\n+", "\n", new_body).rstrip()
        new_block = "const SELECTED_WORK={" + new_body + ("\n" if new_body and not new_body.endswith("\n") else "") + "};"
        if old_block in src:
            src = src.replace(old_block, new_block, 1)
            changes += 1
            print("✔  SELECTED_WORK: removed retractable entry")
        else:
            print("⚠  SELECTED_WORK block located but exact replacement didn't match — skipping (likely already clean)")
    else:
        print("✔  SELECTED_WORK: retractable already absent")
else:
    print("⚠  SELECTED_WORK object not found — skipping")

# ══════════════════════════════════════════════════════════════════
# 7. Delete the ['retractable'].forEach(renderSelectedWork) init line
# ══════════════════════════════════════════════════════════════════
swap(
    "['retractable'].forEach(renderSelectedWork);\n",
    "",
    "Init: remove dead renderSelectedWork call"
)

# ══════════════════════════════════════════════════════════════════
# 8+9. Footer phone → tel: link, email → mailto: link
# Pattern appears in multiple footers (home + each product page + project
# pages); replace all instances in one shot.
# ══════════════════════════════════════════════════════════════════
OLD_FOOTER = '<p>טל: 03-9343159 | פקס: 03-9311921</p><p>skylite@skylite.co.il</p>'
NEW_FOOTER = '<p>טל: <a href="tel:+97239343159" dir="ltr" style="color:inherit;text-decoration:none;border-bottom:1px solid currentColor">03-9343159</a> | פקס: <span dir="ltr">03-9311921</span></p><p><a href="mailto:skylite@skylite.co.il" style="color:inherit;text-decoration:none;border-bottom:1px solid currentColor">skylite@skylite.co.il</a></p>'
count = src.count(OLD_FOOTER)
count_new_footer = src.count(NEW_FOOTER)
if count_new_footer > 0 and count == 0:
    print(f"✔  Footer tel:/mailto: — already applied ({count_new_footer} footer(s))")
elif count > 0:
    src = src.replace(OLD_FOOTER, NEW_FOOTER)
    changes += 1
    print(f"✔  Footer: phone + email made tappable in {count} footer(s)")
else:
    print("⚠  Footer phone/email anchor not found — skipping (already patched or different format)")

# ══════════════════════════════════════════════════════════════════
# 10. Modal scroll-lock — add body.overflow toggle
# ══════════════════════════════════════════════════════════════════
# Look for openCM / closeCM function definitions
OLD_CM_FN_A = """function openCM(){document.getElementById('contact-modal').classList.add('open')}
function closeCM(){document.getElementById('contact-modal').classList.remove('open')}"""
NEW_CM_FN = """function openCM(){document.getElementById('contact-modal').classList.add('open');document.body.style.overflow='hidden'}
function closeCM(){document.getElementById('contact-modal').classList.remove('open');document.body.style.overflow=''}"""
if NEW_CM_FN in src:
    print("✔  Modal scroll-lock — already applied")
elif OLD_CM_FN_A in src:
    src = src.replace(OLD_CM_FN_A, NEW_CM_FN, 1)
    changes += 1
    print("✔  Modal scroll-lock: added body.overflow toggle")
else:
    # Try to find openCM differently; they may be on different lines
    m = re.search(r"function openCM\(\)\{[^}]+\}", src)
    m2 = re.search(r"function closeCM\(\)\{[^}]+\}", src)
    if m and m2 and 'overflow' not in m.group() and 'overflow' not in m2.group():
        src = src.replace(m.group(), m.group().rstrip('}') + ";document.body.style.overflow='hidden'}", 1)
        src = src.replace(m2.group(), m2.group().rstrip('}') + ";document.body.style.overflow=''}", 1)
        changes += 1
        print("✔  Modal scroll-lock: added body.overflow toggle (via regex fallback)")
    else:
        print("⚠  openCM/closeCM not found in expected shape — skipping scroll-lock")

# ══════════════════════════════════════════════════════════════════
# 11+12+13. Mobile CSS tweaks — append to the existing @media(max-width:600px) block
# if one exists, or add a new one near the end of <style>
# ══════════════════════════════════════════════════════════════════
MOBILE_CSS = """
    /* Pre-ship mobile polish */
    @media(max-width:600px){
      .pp-hero{min-height:420px}
      .form-field input{padding:18px 20px;font-size:16px}
      .lb-close{top:14px;right:14px;width:40px;height:40px;font-size:20px}
      .lb-prev{right:8px}
      .lb-next{left:8px}
    }
"""
# Insert right before the closing </style> tag
STYLE_CLOSE = "</style>"
SIGNATURE = "/* Pre-ship mobile polish */"
if SIGNATURE in src:
    print("✔  Mobile polish CSS — already applied")
elif STYLE_CLOSE in src:
    src = src.replace(STYLE_CLOSE, MOBILE_CSS + "  " + STYLE_CLOSE, 1)
    changes += 1
    print("✔  Mobile polish CSS — added (pp-hero height, form padding, lightbox pos)")
else:
    print("❌ </style> not found — mobile CSS skipped")

# ══════════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — everything already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
