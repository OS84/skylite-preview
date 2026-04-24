# Skylite — SEO + AEO Plan

*Approved by Ohad, April 2026. Captures full roadmap + immediate execution queue.*

---

## Status key

- 🟢 **APPROVED — EXECUTE** (items 1–4 below)
- 🟡 **PLANNED — pending trigger** (route refactor, content marketing)
- 🔵 **PLANNED — Ohad-owned** (GBP claim, PR outreach, Wikipedia editor)

---

## Immediate queue (🟢 approved, ship ASAP after current push)

### 1. Per-page `<title>`, `<meta description>`, OpenGraph + Twitter cards
**File:** `apply-seo-meta-tags.py`
**Target per-page:**
| Page | Title | Meta description (Hebrew, ≤160 chars) |
|---|---|---|
| home | סקיילייט — הנדסת אור מאז 1986 \| יצרנית סקיילייטים ישראלית | סקיילייט מתמחה בתכנון, ייצור והתקנה של סקיילייטים, כיפות, מבנים מרחביים וזיגוגים אדריכליים. 40 שנה בפרויקטים ברחבי ישראל. |
| about | אודות סקיילייט \| 40 שנה של הנדסת אור בישראל | החברה הוקמה ב-1986 ע"י אהרון שמיר. פתרונות גגות שקופים — תכנון, ייצור והתקנה לפרויקטים ציבוריים, מסחריים ופרטיים. |
| penthouse | סקיילייט ויציאה לגג לפנטהאוז \| סקיילייט | חלונות ליציאה לגג, לסוכה, לאוורור ושחרור עשן. מופעלים בשלט / מפסק / רכזת. התקנה מותאמת לכל פנטהאוז או וילה. |
| retractable | סקיילייט נוסע — גג שנפתח חשמלית \| סקיילייט | גג שנפתח חשמלית או ידנית — יחידה אחת או מספר חלקים נעים. קמרונות, שיפועים ופירמידות — בהתאמה אישית. |
| fixed | סקיילייט קבוע — חד ודו שיפועי \| סקיילייט | סקיילייט קבוע לגגות שטוחים ומשופעים. פרופילי אלומיניום 6063 TF, FLUSH GLAZING, התאמה אישית לכל פרויקט. |
| walkon | סקיילייט מדרך — רצפת זכוכית \| סקיילייט | סקיילייט במישור הרצפה — לחצרות פנימיות, אתרי מורשת וגשרים מזוגגים. זכוכית ביטחון מרובדת לעומסי הליכה. |
| structural | מבנים מרחביים — כיפות, פירמידות, קשתות \| סקיילייט | כיפות, פירמידות וקמרונות בהתאמה אישית. 40 שנה של ניסיון בגיאומטריות מורכבות. |
| smoke | כיפות תאורה ושחרור עשן EN 12101 \| סקיילייט | פתרונות אוורור ושחרור עשן העומדים בתקן EN 12101. בתי חולים, מבני ציבור, מסחר ומגורים. |
| project:* | Project name \| Skylite | Architect, year, location, product — rendered from PROJECTS data |

**OpenGraph per page:** `og:title`, `og:description`, `og:image` (hero), `og:type=website`, `og:locale=he_IL`.
**Twitter cards:** `twitter:card=summary_large_image`.

### 2. Schema.org JSON-LD
**File:** `apply-seo-schema.py`

**Inject per page, as `<script type="application/ld+json">` in `<head>`:**

- **Global on home page:**
  - `Organization` — name, founder (Aharon Shamir), foundingDate (1986), url, logo, contactPoint (phone, email), sameAs (instagram)
  - `LocalBusiness` — address (Alexander Yanai 8, Petach Tikva), geo (lookup coords), openingHours (Sun–Thu 9–18), telephone
- **Per product page:** `Product` with name, description, brand=Skylite, category
- **Per project detail page:** `CreativeWork` with name, creator (architect), locationCreated, dateCreated, about (the building)
- **FAQ page (future):** `FAQPage` with each Q&A

### 3. `robots.txt` + `sitemap.xml`
**Files:** `robots.txt`, `sitemap.xml` (static generation OK for now; revisit when blog exists)

**robots.txt explicitly allows AI crawlers:**
```
User-agent: *
Allow: /
Sitemap: https://skylite.co.il/sitemap.xml

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: CCBot
Allow: /

User-agent: Applebot-Extended
Allow: /
```

**sitemap.xml:** home + 6 product pages + about + all project detail pages + (future) FAQ + blog posts.

### 4. `llms.txt`
**File:** `llms.txt`

A plaintext summary designed for LLM consumption. Concise, factual, entity-rich. Template:

