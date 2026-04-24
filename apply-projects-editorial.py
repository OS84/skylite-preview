#!/usr/bin/env python3
"""
Restructure product pages to a flat product + editorial projects layout.

Supersedes apply-gallery-restructure.py (reverts the chip bars and sub-tab logic
it added) and removes the sub-tabs + dynamic gallery entirely. Each product page
now ends with one of:
  - editorial projects section (alternating stacked cards → will link to future project detail pages)
  - selected-work gallery (fallback for products with no named projects yet)
  - both, for walkon (1 named project + 6 unnamed "פרויקטים נוספים" shots)

Placeholder meta (—) is used for location/year/architect so the user can fill in.

Idempotent: safe to re-run. Run from Terminal:  python3 apply-projects-editorial.py
"""
import re, sys
PATH = '/Users/ohadshamir/Downloads/skylite-github/index.html'

try:
    html = open(PATH, encoding='utf-8').read()
except FileNotFoundError:
    print(f'❌ File not found: {PATH}')
    sys.exit(1)

changes = 0
PIDS = ['penthouse', 'fixed', 'retractable', 'walkon', 'structural', 'smoke']

# ──────────────────────────────────────────────────────────────────────
# 1. Revert chip-bar CSS from previous apply script
# ──────────────────────────────────────────────────────────────────────
CHIP_CSS_RE = re.compile(
    r'\n    \.pp-projects\{background:var\(--linen\).*?'
    r'@media\(max-width:768px\)\{\.pp-projects\{padding:0 24px 12px\}\}',
    re.DOTALL
)
if CHIP_CSS_RE.search(html):
    html = CHIP_CSS_RE.sub('', html, count=1)
    print('✅ Removed chip-bar CSS from previous script')
    changes += 1
else:
    print('ℹ️  Chip-bar CSS already gone')

# ──────────────────────────────────────────────────────────────────────
# 2. Add new editorial CSS (before the .pp-subs rule since we'll keep that rule intact for harmless dead code)
# ──────────────────────────────────────────────────────────────────────
CSS_ANCHOR = '    .pp-subs{background:var(--linen);padding:0 80px;border-bottom:1px solid var(--warm-gray)}'
NEW_CSS = """    .pp-projects-section{background:var(--cream);padding:100px 0 120px}
    .pp-projects-section-h{padding:0 80px;margin-bottom:56px}
    .pp-projects-section-eye{font-size:12px;font-weight:300;letter-spacing:.22em;color:var(--stone);text-transform:uppercase;margin-bottom:14px}
    .pp-projects-section-t{font-size:clamp(28px,4.2vw,44px);font-weight:700;color:var(--dark);line-height:1.1;margin:0}
    .pp-proj-card{display:grid;grid-template-columns:1.4fr 1fr;gap:56px;align-items:center;padding:0 80px;margin-bottom:96px}
    .pp-proj-card:last-child{margin-bottom:0}
    .pp-proj-card:nth-child(even){grid-template-columns:1fr 1.4fr}
    .pp-proj-card:nth-child(even) .pp-proj-card-img{order:2}
    .pp-proj-card-img{position:relative;aspect-ratio:4/3;overflow:hidden;border-radius:6px;background:var(--dark);cursor:pointer;display:block}
    .pp-proj-card-img img{width:100%;height:100%;object-fit:cover;transition:transform 1s var(--spring),filter 1s var(--spring);filter:brightness(.94) saturate(1.04)}
    .pp-proj-card-img:hover img{transform:scale(1.04);filter:brightness(1) saturate(1.1)}
    .pp-proj-card-num{font-size:11px;font-weight:500;letter-spacing:.26em;color:var(--accent);text-transform:uppercase;margin-bottom:16px}
    .pp-proj-card-name{font-size:clamp(24px,3.2vw,36px);font-weight:700;color:var(--dark);line-height:1.15;margin:0 0 28px}
    .pp-proj-card-meta{display:grid;grid-template-columns:auto 1fr;gap:12px 32px;margin-bottom:32px}
    .pp-proj-card-meta dt{font-size:11px;font-weight:400;letter-spacing:.18em;color:var(--stone);text-transform:uppercase;padding-top:3px;white-space:nowrap}
    .pp-proj-card-meta dd{font-size:15px;font-weight:400;color:var(--dark);margin:0;line-height:1.5}
    .pp-proj-card-link{display:inline-flex;align-items:center;gap:10px;font-size:13px;font-weight:500;letter-spacing:.08em;color:var(--accent);border-bottom:1px solid var(--accent);padding-bottom:4px;text-decoration:none;transition:color .25s var(--spring),border-color .25s var(--spring),gap .25s var(--spring);cursor:pointer}
    .pp-proj-card-link:hover{color:var(--accent-deep);border-color:var(--accent-deep);gap:14px}
    .pp-proj-card-link svg{width:14px;height:14px}
    .pp-selected-work{background:var(--cream);padding:100px 0 120px}
    .pp-selected-work-h{padding:0 80px;margin-bottom:48px}
    .pp-selected-work-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:0 80px}
    .pp-selected-work-item{position:relative;aspect-ratio:4/3;overflow:hidden;border-radius:6px;background:var(--dark);cursor:pointer}
    .pp-selected-work-item img{width:100%;height:100%;object-fit:cover;transition:transform 1s var(--spring),filter 1s var(--spring);filter:brightness(.94) saturate(1.04)}
    .pp-selected-work-item:hover img{transform:scale(1.04);filter:brightness(1) saturate(1.1)}
"""
if '.pp-projects-section{' not in html and CSS_ANCHOR in html:
    html = html.replace(CSS_ANCHOR, NEW_CSS + CSS_ANCHOR, 1)
    print('✅ Added editorial projects + selected-work CSS')
    changes += 1
