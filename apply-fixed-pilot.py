#!/usr/bin/env python3
"""apply-fixed-pilot.py — Pilot 2 of 5 design recommendations on `fixed` category only.

Source of inspiration: alumeshet.co.il + alcon.co.il/projects-en/

What this ships
===============

1) Mosaic media strip (#1 from research):
   MEDIA.fixed gets per-tile aspect hints — 'wide' (3:2 spanning 4 cols of 6),
   'tall' (2:3 spanning 2 cols), or default (1:1 spanning 2 cols).
   The .pp-media-grid renderer adds .pp-media-grid--mosaic for `fixed` only,
   plus .tile-w / .tile-t classes per item. Other categories unaffected.

2) Hover metadata tiles (#5 from research):
   PROJECTS.fixed renders as a 3-col tile grid (`.pp-projects-tiles`) instead
   of the alternating big-card layout. Always-visible: name + location.
   Reveal on hover: architect + year + product. Mobile-safe (touch users
   still see name+location). Switching is per-pid via PROJECTS_LAYOUT map.

What this does NOT do
=====================
- #2 multi-criteria filter — needs a flat project list across categories
- #3 lazy-load + WebP — needs a build step, separate workstream
- #4 dedicated /projects view — separate page, separate work

Idempotent — safe to re-run.
"""
import sys, pathlib, re

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
# 1) CSS — mosaic variant for media strip + tile variant for projects
# ═══════════════════════════════════════════════════════════════

# Append the new CSS rules just before the closing of the existing .pp-media
# block. Anchor: the existing .pp-media @media(max-width:600px) line.
MOSAIC_ANCHOR = '@media(max-width:600px){.pp-media{padding:48px 0 56px}.pp-media-h,.pp-media-grid{padding:0 24px}.pp-media-grid{grid-template-columns:1fr}.pp-media-item .mp-play{width:48px;height:48px}}'

MOSAIC_NEW_CSS = MOSAIC_ANCHOR + """

    /* ── MOSAIC variant (pilot: fixed only) ── */
    .pp-media-grid--mosaic{grid-template-columns:repeat(6,1fr);grid-auto-flow:dense;gap:12px}
    .pp-media-grid--mosaic .pp-media-item{grid-column:span 2;aspect-ratio:1/1}
    .pp-media-grid--mosaic .pp-media-item.tile-w{grid-column:span 4;aspect-ratio:3/2}
    .pp-media-grid--mosaic .pp-media-item.tile-t{grid-column:span 2;aspect-ratio:2/3}
    @media(max-width:1024px){.pp-media-grid--mosaic{grid-template-columns:repeat(4,1fr)}.pp-media-grid--mosaic .pp-media-item.tile-w{grid-column:span 4}.pp-media-grid--mosaic .pp-media-item{grid-column:span 2}}
    @media(max-width:600px){.pp-media-grid--mosaic{grid-template-columns:1fr;gap:10px}.pp-media-grid--mosaic .pp-media-item,.pp-media-grid--mosaic .pp-media-item.tile-w,.pp-media-grid--mosaic .pp-media-item.tile-t{grid-column:span 1;aspect-ratio:4/3}}

    /* ── PROJECTS TILE variant with hover metadata reveal (pilot: fixed only) ── */
    .pp-projects-tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;padding:0 80px}
    .pp-proj-tile{position:relative;display:block;aspect-ratio:4/3;overflow:hidden;border-radius:6px;background:var(--dark);text-decoration:none;cursor:pointer}
    .pp-proj-tile img{width:100%;height:100%;object-fit:cover;transition:transform 1s var(--spring),filter 1s var(--spring);filter:brightness(.92) saturate(1.04)}
    .pp-proj-tile:hover img{transform:scale(1.05);filter:brightness(.7) saturate(1.08)}
    .pp-proj-tile-veil{position:absolute;inset:0;background:linear-gradient(180deg,transparent 35%,rgba(26,30,36,.86) 100%);pointer-events:none}
    .pp-proj-tile-base{position:absolute;left:0;right:0;bottom:0;padding:18px 22px 20px;color:#fff;direction:rtl;pointer-events:none}
    .pp-proj-tile-name{font-size:20px;font-weight:700;line-height:1.2;margin:0 0 4px;letter-spacing:-.005em}
    .pp-proj-tile-where{font-size:12px;font-weight:400;letter-spacing:.14em;color:rgba(255,255,255,.78);text-transform:uppercase}
    .pp-proj-tile-extra{max-height:0;opacity:0;overflow:hidden;transition:max-height .42s var(--spring),opacity .25s var(--spring),margin-top .42s var(--spring);margin-top:0}
    .pp-proj-tile:hover .pp-proj-tile-extra{max-height:140px;opacity:1;margin-top:14px}
    .pp-proj-tile-extra dl{display:grid;grid-template-columns:auto 1fr;gap:6px 18px;margin:0;font-size:13px}
    .pp-proj-tile-extra dt{font-size:11px;font-weight:400;letter-spacing:.16em;color:rgba(255,255,255,.62);text-transform:uppercase;padding-top:2px;white-space:nowrap;margin:0}
    .pp-proj-tile-extra dd{font-size:13px;font-weight:400;color:rgba(255,255,255,.96);line-height:1.45;margin:0}
    .pp-proj-tile-arrow{position:absolute;top:18px;left:18px;width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.14);backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;opacity:0;transform:scale(.86);transition:opacity .35s var(--spring),transform .35s var(--spring)}
    .pp-proj-tile:hover .pp-proj-tile-arrow{opacity:1;transform:scale(1)}
    .pp-proj-tile-arrow svg{width:14px;height:14px;stroke:#fff;fill:none;stroke-width:1.6}
    @media(max-width:1024px){.pp-projects-tiles{grid-template-columns:repeat(2,1fr);padding:0 48px}}
    @media(max-width:600px){.pp-projects-tiles{grid-template-columns:1fr;padding:0 24px;gap:10px}.pp-proj-tile-extra{max-height:140px;opacity:1;margin-top:14px}.pp-proj-tile-arrow{opacity:1;transform:scale(1)}}
"""

