#!/usr/bin/env python3
"""apply-walkon-pilot-v2.py — Catch walk-on up with the new folder structure.

Changes since v1 (apply-walkon-pilot.py):
  • MEDIA.walkon rebuilt from the post-reorg folder (v1 referenced files that
    no longer exist: Hero-topaz-…, 13.jpg, old-well loose shots, etc.)
  • New project: "בית הבאר — מבנה לשימור"   (5 files) + detail page
  • New project: "HP HQ — בניין מרקורי"     (3 files) + detail page
  • renderProjectGallery gains optional filename-hint captions — for images
    like `קבוע - חד שיפועי.jpg` inside a walk-on project folder, the gallery
    overlay reads "סקיילייט קבוע · חד שיפועי" so mixed-product projects make
    clear which skylight is which.

Mixed-product project handling (flagged, not fully automated yet):
  • Each project has a `products:` array — the product pages it can appear on.
  • HP HQ is currently `products:['walkon','fixed']` — when the fixed page
    gets its pattern rolled out, HP HQ shows up there too. For now it only
    renders on walk-on's projects section (no harm — fixed page hasn't been
    migrated yet).

Idempotent (re-run safe). Requires v1 (apply-walkon-pilot.py) already run.
"""
import sys, pathlib, re

HTML = pathlib.Path(__file__).parent / "index.html"
src  = HTML.read_text(encoding="utf-8")
changes = 0

def swap(old, new, label, allow_noop_new=False):
    global src, changes
    if not allow_noop_new and new and new in src:
        print(f"✔  {label} — already applied, skipping")
        return
    if old not in src:
        print(f"❌ {label} — anchor not found; aborting")
        sys.exit(1)
    src = src.replace(old, new, 1)
    changes += 1
    print(f"✔  {label}")

def swap_regex(pattern, new, label):
    """Replace a regex match (used when old text has variable content)."""
    global src, changes
    if new in src:
        print(f"✔  {label} — already applied, skipping")
        return
    m = re.search(pattern, src, re.DOTALL)
    if not m:
        print(f"❌ {label} — regex anchor not found; aborting")
        sys.exit(1)
    src = src[:m.start()] + new + src[m.end():]
    changes += 1
    print(f"✔  {label}")

# ══════════════════════════════════════════════════════════════════
# 1. MEDIA.walkon — rebuild from current folder contents
# ══════════════════════════════════════════════════════════════════
# Match the entire MEDIA.walkon array (from opening `walkon: [` to matching `],`)
MEDIA_WALKON_NEW = """  walkon: [
    { type:'img', src:'03 — סקיילייט מדרך/Hero Banner .jpg' },
    { type:'img', src:'03 — סקיילייט מדרך/HP06.jpg' },
    { type:'img', src:'03 — סקיילייט מדרך/ספריה לאומית/DSC05088.jpg', cap:'הספריה הלאומית' },
    { type:'img', src:'03 — סקיילייט מדרך/ספריה לאומית/DSC05082.jpg', cap:'הספריה הלאומית' },
    { type:'img', src:'03 — סקיילייט מדרך/ספריה לאומית/DSC05094.jpg', cap:'הספריה הלאומית' },
    { type:'img', src:'03 — סקיילייט מדרך/95.jpg' },
    { type:'img', src:'03 — סקיילייט מדרך/HP HQ - בניין מרקורי/269.jpg', cap:'HP HQ — בניין מרקורי' },
    { type:'img', src:'03 — סקיילייט מדרך/בית הבאר - מבנה לשימור/בית הבאר - מבנה לשימור.jpg', cap:'בית הבאר — מבנה לשימור' },
  ],"""
swap_regex(
    r"  walkon: \[\n(?:    \{[^\n]+\n)+  \],",
    MEDIA_WALKON_NEW,
    "JS: rebuild MEDIA.walkon from current folder"
)

