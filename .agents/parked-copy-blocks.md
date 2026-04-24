# Parked Copy Blocks

Content that's been drafted, reviewed, and approved but isn't placed on the site yet.
Keep these ready to drop in when the corresponding page/section gets built.

---

## "Right First Time" — for the About Us page

**Status:** Hebrew copy approved (Ohad, April 2026). Legally-reviewed — no liability-triggering phrases ("אחריות", "ערובה", warranty promises). Safe for site use.

**When to use:** When we build a dedicated "About Us / Why Skylite" page/section. Originally staged between stats and products on the home page but pulled to give About Us its own space.

**Recommended placement:** Primary positioning block on the About Us page, right after the page hero. Use as standalone centered section, `var(--linen)` background.

### Hebrew copy (final — Option 2)

**Headline:**
נכון מהפעם הראשונה. בזמן. בשלמות.
(highlight `בשלמות` in `var(--accent)` via `<em>` tag)

**Body (3 paragraphs):**

בפרויקט בנייה, כל עיכוב בגג עולה זמן וכסף. לכן אנחנו מלווים כל שלב — מהסקיצה, דרך ההנדסה והייצור, ועד ההתקנה בשטח.

כל פרויקט שונה. חלקם מורכבים במיוחד — גיאומטריות חריגות, עומסי רוח, שילוב עם קונסטרוקציה קיימת. אנחנו לא מתחמקים מהמורכבות; אנחנו מתכננים סביבה.

40 שנה של ניסיון, בקרת איכות קפדנית וצוות הנדסה בתוך הבית — זה הסטנדרט שלנו, ולזה אנחנו שואפים בכל פרויקט: סקיילייט שיוצא נכון מהפעם הראשונה, מגיע בזמן, ונמסר במלואו.

### Ready-to-paste HTML

```html
<section class="why-us" id="why-skylite">
  <div class="why-us-inner">
    <h2 class="why-us-title rv">נכון מהפעם הראשונה. בזמן. <em>בשלמות.</em></h2>
    <div class="why-us-body rv rv-d1">
      <p>בפרויקט בנייה, כל עיכוב בגג עולה זמן וכסף. לכן אנחנו מלווים כל שלב — מהסקיצה, דרך ההנדסה והייצור, ועד ההתקנה בשטח.</p>
      <p>כל פרויקט שונה. חלקם מורכבים במיוחד — גיאומטריות חריגות, עומסי רוח, שילוב עם קונסטרוקציה קיימת. אנחנו לא מתחמקים מהמורכבות; אנחנו מתכננים סביבה.</p>
      <p>40 שנה של ניסיון, בקרת איכות קפדנית וצוות הנדסה בתוך הבית — זה הסטנדרט שלנו, ולזה אנחנו שואפים בכל פרויקט: סקיילייט שיוצא נכון מהפעם הראשונה, מגיע בזמן, ונמסר במלואו.</p>
    </div>
  </div>
</section>
```

### Ready-to-paste CSS

```css
.why-us{background:var(--linen);padding:128px 48px 120px;text-align:center;position:relative;border-top:1px solid var(--warm-gray);border-bottom:1px solid var(--warm-gray)}
.why-us-inner{max-width:820px;margin:0 auto}
.why-us-title{font-weight:900;font-size:clamp(30px,4vw,52px);line-height:1.18;color:var(--dark);margin-bottom:44px;letter-spacing:-.005em}
.why-us-title em{font-style:normal;color:var(--accent)}
.why-us-body p{font-size:17px;font-weight:300;line-height:1.9;color:var(--stone);margin-bottom:22px}
.why-us-body p:last-child{margin-bottom:0}
.why-us-body strong{color:var(--dark);font-weight:500}
@media(max-width:1024px){.why-us{padding:88px 40px 88px}}
@media(max-width:600px){.why-us{padding:64px 24px 64px}.why-us-title{margin-bottom:32px}.why-us-body p{font-size:16px;line-height:1.85}}
```

### Legal notes (do not forget)

- Removed **"אנחנו לוקחים אחריות"** (we take responsibility) → replaced with **"אנחנו מלווים"** (we oversee) to avoid liability assumption
- Removed **"הערובה שלנו"** (our guarantee) → replaced with **"הסטנדרט שלנו, ולזה אנחנו שואפים"** (our standard — what we strive for) to avoid warranty-claim framing
- Never introduce **"ללא דליפות"** as a future-tense promise in marketing copy. Only safe as a stated historical fact ("מלון מצפה הימים, 14 שנה יבש")
- Source reference: Glazing Vision UK — adapted, not copied
