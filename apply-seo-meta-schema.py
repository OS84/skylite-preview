#!/usr/bin/env python3
"""apply-seo-meta-schema.py — Phase 1 SEO/AEO: meta tags + JSON-LD schema.

Does:
  1. Rewrites <title> + adds <meta description>
  2. Adds OpenGraph + Twitter Card tags (static = home defaults)
  3. Adds canonical + theme-color
  4. Injects Schema.org JSON-LD @graph with:
       - Organization (Skylite, founder, founding date, contact)
       - LocalBusiness (address, hours, geo)
       - WebSite (search action — useful for sitelinks)
       - Product × 6 (one per product page)
       - CreativeWork × 15 (one per project)
  5. Adds META JS object + updateMeta() + setMeta() helpers
  6. Hooks go() and goProject() to call updateMeta on route change
  7. Calls updateMeta() on initial load

Dynamic meta on SPA navigation won't make Google index hash routes — that
requires the route refactor. But it DOES update:
  - <title> in the browser tab
  - <meta description>, OG, Twitter tags for link sharing
  - Schema @graph is static but @graph entries are URL-addressable, so
    crawlers can find each entity.

Does NOT:
  - Migrate hash routing to real paths (that's the launch-gate refactor)
  - Add GA4/Meta Pixel (waiting on measurement IDs from Ohad)
  - Create FAQ page (phase 2)

Run: python3 apply-seo-meta-schema.py
Idempotent.
"""
import sys, pathlib, re, json

HTML = pathlib.Path(__file__).parent / "index.html"
src = HTML.read_text(encoding="utf-8")
changes = 0

def swap(old, new, label):
    global src, changes
    if new in src:
        print(f"✔  {label} — already applied")
        return
    if old not in src:
        print(f"❌ {label} — anchor not found")
        sys.exit(1)
    src = src.replace(old, new, 1)
    changes += 1
    print(f"✔  {label}")

# Site URL — GitHub Pages preview. Will need updating once custom domain flipped.
SITE_URL = "https://os84.github.io/skylite-preview"
HERO_IMAGE = f"{SITE_URL}/מוצרים מסווגים/Hero Banner .jpg"

# ═══════════════════════════════════════════════════════════════
# 1–3. Replace existing <title> block with full head meta suite
# ═══════════════════════════════════════════════════════════════
OLD_HEAD = """  <title>Skylite — הנדסת האור</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">"""

NEW_HEAD = f"""  <title>סקיילייט — הנדסת אור מאז 1986 | יצרנית סקיילייטים ישראלית</title>
  <meta name="description" content="סקיילייט מתמחה בתכנון, ייצור והתקנה של סקיילייטים, כיפות, מבנים מרחביים וזיגוגים אדריכליים. 40 שנה של ניסיון בפרויקטים ברחבי ישראל — מהפנטהאוז הפרטי ועד הספריה הלאומית.">
  <meta name="keywords" content="סקיילייט, גגון אור, חלון גג, זיגוג אדריכלי, פתח אוורור, שחרור עשן, סקיילייט מדרך, סקיילייט נוסע, כיפת זכוכית, מבנים מרחביים, קירוי שקוף, גג זכוכית, EN 12101">
  <meta name="author" content="Skylite Ltd. — אהרון שמיר">
  <meta name="theme-color" content="#2B7A8C">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{SITE_URL}/">

  <!-- OpenGraph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Skylite — סקיילייט">
  <meta property="og:title" content="סקיילייט — הנדסת אור מאז 1986">
  <meta property="og:description" content="סקיילייט מתמחה בתכנון, ייצור והתקנה של סקיילייטים, כיפות, מבנים מרחביים וזיגוגים אדריכליים. 40 שנה של ניסיון בפרויקטים ברחבי ישראל.">
  <meta property="og:url" content="{SITE_URL}/">
  <meta property="og:image" content="{HERO_IMAGE}">
  <meta property="og:locale" content="he_IL">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="סקיילייט — הנדסת אור מאז 1986">
  <meta name="twitter:description" content="יצרנית סקיילייטים ישראלית מ-1986. פתרונות גגות שקופים לפרויקטים ציבוריים, מסחריים ופרטיים.">
  <meta name="twitter:image" content="{HERO_IMAGE}">

  <link rel="preconnect" href="https://fonts.googleapis.com">"""

