#!/usr/bin/env python3
"""apply-walkon-pilot.py — Pilot the new product-page structure on walk-on.

Changes in one pass (all idempotent):

  A. CSS — media strip grid (images+videos mixed, bottom-gradient overlay
           captions) + project detail page styles.
  B. HTML — swap walk-on page order: media strip above, chosen projects below.
           Replace <pp-selected-work id="selwork-walkon"> with new
           <pp-media id="media-walkon">.
  C. HTML — new project detail page template for "הספריה הלאומית"
           (<div id="page-project-national-library" class="pp">).
  D. JS  — new MEDIA data + autoCap() + renderMedia() + renderProjectGallery().
  E. JS  — update goProject() to navigate to project detail pages (not lightbox);
           update go() to also hide project pages; register 'project-*' ids.
  F. JS  — init wiring: add renderMedia('walkon'), remove old walk-on
           SELECTED_WORK entry so there's one source of truth.
  G. JS  — enrich PROJECTS.walkon[0] with fuller image list (all 34) and a
           placeholder description marked [TODO] for Ohad to replace.

After running, the walk-on page should:
  1. Show hero + description (unchanged)
  2. Show curated media strip (8 images with overlays where relevant)
  3. Show chosen projects (National Library card)
  4. Clicking the project card → navigates to the full detail page

National Library detail page TODOs (marked inline):
  • Real year
  • Architect name
  • 2-3 sentence project description

Preview:
  cd ~/Downloads/skylite-github && python3 -m http.server 8080
  → http://localhost:8080/#walkon
"""
import sys, pathlib

HTML = pathlib.Path(__file__).parent / "index.html"
src  = HTML.read_text(encoding="utf-8")
changes = 0

def swap(old, new, label):
    global src, changes
    if new in src:
        print(f"✔  {label} — already applied, skipping")
        return
    if old not in src:
        print(f"❌ {label} — anchor not found; aborting")
        sys.exit(1)
    src = src.replace(old, new, 1)
    changes += 1
    print(f"✔  {label}")

# ══════════════════════════════════════════════════════════════════
# A. CSS — media strip + project detail page styles
# ══════════════════════════════════════════════════════════════════
CSS_ANCHOR = "    .pp-selected-work-item:hover img{transform:scale(1.04);filter:brightness(1) saturate(1.1)}"
CSS_ADD = CSS_ANCHOR + """

    /* ── MEDIA STRIP (new pattern) ── */
    .pp-media{background:var(--cream);padding:100px 0 120px}
    .pp-media-h{padding:0 80px;margin-bottom:48px}
    .pp-media-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:0 80px}
    .pp-media-item{position:relative;aspect-ratio:4/3;overflow:hidden;border-radius:6px;background:var(--dark);cursor:pointer}
    .pp-media-item>img{width:100%;height:100%;object-fit:cover;transition:transform 1s var(--spring),filter 1s var(--spring);filter:brightness(.94) saturate(1.04)}
    .pp-media-item:hover>img{transform:scale(1.04);filter:brightness(1) saturate(1.1)}
    .pp-media-item.pp-media-vid>img{filter:brightness(.84)}
    .pp-media-item.pp-media-vid:hover>img{filter:brightness(.98)}
    .pp-media-item .mp-play{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:56px;height:56px;pointer-events:none;transition:transform .4s var(--spring);filter:drop-shadow(0 4px 16px rgba(0,0,0,.5))}
    .pp-media-item:hover .mp-play{transform:translate(-50%,-50%) scale(1.08)}
    .pp-media-cap{position:absolute;left:0;right:0;bottom:0;padding:26px 16px 14px 16px;color:#fff;font-size:12px;font-weight:400;letter-spacing:.10em;background:linear-gradient(180deg,transparent,rgba(0,0,0,.62));pointer-events:none;direction:rtl;opacity:.88;transition:opacity .3s}
    .pp-media-item:hover .pp-media-cap{opacity:1}
    @media(max-width:1024px){.pp-media{padding:70px 0 80px}.pp-media-h,.pp-media-grid{padding:0 48px}.pp-media-grid{grid-template-columns:repeat(2,1fr)}}
    @media(max-width:600px){.pp-media{padding:48px 0 56px}.pp-media-h,.pp-media-grid{padding:0 24px}.pp-media-grid{grid-template-columns:1fr}.pp-media-item .mp-play{width:48px;height:48px}}

    /* ── PROJECT DETAIL PAGE ── */
    .pp-project-intro{padding:100px 80px 40px;max-width:1120px;margin:0 auto;display:grid;grid-template-columns:1fr 1.6fr;gap:64px;align-items:start}
    .pp-project-intro-meta{display:grid;grid-template-columns:auto 1fr;gap:18px 32px;margin:0}
    .pp-project-intro-meta dt{font-size:11px;font-weight:400;letter-spacing:.22em;color:var(--stone);text-transform:uppercase;padding-top:4px;white-space:nowrap}
    .pp-project-intro-meta dd{font-size:16px;font-weight:400;color:var(--dark);margin:0;line-height:1.5}
    .pp-project-intro-desc p{font-size:17px;font-weight:300;line-height:1.85;color:var(--stone);margin:0 0 20px}
    .pp-project-intro-desc p:last-child{margin-bottom:0}
    .pp-todo{background:rgba(255,200,60,.22);color:var(--dark);padding:1px 8px;border-radius:3px;font-weight:500}
    .pp-project-gallery{padding:40px 80px 120px}
    .pp-project-gallery .pp-media-grid{padding:0}
    @media(max-width:1024px){.pp-project-intro{grid-template-columns:1fr;gap:32px;padding:64px 48px 24px}.pp-project-gallery{padding:24px 48px 80px}}
    @media(max-width:600px){.pp-project-intro{padding:48px 24px 16px;gap:24px}.pp-project-gallery{padding:16px 24px 56px}}

"""
swap(CSS_ANCHOR + "\n", CSS_ADD, "CSS: media strip + project detail styles")

