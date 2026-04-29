#!/usr/bin/env python3
"""apply-sprint-d2-mosaic.py — V1 Atelier mosaic project strip on home.

Replaces home page horizontal-scroll project carousel with V1's 12-col mosaic:
  • 1 LG (span 7, 540px tall) — hero project (National Library)
  • 1 MD (span 5, 540px tall) — second prestige
  • 3 SM (span 4, 360px tall each) — supporting cast

No carousel state, no arrows, no scrolling JS. Static layout, magazine-cover feel.

Curated home projects: National Library, HP HQ, Mitzpe Hayamim, Recanati, Ben Yehuda.

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
# 1) CSS — mosaic project strip
# ═══════════════════════════════════════════════════════════════
MOSAIC_CSS = """
    /* ── HOME PROJECT MOSAIC (Sprint D-2, V1 Atelier) ── */
    .home-pmosaic{display:grid;grid-template-columns:repeat(12,1fr);gap:4px;direction:rtl}
    .home-pmosaic-card{position:relative;overflow:hidden;cursor:pointer;display:block;text-decoration:none;color:inherit}
    .home-pmosaic-card img{width:100%;height:100%;object-fit:cover;transition:transform 1.4s var(--spring),filter 1s var(--spring);filter:brightness(.94) saturate(1.04)}
    .home-pmosaic-card:hover img{transform:scale(1.04);filter:brightness(1) saturate(1.1)}
    .home-pmosaic-card--lg{grid-column:span 7;height:540px}
    .home-pmosaic-card--md{grid-column:span 5;height:540px}
    .home-pmosaic-card--sm{grid-column:span 4;height:360px}
    .home-pmosaic-cap{position:absolute;left:0;right:0;bottom:0;padding:28px 30px 24px;background:linear-gradient(180deg,transparent 30%,rgba(0,0,0,.78) 100%);color:#fff;direction:rtl;pointer-events:none}
    .home-pmosaic-name{font-weight:700;font-size:24px;letter-spacing:-.005em;line-height:1.15;margin:0}
    .home-pmosaic-card--lg .home-pmosaic-name{font-size:28px}
    .home-pmosaic-loc{font-size:11px;font-weight:500;letter-spacing:.26em;text-transform:uppercase;opacity:.82;margin-top:6px}
    .home-pmosaic-card:focus-visible{outline:3px solid var(--accent);outline-offset:-3px}
    @media(max-width:1024px){.home-pmosaic{grid-template-columns:repeat(6,1fr)}.home-pmosaic-card--lg,.home-pmosaic-card--md,.home-pmosaic-card--sm{grid-column:span 6;height:360px}.home-pmosaic-card--lg{height:440px}}
    @media(max-width:600px){.home-pmosaic-card--lg{height:320px}.home-pmosaic-card--md,.home-pmosaic-card--sm{height:260px}.home-pmosaic-name{font-size:20px}.home-pmosaic-card--lg .home-pmosaic-name{font-size:22px}}
"""

swap(
    "    /* ── HOME REGISTER",
    MOSAIC_CSS + "\n    /* ── HOME REGISTER",
    "Insert mosaic CSS",
)

# ═══════════════════════════════════════════════════════════════
# 2) Replace strip-wrap with home-pmosaic
# ═══════════════════════════════════════════════════════════════
OLD_STRIP = '''  <div class="strip-wrap">
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

NEW_MOSAIC = '''  <div class="home-pmosaic" id="home-pmosaic">
    <!-- rendered by renderHomeProjects() -->
  </div>'''

swap(OLD_STRIP, NEW_MOSAIC, "Replace strip-wrap with home-pmosaic")

# ═══════════════════════════════════════════════════════════════
# 3) Update HOME_STRIP order + slot mapping (LG / MD / SM×3)
# ═══════════════════════════════════════════════════════════════
OLD_HOME_STRIP = '''const HOME_STRIP = [
  { slug:'national-library',     type:'ציבורי' },
  { slug:'recanati-winery',      type:'מסחרי' },
  { slug:'mitzpe-hayamim',       type:'מלונאות' },
  { slug:'hp-hq',                type:'מסחרי' },
  { slug:'beit-habeer',          type:'ציבורי' },
  { slug:'penthouse-ben-yehuda', type:'מגורים' },
  { slug:'beit-gil-hazahav',     type:'מגורים' },
  { slug:'synagogue',            type:'ציבורי' },
];'''

NEW_HOME_STRIP = '''const HOME_STRIP = [
  // V1 mosaic slots: LG=span7×540, MD=span5×540, SM=span4×360
  { slug:'national-library',     type:'ציבורי',  slot:'lg' },
  { slug:'hp-hq',                type:'מסחרי',   slot:'md' },
  { slug:'mitzpe-hayamim',       type:'מלונאות', slot:'sm' },
  { slug:'recanati-winery',      type:'מסחרי',   slot:'sm' },
  { slug:'penthouse-ben-yehuda', type:'מגורים',  slot:'sm' },
];'''

swap(OLD_HOME_STRIP, NEW_HOME_STRIP, "HOME_STRIP: 8 carousel → 5 mosaic slots")

# ═══════════════════════════════════════════════════════════════
# 4) Rewrite renderHomeProjects to emit mosaic HTML
# ═══════════════════════════════════════════════════════════════
OLD_RENDER = '''function renderHomeProjects(){
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
}'''

NEW_RENDER = '''function renderHomeProjects(){
  const host = document.getElementById('home-pmosaic');
  if(!host) return;
  const tiles = HOME_STRIP.map((h, i) => {
    let proj = null;
    for(const pid of Object.keys(PROJECTS)){
      proj = PROJECTS[pid].find(p => p.slug === h.slug);
      if(proj) break;
    }
    if(!proj) return '';
    const delayClass = i > 0 ? ' rv-d' + Math.min(i, 3) : '';
    const slotClass = h.slot ? ` home-pmosaic-card--${h.slot}` : ' home-pmosaic-card--sm';
    const where = (proj.meta && proj.meta.where && proj.meta.where !== '—') ? proj.meta.where : '';
    const year = (proj.meta && proj.meta.when && proj.meta.when !== '—') ? proj.meta.when : '';
    const locline = [where, year].filter(Boolean).join(' · ').toUpperCase();
    return `<a class="home-pmosaic-card${slotClass} rv${delayClass}" href="#project/${h.slug}" onclick="goProject('${h.slug}');return false">`
      + `<img src="${B}${proj.hero}" alt="${proj.name}" loading="lazy">`
      + `<div class="home-pmosaic-cap"><h3 class="home-pmosaic-name">${proj.name}</h3>${locline ? `<div class="home-pmosaic-loc">${locline}</div>` : ''}</div>`
      + `</a>`;
  }).filter(Boolean).join('');
  host.innerHTML = tiles;
}'''

swap(OLD_RENDER, NEW_RENDER, "renderHomeProjects: emit mosaic HTML")

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
