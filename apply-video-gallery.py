#!/usr/bin/env python3
"""apply-video-gallery.py — Add a videos gallery section to product pages.

Adds:
  • CSS: .pp-videos-section / .pp-videos-grid / .pp-video-item / play-icon overlay
  • CSS: lightbox video-mode support (#lb-vid)
  • HTML: <video id="lb-vid"> inside the lightbox
  • HTML: <section class="pp-videos-section" id="videos-retractable"></section>
  • HTML: <section class="pp-videos-section" id="videos-penthouse"></section>
  • JS : VIDEOS data object  (retractable has 2 starter clips; penthouse empty)
  • JS : renderVideos(pid) + openLb/_lbUpdate/closeLb video handling
  • JS : init calls renderVideos for retractable + penthouse

Ships 2 retractable clips pre-populated as a test; fill in VIDEOS.penthouse
when you have penthouse-specific footage.

Idempotent: each insertion is skipped if its target string is already present.
"""
import sys, pathlib

HTML = pathlib.Path(__file__).parent / "index.html"
src  = HTML.read_text(encoding="utf-8")
changes = 0

def swap(old, new, label):
    """Insert `new` in place of `old`, exactly once, logging what happened."""
    global src, changes
    if new in src:
        print(f"✔  {label} — already applied, skipping")
        return
    if old not in src:
        print(f"❌ {label} — anchor not found; aborting")
        sys.exit(1)
    src = src.replace(old, new, 1)
    changes += 1
    print(f"✔  {label}")

# ══════════════════════════════════════════════════════════════════
# 1. CSS — video gallery grid + lightbox video mode
# ══════════════════════════════════════════════════════════════════
CSS_ANCHOR = "    @media(max-width:768px){.lb-prev{right:12px}.lb-next{left:12px}.lb-nav{width:36px;height:36px;font-size:22px}}"
CSS_ADD = CSS_ANCHOR + """
    #lb-vid{max-width:92vw;max-height:82vh;width:auto;height:auto;display:none;background:#000;border-radius:2px;outline:none}
    #lightbox.vid-mode #lb-img{display:none}
    #lightbox.vid-mode #lb-vid{display:block}

    /* ── VIDEO GALLERY ── */
    .pp-videos-section{background:var(--linen);padding:100px 0 120px;border-top:1px solid var(--warm-gray)}
    .pp-videos-section-h{padding:0 80px;margin-bottom:48px}
    .pp-videos-section-eye{font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--stone);font-weight:300;margin-bottom:12px}
    .pp-videos-section-t{font-size:clamp(28px,5vw,52px);font-weight:700;color:var(--dark);line-height:1.05;letter-spacing:-.01em}
    .pp-videos-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;padding:0 80px}
    .pp-video-item{position:relative;aspect-ratio:16/9;overflow:hidden;border-radius:6px;background:var(--dark);cursor:pointer}
    .pp-video-item img{width:100%;height:100%;object-fit:cover;transition:transform .8s var(--spring),filter .8s var(--spring);filter:brightness(.86)}
    .pp-video-item:hover img{transform:scale(1.04);filter:brightness(1)}
    .pp-video-item .play{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;pointer-events:none;transition:transform .4s var(--spring)}
    .pp-video-item .play svg{width:64px;height:64px;fill:#fff;filter:drop-shadow(0 4px 16px rgba(0,0,0,.55));opacity:.92;transition:opacity .3s,transform .4s var(--spring)}
    .pp-video-item:hover .play svg{opacity:1;transform:scale(1.08)}
    .pp-video-cap{position:absolute;left:16px;bottom:14px;right:16px;color:#fff;font-size:12px;letter-spacing:.08em;opacity:.88;pointer-events:none;text-shadow:0 1px 6px rgba(0,0,0,.6);direction:rtl}
    @media(max-width:1024px){.pp-videos-section{padding:70px 0 80px}.pp-videos-section-h,.pp-videos-grid{padding:0 48px}.pp-videos-grid{grid-template-columns:repeat(2,1fr)}}
    @media(max-width:600px){.pp-videos-section{padding:48px 0 56px}.pp-videos-section-h,.pp-videos-grid{padding:0 24px}.pp-videos-grid{grid-template-columns:1fr}.pp-video-item .play svg{width:52px;height:52px}}
  """