if ".pp-projects-tiles" in src:
    print("✔  Mosaic + tile-variant CSS — already present")
else:
    src = src.replace(MOSAIC_ANCHOR, MOSAIC_NEW_CSS, 1)
    changes += 1
    print("✔  Mosaic + tile-variant CSS appended")

# ═══════════════════════════════════════════════════════════════
# 2) MEDIA.fixed — add aspect:'wide'|'tall' hints to selected tiles
# ═══════════════════════════════════════════════════════════════
# Picked for visual rhythm — drone shots and panoramic crops go wide,
# portrait interiors go tall, neutral squares stay default.

ASPECT_TWEAKS = [
    # (anchor_substring, replacement_substring)
    # Wide: drone hero, debut hero
    ("{ type:'img', src:'02 — סקיילייט קבוע/חד שיפועי/DSC05064.jpg', cap:'' },",
     "{ type:'img', src:'02 — סקיילייט קבוע/חד שיפועי/DSC05064.jpg', cap:'', aspect:'wide' },"),
    # Tall: vertical interior (Edited-10 is portrait-ish)
    ("{ type:'img', src:'02 — סקיילייט קבוע/חד שיפועי/Edited-10.jpg', cap:'' },",
     "{ type:'img', src:'02 — סקיילייט קבוע/חד שיפועי/Edited-10.jpg', cap:'', aspect:'tall' },"),
    # Wide: Mitzpe drone shot
    ("{ type:'img', src:'02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/Use/DJI_20260225173740_0134_D(1).jpg', cap:'מצפה הימים' },",
     "{ type:'img', src:'02 — סקיילייט קבוע/מלון מצפה הימים - ראש פינה/Use/DJI_20260225173740_0134_D(1).jpg', cap:'מצפה הימים', aspect:'wide' },"),
    # Wide: HP HQ panoramic
    ("{ type:'img', src:'02 — סקיילייט קבוע/HP HQ - בניין מרקורי/HP06.jpg', cap:'HP HQ — בניין מרקורי' },",
     "{ type:'img', src:'02 — סקיילייט קבוע/HP HQ - בניין מרקורי/HP06.jpg', cap:'HP HQ — בניין מרקורי', aspect:'wide' },"),
    # Tall: 217 vertical detail
    ("{ type:'img', src:'02 — סקיילייט קבוע/דו שיפועי/217.jpg', cap:'' },",
     "{ type:'img', src:'02 — סקיילייט קבוע/דו שיפועי/217.jpg', cap:'', aspect:'tall' },"),
    # Wide: Bar-Ilan dual-slope
    ("{ type:'img', src:'02 — סקיילייט קבוע/דו שיפועי/6ב - מנהלה בר אילן.jpg', cap:'מנהלה — בר אילן' },",
     "{ type:'img', src:'02 — סקיילייט קבוע/דו שיפועי/6ב - מנהלה בר אילן.jpg', cap:'מנהלה — בר אילן', aspect:'wide' },"),
]

for old, new in ASPECT_TWEAKS:
    label = re.search(r"src:'([^']+)'", old).group(1).split('/')[-1]
    swap(old, new, f"MEDIA.fixed aspect → {label}", must_exist=False)

# ═══════════════════════════════════════════════════════════════
# 3) renderMedia — emit mosaic class + per-tile aspect class for fixed
# ═══════════════════════════════════════════════════════════════

