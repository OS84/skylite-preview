# Skylite — Design Audit Synthesis
**Date:** 2026-04-29
**Scope:** Navigation, mobile adaptation, paths health, projects↔products linking, wording/content quality, typography + color/contrast/design-system consistency
**Method:** 4 parallel Explore agents, read-only against `index.html` and supporting docs

---

## Executive read

The site is in better shape than the audit set out to expose. **Schema markup, robots.txt with full AI-bot allowlist, hreflang-ready hash routing, comprehensive WCAG AA contrast, full focus-ring coverage, smart back-navigation, stable type scale and color tokens** — these are all in place and working. There are no P0 ship-blockers.

The most consequential P1 finding cuts across two audits: **the hamburger menu renders on mobile but its drawer DOM is missing**. The CSS for `.nav-drawer` exists and the `toggleDrawer()` JS exists, but the HTML element they target was never built. On a phone today, tapping the hamburger does nothing visible. Highest-leverage single fix.

The second cluster is **content authenticity**: "אלפי פרויקטים" is unverified, the Fixed Skylight page opens with the exact "מגוון רחב" jargon the brand voice forbids, and 20+ CTAs share the same passive "השאירו פרטים" copy across pages. None of these are bugs — they're voice consistency drift that the marketing-skills layer can fix in a single content sprint.

The third cluster is **tech debt**: 4 button variants that could collapse to 2, ~17 inline color overrides that should be utility classes, ~150MB of uncompressed source images, and a windows product page filter chip with zero backing projects. None blocks ship, but each one will compound if not addressed before traffic ramps.

---

## Findings by axis

### 1. Navigation

**Strong:** All 11 page divs route correctly via `go()`, `goProject()`, `home()`. Nav branding (SKYLITE wordmark + צור קשר CTA) is consistent across every page. Mega-menu lists all 7 product categories in 4 logical groups. Project detail pages all use the smart `goBackFromProject()` handler — no stragglers with hardcoded `go('walkon')`. Footer link sets are principled (each page excludes self, includes related products).

**P1:** Mobile drawer DOM missing. `.nav-burger` button renders below 768px (line ~767), `.nav-drawer` CSS slides exist (lines 773–779), `toggleDrawer()` function exists (~line 2721), but the `<nav class="nav-drawer">…</nav>` element it targets is not in the HTML. Hamburger tap → no visible result. **This is the single biggest UX bug on the site for any mobile visitor.**

**P2:** Back-button text inconsistency on product pages. Penthouse and fixed say "חזרה לכל המוצרים"; walkon and retractable say only "חזרה". Pick one pattern. Recommend the longer form for clarity.

**P2:** No active-page indicator in the mega-menu. When you're on `#fixed`, the mega-menu doesn't visually highlight it.

### 2. Mobile adaptation

**Strong:** Breakpoint discipline (1100 / 1024 / 768 / 600px) is consistent across components. RTL holds together on every layout. Form inputs correctly pin `dir="ltr"` on phone/email fields. Reduced-motion respected. Viewport meta is correct, no `user-scalable=no` (a11y green flag).

**P1:** No mobile drawer (see Navigation).

**P2:** Two undersized touch targets on mobile — `.lb-close` is 36×36px (line 1068) and `.pp-ribbon-meta-arr button` is 32×32px (line 851). WCAG 2.5.5 minimum is 44×44. Both should bump to 44.

**P2:** No responsive image strategy. Hero banners load full-resolution on phones — biggest single contributor to mobile data cost. Adding `srcset` on heroes is ~2 hours and would cut median mobile page weight by 60–80%.

**P2:** Drawer slide direction in RTL needs visual QA on a real device — `translateX(100%) → translateX(0)` semantics may not produce the expected right-to-left slide animation in RTL contexts.

### 3. Paths health

**Strong:** **All 116+ MEDIA paths resolve on disk.** All PROJECTS hero and `images[]` paths resolve. All schema.org `image:` URLs resolve. All 12 video posters paired with their .mp4 source. No orphan files detected in spot-checked Use folders.

**P1:** `private-house-jaffa` (was `netiv-hamazalot`) lacks a schema.org JSON-LD entry in the head. Surfaces correctly in the gallery and `/projects` index but not for AI/SEO crawlers. Add an entry analogous to the other project schemas (~5-line block).

