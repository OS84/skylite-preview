#!/usr/bin/env python3
"""apply-revert-to-teal.py — Revert the deep-blue palette back to original teal.

Design-agent review flagged the #2e3192 deep blue as (1) too corporate for a
brand that positions as "luminous", (2) competing with real blue sky in the
photography, and (3) creating visual discord with hardcoded rgba(43,122,140,...)
teal values that never got migrated.

Cleanest fix: full revert. Hardcoded rgbas naturally re-align with the CSS
variables without any extra work.

Idempotent.
"""
import sys, pathlib

HTML = pathlib.Path(__file__).parent / "index.html"
src = HTML.read_text(encoding="utf-8")
changes = 0

def swap(old, new, label):
    global src, changes
    if new in src:
        print(f"✔  {label} — already reverted")
        return
    if old not in src:
        print(f"❌ {label} — current value not found")
        sys.exit(1)
    src = src.replace(old, new, 1)
    changes += 1
    print(f"✔  {label}")

swap("--accent:    #2e3192;",  "--accent:    #2B7A8C;",  "accent ← #2B7A8C (teal)")
swap("--accent-2:  #4448b4;",  "--accent-2:  #34909E;",  "accent-2 ← #34909E")
swap("--accent-pale:#8e93d4;", "--accent-pale:#7FBCC8;", "accent-pale ← #7FBCC8")
swap("--accent-deep:#1e2169;", "--accent-deep:#1D5F6E;", "accent-deep ← #1D5F6E")
swap("--sky:       #2a57a1;",  "--sky:       #4F8FA0;",  "sky ← #4F8FA0")

if changes == 0:
    print("\n(No changes — already on teal.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} change(s))")
    print("   Refresh http://localhost:8100 — back to teal brand palette.")