swap(CSS_ANCHOR + "\n  ", CSS_ADD, "CSS: video gallery + lightbox video mode")

# ══════════════════════════════════════════════════════════════════
# 2. HTML — add <video> element inside the lightbox
# ══════════════════════════════════════════════════════════════════
swap(
    '<img id="lb-img" src="" alt="">\n    <div class="lb-meta">',
    '<img id="lb-img" src="" alt="">\n    <video id="lb-vid" controls playsinline preload="metadata"></video>\n    <div class="lb-meta">',
    "HTML: lightbox <video> element"
)

# ══════════════════════════════════════════════════════════════════
# 3. HTML — add videos section on retractable page
# ══════════════════════════════════════════════════════════════════
swap(
    '<section class="pp-selected-work" id="selwork-retractable"></section>\n\n<section class="pp-cta"><h2 class="rv">יש לכם מרחב שצריך לנשום',
    '<section class="pp-selected-work" id="selwork-retractable"></section>\n<section class="pp-videos-section" id="videos-retractable"></section>\n\n<section class="pp-cta"><h2 class="rv">יש לכם מרחב שצריך לנשום',
    "HTML: videos section on retractable page"
)

# ══════════════════════════════════════════════════════════════════
# 4. HTML — add videos section on penthouse page
# ══════════════════════════════════════════════════════════════════
swap(
    '<section class="pp-projects-section" id="projects-sec-penthouse"></section>\n\n<section class="pp-cta"><h2 class="rv">מתכננים יציאה לגג',
    '<section class="pp-projects-section" id="projects-sec-penthouse"></section>\n<section class="pp-videos-section" id="videos-penthouse"></section>\n\n<section class="pp-cta"><h2 class="rv">מתכננים יציאה לגג',
    "HTML: videos section on penthouse page"
)

# ══════════════════════════════════════════════════════════════════
# 5. JS — add VIDEOS data + renderVideos + video-aware lightbox logic
# ══════════════════════════════════════════════════════════════════
JS_ANCHOR = "const _galReg={};"
JS_ADD = """const _galReg={};

// ── VIDEOS data: general assets per category, not tied to a specific project.
// Filenames relative to ./videos/  — each entry needs a matching .jpg poster.
const VIDEOS = {
  retractable: [
    { v:'retractable-01.mp4', p:'retractable-01.jpg', c:'סקיילייט נוסע — פתיחה מבוקרת' },
    { v:'retractable-02.mp4', p:'retractable-02.jpg', c:'קירוי זז — יציאה לחוץ' },
  ],
  penthouse: [
    // Populate when we have penthouse-specific footage:
    // { v:'penthouse-01.mp4', p:'penthouse-01.jpg', c:'description' },
  ],
};
const VB = './videos/';

function renderVideos(pid){
  const sec = document.getElementById('videos-'+pid);
  if(!sec) return;
  const vids = VIDEOS[pid];
  if(!vids || !vids.length){ sec.style.display='none'; return; }
  const key = 'vids-'+pid;
  const srcs = vids.map(v => VB+v.v);
  const caps = vids.map(v => v.c || '');
  const kinds = vids.map(() => 'vid');
  _galReg[key] = { srcs, caps, kinds };
  const playIcon = '<div class=\"play\"><svg viewBox=\"0 0 64 64\"><circle cx=\"32\" cy=\"32\" r=\"30\" fill=\"rgba(0,0,0,.35)\"/><path d=\"M26 20 L46 32 L26 44 Z\" fill=\"#fff\"/></svg></div>';
  const out = [`<div class=\"pp-videos-section-h\"><div class=\"pp-videos-section-eye\">וידאו</div><h2 class=\"pp-videos-section-t\">בתנועה</h2></div>`, `<div class=\"pp-videos-grid\">`];
  vids.forEach((v,i)=>{
    out.push(`<div class=\"pp-video-item\" onclick=\"openLb('${key}',${i})\"><img src=\"${VB}${v.p}\" alt=\"\" loading=\"lazy\">${playIcon}${v.c?`<div class=\"pp-video-cap\">${v.c}</div>`:''}</div>`);
  });
  out.push('</div>');
  sec.innerHTML = out.join('');
}
"""
swap(JS_ANCHOR, JS_ADD, "JS: VIDEOS data + renderVideos()")

