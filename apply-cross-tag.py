#!/usr/bin/env python3
"""apply-cross-tag.py — Phase 1 of the structured pilot rollout.

What this ships
===============
1. Each PROJECTS entry gains a `categories: [...]` array listing every
   product page it should appear on. This solves the cross-product
   visibility problem (HP HQ has both fixed and walk-on glass; until now
   it only showed on `#fixed`).

2. `renderProjectsSection(pid)` switches from per-array filtering to
   `categories.includes(pid)`. One project, many appearances. Detail page
   stays unique per slug — clicking any tile goes to the same project.

3. Beit Yokra TA (synthetic placeholder, no real data, not in llms.txt)
   is deleted: PROJECTS entry + detail page block + Schema.org entry.

4. Console assertion guards against orphan projects (any project missing
   `categories` will warn at load time).

Cross-tag mapping (confirmed by Ohad)
=====================================
                        fixed  retract  walkon  struct  smoke  penthouse
HP HQ                     ✓             ✓
Mitzpe Hayamim            ✓                              ✓
Beit Gil HaZahav          ✓                              ✓
Mishya                    ✓
Bar-Ilan                  ✓
Beit Zait                 ✓                              ✓
National Library                        ✓
Beit HaBeer                             ✓
Recanati Winery                                  ✓
Synagogue (Yagdil)                               ✓
Penthouse (×5)                  ✓                                ✓

Projected counts after this ships:
  fixed       6 (was 7 — Yokra deleted)
  retractable 5 (was 0 — but no DOM section yet, will render to nothing)
  walkon      3 (was 2 — HP HQ joins)
  structural  2 (unchanged)
  smoke       3 (was 0 — no DOM section yet)
  penthouse   5 (unchanged)

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
# 1) Add categories: [...] to each PROJECTS entry
#    Anchor on `slug:'X',name:` and inject between slug and name
# ═══════════════════════════════════════════════════════════════
CATEGORIES = {
    'penthouse-ben-yehuda':  ['penthouse', 'retractable'],
    'penthouse-jerusalem':   ['penthouse', 'retractable'],
    'penthouse-hayarkon':    ['penthouse', 'retractable'],
    'penthouse-shenkin':     ['penthouse', 'retractable'],
    'penthouse-tel-aviv':    ['penthouse', 'retractable'],
    'mitzpe-hayamim':        ['fixed', 'smoke'],
    'mishya':                ['fixed'],
    'bar-ilan':              ['fixed'],
    'beit-zait':             ['fixed', 'smoke'],
    'beit-gil-hazahav':      ['fixed', 'smoke'],
    'hp-hq':                 ['fixed', 'walkon'],
    'national-library':      ['walkon'],
    'beit-habeer':           ['walkon'],
    'recanati-winery':       ['structural'],
    'synagogue':             ['structural'],
}

for slug, cats in CATEGORIES.items():
    cat_str = "[" + ",".join(f"'{c}'" for c in cats) + "]"
    old = f"{{slug:'{slug}',name:"
    new = f"{{slug:'{slug}',categories:{cat_str},name:"
    swap(old, new, f"{slug}: + categories:{cat_str}", must_exist=False)

# ═══════════════════════════════════════════════════════════════
# 2) DELETE beit-yokra-ta — synthetic placeholder, no real data
# ═══════════════════════════════════════════════════════════════

# 2a) Delete from PROJECTS.fixed (single-line entry)
swap(
    "    {slug:'beit-yokra-ta',name:'בית יוקרה — תל אביב',hero:'02 — סקיילייט קבוע/חד שיפועי/DSC05005.jpg',meta:{where:'תל אביב',when:'—',arch:'—',product:'סקיילייט קבוע, חד שיפועי'},images:['02 — סקיילייט קבוע/חד שיפועי/DSC05005.jpg','02 — סקיילייט קבוע/חד שיפועי/DSC05010.jpg','02 — סקיילייט קבוע/חד שיפועי/DSC05013.jpg']},\n",
    "",
    "Delete PROJECTS.beit-yokra-ta entry",
    must_exist=False,
)

# 2b) Delete detail page block — between the comment and closing </div>
import re
yokra_page_pattern = re.compile(
    r'<!-- ════ PROJECT: בית יוקרה — תל אביב ════ -->\n'
    r'<div id="page-project-beit-yokra-ta" class="pp">\n'
    r'.*?\n'
    r'</div>\n\n',
    re.DOTALL
)
m = yokra_page_pattern.search(src)
if m:
    src = src[:m.start()] + src[m.end():]
    changes += 1
    print(f"✔  Delete page-project-beit-yokra-ta detail block ({m.end()-m.start()} chars)")
else:
    if 'page-project-beit-yokra-ta' in src:
        print("⚠  Yokra detail page anchor mismatch — manual check needed")
    else:
        print("✔  Yokra detail page already removed")

# 2c) Delete Schema.org entry
yokra_schema_pattern = re.compile(
    r'    \{\n'
    r'      "@type": "CreativeWork",\n'
    r'      "@id": "https://os84\.github\.io/skylite-preview/#project-beit-yokra-ta",\n'
    r'.*?\n'
    r'    \},\n',
    re.DOTALL
)
m = yokra_schema_pattern.search(src)
if m:
    src = src[:m.start()] + src[m.end():]
    changes += 1
    print(f"✔  Delete Schema.org #project-beit-yokra-ta entry")
else:
    if '#project-beit-yokra-ta' in src:
        print("⚠  Yokra schema anchor mismatch — manual check needed")
    else:
        print("✔  Yokra schema entry already removed")

# ═══════════════════════════════════════════════════════════════
# 3) Update renderProjectsSection to use cross-tag filter
# ═══════════════════════════════════════════════════════════════
swap(
    "function renderProjectsSection(pid){\n  const sec=document.getElementById('projects-sec-'+pid);\n  if(!sec)return;\n  const projs=PROJECTS[pid];\n  if(!projs||!projs.length){sec.style.display='none';return}",
    "function renderProjectsSection(pid){\n  const sec=document.getElementById('projects-sec-'+pid);\n  if(!sec)return;\n  // Cross-tag filter: a project appears on every page listed in its `categories` array\n  const projs=Object.values(PROJECTS).flat().filter(p => (p.categories||[]).includes(pid));\n  if(!projs||!projs.length){sec.style.display='none';return}",
    "renderProjectsSection: cross-tag filter",
)

# ═══════════════════════════════════════════════════════════════
# 4) Console assertion: every project must have ≥1 category
# ═══════════════════════════════════════════════════════════════
swap(
    "// Init\n['penthouse','fixed','walkon','structural'].forEach(renderProjectsSection);",
    """// Sanity: every project must have at least 1 category, else it won't render anywhere
Object.values(PROJECTS).flat().forEach(p => {
  if(!p.categories || !p.categories.length) console.warn(`[project orphan] ${p.slug} has no categories`);
});

// Init
['penthouse','fixed','walkon','structural'].forEach(renderProjectsSection);""",
    "Console orphan-check assertion",
)

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
