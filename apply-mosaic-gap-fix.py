#!/usr/bin/env python3
"""apply-mosaic-gap-fix.py — Snap mosaic tile heights to a unit grid.

Bug: aspect-ratio on grid items doesn't include the internal gap that
lives inside a multi-column span. So:
  sq  (span 1 col)         → height = col-width
  wide (span 2 col @ 2:1)  → height = (2·col + gap) / 2 = col-width + ½·gap

That ½·gap = 6px (with gap:12px) shows up as a sliver of cream below the
wide tile vs. its sq neighbor.

Fix: drop aspect-ratio on mosaic tiles and use `grid-auto-rows: <col-width>`
instead. All rows are exactly one column-width tall, so any tile spanning
1 row aligns perfectly with any other 1-row tile in that row, regardless
of column span.

Math behind the auto-rows value:
  page padding (.pp-media-grid):      80px each side
  column gap:                          12px
  3 cols → row height = (100vw - 2·80 - 2·12) / 3 = (100vw - 184px) / 3
  2 cols → row height = (100vw - 2·48 - 1·12) / 2 = (100vw - 108px) / 2
  1 col  → fall back to aspect-ratio:4/3 (single-column mode, no math gymnastics)

Idempotent.
"""
import sys, pathlib

HTML = pathlib.Path(__file__).parent / "index.html"
src = HTML.read_text(encoding="utf-8")

OLD = """    /* ── MOSAIC variant (pilot: fixed only) — 3-col grid, aspect ratios snap to unit grid ── */
    .pp-media-grid--mosaic{grid-template-columns:repeat(3,1fr);grid-auto-flow:dense;gap:12px}
    .pp-media-grid--mosaic .pp-media-item{grid-column:span 1;aspect-ratio:1/1}
    .pp-media-grid--mosaic .pp-media-item.tile-w{grid-column:span 2;aspect-ratio:2/1}
    .pp-media-grid--mosaic .pp-media-item.tile-t{grid-column:span 1;grid-row:span 2;aspect-ratio:1/2}
    @media(max-width:1024px){.pp-media-grid--mosaic{grid-template-columns:repeat(2,1fr)}.pp-media-grid--mosaic .pp-media-item.tile-w{grid-column:span 2}.pp-media-grid--mosaic .pp-media-item{grid-column:span 1}.pp-media-grid--mosaic .pp-media-item.tile-t{grid-row:span 2}}
    @media(max-width:600px){.pp-media-grid--mosaic{grid-template-columns:1fr;gap:10px}.pp-media-grid--mosaic .pp-media-item,.pp-media-grid--mosaic .pp-media-item.tile-w,.pp-media-grid--mosaic .pp-media-item.tile-t{grid-column:span 1;grid-row:span 1;aspect-ratio:4/3}}"""

NEW = """    /* ── MOSAIC variant (pilot: fixed + structural) — uniform row heights via grid-auto-rows ── */
    /* Row height tracks column width exactly — eliminates ½·gap bottom-edge misalignment */
    .pp-media-grid--mosaic{grid-template-columns:repeat(3,1fr);grid-auto-rows:calc((100vw - 184px) / 3);grid-auto-flow:dense;gap:12px}
    .pp-media-grid--mosaic .pp-media-item{grid-column:span 1;grid-row:span 1;aspect-ratio:auto}
    .pp-media-grid--mosaic .pp-media-item.tile-w{grid-column:span 2;grid-row:span 1}
    .pp-media-grid--mosaic .pp-media-item.tile-t{grid-column:span 1;grid-row:span 2}
    @media(max-width:1024px){.pp-media-grid--mosaic{grid-template-columns:repeat(2,1fr);grid-auto-rows:calc((100vw - 108px) / 2)}.pp-media-grid--mosaic .pp-media-item.tile-w{grid-column:span 2}.pp-media-grid--mosaic .pp-media-item{grid-column:span 1}.pp-media-grid--mosaic .pp-media-item.tile-t{grid-row:span 2}}
    @media(max-width:600px){.pp-media-grid--mosaic{grid-template-columns:1fr;grid-auto-rows:auto;gap:10px}.pp-media-grid--mosaic .pp-media-item,.pp-media-grid--mosaic .pp-media-item.tile-w,.pp-media-grid--mosaic .pp-media-item.tile-t{grid-column:span 1;grid-row:span 1;aspect-ratio:4/3}}"""

if NEW in src:
    print("✔ Already applied")
elif OLD in src:
    src = src.replace(OLD, NEW, 1)
    HTML.write_text(src, encoding="utf-8")
    print("✅ Mosaic CSS: grid-auto-rows now drives row heights")
    print("   Result: all tiles in any row align to the bottom, no ½·gap drift")
else:
    print("❌ Old CSS block not found — file may have drifted")
    sys.exit(1)
