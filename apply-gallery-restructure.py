#!/usr/bin/env python3
"""
Gallery restructure (hybrid: product-tabs + project chip filter + persistent captions).

- Changes grid-dyn caption from full-width gradient bar to always-visible corner chip
- Adds CSS for a new .pp-projects chip row (teal-accent pills matching brand)
- Injects <div class="pp-projects" id="proj-{pid}"></div> on all 6 product pages
- Rewrites renderGallery into _renderGalGrid + _renderProjChips with chip filtering
- Adds data-project="…" on each .pp-gal-item for the upcoming project detail pages

Idempotent: safe to re-run. Run from Terminal: python3 apply-gallery-restructure.py
"""
import sys
PATH = '/Users/ohadshamir/Downloads/skylite-github/index.html'

try:
    html = open(PATH, encoding='utf-8').read()
except FileNotFoundError:
    print(f'❌ Could not find {PATH}')
    sys.exit(1)

changes = 0

# ─────────────────────────────────────────────────────────────────────
# 1. Replace grid-dyn caption style: compact corner chip, always visible
# ─────────────────────────────────────────────────────────────────────
OLD_CAP = '.pp-gal-grid.grid-dyn>.pp-gal-item .pp-gal-cap{position:absolute;bottom:0;right:0;left:0;padding:14px 18px;background:linear-gradient(transparent,rgba(0,0,0,.5));font-size:12px;font-weight:300;letter-spacing:.1em;color:rgba(255,255,255,.88);border-radius:0 0 8px 8px}'
NEW_CAP = '.pp-gal-grid.grid-dyn>.pp-gal-item .pp-gal-cap{position:absolute;bottom:12px;right:12px;padding:6px 12px;background:rgba(26,30,36,.74);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);font-size:11px;font-weight:400;letter-spacing:.08em;color:rgba(255,255,255,.94);border:1px solid rgba(255,255,255,.08);border-radius:3px;pointer-events:none;max-width:calc(100% - 24px);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'

if OLD_CAP in html:
    html = html.replace(OLD_CAP, NEW_CAP, 1)
    print('✅ Updated grid-dyn caption to persistent corner chip')
    changes += 1
elif NEW_CAP in html:
    print('ℹ️  Caption style already updated')
else:
    print('⚠️  Could not locate old caption style — skipping')

# ─────────────────────────────────────────────────────────────────────
# 2. Append project-chip CSS after .pp-subs rule block
# ─────────────────────────────────────────────────────────────────────
SUBS_ANCHOR = '    .pp-subs{background:var(--linen);padding:0 80px;border-bottom:1px solid var(--warm-gray)}'
CHIP_CSS = '''
    .pp-projects{background:var(--linen);padding:0 80px 16px;border-bottom:1px solid var(--warm-gray);display:none}
    .pp-projects.has-chips{display:block}
    .pp-projects-inner{display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding-top:14px}
    .pp-projects-lbl{font-size:10.5px;font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:var(--stone);margin-left:10px}
    .pp-proj-chip{background:transparent;border:1px solid var(--warm-gray);color:var(--dark);padding:6px 14px;font-size:12px;font-weight:400;letter-spacing:.04em;border-radius:100px;cursor:pointer;transition:background .25s var(--spring),border-color .25s var(--spring),color .25s var(--spring);font-family:inherit}
    .pp-proj-chip:hover{border-color:var(--accent);color:var(--accent)}
    .pp-proj-chip.active{background:var(--accent);border-color:var(--accent);color:#fff}
    @media(max-width:1100px){.pp-projects{padding:0 48px 14px}}
    @media(max-width:768px){.pp-projects{padding:0 24px 12px}}'''

if SUBS_ANCHOR in html and '.pp-projects{' not in html:
    html = html.replace(SUBS_ANCHOR, SUBS_ANCHOR + CHIP_CSS, 1)
    print('✅ Added project filter chip CSS')
    changes += 1
elif '.pp-projects{' in html:
    print('ℹ️  Chip CSS already present')
else:
    print('⚠️  Could not find .pp-subs CSS anchor')

# ─────────────────────────────────────────────────────────────────────
# 3. Inject chip bar into each of 6 product pages
#    Placement: between .pp-subs and .pp-gallery
# ─────────────────────────────────────────────────────────────────────
PIDS = ['penthouse', 'fixed', 'retractable', 'walkon', 'structural', 'smoke']
for pid in PIDS:
    needle = f'<section class="pp-gallery"><div class="pp-gallery-t">גלריית פרויקטים</div><div class="pp-gal-grid grid-dyn" id="gal-{pid}"></div></section>'
    inject = f'<div class="pp-projects" id="proj-{pid}"></div>\n{needle}'
    if f'id="proj-{pid}"' in html:
        print(f'ℹ️  proj-{pid} chip bar already present')
        continue
    if needle in html:
        html = html.replace(needle, inject, 1)
        print(f'✅ Injected chip bar for {pid}')
        changes += 1
    else:
        print(f'⚠️  Could not find gallery section for {pid} — skipping')

