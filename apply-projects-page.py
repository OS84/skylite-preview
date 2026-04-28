#!/usr/bin/env python3
"""apply-projects-page.py — Sprint A: central /projects page.

Adds a flat filterable view of all 15 projects with:
  - Sector chips (5): מגורים · מסחרי · ציבורי · מלונאות · שימור
  - Product chips (7): נוסע · קבוע · מדרך · מבנים מרחביים · שחרור עשן · יציאה לגג · חלונות
  - Curated manual order (defaults — leads with prestige projects)
  - Friendly empty state with CTA
  - Reuses Option C `.pp-proj-tile` design

Adds `sector:` field to each PROJECTS entry. Reuses `categories:` from Phase 1
for product-type filtering.

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
# 1) Add sector: field to each PROJECTS entry
# ═══════════════════════════════════════════════════════════════
SECTORS = {
    'national-library':      'ציבורי',
    'hp-hq':                 'מסחרי',
    'mitzpe-hayamim':        'מלונאות',
    'mishya':                'מסחרי',
    'bar-ilan':              'ציבורי',
    'beit-zait':             'מגורים',
    'beit-gil-hazahav':      'מגורים',
    'beit-habeer':           'שימור',
    'recanati-winery':       'מסחרי',
    'synagogue':             'ציבורי',
    'penthouse-ben-yehuda':  'מגורים',
    'penthouse-jerusalem':   'מגורים',
    'penthouse-hayarkon':    'מגורים',
    'penthouse-shenkin':     'מגורים',
    'penthouse-tel-aviv':    'מגורים',
}

for slug, sector in SECTORS.items():
    old = f"{{slug:'{slug}',categories:"
    new = f"{{slug:'{slug}',sector:'{sector}',categories:"
    swap(old, new, f"{slug}: + sector:'{sector}'", must_exist=False)

# ═══════════════════════════════════════════════════════════════
# 2) CSS for /projects page (filter chips, header, empty state)
# ═══════════════════════════════════════════════════════════════
CSS_BLOCK = """
    /* ── /projects page ── */
    .projects-page-hero{padding:140px 80px 40px;background:var(--cream)}
    .projects-page-eye{font-size:12px;font-weight:500;letter-spacing:.22em;color:var(--accent);text-transform:uppercase;margin-bottom:18px}
    .projects-page-title{font-size:clamp(38px,6vw,68px);font-weight:700;color:var(--dark);line-height:1.05;margin:0 0 24px;letter-spacing:-.01em}
    .projects-page-sub{font-size:17px;font-weight:400;color:var(--stone);line-height:1.7;max-width:640px;margin:0}
    .projects-filters{padding:36px 80px 0;background:var(--cream)}
    .projects-filter-row{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-bottom:14px}
    .projects-filter-label{font-size:11px;font-weight:500;letter-spacing:.22em;color:var(--stone);text-transform:uppercase;margin-left:18px;min-width:88px}
    .projects-chip{display:inline-flex;align-items:center;height:32px;padding:0 16px;border-radius:18px;background:transparent;border:1px solid var(--warm-gray);font-size:13px;font-weight:400;color:var(--dark);font-family:var(--font);cursor:pointer;transition:background .25s var(--spring),border-color .25s var(--spring),color .25s var(--spring);direction:rtl}
    .projects-chip:hover{border-color:var(--accent)}
    .projects-chip.active{background:var(--dark);border-color:var(--dark);color:#fff}
    .projects-chip:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
    .projects-grid-section{padding:48px 0 120px;background:var(--cream)}
    .projects-grid-count{padding:0 80px;margin-bottom:28px;font-size:13px;color:var(--stone);letter-spacing:.06em}
    .projects-empty{padding:80px 80px;text-align:center;max-width:560px;margin:0 auto}
    .projects-empty h3{font-size:24px;font-weight:600;color:var(--dark);margin:0 0 12px}
    .projects-empty p{font-size:15px;color:var(--stone);line-height:1.7;margin:0 0 28px}
    @media(max-width:1024px){.projects-page-hero,.projects-filters,.projects-grid-count{padding-left:48px;padding-right:48px}.projects-empty{padding:60px 48px}}
    @media(max-width:600px){.projects-page-hero{padding:100px 24px 32px}.projects-filters,.projects-grid-count{padding-left:24px;padding-right:24px}.projects-filter-label{display:block;width:100%;margin-bottom:8px}.projects-empty{padding:48px 24px}}
"""
swap(
    "    /* ── PROJECT TILES — Option C",
    CSS_BLOCK + "\n    /* ── PROJECT TILES — Option C",
    "Add /projects page CSS",
)

# ═══════════════════════════════════════════════════════════════
# 3) HTML page block — insert before <!-- ════ TECH ════ -->
# ═══════════════════════════════════════════════════════════════
PAGE_HTML = """<!-- ════ /projects ════ -->
<div id="page-projects" class="pp">
<nav class="nav scrolled"><div class="nav-logo"><svg viewBox="0 0 50 50" width="36" height="36" fill="none"><rect width="50" height="50" fill="#E9EEF2"/><path d="M26,0 L50,0 L50,50 L0,50 L0,40 C3,30 18,10 26,0Z" fill="#1A1E24"/></svg><span class="nav-wordmark">SKYLITE</span></div><a href="#" class="nav-back" onclick="home();return false"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M13 8H3M7 12l-4-4 4-4"/></svg>חזרה לדף הבית</a><a href="#" class="nav-cta" onclick="openCM();return false">צור קשר</a></nav>
<section class="projects-page-hero">
  <div class="projects-page-eye rv">פרויקטים נבחרים</div>
  <h1 class="projects-page-title rv rv-d1">היכן בנינו</h1>
  <p class="projects-page-sub rv rv-d2">מהפנטהאוז הפרטי ועד הספריה הלאומית — אוסף הפרויקטים שלנו בארץ. סננו לפי סוג הלקוח או סוג המוצר כדי למצוא פרויקטים דומים לשלכם.</p>
</section>
<section class="projects-filters">
  <div class="projects-filter-row" id="filter-row-sector"></div>
  <div class="projects-filter-row" id="filter-row-product"></div>
</section>
<section class="projects-grid-section">
  <div class="projects-grid-count" id="projects-count"></div>
  <div id="projects-grid-host"></div>
</section>
<section class="pp-cta"><h2 class="rv">לא מצאתם פרויקט שמתאים?<br><em>בואו נדבר</em></h2><div class="cta-acts rv rv-d1"><button class="btn-pd" onclick="openCM()">השאירו פרטים</button><a href="tel:+97239343159" class="btn-od">טלפון: 03-9343159</a></div></section>
<footer><div class="f-brand"><svg viewBox="0 0 50 50" width="32" fill="none"><rect width="50" height="50" fill="#1A1E24"/><path d="M26,0 L50,0 L50,50 L0,50 L0,40 C3,30 18,10 26,0Z" fill="#E9EEF2"/></svg><div class="f-name">Skylite</div><div class="f-tag">הנדסת הטבע<br>האור שחותך את החלל — מ-1986</div></div><div class="f-links"><a href="#" onclick="home();return false">← חזרה לדף הבית</a><a href="#" onclick="go('fixed');return false">סקיילייט קבוע</a><a href="#" onclick="go('retractable');return false">סקיילייט נוסע</a><a href="#" onclick="go('tech');return false">מידע טכני</a></div><div class="f-contact"><p><strong>סקיילייט בע"מ</strong></p><p>אלכסנדר ינאי 8, א.ת סגולה, פתח תקווה</p><p>טל: <a href="tel:+97239343159" dir="ltr" style="color:inherit;text-decoration:none;border-bottom:1px solid currentColor">03-9343159</a> | פקס: <span dir="ltr">03-9311921</span></p><p><a href="mailto:skylite@skylite.co.il" style="color:inherit;text-decoration:none;border-bottom:1px solid currentColor">skylite@skylite.co.il</a></p></div></footer>
</div>

<!-- ════ TECH ════ -->"""

swap(
    "<!-- ════ TECH ════ -->",
    PAGE_HTML,
    "Insert page-projects DOM",
)

# ═══════════════════════════════════════════════════════════════
# 4) Add 'projects' to pages array
# ═══════════════════════════════════════════════════════════════
swap(
    "const pages=['home','about','penthouse','fixed','retractable','walkon','structural','smoke','windows','tech'];",
    "const pages=['home','about','projects','penthouse','fixed','retractable','walkon','structural','smoke','windows','tech'];",
    "pages array += 'projects'",
)

# ═══════════════════════════════════════════════════════════════
# 5) JS — render filter chips + grid + state
# ═══════════════════════════════════════════════════════════════
JS_BLOCK = """
// ─── /projects page ────────────────────────────────────────────
// Curated manual order — leads with prestige + variety
const PROJECTS_PAGE_ORDER = [
  'national-library', 'hp-hq', 'mitzpe-hayamim', 'recanati-winery',
  'beit-habeer', 'beit-gil-hazahav', 'synagogue', 'penthouse-ben-yehuda',
  'penthouse-jerusalem', 'mishya', 'penthouse-shenkin', 'beit-zait',
  'penthouse-tel-aviv', 'bar-ilan', 'penthouse-hayarkon',
];

const PROJECTS_FILTER_SECTORS = ['מגורים', 'מסחרי', 'ציבורי', 'מלונאות', 'שימור'];
const PROJECTS_FILTER_PRODUCTS = [
  { id: 'retractable', label: 'נוסע' },
  { id: 'fixed',       label: 'קבוע' },
  { id: 'walkon',      label: 'מדרך' },
  { id: 'structural',  label: 'מבנים מרחביים' },
  { id: 'smoke',       label: 'שחרור עשן' },
  { id: 'penthouse',   label: 'יציאה לגג' },
  { id: 'windows',     label: 'חלונות' },
];
let projectsFilterState = { sectors: new Set(), products: new Set() };

function renderProjectsPageChips(){
  const sRow = document.getElementById('filter-row-sector');
  const pRow = document.getElementById('filter-row-product');
  if(!sRow || !pRow) return;
  const chip = (label, active, onClick) => {
    const b = document.createElement('button');
    b.className = 'projects-chip' + (active ? ' active' : '');
    b.textContent = label;
    b.type = 'button';
    b.onclick = onClick;
    return b;
  };
  sRow.innerHTML = '<span class="projects-filter-label">לפי סקטור</span>';
  PROJECTS_FILTER_SECTORS.forEach(s => {
    sRow.appendChild(chip(s, projectsFilterState.sectors.has(s), () => {
      if(projectsFilterState.sectors.has(s)) projectsFilterState.sectors.delete(s);
      else projectsFilterState.sectors.add(s);
      renderProjectsPage();
    }));
  });
  pRow.innerHTML = '<span class="projects-filter-label">לפי מוצר</span>';
  PROJECTS_FILTER_PRODUCTS.forEach(p => {
    pRow.appendChild(chip(p.label, projectsFilterState.products.has(p.id), () => {
      if(projectsFilterState.products.has(p.id)) projectsFilterState.products.delete(p.id);
      else projectsFilterState.products.add(p.id);
      renderProjectsPage();
    }));
  });
}

function renderProjectsPage(){
  const host = document.getElementById('projects-grid-host');
  const count = document.getElementById('projects-count');
  if(!host || !count) return;
  const all = Object.values(PROJECTS).flat();
  const bySlug = Object.fromEntries(all.map(p => [p.slug, p]));
  // Apply curated order
  const ordered = PROJECTS_PAGE_ORDER.map(s => bySlug[s]).filter(Boolean);
  // Filter
  const sFilter = projectsFilterState.sectors;
  const pFilter = projectsFilterState.products;
  const filtered = ordered.filter(p => {
    if(sFilter.size > 0 && !sFilter.has(p.sector)) return false;
    if(pFilter.size > 0){
      const cats = p.categories || [];
      if(!cats.some(c => pFilter.has(c))) return false;
    }
    return true;
  });
  count.textContent = filtered.length === all.length
    ? `כל הפרויקטים (${filtered.length})`
    : `${filtered.length} פרויקטים`;
  if(filtered.length === 0){
    host.innerHTML = `<div class="projects-empty"><h3>לא מצאנו פרויקט שתואם את הסינון</h3><p>נסו פחות מסננים, או צרו קשר ונשמח לספר לכם על פרויקטים שעדיין לא נמצאים באתר.</p><button class="btn-pd" onclick="openCM()">השאירו פרטים</button></div>`;
    _runA11yAfterRender();
    return;
  }
  const arrow = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 8h10M9 4l4 4-4 4"/></svg>';
  const tiles = filtered.map(p => {
    const m = p.meta||{};
    const where = (m.where && m.where !== '—') ? m.where : '';
    const specRows = [];
    if(p.sector) specRows.push(`<div class="pp-proj-tile-spec-row"><span>סקטור</span><b>${p.sector}</b></div>`);
    if(m.arch && m.arch !== '—') specRows.push(`<div class="pp-proj-tile-spec-row"><span>אדריכל</span><b>${m.arch}</b></div>`);
    if(m.when && m.when !== '—') specRows.push(`<div class="pp-proj-tile-spec-row"><span>שנה</span><b>${m.when}</b></div>`);
    const specHtml = specRows.length ? `<div class="pp-proj-tile-spec">${specRows.join('')}</div>` : '';
    return `<a class="pp-proj-tile" href="#project/${p.slug}" onclick="goProject('${p.slug}');return false">
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
    </a>`;
  }).join('');
  host.innerHTML = `<div class="pp-projects-tiles">${tiles}</div>`;
  _runA11yAfterRender();
}
"""

swap(
    "// ─── /projects page ────────────────────────────────────────────",
    JS_BLOCK,
    "Add /projects rendering JS",
    must_exist=False,
)
# If anchor wasn't there (script not yet inserted), insert before HOME_STRIP
if "renderProjectsPage" not in src:
    swap(
        "// Home-page projects strip — curated subset of PROJECTS as clickable entry",
        JS_BLOCK + "\n// Home-page projects strip — curated subset of PROJECTS as clickable entry",
        "Add /projects rendering JS (anchored on HOME_STRIP comment)",
    )

# ═══════════════════════════════════════════════════════════════
# 6) Hook into init — call render on load
# ═══════════════════════════════════════════════════════════════
swap(
    "['penthouse','fixed','walkon','structural'].forEach(renderProjectsSection);\n_a11yMakeKeyboardable();",
    """['penthouse','fixed','walkon','structural'].forEach(renderProjectsSection);
renderProjectsPageChips();
renderProjectsPage();
_a11yMakeKeyboardable();""",
    "Init: render projects-page chips + grid",
)

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