# Init hook — add renderVideos for retractable + penthouse
swap(
    "['retractable','smoke','walkon'].forEach(renderSelectedWork);",
    "['retractable','smoke','walkon'].forEach(renderSelectedWork);\n['retractable','penthouse'].forEach(renderVideos);",
    "JS: init calls renderVideos"
)

# ══════════════════════════════════════════════════════════════════
# 6. JS — teach the lightbox to handle videos
# ══════════════════════════════════════════════════════════════════
# Replace _lbUpdate + closeLb with video-aware versions.
OLD_LB = """function closeLb(){
  document.getElementById('lightbox').classList.remove('open');
  document.body.style.overflow='';
}

function lbNav(dir){
  const reg=_galReg[_lbKey];
  if(!reg)return;
  _lbIdx=(_lbIdx+dir+reg.srcs.length)%reg.srcs.length;
  _lbUpdate();
}

function _lbUpdate(){
  const reg=_galReg[_lbKey];
  if(!reg)return;
  document.getElementById('lb-img').src=reg.srcs[_lbIdx];
  document.getElementById('lb-cap').textContent=reg.caps[_lbIdx]||'';
  document.getElementById('lb-counter').textContent=(_lbIdx+1)+' / '+reg.srcs.length;
}"""

NEW_LB = """function closeLb(){
  const lb=document.getElementById('lightbox');
  lb.classList.remove('open');
  lb.classList.remove('vid-mode');
  const v=document.getElementById('lb-vid');
  if(v){ v.pause(); v.removeAttribute('src'); v.load(); }
  document.body.style.overflow='';
}

function lbNav(dir){
  const reg=_galReg[_lbKey];
  if(!reg)return;
  _lbIdx=(_lbIdx+dir+reg.srcs.length)%reg.srcs.length;
  _lbUpdate();
}

function _lbUpdate(){
  const reg=_galReg[_lbKey];
  if(!reg)return;
  const lb=document.getElementById('lightbox');
  const src=reg.srcs[_lbIdx];
  const isVid=(reg.kinds&&reg.kinds[_lbIdx]==='vid')||/\\.(mp4|webm|mov)$/i.test(src);
  const vEl=document.getElementById('lb-vid');
  if(isVid){
    lb.classList.add('vid-mode');
    vEl.src=src;
    vEl.play().catch(()=>{});
  } else {
    lb.classList.remove('vid-mode');
    if(vEl){ vEl.pause(); vEl.removeAttribute('src'); vEl.load(); }
    document.getElementById('lb-img').src=src;
  }
  document.getElementById('lb-cap').textContent=reg.caps[_lbIdx]||'';
  document.getElementById('lb-counter').textContent=(_lbIdx+1)+' / '+reg.srcs.length;
}"""

swap(OLD_LB, NEW_LB, "JS: video-aware lightbox (_lbUpdate + closeLb)")

# ══════════════════════════════════════════════════════════════════
# Write it out
# ══════════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — everything already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
    print("   Preview locally: python3 -m http.server 8080 → http://localhost:8080/#retractable")
