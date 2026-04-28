#!/usr/bin/env python3
"""apply-tile-option-c.py — Adopt Claude Design's Option C (Technical Frame).

Source: skylight-website/project/tile-variations.css §Variation C
        (corners + spec rail design)

What changes
============
• 2-col grid at desktop (was 3-col); 1-col at ≤1024px
• Lighter veil: linear-gradient(180deg, transparent 50%, rgba(26,30,36,.6) 100%)
• 4 teal L-corner brackets (--accent-pale), drawing in 24→30px on hover
• Spec rail: translucent dark panel with backdrop-blur, slides from start
  edge (right in RTL), 46% width, 3 stacked label/value rows w/ hairlines
• Drawing-set arrow: line extends 0→36px next to project name + 12px arrowhead
• Mobile: spec rail always visible (no hover available on touch)

This replaces the entire .pp-proj-tile* CSS block (lines ~736-754) and
rewrites the tile HTML in renderProjectsSection.

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
# 1) CSS — replace entire .pp-proj-tile* block with Option C
# ═══════════════════════════════════════════════════════════════
OLD_CSS = """    .pp-projects-tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;padding:0 80px}
    .pp-proj-tile{position:relative;display:block;aspect-ratio:4/3;overflow:hidden;border-radius:6px;background:var(--dark);text-decoration:none;cursor:pointer}
    .pp-proj-tile img{width:100%;height:100%;object-fit:cover;transition:transform 1s var(--spring),filter 1s var(--spring);filter:brightness(.92) saturate(1.04)}
    .pp-proj-tile:hover img{transform:scale(1.05);filter:brightness(.7) saturate(1.08)}
    .pp-proj-tile-veil{position:absolute;inset:0;background:linear-gradient(180deg,transparent 35%,rgba(26,30,36,.86) 100%);pointer-events:none}
    .pp-proj-tile-base{position:absolute;left:0;right:0;bottom:0;padding:18px 22px 20px;color:#fff;direction:rtl;pointer-events:none}
    .pp-proj-tile-name{font-size:20px;font-weight:700;line-height:1.2;margin:0 0 4px;letter-spacing:-.005em}
    .pp-proj-tile-where{font-size:12px;font-weight:400;letter-spacing:.14em;color:rgba(255,255,255,.78);text-transform:uppercase}
    .pp-proj-tile-extra{max-height:0;opacity:0;overflow:hidden;transition:max-height .42s var(--spring),opacity .25s var(--spring),margin-top .42s var(--spring);margin-top:0}
    .pp-proj-tile:hover .pp-proj-tile-extra,.pp-proj-tile:focus-within .pp-proj-tile-extra{max-height:140px;opacity:1;margin-top:14px}
    .pp-proj-tile-extra dl{display:grid;grid-template-columns:auto 1fr;gap:6px 18px;margin:0;font-size:13px}
    .pp-proj-tile-extra dt{font-size:11px;font-weight:400;letter-spacing:.16em;color:rgba(255,255,255,.62);text-transform:uppercase;padding-top:2px;white-space:nowrap;margin:0}
    .pp-proj-tile-extra dd{font-size:13px;font-weight:400;color:rgba(255,255,255,.96);line-height:1.45;margin:0}
    .pp-proj-tile-arrow{position:absolute;top:18px;left:18px;width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.14);backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;opacity:0;transform:scale(.86);transition:opacity .35s var(--spring),transform .35s var(--spring)}
    .pp-proj-tile:hover .pp-proj-tile-arrow,.pp-proj-tile:focus-within .pp-proj-tile-arrow{opacity:1;transform:scale(1)}
    .pp-proj-tile:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
    .pp-proj-tile-arrow svg{width:14px;height:14px;stroke:#fff;fill:none;stroke-width:1.6}
    @media(max-width:1024px){.pp-projects-tiles{grid-template-columns:repeat(2,1fr);padding:0 48px}}
    @media(max-width:600px){.pp-projects-tiles{grid-template-columns:1fr;padding:0 24px;gap:10px}.pp-proj-tile-extra{max-height:140px;opacity:1;margin-top:14px}.pp-proj-tile-arrow{opacity:1;transform:scale(1)}}"""

NEW_CSS = """    /* ── PROJECT TILES — Option C "Technical Frame" (corners + spec rail) ── */
    .pp-projects-tiles{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;padding:0 80px}
    .pp-proj-tile{position:relative;display:block;aspect-ratio:4/3;overflow:hidden;background:var(--dark);text-decoration:none;cursor:pointer}
    .pp-proj-tile img{width:100%;height:100%;object-fit:cover;transition:transform 1.2s var(--spring),filter .9s var(--spring);filter:brightness(.95) saturate(1.06)}
    .pp-proj-tile:hover img{transform:scale(1.03);filter:brightness(.78) saturate(1.08)}
    .pp-proj-tile-veil{position:absolute;inset:0;background:linear-gradient(180deg,transparent 50%,rgba(26,30,36,.6) 100%);pointer-events:none}
    /* Corner brackets — draw in from each corner on hover */
    .pp-proj-tile-corner{position:absolute;width:24px;height:24px;border-color:var(--accent-pale);border-style:solid;border-width:0;opacity:0;transition:opacity .35s var(--spring),width .45s var(--spring),height .45s var(--spring);pointer-events:none;z-index:3}
    .pp-proj-tile:hover .pp-proj-tile-corner,.pp-proj-tile:focus-within .pp-proj-tile-corner{opacity:1;width:30px;height:30px}
    .pp-proj-tile-corner-tl{top:14px;left:14px;border-top-width:1.5px;border-left-width:1.5px}
    .pp-proj-tile-corner-tr{top:14px;right:14px;border-top-width:1.5px;border-right-width:1.5px}
    .pp-proj-tile-corner-bl{bottom:14px;left:14px;border-bottom-width:1.5px;border-left-width:1.5px}
    .pp-proj-tile-corner-br{bottom:14px;right:14px;border-bottom-width:1.5px;border-right-width:1.5px}
    /* Bottom name + drawing-set arrow */
    .pp-proj-tile-base{position:absolute;inset-inline:0;bottom:0;padding:26px 30px;color:#fff;z-index:4;pointer-events:none;direction:rtl}
    .pp-proj-tile-name-row{display:flex;align-items:center;gap:16px}
    .pp-proj-tile-name{font-size:20px;font-weight:700;line-height:1.2;margin:0;letter-spacing:-.005em;text-shadow:0 1px 10px rgba(0,0,0,.4)}
    .pp-proj-tile-arrow{display:inline-flex;align-items:center;gap:8px;color:var(--accent-pale);flex:0 0 auto}
    .pp-proj-tile-arrow-line{display:block;width:0;height:1px;background:currentColor;transition:width .4s var(--spring)}
    .pp-proj-tile:hover .pp-proj-tile-arrow-line,.pp-proj-tile:focus-within .pp-proj-tile-arrow-line{width:36px}
    .pp-proj-tile-arrow svg{width:12px;height:12px;flex:0 0 auto}
    .pp-proj-tile-where{font-size:11px;font-weight:400;letter-spacing:.22em;text-transform:uppercase;color:rgba(255,255,255,.78);margin-top:8px}
    /* Spec rail — slides in from start edge (right in RTL) on hover */
    .pp-proj-tile-spec{position:absolute;top:14px;bottom:14px;right:14px;width:46%;padding:30px 26px;background:linear-gradient(265deg,rgba(16,20,26,.78) 0%,rgba(16,20,26,.55) 100%);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);display:flex;flex-direction:column;justify-content:center;gap:14px;transform:translateX(20px);opacity:0;transition:transform .55s var(--spring),opacity .35s var(--spring);z-index:5;pointer-events:none;border-left:1px solid rgba(127,188,200,.22);direction:rtl}
    .pp-proj-tile:hover .pp-proj-tile-spec,.pp-proj-tile:focus-within .pp-proj-tile-spec{transform:translateX(0);opacity:1}
    .pp-proj-tile-spec-row{display:flex;flex-direction:column;gap:4px;padding-bottom:12px;border-bottom:1px solid rgba(255,255,255,.12)}
    .pp-proj-tile-spec-row:last-child{border-bottom:0;padding-bottom:0}
    .pp-proj-tile-spec-row span{font-size:10px;font-weight:400;letter-spacing:.22em;text-transform:uppercase;color:var(--accent-pale)}
    .pp-proj-tile-spec-row b{font-size:13px;font-weight:500;color:#fff;line-height:1.35;letter-spacing:-.002em}
    .pp-proj-tile:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
    /* Mobile/tablet: collapse to 1-col, spec rail always visible (no hover on touch) */
    @media(max-width:1024px){.pp-projects-tiles{grid-template-columns:1fr;padding:0 48px}}
    @media(max-width:600px){.pp-projects-tiles{padding:0 24px;gap:10px}.pp-proj-tile-spec{transform:translateX(0);opacity:1;width:50%}.pp-proj-tile-corner{opacity:1;width:30px;height:30px}.pp-proj-tile-arrow-line{width:36px}}"""

swap(OLD_CSS, NEW_CSS, "Option C tile CSS replacement")

# ═══════════════════════════════════════════════════════════════
# 2) JS — rewrite renderProjectsSection's tile HTML to Option C structure
# ═══════════════════════════════════════════════════════════════
OLD_RENDER = """    out.push('<div class="pp-projects-tiles">');
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
    out.push('</div>');"""

NEW_RENDER = """    out.push('<div class="pp-projects-tiles">');
    projs.forEach(p => {
      const m = p.meta||{};
      const where = (m.where && m.where !== '—') ? m.where : '';
      const specRows = [];
      if(m.arch && m.arch !== '—') specRows.push(`<div class="pp-proj-tile-spec-row"><span>אדריכל</span><b>${m.arch}</b></div>`);
      if(m.when && m.when !== '—') specRows.push(`<div class="pp-proj-tile-spec-row"><span>שנה</span><b>${m.when}</b></div>`);
      if(m.product && m.product !== '—') specRows.push(`<div class="pp-proj-tile-spec-row"><span>מוצר</span><b>${m.product}</b></div>`);
      const specHtml = specRows.length ? `<div class="pp-proj-tile-spec">${specRows.join('')}</div>` : '';
      out.push(`<a class="pp-proj-tile" href="#project/${p.slug}" onclick="goProject('${p.slug}');return false">
        <img src="${B}${p.hero}" alt="${p.name}" loading="lazy">
        <div class="pp-proj-tile-veil"></div>
        <span class="pp-proj-tile-corner pp-proj-tile-corner-tl"></span>
        <span class="pp-proj-tile-corner pp-proj-tile-corner-tr"></span>
        <span class="pp-proj-tile-corner pp-proj-tile-corner-bl"></span>
        <span class="pp-proj-tile-corner pp-proj-tile-corner-br"></span>
        <div class="pp-proj-tile-base">
          <div class="pp-proj-tile-name-row">
            <h3 class="pp-proj-tile-name">${p.name}</h3>
            <div class="pp-proj-tile-arrow" aria-hidden="true">
              <span class="pp-proj-tile-arrow-line"></span>
              <svg viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M1 5h8M6 1l3 4-3 4"/></svg>
            </div>
          </div>
          ${where ? `<div class="pp-proj-tile-where">${where}</div>` : ''}
        </div>
        ${specHtml}
      </a>`);
    });
    out.push('</div>');"""

swap(OLD_RENDER, NEW_RENDER, "renderProjectsSection: Option C tile HTML")

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
