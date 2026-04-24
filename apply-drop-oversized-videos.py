#!/usr/bin/env python3
"""apply-drop-oversized-videos.py — Remove 3 oversized video refs from MEDIA.

GitHub rejects pushes with files over 100MB. Three retractable videos are
over that limit and cause push failures:
  - 40.mp4 (133MB)
  - 43.mp4 (177MB)
  - סקיילייט נוסע 2.mp4 (174MB)

Removes them from MEDIA.retractable. Leaves 7 video tiles on retractable
page — still a healthy strip. User can add back compressed versions later.

The files themselves stay on disk; the .gitignore (see separate commands)
will keep them out of git history going forward.
"""
import sys, pathlib

HTML = pathlib.Path(__file__).parent / "index.html"
src = HTML.read_text(encoding="utf-8")
changes = 0

def drop(line_substring, label):
    global src, changes
    # Find the full line containing the substring
    for line in src.split("\n"):
        if line_substring in line and "type:'vid'" in line:
            # Remove the whole line including trailing newline
            old = line + "\n"
            if old in src:
                src = src.replace(old, "", 1)
                changes += 1
                print(f"✔  Dropped: {label}")
                return
    print(f"✔  {label} — not found (already removed?)")

drop("src:'01 — סקיילייט נוסע/40.mp4'", "40.mp4 (133MB)")
drop("src:'01 — סקיילייט נוסע/43.mp4'", "43.mp4 (177MB)")
drop("src:'01 — סקיילייט נוסע/סקיילייט נוסע 2.mp4'", "סקיילייט נוסע 2.mp4 (174MB)")

if changes == 0:
    print("\n(No changes.)")
else:
    HTML.write_text(src, encoding="utf-8")
    print(f"\n✅ Wrote {HTML} ({changes} removed)")