# ══════════════════════════════════════════════════════════════════
# 2. PROJECTS.walkon — append two new projects
# ══════════════════════════════════════════════════════════════════
# The existing walkon array has only National Library. We append the two new
# projects before the closing `]`.
NL_HERO = "03 — סקיילייט מדרך/ספריה לאומית/DSC05088.jpg"
WELL_FILES = [
    "בית הבאר - מבנה לשימור.jpg",
    "Hero copy.jpg",
    "סקיילייט מדרך מעל באר ישנה.jpg",
    "סקיילייט מדרך מעל באר ישנה 3.jpg",
    "סקיילייט מדרך מעל באר ישנה 4.jpg",
]
WELL_IMGS = ",".join(f"'03 — סקיילייט מדרך/בית הבאר - מבנה לשימור/{f}'" for f in WELL_FILES)
WELL_PROJECT = (
    "{slug:'well-house',name:'בית הבאר — מבנה לשימור',"
    "hero:'03 — סקיילייט מדרך/בית הבאר - מבנה לשימור/בית הבאר - מבנה לשימור.jpg',"
    "meta:{where:'—',when:'—',arch:'—',product:'סקיילייט מדרך'},"
    "products:['walkon'],"
    f"images:[{WELL_IMGS}]}}"
)

HP_FILES = ["269.jpg", "קבוע - חד שיפועי.jpg", "קבוע - חד שיפועי.png"]
HP_IMGS = ",".join(f"'03 — סקיילייט מדרך/HP HQ - בניין מרקורי/{f}'" for f in HP_FILES)
HP_PROJECT = (
    "{slug:'hp-hq-mercury',name:'HP HQ — בניין מרקורי',"
    "hero:'03 — סקיילייט מדרך/HP HQ - בניין מרקורי/269.jpg',"
    "meta:{where:'—',when:'—',arch:'—',product:'סקיילייט מדרך + קבוע'},"
    "products:['walkon','fixed'],"
    f"images:[{HP_IMGS}]}}"
)

# Extend the existing walkon: [...] in PROJECTS
OLD_WALKON_CLOSE = "meta:{where:'ירושלים',when:'—',arch:'—',product:'סקיילייט מדרך'},images:["
# We find the National Library entry's closing `]}` (right before `],` for walkon)
# The cleanest way: add new entries after the NL entry and before the closing `],`
# Search for `]}\n  ],\n  structural:` (end of walkon block)
OLD_END = "]},\n  ],\n  structural:["
NEW_END = f"]}},\n    {WELL_PROJECT},\n    {HP_PROJECT},\n  ],\n  structural:["
swap(OLD_END, NEW_END, "JS: append well-house + hp-hq-mercury to PROJECTS.walkon")

# ══════════════════════════════════════════════════════════════════
# 3. Project detail page template — reusable generator
# ══════════════════════════════════════════════════════════════════
PROJECT_NAV = '''<nav class="nav scrolled"><div class="nav-logo"><svg viewBox="0 0 50 50" width="36" height="36" fill="none"><rect width="50" height="50" fill="#E9EEF2"/><path d="M26,0 L50,0 L50,50 L0,50 L0,40 C3,30 18,10 26,0Z" fill="#1A1E24"/></svg><span class="nav-wordmark">SKYLITE</span></div><a href="#" class="nav-back" onclick="go(\'walkon\');return false"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M13 8H3M7 12l-4-4 4-4"/></svg>חזרה לסקיילייט מדרך</a><a href="#" class="nav-cta" onclick="openCM();return false">צור קשר</a></nav>'''