elif '.pp-projects-section{' in html:
    print('ℹ️  Editorial CSS already present')
else:
    print('⚠️  Could not find CSS anchor for .pp-subs')

# ──────────────────────────────────────────────────────────────────────
# Responsive CSS overrides — inject into existing media queries
# ──────────────────────────────────────────────────────────────────────
RESP_1100_ANCHOR = '.pp-gallery{padding:60px 0 0}'
RESP_1100_ADD = ('.pp-gallery{padding:60px 0 0}'
                 '.pp-projects-section,.pp-selected-work{padding:70px 0 80px}'
                 '.pp-projects-section-h,.pp-selected-work-h,.pp-proj-card{padding:0 48px}'
                 '.pp-proj-card{grid-template-columns:1fr;gap:28px;margin-bottom:64px}'
                 '.pp-proj-card:nth-child(even){grid-template-columns:1fr}'
                 '.pp-proj-card:nth-child(even) .pp-proj-card-img{order:0}'
                 '.pp-selected-work-grid{grid-template-columns:repeat(2,1fr);padding:0 48px}')
if '.pp-projects-section,.pp-selected-work{padding:70px' not in html and RESP_1100_ANCHOR in html:
    html = html.replace(RESP_1100_ANCHOR, RESP_1100_ADD, 1)
    print('✅ Added tablet responsive CSS')
    changes += 1
elif '.pp-projects-section,.pp-selected-work{padding:70px' in html:
    print('ℹ️  Tablet responsive CSS already present')

RESP_768_ANCHOR = '.pp-gallery-t{padding:0 24px}'
RESP_768_ADD = ('.pp-gallery-t{padding:0 24px}'
                '.pp-projects-section,.pp-selected-work{padding:48px 0 56px}'
                '.pp-projects-section-h,.pp-selected-work-h,.pp-proj-card{padding:0 24px}'
                '.pp-proj-card-meta{grid-template-columns:auto 1fr;gap:8px 20px}'
                '.pp-selected-work-grid{grid-template-columns:1fr;padding:0 24px}')
