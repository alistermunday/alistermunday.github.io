# alistermunday.github.io

Source for [alistermunday.com](https://alistermunday.com).

## Shape

Substrate-mirror — four bands, in order: centre (axioms) → frameworks → live edges → logs. Plus tools and provenance. See `index.md`.

## Hosting

GitHub Pages, Jekyll (minima theme), custom domain via `CNAME`.

## Content homes

Some sections live as sub-paths in this repo (`/frameworks/`, `/falsifications/uap/`, `/tools/necessary-constraints/`). Others link out to standalone repos (`coherence-framework`, `structural-predictions`, `posts`, `the-constraint-framework`, `substrate`). The choice per piece is pragmatic, not architectural.

## Adding a piece

1. Drop the markdown / static HTML into the relevant sub-path.
2. Update `index.md` to add a one-line entry under the right band.
3. Commit, push. GitHub Pages rebuilds.

If a piece already has its own repo and a working public URL, just link from `index.md`; don't migrate.
