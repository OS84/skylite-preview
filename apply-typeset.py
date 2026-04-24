#!/usr/bin/env python3
"""Typeset pass: bump 10-11px labels to 12px, improve body text size/weight,
raise low-opacity white text on dark backgrounds for readability."""
PATH = '/Users/ohadshamir/Downloads/skylite-github/index.html'
html = open(PATH, encoding='utf-8').read()
changes = 0

FIXES = [
    # ── Labels 10px → 12px ──────────────────────────────────────────────────
    ('.hero-label{font-size:10px;',             '.hero-label{font-size:12px;'),
    ('.statement-num{font-size:10px;',          '.statement-num{font-size:12px;'),
    ('.sec-label{font-size:10px;',              '.sec-label{font-size:12px;'),
    ('.p-card-en{font-size:10px;',              '.p-card-en{font-size:12px;'),
    ('.thumb-type{font-size:10px;',             '.thumb-type{font-size:12px;'),
    ('.proc-num{font-size:10px;',               '.proc-num{font-size:12px;'),
    ('.water-label{font-size:10px;',            '.water-label{font-size:12px;'),
    ('.clients-label{font-size:10px;',          '.clients-label{font-size:12px;'),
    ('.pp-hero-cat{font-size:10px;',            '.pp-hero-cat{font-size:12px;'),

    # ── Labels 11px → 12px ──────────────────────────────────────────────────
    ('.p-card-num{font-size:11px;',             '.p-card-num{font-size:12px;'),
    ('.p-card-badge{display:inline-block;padding:4px 14px;background:var(--accent-deep);font-size:10px;',
     '.p-card-badge{display:inline-block;padding:4px 14px;background:var(--accent-deep);font-size:12px;'),
    ('.nav-cta{font-size:11px;',                '.nav-cta{font-size:12px;'),
    ('.pp-desc-label{font-size:11px;',          '.pp-desc-label{font-size:12px;'),
    ('.pp-chars-title{font-size:11px;',         '.pp-chars-title{font-size:12px;'),
    ('.pp-char-n{font-size:11px;',              '.pp-char-n{font-size:12px;'),
    ('.pp-gallery-t{font-size:11px;',           '.pp-gallery-t{font-size:12px;'),
    ('.pp-video-label{font-size:11px;',         '.pp-video-label{font-size:12px;'),
    ('.tech-hero-label{font-size:11px;',        '.tech-hero-label{font-size:12px;'),
    ('.f-copy{font-size:11px;',                 '.f-copy{font-size:12px;'),
    ('.form-note{font-size:11px;',              '.form-note{font-size:12px;'),
    ('#lb-cap{color:rgba(255,255,255,.55);font-size:11px;',
     '#lb-cap{color:rgba(255,255,255,.72);font-size:12px;'),
    ('#lb-counter{color:rgba(255,255,255,.45);font-size:11px;',
     '#lb-counter{color:rgba(255,255,255,.6);font-size:12px;'),

    # ── Body text: 14px weight-300 → 15px weight-400 ────────────────────────
    ('.proc-desc{font-size:14px;font-weight:300;',
     '.proc-desc{font-size:15px;font-weight:400;'),
    ('.tech-card-desc{font-size:14px;font-weight:300;',
     '.tech-card-desc{font-size:15px;font-weight:400;'),
    ('.tech-spec-val{font-size:14px;font-weight:300;',
     '.tech-spec-val{font-size:15px;font-weight:400;'),
    ('.pp-char-desc{font-size:14px;font-weight:300;',
     '.pp-char-desc{font-size:15px;font-weight:400;'),

    # ── Low-opacity white text on dark sections ──────────────────────────────
    ('.water-lead{font-size:17px;font-weight:300;line-height:1.85;color:rgba(255,255,255,.55);',
     '.water-lead{font-size:17px;font-weight:300;line-height:1.85;color:rgba(255,255,255,.75);'),
    ('.water-point-desc{font-size:14px;font-weight:300;line-height:1.75;color:rgba(255,255,255,.45)}',
     '.water-point-desc{font-size:15px;font-weight:400;line-height:1.75;color:rgba(255,255,255,.7)}'),
    ('.tech-hero-sub{font-size:17px;font-weight:300;color:rgba(255,255,255,.5);',
     '.tech-hero-sub{font-size:17px;font-weight:300;color:rgba(255,255,255,.72);'),
    ('.pp-hero-tag{font-size:clamp(16px,1.8vw,22px);font-weight:300;color:rgba(255,255,255,.55)}',
     '.pp-hero-tag{font-size:clamp(16px,1.8vw,22px);font-weight:300;color:rgba(255,255,255,.72)}'),
    # The inline water paragraph
    ('color:rgba(255,255,255,.4)">40 שנה של התקנות',
     'color:rgba(255,255,255,.65)">40 שנה של התקנות'),
]

for old, new in FIXES:
    if old in html:
        html = html.replace(old, new, 1)
        label = old.split('{')[0].strip().split('.')[-1][:30] if '{' in old else old[:40]
        print(f'✅ {label}')
        changes += 1
    else:
        label = old.split('{')[0].strip().split('.')[-1][:30] if '{' in old else old[:40]
        print(f'ℹ️  Already updated: {label}')

open(PATH, 'w', encoding='utf-8').write(html)
print(f'\n{"🎉 Applied "+str(changes)+" fix(es). Hard refresh to see changes." if changes else "✅ All changes already applied."}')
