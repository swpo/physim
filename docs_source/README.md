# Maintaining the public documentation

The site is static HTML served from `docs/` by the existing GitHub Pages setup.
No JavaScript framework or package installation is needed to build it.

```sh
python3 scripts/build_docs.py
python3 scripts/check_docs.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory docs
```

Edit `pages/*.html`, `template.html`, and `site.css` here, then rebuild. Page
metadata and the shared navigation are in `scripts/build_docs.py`. Its `MAIN`
sequence drives the header and previous/next links. Technical detail pages are
linked from the relevant main page; `DETAIL_PARENTS` supplies their breadcrumb
and return link. There is no separate reference menu. The HTML
fragments are the sole content source; `docs/*.html` is generated output.

`worlds.json` supplies the world card and downloadable coverage metadata. It is a
documentation catalog, not the proposed release manifest. The immutable genome snapshot in `data/` records its published HF source. Its
copy in `docs/data/` is checked against that snapshot and the catalog hash, so a
clean documentation build does not require an environment source fixture.

`results.json` is a public, bounded snapshot of saved controls and two native
model-run profiles. Refresh deliberately with `python3 scripts/export_docs_evidence.py`;
this command reads local research evidence and never runs a model or simulator.
It includes every attempt from those two profiles, source hashes, and selected
settings, excluding transcripts and local artifact paths. Do not make ordinary
site builds depend on large research caches or run directories.
The page shows one result per model in each profile: a scored attempt supersedes
unscored attempts, and the last recorded scored attempt is used regardless of
score improvement. Costs refer to that displayed attempt. All attempts and costs
remain in the snapshot; this display rule does not change the research ledger.

`examples/` is the source for downloadable code, request JSON, and the public
agent contract. Keep the contract aligned with the worked example and check the
runnable predictor when changing the API. The zero example demonstrates shapes;
it is not a physical accuracy test.

`archive-map.json` records the 29 original pages and their archive destinations.
Historical HTML lives under `docs/archive/` with an archive banner. Existing media
remain in their original locations. The build creates an archive index and small
compatibility pages at old URLs; redirects preserve fragments. The build does not
regenerate the archived studies. The older `physim.results`, `physim.viz`, and
`physim.traces` generators default to the archive and refuse current-docs output
paths. They can also write to an explicit directory outside `docs/`.

Before public release, include the new documentation sources, examples, scripts,
archive pages, and source modules in the reviewed source set. The web build does
not implement the registry, package the native fixtures, or publish any data.
The public releases have passed clean-install and native checks for all three preparations; preserve those numerical identities when updating the site.