swap(OLD_HEAD, NEW_HEAD, "Head: title + meta description + OG + Twitter + canonical")

# ═══════════════════════════════════════════════════════════════
# 4. Build Schema.org JSON-LD @graph (Organization + LocalBusiness + WebSite
#    + Products + Projects). Extract projects from index.html directly.
# ═══════════════════════════════════════════════════════════════

# Pull project data out of the already-committed PROJECTS object
project_entries = []
for m in re.finditer(r"\{slug:'([^']+)',name:'([^']+)',hero:'([^']+)',meta:\{where:'([^']*)',when:'([^']*)',arch:'([^']*)',product:'([^']*)'\}", src):
    slug, name, hero, where, when, arch, product = m.groups()
    project_entries.append({
        "slug": slug, "name": name, "hero": hero,
        "where": where, "when": when, "arch": arch, "product": product
    })

# Product page descriptions
PRODUCTS = [
    {"pid": "penthouse", "name": "יציאה לגג — פנטהאוז", "desc": "חלונות סקיילייט ליציאה לגג, סוכה, אוורור ושחרור עשן. מופעלים בשלט, מפסק או רכזת הפעלה."},
    {"pid": "fixed",     "name": "סקיילייט קבוע",      "desc": "סקיילייט קבוע חד-שיפועי ודו-שיפועי. פרופילי אלומיניום 6063 TF, שיטת FLUSH GLAZING, התאמה אישית."},
    {"pid": "retractable","name": "סקיילייט נוסע",      "desc": "גג שנפתח חשמלית או ידנית — יחידה אחת או מספר חלקים נעים. קמרונות, שיפועים ופירמידות."},
    {"pid": "walkon",    "name": "סקיילייט מדרך",       "desc": "רצפת זכוכית מעל פתחים. זכוכית ביטחון מרובדת לעומסי הליכה. לחצרות פנימיות, אתרי מורשת וגשרים."},
    {"pid": "structural","name": "מבנים מרחביים",       "desc": "כיפות, פירמידות, קשתות וחרוטים. גיאומטריות מורכבות בהתאמה אישית לאדריכלות."},
    {"pid": "smoke",     "name": "כיפות תאורה ושחרור עשן", "desc": "פתרונות אוורור ושחרור עשן בתקן EN 12101. בסיס PVC דופן כפול, זיגוג כפול, מנועים חשמליים."},
]

def project_to_schema(p):
    entity = {
        "@type": "CreativeWork",
        "@id": f"{SITE_URL}/#project-{p['slug']}",
        "name": p["name"],
        "url": f"{SITE_URL}/#project-{p['slug']}",
        "image": f"{SITE_URL}/מוצרים מסווגים/{p['hero']}",
    }
    if p["where"] and p["where"] != "—":
        entity["locationCreated"] = {"@type": "Place", "name": p["where"]}
    if p["when"] and p["when"] != "—":
        entity["dateCreated"] = p["when"]
    if p["arch"] and p["arch"] != "—":
        entity["creator"] = {"@type": "Organization", "name": p["arch"]}
    if p["product"]:
        entity["about"] = p["product"]
    return entity

