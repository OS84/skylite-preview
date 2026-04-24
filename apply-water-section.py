#!/usr/bin/env python3
"""Rewrite the water philosophy section — tighter copy, verified specs only."""
PATH = '/Users/ohadshamir/Downloads/skylite-github/index.html'
html = open(PATH, encoding='utf-8').read()

OLD = '''<section class="water" id="water-philosophy">
  <div class="water-inner">
    <div>
      <div class="water-label rv">הנדסת אטימות</div>
      <h2 class="water-quote rv rv-d1">״רוב פתחי הגג נכשלים<br>בגלל מים. אנחנו פיתחנו<br><em>פרופיל שפותר את זה מיסודו.</em>״</h2>
      <p class="water-lead rv rv-d2">הגישה הנפוצה לאיטום — סיליקון, אטמים מודבקים, שכבות הגנה חיצוניות — מתיישנת. ובשנה השניה או השלישית, המים מוצאים את הדרך. אנחנו בחרנו עיקרון הנדסי שונה: לא לחסום מים בכוח, אלא לנהל אותם.</p>
      <div class="water-divider rv rv-d2"></div>
      <p class="rv rv-d3" style="font-size:15px;font-weight:400;line-height:1.85;color:rgba(255,255,255,.75);margin-bottom:20px">פרופיל האלומיניום הקנייני שפיתחנו לאורך 40 שנה טומן בתוכו מערכת ניקוז פנימית — תעלות מוחצנות בגוף הפרופיל עצמו, שמסיטות כל טיפה: גשם, עיבוי, גלישה צדדית — ומובילות אותה החוצה אוטומטית לפני שהיא מגיעה לפנים. ללא תלות בסיליקון. ללא תחזוקת אטימה.</p>
      <p class="rv rv-d3" style="font-size:15px;font-weight:400;line-height:1.85;color:rgba(255,255,255,.65)">זו לא תיאוריה: המערכת פועלת מזה עשרות שנים בפרויקטים כמו הספריה הלאומית, כנסת ישראל ומלון מצפה הימים — מבנים שבהם כשל חדירת מים הוא בגדר אסון תכנוני.</p>
    </div>'''

NEW = '''<section class="water" id="water-philosophy">
  <div class="water-inner">
    <div>
      <div class="water-label rv">הנדסת אטימות</div>
      <h2 class="water-quote rv rv-d1">״רוב פתחי הגג נכשלים<br>בגלל מים. אנחנו פיתחנו<br><em>פרופיל שפותר את זה מיסודו.</em>״</h2>
      <p class="water-lead rv rv-d2">הגישה הנפוצה — סיליקון ואטמים מודבקים — מתיישנת. אנחנו עובדים לפי עיקרון הנדסי שונה: פרופיל אלומיניום קנייני עם איטום ומירזוב עצמיים, שמנהל מים החוצה לפני שהם מגיעים לפנים. 40 שנה של פרויקטים בתנאי קיצון ישראלים הוכיחו שהמערכת עובדת.</p>
      <div class="water-divider rv rv-d2"></div>
    </div>'''

if OLD in html:
    html = html.replace(OLD, NEW, 1)
    print('✅ Water left column updated.')
else:
    print('❌ Could not find old left column — check for prior edits.')

