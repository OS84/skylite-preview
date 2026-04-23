# Skylite — Claude Project Brief

> **Goal:** Ship the finished site by end of week (April 2026).
> **Live site:** https://os84.github.io/skylite-preview/
> **Repo:** https://github.com/OS84/skylite-preview
> **Local preview:** `pkill -9 -f http.server; cd ~/Downloads/skylite-github && python3 -m http.server 8100` → http://localhost:8100

---

## What this is

Single-file Hebrew RTL website for **Skylite** (סקיילייט), an Israeli skylight manufacturer. The entire site lives in `index.html` — one file, no build system, no frameworks. ~1300 lines.

---

## Language & direction

- `lang="he" dir="rtl"` — everything flows right-to-left
- Font: **Heebo** (Google Fonts) — weights 300, 400, 500, 700, 900
- All copy is Hebrew. **Never translate or change Hebrew text unless explicitly asked.**

---

## Design system

### Color tokens (`:root` CSS vars)
```
--cream:      #F4F6F8   page background
--chalk:      #E9EEF2   subtle sections
--dark:       #1A1E24   primary text / dark backgrounds
--dark-mid:   #252A32   footers
--accent:     #2B7A8C   primary brand teal
--accent-2:   #34909E
--accent-pale:#7FBCC8   lighter teal, links
--accent-deep:#1D5F6E   hover states
--sky:        #4F8FA0
--stone:      #6B7680   secondary text
--linen:      #F8FAFB
--sand:       #EDF1F4
--warm-gray:  #DDE3E8   dividers
```

### Typography (current — post typeset pass)
- Labels/eyebrows: `12px; letter-spacing:.22em; text-transform:uppercase; font-weight:300`
- Body text: `15px; font-weight:400; line-height:1.75`
- Section titles: `clamp(28px,5vw,52px); font-weight:700`
- Hero: weight 900 for max hierarchy contrast

### Spacing
Generous whitespace. Sections: `padding: 80px 0` desktop, `48px 0` tablet, `32px 0` mobile.

---

## File structure
```
skylite-github/
├── index.html                  ← entire site
├── CLAUDE.md                   ← this file
├── .impeccable.md              ← design context for impeccable skill
├── apply-critique-fixes.py     ← apply script: CTAs, gradients, icons
├── apply-typeset.py            ← apply script: font sizes, contrast
├── .nojekyll                   ← disables Jekyll on GitHub Pages
├── .claude/skills/             ← installed design skills (see Skills section)
└── מוצרים מסווגים/             ← 104 compressed product images (43MB)
    ├── 01 — סקיילייט נוסע/
    ├── 02 — סקיילייט קבוע/
    ├── 03 — סקיילייט מדרך/
    ├── 04 — מבנים מרחביים/
    ├── 05 — כיפות תאורה, אוורור ושחרור עשן/
    ├── 06 — יציאה לגג/
    └── Hero Banner .jpg
```

---

## Page architecture

JavaScript SPA — hash routing via `go(id)` / `showPage(pid)`.

### Page IDs
| ID | Hebrew name |
|---|---|
| `penthouse` | יציאה לגג |
| `fixed` | סקיילייט קבוע |
| `retractable` | סקיילייט נוסע |
| `walkon` | סקיילייט מדרך |
| `structural` | מבנים מרחביים |
| `smoke` | כיפות תאורה, אוורור ושחרור עשן |

### CSS visibility rules
- Product pages: `<div class="pp" id="page-{pid}">` — hidden by default
- Active page: `.pp.active { display:block }`
- Home: `<div id="page-home">` — always visible (no `.pp` class)

---

## Gallery system
```js
const B = './מוצרים מסווגים/';
const GALLERIES = {
  penthouse: {
    'tab label': [
      { s: 'folder/filename.jpg', c: 'optional caption' },
    ]
  },
  // fixed, retractable, walkon, structural, smoke
};
```
`renderGallery(pid)` reads `GALLERIES[pid]` and populates `#gal-{pid}`.
`subTab(el, pid)` switches between sub-tabs within a product page.

---

## Critical CSS conventions

### Apply scripts pattern
**Never make CSS edits directly to index.html from Cowork** — the file is large and direct edits may not sync reliably to Mac. Instead:
1. Write the change as a Python `str.replace()` in a new `apply-[feature].py` script
2. Give the script to the user to run from Terminal: `python3 apply-[feature].py`
3. User runs it, git commits and pushes

### ID-scoped CSS for dark/light section discrimination
Several `.tech-specs` sections appear on the technology page. Two of them have dark backgrounds (`#tech-construction`, `#tech-motors`) — the rest are light cream. **Do NOT use `.tech-specs .rule{}` globally.** Always scope dark overrides to the specific IDs:
```css
#tech-construction .sec-title,
#tech-motors .sec-title { color: #fff }
```
Global class-based overrides will break the light sections (`#tech-glazing`, `#tech-domes`).

