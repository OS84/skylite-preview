#!/bin/bash
# Apply all pending fixes — run from Mac Terminal:
#   cd ~/Downloads/skylite-github && bash fix-blank-page.sh

FILE="index.html"

if [ ! -f "$FILE" ]; then
  echo "❌ index.html not found. Make sure you're in ~/Downloads/skylite-github/"
  exit 1
fi

python3 << 'PYEOF'
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

changes = 0

# Fix 1: Close unclosed lightbox div
old1 = '<button class="lb-nav lb-next" onclick="lbNav(1)">&#8250;</button>\n\n<!-- Contact Modal -->'
new1 = '<button class="lb-nav lb-next" onclick="lbNav(1)">&#8250;</button>\n</div>\n\n<!-- Contact Modal -->'
if old1 in html:
    html = html.replace(old1, new1)
    changes += 1
    print("✅ Closed unclosed <div id='lightbox'>")
else:
    print("ℹ️  Lightbox already closed")

# Fix 2: Hero background
if '.hero{' in html and 'background:var(--sand)' in html:
    html = html.replace('background:var(--sand)', 'background:var(--dark)', 1)
    changes += 1
    print("✅ Hero background → var(--dark)")
else:
    print("ℹ️  Hero background already dark")

# Fix 3: Replace old logo SVG (dark bg version) with new beam logo
old_logo_dark = '<rect width="50" height="50" fill="#1A1E24"/><polygon points="26,0 50,0 50,30" fill="#E9EEF2"/><polygon points="33,0 50,0 50,20" fill="#E9EEF2" opacity=".35"/>'
new_logo_dark = '<rect width="50" height="50" fill="#1A1E24"/><path d="M26,0 L50,0 L50,50 L0,50 L0,40 C3,30 18,10 26,0Z" fill="#E9EEF2"/>'
if old_logo_dark in html:
    count = html.count(old_logo_dark)
    html = html.replace(old_logo_dark, new_logo_dark)
    changes += 1
    print(f"✅ Replaced {count} dark-bg logo(s) with new beam design")
else:
    print("ℹ️  Dark logos already updated")

# Fix 4: Replace old logo SVG (light bg version) with new beam logo
old_logo_light = '<rect width="50" height="50" fill="#E9EEF2"/><polygon points="26,0 50,0 50,30" fill="#1A1E24"/><polygon points="33,0 50,0 50,20" fill="#1A1E24" opacity=".35"/>'
new_logo_light = '<rect width="50" height="50" fill="#E9EEF2"/><path d="M26,0 L50,0 L50,50 L0,50 L0,40 C3,30 18,10 26,0Z" fill="#1A1E24"/>'
if old_logo_light in html:
    count = html.count(old_logo_light)
    html = html.replace(old_logo_light, new_logo_light)
    changes += 1
    print(f"✅ Replaced {count} light-bg logo(s) with new beam design")
else:
    print("ℹ️  Light logos already updated")

# Fix 5: Update nav wordmark to uppercase SKYLITE
if '<span class="nav-wordmark">Skylite</span>' in html:
    html = html.replace('<span class="nav-wordmark">Skylite</span>', '<span class="nav-wordmark">SKYLITE</span>')
    changes += 1
    print("✅ Nav wordmark → SKYLITE")
else:
    print("ℹ️  Nav wordmark already updated")

# Fix 6: Remove old water philosophy from statement section
water_old = '\u05de\u05d9\u05dd \u05ea\u05de\u05d9\u05d3 \u05d9\u05de\u05e6\u05d0\u05d5 \u05d0\u05ea \u05d4\u05d3\u05e8\u05da \u05d3\u05e8\u05da \u05de\u05e2\u05d8\u05e4\u05ea \u05d4\u05d0\u05d9\u05d8\u05d5\u05dd'
if 'font-style:italic' in html and water_old in html:
    lines = html.split('\n')
    new_lines = [l for l in lines if not ('font-style:italic' in l and water_old in l)]
    if len(new_lines) < len(lines):
        html = '\n'.join(new_lines)
        changes += 1
        print("✅ Removed old water philosophy from statement")

# Fix 7: Remove old water philosophy from process header
proc_water = 'font-size:13px;font-weight:300;color:var(--accent);line-height:1.75;max-width:320px'
if proc_water in html and '\u05e4\u05d9\u05dc\u05d5\u05e1\u05d5\u05e4\u05d9\u05d9\u05ea \u05d4\u05de\u05d9\u05dd' in html:
    import re
    html = re.sub(r'<p style="font-size:13px;font-weight:300;color:var\(--accent\)[^>]*>[^<]*\u05e4\u05d9\u05dc\u05d5\u05e1\u05d5\u05e4\u05d9\u05d9\u05ea[^<]*</p>', '', html)
    changes += 1
    print("✅ Removed old water philosophy from process header")