PROJECT_FOOTER = '''<footer><div class="f-brand"><svg viewBox="0 0 50 50" width="32" fill="none"><rect width="50" height="50" fill="#1A1E24"/><path d="M26,0 L50,0 L50,50 L0,50 L0,40 C3,30 18,10 26,0Z" fill="#E9EEF2"/></svg><div class="f-name">Skylite</div><div class="f-tag">הנדסת הטבע<br>האור שחותך את החלל — מ-1986</div></div><div class="f-links"><a href="#" onclick="home();return false">← חזרה לדף הבית</a><a href="#" onclick="go(\'walkon\');return false">סקיילייט מדרך</a><a href="#" onclick="go(\'fixed\');return false">סקיילייט קבוע</a><a href="#" onclick="go(\'retractable\');return false">סקיילייט נוסע</a><a href="#" onclick="go(\'tech\');return false">מידע טכני</a></div><div class="f-contact"><p><strong>סקיילייט בע"מ</strong></p><p>אלכסנדר ינאי 8, א.ת סגולה, פתח תקווה</p><p>טל: 03-9343159 | פקס: 03-9311921</p><p>skylite@skylite.co.il</p><p style="margin-top:8px">שעות פעילות: ראשון–חמישי 9:00–18:00</p><p>שישי–שבת: סגור | הגעה בתיאום מראש</p><p style="margin-top:10px"><a href="https://instagram.com/skyliteisrael/" target="_blank" rel="noopener" style="color:var(--accent-pale);text-decoration:none;font-size:12px;letter-spacing:.06em">Instagram — @skyliteisrael</a></p></div></footer>'''

def project_page_html(slug, name, hero_path, where, product_label, tagline):
    return f'''
<!-- ════ PROJECT: {slug} ════ -->
<div id="page-project-{slug}" class="pp">
{PROJECT_NAV}
<section class="pp-hero"><img src="./מוצרים מסווגים/{hero_path}" alt="{name}"><div class="pp-hero-ov"></div><div class="pp-hero-c"><div class="pp-hero-cat">Project · Walk-On Glass</div><h1 class="pp-hero-name">{name}</h1><div class="pp-hero-tag">{tagline}</div></div></section>
<section class="pp-project-intro">
  <dl class="pp-project-intro-meta rv">
    <dt>מיקום</dt><dd>{where or '<span class="pp-todo">[Ohad — מיקום]</span>'}</dd>
    <dt>שנה</dt><dd><span class="pp-todo">[Ohad — שנה]</span></dd>
    <dt>אדריכל</dt><dd><span class="pp-todo">[Ohad — אדריכל]</span></dd>
    <dt>מוצר</dt><dd>{product_label}</dd>
  </dl>
  <div class="pp-project-intro-desc rv rv-d1">
    <p><span class="pp-todo">[TODO — Ohad: 2-3 sentences about the project: the challenge, what we engineered, the outcome.]</span></p>
  </div>
</section>
<section class="pp-project-gallery" id="project-gal-{slug}"></section>
<section class="pp-cta"><h2 class="rv">מתכננים פרויקט דומה?<br><em>נשמח להיפגש</em></h2><div class="cta-acts rv rv-d1"><button class="btn-pd" onclick="openCM()">השאירו פרטים</button><a href="tel:+97239343159" class="btn-od">טלפון: 03-9343159</a></div></section>
{PROJECT_FOOTER}
</div>
'''

WELL_PAGE = project_page_html(
    slug='well-house',
    name='בית הבאר — מבנה לשימור',
    hero_path='03 — סקיילייט מדרך/בית הבאר - מבנה לשימור/בית הבאר - מבנה לשימור.jpg',
    where='—',
    product_label='סקיילייט מדרך',
    tagline='אתר שימור · סקיילייט מדרך מעל הבאר ההיסטורית',
)

HP_PAGE = project_page_html(
    slug='hp-hq-mercury',
    name='HP HQ — בניין מרקורי',
    hero_path='03 — סקיילייט מדרך/HP HQ - בניין מרקורי/269.jpg',
    where='—',
    product_label='סקיילייט מדרך + קבוע',
    tagline='בניין משרדים · סקיילייט מדרך וסקיילייט קבוע',
)

