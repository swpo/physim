# Published world dataset — 2026-09-14

Export, publication, and verification are complete for
[`seanpohorence/physim-worlds`](https://huggingface.co/datasets/seanpohorence/physim-worlds/tree/dcd6abd5eae76a47f326c70518315d2d1e101d86).

- Immutable revision: `dcd6abd5eae76a47f326c70518315d2d1e101d86`.
- 24 world records representing 19 distinct genomes: 21 preserved records and
  three eval-ready preparations (`p4g2_044`, `bf_trail_lab`, `xv_rotor_lab`).
- Complete available registry provenance, including 204 artifacts, four recipes,
  four generation runs, six candidates, three checkpoints, and a generation result.
- 330 published files, 18,433,848 bytes, including the checksummed release inventory.

The destination did not exist before this publication. The existing
`seanpohorence/physim-rollouts` dataset is separate and was not changed. Archived
historical provenance retains its recorded gaps; publication does not reconstruct
missing historical settings. World physics, preparations with apparatus, and
evaluation suites retain their separate identities.

## Verification

The verifier downloaded the full immutable snapshot without credentials and
checked every file against the release inventory. The registry verified, and
every registered world genome loaded successfully.

For each preparation, the normal Physim client fetched both simulation and
evaluation profiles into a fresh cache and successfully reused both offline.
The catalog also worked offline. Each native taskset loaded one task, passed
all seven public interface checks, reproduced its stored reference score, and
ran a fresh 0.02-tu simulation:

| Preparation | Reference score | Checks |
| --- | ---: | --- |
| BF trail lab | 0.46001066377541483 | Passed |
| Original p4g2_044 | 0.8271209896216252 | Passed |
| XV rotor lab | 0.4298978335198635 | Passed |

The release-export, registry-catalog, and bundle tests passed. The initial combined
run reported 20 passed and seven bundle-fixture skips; rerunning the bundle suite
with `PHYSIM_TEST_BUNDLE=dist/residency-reference-bundle` passed all 15 tests and
nine subtests. Ruff passed for the exporter and its new tests. The rebuilt docs
passed checks across 67 HTML pages and 678 local links, with no errors.

No model API calls or GPU rentals were needed. This verifies the published data
using the current development runtime; it does not establish installation from
public code packages or portability to the upstream evaluation runner.

## Recorded state and remaining work

`publication.json` records the upload receipt; `verification.json` records the
anonymous download and native checks. `publish.py` and `verify_published.py`
preserve the procedures used. Local release configuration, catalog metadata,
README files, and generated documentation now point at the published revision.

The exporter now stages the complete registry and every declared eval-ready
preparation, and fails if an evaluation bundle cannot be exported. The original
reference currently needs the supplemental `--bundle` input; BF and XV can be
reconstructed from registry artifacts.

The remaining upstream work concerns portable code distribution and evaluation
setup: publish blobkit or pin an installable immutable source, test the packages
outside the development workspace against this HF revision, provide portable
explicit world selection, and verify the Docker/model workflow used by the
residency runner. Dockerfiles already exist; publishing prebuilt images is
optional. No code packages or images were published in this step.