# ══════════════════════════════════════════════════════════════════
# B. HTML — swap walk-on section order + rename selwork → media
# ══════════════════════════════════════════════════════════════════
OLD_WALKON = '''<section class="pp-projects-section" id="projects-sec-walkon"></section>
<section class="pp-selected-work" id="selwork-walkon"></section>'''
NEW_WALKON = '''<section class="pp-media" id="media-walkon"></section>
<section class="pp-projects-section" id="projects-sec-walkon"></section>'''
swap(OLD_WALKON, NEW_WALKON, "HTML: walk-on section order (strip above, projects below)")

# ══════════════════════════════════════════════════════════════════
# C. HTML — insert project detail page (National Library) before STRUCTURAL
# ══════════════════════════════════════════════════════════════════
PROJECT_NAV = '''<nav class="nav scrolled"><div class="nav-logo"><svg viewBox="0 0 50 50" width="36" height="36" fill="none"><rect width="50" height="50" fill="#E9EEF2"/><path d="M26,0 L50,0 L50,50 L0,50 L0,40 C3,30 18,10 26,0Z" fill="#1A1E24"/></svg><span class="nav-wordmark">SKYLITE</span></div><a href="#" class="nav-back" onclick="go(\'walkon\');return false"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M13 8H3M7 12l-4-4 4-4"/></svg>חזרה לסקיילייט מדרך</a><a href="#" class="nav-cta" onclick="openCM();return false">צור קשר</a></nav>'''