### Hero overlay gradient
The hero overlay uses a bottom-weighted gradient for photography contrast + top-weighted for nav readability:
```css
.hero-ov {
  background: radial-gradient(ellipse at 50% 110%, rgba(43,122,140,.10) 0%, transparent 55%),
              linear-gradient(180deg, rgba(26,30,36,.52) 0%, rgba(26,30,36,.18) 22%,
                             transparent 42%, rgba(26,30,36,.54) 100%);
}
```

---

## What has been completed (April 2026)

**Design & copy:**
- ✅ Hero CTAs — "קבלו הצעת מחיר" (primary) + "לצפייה במוצרים" (secondary)
- ✅ Statement headline rewritten — "סקיילייט הוא האמצעי — המוצר האמיתי הוא האור שנכנס פנימה"
- ✅ Hero subtitle — "מהפנטהאוז הפרטי ועד הספריה הלאומית"
- ✅ Water section rewritten — label "הנדסת אטימות", new headline, spec-accurate 4 points
- ✅ Typeset pass — 10–11px labels → 12px; body text → 15px weight-400; low-opacity white raised
- ✅ Process step numbers — gradient text removed → solid `color:rgba(43,122,140,.28)`
- ✅ Tech card icons hidden; dark section text scoped to `#tech-construction` + `#tech-motors`
- ✅ Nav readability — hero overlay gradient darkened at top
- ✅ Stats section repositioned — between statement and products
- ✅ `.impeccable.md` created; `.agents/product-marketing-context.md` V1 strategic doc written

**Architecture (walk-on pilot — new pattern):**
- ✅ **Media strip** — 8 image tiles with auto-derived overlays above projects section
- ✅ **Project detail pages** — `#page-project-{slug}` with hero, metadata, full gallery. 3 live: National Library, בית הבאר, HP HQ (Mercury Building)
- ✅ **`renderProjectGallery`** — `_filenameHint()` auto-captions tiles from filenames (מדרך/קבוע/נוסע/כיפה)
- ✅ **Video gallery** — wired on retractable + penthouse pages via `renderVideos(pid)`; 2 live videos on retractable
- ✅ Projects have `products:[]` array for future cross-page appearance

**Strategic docs in repo:**
- `.agents/product-marketing-context.md` — positioning, differentiators, objections, voice, proof points
- `.agents/parked-copy-blocks.md` — "Right First Time" Hebrew copy block (legally reviewed, ready for About page)
- `.impeccable.md` — design context
- `CLAUDE.md` — this file

---

## ⚠️ Active issue — image folder sync

Two copies of `מוצרים מסווגים` exist on the Mac:
1. `~/Downloads/skylite-github/מוצרים מסווגים/` — OLD, 105 files, what the site reads
2. `~/Downloads/מוצרים מסווגים/` — NEW, 387 files, where images have been curated (has HP HQ, בית הבאר, etc.)

**Fix (run line by line):**
```bash
cd ~/Downloads
mv skylite-github/"מוצרים מסווגים" skylite-github/"מוצרים מסווגים.bak"
cp -R "מוצרים מסווגים" skylite-github/
```

**After sync:** two MEDIA.walkon paths need swapping — `HP06.jpg` and `95.jpg` only exist in the old repo copy. Swap for images that exist in the synced folder.

**Verify sync worked:**
```bash
ls ~/Downloads/skylite-github/"מוצרים מסווגים/03 — סקיילייט מדרך/"
```
Should show HP HQ, בית הבאר, ספריה לאומית folders.

---

## Remaining tasks to ship (end-of-week)

### P0 — Must ship
1. **Finish walk-on pilot** — verify image sync, preview locally (`http://localhost:8100/#walkon`), fix broken MEDIA paths (HP06.jpg, 95.jpg)
2. **Fill project TODOs** — National Library, בית הבאר, HP HQ detail pages need: year, architect, 2–3 sentence description (yellow `[TODO]` placeholders in HTML)
3. **Roll out pilot to penthouse** — same media strip + project detail page pattern
4. **Roll out to fixed, retractable, structural, smoke**
5. **New project pages** — beyond the 3 walk-on ones already built

### P1 — Should ship
6. **Form success message** — improve "תודה רבה" with expectation-setting (response time, next step)
7. **Tech PDFs** — user-provided files, link in tech documentation section
8. **Button variant cleanup** — `btn-p`, `btn-pd`, `btn-s`, `btn-od` → consolidate to 2

### P2 — Nice to have
9. **Alt text** — Hebrew `alt` attributes on all images (accessibility + SEO)
10. **Meta descriptions** — unique per product page
11. **Final `/polish` pass** — run before deploy

---

## Installed skills

Skills live in `.claude/skills/`. Invoked with `/skill-name` in any Claude session.

### Design skills (impeccable suite) — use for site work

| Skill | When to invoke |
|---|---|
| `/critique` | Full UX review with scored heuristics. Re-run after major changes. |
| `/typeset` | If new sections are added and font sizing feels off. |
| `/polish` | **Run last, before final deploy.** Alignment, spacing, micro-detail pass. |
| `/audit` | Accessibility + performance check. Flags missing alt text, contrast issues. |
| `/colorize` | If any section feels flat or monochromatic. |
| `/redesign-existing-projects` | For deeper structural rethinks of a section. |
| `/impeccable` | Foundation skill — run `impeccable teach` only if starting from scratch. Context already in `.impeccable.md`. |

