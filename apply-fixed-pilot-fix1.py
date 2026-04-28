#!/usr/bin/env python3
"""apply-fixed-pilot-fix1.py — Fix the mosaic gap problem on MEDIA.fixed.

The original 6-col mosaic produced ugly vertical gaps because aspect ratios
(3:2 wide, 2:3 tall, 1:1 default) didn't snap to a consistent unit grid.
With grid-auto-flow:dense, the layout couldn't pack tiles cleanly so
whitespace bled between rows.

This rewrite uses a 3-col grid where every tile's height is either 1 unit
(= one column-width) or 2 units. Rows always align.

Cell math (3-col grid):
  default — 1 col span, aspect 1:1  → 1 unit tall
  wide    — 2 col span, aspect 2:1  → 1 unit tall (= 1 default-row baseline)
  tall    — 1 col span, aspect 1:2 + grid-row span 2 → 2 units tall

Side benefit: default tile size now matches the existing uniform 3-col
grid the user is used to. Only the shape varies; the scale doesn't shrink.

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
# Replace the mosaic CSS rules with the 3-col snapping variant
# ═══════════════════════════════════════════════════════════════

OLD_MOSAIC_CSS = """    /* ── MOSAIC variant (pilot: fixed only) ── */
    .pp-media-grid--mosaic{grid-template-columns:repeat(6,1fr);grid-auto-flow:dense;gap:12px}
    .pp-media-grid--mosaic .pp-media-item{grid-column:span 2;aspect-ratio:1/1}
    .pp-media-grid--mosaic .pp-media-item.tile-w{grid-column:span 4;aspect-ratio:3/2}
    .pp-media-grid--mosaic .pp-media-item.tile-t{grid-column:span 2;aspect-ratio:2/3}
    @media(max-width:1024px){.pp-media-grid--mosaic{grid-template-columns:repeat(4,1fr)}.pp-media-grid--mosaic .pp-media-item.tile-w{grid-column:span 4}.pp-media-grid--mosaic .pp-media-item{grid-column:span 2}}
    @media(max-width:600px){.pp-media-grid--mosaic{grid-template-columns:1fr;gap:10px}.pp-media-grid--mosaic .pp-media-item,.pp-media-grid--mosaic .pp-media-item.tile-w,.pp-media-grid--mosaic .pp-media-item.tile-t{grid-column:span 1;aspect-ratio:4/3}}"""

NEW_MOSAIC_CSS = """    /* ── MOSAIC variant (pilot: fixed only) — 3-col grid, aspect ratios snap to unit grid ── */
    .pp-media-grid--mosaic{grid-template-columns:repeat(3,1fr);grid-auto-flow:dense;gap:12px}
    .pp-media-grid--mosaic .pp-media-item{grid-column:span 1;aspect-ratio:1/1}
    .pp-media-grid--mosaic .pp-media-item.tile-w{grid-column:span 2;aspect-ratio:2/1}
    .pp-media-grid--mosaic .pp-media-item.tile-t{grid-column:span 1;grid-row:span 2;aspect-ratio:1/2}
    @media(max-width:1024px){.pp-media-grid--mosaic{grid-template-columns:repeat(2,1fr)}.pp-media-grid--mosaic .pp-media-item.tile-w{grid-column:span 2}.pp-media-grid--mosaic .pp-media-item{grid-column:span 1}.pp-media-grid--mosaic .pp-media-item.tile-t{grid-row:span 2}}
    @media(max-width:600px){.pp-media-grid--mosaic{grid-template-columns:1fr;gap:10px}.pp-media-grid--mosaic .pp-media-item,.pp-media-grid--mosaic .pp-media-item.tile-w,.pp-media-grid--mosaic .pp-media-item.tile-t{grid-column:span 1;grid-row:span 1;aspect-ratio:4/3}}"""

swap(OLD_MOSAIC_CSS, NEW_MOSAIC_CSS, "Mosaic CSS: 6-col fragments → 3-col snapping grid")

# ═══════════════════════════════════════════════════════════════
# Untag Bar-Ilan from wide — it's already paired with HP06 and Mitzpe drone,
# 4 wide tiles in 15 was too many. Let it ride as a default square.
# ═══════════════════════════════════════════════════════════════
swap(
    "{ type:'img', src:'02 — סקיילייט קבוע/דו שיפועי/6ב - מנהלה בר אילן.jpg', cap:'מנהלה — בר אילן', aspect:'wide' },",
    "{ type:'img', src:'02 — סקיילייט קבוע/דו שיפועי/6ב - מנהלה בר אילן.jpg', cap:'מנהלה — בר אילן' },",
    "MEDIA.fixed: drop wide on Bar-Ilan (3 wide tiles is enough)",
    must_exist=False,
)

# ═══════════════════════════════════════════════════════════════
if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
