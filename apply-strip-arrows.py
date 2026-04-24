#!/usr/bin/env python3
"""apply-strip-arrows.py — Make the home projects strip scroll smoothly + add arrows.

Changes:
  1. Add scroll-snap + scroll-behavior:smooth to .strip
  2. Wrap the strip in a relative container with arrow buttons (prev right, next left — RTL)
  3. Style the arrow buttons (circle, soft shadow, hover)
  4. Hide arrows on mobile (users swipe naturally)
  5. Add JS scrollStrip() function — scrolls by thumb-width + gap, direction-aware for RTL

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
# 1. CSS: scroll-snap on strip, scroll-snap-align on thumbs, arrow styles
# ═══════════════════════════════════════════════════════════════
OLD_STRIP_CSS = ".strip{display:flex;gap:20px;overflow-x:auto;cursor:grab;padding-bottom:16px;scrollbar-width:none;-ms-overflow-style:none;user-select:none}"
NEW_STRIP_CSS = ".strip{display:flex;gap:20px;overflow-x:auto;cursor:grab;padding-bottom:16px;scrollbar-width:none;-ms-overflow-style:none;user-select:none;scroll-snap-type:x mandatory;scroll-behavior:smooth;scroll-padding-inline:24px}"
swap(OLD_STRIP_CSS, NEW_STRIP_CSS, "Strip: scroll-snap + smooth scroll")

OLD_THUMB_CSS = ".thumb{flex-shrink:0;width:340px}"
NEW_THUMB_CSS = ".thumb{flex-shrink:0;width:340px;scroll-snap-align:start}"
swap(OLD_THUMB_CSS, NEW_THUMB_CSS, "Thumb: scroll-snap-align:start")

# Insert arrow styles right after .thumb-type
ARROW_CSS = """
    .strip-wrap{position:relative}
    .strip-arrow{position:absolute;top:calc(50% - 8px);transform:translateY(-50%);width:48px;height:48px;border-radius:50%;background:rgba(255,255,255,.94);box-shadow:0 6px 20px rgba(0,0,0,.14);border:1px solid rgba(28,26,22,.08);cursor:pointer;display:flex;align-items:center;justify-content:center;z-index:5;transition:background .25s var(--spring),transform .25s var(--spring),box-shadow .25s}
    .strip-arrow:hover{background:#fff;transform:translateY(-50%) scale(1.08);box-shadow:0 10px 28px rgba(0,0,0,.18)}
    .strip-arrow:active{transform:translateY(-50%) scale(.96)}
    .strip-arrow svg{width:18px;height:18px;color:var(--dark);stroke-width:2}
    .strip-arrow-next{left:-4px}
    .strip-arrow-prev{right:-4px}
    @media(max-width:768px){.strip-arrow{display:none}}
"""

THUMB_TYPE_CSS = ".thumb-type{font-size:12px;font-weight:300;letter-spacing:.20em;color:var(--stone);text-transform:uppercase}"
if ".strip-arrow{" in src:
    print("✔  Arrow CSS already present")
else:
    src = src.replace(THUMB_TYPE_CSS, THUMB_TYPE_CSS + ARROW_CSS, 1)
    changes += 1
    print("✔  Added arrow button CSS")

# ═══════════════════════════════════════════════════════════════
# 2. HTML: wrap strip in <div class="strip-wrap"> + add arrow buttons
# ═══════════════════════════════════════════════════════════════
OLD_HTML = '''  <div class="strip" id="strip">
    <!-- rendered by renderHomeProjects() -->
    </div>'''
NEW_HTML = '''  <div class="strip-wrap">
    <button class="strip-arrow strip-arrow-next" onclick="scrollStrip(1)" aria-label="הבא">
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M10 12L6 8l4-4"/></svg>
    </button>
    <div class="strip" id="strip">
    <!-- rendered by renderHomeProjects() -->
    </div>
    <button class="strip-arrow strip-arrow-prev" onclick="scrollStrip(-1)" aria-label="הקודם">
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor"><path d="M6 4l4 4-4 4"/></svg>
    </button>
  </div>'''
swap(OLD_HTML, NEW_HTML, "HTML: wrap strip with arrow buttons")

# ═══════════════════════════════════════════════════════════════
# 3. JS: add scrollStrip(dir) function
# ═══════════════════════════════════════════════════════════════
JS_FUNC = """
function scrollStrip(forward){
  const strip = document.getElementById('strip');
  if(!strip) return;
  // thumb width (340) + gap (20) = 360 per step
  const rtl = document.documentElement.dir === 'rtl';
  const step = 360 * (rtl ? -forward : forward);
  strip.scrollBy({ left: step, behavior: 'smooth' });
}
"""

# Anchor: place it near renderHomeProjects
ANCHOR = "function renderHomeProjects(){"
if "function scrollStrip" in src:
    print("✔  scrollStrip() already present")
elif ANCHOR in src:
    src = src.replace(ANCHOR, JS_FUNC.strip() + "\n\n" + ANCHOR, 1)
    changes += 1
    print("✔  Added scrollStrip() function")
else:
    print("❌ renderHomeProjects anchor not found")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