**Skip these** (wrong aesthetic for Skylite): `high-end-visual-design`, `design-taste-frontend`, `stitch-design-taste` — all assume dark/React stacks.

---

### Marketing skills — use for copy, SEO, and traffic

**For the site now (copy + positioning):**

| Skill | When to invoke |
|---|---|
| `/copywriting` | Write or rewrite any section — hero, product pages, CTAs, about. |
| `/copy-editing` | Review and tighten existing Hebrew copy for clarity and tone. |
| `/content-strategy` | Plan blog posts, case studies, or any content beyond the site itself. |
| `/competitor-profiling` | Research and profile competing skylight companies in Israel. |
| `/marketing-psychology` | Apply persuasion principles to copy, layout, and CTAs. |
| `/product-marketing-context` | Define positioning, messaging hierarchy, and value props. |

**For when you start pushing traffic:**

| Skill | When to invoke |
|---|---|
| `/seo-audit` | Full SEO audit of the site — titles, meta, headings, keywords, structure. |
| `/ai-seo` | Optimize for AI search engines (ChatGPT, Perplexity, Google AI Overviews). |
| `/programmatic-seo` | Scale SEO with templated pages (e.g. per city, product type, use case). |
| `/paid-ads` | Write and structure Google/Meta ad campaigns and landing pages. |
| `/ad-creative` | Generate and iterate ad copy and creatives for campaigns. |
| `/analytics-tracking` | Set up GA4, conversion tracking, and measurement for the site. |
| `/site-architecture` | Audit and improve URL structure, internal linking, and crawlability. |

**For growth beyond the site:**

| Skill | When to invoke |
|---|---|
| `/social-content` | Write Instagram/LinkedIn posts for @skyliteisrael. |
| `/lead-magnets` | Create downloadable assets (spec sheets, guides) to capture architect emails. |
| `/marketing-ideas` | Brainstorm campaigns, partnerships, or growth ideas. |

**Skip these for now**: `ab-test-setup` (need traffic first), `community-marketing` (not relevant), `aso-audit` (mobile app only).

---

### Use these for the remaining work:

| Skill | When to invoke |
|---|---|
| `/critique` | Run a full UX design review with scored heuristics. Re-run after major changes to track improvement. |
| `/typeset` | If any new sections are added and font sizing feels off. Already run once — don't re-run unless new content added. |
| `/polish` | **Run last, before final deploy.** Catches alignment, spacing inconsistencies, micro-detail issues. |
| `/audit` | Run for accessibility + performance check. Will flag missing alt text, contrast issues, heading hierarchy. |
| `/colorize` | If any section feels flat or monochromatic after gallery/project page work. |
| `/redesign-existing-projects` | If a section needs a deeper structural rethink rather than a tweak. |
| `/impeccable` | Foundation skill — run `impeccable teach` if starting a new session from scratch. Context is already in `.impeccable.md`. |

### Skip these (not relevant to this project):
- `high-end-visual-design` — prescribes dark/glassmorphism aesthetics that contradict Skylite's light, photography-led direction
- `design-taste-frontend` — React/Next.js focused; site is vanilla HTML
- `stitch-design-taste` — Same issue, framework-dependent

---

## Deploy workflow
```bash
git add index.html
git commit -m "Brief description"
git push origin main
# GitHub Pages updates in ~60 seconds
```

**If you get a lock error:**
```bash
rm ~/Downloads/skylite-github/.git/index.lock
```
Happens when GitHub Desktop is open alongside Terminal. Quit GitHub Desktop first.

---

## Contact info (use exactly)
```
סקיילייט בע"מ
אלכסנדר ינאי 8, א.ת סגולה, פתח תקווה
טל: 03-9343159 | פקס: 03-9311921
skylite@skylite.co.il
שעות פעילות: ראשון–חמישי 9:00–18:00
Instagram: @skyliteisrael → https://instagram.com/skyliteisrael/
```

---

## Brand brief (summary of `.impeccable.md`)

**Audiences (equal weight):**
- **Professionals** (architects, designers, contractors) — need technical credibility, named projects, compliance standards
- **Homeowners** (penthouses, villas) — need emotional inspiration, light/space photography, trust signals

**Brand personality:** precise · experienced · luminous

**Aesthetic:** Light mode. Teal accent on near-white. Photography leads, UI follows. Not SaaS, not corporate, not government.

**Primary goal:** Generate contact/quote inquiries. Secondary: establish Skylite as Israel's category leader so architects specify them by name.

---

## SEO (future work)
- Keywords: סקיילייט, גגון אור, חלון גג, פתח אוורור גג, שחרור עשן תקן EN 12101
- All product pages need unique `<title>` and `<meta description>`
- Images need Hebrew `alt` attributes
- Schema markup: LocalBusiness + Product
