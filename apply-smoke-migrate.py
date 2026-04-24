#!/usr/bin/env python3
"""apply-smoke-migrate.py — Migrate smoke category from pp-selected-work → pp-media.

Changes:
  1. Add MEDIA.smoke array (12 curated tiles) inside the MEDIA={...} object.
  2. Swap <section class="pp-selected-work" id="selwork-smoke"> → pp-media / media-smoke.
  3. Init: remove 'smoke' from forEach(renderSelectedWork); add to forEach(renderMedia).
  4. Delete SELECTED_WORK.smoke entry (no longer referenced).

Smoke has no projects/videos — product strip only. Current SELECTED_WORK.smoke
includes one broken file (7.jpg doesn't exist on disk) — this migration fixes
that implicitly by picking from an audited list.

Idempotent.
"""
import sys, pathlib, re

HTML = pathlib.Path(__file__).parent / "index.html"
src = HTML.read_text(encoding="utf-8")
changes = 0

def swap(old, new, label):
    global src, changes
    if new in src:
        print(f"✔  {label} — already applied")
        return
    if old not in src:
        print(f"❌ {label} — anchor not found; aborting")
        sys.exit(1)
    src = src.replace(old, new, 1)
    changes += 1
    print(f"✔  {label}")

# ═══════════════════════════════════════════════════════════════
# 1. Add MEDIA.smoke inside the MEDIA={...} object.
#    Insert before the closing "};" of MEDIA by appending after the structural
#    entry's closing line "  ],".
# ═══════════════════════════════════════════════════════════════
SMOKE_ENTRY = """
  smoke: [
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/22.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/בית פרטי חד שיפועי שחרור עשן.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/AlfVjy-ryenVRYXksChGM_1Zu0pUByH44zoXInIzwZqq.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/גפני1.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/18.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/13 (1).jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/142.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/251.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/9.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/213.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/118.jpg' },
    { type:'img', src:'05 — כיפות תאורה, אוורור ושחרור עשן/262.jpg' },
  ],
"""

# We need to find the closing "];" of MEDIA.structural (the LAST entry currently)
# and insert SMOKE_ENTRY before the final "};" that closes MEDIA.
# Strategy: locate MEDIA={ then find its matching };. Just before that }, insert.
if "smoke: [" in src and "05 — כיפות תאורה, אוורור ושחרור עשן/22.jpg" in src:
    print("✔  MEDIA.smoke — already present")
else:
    m = re.search(r"const MEDIA\s*=\s*\{", src)
    if not m:
        print("❌ const MEDIA not found"); sys.exit(1)
    media_start = m.end()
    # Find the first "};" at column 0 after media_start
    close_match = re.search(r"\n\};", src[media_start:])
    if not close_match:
        print("❌ closing }; not found for MEDIA"); sys.exit(1)
    # Insert SMOKE_ENTRY right before "\n};"
    insert_at = media_start + close_match.start()
    src = src[:insert_at] + SMOKE_ENTRY.rstrip() + src[insert_at:]
    changes += 1
    print("✔  Added MEDIA.smoke (12 tiles)")

# ═══════════════════════════════════════════════════════════════
# 2. HTML: swap selwork-smoke → media-smoke
# ═══════════════════════════════════════════════════════════════
swap(
    '<section class="pp-selected-work" id="selwork-smoke"></section>',
    '<section class="pp-media" id="media-smoke"></section>',
    "HTML: swap selwork-smoke → media-smoke"
)

# ═══════════════════════════════════════════════════════════════
# 3a. Init: remove 'smoke' from renderSelectedWork list
# ═══════════════════════════════════════════════════════════════
swap(
    "['retractable','smoke'].forEach(renderSelectedWork);",
    "['retractable'].forEach(renderSelectedWork);",
    "Init: remove 'smoke' from renderSelectedWork"
)

# ═══════════════════════════════════════════════════════════════
# 3b. Init: add 'smoke' to renderMedia list
# ═══════════════════════════════════════════════════════════════
swap(
    "['walkon','penthouse','fixed','retractable','structural'].forEach(renderMedia);",
    "['walkon','penthouse','fixed','retractable','structural','smoke'].forEach(renderMedia);",
    "Init: add 'smoke' to renderMedia"
)

# ═══════════════════════════════════════════════════════════════
# 4. Remove SELECTED_WORK.smoke entry
# ═══════════════════════════════════════════════════════════════
OLD_SW = "  smoke:['05 — כיפות תאורה, אוורור ושחרור עשן/13 (1).jpg','05 — כיפות תאורה, אוורור ושחרור עשן/7.jpg','05 — כיפות תאורה, אוורור ושחרור עשן/18.jpg','05 — כיפות תאורה, אוורור ושחרור עשן/22.jpg','05 — כיפות תאורה, אוורור ושחרור עשן/9.jpg','05 — כיפות תאורה, אוורור ושחרור עשן/שחרור עשן.jpg','05 — כיפות תאורה, אוורור ושחרור עשן/בית פרטי חד שיפועי שחרור עשן.jpg','05 — כיפות תאורה, אוורור ושחרור עשן/AlfVjy-ryenVRYXksChGM_1Zu0pUByH44zoXInIzwZqq.jpg'],\n"
if OLD_SW in src:
    src = src.replace(OLD_SW, "", 1)
    changes += 1
    print("✔  Removed SELECTED_WORK.smoke entry")
else:
    print("✔  SELECTED_WORK.smoke — already removed")

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already fully applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
