#!/usr/bin/env python3
"""apply-nav-visibility.py — Bump nav font weight + contrast.

Current:
  • nav-wordmark: weight 300 (looks washed out)
  • nav-links a: weight 400 + rgba(255,255,255,.65) over hero (low contrast)
                 + rgba(28,26,22,.6) when scrolled (still low)
  • nav-back: rgba(28,26,22,.5) (hard to see)
  • nav-cta: weight 500, size 12px

After:
  • nav-wordmark: weight 500 (was 300)
  • nav-links a: weight 500 (was 400), size 14px (was 13), alpha .85 / .78
  • nav-back: alpha .72 (was .5), weight 500
  • nav-cta: weight 600 (was 500), size 13px (was 12)

Idempotent.
"""
import sys, pathlib

HTML = pathlib.Path(__file__).parent / "index.html"
src = HTML.read_text(encoding="utf-8")
changes = 0

def swap(old, new, label):
    global src, changes
    if new in src:
        print(f"✔  {label} — already applied")
        return
    if old not in src:
        print(f"❌ {label} — anchor not found")
        sys.exit(1)
    src = src.replace(old, new, 1)
    changes += 1
    print(f"✔  {label}")

swap(
    ".nav-wordmark{font-weight:300;font-size:14px;letter-spacing:.44em;color:#fff;text-transform:uppercase;transition:color .4s var(--ease)}",
    ".nav-wordmark{font-weight:500;font-size:14px;letter-spacing:.44em;color:#fff;text-transform:uppercase;transition:color .4s var(--ease)}",
    "Wordmark: weight 300 → 500"
)

swap(
    ".nav-links a{font-size:13px;font-weight:400;color:rgba(255,255,255,.65);letter-spacing:.06em;transition:color .4s;position:relative}",
    ".nav-links a{font-size:14px;font-weight:500;color:rgba(255,255,255,.85);letter-spacing:.06em;transition:color .4s;position:relative}",
    "Nav links: weight 400→500, size 13→14, alpha .65→.85"
)

swap(
    ".nav.scrolled .nav-links a{color:rgba(28,26,22,.6)}",
    ".nav.scrolled .nav-links a{color:rgba(28,26,22,.78)}",
    "Scrolled nav links: alpha .6 → .78"
)

swap(
    ".nav-back{display:flex;align-items:center;gap:8px;font-size:13px;color:rgba(28,26,22,.5);letter-spacing:.06em;transition:color .2s}",
    ".nav-back{display:flex;align-items:center;gap:8px;font-size:14px;font-weight:500;color:rgba(28,26,22,.72);letter-spacing:.06em;transition:color .2s}",
    "Back link: size 13→14, weight 500, alpha .5 → .72"
)

swap(
    ".nav-cta{font-size:12px;font-weight:500;letter-spacing:.14em;padding:9px 28px;border:1px solid rgba(255,255,255,.26);color:#fff;transition:all .35s var(--spring)}",
    ".nav-cta{font-size:13px;font-weight:600;letter-spacing:.14em;padding:9px 28px;border:1px solid rgba(255,255,255,.35);color:#fff;transition:all .35s var(--spring)}",
    "CTA: size 12→13, weight 500→600, border alpha .26→.35"
)

if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
