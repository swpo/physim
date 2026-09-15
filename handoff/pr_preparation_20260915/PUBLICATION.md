# Publication handoff

The normal Git pushes succeeded after connectivity recovered. The code and
documentation are published, and the Prime contribution is open as
[draft PR #22](https://github.com/PrimeIntellect-ai/residency-environments/pull/22).
Both upstream checks and the personal repository’s full CI passed. Publication
used the original tested commits; no file-by-file API upload was needed.

## Prime contribution

- Checkout: `/tmp/physim-pr-20260915`
- Commit: `a90b133eb96882a2260002a3f24d754c32bfe75b`
- Tree: `5a633156e1173b206d9bcaf6dbd42eeeccd61071`
- Base: `01d9f5f80572b7ec82575b10d45a800ed844e496`
- Fork branch: `swpo/residency-environments:codex/physim`
- Target: `PrimeIntellect-ai/residency-environments:main`
- Draft title: **Add Physim experimental prediction environment**
- [Prepared description](PR_DESCRIPTION.md)

## Personal repository

- Checkout: `/tmp/physim-personal-publication-20260915`
- Commit: `652c2fd68300014c905ccc034a3cbba8a756ff6e`
- Tree: `0e3f8f67781806ea9221e8588e3a134b1cced1b4`
- Prepared branch: `codex/physim-publication-20260915`
- Target: `swpo/physim:main`, using a fast-forward update
- Pages source: `main:/docs`
- Site: <https://swpo.github.io/physim/>

The original research checkout and its untracked run outputs are preserved.
Do not replace its working tree with a clean checkout or run a hard reset.

## Recovery and verification

Verified Git bundles and the complete Prime patch are saved locally under
`dist/publication-20260915/`. Their hashes and prerequisites are recorded in
[publication_status.json](publication_status.json). The Prime bundle requires
the upstream base above; the personal bundle requires the public commit
`87325d9fbf37225c1ef5f44c3138de7fca81c704`.

The remote contribution and code commits match the tested trees above. A
documentation-only follow-up adds publication records and PR crosslinks to the
personal repository. The PR remains a draft for review; the website is published
from `main:/docs`. [GitHub Actions](https://github.com/swpo/physim/actions) records
CI and Pages deployments. The original bundles preserve the tested code commits.

See [REPORT.md](REPORT.md) for completed scientific, integration, and
documentation checks. No additional model runs or GPU rentals are needed for
the publication step.