OLD2 = '''      <div class="water-point">
        <div class="water-point-num">01</div>
        <div>
          <div class="water-point-name">פרופיל אלומיניום קנייני עם ניקוז מובנה</div>
          <div class="water-point-desc">תעלות הניקוז מוחצנות בגוף הפרופיל בתהליך הייצור — לא מתווספות בשלב ההרכבה. הפרופיל מתוכנן כך שמי גשם הספוחים דרך פתחי אוורור טכניים מוסטים מיידית למסלול ניקוז סגור, ומוצאים בנקודת ניקוז מוגדרת בבסיס המסגרת. אין נקודה בה מים יכולים להצטבר בתוך גוף הפרופיל.</div>
        </div>
      </div>
      <div class="water-point">
        <div class="water-point-num">02</div>
        <div>
          <div class="water-point-name">אטמי EPDM משולבים בייצור — לא מודבקים</div>
          <div class="water-point-desc">אטמי EPDM (Ethylene Propylene Diene Monomer) מוכנסים כחלק אינטגרלי מהפרופיל בתהליך הייצור — לא בשלב ההתקנה בשטח. EPDM מציע עמידות גבוהה לאוזון, קרינת UV וטמפרטורות קיצוניות (−40°C עד +120°C), ושומר על גמישות מלאה לאורך חיי המבנה. אטם שמוצב לאחר הייצור נדחס ומתיישן; אטם שחי בתוך הפרופיל — מוגן, יציב, יעיל לאורך זמן. הדבקת אטמים לפרופיל אינה מותרת בשום שלב של ההתקנה.</div>
        </div>
      </div>
      <div class="water-point">
        <div class="water-point-num">03</div>
        <div>
          <div class="water-point-name">ניקוז כפול — גשם ועיבוי בנפרד</div>
          <div class="water-point-desc">המערכת מטפלת בשני מקורות לחות שונים: מי גשם החודרים מבחוץ ועיבוי הנוצר על פני הזכוכית מצד פנים בשל הפרשי טמפרטורה. לכל אחד תעלת ניקוז ייעודית בתוך הפרופיל עם מסלול פינוי ויציאה נפרדים. ניהול שני המקורות בנפרד מונע הצטברות לחות — הגורם הנפוץ ביותר להידרדרות מבנית בפתחי גג שאינם מתוכננים כהלכה.</div>
        </div>
      </div>
      <div class="water-point">
        <div class="water-point-num">04</div>
        <div>
          <div class="water-point-name">הפרדה מוחלטת זכוכית–אלומיניום ותנועה תרמית מחושבת</div>
          <div class="water-point-desc">חומר הזיגוג לא בא במגע ישיר עם האלומיניום בשום נקודה לאורך המסגרת. הזכוכית מוחזקת אך ורק באמצעות פרופילי האלומיניום, עם מרווח תנועה מחושב. מקדמי ההתפשטות התרמית של אלומיניום וזכוכית שונים; תכנון שמתעלם מכך מייצר מאמצים שפוגעים באטימה לאורך זמן. המערכת בנויה לספוג את הדיפרנציאל הזה ולשמור על אטימות מלאה גם לאחר עשרות מחזורי חורף–קיץ.</div>
        </div>
      </div>'''

NEW2 = '''      <div class="water-point">
        <div class="water-point-num">01</div>
        <div>
          <div class="water-point-name">פרופיל אלומיניום קנייני עם ניקוז מובנה</div>
          <div class="water-point-desc">הפרופילים כוללים תעלות ניקוז פנימי המונעות חדירת מים לחלל המבנה — כולל תעלות ייעודיות לנוזלים הנוצרים מהתעבות. הניקוז מובנה בגוף הפרופיל בתהליך הייצור, לא מוסף בשלב ההרכבה.</div>
        </div>
      </div>
      <div class="water-point">
        <div class="water-point-num">02</div>
        <div>
          <div class="water-point-name">אטמי EPDM משולבים — לא מודבקים</div>
          <div class="water-point-desc">אטמי EPDM משולבים כחלק אינטגרלי בפרופילי האלומיניום. החלקה ויציאה של האטמים במשך הזמן — הדבקת אטמים לפרופיל אינה מותרת בשום שלב של ההתקנה.</div>
        </div>
      </div>
      <div class="water-point">
        <div class="water-point-num">03</div>
        <div>
          <div class="water-point-name">הפרדה מוחלטת זכוכית–אלומיניום</div>
          <div class="water-point-desc">בשום נקודה חומר הזיגוג לא בא במגע ישיר עם האלומיניום. הזכוכית מוחזקת אך ורק באמצעות פרופילי האלומיניום — עיקרון שמונע מתחים שמשפיעים על האטימה לאורך זמן.</div>
        </div>
      </div>
      <div class="water-point">
        <div class="water-point-num">04</div>
        <div>
          <div class="water-point-name">אטימות מוחלטת ותנועה תרמית — בו זמנית</div>
          <div class="water-point-desc">המערכת מתוכננת לאטימות מוחלטת ובמקביל לתנועה חופשית של חומר הזיגוג — למניעת דפורמציות ועיוותים גם בתנאי עומס תרמי קיצוני.</div>
        </div>
      </div>'''

if OLD2 in html:
    html = html.replace(OLD2, NEW2, 1)
    open(PATH, 'w', encoding='utf-8').write(html)
    print('✅ Water points updated. Hard refresh to see changes.')
else:
    print('❌ Could not find old water points — check for prior edits.')