PROJECT_FOOTER = '''<footer><div class="f-brand"><svg viewBox="0 0 50 50" width="32" fill="none"><rect width="50" height="50" fill="#1A1E24"/><path d="M26,0 L50,0 L50,50 L0,50 L0,40 C3,30 18,10 26,0Z" fill="#E9EEF2"/></svg><div class="f-name">Skylite</div><div class="f-tag">הנדסת הטבע<br>האור שחותך את החלל — מ-1986</div></div><div class="f-links"><a href="#" onclick="home();return false">← חזרה לדף הבית</a><a href="#" onclick="go(\'walkon\');return false">סקיילייט מדרך</a><a href="#" onclick="go(\'fixed\');return false">סקיילייט קבוע</a><a href="#" onclick="go(\'retractable\');return false">סקיילייט נוסע</a><a href="#" onclick="go(\'tech\');return false">מידע טכני</a></div><div class="f-contact"><p><strong>סקיילייט בע"מ</strong></p><p>אלכסנדר ינאי 8, א.ת סגולה, פתח תקווה</p><p>טל: 03-9343159 | פקס: 03-9311921</p><p>skylite@skylite.co.il</p><p style="margin-top:8px">שעות פעילות: ראשון–חמישי 9:00–18:00</p><p>שישי–שבת: סגור | הגעה בתיאום מראש</p><p style="margin-top:10px"><a href="https://instagram.com/skyliteisrael/" target="_blank" rel="noopener" style="color:var(--accent-pale);text-decoration:none;font-size:12px;letter-spacing:.06em">Instagram — @skyliteisrael</a></p></div></footer>'''

PROJECT_PAGE = f'''
<!-- ════ PROJECT: National Library ════ -->
<div id="page-project-national-library" class="pp">
{PROJECT_NAV}
<section class="pp-hero"><img src="./מוצרים מסווגים/03 — סקיילייט מדרך/ספריה לאומית/DSC05088.jpg" alt="הספריה הלאומית — סקיילייט מדרך"><div class="pp-hero-ov"></div><div class="pp-hero-c"><div class="pp-hero-cat">Project · Walk-On Glass</div><h1 class="pp-hero-name">הספריה הלאומית</h1><div class="pp-hero-tag">ירושלים · סקיילייט מדרך מעל אולם הקריאה</div></div></section>
<section class="pp-project-intro">
  <dl class="pp-project-intro-meta rv">
    <dt>מיקום</dt><dd>ירושלים</dd>
    <dt>שנה</dt><dd><span class="pp-todo">[Ohad — שנה]</span></dd>
    <dt>אדריכל</dt><dd><span class="pp-todo">[Ohad — אדריכל]</span></dd>
    <dt>מוצר</dt><dd>סקיילייט מדרך</dd>
  </dl>
  <div class="pp-project-intro-desc rv rv-d1">
    <p><span class="pp-todo">[TODO — Ohad to replace with 2-3 sentences about the project: the challenge, what we engineered, the outcome.]</span></p>
    <p>סקיילייט מדרך מעל אולם הקריאה — מאפשר חדירת אור טבעי עמוק לתוך המבנה, תוך שמירה על משטח הליכה בטיחותי ברצפה שמעל.</p>
  </div>
</section>
<section class="pp-project-gallery" id="project-gal-national-library"></section>
<section class="pp-cta"><h2 class="rv">מתכננים פרויקט דומה?<br><em>נשמח להיפגש</em></h2><div class="cta-acts rv rv-d1"><button class="btn-pd" onclick="openCM()">השאירו פרטים</button><a href="tel:+97239343159" class="btn-od">טלפון: 03-9343159</a></div></section>
{PROJECT_FOOTER}
</div>

<!-- ════ STRUCTURAL ════ -->'''

swap("\n<!-- ════ STRUCTURAL ════ -->", PROJECT_PAGE, "HTML: National Library project detail page")

