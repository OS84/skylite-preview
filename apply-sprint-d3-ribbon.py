#!/usr/bin/env python3
"""apply-sprint-d3-ribbon.py — Quiet Ribbon gallery (Claude Design V1 Atelier).

Replaces the mosaic gallery with: one large lead image + a horizontal
ribbon of small thumbnails. Click a thumb to swap the lead. Includes a
plate caption ("פלטה 03 — מצפה הימים") and a figure counter ("FIG. 03 / 06").

Why this lands well
==================
• Solves the "different categories have different image counts" problem —
  layout is identical for 3 images or 30
• Photography-led — the lead is huge, ribbon is supporting cast
• Drawing-set typography (PLATE / FIG. counter) reinforces architectural brand
• Mobile: aspect collapses to 4:3, ribbon scrolls horizontally, thumbs shrink

Adopted on: fixed, structural, penthouse, retractable, smoke (all the
pilot categories with curated MEDIA arrays). Windows kept as default
(only 6 product variation shots, doesn't need ribbon mechanics).

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
# 1) CSS — quiet ribbon variant
# ═══════════════════════════════════════════════════════════════
RIBBON_CSS = """
    /* ── QUIET RIBBON GALLERY (Sprint D-3, V1 Atelier) ── */
    .pp-media-grid--ribbon{display:flex;flex-direction:column;gap:0;padding:0 80px}
    .pp-ribbon-lead{position:relative;width:100%;aspect-ratio:16/9;overflow:hidden;background:var(--dark);cursor:pointer}
    .pp-ribbon-lead-img{width:100%;height:100%;object-fit:cover;transition:opacity .45s var(--spring)}
    .pp-ribbon-lead-img.fading{opacity:.0}
    .pp-ribbon-lead-cap{position:absolute;left:0;right:0;bottom:0;padding:32px 36px 28px;background:linear-gradient(180deg,transparent 30%,rgba(0,0,0,.72) 100%);color:#fff;direction:rtl;display:flex;align-items:baseline;gap:24px;flex-wrap:wrap;pointer-events:none}
    .pp-ribbon-lead-plate{font-size:11px;font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:var(--accent-pale);font-feature-settings:'tnum';flex:0 0 auto}
    .pp-ribbon-lead-text{font-size:15px;font-weight:400;letter-spacing:.02em;line-height:1.5;flex:1;min-width:200px;color:rgba(255,255,255,.94)}
    .pp-ribbon-strip{display:flex;gap:8px;margin-top:14px;overflow-x:auto;padding:4px 2px;scrollbar-width:thin;scrollbar-color:var(--warm-gray) transparent;direction:rtl}
    .pp-ribbon-strip::-webkit-scrollbar{height:6px}
    .pp-ribbon-strip::-webkit-scrollbar-track{background:transparent}
    .pp-ribbon-strip::-webkit-scrollbar-thumb{background:var(--warm-gray);border-radius:3px}
    .pp-ribbon-thumb{flex:0 0 auto;width:120px;height:78px;position:relative;overflow:hidden;cursor:pointer;background:var(--dark);opacity:.55;transition:opacity .25s var(--spring),transform .25s var(--spring);outline:0;border:0;padding:0}
    .pp-ribbon-thumb:hover{opacity:.85}
    .pp-ribbon-thumb.active{opacity:1;box-shadow:inset 0 0 0 2px var(--accent)}
    .pp-ribbon-thumb img{width:100%;height:100%;object-fit:cover;display:block}
    .pp-ribbon-thumb .mp-play-tiny{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:24px;height:24px;pointer-events:none}
    .pp-ribbon-thumb:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
    .pp-ribbon-meta{display:flex;justify-content:space-between;align-items:center;margin-top:14px;font-size:11px;font-weight:400;letter-spacing:.22em;color:var(--stone);text-transform:uppercase;font-feature-settings:'tnum';direction:rtl}
    .pp-ribbon-meta-arr{display:flex;gap:8px}
    .pp-ribbon-meta-arr button{width:32px;height:32px;border:1px solid var(--warm-gray);background:transparent;cursor:pointer;display:flex;align-items:center;justify-content:center;color:var(--dark);transition:border-color .25s var(--spring),background .25s var(--spring)}
    .pp-ribbon-meta-arr button:hover{border-color:var(--accent);background:rgba(43,122,140,.05)}
    .pp-ribbon-meta-arr button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
    .pp-ribbon-meta-arr svg{width:12px;height:12px;stroke:currentColor;fill:none;stroke-width:1.5}
    @media(max-width:1024px){.pp-media-grid--ribbon{padding:0 48px}}
    @media(max-width:600px){.pp-media-grid--ribbon{padding:0 24px}.pp-ribbon-lead{aspect-ratio:4/3}.pp-ribbon-lead-cap{padding:20px 22px 18px;gap:12px}.pp-ribbon-lead-text{font-size:13px}.pp-ribbon-thumb{width:88px;height:58px}}
"""

# Insert before "MOSAIC variant" comment
swap(
    "    /* ── MOSAIC variant",
    RIBBON_CSS + "\n    /* ── MOSAIC variant",
    "Insert quiet-ribbon CSS",
)

# ═══════════════════════════════════════════════════════════════
# 2) Update MEDIA_LAYOUT — switch all pilot categories to 'ribbon'
# ═══════════════════════════════════════════════════════════════
swap(
    "const MEDIA_LAYOUT = { fixed: 'mosaic', structural: 'mosaic', penthouse: 'mosaic', retractable: 'mosaic', smoke: 'mosaic' };",
    "const MEDIA_LAYOUT = { fixed: 'ribbon', structural: 'ribbon', penthouse: 'ribbon', retractable: 'ribbon', smoke: 'ribbon' };",
    "MEDIA_LAYOUT: mosaic → ribbon (all pilot categories)",
)

# ═══════════════════════════════════════════════════════════════
# 3) Rewrite renderMedia to branch on ribbon layout
# ═══════════════════════════════════════════════════════════════
OLD_RENDER = """function renderMedia(pid){
  const sec = document.getElementById('media-'+pid);
  if(!sec) return;
  const items = MEDIA[pid];
  if(!items || !items.length){ sec.style.display='none'; return; }
  const key = 'media-'+pid;
  const srcs  = items.map(it => it.type === 'vid' ? (it.vidbase==='img' ? B : VB)+it.src : B+it.src);
  const caps  = items.map(_effCap);
  const kinds = items.map(it => it.type === 'vid' ? 'vid' : 'img');
  _galReg[key] = { srcs, caps, kinds };

  const layout = MEDIA_LAYOUT[pid] || '';
  const gridClass = layout === 'mosaic' ? 'pp-media-grid pp-media-grid--mosaic' : 'pp-media-grid';
  const aspectClass = it => {
    if(layout !== 'mosaic') return '';
    if(it.aspect === 'wide') return ' tile-w';
    if(it.aspect === 'tall') return ' tile-t';
    return '';
  };"""

NEW_RENDER = """function renderMedia(pid){
  const sec = document.getElementById('media-'+pid);
  if(!sec) return;
  const items = MEDIA[pid];
  if(!items || !items.length){ sec.style.display='none'; return; }
  const key = 'media-'+pid;
  const srcs  = items.map(it => it.type === 'vid' ? (it.vidbase==='img' ? B : VB)+it.src : B+it.src);
  const caps  = items.map(_effCap);
  const kinds = items.map(it => it.type === 'vid' ? 'vid' : 'img');
  _galReg[key] = { srcs, caps, kinds };

  const layout = MEDIA_LAYOUT[pid] || '';
  // Ribbon variant — early return: one lead + thumbnail strip
  if(layout === 'ribbon') return _renderRibbonMedia(pid, items, key, sec);

  const gridClass = layout === 'mosaic' ? 'pp-media-grid pp-media-grid--mosaic' : 'pp-media-grid';
  const aspectClass = it => {
    if(layout !== 'mosaic') return '';
    if(it.aspect === 'wide') return ' tile-w';
    if(it.aspect === 'tall') return ' tile-t';
    return '';
  };"""

swap(OLD_RENDER, NEW_RENDER, "renderMedia: branch on ribbon layout")

# ═══════════════════════════════════════════════════════════════
# 4) Add _renderRibbonMedia helper + state setter
# ═══════════════════════════════════════════════════════════════
RIBBON_JS = """
// ─── QUIET RIBBON RENDERER (Sprint D-3) ───────────────────────
const _ribbonState = {};  // { pid: activeIdx }

function _renderRibbonMedia(pid, items, key, sec){
  _ribbonState[pid] = 0;
  const hdr = MEDIA_HEADERS[pid] || { eye: 'גלריה', title: 'עבודות נבחרות' };
  const playIcon = '<svg class="mp-play-tiny" viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="rgba(0,0,0,.55)"/><path d="M9 7l8 5-8 5z" fill="#fff"/></svg>';
  const out = [`<div class="pp-media-h"><div class="pp-projects-section-eye">${hdr.eye}</div><h2 class="pp-projects-section-t">${hdr.title}</h2></div>`];
  out.push('<div class="pp-media-grid pp-media-grid--ribbon">');

  // Lead — first item
  const first = items[0];
  const firstCap = _effCap(first);
  const firstSrc = first.type === 'vid' ? (first.poster ? (first.vidbase==='img' ? B : VB)+first.poster : '') : B + first.src;
  out.push(`<div class="pp-ribbon-lead" id="ribbon-lead-${pid}" onclick="_ribbonOpenLb('${pid}','${key}')">
    <img class="pp-ribbon-lead-img" id="ribbon-lead-img-${pid}" src="${firstSrc}" alt="${firstCap || ''}" loading="lazy">
    <div class="pp-ribbon-lead-cap">
      <span class="pp-ribbon-lead-plate" id="ribbon-lead-plate-${pid}">פלטה 01</span>
      <span class="pp-ribbon-lead-text" id="ribbon-lead-text-${pid}">${firstCap || ''}</span>
    </div>
  </div>`);

  // Strip
  out.push('<div class="pp-ribbon-strip" id="ribbon-strip-'+pid+'">');
  items.forEach((it,i) => {
    const isVid = it.type === 'vid';
    const thumbSrc = isVid ? (it.poster ? (it.vidbase==='img' ? B : VB)+it.poster : B + it.src) : B + it.src;
    const cap = _effCap(it);
    out.push(`<button class="pp-ribbon-thumb${i===0?' active':''}" data-idx="${i}" onclick="_ribbonSetActive('${pid}',${i})" aria-label="תמונה ${i+1}"><img src="${thumbSrc}" alt="${cap || ''}" loading="lazy">${isVid ? playIcon : ''}</button>`);
  });
  out.push('</div>');

  // Counter + arrow controls
  out.push(`<div class="pp-ribbon-meta">
    <span id="ribbon-counter-${pid}">FIG. 01 / ${String(items.length).padStart(2,'0')}</span>
    <span class="pp-ribbon-meta-arr">
      <button onclick="_ribbonStep('${pid}',-1)" aria-label="הקודם"><svg viewBox="0 0 16 16"><path d="M10 12L6 8l4-4"/></svg></button>
      <button onclick="_ribbonStep('${pid}',1)" aria-label="הבא"><svg viewBox="0 0 16 16"><path d="M6 12l4-4-4-4"/></svg></button>
    </span>
  </div>`);

  out.push('</div>');
  sec.innerHTML = out.join('');
  _runA11yAfterRender();
}

function _ribbonSetActive(pid, idx){
  const items = MEDIA[pid];
  if(!items || idx < 0 || idx >= items.length) return;
  _ribbonState[pid] = idx;
  const it = items[idx];
  const cap = _effCap(it);
  const isVid = it.type === 'vid';
  const newSrc = isVid ? (it.poster ? (it.vidbase==='img' ? B : VB)+it.poster : B + it.src) : B + it.src;
  const img = document.getElementById('ribbon-lead-img-'+pid);
  const plate = document.getElementById('ribbon-lead-plate-'+pid);
  const text = document.getElementById('ribbon-lead-text-'+pid);
  const counter = document.getElementById('ribbon-counter-'+pid);
  if(img){
    img.classList.add('fading');
    setTimeout(() => {
      img.src = newSrc;
      img.alt = cap || '';
      img.classList.remove('fading');
    }, 220);
  }
  if(plate) plate.textContent = `פלטה ${String(idx+1).padStart(2,'0')}`;
  if(text) text.textContent = cap || '';
  if(counter) counter.textContent = `FIG. ${String(idx+1).padStart(2,'0')} / ${String(items.length).padStart(2,'0')}`;
  // Update active thumb class
  const strip = document.getElementById('ribbon-strip-'+pid);
  if(strip){
    strip.querySelectorAll('.pp-ribbon-thumb').forEach((el,i) => el.classList.toggle('active', i === idx));
    // Scroll the active thumb into view (smooth)
    const active = strip.querySelector('.pp-ribbon-thumb.active');
    if(active) active.scrollIntoView({behavior:'smooth', block:'nearest', inline:'center'});
  }
}

function _ribbonStep(pid, dir){
  const items = MEDIA[pid];
  if(!items) return;
  const cur = _ribbonState[pid] || 0;
  const next = (cur + dir + items.length) % items.length;
  _ribbonSetActive(pid, next);
}

function _ribbonOpenLb(pid, key){
  const idx = _ribbonState[pid] || 0;
  if(typeof openLb === 'function') openLb(key, idx);
}
"""

# Insert before "// ── VIDEOS data" comment so it sits right after renderMedia + helpers
swap(
    "// Auto-derive overlay caption from image path.",
    RIBBON_JS + "\n// Auto-derive overlay caption from image path.",
    "Add _renderRibbonMedia + helpers",
)

# ═══════════════════════════════════════════════════════════════
# 5) Update MEDIA_HEADERS for ribbon variant — title can be more evocative
# ═══════════════════════════════════════════════════════════════
swap(
    """const MEDIA_HEADERS = {
  fixed:       { eye: 'גלריה', title: 'המוצר במגוון' },
  structural:  { eye: 'גלריה', title: 'המוצר במגוון' },
  penthouse:   { eye: 'גלריה', title: 'המוצר במגוון' },
  retractable: { eye: 'גלריה', title: 'המוצר בתנועה' },
  smoke:       { eye: 'גלריה', title: 'המוצר במגוון' },
};""",
    """const MEDIA_HEADERS = {
  fixed:       { eye: 'גלריה',         title: 'המוצר במגוון' },
  structural:  { eye: 'גלריה',         title: 'המוצר במגוון' },
  penthouse:   { eye: 'גלריה',         title: 'המוצר במגוון' },
  retractable: { eye: 'תנועה',          title: 'המוצר בפעולה' },
  smoke:       { eye: 'בטיחות',         title: 'אוורור ושחרור עשן' },
};""",
    "MEDIA_HEADERS: refine eye/title per category",
)

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
