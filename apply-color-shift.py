#!/usr/bin/env python3
"""apply-color-shift.py — Swap teal brand palette → deep-blue per PDF option 3.

New palette:
  --accent:      #2e3192 (primary — PDF color 2, אנרגטי טכנולוגי)
  --accent-2:    #4448b4 (15% lighter — secondary)
  --accent-pale: #8e93d4 (pale — for links on light bg, subtle hover)
  --accent-deep: #1e2169 (darker — for hover states on buttons)
  --sky:         #2a57a1 (PDF color 1, שמיים — complementary sky-blue)

Was:
  --accent:      #2B7A8C  (teal)
  --accent-2:    #34909E
  --accent-pale: #7FBCC8
  --accent-deep: #1D5F6E
  --sky:         #4F8FA0

Reversing: rerun with OLD and NEW swapped, or `git checkout -- index.html`.

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

swap("--accent:    #2B7A8C;",  "--accent:    #2e3192;",  "accent → #2e3192 (deep blue)")
swap("--accent-2:  #34909E;",  "--accent-2:  #4448b4;",  "accent-2 → #4448b4 (lighter)")
swap("--accent-pale:#7FBCC8;", "--accent-pale:#8e93d4;", "accent-pale → #8e93d4 (pale)")
swap("--accent-deep:#1D5F6E;", "--accent-deep:#1e2169;", "accent-deep → #1e2169 (darker, hover)")
swap("--sky:       #4F8FA0;",  "--sky:       #2a57a1;",  "sky → #2a57a1 (PDF color 1)")

if changes == 0:
    print("\n(No changes — already applied.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
    print("   All teal in the UI (CTAs, links, accents, hover) → now deep brand blue")