RENDER_MEDIA_OLD = """function renderMedia(pid){
  const sec = document.getElementById('media-'+pid);
  if(!sec) return;
  const items = MEDIA[pid];
  if(!items || !items.length){ sec.style.display='none'; return; }
  const key = 'media-'+pid;
  const srcs  = items.map(it => it.type === 'vid' ? (it.vidbase==='img' ? B : VB)+it.src : B+it.src);
  const caps  = items.map(_effCap);
  const kinds = items.map(it => it.type === 'vid' ? 'vid' : 'img');
  _galReg[key] = { srcs, caps, kinds };

  const playIcon = '<svg class="mp-play" viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" fill="rgba(0,0,0,.38)"/><path d="M26 20 L46 32 L26 44 Z" fill="#fff"/></svg>';
  const out = [`<div class="pp-media-h"><div class="pp-projects-section-eye">גלריה</div><h2 class="pp-projects-section-t">עבודות נבחרות</h2></div>`, `<div class="pp-media-grid">`];
  items.forEach((it,i) => {
    const cap = _effCap(it);
    const capHtml = cap ? `<div class="pp-media-cap">${cap}</div>` : '';
    if(it.type === 'vid'){
      const vidSrc = (it.vidbase==='img' ? B : VB) + it.src;
      const poster = it.poster ? (it.vidbase==='img' ? B : VB)+it.poster : '';
      const thumb = poster
        ? `<img src="${poster}" alt="" loading="lazy">`
        : `<video src="${vidSrc}" preload="metadata" muted playsinline style="width:100%;height:100%;object-fit:cover;pointer-events:none"></video>`;
      out.push(`<div class="pp-media-item pp-media-vid" onclick="openLb('${key}',${i})">${thumb}${playIcon}${capHtml}</div>`);
    } else {
      out.push(`<div class="pp-media-item" onclick="openLb('${key}',${i})"><img src="${B}${it.src}" alt="" loading="lazy">${capHtml}</div>`);
    }
  });
  out.push('</div>');
  sec.innerHTML = out.join('');
}"""

RENDER_MEDIA_NEW = """// Pilot: per-pid mosaic layout map. 'mosaic' enables varied aspect ratios
// driven by `aspect:'wide'|'tall'` on each MEDIA item (default = square).
const MEDIA_LAYOUT = { fixed: 'mosaic' };

function renderMedia(pid){
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
  };

  const playIcon = '<svg class="mp-play" viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" fill="rgba(0,0,0,.38)"/><path d="M26 20 L46 32 L26 44 Z" fill="#fff"/></svg>';
  const out = [`<div class="pp-media-h"><div class="pp-projects-section-eye">גלריה</div><h2 class="pp-projects-section-t">עבודות נבחרות</h2></div>`, `<div class="${gridClass}">`];
  items.forEach((it,i) => {
    const cap = _effCap(it);
    const capHtml = cap ? `<div class="pp-media-cap">${cap}</div>` : '';
    const ac = aspectClass(it);
    if(it.type === 'vid'){
      const vidSrc = (it.vidbase==='img' ? B : VB) + it.src;
      const poster = it.poster ? (it.vidbase==='img' ? B : VB)+it.poster : '';
      const thumb = poster
        ? `<img src="${poster}" alt="" loading="lazy">`
        : `<video src="${vidSrc}" preload="metadata" muted playsinline style="width:100%;height:100%;object-fit:cover;pointer-events:none"></video>`;
      out.push(`<div class="pp-media-item pp-media-vid${ac}" onclick="openLb('${key}',${i})">${thumb}${playIcon}${capHtml}</div>`);
    } else {
      out.push(`<div class="pp-media-item${ac}" onclick="openLb('${key}',${i})"><img src="${B}${it.src}" alt="" loading="lazy">${capHtml}</div>`);
    }
  });
  out.push('</div>');
  sec.innerHTML = out.join('');
}"""

swap(RENDER_MEDIA_OLD, RENDER_MEDIA_NEW, "renderMedia: mosaic-aware variant")

# ═══════════════════════════════════════════════════════════════
# 4) renderProjectsSection — branch on layout (cards | tiles)
# ═══════════════════════════════════════════════════════════════

