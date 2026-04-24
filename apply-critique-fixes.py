#!/usr/bin/env python3
"""Apply critique fixes: conversion CTAs, gradient text removal, tech card icons."""
import re, sys
PATH = '/Users/ohadshamir/Downloads/skylite-github/index.html'
html = open(PATH, encoding='utf-8').read()
changes = 0

# 1. Remove gradient text from process step numbers
OLD = 'background:linear-gradient(160deg,rgba(43,122,140,.35),rgba(43,122,140,.15));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;'
NEW = 'color:rgba(43,122,140,.28);'
if OLD in html:
    html = html.replace(OLD, NEW, 1)
    print('✅ Removed gradient text from .proc-num-large')
    changes += 1
else:
    print('ℹ️  proc-num-large already updated')

# 2. Hide tech card icon boxes
OLD2 = '    .tech-card-icon{width:40px;height:40px;margin-bottom:20px;display:flex;align-items:center;justify-content:center;background:var(--dark);border-radius:6px}\n    .tech-card-icon svg{width:20px;height:20px;color:var(--accent)}'
NEW2 = '    .tech-card-icon{display:none}'
if OLD2 in html:
    html = html.replace(OLD2, NEW2, 1)
    print('✅ Hidden tech card icon boxes')
    changes += 1
else:
    print('ℹ️  tech-card-icon already updated')

# 3. Add CTA buttons to hero section
OLD3 = '  <p class="hero-sub" style="color:rgba(255,255,255,.6)">תכנון מדויק שמותאם לכל פרויקט — מהלופט הפרטי ועד הספריה הלאומית</p>\n  <div class="hero-scroll"'
NEW3 = '  <p class="hero-sub" style="color:rgba(255,255,255,.6)">תכנון מדויק שמותאם לכל פרויקט — מהלופט הפרטי ועד הספריה הלאומית</p>\n  <div style="margin-top:40px;display:flex;gap:16px;position:relative;z-index:1;flex-wrap:wrap">\n    <a href="#" onclick="openCM();return false" class="btn-p" style="width:auto;padding:16px 36px">קבלו הצעת מחיר</a>\n    <a href="#products" class="btn-s" style="width:auto;padding:16px 28px;border-color:rgba(255,255,255,.3);color:rgba(255,255,255,.8)">לצפייה במוצרים</a>\n  </div>\n  <div class="hero-scroll"'
if OLD3 in html:
    html = html.replace(OLD3, NEW3, 1)
    print('✅ Added CTA buttons to hero section')
    changes += 1
else:
    print('ℹ️  Hero CTAs already present')

# 4. Add CTA button in statement section
OLD4 = '    <a class="statement-link" href="#projects">\n      לפרויקטים שלנו\n      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 8h10M9 4l4 4-4 4"/></svg>\n    </a>\n  </div>\n</section>'
NEW4 = '    <a class="statement-link" href="#projects">\n      לפרויקטים שלנו\n      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 8h10M9 4l4 4-4 4"/></svg>\n    </a>\n    <a href="#" onclick="openCM();return false" class="btn-p" style="width:auto;display:inline-flex;margin-top:28px;padding:15px 32px">קבלו הצעת מחיר</a>\n  </div>\n</section>'
if OLD4 in html:
    html = html.replace(OLD4, NEW4, 1)
    print('✅ Added CTA button to statement section')
    changes += 1
else:
    print('ℹ️  Statement CTA already present')

open(PATH, 'w', encoding='utf-8').write(html)
if changes:
    print(f'\n🎉 Applied {changes} fix(es). Hard refresh to see changes.')
else:
    print('\n✅ All changes already applied — nothing to do.')
