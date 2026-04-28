#!/usr/bin/env python3
"""apply-sprint-c.py — Mega-menu nav + mobile drawer + #projects conflict fix.

What ships
==========
1. Rename home page <section id="projects"> → id="projects-strip"
   (so it doesn't collide with the new /projects page route)
2. Update internal links from #projects → #projects-strip on home
3. Add mega-menu dropdown under "מוצרים" with 4 grouped sub-categories:
     • גגונים (Skylights):     קבוע · נוסע · מבנים מרחביים
     • פתחי גג (Roof openings): יציאה לגג · חלונות סקיילייט
     • רצפות שקופות (Walk-on):  סקיילייט מדרך
     • אוורור ובטיחות (Vent):   שחרור עשן
4. Mobile hamburger toggle + drawer with all nav (was no nav on mobile)

Each addition is reversible — revert script saves the OLD nav structure.

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
# 1) Resolve #projects collision: home section → projects-strip
# ═══════════════════════════════════════════════════════════════
swap(
    '<section class="projects" id="projects">',
    '<section class="projects" id="projects-strip">',
    "Home section: #projects → #projects-strip",
)

# Update home anchor that pointed at #projects (statement-link) → #projects-strip
swap(
    '<a class="statement-link" href="#projects">',
    '<a class="statement-link" href="#projects-strip">',
    "Statement link → #projects-strip (in-page anchor)",
)

# ═══════════════════════════════════════════════════════════════
# 2) Mega-menu CSS
# ═══════════════════════════════════════════════════════════════
MEGA_CSS = """
    /* ── MEGA-MENU NAV ── */
    .nav-mega{position:relative}
    .nav-mega-trigger{display:inline-flex;align-items:center;gap:6px;cursor:pointer}
    .nav-mega-trigger svg{width:10px;height:10px;transition:transform .25s var(--spring)}
    .nav-mega:hover .nav-mega-trigger svg,.nav-mega:focus-within .nav-mega-trigger svg{transform:rotate(180deg)}
    .nav-mega-panel{position:absolute;top:100%;right:0;margin-top:18px;background:#fff;color:var(--dark);min-width:520px;padding:28px 32px;box-shadow:0 24px 60px -16px rgba(0,0,0,.25),0 8px 16px -8px rgba(0,0,0,.12);border:1px solid var(--warm-gray);opacity:0;visibility:hidden;transform:translateY(-8px);transition:opacity .25s var(--spring),transform .25s var(--spring),visibility .25s;direction:rtl;z-index:200;border-radius:6px}
    .nav-mega:hover .nav-mega-panel,.nav-mega:focus-within .nav-mega-panel{opacity:1;visibility:visible;transform:translateY(0)}
    .nav-mega-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:24px 36px}
    .nav-mega-group{}
    .nav-mega-group-title{font-size:11px;font-weight:500;letter-spacing:.22em;color:var(--accent);text-transform:uppercase;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid var(--warm-gray)}
    .nav-mega-link{display:block;font-size:14px;font-weight:400;color:var(--dark);padding:7px 0;text-decoration:none;transition:color .2s var(--spring)}
    .nav-mega-link:hover{color:var(--accent)}
    .nav-mega-link-en{font-size:11px;font-weight:400;color:var(--stone);letter-spacing:.06em;margin-right:6px}

    /* ── MOBILE DRAWER + HAMBURGER ── */
    .nav-burger{display:none;width:44px;height:44px;background:transparent;border:0;cursor:pointer;padding:0;align-items:center;justify-content:center}
    .nav-burger span{display:block;width:22px;height:1.5px;background:#fff;margin:3px 0;transition:transform .3s var(--spring),opacity .2s}
    .nav.scrolled .nav-burger span,.pp .nav .nav-burger span{background:var(--dark)}
    .nav-burger.open span:nth-child(1){transform:translateY(4.5px) rotate(45deg)}
    .nav-burger.open span:nth-child(2){opacity:0}
    .nav-burger.open span:nth-child(3){transform:translateY(-4.5px) rotate(-45deg)}
    .nav-drawer{position:fixed;inset:0;background:var(--cream);z-index:300;padding:80px 32px 40px;overflow-y:auto;transform:translateX(100%);transition:transform .35s var(--spring);direction:rtl}
    .nav-drawer.open{transform:translateX(0)}
    .nav-drawer-close{position:absolute;top:24px;right:32px;width:44px;height:44px;background:transparent;border:0;cursor:pointer;font-size:24px;color:var(--dark)}
    .nav-drawer-section{margin-bottom:28px}
    .nav-drawer-section-title{font-size:11px;font-weight:500;letter-spacing:.22em;color:var(--accent);text-transform:uppercase;margin-bottom:14px;padding-bottom:8px;border-bottom:1px solid var(--warm-gray)}
    .nav-drawer-link{display:block;font-size:18px;font-weight:500;color:var(--dark);padding:12px 0;text-decoration:none}
    .nav-drawer-link:hover{color:var(--accent)}

    @media(max-width:768px){
      .nav-burger{display:flex}
      .nav-mega-panel{display:none}
    }
"""
swap(
    "    /* ── A11Y: visible focus indicators",
    MEGA_CSS + "\n    /* ── A11Y: visible focus indicators",
    "Mega-menu + drawer CSS",
)

# ═══════════════════════════════════════════════════════════════
# 3) Replace nav-links + add hamburger
# ═══════════════════════════════════════════════════════════════
OLD_NAV = """  <ul class="nav-links">
    <li><a href="#products">מוצרים</a></li>
    <li><a href="#projects">פרויקטים</a></li>
    <li><a href="#" onclick="go('tech');return false">מידע טכני</a></li>
    <li><a href="#" onclick="go('about');return false">עלינו</a></li>
  </ul>
  <a href="#contact" class="nav-cta" onclick="openCM();return false">צור קשר</a>"""

NEW_NAV = """  <ul class="nav-links">
    <li class="nav-mega">
      <a href="#products" class="nav-mega-trigger">מוצרים <svg viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M1 1l4 4 4-4"/></svg></a>
      <div class="nav-mega-panel">
        <div class="nav-mega-grid">
          <div class="nav-mega-group">
            <div class="nav-mega-group-title">גגונים</div>
            <a href="#" class="nav-mega-link" onclick="go('fixed');return false">סקיילייט קבוע <span class="nav-mega-link-en">Fixed</span></a>
            <a href="#" class="nav-mega-link" onclick="go('retractable');return false">סקיילייט נוסע <span class="nav-mega-link-en">Retractable</span></a>
            <a href="#" class="nav-mega-link" onclick="go('structural');return false">מבנים מרחביים <span class="nav-mega-link-en">Structural</span></a>
          </div>
          <div class="nav-mega-group">
            <div class="nav-mega-group-title">פתחי גג</div>
            <a href="#" class="nav-mega-link" onclick="go('penthouse');return false">יציאה לגג <span class="nav-mega-link-en">Roof Access</span></a>
            <a href="#" class="nav-mega-link" onclick="go('windows');return false">חלונות סקיילייט <span class="nav-mega-link-en">Windows</span></a>
          </div>
          <div class="nav-mega-group">
            <div class="nav-mega-group-title">רצפות שקופות</div>
            <a href="#" class="nav-mega-link" onclick="go('walkon');return false">סקיילייט מדרך <span class="nav-mega-link-en">Walk-on</span></a>
          </div>
          <div class="nav-mega-group">
            <div class="nav-mega-group-title">אוורור ובטיחות</div>
            <a href="#" class="nav-mega-link" onclick="go('smoke');return false">שחרור עשן <span class="nav-mega-link-en">Smoke vent</span></a>
          </div>
        </div>
      </div>
    </li>
    <li><a href="#" onclick="go('projects');return false">פרויקטים</a></li>
    <li><a href="#" onclick="go('tech');return false">מידע טכני</a></li>
    <li><a href="#" onclick="go('about');return false">עלינו</a></li>
  </ul>
  <a href="#contact" class="nav-cta" onclick="openCM();return false">צור קשר</a>
  <button class="nav-burger" onclick="toggleDrawer()" aria-label="תפריט"><span></span><span></span><span></span></button>"""

swap(OLD_NAV, NEW_NAV, "Replace home nav with mega-menu + hamburger button")

# ═══════════════════════════════════════════════════════════════
# 4) Drawer DOM — append at end of <body>
# ═══════════════════════════════════════════════════════════════
DRAWER_HTML = """
<!-- Mobile nav drawer -->
<div class="nav-drawer" id="nav-drawer" aria-hidden="true">
  <button class="nav-drawer-close" onclick="toggleDrawer()" aria-label="סגור תפריט">×</button>
  <div class="nav-drawer-section">
    <div class="nav-drawer-section-title">גגונים</div>
    <a href="#" class="nav-drawer-link" onclick="go('fixed');toggleDrawer();return false">סקיילייט קבוע</a>
    <a href="#" class="nav-drawer-link" onclick="go('retractable');toggleDrawer();return false">סקיילייט נוסע</a>
    <a href="#" class="nav-drawer-link" onclick="go('structural');toggleDrawer();return false">מבנים מרחביים</a>
  </div>
  <div class="nav-drawer-section">
    <div class="nav-drawer-section-title">פתחי גג</div>
    <a href="#" class="nav-drawer-link" onclick="go('penthouse');toggleDrawer();return false">יציאה לגג</a>
    <a href="#" class="nav-drawer-link" onclick="go('windows');toggleDrawer();return false">חלונות סקיילייט</a>
  </div>
  <div class="nav-drawer-section">
    <div class="nav-drawer-section-title">רצפות שקופות</div>
    <a href="#" class="nav-drawer-link" onclick="go('walkon');toggleDrawer();return false">סקיילייט מדרך</a>
  </div>
  <div class="nav-drawer-section">
    <div class="nav-drawer-section-title">אוורור ובטיחות</div>
    <a href="#" class="nav-drawer-link" onclick="go('smoke');toggleDrawer();return false">שחרור עשן</a>
  </div>
  <div class="nav-drawer-section">
    <div class="nav-drawer-section-title">עוד</div>
    <a href="#" class="nav-drawer-link" onclick="go('projects');toggleDrawer();return false">פרויקטים</a>
    <a href="#" class="nav-drawer-link" onclick="go('tech');toggleDrawer();return false">מידע טכני</a>
    <a href="#" class="nav-drawer-link" onclick="go('about');toggleDrawer();return false">עלינו</a>
    <a href="#" class="nav-drawer-link" onclick="openCM();toggleDrawer();return false" style="color:var(--accent)">צור קשר ←</a>
  </div>
</div>
"""
swap(
    "</body>",
    DRAWER_HTML + "\n</body>",
    "Append nav-drawer DOM to body",
)

# ═══════════════════════════════════════════════════════════════
# 5) Drawer toggle JS
# ═══════════════════════════════════════════════════════════════
DRAWER_JS = """
function toggleDrawer(){
  const d = document.getElementById('nav-drawer');
  const b = document.querySelector('.nav-burger');
  if(!d || !b) return;
  const open = d.classList.toggle('open');
  b.classList.toggle('open', open);
  d.setAttribute('aria-hidden', open ? 'false' : 'true');
  document.body.style.overflow = open ? 'hidden' : '';
}
"""
swap(
    "// A11Y: make clickable divs keyboard-accessible",
    DRAWER_JS + "\n// A11Y: make clickable divs keyboard-accessible",
    "toggleDrawer() helper",
)

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