# ══════════════════════════════════════════════════════════════════
# D. JS — MEDIA data + autoCap + renderMedia + renderProjectGallery
# ══════════════════════════════════════════════════════════════════
JS_ANCHOR = "const _galReg={};"
JS_ADD = """const _galReg={};

// ── MEDIA: curated strip per product page (images + videos mixed).
// Each entry: { type:'img'|'vid', src:path, poster?:path, cap?:string }
// Captions are auto-derived from the immediate parent folder via autoCap().
// Provide `cap:` explicitly to override, or `cap:''` to force no caption.
const MEDIA = {
  walkon: [
    { type:'img', src:'03 — סקיילייט מדרך/Hero-topaz-upscale-2x-denoise-sharpen-color-lighting.jpg' },
    { type:'img', src:'03 — סקיילייט מדרך/ספריה לאומית/DSC05082.jpg', cap:'הספריה הלאומית' },
    { type:'img', src:'03 — סקיילייט מדרך/ספריה לאומית/DSC05088.jpg', cap:'הספריה הלאומית' },
    { type:'img', src:'03 — סקיילייט מדרך/HP06.jpg' },
    { type:'img', src:'03 — סקיילייט מדרך/ספריה לאומית/DSC05094.jpg', cap:'הספריה הלאומית' },
    { type:'img', src:'03 — סקיילייט מדרך/ספריה לאומית/DSC05096.jpg', cap:'הספריה הלאומית' },
    { type:'img', src:'03 — סקיילייט מדרך/סקיילייט מדרך מעל באר ישנה.jpg', cap:'סקיילייט מעל באר ישנה' },
    { type:'img', src:'03 — סקיילייט מדרך/13.jpg' },
  ],
  // penthouse/fixed/retractable/structural/smoke come next
};

// Auto-derive overlay caption from image path.
// Rule: use the second-to-last path segment (immediate parent folder).
// Skip generic folders (anything that would be redundant with the page itself).
const _CAP_SKIP = new Set(['כללי', 'חלונות סקיילייט', 'חד שיפועי', 'דו שיפועי', 'חצר אנגלית', 'קירוי בריכה', 'חרוט', 'כיפה', 'פירמידה', 'קשת']);
function autoCap(src){
  const parts = src.split('/');
  if(parts.length <= 2) return '';
  const parent = parts[parts.length - 2];
  if(_CAP_SKIP.has(parent)) return '';
  return parent;
}
function _effCap(item){ return item.cap !== undefined ? item.cap : autoCap(item.src); }

function renderMedia(pid){
  const sec = document.getElementById('media-'+pid);
  if(!sec) return;
  const items = MEDIA[pid];
  if(!items || !items.length){ sec.style.display='none'; return; }
  const key = 'media-'+pid;
  const srcs  = items.map(it => it.type === 'vid' ? VB+it.src : B+it.src);
  const caps  = items.map(_effCap);
  const kinds = items.map(it => it.type === 'vid' ? 'vid' : 'img');
  _galReg[key] = { srcs, caps, kinds };

  const playIcon = '<svg class=\"mp-play\" viewBox=\"0 0 64 64\"><circle cx=\"32\" cy=\"32\" r=\"30\" fill=\"rgba(0,0,0,.38)\"/><path d=\"M26 20 L46 32 L26 44 Z\" fill=\"#fff\"/></svg>';
  const out = [`<div class=\"pp-media-h\"><div class=\"pp-projects-section-eye\">גלריה</div><h2 class=\"pp-projects-section-t\">עבודות נבחרות</h2></div>`, `<div class=\"pp-media-grid\">`];
  items.forEach((it,i) => {
    const cap = _effCap(it);
    const capHtml = cap ? `<div class=\"pp-media-cap\">${cap}</div>` : '';
    if(it.type === 'vid'){
      const poster = it.poster ? VB+it.poster : '';
      out.push(`<div class=\"pp-media-item pp-media-vid\" onclick=\"openLb('${key}',${i})\"><img src=\"${poster}\" alt=\"\" loading=\"lazy\">${playIcon}${capHtml}</div>`);
    } else {
      out.push(`<div class=\"pp-media-item\" onclick=\"openLb('${key}',${i})\"><img src=\"${B}${it.src}\" alt=\"\" loading=\"lazy\">${capHtml}</div>`);
    }
  });
  out.push('</div>');
  sec.innerHTML = out.join('');
}

// Render the full image gallery on a project detail page.
function renderProjectGallery(slug){
  const pid = Object.keys(PROJECTS).find(p => PROJECTS[p].some(pr => pr.slug === slug));
  if(!pid) return;
  const proj = PROJECTS[pid].find(pr => pr.slug === slug);
  const sec = document.getElementById('project-gal-'+slug);
  if(!sec || !proj.images || !proj.images.length) return;
  const key = 'projgal-'+slug;
  const srcs = proj.images.map(s => B+s);
  const caps = proj.images.map(() => proj.name);
  const kinds = srcs.map(() => 'img');
  _galReg[key] = { srcs, caps, kinds };
  const tiles = proj.images.map((src,i) =>
    `<div class=\"pp-media-item\" onclick=\"openLb('${key}',${i})\"><img src=\"${B}${src}\" alt=\"\" loading=\"lazy\"></div>`
  ).join('');
  sec.innerHTML = `<div class=\"pp-media-grid\">${tiles}</div>`;
}

"""
swap(JS_ANCHOR + "\n", JS_ADD, "JS: MEDIA + autoCap + renderMedia + renderProjectGallery")

