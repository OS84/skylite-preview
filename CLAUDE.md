# Skylite — Claude Code Project Brief

## What this is
Single-file Hebrew RTL website for **Skylite** (סקיילייט), an Israeli skylight manufacturer based in Petah Tikva. The entire site lives in `index.html` — one file, no build system, no frameworks.

**Live site:** https://os84.github.io/skylite-preview/  
**Repo:** https://github.com/OS84/skylite-preview  
**Local preview:** `python3 -m http.server 8080` → http://localhost:8080

---

## Language & direction
- `lang="he" dir="rtl"` — everything flows right-to-left
- Font: **Heebo** (Google Fonts) — weights 300, 400, 500, 700, 900
- All copy is in Hebrew. Don't translate or change Hebrew text unless explicitly asked.

---

## Design system

### Color tokens (CSS vars in `:root`)
```
--cream:      #F4F6F8   (page background)
--chalk:      #E9EEF2   (subtle sections)
--dark:       #1A1E24   (primary text / dark backgrounds)
--dark-mid:   #252A32   (footers)
--accent:     #2B7A8C   (primary brand color — teal)
--accent-2:   #34909E
--accent-pale:#7FBCC8   (lighter teal, links)
--accent-deep:#1D5F6E   (hover states)
--sky:        #4F8FA0
--stone:      #6B7680   (secondary text)
--linen:      #F8FAFB
--sand:       #EDF1F4
--warm-gray:  #DDE3E8   (dividers)
--ease:       cubic-bezier(.25,.1,.25,1)
--ease-out:   cubic-bezier(0,0,.2,1)
--spring:     cubic-bezier(.16,1,.3,1)
```

### Typography scale
- Labels/eyebrows: `font-size:11px; letter-spacing:.22em; text-transform:uppercase; font-weight:300`
- Body: `font-size:15px; font-weight:300; line-height:1.75`
- Section titles: `font-size:clamp(28px,5vw,52px); font-weight:700`
- Keep it light and airy — prefer weight 300/400 over heavy text

### Spacing philosophy
Generous whitespace. Sections use `padding: 80px 0` on desktop, `48px 0` on tablet, `32px 0` mobile.

---

## File structure
```
skylite-github/
├── index.html              ← entire site (1200 lines)
├── CLAUDE.md               ← this file
├── .nojekyll               ← disables Jekyll on GitHub Pages
└── מוצרים מסווגים/         ← 104 compressed images (43MB)
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
JavaScript SPA — no server routing needed.

```js
showPage(pid)   // switches active product page
subTab(el, pid) // switches sub-tabs within a page
```

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
    'project name': [
      { s: 'folder/filename.jpg', c: 'optional caption' },
    ]
  },
  fixed: { ... },
  // retractable, walkon, structural, smoke
};
```
`renderGallery(pid)` reads `GALLERIES[pid]` and populates `#gal-{pid}`.

---

## Content already implemented
1. ✅ **Water philosophy** — `פילוסופיית המים` paragraph in the process/about section
2. ✅ **Motors section** — on smoke page: chain motor, piston motor, EN 12101 effective area, control hub
3. ✅ **Enriched footers** — all product pages have: full address, phone, fax, hours, Instagram link

### Contact info (use exactly as written)
```
סקיילייט בע"מ
אלכסנדר ינאי 8, א.ת סגולה, פתח תקווה
טל: 03-9343159 | פקס: 03-9311921
skylite@skylite.co.il
שעות פעילות: ראשון–חמישי 9:00–18:00
Instagram: @skyliteisrael → https://instagram.com/skyliteisrael/
```

---

## Coding conventions
- **No frameworks** — vanilla HTML/CSS/JS only
- **No external CSS libraries** — all styles are inline in `<style>` block in `<head>`
- **Inline styles for one-off tweaks** — use `style="..."` for small adjustments rather than adding new CSS classes
- **CSS classes for patterns** — if something repeats 3+ times, add a class
- **Mobile-first breakpoints:** `768px` (tablet), `480px` (mobile)
- **Images:** always reference as `./מוצרים מסווגים/folder/file.jpg` — keep Hebrew paths as-is
- **No video tags** — videos were stripped (too large for GitHub Pages). Use YouTube/Vimeo embeds if video is needed.

---

## Deploy workflow
```bash
git add index.html
git commit -m "Brief description of change"
git push origin main
# GitHub Pages updates in ~60 seconds
```

**If you get a lock error:**
```bash
rm ~/Downloads/skylite-github/.git/index.lock
rm ~/Downloads/skylite-github/.git/HEAD.lock   # if it exists
```
This happens when GitHub Desktop is open alongside Terminal. Quit GitHub Desktop before running git commands.

---

## Design goals & brand voice
- **Premium but approachable** — luxury product, not cold or corporate
- **Light and architectural** — lots of white space, clean lines, photography-led
- **Trust signals** — years of experience, named projects (מלון מצפה הימים, אוניברסיטת בר אילן, etc.)
- **Technical credibility** — EN 12101 compliance, engineering specs build confidence
- Tone of Hebrew copy: professional, warm, direct — not salesy

---

## SEO notes (for future work)
- Target keywords: סקיילייט, גגון אור, חלון גג, פתח אוורור גג, שחרור עשן תקן EN 12101
- All product pages need `<meta description>` tags
- Images need `alt` attributes in Hebrew
- Schema markup (LocalBusiness + Product) would be a high-value addition
- Page titles are all "Skylite — הנדסת האור" — each page should have a unique title

---

## Known issues (as of April 2026)
- GitHub Pages intermittently slow to deploy after large commits (43MB image folder)
- One unchecked div mismatch pre-exists in original HTML — not introduced by recent edits, not causing visible issues
- Videos excluded from deploy — hosted nowhere yet
