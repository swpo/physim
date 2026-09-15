# Web refresh — 10 September 2026

Implemented the web portion of the documentation audit in the working tree.
Existing GitHub Pages structure is preserved. Nothing has been published.

- Twelve current pages cover overview, worlds, experiment/predict, evaluation,
  the runnable interface example, results, field dynamics, generation, numerics,
  API, registry design, and contributions.
- Shared navigation, semantic HTML, responsive stylesheet, and a standard-library
  generator replace separately maintained page chrome.
- All 29 original pages are preserved under `docs/archive/`. Original visible
  text was compared with Git HEAD and retained exactly (apart from a separate
  archive banner). Media remain in their original locations. Compatibility
  redirects preserve deep-link fragments.
- README entry points now describe the current program and its packaging limits.
- The results snapshot contains all 15 attempts in two native resource profiles,
  including retries, invalid submissions, and missing artifacts. Thirteen
  hand-written controls have separate sampling conditions. No source traces,
  prompts, private truth arrays, or local artifact paths were copied.
- Historical results/world/trace generators default to `docs/archive/` and reject
  current-docs output paths. Explicit external output directories are supported.

Validation: 676 local links, 67 total HTML pages, 12 current-page semantic checks,
three source-evidence hashes, catalog/genome hashes, contract/example consistency,
deterministic rebuild, and preservation of all archived article text. The example
was accepted by production request/sample validators; empty outputs were checked.
All 30 evaluator and 10 exploration tests passed. Generator refusal checks and
report generation into a temporary directory passed. Eighteen localhost HEAD
requests returned 200. Browser checks after restoring the preview confirmed all
six main navigation links and actual video playback (22.4 seconds, decoded
frames, readyState 4, no media error). The localhost preview is left running
for review; do not stop it at turn completion while the user is reviewing it.

Maintain content in `docs_source/`; rebuild with `python3 scripts/build_docs.py`
and check with `python3 scripts/check_docs.py`. See `docs_source/README.md`.

Next: implement the bundle schema/export/local resolver, then make the native
example reproducible without research-cache paths. The web registry page clearly
labels that infrastructure as planned. Source-set review and publication remain
separate steps; existing unrelated working-tree changes were preserved.

Follow-up: removed the homepage coverage callout. Preparation, program count,
horizon, and sampling details now sit in the single world card. Simplified the
worlds registry paragraph to refer to that listing. The original broken links
and video were caused by stopping the local server after the first handoff.

Navigation follow-up: removed the reference sidebar. The six main pages retain
their header order and now share generated previous/next links in that sequence.
World details are linked from Worlds; the API is linked from Experiment & predict
and Try it. Detail pages show their parent and a return link. Contribute moved
to the footer. The single-column layout was checked in the browser, along with
Worlds → field dynamics → Worlds → Experiment & predict → API navigation.
The link checker enforces one main navigation and reachable detail pages.