# ══════════════════════════════════════════════════════════════════
# E. JS — update goProject to navigate; update go() to hide project pages
# ══════════════════════════════════════════════════════════════════
OLD_GOPROJECT = '''function goProject(slug){
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
}'''

NEW_GOPROJECT = '''function goProject(slug){
  // Navigate to the project detail page. Falls back to lightbox if the detail
  // page doesn't exist yet (only National Library has one as of the pilot).
  const targetId = 'page-project-'+slug;
  const target = document.getElementById(targetId);
  if(!target){
    // Fallback: open the project's images in the lightbox.
    const pid=Object.keys(PROJECTS).find(p=>PROJECTS[p].some(pr=>pr.slug===slug));
    if(!pid) return;
    const proj=PROJECTS[pid].find(pr=>pr.slug===slug);
    if(!proj) return;
    const key='proj-'+slug;
    const srcs=proj.images.map(s=>B+s);
    const caps=proj.images.map(()=>proj.name);
    _galReg[key]={srcs,caps,kinds:srcs.map(()=>'img')};
    openLb(key,0);
    return;
  }
  // Hide all product pages and project pages
  pages.forEach(p => { const el=document.getElementById('page-'+p); if(el){ el.style.display='none'; el.classList.remove('active'); }});
  document.querySelectorAll('[id^=\"page-project-\"]').forEach(el => { el.style.display='none'; el.classList.remove('active'); });
  // Show the target project page
  target.style.display='block';
  target.classList.add('active');
  window.scrollTo({top:0,behavior:'smooth'});
  renderProjectGallery(slug);
  setTimeout(()=>{ target.querySelectorAll('.rv:not(.on)').forEach(el=>obs.observe(el)) }, 100);
}'''
swap(OLD_GOPROJECT, NEW_GOPROJECT, "JS: goProject navigates to detail page")

# Update go() to hide project pages too when switching product pages
OLD_GO = '''function go(id){pages.forEach(p=>{const el=document.getElementById('page-'+p);if(el){el.style.display='none';el.classList.remove('active')}});const t=document.getElementById('page-'+id);if(t){t.style.display='block';t.classList.add('active');window.scrollTo({top:0,behavior:'smooth'});setTimeout(()=>{t.querySelectorAll('.rv:not(.on)').forEach(el=>obs.observe(el))},100)}}'''

NEW_GO = '''function go(id){pages.forEach(p=>{const el=document.getElementById('page-'+p);if(el){el.style.display='none';el.classList.remove('active')}});document.querySelectorAll('[id^="page-project-"]').forEach(el=>{el.style.display='none';el.classList.remove('active')});const t=document.getElementById('page-'+id);if(t){t.style.display='block';t.classList.add('active');window.scrollTo({top:0,behavior:'smooth'});setTimeout(()=>{t.querySelectorAll('.rv:not(.on)').forEach(el=>obs.observe(el))},100)}}'''
swap(OLD_GO, NEW_GO, "JS: go() also hides project pages")

# ══════════════════════════════════════════════════════════════════
# F. JS — init: add renderMedia('walkon'), remove walkon from renderSelectedWork
# ══════════════════════════════════════════════════════════════════
swap(
    "['retractable','smoke','walkon'].forEach(renderSelectedWork);",
    "['retractable','smoke'].forEach(renderSelectedWork);\n['walkon'].forEach(renderMedia);",
    "JS: init — walkon uses renderMedia, no longer renderSelectedWork"
)