**P2:** Casing inconsistency — most Use folders are `Use/` (capital U) but `04 — מבנים מרחביים/חרוט/use/` and `02 — סקיילייט קבוע/חצר אנגלית/use/` are lowercase. Doesn't break paths (case-insensitive on macOS HFS+, but case-sensitive on Linux GitHub Pages servers). Standardize to `Use/`.

### 4. Projects ↔ Products linking

**Strong:** All 16 projects have unique slugs, valid categories, valid hero/images, and 14 of 16 have detail pages. PROJECTS_PAGE_ORDER is 100% covered (no orphans, no phantoms). All 5 PROJECTS_FILTER_SECTORS are used. Cross-tagging is working — `mitzpe-hayamim` correctly surfaces on both `#fixed` and `#smoke`.

**P1:** **`windows` filter chip is dead.** PROJECTS_FILTER_PRODUCTS lists windows as a chip (line 2768), but zero projects have `windows` in their categories. The chip exists but always returns empty results. Either (a) tag at least one existing project with `windows` if any project has skylight windows, (b) wait until the team adds a windows project, or (c) remove the chip until then.

**P1:** `private-house-jaffa` has no detail page (`<div id="page-project-private-house-jaffa">`). Falls back to lightbox on click — functional but inconsistent with how the National Library, HP HQ, etc. behave.

**P2:** Walk-on (2 projects) and structural (2 projects) are thin. Not broken — render with the existing empty-state guard handling — but the section feels under-stocked.

**P2:** HP HQ is tagged as "Project · Walk-On Glass" in its hero `pp-hero-cat` (line ~1597) but its primary product is fixed skylight. Minor taxonomy slip, ~30-second fix.

### 5. Wording + content (insights only — no rewrites)

**Voice grade:** 7.5/10. Strongest pages: home statement, water philosophy section, Structural Glazing, Retractable, project detail pages. Weakest page: **Fixed Skylight** — opens with "מתאפיין במגוון רחב של צורות ושימושים" which is the exact passive-voice + generic-jargon pattern the brand voice explicitly avoids.

**Top 3 strengths:**
- Hero taglines are a genuine creative achievement. "כאשר הגיאומטריה הופכת לשירה" (Structural), "גג שנפתח — שמיים שנכנסים" (Retractable), "הדלת שפותחת שמיים" (Roof Access). All three nail precise + experienced + luminous in 4–6 words.
- The water philosophy section (lines 1374–1407) is the persuasion engine — opens with the architect's deepest fear ("most roof openings fail due to water"), pivots to engineering mastery, closes with 40-year proof in Israeli climate.
- Named-project credibility is solid and consistently spelled — National Library, Mitzpe Hayamim, Recanati Winery all reinforce the same trust narrative across pages.

**Top 3 weaknesses:**
- "אלפי פרויקטים" (line 1267) is unverified hedging. Replace with an actual count or remove the noun.
- Fixed Skylight page opening copy speaks only to architects — homeowner perspective absent.
- 20+ CTA buttons say verbatim "השאירו פרטים". Zero audience differentiation, no zero-risk reassurance, no outcome framing.

**Specificity gaps to fact-check with the team:**
- Manufacturing lead time (parked-copy says 6–12 weeks — confirm)
- Total project count (replace "אלפי" with real number)
- Bar-Ilan and HP HQ commissioning years (currently `—` in meta)
- Architect attribution on a few projects (multiple `arch:'—'` placeholders)

**CTA standouts (keep these as voice exemplars):**
- Structural Glazing: "יש לכם חלום אדריכלי? נממש אותו יחד" (architect-aspirational, co-creation framing)
- Retractable: "יש לכם מרחב שצריך לנשום? בואו נתכנן יחד" (homeowner-experiential)
- Form success: "תודה רבה! קיבלנו את פרטיכם — נחזור אליכם תוך יום עסקים אחד" (specific time promise, reassurance)

### 6. Typography, color, design system