if '.pp-projects-section,.pp-selected-work{padding:48px' not in html and RESP_768_ANCHOR in html:
    html = html.replace(RESP_768_ANCHOR, RESP_768_ADD, 1)
    print('✅ Added mobile responsive CSS')
    changes += 1
elif '.pp-projects-section,.pp-selected-work{padding:48px' in html:
    print('ℹ️  Mobile responsive CSS already present')

# ──────────────────────────────────────────────────────────────────────
# 3. Per-page HTML surgery — remove .pp-subs + chipbar + .pp-gallery, replace with new section(s)
# ──────────────────────────────────────────────────────────────────────
PAGE_SECTIONS = {
    'penthouse':   '<section class="pp-projects-section" id="projects-sec-penthouse"></section>',
    'fixed':       '<section class="pp-projects-section" id="projects-sec-fixed"></section>',
    'retractable': '<section class="pp-selected-work" id="selwork-retractable"></section>',
    'walkon':      '<section class="pp-projects-section" id="projects-sec-walkon"></section>\n<section class="pp-selected-work" id="selwork-walkon"></section>',
    'structural':  '<section class="pp-projects-section" id="projects-sec-structural"></section>',
    'smoke':       '<section class="pp-selected-work" id="selwork-smoke"></section>',
}

for pid in PIDS:
    new_sec = PAGE_SECTIONS[pid]
    if f'id="projects-sec-{pid}"' in html or f'id="selwork-{pid}"' in html:
        print(f'ℹ️  {pid} already migrated')
        continue
    pattern = re.compile(
        r'<div class="pp-subs">[^\n]*subTab\(this,\'' + pid + r'\'\)[^\n]*</div></div>\n'
        r'(?:<div class="pp-projects" id="proj-' + pid + r'"></div>\n)?'
        r'<section class="pp-gallery">[^\n]*id="gal-' + pid + r'"[^\n]*</section>\n'
    )
    m = pattern.search(html)
    if m:
        html = pattern.sub(new_sec + '\n', html, count=1)
        print(f'✅ Replaced gallery block for {pid}')
        changes += 1
    else:
        print(f'⚠️  Could not match gallery block for {pid}')

# ──────────────────────────────────────────────────────────────────────
# 4. Replace JS engine — swap subTab/GALLERIES/renderGallery/chip-helpers/init
#    with PROJECTS + SELECTED_WORK + renderers + new init
# ──────────────────────────────────────────────────────────────────────
OLD_JS_START = 'function subTab(btn,pid){'
OLD_JS_END_MARKER = '});\n\n// ── Lightbox ──'

idx_start = html.find(OLD_JS_START)
idx_end   = html.find(OLD_JS_END_MARKER, idx_start) if idx_start >= 0 else -1

