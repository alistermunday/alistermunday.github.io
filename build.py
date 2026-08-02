#!/usr/bin/env python3
"""
build.py — local generator, not a hosting build step. GitHub Pages still just
serves plain files (.nojekyll); this script only keeps two bits of boilerplate
in sync so you never hand-edit them:

  1. The nav bar on every content page (between <!-- NAV:START/END -->).
  2. The card grid on index.html (between <!-- CARDS:START/END -->).

Everything else about a page — colour, layout, fonts, mood — is untouched.
That's deliberate: 300 wildly different pages should look like 300 wildly
different pages.

Usage:
    1. Add a page: write the .html file, and near the top add one line:
       <!-- PAGE-META emoji="X" title="Y" blurb="one line about it" -->
    2. Wrap its nav with the markers (copy from any existing page).
    3. Run:  python build.py
    4. git add -A && git commit -m "..." && git push
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"

NAV_BLOCK = (
    '<!-- NAV:START -->\n'
    '<nav class="site-nav"><a href="index.html">← home</a></nav>\n'
    '<!-- NAV:END -->'
)

PAGE_META_RE = re.compile(
    r'<!--\s*PAGE-META\s+emoji="([^"]*)"\s+title="([^"]*)"\s+blurb="([^"]*)"\s*-->'
)
NAV_RE = re.compile(r'<!-- NAV:START -->.*?<!-- NAV:END -->', re.DOTALL)
CARDS_RE = re.compile(r'<!-- CARDS:START -->.*?<!-- CARDS:END -->', re.DOTALL)


def find_pages():
    pages = []
    for f in sorted(ROOT.glob("*.html")):
        if f.name == "index.html":
            continue
        text = f.read_text(encoding="utf-8")
        m = PAGE_META_RE.search(text)
        if not m:
            print(f"  skip {f.name} — no PAGE-META comment")
            continue
        emoji, title, blurb = m.groups()
        pages.append((f, emoji, title, blurb))
    return pages


def rewrite_nav(pages):
    for f, emoji, title, blurb in pages:
        text = f.read_text(encoding="utf-8")
        if not NAV_RE.search(text):
            print(f"  {f.name}: no NAV markers — leaving nav untouched")
            continue
        new_text = NAV_RE.sub(lambda m: NAV_BLOCK, text)
        if new_text != text:
            f.write_text(new_text, encoding="utf-8")
            print(f"  {f.name}: nav refreshed")


def rewrite_index(pages):
    text = INDEX.read_text(encoding="utf-8")
    if not CARDS_RE.search(text):
        print("  index.html: no CARDS markers found — skipped")
        return
    ordered = sorted(pages, key=lambda p: p[2].lower())
    cards = []
    for f, emoji, title, blurb in ordered:
        cards.append(
            f'    <a class="card" href="{f.name}">\n'
            f'      <div class="emoji">{emoji}</div>\n'
            f'      <h2>{title}</h2>\n'
            f'      <p>{blurb}</p>\n'
            f'    </a>'
        )
    block = "<!-- CARDS:START -->\n" + "\n".join(cards) + "\n<!-- CARDS:END -->"
    new_text = CARDS_RE.sub(lambda m: block, text)
    if new_text != text:
        INDEX.write_text(new_text, encoding="utf-8")
        print(f"  index.html: {len(cards)} card(s) written")
    else:
        print("  index.html: no change")


def main():
    print("Scanning pages...")
    pages = find_pages()
    print(f"Found {len(pages)} page(s) with PAGE-META.")
    print("Rewriting nav blocks...")
    rewrite_nav(pages)
    print("Rewriting index.html card grid...")
    rewrite_index(pages)
    print("Done.")


if __name__ == "__main__":
    main()
