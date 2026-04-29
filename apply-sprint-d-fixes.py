#!/usr/bin/env python3
"""apply-sprint-d-fixes.py — Three small Sprint D follow-ups.

1. Home projects strip — add "כל הפרויקטים →" link routing to /projects
2. Quiet ribbon — remove the פלטה caption overlay (dark gradient + text)
3. Quiet ribbon — move prev/next arrows from meta row onto the lead image
   (positioned absolute, fade in on hover, RTL-correct)

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
# FIX 1 — Add "see all" link to home projects strip section header
# ═══════════════════════════════════════════════════════════════
swap(
    '<section class="projects" id="projects-strip">\n  <div class="sec-header"><div><div class="sec-label">03 — לקוחות ופרויקטים</div><h2 class="sec-title">עבודות נבחרות</h2></div></div>',
    '<section class="projects" id="projects-strip">\n  <div class="sec-header"><div><div class="sec-label">03 — לקוחות ופרויקטים</div><h2 class="sec-title">עבודות נבחרות</h2></div><a href="#" class="sec-link" onclick="go(\'projects\');return false">כל הפרויקטים →</a></div>',
    "Home projects strip: + 'כל הפרויקטים' link",
)

# ═══════════════════════════════════════════════════════════════
# FIX 2 — Remove פלטה caption overlay from ribbon lead
# ═══════════════════════════════════════════════════════════════

# Remove the lead-cap HTML emission in _renderRibbonMedia
swap(
    '''  out.push(`<div class="pp-ribbon-lead" id="ribbon-lead-${pid}" onclick="_ribbonOpenLb('${pid}','${key}')">
    <img class="pp-ribbon-lead-img" id="ribbon-lead-img-${pid}" src="${firstSrc}" alt="${firstCap || ''}" loading="lazy">
    <div class="pp-ribbon-lead-cap">
      <span class="pp-ribbon-lead-plate" id="ribbon-lead-plate-${pid}">פלטה 01</span>
      <span class="pp-ribbon-lead-text" id="ribbon-lead-text-${pid}">${firstCap || ''}</span>
    </div>
  </div>`);''',
    '''  out.push(`<div class="pp-ribbon-lead" id="ribbon-lead-${pid}">
    <img class="pp-ribbon-lead-img" id="ribbon-lead-img-${pid}" src="${firstSrc}" alt="${firstCap || ''}" loading="lazy" onclick="_ribbonOpenLb('${pid}','${key}')">
    <button class="pp-ribbon-lead-arrow pp-ribbon-lead-arrow--prev" onclick="_ribbonStep('${pid}',-1)" aria-label="הקודם"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M10 12L6 8l4-4"/></svg></button>
    <button class="pp-ribbon-lead-arrow pp-ribbon-lead-arrow--next" onclick="_ribbonStep('${pid}',1)" aria-label="הבא"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M6 12l4-4-4-4"/></svg></button>
  </div>`);''',
    "Ribbon lead: remove caption overlay, add prev/next arrows on image",
)

# ═══════════════════════════════════════════════════════════════
# Update _ribbonSetActive — drop plate/text update (they no longer exist)
# ═══════════════════════════════════════════════════════════════
swap(
    '''  if(plate) plate.textContent = `פלטה ${String(idx+1).padStart(2,'0')}`;
  if(text) text.textContent = cap || '';
  if(counter) counter.textContent''',
    '''  if(counter) counter.textContent''',
    "_ribbonSetActive: drop plate/text update calls",
)

# Also drop the unused getElementById calls for plate/text
swap(
    '''  const plate = document.getElementById('ribbon-lead-plate-'+pid);
  const text = document.getElementById('ribbon-lead-text-'+pid);
  const counter''',
    '''  const counter''',
    "_ribbonSetActive: drop unused plate/text refs",
)

# ═══════════════════════════════════════════════════════════════
# Update meta row — remove the small arrow buttons (lead arrows replace them)
# ═══════════════════════════════════════════════════════════════
swap(
    '''  out.push(`<div class="pp-ribbon-meta">
    <span id="ribbon-counter-${pid}">FIG. 01 / ${String(items.length).padStart(2,'0')}</span>
    <span class="pp-ribbon-meta-arr">
      <button onclick="_ribbonStep('${pid}',-1)" aria-label="הקודם"><svg viewBox="0 0 16 16"><path d="M10 12L6 8l4-4"/></svg></button>
      <button onclick="_ribbonStep('${pid}',1)" aria-label="הבא"><svg viewBox="0 0 16 16"><path d="M6 12l4-4-4-4"/></svg></button>
    </span>
  </div>`);''',
    '''  out.push(`<div class="pp-ribbon-meta">
    <span id="ribbon-counter-${pid}">FIG. 01 / ${String(items.length).padStart(2,'0')}</span>
    <span class="pp-ribbon-meta-hint">לחצו על תמונה להגדלה · השתמשו בחצים לדפדוף</span>
  </div>`);''',
    "Meta row: replace duplicate arrows with hint text",
)

# ═══════════════════════════════════════════════════════════════
# CSS — add lead arrows + adjust meta hint styling
# ═══════════════════════════════════════════════════════════════

LEAD_ARROW_CSS = """
    /* Lead-image arrow controls (Sprint D follow-up) */
    .pp-ribbon-lead-img{cursor:zoom-in}
    .pp-ribbon-lead-arrow{position:absolute;top:50%;transform:translateY(-50%);width:52px;height:52px;border:0;border-radius:50%;background:rgba(26,30,36,.55);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;opacity:0;transition:opacity .3s var(--spring),background .25s var(--spring),transform .3s var(--spring);z-index:5}
    .pp-ribbon-lead-arrow svg{width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:1.6;display:block}
    .pp-ribbon-lead-arrow:hover{background:rgba(26,30,36,.78)}
    .pp-ribbon-lead-arrow:focus-visible{outline:2px solid var(--accent-pale);outline-offset:3px;opacity:1}
    .pp-ribbon-lead:hover .pp-ribbon-lead-arrow{opacity:1}
    .pp-ribbon-lead-arrow--prev{right:18px}
    .pp-ribbon-lead-arrow--next{left:18px}
    .pp-ribbon-lead-arrow--prev:hover{transform:translateY(-50%) translateX(4px)}
    .pp-ribbon-lead-arrow--next:hover{transform:translateY(-50%) translateX(-4px)}
    .pp-ribbon-meta-hint{font-size:11px;font-weight:400;letter-spacing:.04em;color:var(--stone);text-transform:none;font-feature-settings:initial}
    @media(max-width:600px){.pp-ribbon-lead-arrow{width:40px;height:40px;opacity:1}.pp-ribbon-lead-arrow svg{width:14px;height:14px}.pp-ribbon-lead-arrow--prev{right:8px}.pp-ribbon-lead-arrow--next{left:8px}.pp-ribbon-meta-hint{display:none}}
"""

# Insert before the closing of the ribbon CSS block — anchor on .pp-media-grid--ribbon mobile media query
swap(
    "@media(max-width:600px){.pp-media-grid--ribbon{padding:0 24px}.pp-ribbon-lead{aspect-ratio:4/3}",
    LEAD_ARROW_CSS + "\n    @media(max-width:600px){.pp-media-grid--ribbon{padding:0 24px}.pp-ribbon-lead{aspect-ratio:4/3}",
    "Add lead-arrow CSS",
)

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