RENDER_PROJ_OLD = """function renderProjectsSection(pid){
  const sec=document.getElementById('projects-sec-'+pid);
  if(!sec)return;
  const projs=PROJECTS[pid];
  if(!projs||!projs.length){sec.style.display='none';return}
  const arrow='<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 8h10M9 4l4 4-4 4"/></svg>';
  const out=[`<div class="pp-projects-section-h"><div class="pp-projects-section-eye">מבחר עבודות</div><h2 class="pp-projects-section-t">פרויקטים</h2></div>`];
  projs.forEach((p,i)=>{
    const num=String(i+1).padStart(2,'0');
    const m=p.meta||{};
    out.push(`<div class="pp-proj-card">
      <a class="pp-proj-card-img" href="#project/${p.slug}" onclick="goProject('${p.slug}');return false">
        <img src="${B}${p.hero}" alt="${p.name}" loading="lazy">
      </a>
      <div class="pp-proj-card-txt">
        <div class="pp-proj-card-num">פרויקט ${num}</div>
        <h3 class="pp-proj-card-name">${p.name}</h3>
        <dl class="pp-proj-card-meta">
          ${m.where&&m.where!=='—'?`<dt>מיקום</dt><dd>${m.where}</dd>`:''}
          ${m.when&&m.when!=='—'?`<dt>שנה</dt><dd>${m.when}</dd>`:''}
          ${m.arch&&m.arch!=='—'?`<dt>אדריכל</dt><dd>${m.arch}</dd>`:''}
          ${m.product&&m.product!=='—'?`<dt>מוצר</dt><dd>${m.product}</dd>`:''}
        </dl>
        <a class="pp-proj-card-link" href="#project/${p.slug}" onclick="goProject('${p.slug}');return false">צפו בפרויקט ${arrow}</a>
      </div>
    </div>`);
  });
  sec.innerHTML=out.join('');
}"""

RENDER_PROJ_NEW = """// Pilot: per-pid layout map. 'tiles' = hover-reveal mosaic; default = cards.
const PROJECTS_LAYOUT = { fixed: 'tiles' };

function renderProjectsSection(pid){
  const sec=document.getElementById('projects-sec-'+pid);
  if(!sec)return;
  const projs=PROJECTS[pid];
  if(!projs||!projs.length){sec.style.display='none';return}
  const arrow='<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 8h10M9 4l4 4-4 4"/></svg>';
  const layout = PROJECTS_LAYOUT[pid] || 'cards';
  const out=[`<div class="pp-projects-section-h"><div class="pp-projects-section-eye">מבחר עבודות</div><h2 class="pp-projects-section-t">פרויקטים</h2></div>`];

  if(layout === 'tiles'){
    out.push('<div class="pp-projects-tiles">');
    projs.forEach(p => {
      const m = p.meta||{};
      const extras = [];
      if(m.arch && m.arch !== '—') extras.push(`<dt>אדריכל</dt><dd>${m.arch}</dd>`);
      if(m.when && m.when !== '—') extras.push(`<dt>שנה</dt><dd>${m.when}</dd>`);
      if(m.product && m.product !== '—') extras.push(`<dt>מוצר</dt><dd>${m.product}</dd>`);
      const extraHtml = extras.length ? `<div class="pp-proj-tile-extra"><dl>${extras.join('')}</dl></div>` : '';
      const where = (m.where && m.where !== '—') ? m.where : '';
      out.push(`<a class="pp-proj-tile" href="#project/${p.slug}" onclick="goProject('${p.slug}');return false">
        <img src="${B}${p.hero}" alt="${p.name}" loading="lazy">
        <div class="pp-proj-tile-veil"></div>
        <div class="pp-proj-tile-arrow">${arrow}</div>
        <div class="pp-proj-tile-base">
          <h3 class="pp-proj-tile-name">${p.name}</h3>
          ${where ? `<div class="pp-proj-tile-where">${where}</div>` : ''}
          ${extraHtml}
        </div>
      </a>`);
    });
    out.push('</div>');
  } else {
    projs.forEach((p,i)=>{
      const num=String(i+1).padStart(2,'0');
      const m=p.meta||{};
      out.push(`<div class="pp-proj-card">
        <a class="pp-proj-card-img" href="#project/${p.slug}" onclick="goProject('${p.slug}');return false">
          <img src="${B}${p.hero}" alt="${p.name}" loading="lazy">
        </a>
        <div class="pp-proj-card-txt">
          <div class="pp-proj-card-num">פרויקט ${num}</div>
          <h3 class="pp-proj-card-name">${p.name}</h3>
          <dl class="pp-proj-card-meta">
            ${m.where&&m.where!=='—'?`<dt>מיקום</dt><dd>${m.where}</dd>`:''}
            ${m.when&&m.when!=='—'?`<dt>שנה</dt><dd>${m.when}</dd>`:''}
            ${m.arch&&m.arch!=='—'?`<dt>אדריכל</dt><dd>${m.arch}</dd>`:''}
            ${m.product&&m.product!=='—'?`<dt>מוצר</dt><dd>${m.product}</dd>`:''}
          </dl>
          <a class="pp-proj-card-link" href="#project/${p.slug}" onclick="goProject('${p.slug}');return false">צפו בפרויקט ${arrow}</a>
        </div>
      </div>`);
    });
  }
  sec.innerHTML=out.join('');
}"""

swap(RENDER_PROJ_OLD, RENDER_PROJ_NEW, "renderProjectsSection: layout-aware variant")

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
