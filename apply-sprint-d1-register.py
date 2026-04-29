#!/usr/bin/env python3
"""apply-sprint-d1-register.py — Replace home product grid with V1 Register list.

V1 Atelier shows the 7 products as a vertical "register" of rows. Each row:
  num · 220×130 thumbnail · Hebrew name + English subtitle · 1-line tag · arrow

Replaces the 7-card photo grid (.p-grid) with the Register pattern.

Idempotent.
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
# 1) CSS — Register pattern
# ═══════════════════════════════════════════════════════════════
REGISTER_CSS = """
    /* ── HOME REGISTER (Sprint D-1, V1 Atelier) ── */
    .p-register{display:flex;flex-direction:column;direction:rtl}
    .p-register-row{display:grid;grid-template-columns:60px 220px 1fr 1.4fr 80px;gap:36px;align-items:center;padding:22px 0;border-bottom:1px solid var(--warm-gray);cursor:pointer;transition:background .35s var(--spring);position:relative;text-decoration:none;color:inherit}
    .p-register-row:first-child{border-top:1px solid var(--warm-gray)}
    .p-register-row:hover{background:rgba(28,26,22,.025)}
    .p-register-row:focus-visible{outline:2px solid var(--accent);outline-offset:-2px;background:rgba(43,122,140,.04)}
    .p-register-num{font-size:13px;font-weight:500;letter-spacing:.14em;color:var(--stone);font-feature-settings:'tnum'}
    .p-register-thumb{width:220px;height:130px;object-fit:cover;filter:saturate(.96) contrast(1.04);transition:filter .55s var(--spring);background:var(--dark)}
    .p-register-row:hover .p-register-thumb{filter:saturate(1.10) brightness(1.04)}
    .p-register-name-block{}
    .p-register-name{font-weight:700;font-size:26px;line-height:1.15;letter-spacing:-.005em;color:var(--dark);margin:0}
    .p-register-en{font-size:11px;font-weight:500;letter-spacing:.22em;color:var(--stone);text-transform:uppercase;margin-top:6px}
    .p-register-tag{font-size:15px;font-weight:400;line-height:1.55;color:var(--stone)}
    .p-register-arr{display:flex;align-items:center;justify-content:flex-start;color:var(--accent);transition:transform .35s var(--spring)}
    .p-register-row:hover .p-register-arr{transform:translateX(-8px)}
    .p-register-arr svg{width:28px;height:28px;stroke:currentColor;fill:none;stroke-width:1.5}
    @media(max-width:1024px){.p-register-row{grid-template-columns:50px 180px 1fr 1fr 60px;gap:24px}.p-register-thumb{width:180px;height:108px}.p-register-name{font-size:22px}}
    @media(max-width:768px){.p-register-row{grid-template-columns:1fr;gap:14px;padding:24px 0;text-align:start}.p-register-num{display:none}.p-register-thumb{width:100%;height:160px}.p-register-name{font-size:24px}.p-register-arr{display:none}}