graph = [
    {
        "@type": "Organization",
        "@id": f"{SITE_URL}/#org",
        "name": "Skylite",
        "alternateName": "סקיילייט",
        "url": f"{SITE_URL}/",
        "logo": f"{SITE_URL}/logo.png",
        "foundingDate": "1986",
        "founder": {"@type": "Person", "name": "Aharon Shamir", "alternateName": "אהרון שמיר"},
        "sameAs": ["https://instagram.com/skyliteisrael/"],
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "+972-3-9343159",
            "email": "skylite@skylite.co.il",
            "contactType": "customer service",
            "areaServed": "IL",
            "availableLanguage": ["Hebrew", "English"]
        },
        "description": "Israeli manufacturer of custom-engineered skylights and architectural glazing systems. Founded 1986 by Aharon Shamir."
    },
    {
        "@type": "LocalBusiness",
        "@id": f"{SITE_URL}/#lb",
        "name": "Skylite — סקיילייט",
        "image": HERO_IMAGE,
        "url": f"{SITE_URL}/",
        "telephone": "+972-3-9343159",
        "email": "skylite@skylite.co.il",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Alexander Yanai 8, Segula Industrial Zone",
            "addressLocality": "Petah Tikva",
            "addressCountry": "IL"
        },
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"],
            "opens": "09:00",
            "closes": "18:00"
        }],
        "priceRange": "$$$"
    },
    {
        "@type": "WebSite",
        "@id": f"{SITE_URL}/#website",
        "url": f"{SITE_URL}/",
        "name": "סקיילייט",
        "inLanguage": "he-IL",
        "publisher": {"@id": f"{SITE_URL}/#org"}
    },
]

# Products
for prod in PRODUCTS:
    graph.append({
        "@type": "Product",
        "@id": f"{SITE_URL}/#product-{prod['pid']}",
        "name": prod["name"],
        "description": prod["desc"],
        "url": f"{SITE_URL}/#{prod['pid']}",
        "brand": {"@id": f"{SITE_URL}/#org"},
        "manufacturer": {"@id": f"{SITE_URL}/#org"}
    })

# Projects — from PROJECTS data
for p in project_entries:
    graph.append(project_to_schema(p))

schema_json = json.dumps({
    "@context": "https://schema.org",
    "@graph": graph
}, ensure_ascii=False, indent=2)

SCHEMA_BLOCK = f"""
  <!-- Schema.org JSON-LD — Organization, LocalBusiness, WebSite, Products, Projects -->
  <script type="application/ld+json">
{schema_json}
  </script>

  <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700;900&display=swap" rel="stylesheet">"""

# Inject Schema block right before the Google Fonts stylesheet link
ANCHOR = '  <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700;900&display=swap" rel="stylesheet">'
if '"@graph"' in src:
    print("✔  Schema.org JSON-LD — already present")
else:
    if ANCHOR not in src:
        print(f"❌ Fonts link anchor not found"); sys.exit(1)
    src = src.replace(ANCHOR, SCHEMA_BLOCK.rstrip(), 1)
    changes += 1
    print(f"✔  Schema.org JSON-LD @graph ({len(graph)} entities: Org + LocalBusiness + WebSite + {len(PRODUCTS)} products + {len(project_entries)} projects)")

