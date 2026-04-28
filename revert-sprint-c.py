#!/usr/bin/env python3
"""revert-sprint-c.py — Roll back Sprint C nav changes if mega-menu doesn't land.

Restores:
  • Simple 4-link nav (מוצרים / פרויקטים / מידע טכני / עלינו)
  • #projects (no -strip suffix) on home
Removes:
  • Mega-menu CSS, panel, group HTML
  • Hamburger button + drawer DOM + toggleDrawer JS

Does NOT undo:
  • Any other Sprint A/B changes (those stay)
  • The new /projects page (still routable via go('projects') if needed)

Run only if user wants to back out the mega-menu specifically.
"""
import sys, pathlib

HTML = pathlib.Path(__file__).parent / "index.html"
src = HTML.read_text(encoding="utf-8")
changes = 0

def swap(old, new, label, must_exist=True):
    global src, changes
    if old not in src:
        if must_exist:
            print(f"❌ {label} — anchor not found")
            return
        return
    src = src.replace(old, new, 1)
    changes += 1
    print(f"✔  {label}")

# Restore #projects (drop -strip suffix on home)
swap('<section class="projects" id="projects-strip">',
     '<section class="projects" id="projects">',
     "Restore home id=projects")
swap('<a class="statement-link" href="#projects-strip">',
     '<a class="statement-link" href="#projects">',
     "Restore statement-link → #projects")

# Restore simple nav
NEW_NAV_PATTERN = '''  <ul class="nav-links">
    <li class="nav-mega">'''
SIMPLE_NAV = '''  <ul class="nav-links">
    <li><a href="#products">מוצרים</a></li>
    <li><a href="#" onclick="go(\'projects\');return false">פרויקטים</a></li>
    <li><a href="#" onclick="go(\'tech\');return false">מידע טכני</a></li>
    <li><a href="#" onclick="go(\'about\');return false">עלינו</a></li>
  </ul>
  <a href="#contact" class="nav-cta" onclick="openCM();return false">צור קשר</a>'''

# Find and replace the entire mega-menu nav block
import re
mega_block_pattern = re.compile(
    r'  <ul class="nav-links">\n    <li class="nav-mega">.*?</ul>\n  <a href="#contact" class="nav-cta"[^>]*>צור קשר</a>\n  <button class="nav-burger"[^>]*>(?:<span></span>){3}</button>',
    re.DOTALL
)
m = mega_block_pattern.search(src)
if m:
    src = src[:m.start()] + SIMPLE_NAV + src[m.end():]
    changes += 1
    print("✔  Restore simple nav block")

# Strip drawer DOM
drawer_pattern = re.compile(r'\n<!-- Mobile nav drawer -->\n<div class="nav-drawer" id="nav-drawer".*?</div>\n', re.DOTALL)
m = drawer_pattern.search(src)
if m:
    src = src[:m.start()] + src[m.end():]
    changes += 1
    print("✔  Remove drawer DOM")

# Strip toggleDrawer helper
toggle_pattern = re.compile(r'\nfunction toggleDrawer\(\)\{[^}]*\}\n', re.DOTALL)
m = toggle_pattern.search(src)
if m:
    src = src[:m.start()] + '\n' + src[m.end():]
    changes += 1
    print("✔  Remove toggleDrawer helper")

# Strip mega-menu + drawer CSS block (find by sentinel comment)
css_pattern = re.compile(
    r'    /\* ── MEGA-MENU NAV ── \*/.*?@media\(max-width:768px\)\{\s*.nav-burger\{display:flex\}\s*.nav-mega-panel\{display:none\}\s*\}\n',
    re.DOTALL
)
m = css_pattern.search(src)
if m:
    src = src[:m.start()] + src[m.end():]
    changes += 1
    print("✔  Remove mega-menu + drawer CSS")

if changes == 0:
    print("\n(Nothing to revert.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Reverted {changes} change(s)")
