#!/usr/bin/env python3
"""apply-a11y-fixes.py — Phase 3: WCAG 2.1 AA fixes for fixed pilot + adjacent.

Addresses the audit's P0 blockers and P1 must-fixes that affect the path
to the fixed page. Defers P1#8 heading hierarchy + P2 polish to a later
pass — they aren't pilot-blocking.

What this ships
===============
P0 — Blockers:
  • #3 :focus-within on .pp-proj-tile metadata (keyboard nav reveals meta)
  • #1 .p-card keyboard accessibility (tabindex + role + keydown handler)
  • #2 Form placeholder contrast (#545E69 → #404A55, weight 300 → 400)

P1 — Must-fix:
  • #4 Strip arrows 40×40 → 44×44 on mobile (touch target)
  • #5 Visible focus outlines on .pp-proj-tile, form inputs, lightbox video
  • #6 Gallery alt text via caption/filename hint (renderMedia + renderProjectGallery)
  • #7 Hero alt text on all product pages (was empty on #fixed)

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
# P0#3 + P1#5 — :focus-within for hover-tile metadata + focus outline
# ═══════════════════════════════════════════════════════════════
swap(
    ".pp-proj-tile:hover .pp-proj-tile-extra{max-height:140px;opacity:1;margin-top:14px}",
    ".pp-proj-tile:hover .pp-proj-tile-extra,.pp-proj-tile:focus-within .pp-proj-tile-extra{max-height:140px;opacity:1;margin-top:14px}",
    "P0#3 :focus-within reveals tile metadata",
)
swap(
    ".pp-proj-tile:hover .pp-proj-tile-arrow{opacity:1;transform:scale(1)}",
    ".pp-proj-tile:hover .pp-proj-tile-arrow,.pp-proj-tile:focus-within .pp-proj-tile-arrow{opacity:1;transform:scale(1)}\n    .pp-proj-tile:focus-visible{outline:3px solid var(--accent);outline-offset:3px}",
    "P0#3 + P1#5 :focus-within arrow + focus-visible outline",
)

# ═══════════════════════════════════════════════════════════════
# P0#2 — Form placeholder contrast (find and fix)
# ═══════════════════════════════════════════════════════════════
import re
# Locate placeholder rule(s) in CSS
placeholder_count = src.count('::placeholder')
print(f"   (info: {placeholder_count} ::placeholder rule(s) found)")
# Common pattern in this file
swap(
    ".cm-input::placeholder,.cm-textarea::placeholder{color:var(--stone);font-weight:300}",
    ".cm-input::placeholder,.cm-textarea::placeholder{color:#404A55;font-weight:400;opacity:.85}",
    "P0#2 form placeholder contrast (#545E69 → #404A55, weight 300 → 400)",
    must_exist=False,
)

# ═══════════════════════════════════════════════════════════════
# P1#4 — Strip arrows 40×40 → 44×44 on mobile (touch target ≥44px)
# ═══════════════════════════════════════════════════════════════
swap(
    "@media(max-width:768px){.strip-arrow{width:40px;height:40px}.strip-arrow svg{width:15px;height:15px}.strip-arrow-next{left:4px}.strip-arrow-prev{right:4px}}",
    "@media(max-width:768px){.strip-arrow{width:44px;height:44px}.strip-arrow svg{width:16px;height:16px}.strip-arrow-next{left:4px}.strip-arrow-prev{right:4px}}",
    "P1#4 strip arrows 40px → 44px (touch target)",
    must_exist=False,
)

# ═══════════════════════════════════════════════════════════════
# P1#5 — Focus outlines on form inputs + lightbox video
# ═══════════════════════════════════════════════════════════════
# We add a global focus-visible rule rather than chasing every input.
# Insert before the closing </style> tag of the main inline stylesheet.
A11Y_FOCUS_BLOCK = """
    /* ── A11Y: visible focus indicators on all interactive elements ── */
    a:focus-visible,button:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible,
    .p-card:focus-visible,.pp-media-item:focus-visible,.pp-proj-tile:focus-visible{
      outline:3px solid var(--accent);outline-offset:3px;
    }
    .nav-cta:focus-visible{outline-offset:6px}