# Also remove SELECTED_WORK.walkon entry so there's one source of truth
swap(
    "  walkon:['03 — סקיילייט מדרך/HP06.jpg','03 — סקיילייט מדרך/13.jpg','03 — סקיילייט מדרך/18.jpg','03 — סקיילייט מדרך/95.jpg','03 — סקיילייט מדרך/סקיילייט מדרך מעל באר ישנה.jpg','03 — סקיילייט מדרך/סקיילייט מדרך 2.jpeg'],\n",
    "",
    "JS: remove SELECTED_WORK.walkon (replaced by MEDIA.walkon)"
)

# ══════════════════════════════════════════════════════════════════
# G. JS — enrich PROJECTS.walkon[0] (National Library) with all 34 images
# ══════════════════════════════════════════════════════════════════
NL_FOLDER = "03 — סקיילייט מדרך/ספריה לאומית"
NL_FILES = [
    "DSC05079.jpg", "DSC05080.jpg", "DSC05081.jpg", "DSC05082.jpg",
    "DSC05083.jpg", "DSC05084.jpg", "DSC05085.jpg", "DSC05086.jpg",
    "DSC05087.jpg", "DSC05088.jpg", "DSC05089.jpg", "DSC05090.jpg",
    "DSC05091.jpg", "DSC05092.jpg", "DSC05093.jpg", "DSC05094.jpg",
    "DSC05095.jpg", "DSC05096.jpg", "DSC05098.jpg", "DSC05099.jpg",
    "IMG_20260311_120147_194.jpg", "IMG_20260311_120152_195.jpg",
    "IMG_20260311_120738_205.jpg", "IMG_20260311_120811_206.jpg",
    "IMG_20260311_120823_207.jpg", "IMG_20260311_122620_220.jpg",
    "IMG_20260311_122629_221.jpg", "IMG_20260311_122640_222.jpg",
    "IMG_20260311_122647_223.jpg", "IMG_20260311_122711_224.jpg",
    "IMG_20260311_124140_234.jpg", "IMG_20260311_124148_235.jpg",
    "IMG_20260311_124208_237.jpg", "IMG_20260311_124216_238.jpg",
]
NL_IMAGES_JS = ",".join(f"'{NL_FOLDER}/{f}'" for f in NL_FILES)

OLD_NL = "{slug:'national-library',name:'הספריה הלאומית',hero:'03 — סקיילייט מדרך/ספריה לאומית/DSC05088.jpg',meta:{where:'ירושלים',when:'—',arch:'—',product:'סקיילייט מדרך'},images:['03 — סקיילייט מדרך/ספריה לאומית/DSC05082.jpg','03 — סקיילייט מדרך/ספריה לאומית/DSC05085.jpg','03 — סקיילייט מדרך/ספריה לאומית/DSC05086.jpg','03 — סקיילייט מדרך/ספריה לאומית/DSC05088.jpg','03 — סקיילייט מדרך/ספריה לאומית/DSC05090.jpg','03 — סקיילייט מדרך/ספריה לאומית/DSC05094.jpg','03 — סקיילייט מדרך/ספריה לאומית/DSC05095.jpg','03 — סקיילייט מדרך/ספריה לאומית/DSC05096.jpg']}"
NEW_NL = (
    "{slug:'national-library',name:'הספריה הלאומית',"
    "hero:'03 — סקיילייט מדרך/ספריה לאומית/DSC05088.jpg',"
    "meta:{where:'ירושלים',when:'—',arch:'—',product:'סקיילייט מדרך'},"
    f"images:[{NL_IMAGES_JS}]}}"
)
swap(OLD_NL, NEW_NL, "JS: enrich National Library with all 34 images")

# ══════════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — everything already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
    print("   Preview: python3 -m http.server 8080 → http://localhost:8080/#walkon")