# ─────────────────────────────────────────────────────────────────────
# 4. Upgrade renderGallery — split into grid + chip renderers with filter
# ─────────────────────────────────────────────────────────────────────
OLD_RENDER = '''function renderGallery(pid, tabLabel){
  const grid=document.getElementById('gal-'+pid);
  if(!grid)return;
  const data=GALLERIES[pid];
  if(!data)return;
  const imgs=data[tabLabel]||data[Object.keys(data)[0]];
  const key=pid+'|'+tabLabel;
  const srcs=imgs.map(item=>item.s.startsWith('data:')?item.s:B+item.s);
  const caps=imgs.map(item=>item.c||'');
  _galReg[key]={srcs,caps};
  grid.innerHTML=imgs.map((item,i)=>{
    const src=srcs[i];
    const cap=item.c?`<span class="pp-gal-cap">${item.c}</span>`:'';
    return `<div class="pp-gal-item" onclick="openLb('${key}',${i})"><img src="${src}" alt="" loading="lazy">${cap}</div>`;
  }).join('');
}'''

NEW_RENDER = '''function _projKey(c){return (c||'').trim()}

function renderGallery(pid, tabLabel){
  const grid=document.getElementById('gal-'+pid);
  if(!grid)return;
  const data=GALLERIES[pid];
  if(!data)return;
  const label=data[tabLabel]?tabLabel:Object.keys(data)[0];
  const imgs=data[label];
  const key=pid+'|'+label;
  const srcs=imgs.map(item=>item.s.startsWith('data:')?item.s:B+item.s);
  const caps=imgs.map(item=>item.c||'');
  _galReg[key]={srcs,caps,imgs,pid,label};
  _renderGalGrid(pid,label,null);
  _renderProjChips(pid,label);
}

function _renderGalGrid(pid,label,filterProj){
  const grid=document.getElementById('gal-'+pid);
  if(!grid)return;
  const key=pid+'|'+label;
  const reg=_galReg[key];
  if(!reg)return;
  grid.innerHTML=reg.imgs.map((item,i)=>{
    if(filterProj && _projKey(item.c)!==filterProj) return '';
    const src=reg.srcs[i];
    const cap=item.c?`<span class="pp-gal-cap">${item.c}</span>`:'';
    const pk=_projKey(item.c);
    const dp=pk?` data-project="${pk.replace(/"/g,'&quot;')}"`:'';
    return `<div class="pp-gal-item"${dp} onclick="openLb('${key}',${i})"><img src="${src}" alt="" loading="lazy">${cap}</div>`;
  }).join('');
}

function _renderProjChips(pid,label){
  const bar=document.getElementById('proj-'+pid);
  if(!bar)return;
  const key=pid+'|'+label;
  const reg=_galReg[key];
  if(!reg){bar.classList.remove('has-chips');bar.innerHTML='';return}
  const seen=new Set(),projects=[];
  reg.imgs.forEach(it=>{const pk=_projKey(it.c);if(pk && !seen.has(pk)){seen.add(pk);projects.push(pk)}});
  if(projects.length<2){bar.classList.remove('has-chips');bar.innerHTML='';return}
  bar.classList.add('has-chips');
  const escA=s=>String(s).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;');
  const frag=['<div class="pp-projects-inner"><span class="pp-projects-lbl">פרויקט</span>'];
  frag.push(`<button class="pp-proj-chip active" data-proj="">הכל</button>`);
  projects.forEach(p=>{
    frag.push(`<button class="pp-proj-chip" data-proj="${escA(p)}">${p}</button>`);
  });
  frag.push('</div>');
  bar.innerHTML=frag.join('');
  bar.querySelectorAll('.pp-proj-chip').forEach(btn=>{
    btn.addEventListener('click',()=>{
      bar.querySelectorAll('.pp-proj-chip').forEach(c=>c.classList.remove('active'));
      btn.classList.add('active');
      _renderGalGrid(pid,label,btn.dataset.proj||null);
    });
  });
}'''

if OLD_RENDER in html:
    html = html.replace(OLD_RENDER, NEW_RENDER, 1)
    print('✅ Upgraded renderGallery + added chip-filter logic')
    changes += 1
elif '_renderProjChips' in html:
    print('ℹ️  renderGallery already upgraded')
else:
    print('⚠️  Could not find old renderGallery — skipping')

# ─────────────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────────────
if changes:
    open(PATH, 'w', encoding='utf-8').write(html)
    print(f'\n━━ {changes} change(s) saved to index.html')
    print('Next: git add index.html && git commit -m "Gallery restructure: project chip filter + persistent captions" && git push')
else:
    print('\n━━ No changes made (all edits already applied)')
