#!/usr/bin/env python3
"""python3 build_site.py builds _site/ for GitHub Pages; the deploy workflow
runs it automatically, so you normally don't run it yourself except to test.

_site/ contains index.html (from hanzi-drill.html), the word and stroke data,
vendor/, icons/, manifest.webmanifest, LICENSE and a generated sw.js that
precaches all of it under a cache name derived from a content hash.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_site"


def fail(msg):
    sys.exit(f"build_site.py: error: {msg}")


def main():
    for name in ("manifest.webmanifest", "icons"):
        if not (ROOT / name).exists():
            fail(f"{name} is missing; it is required in the repo root")
    if not (ROOT / "icons").is_dir() or not any(p.is_file() for p in (ROOT / "icons").rglob("*")):
        fail("icons/ must be a directory containing files")

    # (source path, destination relative path)
    items = [(ROOT / "hanzi-drill.html", "index.html")]
    names = [f"hsk{i}.js" for i in range(1, 8)] + [f"strokes{i}.js" for i in range(1, 8)]
    names += ["LICENSE", "manifest.webmanifest"]
    for n in names:
        items.append((ROOT / n, n))
    for d in ("vendor", "icons"):
        for p in sorted((ROOT / d).rglob("*")):
            if p.is_file():
                items.append((p, p.relative_to(ROOT).as_posix()))
    for src, _ in items:
        if not src.is_file():
            fail(f"missing source file: {src.relative_to(ROOT)}")

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    items.sort(key=lambda it: it[1])
    total = 0
    h = hashlib.sha256()
    for src, rel in items:
        dst = OUT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        data = dst.read_bytes()
        total += len(data)
        h.update(rel.encode("utf-8") + b"\0")
        h.update(data + b"\0")

    template = (ROOT / "sw.js").read_bytes()
    h.update(template)
    version = h.hexdigest()[:12]

    text = template.decode("utf-8")
    for ph in ("__VERSION__", "__FILES__"):
        if text.count(ph) != 1:
            fail(f"placeholder {ph} must appear exactly once in sw.js (found {text.count(ph)})")
    files = ["./"] + [rel for _, rel in items]  # includes index.html, sorted
    text = text.replace("__VERSION__", version).replace("__FILES__", json.dumps(files, indent=2))
    (OUT / "sw.js").write_text(text, encoding="utf-8")
    total += len(text.encode("utf-8"))

    print(f"files: {len(items) + 1} (incl. sw.js)")
    print(f"total size: {total / 1e6:.2f} MB")
    print(f"VERSION: {version}")


if __name__ == "__main__":
    main()