# ═══════════════════════════════════════════════════════════════
# 5-7. JS: META object + updateMeta() + hook into go/goProject
# ═══════════════════════════════════════════════════════════════
META_JS = '''
// ── SEO: per-page meta updater. Hash routing isn't SEO-indexable, but this
// updates the browser tab title, meta description, OG/Twitter tags when
// navigating — so link-sharing and in-browser UX both improve.
const META = {
  home: {
    title: "סקיילייט — הנדסת אור מאז 1986 | יצרנית סקיילייטים ישראלית",
    desc: "סקיילייט מתמחה בתכנון, ייצור והתקנה של סקיילייטים, כיפות, מבנים מרחביים וזיגוגים אדריכליים. 40 שנה של ניסיון בפרויקטים ברחבי ישראל — מהפנטהאוז הפרטי ועד הספריה הלאומית.",
    image: "./מוצרים מסווגים/Hero Banner .jpg"
  },
  about: {
    title: "אודות סקיילייט | 40 שנה של הנדסת אור בישראל",
    desc: "החברה הוקמה ב-1986 ע\\"י אהרון שמיר. פתרונות גגות שקופים — תכנון, ייצור והתקנה לפרויקטים ציבוריים, מסחריים ופרטיים.",
    image: "./מוצרים מסווגים/03 — סקיילייט מדרך/Hero Banner .jpg"
  },
  penthouse: {
    title: "סקיילייט ויציאה לגג לפנטהאוז | סקיילייט",
    desc: "חלונות ליציאה לגג, לסוכה, לאוורור ושחרור עשן. מופעלים בשלט / מפסק / רכזת. התקנה מותאמת לכל פנטהאוז או וילה.",
    image: "./מוצרים מסווגים/06 — יציאה לגג/פנטהאוז פרטי - בן יהודה תל אביב/DJI_20260304175337_0201_D.jpg"
  },
  retractable: {
    title: "סקיילייט נוסע — גג שנפתח חשמלית | סקיילייט",
    desc: "גג שנפתח חשמלית או ידנית — יחידה אחת או מספר חלקים נעים. קמרונות, שיפועים ופירמידות — בהתאמה אישית לכל פרויקט.",
    image: "./מוצרים מסווגים/01 — סקיילייט נוסע/חד שיפועי/DOR_6758-HDR.jpg"
  },
  fixed: {
    title: "סקיילייט קבוע — חד ודו שיפועי | סקיילייט",
    desc: "סקיילייט קבוע לגגות שטוחים ומשופעים. פרופילי אלומיניום 6063 TF, שיטת FLUSH GLAZING, התאמה אישית לכל פרויקט.",
    image: "./מוצרים מסווגים/02 — סקיילייט קבוע/חד שיפועי/DSC05064.jpg"
  },
  walkon: {
    title: "סקיילייט מדרך — רצפת זכוכית | סקיילייט",
    desc: "סקיילייט במישור הרצפה — לחצרות פנימיות, אתרי מורשת וגשרים מזוגגים. זכוכית ביטחון מרובדת לעומסי הליכה.",
    image: "./מוצרים מסווגים/03 — סקיילייט מדרך/Hero Banner .jpg"
  },
  structural: {
    title: "מבנים מרחביים — כיפות, פירמידות, קשתות | סקיילייט",
    desc: "כיפות, פירמידות וקמרונות בהתאמה אישית. 40 שנה של ניסיון בגיאומטריות מורכבות — מבית כנסת עד יקב רקנאטי.",
    image: "./מוצרים מסווגים/04 — מבנים מרחביים/קשת/סקייליט מקומר בניין עתידים.JPG"
  },
  smoke: {
    title: "כיפות תאורה ושחרור עשן EN 12101 | סקיילייט",
    desc: "פתרונות אוורור ושחרור עשן העומדים בתקן EN 12101. לבתי חולים, מבני ציבור, מבנים מסחריים ומגורים.",
    image: "./מוצרים מסווגים/05 — כיפות תאורה, אוורור ושחרור עשן/בית פרטי חד שיפועי שחרור עשן.jpg"
  },
  tech: {
    title: "מידע טכני | סקיילייט",
    desc: "מידע טכני ותיעוד — פרופילי אלומיניום 6063 TF, אטמי EPDM, FLUSH GLAZING, תקן EN 12101 ומערכות בקרה.",
    image: "./מוצרים מסווגים/Hero Banner .jpg"
  }
};

function _setMeta(selector, attr, content) {
  let el = document.querySelector(selector);
  if (!el) return;
  el.setAttribute(attr, content);
}

function updateMeta(pid) {
  // For project pages: derive meta from PROJECTS data
  if (pid && pid.indexOf('project-') === 0) {
    const slug = pid.slice('project-'.length);
    let proj = null;
    for (const pk of Object.keys(PROJECTS)) {
      proj = PROJECTS[pk].find(p => p.slug === slug);
      if (proj) break;
    }
    if (proj) {
      const archPart = proj.meta.arch !== '\\u2014' && proj.meta.arch !== '-' ? ` אדריכל: ${proj.meta.arch}.` : '';
      const yearPart = proj.meta.when !== '\\u2014' && proj.meta.when !== '-' ? ` ${proj.meta.when}.` : '';
      const wherePart = proj.meta.where !== '\\u2014' && proj.meta.where !== '-' ? proj.meta.where : '';
      const title = `${proj.name} | סקיילייט`;
      const desc = `פרויקט סקיילייט${wherePart ? ' ב' + wherePart : ''}.${archPart} מוצר: ${proj.meta.product}.${yearPart}`;
      const image = './מוצרים מסווגים/' + proj.hero;
      document.title = title;
      _setMeta('meta[name="description"]', 'content', desc);
      _setMeta('meta[property="og:title"]', 'content', title);
      _setMeta('meta[property="og:description"]', 'content', desc);
      _setMeta('meta[property="og:image"]', 'content', image);
      _setMeta('meta[name="twitter:title"]', 'content', title);
      _setMeta('meta[name="twitter:description"]', 'content', desc);
      _setMeta('meta[name="twitter:image"]', 'content', image);
      return;
    }
  }
  // Standard pages
  const m = META[pid] || META.home;
  document.title = m.title;
  _setMeta('meta[name="description"]', 'content', m.desc);
  _setMeta('meta[property="og:title"]', 'content', m.title);
  _setMeta('meta[property="og:description"]', 'content', m.desc);
  _setMeta('meta[property="og:image"]', 'content', m.image);
  _setMeta('meta[name="twitter:title"]', 'content', m.title);
  _setMeta('meta[name="twitter:description"]', 'content', m.desc);
  _setMeta('meta[name="twitter:image"]', 'content', m.image);
}

// Initial load — update meta based on current hash
(function initMeta(){
  const h = (location.hash || '').slice(1);
  const pid = h.indexOf('project/') === 0 ? 'project-' + h.slice('project/'.length) : (h || 'home');
  updateMeta(pid);
})();
'''

