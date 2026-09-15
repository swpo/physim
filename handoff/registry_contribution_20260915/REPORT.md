# Registry contribution guide — 2026-09-15

Published [CONTRIBUTING.md](https://huggingface.co/datasets/seanpohorence/physim-worlds/blob/main/CONTRIBUTING.md)
at HF commit `1d8b73624669aea004befd54ec050bb7280f1678`. The editable source is
`registry/CONTRIBUTING.md`; release staging includes it at the dataset root and
records its source hash and published file hash.

The guide covers preserved worlds and eval-ready preparations, provenance and
licensing, the existing Blobkit registry API, community pull requests, updating
an existing PR, and manual maintainer review/publication. Contributors do not
need main-branch write access. No submission CLI or automatic review service was
introduced, and no example PR was opened.

Linked from the HF card and registry README, Blobkit README, local website
contribution page, and environment data documentation. The prepared Prime patch
contains the environment link and current publication metadata. Website changes
were rebuilt locally; this task did not deploy GitHub Pages.

Validation:

- Executed the guide's packaging example against installed public Blobkit 0.3.5;
  verified genome round-trip, artifact bytes, and the registry CLI. Archived code
  was not executed. The upload example was checked with a mocked HF API call.
- All 12 existing registry-catalog and release tests passed; exporter Ruff passed.
- Rebuilt the website: 67 HTML pages, 678 local links checked, zero errors.
- Compared the complete HF stages: only CONTRIBUTING.md, the two READMEs, and
  release.json changed. All scientific payloads and catalog rows are identical.
- Downloaded all four changed files anonymously and verified exact bytes; the
  public snapshot contains 331 files. Runtime configs retain the original data pin.
- Refreshed the 35-file Prime patch and checked that it applies to its recorded
  upstream baseline. The separate portable generator work remains outstanding.

Machine-readable receipts are stored alongside this report.