# Insert both new project pages immediately after the existing national-library
# page and before the "<!-- ════ STRUCTURAL ════ -->" marker.
OLD_BEFORE_STRUCTURAL = "\n<!-- ════ STRUCTURAL ════ -->"
NEW_BEFORE_STRUCTURAL = WELL_PAGE + HP_PAGE + "\n<!-- ════ STRUCTURAL ════ -->"
swap(OLD_BEFORE_STRUCTURAL, NEW_BEFORE_STRUCTURAL, "HTML: well-house + hp-hq-mercury detail pages")

# ══════════════════════════════════════════════════════════════════
# 4. Enhance renderProjectGallery with filename-hint captions
# ══════════════════════════════════════════════════════════════════
OLD_RPG = '''// Render the full image gallery on a project detail page.
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
    `<div class="pp-media-item" onclick="openLb('${key}',${i})"><img src="${B}${src}" alt="" loading="lazy"></div>`
  ).join('');
  sec.innerHTML = `<div class="pp-media-grid">${tiles}</div>`;
}'''

NEW_RPG = """// Filename-based product-type hints for mixed-product projects.
// Example: an image named \"קבוע - חד שיפועי.jpg\" inside a walk-on project
// folder tells us this specific image shows a fixed skylight.
const _FILENAME_PRODUCT_HINTS = [
  { kw:'קבוע',   label:'סקיילייט קבוע' },
  { kw:'נוסע',   label:'סקיילייט נוסע' },
  { kw:'מדרך',   label:'סקיילייט מדרך' },
  { kw:'מבנים',  label:'מבנים מרחביים' },
  { kw:'פירמידה',label:'פירמידה' },
  { kw:'כיפה',   label:'כיפה' },
  { kw:'חרוט',   label:'חרוט' },
  { kw:'עשן',    label:'שחרור עשן' },
  { kw:'פנטהאוז',label:'יציאה לגג' },
];
function _filenameHint(path){
  const base = path.split('/').pop().replace(/\\.[^/.]+$/, '');
  for(const h of _FILENAME_PRODUCT_HINTS){
    if(base.includes(h.kw)){
      // If there's an additional qualifier after the keyword (e.g. 'קבוע - חד שיפועי'),
      // include it too.
      const m = base.match(new RegExp(h.kw + '\\\\s*-\\\\s*(.+?)(?:\\\\s*\\\\d+\\\\s*)?$'));
      return m ? `${h.label} · ${m[1].trim()}` : h.label;
    }
  }
  return null;
}

// Render the full image gallery on a project detail page.
// Each tile gets a filename-hint caption if the filename indicates a product
// type (useful for mixed-product projects). Otherwise no caption — the project
// name is already in the hero.
function renderProjectGallery(slug){
  const pid = Object.keys(PROJECTS).find(p => PROJECTS[p].some(pr => pr.slug === slug));
  if(!pid) return;
  const proj = PROJECTS[pid].find(pr => pr.slug === slug);
  const sec = document.getElementById('project-gal-'+slug);
  if(!sec || !proj.images || !proj.images.length) return;
  const key = 'projgal-'+slug;
  const srcs = proj.images.map(s => B+s);
  const caps = proj.images.map(s => _filenameHint(s) || '');
  const kinds = srcs.map(() => 'img');
  _galReg[key] = { srcs, caps, kinds };
  const tiles = proj.images.map((src,i) => {
    const hint = _filenameHint(src);
    const capHtml = hint ? `<div class=\\"pp-media-cap\\">${hint}</div>` : '';
    return `<div class=\\"pp-media-item\\" onclick=\\"openLb('${key}',${i})\\"><img src=\\"${B}${src}\\" alt=\\"\\" loading=\\"lazy\\">${capHtml}</div>`;
  }).join('');
  sec.innerHTML = `<div class=\\"pp-media-grid\\">${tiles}</div>`;
}"""

swap(OLD_RPG, NEW_RPG, "JS: renderProjectGallery gains filename-hint captions")

# ══════════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — everything already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
    print("   Preview: python3 -m http.server 8081 → http://localhost:8081/#walkon")