"""

# Insert before "QUIET RIBBON GALLERY" comment which we know is in CSS
swap(
    "    /* ── QUIET RIBBON GALLERY",
    REGISTER_CSS + "\n    /* ── QUIET RIBBON GALLERY",
    "Insert Register CSS",
)

# ═══════════════════════════════════════════════════════════════
# 2) Replace .p-grid HTML with Register list
# ═══════════════════════════════════════════════════════════════
REGISTER_HTML = """  <div class="p-register">

    <a class="p-register-row rv" href="#" onclick="go('retractable');return false">
      <div class="p-register-num">01</div>
      <img class="p-register-thumb" src="./מוצרים מסווגים/01 — סקיילייט נוסע/חד שיפועי/DOR_6758-HDR.jpg" alt="סקיילייט נוסע" loading="lazy">
      <div class="p-register-name-block">
        <h3 class="p-register-name">סקיילייט נוסע</h3>
        <div class="p-register-en">Retractable Systems</div>
      </div>
      <div class="p-register-tag">גג שנפתח — שמיים שנכנסים</div>
      <div class="p-register-arr"><svg viewBox="0 0 24 24"><path d="M19 12H5M11 5l-6 7 6 7"/></svg></div>
    </a>

    <a class="p-register-row rv" href="#" onclick="go('fixed');return false">
      <div class="p-register-num">02</div>
      <img class="p-register-thumb" src="./מוצרים מסווגים/02 — סקיילייט קבוע/חד שיפועי/Edited-2.jpg" alt="סקיילייט קבוע" loading="lazy">
      <div class="p-register-name-block">
        <h3 class="p-register-name">סקיילייט קבוע</h3>
        <div class="p-register-en">Fixed Skylights</div>
      </div>
      <div class="p-register-tag">הידוע — המוכח</div>
      <div class="p-register-arr"><svg viewBox="0 0 24 24"><path d="M19 12H5M11 5l-6 7 6 7"/></svg></div>
    </a>

    <a class="p-register-row rv" href="#" onclick="go('walkon');return false">
      <div class="p-register-num">03</div>
      <img class="p-register-thumb" src="./מוצרים מסווגים/03 — סקיילייט מדרך/Hero.jpeg" alt="סקיילייט מדרך" loading="lazy">
      <div class="p-register-name-block">
        <h3 class="p-register-name">סקיילייט מדרך</h3>
        <div class="p-register-en">Walk-On Glass</div>
      </div>
      <div class="p-register-tag">אפס קו — מקסימום עומק</div>
      <div class="p-register-arr"><svg viewBox="0 0 24 24"><path d="M19 12H5M11 5l-6 7 6 7"/></svg></div>
    </a>

    <a class="p-register-row rv" href="#" onclick="go('structural');return false">
      <div class="p-register-num">04</div>
      <img class="p-register-thumb" src="./מוצרים מסווגים/04 — מבנים מרחביים/כיפה/Edited-1.jpg" alt="מבנים מרחביים" loading="lazy">
      <div class="p-register-name-block">
        <h3 class="p-register-name">מבנים מרחביים</h3>
        <div class="p-register-en">Structural Glazing</div>
      </div>
      <div class="p-register-tag">כאשר הגיאומטריה הופכת לשירה</div>
      <div class="p-register-arr"><svg viewBox="0 0 24 24"><path d="M19 12H5M11 5l-6 7 6 7"/></svg></div>
    </a>

    <a class="p-register-row rv" href="#" onclick="go('smoke');return false">
      <div class="p-register-num">05</div>
      <img class="p-register-thumb" src="./מוצרים מסווגים/05 — כיפות תאורה, אוורור ושחרור עשן/גפני1.jpg" alt="כיפות תאורה ושחרור עשן" loading="lazy">
      <div class="p-register-name-block">
        <h3 class="p-register-name">כיפות תאורה ושחרור עשן</h3>
        <div class="p-register-en">Light Domes & Smoke Vents</div>
      </div>
      <div class="p-register-tag">בטיחות שלא מוותרת על עיצוב</div>
      <div class="p-register-arr"><svg viewBox="0 0 24 24"><path d="M19 12H5M11 5l-6 7 6 7"/></svg></div>
    </a>

    <a class="p-register-row rv" href="#" onclick="go('penthouse');return false">
      <div class="p-register-num">06</div>
      <img class="p-register-thumb" src="./מוצרים מסווגים/06 — יציאה לגג/Hero copy.jpg" alt="יציאה לגג" loading="lazy">
      <div class="p-register-name-block">
        <h3 class="p-register-name">יציאה לגג</h3>
        <div class="p-register-en">Roof Access</div>
      </div>
      <div class="p-register-tag">הדלת שפותחת שמיים</div>
      <div class="p-register-arr"><svg viewBox="0 0 24 24"><path d="M19 12H5M11 5l-6 7 6 7"/></svg></div>
    </a>

    <a class="p-register-row rv" href="#" onclick="go('windows');return false">
      <div class="p-register-num">07</div>
      <img class="p-register-thumb" src="./מוצרים מסווגים/02 — סקיילייט קבוע/חלונות סקיילייט/חלון סקיילייט.png" alt="חלונות סקיילייט" loading="lazy">
      <div class="p-register-name-block">
        <h3 class="p-register-name">חלונות סקיילייט</h3>
        <div class="p-register-en">Skylite Windows</div>
      </div>
      <div class="p-register-tag">חלון. כן. אבל לאור.</div>
      <div class="p-register-arr"><svg viewBox="0 0 24 24"><path d="M19 12H5M11 5l-6 7 6 7"/></svg></div>
    </a>

  </div>"""

# Find the .p-grid block and replace it
import re
grid_pattern = re.compile(r'  <div class="p-grid">\n.*?\n  </div>\n', re.DOTALL)
m = grid_pattern.search(src)
if m:
    if 'p-register-row' in src:
        print("✔  Register HTML — already applied")
    else:
        src = src[:m.start()] + REGISTER_HTML + "\n" + src[m.end():]
        changes += 1
        print(f"✔  Replace .p-grid with Register HTML")
else:
    print("❌ .p-grid block not found")

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
