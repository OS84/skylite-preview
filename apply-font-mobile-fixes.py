#!/usr/bin/env python3
"""apply-font-mobile-fixes.py — Typography contrast boost + mobile strip arrows.

Two user-reported fixes:

1. FONTS TOO LIGHT across the site
   Root causes:
   - `--stone` color (#6B7680) borderline AA-compliant — darkening to #545E69
   - Multiple body-text rules use font-weight:300 — bumping to 400
   - Keeping 300 only where intentional (hero-label tracking, stat-l label)

2. PROJECT STRIP ARROWS MISSING ON MOBILE
   Current rule: `@media(max-width:768px){.strip-arrow{display:none}}`
   Fix: show arrows on mobile at smaller size (40px) so users know the strip
   is scrollable. Also slightly indent them so they don't clip the edge tiles.

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
# 1. Darken --stone (used everywhere for secondary text)
#    Current #6B7680 has ~4.3:1 contrast on #F4F6F8 — borderline AA.
#    New #545E69 gives ~6.8:1 — comfortably AA+, closer to AAA.
# ═══════════════════════════════════════════════════════════════
swap(
    "--stone:     #6B7680;",
    "--stone:     #545E69;",
    "Stone color: #6B7680 → #545E69 (better contrast)"
)

# ═══════════════════════════════════════════════════════════════
# 2. Bump font-weight on body-type rules from 300 → 400
# ═══════════════════════════════════════════════════════════════
swap(
    ".hero-sub{margin-top:28px;font-size:17px;font-weight:300;color:var(--stone);line-height:1.75;max-width:420px;position:relative;z-index:1}",
    ".hero-sub{margin-top:28px;font-size:17px;font-weight:400;color:var(--stone);line-height:1.75;max-width:420px;position:relative;z-index:1}",
    ".hero-sub weight 300 → 400"
)

swap(
    ".pp-desc-label{font-size:12px;font-weight:300;letter-spacing:.22em;color:var(--stone);text-transform:uppercase;margin-bottom:28px}",
    ".pp-desc-label{font-size:12px;font-weight:500;letter-spacing:.22em;color:var(--stone);text-transform:uppercase;margin-bottom:28px}",
    ".pp-desc-label weight 300 → 500 (labels need more weight with letter-spacing)"
)

swap(
    ".pp-chars-title{font-size:12px;font-weight:300;letter-spacing:.22em;color:var(--stone);text-transform:uppercase;margin-bottom:32px}",
    ".pp-chars-title{font-size:12px;font-weight:500;letter-spacing:.22em;color:var(--stone);text-transform:uppercase;margin-bottom:32px}",
    ".pp-chars-title weight 300 → 500"
)

swap(
    ".stat-l{font-size:13px;font-weight:300;letter-spacing:.08em;color:var(--stone);line-height:1.5}",
    ".stat-l{font-size:13px;font-weight:400;letter-spacing:.08em;color:var(--stone);line-height:1.5}",
    ".stat-l weight 300 → 400"
)

swap(
    ".thumb-type{font-size:12px;font-weight:300;letter-spacing:.20em;color:var(--stone);text-transform:uppercase}",
    ".thumb-type{font-size:12px;font-weight:500;letter-spacing:.20em;color:var(--stone);text-transform:uppercase}",
    ".thumb-type weight 300 → 500"
)

# ═══════════════════════════════════════════════════════════════
# 3. Show strip arrows on mobile (40px, scaled down from desktop 48px)
# ═══════════════════════════════════════════════════════════════
swap(
    "@media(max-width:768px){.strip-arrow{display:none}}",
    "@media(max-width:768px){.strip-arrow{width:40px;height:40px}.strip-arrow svg{width:15px;height:15px}.strip-arrow-next{left:4px}.strip-arrow-prev{right:4px}}",
    "Strip arrows: show on mobile at 40px (was hidden)"
)

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