NEW_JS = r"""const B='./מוצרים מסווגים/';

const PROJECTS={
  penthouse:[
    {slug:'penthouse-jerusalem',name:'בית יוקרה — ירושלים',hero:'06 — יציאה לגג/DJI_20260311171920_0260_D.jpg',meta:{where:'ירושלים',when:'—',arch:'—',product:'יציאה לגג'},images:['06 — יציאה לגג/DJI_20260311171920_0260_D.jpg','06 — יציאה לגג/DJI_20260311171943_0261_D.jpg','06 — יציאה לגג/DJI_20260311172525_0266_D.jpg','06 — יציאה לגג/DJI_20260311172739_0269_D.jpg','06 — יציאה לגג/DSC05074.jpg','06 — יציאה לגג/DSC05075.jpg','06 — יציאה לגג/DSC05077.jpg','06 — יציאה לגג/DSC05078.jpg']},
    {slug:'penthouse-ben-yehuda',name:'דירת גג — בן יהודה',hero:'06 — יציאה לגג/DJI_20260304175337_0201_D.jpg',meta:{where:'תל אביב',when:'—',arch:'—',product:'יציאה לגג'},images:['06 — יציאה לגג/DSC05026.jpg','06 — יציאה לגג/DSC05032.jpg','06 — יציאה לגג/DSC05037.jpg','06 — יציאה לגג/DSC05038.jpg','06 — יציאה לגג/DJI_20260304175337_0201_D.jpg']},
    {slug:'penthouse-shenkin',name:'דירת גג — שנקין',hero:'06 — יציאה לגג/Edited-8.jpg',meta:{where:'תל אביב',when:'—',arch:'—',product:'יציאה לגג'},images:['06 — יציאה לגג/DSC05055.jpg','06 — יציאה לגג/DSC05046.jpg','06 — יציאה לגג/DSC05040.jpg','06 — יציאה לגג/DSC05059.jpg','06 — יציאה לגג/Edited-8.jpg']},
  ],
  fixed:[
    {slug:'beit-yokra-ta',name:'בית יוקרה — תל אביב',hero:'02 — סקיילייט קבוע/חד שיפועי/בית יוקרה תל אביב/DSC05005.jpg',meta:{where:'תל אביב',when:'—',arch:'—',product:'סקיילייט קבוע, חד שיפועי'},images:['02 — סקיילייט קבוע/חד שיפועי/בית יוקרה תל אביב/DSC05005.jpg','02 — סקיילייט קבוע/חד שיפועי/בית יוקרה תל אביב/DSC05010.jpg','02 — סקיילייט קבוע/חד שיפועי/בית יוקרה תל אביב/DSC05013.jpg']},
    {slug:'mitzpe-hayamim',name:'מלון מצפה הימים',hero:'02 — סקיילייט קבוע/דו שיפועי/מצפה הימים מבט על.jpg',meta:{where:'—',when:'—',arch:'—',product:'סקיילייט קבוע'},images:['02 — סקיילייט קבוע/חד שיפועי/מצפה הימים מסעדה.jpg','02 — סקיילייט קבוע/דו שיפועי/מצפה הימים מבט על.jpg']},
    {slug:'mishya',name:'מסעדת משייה',hero:'02 — סקיילייט קבוע/חד שיפועי/מסעדת משייה.jpg',meta:{where:'—',when:'—',arch:'—',product:'סקיילייט קבוע, חד שיפועי'},images:['02 — סקיילייט קבוע/חד שיפועי/מסעדת משייה.jpg','02 — סקיילייט קבוע/חד שיפועי/מסעדת משייה 2.jpg']},
    {slug:'bar-ilan',name:'מנהלה — אוניברסיטת בר אילן',hero:'02 — סקיילייט קבוע/דו שיפועי/6ב - מנהלה בר אילן.jpg',meta:{where:'רמת גן',when:'—',arch:'—',product:'סקיילייט קבוע, דו שיפועי'},images:['02 — סקיילייט קבוע/דו שיפועי/6ב - מנהלה בר אילן.jpg']},
    {slug:'beit-zait',name:'בית זית',hero:'02 — סקיילייט קבוע/חצר אנגלית/בית זית/DJI_20260311194246_0277_D.jpg',meta:{where:'בית זית',when:'—',arch:'—',product:'סקיילייט קבוע, חצר אנגלית'},images:['02 — סקיילייט קבוע/חצר אנגלית/בית זית/DSC05100.jpg','02 — סקיילייט קבוע/חצר אנגלית/בית זית/DSC05103.jpg','02 — סקיילייט קבוע/חצר אנגלית/בית זית/DSC05105.jpg','02 — סקיילייט קבוע/חצר אנגלית/בית זית/DJI_20260311194246_0277_D.jpg']},
  ],
  walkon:[
    {slug:'national-library',name:'הספריה הלאומית',hero:'03 — סקיילייט מדרך/ספריה לאומית/DSC05088.jpg',meta:{where:'ירושלים',when:'—',arch:'—',product:'סקיילייט מדרך'},images:['03 — סקיילייט מדרך/ספריה לאומית/DSC05082.jpg','03 — סקיילייט מדרך/ספריה לאומית/DSC05085.jpg','03 — סקיילייט מדרך/ספריה לאומית/DSC05086.jpg','03 — סקיילייט מדרך/ספריה לאומית/DSC05088.jpg','03 — סקיילייט מדרך/ספריה לאומית/DSC05090.jpg','03 — סקיילייט מדרך/ספריה לאומית/DSC05094.jpg','03 — סקיילייט מדרך/ספריה לאומית/DSC05095.jpg','03 — סקיילייט מדרך/ספריה לאומית/DSC05096.jpg']},
  ],
  structural:[
    {slug:'recanati-winery',name:'יקב רקנאטי',hero:'04 — מבנים מרחביים/פירמידה/יקב רקנאטי/DJI_20260225203307_0163_D.jpg',meta:{where:'עמק חפר',when:'—',arch:'—',product:'מבנים מרחביים, פירמידה'},images:['04 — מבנים מרחביים/פירמידה/יקב רקנאטי/DSC04979.jpg','04 — מבנים מרחביים/פירמידה/יקב רקנאטי/DSC04981.jpg','04 — מבנים מרחביים/פירמידה/יקב רקנאטי/DSC04988.jpg','04 — מבנים מרחביים/פירמידה/יקב רקנאטי/DSC04994.jpg','04 — מבנים מרחביים/פירמידה/יקב רקנאטי/DJI_20260225203307_0163_D.jpg']},
    {slug:'synagogue',name:'בית כנסת',hero:'04 — מבנים מרחביים/כיפה/בית כנסת/DJI_20260311152443_0235_D.jpg',meta:{where:'—',when:'—',arch:'—',product:'מבנים מרחביים, כיפה'},images:['04 — מבנים מרחביים/כיפה/בית כנסת/DJI_20260311152443_0235_D.jpg']},
    {slug:'atidim',name:'בניין עתידים',hero:'04 — מבנים מרחביים/קשת/סקייליט מקומר בניין עתידים.JPG',meta:{where:'תל אביב',when:'—',arch:'—',product:'מבנים מרחביים, קשת'},images:['04 — מבנים מרחביים/קשת/סקייליט מקומר בניין עתידים.JPG']},
  ],
};

const SELECTED_WORK={
  retractable:['01 — סקיילייט נוסע/חד שיפועי/DOR_6758-HDR.jpg','01 — סקיילייט נוסע/חד שיפועי/DOR_6764-HDR.jpg','01 — סקיילייט נוסע/חד שיפועי/Edited-30.jpg','01 — סקיילייט נוסע/דו שיפועי/Edited-21.jpg','01 — סקיילייט נוסע/דו שיפועי/בית פרטי סקיילייט נוסע .jpg','01 — סקיילייט נוסע/דו שיפועי/בית פרטי סקיילייט נוסע 2.jpg','01 — סקיילייט נוסע/קירוי בריכה/63.jpg','01 — סקיילייט נוסע/קירוי בריכה/65.jpg','01 — סקיילייט נוסע/קירוי בריכה/Edited-27.jpg'],
  smoke:['05 — כיפות תאורה, אוורור ושחרור עשן/13 (1).jpg','05 — כיפות תאורה, אוורור ושחרור עשן/7.jpg','05 — כיפות תאורה, אוורור ושחרור עשן/18.jpg','05 — כיפות תאורה, אוורור ושחרור עשן/22.jpg','05 — כיפות תאורה, אוורור ושחרור עשן/9.jpg','05 — כיפות תאורה, אוורור ושחרור עשן/שחרור עשן.jpg','05 — כיפות תאורה, אוורור ושחרור עשן/בית פרטי חד שיפועי שחרור עשן.jpg','05 — כיפות תאורה, אוורור ושחרור עשן/AlfVjy-ryenVRYXksChGM_1Zu0pUByH44zoXInIzwZqq.jpg'],
  walkon:['03 — סקיילייט מדרך/HP06.jpg','03 — סקיילייט מדרך/13.jpg','03 — סקיילייט מדרך/18.jpg','03 — סקיילייט מדרך/95.jpg','03 — סקיילייט מדרך/סקיילייט מדרך מעל באר ישנה.jpg','03 — סקיילייט מדרך/סקיילייט מדרך 2.jpeg'],
};

const _galReg={};

function goProject(slug){
  // Placeholder until project detail pages ship (next P0).
  // For now: open the project's full image set in the lightbox.
  const pid=Object.keys(PROJECTS).find(p=>PROJECTS[p].some(pr=>pr.slug===slug));
  if(!pid)return;
  const proj=PROJECTS[pid].find(pr=>pr.slug===slug);
  if(!proj)return;
  const key='proj-'+slug;
  const srcs=proj.images.map(s=>B+s);
  const caps=proj.images.map(()=>proj.name);
  _galReg[key]={srcs,caps};
  openLb(key,0);
}

function renderProjectsSection(pid){
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
          <dt>מיקום</dt><dd>${m.where||'—'}</dd>
          <dt>שנה</dt><dd>${m.when||'—'}</dd>
          <dt>אדריכל</dt><dd>${m.arch||'—'}</dd>
          <dt>מוצר</dt><dd>${m.product||'—'}</dd>
        </dl>
        <a class="pp-proj-card-link" href="#project/${p.slug}" onclick="goProject('${p.slug}');return false">צפו בפרויקט ${arrow}</a>
      </div>
    </div>`);
  });
  sec.innerHTML=out.join('');
}

function renderSelectedWork(pid){
  const sec=document.getElementById('selwork-'+pid);
  if(!sec)return;
  const imgs=SELECTED_WORK[pid];
  if(!imgs||!imgs.length){sec.style.display='none';return}
  const key='selwork-'+pid;
  const srcs=imgs.map(s=>B+s);
  const caps=imgs.map(()=>'');
  _galReg[key]={srcs,caps};
  const out=[`<div class="pp-selected-work-h"><div class="pp-projects-section-eye">גלריה</div><h2 class="pp-projects-section-t">עבודות נבחרות</h2></div>`,`<div class="pp-selected-work-grid">`];
  imgs.forEach((src,i)=>{
    out.push(`<div class="pp-selected-work-item" onclick="openLb('${key}',${i})"><img src="${B}${src}" alt="" loading="lazy"></div>`);
  });
  out.push('</div>');
  sec.innerHTML=out.join('');
}

// Init
['penthouse','fixed','walkon','structural'].forEach(renderProjectsSection);
['retractable','smoke','walkon'].forEach(renderSelectedWork);

"""

if idx_start >= 0 and idx_end >= 0:
    # Splice: keep everything before subTab, drop subTab..Init-loop-trailing-blank, prepend NEW_JS, then the lightbox comment onward.
    # idx_end points to the start of '});\n\n// ── Lightbox ──'. We consume '});\n\n' (5 chars) so the "// ── Lightbox ──" line is preserved.
    consumed = len('});\n\n')
    html = html[:idx_start] + NEW_JS + html[idx_end + consumed:]
    print('✅ Replaced old gallery JS with PROJECTS + renderers')
    changes += 1
elif 'const PROJECTS=' in html:
    print('ℹ️  PROJECTS engine already in place')
else:
    print(f'⚠️  Could not locate old JS range (start={idx_start}, end={idx_end})')

# ──────────────────────────────────────────────────────────────────────
# Save
# ──────────────────────────────────────────────────────────────────────
if changes:
    open(PATH, 'w', encoding='utf-8').write(html)
    print(f'\n━━ {changes} change(s) saved to index.html')
    print('Next: git add index.html && git commit -m "Restructure product pages: editorial projects section" && git push')
else:
    print('\n━━ No changes made (idempotent re-run)')