"""

if "/* ── A11Y: visible focus indicators" in src:
    print("✔  P1#5 a11y focus block — already present")
else:
    # Insert just before the closing of the main stylesheet — find a stable anchor
    css_anchor = "    /* ── MOSAIC variant"
    if css_anchor in src:
        src = src.replace(css_anchor, A11Y_FOCUS_BLOCK + "\n" + css_anchor, 1)
        changes += 1
        print("✔  P1#5 a11y focus block inserted")
    else:
        print("⚠  P1#5 anchor for a11y block not found")

# ═══════════════════════════════════════════════════════════════
# P0#1 — .p-card keyboard accessibility (tabindex + role + keydown)
# ═══════════════════════════════════════════════════════════════
# Inject a small JS init that runs on load and decorates all .p-card / clickable divs
A11Y_KEYBOARD_INIT = """
// A11Y: make clickable divs keyboard-accessible (.p-card, .pp-media-item)
function _a11yMakeKeyboardable(){
  document.querySelectorAll('.p-card, .pp-media-item').forEach(el => {
    if(el.hasAttribute('data-a11y-init')) return;
    el.setAttribute('tabindex', '0');
    el.setAttribute('role', el.classList.contains('p-card') ? 'link' : 'button');
    el.addEventListener('keydown', e => {
      if(e.key === 'Enter' || e.key === ' '){
        e.preventDefault();
        el.click();
      }
    });
    el.setAttribute('data-a11y-init', '1');
  });
}
"""

# Place before "Init" comment
swap(
    "// Sanity: every project must have at least 1 category, else it won't render anywhere",
    A11Y_KEYBOARD_INIT + "\n// Sanity: every project must have at least 1 category, else it won't render anywhere",
    "P0#1 _a11yMakeKeyboardable() helper",
    must_exist=False,
)

# Hook the helper into init — call it after rendering completes
swap(
    "['penthouse','fixed','walkon','structural'].forEach(renderProjectsSection);",
    "['penthouse','fixed','walkon','structural'].forEach(renderProjectsSection);\n_a11yMakeKeyboardable();",
    "P0#1 call _a11yMakeKeyboardable on init",
    must_exist=False,
)

# Also hook after MEDIA renders (gallery tiles get the role/tabindex)
# renderMedia is called per page — it appends .pp-media-item children. Re-run keyboard helper.
swap(
    "function renderMedia(pid){",
    "function _runA11yAfterRender(){ if(typeof _a11yMakeKeyboardable === 'function') _a11yMakeKeyboardable(); }\nfunction renderMedia(pid){",
    "P0#1 _runA11yAfterRender helper",
    must_exist=False,
)
swap(
    "  sec.innerHTML = out.join('');\n}\n\n// Auto-derive overlay caption from image path.",
    "  sec.innerHTML = out.join('');\n  _runA11yAfterRender();\n}\n\n// Auto-derive overlay caption from image path.",
    "P0#1 call _runA11yAfterRender after renderMedia",
    must_exist=False,
)

# ═══════════════════════════════════════════════════════════════
# P1#6 — Gallery alt text via caption / filename hint
# ═══════════════════════════════════════════════════════════════
# In renderMedia, the img tag uses alt="" — switch to use the cap or filename-hint
swap(
    """      out.push(`<div class="pp-media-item" onclick="openLb('${key}',${i})"><img src="${B}${it.src}" alt="" loading="lazy">${capHtml}</div>`);""",
    """      const altText = cap || _filenameHint(it.src) || 'סקיילייט — תמונת מוצר';
      out.push(`<div class="pp-media-item${ac}" onclick="openLb('${key}',${i})"><img src="${B}${it.src}" alt="${altText}" loading="lazy">${capHtml}</div>`);""",
    "P1#6 gallery image alt text from caption/filename",
    must_exist=False,
)

# Patch the project gallery render too
swap(
    "  const tiles = proj.images.map((src,i) => {\n    return `<div class=\"pp-media-item\" onclick=\"openLb('${key}',${i})\"><img src=\"${B}${src}\" alt=\"\" loading=\"lazy\"></div>`;\n  }).join('');",
    "  const tiles = proj.images.map((src,i) => {\n    const altText = _filenameHint(src) || `${proj.name} — תמונה ${i+1}`;\n    return `<div class=\"pp-media-item\" onclick=\"openLb('${key}',${i})\"><img src=\"${B}${src}\" alt=\"${altText}\" loading=\"lazy\"></div>`;\n  }).join('');",
    "P1#6 project gallery alt text",
    must_exist=False,
)

# ═══════════════════════════════════════════════════════════════
# P1#7 — Hero alt text on product pages (find + fix all empty hero alts)
# ═══════════════════════════════════════════════════════════════
HERO_FIXES = [
    ('alt=""><div class="pp-hero-ov"></div><div class="pp-hero-c"><div class="pp-hero-cat">02 — Fixed Skylights',
     'alt="סקיילייט קבוע — חד-שיפועי על גג שטוח"><div class="pp-hero-ov"></div><div class="pp-hero-c"><div class="pp-hero-cat">02 — Fixed Skylights',
     "P1#7 fixed hero alt text"),
    ('alt=""><div class="pp-hero-ov"></div><div class="pp-hero-c"><div class="pp-hero-cat">06 — Roof Access',
     'alt="פנטהאוז עם יציאה לגג נפתחת"><div class="pp-hero-ov"></div><div class="pp-hero-c"><div class="pp-hero-cat">06 — Roof Access',
     "P1#7 penthouse hero alt text"),
]
for old, new, label in HERO_FIXES:
    swap(old, new, label, must_exist=False)

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