**Typography:** B+. Heebo loaded at all 5 weights (300/400/500/700/900) — all used. Type scale reads as 9 / 11 / 12 / 13 / 14 / 15 / 17 / 18 / 24px for utilities and `clamp()` fluid for headings. Hierarchy consistent. Letter-spacing pattern (`.22em` for eyebrows) consistent. Two minor inline `font-size` overrides are tech debt.

**Color & contrast:** A−. All 12 brand tokens defined and used. Zero hardcoded hex colors in the stylesheet (great discipline). **All major text-on-bg pairings pass WCAG AA, most exceed AAA** — body on cream is ~8.2:1, headings on cream ~14:1, accent links on cream ~4.8:1. Focus rings present on every interactive element, consistent 3px solid accent. ~17 inline color overrides in HTML body (links, hero text) — should be extracted to utility classes (.link-accent etc.) for future palette swaps.

**Design system:** B. Component patterns coherent (eyebrow labels, section headers, product cards, gallery items, project tiles). Spacing follows a 4px-base scale. Border-radius scale is minimal (12 / 8 / 6 / 4 / 3 / 1px). Shadow system has 4 elevation levels. Animation easing has 3 named curves (`--ease`, `--ease-out`, `--spring`).

**The 4-button-variant problem:** `.btn-p`, `.btn-pd`, `.btn-s`, `.btn-od` are at most 2 actual designs. `.btn-p` and `.btn-pd` are identical except for reset method. `.btn-s` and `.btn-od` differ only in font-size (13 vs 14px). Consolidate to `.btn-primary` and `.btn-secondary`.

**`.rv` reveal-on-scroll:** referenced in HTML but no CSS keyframe found in the stylesheet. Either it's JS-driven (likely) and working, or it's a no-op. Worth confirming on a fresh load.

**Unused token:** `--sand: #EDF1F4` is defined but not used anywhere. Either delete or document its intended use.

---

## Top 5 prioritized actions for the sprint queue

1. **Build the mobile nav drawer DOM.** CSS and JS already exist; just add the `<nav class="nav-drawer">…</nav>` element with a section-grouped link list mirroring the desktop mega-menu. Estimated effort: 1–2 hours including RTL slide-direction QA on a real phone.

2. **Add schema.org JSON-LD entry for `private-house-jaffa`** + build a project detail page for it (use `page-project-beit-habeer` as a template). Estimated effort: 30 minutes.

3. **Fix the windows filter chip.** Either tag at least one existing project as `windows`, or remove the chip from `PROJECTS_FILTER_PRODUCTS` until a windows project ships. Don't leave the chip dead.

4. **CTA copy diversification.** Replace generic "השאירו פרטים" with audience-segmented copy across product pages. Use Structural and Retractable CTAs as the model. Pair this with the "אלפי" verification + Fixed Skylight rewrite — single content-sprint deliverable.

5. **Image compression pass + responsive `srcset`.** Batch-compress all Use folder source images to ≤500KB at max 2400px wide (originals retained as masters), then add `srcset` on hero images. This bundles two of the heaviest performance wins into one sweep. Estimated effort: 2–3 hours including the bash script.

---

## What I did not audit (out of scope this round)

- **Lighthouse / Core Web Vitals** — would need live testing.
- **Real-device RTL behavior** — agents are read-only against code; some findings (drawer slide direction, touch target ergonomics) need physical device QA.
- **AI search citation tests** — querying ChatGPT, Perplexity, AI Overviews for target Hebrew keywords to see if Skylite is cited. Belongs in the AEO sprint.
- **Customer journey / conversion analytics** — no GA4 data was available.

---

## Backlog deltas this audit produced

These items were not in the task list before today; consider adding them:

- **Mobile drawer DOM build** (P1)
- **Schema entry + detail page for private-house-jaffa** (P1)
- **Windows filter chip resolution** (P1)
- **Inline color overrides → utility classes** (P2)
- **Button variant consolidation** (P2)
- **Touch target sizing fixes** (P2)
- **Folder casing standardization (Use vs use)** (P2)
- **Unused `--sand` token cleanup** (P2)
- **Reveal-on-scroll `.rv` confirmation** (P2)

---

**Audit complete.** The site has earned the right to ship — there are no P0 blockers. The P1 backlog (drawer, schema, dead chip, content tightening) totals roughly 1 day of work for someone familiar with the codebase.