# Fix 8: Add water philosophy CSS + section if not present
if '.water{' not in html:
    water_css = """
    /* ═══ WATER PHILOSOPHY ═══ */
    .water{background:var(--dark);padding:120px 80px;position:relative;overflow:hidden}
    .water::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(43,122,140,.08) 0%,transparent 60%);pointer-events:none}
    .water-inner{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:start}
    .water-label{font-size:10px;font-weight:400;letter-spacing:.30em;color:var(--accent-pale);margin-bottom:28px}
    .water-quote{font-weight:900;font-size:clamp(24px,3vw,38px);line-height:1.25;color:#fff;margin-bottom:32px}
    .water-quote em{font-style:normal;color:var(--accent-pale)}
    .water-lead{font-size:17px;font-weight:300;line-height:1.85;color:rgba(255,255,255,.55);margin-bottom:40px}
    .water-points{display:grid;gap:28px}
    .water-point{display:grid;grid-template-columns:48px 1fr;gap:16px;align-items:start}
    .water-point-num{font-size:32px;font-weight:900;color:rgba(43,122,140,.35);line-height:1;font-feature-settings:'tnum'}
    .water-point-name{font-size:15px;font-weight:500;color:#fff;margin-bottom:4px}
    .water-point-desc{font-size:14px;font-weight:300;line-height:1.75;color:rgba(255,255,255,.45)}
    .water-divider{width:48px;height:1px;background:linear-gradient(90deg,var(--accent),transparent);margin-bottom:40px}
    @media(max-width:900px){.water-inner{grid-template-columns:1fr;gap:48px}.water{padding:80px 32px}}
    @media(max-width:480px){.water{padding:56px 24px}}
"""
    anchor = "    @media(max-width:1100px){.proc-grid"
    if anchor in html:
        html = html.replace(anchor, water_css + "\n" + anchor)
        changes += 1
        print("✅ Added water philosophy CSS")

