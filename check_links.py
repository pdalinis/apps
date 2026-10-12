#!/usr/bin/env python3
"""Check every local link and image in the site resolves to a real file."""
import os
import re

bad = []
pages = 0
for root, _, files in os.walk("."):
    for f in files:
        if not f.endswith(".html"):
            continue
        pages += 1
        path = os.path.join(root, f)
        html = open(path, encoding="utf-8").read()
        for ref in re.findall(r'(?:href|src)="([^"]+)"', html):
            if ref.startswith(("http", "mailto:", "#")):
                continue
            target = os.path.normpath(os.path.join(root, ref))
            if os.path.isdir(target):
                target = os.path.join(target, "index.html")
            if not os.path.exists(target):
                bad.append(f"{path} -> {ref}")
print(f"pages checked: {pages}")
print("broken links:", bad if bad else "none")
raise SystemExit(1 if bad else 0)
