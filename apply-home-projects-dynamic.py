#!/usr/bin/env python3
"""apply-home-projects-dynamic.py — Home projects strip as dynamic entry point.

Previously the home-page projects strip had 8 hardcoded <div class="thumb">
entries with hand-picked image paths and Hebrew names, some of which didn't
match the PROJECTS data object (different names, duplicates like two National
Library tiles, and non-project entries like "חצר פנימית — גג נוסע").

None of them linked to the project detail pages — a dead-end strip.

This change:
  1. Replace the 8 hardcoded tiles with an empty <div class="strip" id="strip">
  2. Add HOME_STRIP array — curated slugs + type labels (8 diverse projects)
  3. Add renderHomeProjects() that reads from PROJECTS and renders clickable
     tiles calling goProject(slug) — same routing as product pages use.
  4. Call renderHomeProjects() at init.

Selected projects (diverse across product lines + building types):
  • national-library       — walkon / ציבורי
  • recanati-winery        — structural / מסחרי
  • mitzpe-hayamim         — fixed / מלונאות
  • hp-hq                  — walkon / מסחרי
  • beit-habeer            — walkon / ציבורי
  • penthouse-ben-yehuda   — penthouse / מגורים
  • beit-gil-hazahav       — fixed / מגורים
  • synagogue              — structural / ציבורי

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

# ═══════════════════════════════════════════════════════════════
# 1. Replace the 8 hardcoded tiles with an empty render target.
# We match the whole <div class="strip"...> block replacing all tiles at once.
# ═══════════════════════════════════════════════════════════════
STRIP_START = '<div class="strip" id="strip">'
STRIP_END = '</div>\n</section>\n\n<section class="process">'

# Find the strip start
i = src.find(STRIP_START)
if i == -1:
    print("❌ home strip opening not found")
    sys.exit(1)

# Find strip close — looking for the closing </div></section> of projects
search_from = i + len(STRIP_START)
j = src.find("  </div>\n</section>\n\n<section class=\"process\"", search_from)
if j == -1:
    # Try alternate nearby patterns
    j = src.find("</div>\n</section>\n\n<section class=\"process\"", search_from)
if j == -1:
    print("❌ home strip closing not found near </section><section process>")
    sys.exit(1)

# Replace contents between STRIP_START and the closing </div>
current_inner = src[i + len(STRIP_START):j]
# Idempotency: if it's already empty or just whitespace, skip
if current_inner.strip() == "":
    print("✔  Home strip already emptied")
else:
    # Replace with just a newline + closing indent match
    new_block = STRIP_START + "\n    <!-- rendered by renderHomeProjects() -->\n  "
    src = src[:i] + new_block + src[j:]
    changes += 1
    thumb_marker = 'class="thumb'
    n_tiles = current_inner.count(thumb_marker)
    print(f"✔  Home strip: cleared {n_tiles} hardcoded tiles")

# ═══════════════════════════════════════════════════════════════
# 2. Add HOME_STRIP data + renderHomeProjects() function
# Insert alongside other render functions — after renderProjectGallery or
# before the init forEach lines.
# ═══════════════════════════════════════════════════════════════
RENDER_FN_BLOCK = """
// Home-page projects strip — curated subset of PROJECTS as clickable entry
// points to the project detail pages.
const HOME_STRIP = [
  { slug:'national-library',     type:'ציבורי' },
  { slug:'recanati-winery',      type:'מסחרי' },
  { slug:'mitzpe-hayamim',       type:'מלונאות' },
  { slug:'hp-hq',                type:'מסחרי' },
  { slug:'beit-habeer',          type:'ציבורי' },
  { slug:'penthouse-ben-yehuda', type:'מגורים' },
  { slug:'beit-gil-hazahav',     type:'מגורים' },
  { slug:'synagogue',            type:'ציבורי' },
];

function renderHomeProjects(){
  const strip = document.getElementById('strip');
  if(!strip) return;
  const tiles = HOME_STRIP.map((h, i) => {
    // Locate this project in the PROJECTS object
    let proj = null;
    for(const pid of Object.keys(PROJECTS)){
      proj = PROJECTS[pid].find(p => p.slug === h.slug);
      if(proj) break;
    }
    if(!proj) return '';  // silently skip missing projects
    const delayClass = i > 0 ? ' rv-d' + Math.min(i, 3) : '';
    return `<div class="thumb rv${delayClass}" onclick="goProject('${h.slug}')" style="cursor:pointer">`
      + `<div class="thumb-wrap"><img class="thumb-img" src="${B}${proj.hero}" alt="${proj.name}" loading="lazy"></div>`
      + `<div class="thumb-meta"><span class="thumb-name">${proj.name}</span><span class="thumb-type">${h.type}</span></div>`
      + `</div>`;
  }).filter(Boolean).join('');
  strip.innerHTML = tiles;
}
"""

# Anchor — insert right before the forEach(renderMedia) init line
INIT_ANCHOR = "['walkon','penthouse','fixed','retractable','structural','smoke'].forEach(renderMedia);"
if "function renderHomeProjects" in src:
    print("✔  renderHomeProjects — already present")
elif INIT_ANCHOR in src:
    src = src.replace(INIT_ANCHOR, RENDER_FN_BLOCK.strip() + "\n" + INIT_ANCHOR, 1)
    changes += 1
    print("✔  Added HOME_STRIP + renderHomeProjects()")
else:
    print("❌ init anchor not found; aborting")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════
# 3. Call renderHomeProjects() at init
# ═══════════════════════════════════════════════════════════════
swap(
    "['walkon','penthouse','fixed','retractable','structural','smoke'].forEach(renderMedia);",
    "['walkon','penthouse','fixed','retractable','structural','smoke'].forEach(renderMedia);\nrenderHomeProjects();",
    "Init: call renderHomeProjects()"
)

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