# Insert META_JS block right before the `const pages=` declaration
JS_ANCHOR = "const pages=['home','about','penthouse','fixed','retractable','walkon','structural','smoke','tech'];"
if "function updateMeta" in src:
    print("✔  updateMeta JS — already present")
elif JS_ANCHOR in src:
    src = src.replace(JS_ANCHOR, META_JS.strip() + "\n\n" + JS_ANCHOR, 1)
    changes += 1
    print("✔  Added META object + updateMeta() + initial-load hook")
else:
    print(f"❌ JS anchor ({JS_ANCHOR[:40]}...) not found")
    sys.exit(1)

# Hook go() to call updateMeta
OLD_GO = "function go(id){pages.forEach(p=>{const el=document.getElementById('page-'+p);if(el){el.style.display='none';el.classList.remove('active')}});document.querySelectorAll('[id^=\"page-project-\"]').forEach(el=>{el.style.display='none';el.classList.remove('active')});const t=document.getElementById('page-'+id);if(t){t.style.display='block';t.classList.add('active');window.scrollTo({top:0,behavior:'smooth'});setTimeout(()=>{t.querySelectorAll('.rv:not(.on)').forEach(el=>obs.observe(el))},100)}}"
NEW_GO = "function go(id){pages.forEach(p=>{const el=document.getElementById('page-'+p);if(el){el.style.display='none';el.classList.remove('active')}});document.querySelectorAll('[id^=\"page-project-\"]').forEach(el=>{el.style.display='none';el.classList.remove('active')});const t=document.getElementById('page-'+id);if(t){t.style.display='block';t.classList.add('active');window.scrollTo({top:0,behavior:'smooth'});setTimeout(()=>{t.querySelectorAll('.rv:not(.on)').forEach(el=>obs.observe(el))},100);updateMeta(id)}}"
swap(OLD_GO, NEW_GO, "go(): calls updateMeta(id) on route change")

# Hook goProject to call updateMeta
OLD_GOPROJ = "setTimeout(()=>{ target.querySelectorAll('.rv:not(.on)').forEach(el=>obs.observe(el)) }, 100);\n}"
NEW_GOPROJ = "setTimeout(()=>{ target.querySelectorAll('.rv:not(.on)').forEach(el=>obs.observe(el)) }, 100);\n  updateMeta('project-' + slug);\n}"
swap(OLD_GOPROJ, NEW_GOPROJ, "goProject(): calls updateMeta('project-'+slug)")

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