```
# Skylite (סקיילייט)

Skylite is an Israeli manufacturer of custom-engineered skylights and 
architectural glazing systems. Founded 1986 by Aharon Shamir. 
Headquartered at Alexander Yanai 8, Segula Industrial Zone, Petach Tikva, Israel.
Phone: +972-3-9343159. Email: skylite@skylite.co.il.

## Products

- Retractable skylights (electric or manual operation)
- Fixed skylights (single-slope, dual-slope, custom)
- Walk-on glass skylights (floor-level, for public buildings)
- Structural glazing: domes, pyramids, arches, cones
- Roof-access windows (penthouse, sukkah, ventilation, smoke vent)
- Light domes + smoke ventilation systems (EN 12101 compliant)

## Notable projects

- National Library of Israel, Jerusalem (2023) — walk-on skylight over main reading hall
  Architects: Herzog & de Meuron + Mann-Shinar
- HP HQ Mercury Building, Yehud (2012) — fixed + walk-on skylights
  Architects: Amir Mann & Ami Shenar
- Mitzpe Hayamim Hotel, Rosh Pina (2020 renovation) — dual-slope skylights
  Architects: Yehuda & Yoel Feigin
- Recanati Winery Visitor Center, Ramat Dalton — pyramid skylight
  Architects: Yaad Architects
- Beit Habeer Heritage Building, Kfar Saba (2014–2018) — walk-on skylight over historic well
  Architects: Amnon Bar-Or – Tal Gazit Architects
- Beit Gil HaZahav, Ramat HaHayal, Tel Aviv (2014) — dual-slope skylights with smoke vent
  Architects: Yashar Architects
- Beit Knesset Yagdil Torah, Or Yehuda — spatial dome
- Atidim Building, Tel Aviv — arched skylight

## Standards + materials

- EN 12101 (European smoke & heat exhaust ventilation standard)
- 6063 TF aluminum profiles
- EPDM integral seals
- FLUSH GLAZING method (glass held by aluminum only)

## Website

https://skylite.co.il

## Social

Instagram: https://instagram.com/skyliteisrael/
```

---

## Phase 2 — On-page optimization (🟡 after items 1–4 ship)

- Keyword-native copy audit
- H1/H2/H3 hierarchy review
- Internal linking (products ↔ projects)
- URL slugs in English (recommended) vs Hebrew
- **Route refactor from hash to real paths** — *prerequisite for SEO to actually work* — needs `_redirects` file on Cloudflare Pages / Netlify, or separate HTML files per page

---

## Phase 3 — Local + citations (🔵 Ohad-owned, first month post-launch)

- **Google Business Profile** — claim at google.com/business. Add photos, hours, services, description. Most important single SEO action.
- **Directory listings:** Dun's 100 (israelbusiness.co.il), BDI, D&B Israel, Ynet business
- **Architecture associations:** מועצת האדריכלות (archunion.co.il), Israel Builders Association
- **Google Maps / Waze** — verify pin at Alexander Yanai 8

---

## Phase 4 — Content marketing (🟡 ongoing)

### Project case studies (highest leverage)
Each named project = 1 long-form article. Template:
- Challenge (what the architect needed)
- Solution (what Skylite engineered)
- Outcome (final installation, named architect credit)
- Photo gallery

10+ named projects = 10+ indexable content pages.

### Technical guides
- איך לבחור בין סקיילייט קבוע לנוסע
- תקן EN 12101 — מדריך למתכננים
- זכוכית ביטחון למדרך — מה חשוב לדעת
- סקיילייט לפנטהאוז — צ'ק ליסט לאדריכלים

### FAQ page (high AEO value)
- מי היצרן של הסקיילייט בספרייה הלאומית?
- איזו חברה מייצרת סקיילייטים בישראל?
- איך לבחור סקיילייט לפנטהאוז?
- מה התקן לכיפות שחרור עשן?
- מהו סקיילייט מדרך?
- איך להזמין סקיילייט בהתאמה אישית?

### Blog (quarterly minimum)
Architecture trends, technical how-tos, project spotlights.

---

## AEO-specific tactics (🟡🔵 mix)

### Highest leverage moves

1. **Wikipedia article (Hebrew)** — company likely qualifies for notability (40 years, public projects). Single highest-impact AEO action. Requires neutral-tone writing + secondary-source citations. Can draft; needs submission by an experienced Hebrew Wikipedia editor.

2. **Press coverage** — pitch to:
   - **ynet אדריכלות**
   - **Globes** / **Calcalist** / **TheMarker**
   - **Architecture magazines** (עיצוב פנים, אדריכל)
   - Angles: "40 שנה של הנדסת אור", founder retrospective, "איך עושים סקיילייט לספרייה הלאומית", Atidim Building arched skylight story

3. **Architect partner backlinks** — ask Mann-Shinar, Amnon Bar-Or, Yashar Architects, Yaad Architects to credit Skylite with a link on their project pages

4. **Structured "facts" content** — About + FAQ + project pages with clear entity relationships (who + when + where + what)

5. **llms.txt** (item 4 above) — explicit feed for LLMs

6. **FAQPage schema** — converts FAQ content into LLM-friendly format

---

## Measurement

### SEO
- **Google Search Console** — claim domain, monitor impressions/clicks/positions weekly
- **Google Analytics 4** — sessions, top-entry pages, bounce rate, conversion events
- **Bing Webmaster Tools** — smaller but still worth submitting sitemap
- **Ahrefs / Semrush** (paid, optional) — backlink tracking, keyword position monitoring

### AEO
- **Monthly LLM spot-check** — ask ChatGPT, Claude, Perplexity, Gemini:
  - "Who makes custom skylights in Israel?"
  - "Who installed the skylight in the National Library of Israel?"
  - "איזו חברה מייצרת סקיילייטים בישראל?"
  - Track if Skylite gets cited and whether facts are accurate
- **Mentions monitoring** — Google Alerts for "סקיילייט" + company name

---

## Remember for the future

- **Ohad approved items 1–4 on April 24, 2026** — execute as `apply-seo-*.py` scripts as soon as current push lands
- **Ohad committed to doing everything required** — GBP claim, PR outreach, Wikipedia editor hire, architect partnership emails — will do whatever's needed for full SEO + AEO optimization
- **Before launch gate:** route refactor from hash to real paths is mandatory. Without real paths, phase 1 SEO work won't index.
- **Analytics IDs needed from Ohad:** GA4 measurement ID, Meta Pixel ID (if paid ads are in plan)