if 'id="water-philosophy"' not in html:
    water_section = '''
<section class="water" id="water-philosophy">
  <div class="water-inner">
    <div>
      <div class="water-label rv">\u05e4\u05d9\u05dc\u05d5\u05e1\u05d5\u05e4\u05d9\u05d9\u05ea \u05d4\u05de\u05d9\u05dd</div>
      <h2 class="water-quote rv rv-d1">\u05d4\u05de\u05d9\u05dd \u05ea\u05de\u05d9\u05d3 \u05d9\u05de\u05e6\u05d0\u05d5 \u05d0\u05ea \u05d4\u05d3\u05e8\u05da<br>\u05d3\u05e8\u05da \u05de\u05e2\u05d8\u05e4\u05ea \u05d4\u05d0\u05d9\u05d8\u05d5\u05dd.\u05d4</h2>
      <p class="water-lead rv rv-d2">\u05d6\u05d5 \u05dc\u05d0 \u05e1\u05ea\u05dd \u05d0\u05de\u05e8\u05d4 \u2014 \u05d6\u05d4 \u05d4\u05e2\u05d9\u05e7\u05e8\u05d5\u05df \u05e9\u05de\u05e0\u05d7\u05d4 \u05db\u05dc \u05ea\u05db\u05e0\u05d5\u05df \u05e9\u05dc\u05e0\u05d5. \u05d1\u05de\u05e7\u05d5\u05dd \u05dc\u05e0\u05e1\u05d5\u05ea \u05dc\u05d7\u05e1\u05d5\u05dd \u05de\u05d9\u05dd \u05d1\u05db\u05d5\u05d7, \u05d0\u05e0\u05d7\u05e0\u05d5 \u05de\u05ea\u05db\u05e0\u05e0\u05d9\u05dd \u05de\u05e2\u05e8\u05db\u05d5\u05ea \u05e9\u05de\u05e0\u05d4\u05dc\u05d5\u05ea \u05d0\u05d5\u05ea\u05dd. \u05ea\u05e2\u05dc\u05d5\u05ea \u05e0\u05d9\u05e7\u05d5\u05d6 \u05e4\u05e0\u05d9\u05de\u05d9\u05d5\u05ea \u05d1\u05ea\u05d5\u05da \u05e4\u05e8\u05d5\u05e4\u05d9\u05dc\u05d9 \u05d4\u05d0\u05dc\u05d5\u05de\u05d9\u05e0\u05d9\u05d5\u05dd \u05de\u05d5\u05d1\u05d9\u05dc\u05d5\u05ea \u05db\u05dc \u05d8\u05d9\u05e4\u05d4 \u05d4\u05d7\u05d5\u05e6\u05d4 \u2014 \u05d1\u05dc\u05d9 \u05dc\u05d4\u05e1\u05ea\u05de\u05da \u05e2\u05dc \u05e1\u05d9\u05dc\u05d9\u05e7\u05d5\u05df \u05d1\u05dc\u05d1\u05d3.</p>
      <div class="water-divider rv rv-d2"></div>
      <p class="rv rv-d3" style="font-size:14px;font-weight:300;line-height:1.85;color:rgba(255,255,255,.4)">40 \u05e9\u05e0\u05d4 \u05e9\u05dc \u05d4\u05ea\u05e7\u05e0\u05d5\u05ea \u05d1\u05e4\u05e8\u05d5\u05d9\u05e7\u05d8\u05d9\u05dd \u05d7\u05e9\u05d5\u05e4\u05d9\u05dd \u05dc\u05ea\u05e0\u05d0\u05d9 \u05de\u05d6\u05d2 \u05d0\u05d5\u05d5\u05d9\u05e8 \u05e7\u05d9\u05e6\u05d5\u05e0\u05d9\u05d9\u05dd \u05dc\u05d9\u05de\u05d3\u05d5 \u05d0\u05d5\u05ea\u05e0\u05d5 \u05e9\u05d0\u05d8\u05d9\u05de\u05d5\u05ea \u05de\u05ea\u05d7\u05d9\u05dc\u05d4 \u05d1\u05ea\u05db\u05e0\u05d5\u05df \u2014 \u05dc\u05d0 \u05d1\u05e9\u05dc\u05d1 \u05d4\u05d0\u05d7\u05e8\u05d5\u05df \u05e9\u05dc \u05d4\u05d4\u05ea\u05e7\u05e0\u05d4.</p>
    </div>
    <div class="water-points rv rv-d2">
      <div class="water-point">
        <div class="water-point-num">01</div>
        <div>
          <div class="water-point-name">\u05e0\u05d9\u05e7\u05d5\u05d6 \u05e4\u05e0\u05d9\u05de\u05d9 \u05d1\u05e4\u05e8\u05d5\u05e4\u05d9\u05dc\u05d9\u05dd</div>
          <div class="water-point-desc">\u05d4\u05e4\u05e8\u05d5\u05e4\u05d9\u05dc\u05d9\u05dd \u05db\u05d5\u05dc\u05dc\u05d9\u05dd \u05ea\u05e2\u05dc\u05d5\u05ea \u05e0\u05d9\u05e7\u05d5\u05d6 \u05e4\u05e0\u05d9\u05de\u05d9 \u05d4\u05de\u05d5\u05e0\u05e2\u05d5\u05ea \u05d7\u05d3\u05d9\u05e8\u05ea \u05de\u05d9\u05dd \u05dc\u05d7\u05dc\u05dc \u05d4\u05de\u05d1\u05e0\u05d4, \u05db\u05d5\u05dc\u05dc \u05ea\u05e2\u05dc\u05d5\u05ea \u05d9\u05d9\u05e2\u05d5\u05d3\u05d9\u05d5\u05ea \u05dc\u05e0\u05d5\u05d6\u05dc\u05d9\u05dd \u05d4\u05e0\u05d5\u05e6\u05e8\u05d9\u05dd \u05de\u05d4\u05ea\u05e2\u05d1\u05d5\u05ea.</div>
        </div>
      </div>
      <div class="water-point">
        <div class="water-point-num">02</div>
        <div>
          <div class="water-point-name">\u05d0\u05d8\u05de\u05d9 EPDM \u05d0\u05d9\u05e0\u05d8\u05d2\u05e8\u05dc\u05d9\u05d9\u05dd</div>
          <div class="water-point-desc">\u05d0\u05d8\u05de\u05d9 EPDM \u05de\u05e9\u05d5\u05dc\u05d1\u05d9\u05dd \u05db\u05d7\u05dc\u05e7 \u05d0\u05d9\u05e0\u05d8\u05d2\u05e8\u05dc\u05d9 \u05d1\u05e4\u05e8\u05d5\u05e4\u05d9\u05dc\u05d9 \u05d4\u05d0\u05dc\u05d5\u05de\u05d9\u05e0\u05d9\u05d5\u05dd \u2014 \u05dc\u05d0 \u05de\u05d5\u05d3\u05d1\u05e7\u05d9\u05dd, \u05dc\u05d0 \u05e0\u05d3\u05d7\u05e1\u05d9\u05dd. \u05d0\u05e1\u05d5\u05e8 \u05dc\u05d4\u05d3\u05e7 \u05d0\u05d8\u05de\u05d9\u05dd \u05dc\u05e4\u05e8\u05d5\u05e4\u05d9\u05dc\u05d9\u05dd \u05d1\u05d0\u05de\u05e6\u05e2\u05d5\u05ea \u05d3\u05d1\u05e7.</div>
        </div>
      </div>
      <div class="water-point">
        <div class="water-point-num">03</div>
        <div>
          <div class="water-point-name">\u05d4\u05e4\u05e8\u05d3\u05d4 \u05de\u05d5\u05d7\u05dc\u05d8\u05ea \u05d6\u05db\u05d5\u05db\u05d9\u05ea-\u05d0\u05dc\u05d5\u05de\u05d9\u05e0\u05d9\u05d5\u05dd</div>
          <div class="water-point-desc">\u05d1\u05e9\u05d5\u05dd \u05e0\u05e7\u05d5\u05d3\u05d4 \u05d7\u05d5\u05de\u05e8 \u05d4\u05d6\u05d9\u05d2\u05d5\u05d2 \u05dc\u05d0 \u05d1\u05d0 \u05d1\u05de\u05d2\u05e2 \u05d9\u05e9\u05d9\u05e8 \u05e2\u05dd \u05d4\u05d0\u05dc\u05d5\u05de\u05d9\u05e0\u05d9\u05d5\u05dd. \u05d4\u05d6\u05db\u05d5\u05db\u05d9\u05ea \u05de\u05d4\u05d5\u05d3\u05e7\u05ea \u05d0\u05da \u05d5\u05e8\u05e7 \u05d1\u05d0\u05de\u05e6\u05e2\u05d5\u05ea \u05e4\u05e8\u05d5\u05e4\u05d9\u05dc\u05d9 \u05d4\u05d0\u05dc\u05d5\u05de\u05d9\u05e0\u05d9\u05d5\u05dd.</div>
        </div>
      </div>
      <div class="water-point">
        <div class="water-point-num">04</div>
        <div>
          <div class="water-point-name">\u05ea\u05e0\u05d5\u05e2\u05d4 \u05ea\u05e8\u05de\u05d9\u05ea \u05de\u05d1\u05d5\u05e7\u05e8\u05ea</div>
          <div class="water-point-desc">\u05d4\u05de\u05e2\u05e8\u05db\u05ea \u05de\u05ea\u05d5\u05db\u05e0\u05e0\u05ea \u05dc\u05d0\u05d8\u05d9\u05de\u05d5\u05ea \u05de\u05d5\u05d7\u05dc\u05d8\u05ea \u05d5\u05d1\u05d5 \u05d6\u05de\u05e0\u05d9\u05ea \u05dc\u05ea\u05e0\u05d5\u05e2\u05d4 \u05e9\u05dc \u05d7\u05d5\u05de\u05e8 \u05d4\u05d6\u05d9\u05d2\u05d5\u05d2 \u2014 \u05dc\u05de\u05e0\u05d9\u05e2\u05ea \u05d3\u05e4\u05d5\u05e8\u05de\u05e6\u05d9\u05d5\u05ea \u05d5\u05e2\u05d9\u05d5\u05d5\u05ea\u05d9\u05dd, \u05d2\u05dd \u05d1\u05ea\u05e0\u05d0\u05d9 \u05e7\u05d9\u05e6\u05d5\u05df.</div>
        </div>
      </div>
    </div>
  </div>
</section>
'''
    anchor2 = '<section class="projects" id="projects">'
    if anchor2 in html:
        html = html.replace(anchor2, water_section + '\n' + anchor2)
        changes += 1
        print("✅ Added water philosophy section")

if changes > 0:
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n🎉 Applied {changes} fix(es). Refresh http://localhost:8080")
else:
    print("\nℹ️  All fixes already applied.")
PYEOF

echo ""
echo "If the server isn't running: python3 -m http.server 8080"
