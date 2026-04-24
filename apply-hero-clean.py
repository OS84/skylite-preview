#!/usr/bin/env python3
"""apply-hero-clean.py — Remove placeholder-looking treatment from home hero.

Drops:
  1. .hero-grid overlay (80x80 grid lines that gave a "wireframe placeholder" feel)
  2. .hero-img aggressive filter (.88 brightness dimmed the photo); soften to
     brightness(.96) for subtle atmospheric effect without looking processed.

Keeps:
  - .hero-ov gradient (required for nav + text contrast over photography)
  - .hero-beam / .hero-beam2 (subtle light-ray atmospherics; not placeholder-y)
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

# 1. Remove grid overlay from HTML
swap(
    '<div class="hero-grid"></div>\n',
    '',
    "HTML: remove <div class=\"hero-grid\">"
)

# 2. Neutralize the grid CSS (keep rule present but collapse to nothing, in
#    case any other hero inherits it later)
swap(
    '.hero-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);background-size:80px 80px;z-index:1}',
    '.hero-grid{display:none}',
    "CSS: .hero-grid → display:none"
)

# 3. Soften the hero-img filter
swap(
    '.hero-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.88) saturate(1.06) contrast(1.04);z-index:0;will-change:transform}',
    '.hero-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.96) saturate(1.03);z-index:0;will-change:transform}',
    "CSS: .hero-img filter softened (.88→.96, drop contrast boost)"
)

if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
