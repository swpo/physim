# Fair-scorer reseal of `seanpohorence/physim-worlds`: staged, not published

Date: 2026-11-07. Nothing was uploaded to Hugging Face, nothing was pushed, and no PR
was opened or merged. The user's checkout `/Users/spoho/Documents/prime/test/physim`
was only read. Its branch, working tree and the input workspaces are unchanged. The
only side effects in its `.git` are the worktree entry from `git worktree add` and
the remote-tracking refs updated by one `git fetch origin` at the start.

- Release worktree: `/Users/spoho/physim-release/physim`, local branch
  `release/fair-scorer-20261107` (no upstream), head
  `6199f18c539dd1884174b178c9da829784244ad0`, based on origin/main `bace4e693`.
- Staged dataset: `/Users/spoho/physim-release/dist/hf-worlds-next` (524 files,
  32,749,023 bytes), release id
  `dataset-release:sha256:bc6c58337617647e487b61927ef7981fcbff18cddacc8b52b8a01e1409de34dd`.
- Logs and JSON receipts: `/Users/spoho/physim-release/logs/`. Helper scripts:
  `/Users/spoho/physim-release/tools/`. Publish step: `/Users/spoho/physim-release/publish/`.

## Approach

**Documented build path, not the manifest-only fallback.** The original 2026-09-16
development workspaces were all present on this Mac and fully materialised:
`outputs/eval-preparation-20260916/{bf,xv,p4g2_044}`. Their `registry_receipt.json`
files name exactly the published world records (dece876c, 045a8068, 8a4d3f8b) and
their bundle manifests hash to the published manifests (6796d01d, 5de99491, 571071d4);
every bundle file matched its manifest. No `brctl download` was needed.

Each workspace was copied to `/Users/spoho/physim-release/work/<world>/`
(`preparation/`, `programs.json`, `science/`, `controls/`, `causal/`,
`score_groups.json` for p4). `bundle/` was seeded with the original `truth/*.npz` and
`suite.json` only, and `build_evaluation_bundle.py --resume` was run into it. Resume
reuses every existing truth file (it asserts each stored request), reuses the saved
native control forecasts in `controls/`, asserts the preparation files and the frozen
suite are unchanged, and rescores. No truth was regenerated, no control forecast
was resimulated, and no model was called. The original bundles were kept for
comparison in `/Users/spoho/physim-release/old/<world>/bundle`.

Result for all three worlds:

- World, preparation, apparatus, suite and every truth file are byte-identical; the
  file list is identical; world and preparation ids are unchanged.
- Manifest fields that changed: `bundle_id`, `objects.suite.id`,
  `objects.suite.scoring_source_sha256` (3d8e3fb3 -> 9deb1738). Nothing else.
- `checks.json` changed only in `control_scores` (fair estimator) and, for BF and XV,
  `recipe_sha256` (dfaaa41f -> 6de0912b: the current `build_evaluation_bundle.py`,
  which already built p4 in September). The reference entry
  (`initial_persistence`, 4 members, tolerance 1e-10) is unchanged.
- The new bundle ids equal the earlier manifest-only preview in
  `scorer-fix/reseal/reseal_report.json` (035caa2d, 5119c0ef, f1680d63).

## Code pins (step 1)

Commit `acc1d5a865f49d610ea139f631e9b9c748c26c31` moves `pyproject.toml`
`[tool.uv.sources] physim` rev, `configs/physim/release.toml [code_packages] physim`
and `source_commit`, and `uv.lock` from residency `a124e9bd` to
`c36626cabbb2c35273d6ed2fd97d3a67db4682da`. After `uv sync --locked`,
`import physim.blobround6_eval` resolves to
`.venv/lib/python3.12/site-packages/physim/blobround6_eval.py`, sha256
`9deb1738cba2e3df193970bf08a33dcf264f4c9af4223d3441f0e048dca5bc68` (legacy_v1
`d9277b6057d375b9...`), installed from git commit c36626ca (direct_url.json).
numpy 2.5.2, scipy 1.18.0, blobkit 0.3.5 (workspace).

The lock also switches Verifiers from the git source to the checksummed wheel that
the fix commit pins in `environments/physim/pyproject.toml`. Between a124e9b and
c36626c, `environments/physim` also changes `evaluation.py` (`SCORING_ESTIMATOR =
"fair"`, recorded in grades) and `rewards.py` (negative energies within 1e-12 of zero
reward as 0), besides the scorer, its legacy copy and README text.

## Identities (old -> new)

| | BF `bf_trail_lab_centered_v2` | XV `xv_rotor_lab_centered_v2` | p4 `p4g2_044_centered_v2` |
|---|---|---|---|
| world record | `dece876c2b6772c7…` -> `762d8708856ec43fa6b2d0c3a469d0daeeba66758a7c166bec7aace4ed0c7d6c` | `045a806893b09d4f…` -> `94b463ed0b221d4ed25b4c748d3f79a4f1735d88304c91e28b062c70585d059e` | `8a4d3f8b8842b8f7…` -> `15162df8b0fa30475359f821aa9fd36127c3850c7746f8cee22dccbc7223a199` |
| bundle | `38d159a8052bb0fc…` -> `035caa2d314ee729b4dd407d835d2aa3646eb7b452756e958caddb1d8195207e` | `440472fb5868d80d…` -> `5119c0ef63309b0f73f909871133022520065fb791e68589a659a608369b5820` | `0a1aa9090d76b7ef…` -> `f1680d63444d024c6f196f63d630c970c1f32bf51653b65171eed282966c9266` |
| suite | `4d1a8e77e4f9acad…` -> `33ab8585ae62964108bc7bcaa63852a16055bc1533acb21a4506cf174fefcc2c` | `f9078d51a0644605…` -> `d1ea5c20ea4de973679de2d95fdbb0edc8e3da4dbc8ee8fbc3bff052cd06159b` | `4dae337dc56df0cf…` -> `ceebee09358a3640c3123dc70905c5204602a3749426d2035a0c90f4ff7613a3` |
| manifest sha256 | `6796d01d…` -> `464cfc565ffc418773d40c274fe092ee1a0db1b7dbcf650052a21303ca220aa6` | `5de99491…` -> `f9e556b9e592e71c320a3a7cce2e57e68f65c804889d8c1e647480c22c93a78e` | `571071d4…` -> `036d6c2c8fa942f9fdaaf56c455bbb99db4bbcf1a69cc4429bc01d6ff9f33dcc` |
| recipe | `84a671f4…` -> `9ce85cc1c0cef64350d7c8e5c0ba5de758d4c63d668a47419cff79efe57f77a7` | `741782b0…` -> `b26123c3e57eaa7474f254e85118a9dc1844814ba0b40db1ab084e4ad7642515` | `cc5d6705…` -> `d6301c9ed32456aa624627b1c7339fccb9584dd563948563a1b5fc90fa527d06` |
| generation run | `f3afac87…` -> `7a19786cad0cd3e63a42c6e9dc88ce342c40eb1c74bd8de2218c879f1ee728f7` | `94930dc2…` -> `05ce67b9addac90a2c1f4f90644e60d561f0e4c3224d84ad776921cbd70d7c7d` | `3c05678b…` -> `eee7bf5475d646ecde34ca0ccbed464cd78fad7f7c8437f4aef48f0b48eda23f` |
| world (unchanged) | `aa35f132db7ff9cc…` | `d1b3c19d9ff8337b…` | `9b25d7d82c2cb77d…` |
| preparation (unchanged) | `579e736c902b5344…` | `506fce0fe350b2bf…` | `4f1c99b3884cb327…` |

Each new world record differs from the old one only in `links`, `recipe`, `run` and
five artifacts (`bundle/manifest.json`, `bundle/checks.json`,
`evidence/control_summary.json`, `evidence/native_validation.json`,
`evidence/reference-demo/reference_check.json`); name, genome and source are equal.
Each new recipe differs only by the current `EVALUATION_WORKFLOW.md` (5b355879 ->
b2430e06), the fixed `register_evaluation.py` (5bf64fba -> faad01aa) and an added
`executed/6de0912b…/build_evaluation_bundle.py` naming the build that ran the reseal.
The original executed sources (`dfaaa41f` build, `e78f75ef` eval_preparation) were
restored from registry artifacts and archived again with `--source-archive`.

## control_scores (checks.json), plug-in -> fair

| world | control | old (plug-in) | new (fair) | change |
|---|---|---:|---:|---:|
| BF | independent_native | 0.002211658634838555 | 0.001764251856280229 | -20.2% |
| BF | ignore_actions | 0.20224133870949884 | 0.20174186755631437 | -0.25% |
| BF | remove_feedback | 0.13832800342585688 | 0.13781378903839975 | -0.37% |
| BF | wrong_probe_geometry | 0.4678514404557609 | 0.46743477444057646 | -0.09% |
| BF | initial_persistence (reference) | 0.4970086688520715 | 0.4970086688520715 | 0 |
| XV | independent_native | 0.002067726625516691 | 0.0017289108337148627 | -16.4% |
| XV | ignore_actions | 0.16378194685678457 | 0.16338980108611173 | -0.24% |
| XV | remove_feedback | 0.16192127254268923 | 0.16151673528005642 | -0.25% |
| XV | wrong_probe_geometry | 0.5359862104912364 | 0.5356147715237493 | -0.07% |
| XV | initial_persistence (reference) | 0.4278520374639126 | 0.4278520374639126 | 0 |
| p4 | independent_native | 0.0013570941707892986 | 0.0010268869255814258 | -24.3% |
| p4 | ignore_actions | 0.6430263622089002 | 0.6429680463000562 | -0.01% |
| p4 | remove_feedback | 2.13584655971546 | 2.135806911295265 | -0.002% |
| p4 | wrong_probe_geometry | 0.4496597392797952 | 0.449170816099193 | -0.11% |
| p4 | initial_persistence (reference) | 0.8729905732429272 | 0.8729905732429272 | 0 |

Cross-check (`tools/crosscheck_controls.py`): rescoring the same saved control
forecasts with `estimator="plugin"` reproduces every old value bit for bit, and with
`"fair"` every new value bit for bit. The plug-in bias, E|X-X'|/(2m) with m=4, is
at most about 5e-4 in absolute terms. It matters only for the near-perfect
independent-native control. The persistence reference has zero ensemble spread, so it does not change.

## Validation (step 3)

- `validate_evaluation.py --source work/<world>`: all three ready; native roster
  shapes correct; out-of-roster action rejected without charge; all truths verified;
  `reference_demo` passes all 7 public checks and reproduces checks.json exactly
  (BF 0.4970086688520715, XV 0.4278520374639126, p4 0.8729905732429272; difference 0).
- Profile copies opened with the fixed physim (`logs/open_profiles.json`): every new
  bundle opens in the simulation profile (check_runtime plus a short native
  simulation) and the evaluation profile (check_runtime plus all truths). The old
  bundles open in simulation and are refused in evaluation ("bundle requires a
  different scoring implementation"), as expected.
- `uv run blobkit registry verify registry`: ok; candidate 6, checkpoint 3,
  generation-result 1, generation-run 7, genome 19, recipe 7, world-record 24,
  artifact 379 (the same counts as the September 28 registry).
- Registration round-trips each bundle from registry bytes (`registry_roundtrip: true`).
- Staged release, offline (`tools/verify_staged.py`, modeled on
  `verify_published.py`): all 524 inventory hashes; registry verification equals
  release.json; all 24 genomes load; for each of the three worlds both profile copies
  open with matching references, all truths verify, reference_demo reproduces exactly,
  `load_taskset` yields one task, and a native 0.02-tu experiment runs.
- Staged bundles are byte-identical to the built bundles in `work/`.
- `pytest tests/test_world_release.py tests/test_registry_catalog.py`: 12 passed.
  Full `pytest -n 4 tests`: 158 passed, 1 skipped, 1 failed (see Problems).
- `scripts/build_docs.py` then `scripts/check_docs.py`: 0 errors, 616 local links.

## Registration and the superseded seals (step 4)

`register_evaluation.py add` failed for p4 under the fixed code. It opened the
original fixed-source p4 bundle (0c133190, sealed to the legacy scorer dcd1ab23)
in the evaluation profile only to check its identities and prepared fields. Commit
`a8e059e1d580f1adc272a4bf0008ffd8e6982602` opens it in the simulation profile and
hash-checks every manifest file instead. The provenance check is otherwise
unchanged. The registry was reset and all three were then registered with the
fixed tool, so their recipes archive the same tooling.

The tool only appends to `availability.json`. `tools/move_availability.py` removed
exactly the three superseded ids from `eval_ready`, using the tool's own
serialization (commit `b4c1f4bb7be206352544328ff397571d6bba8f11`, which also has the
new records, catalog and `docs_source/registry.json`).

**Decision taken beyond the literal task:** commit
`162b591b1bc1f5a2ae5c7f1d6745a928affc9d35` removes the three superseded seals,
following HF commit `1dce3735` ("Keep only current evaluation preparations in the
published dataset", 2026-09-28): their world records, recipes and runs, and the 17
artifacts only they referenced. Those artifacts are the old manifests, checks,
control summaries, validation receipts, and the earlier `EVALUATION_WORKFLOW.md` and
`register_evaluation.py`. Every genome and every other record stays, and
`tools/prune_superseded.py` asserts that nothing a remaining record references is
removed. The removed records remain at revision bd77a0da and in physim origin/main.
Without this commit the registry would hold 27 world records with three duplicate
names, the published dataset would again carry seals the fixed scorer refuses, and
`tests/test_world_release.py` (24 worlds, 21 preserved, 3 eval-ready, p4 looked up
by name) would fail. **To keep the superseded records instead,** drop that commit,
re-export the catalog and docs, update the test, and re-stage.

## Staged release (step 5)

`prepare_world_release.py --registry registry --output
/Users/spoho/physim-release/dist/hf-worlds-next`. It was staged first at 162b591b,
then deleted and staged again after the docs commit, so release.json records the
final head.

- `catalog.jsonl` lists exactly the three new bundle paths:
  `bundles/bf_trail_lab_centered_v2/035caa2d…`, `bundles/p4g2_044_centered_v2/f1680d63…`,
  `bundles/xv_rotor_lab_centered_v2/5119c0ef…`. `worlds.jsonl` has 24 rows
  (3 eval-ready, 21 preserved).
- `release.json`: `code_packages.physim =
  git+https://github.com/swpo/residency-environments.git@c36626cabbb2c35273d6ed2fd97d3a67db4682da#subdirectory=environments/physim`,
  `source_commit = c36626ca…`, blobkit 0.3.5 wheel pin unchanged,
  `git_baseline = 6199f18c539dd1884174b178c9da829784244ad0`,
  `working_tree_dirty = false`. The release id recomputes correctly.
- Inventory: 523 rows plus release.json; every file on disk is inventoried with the
  correct size and sha256, and nothing extra is present.
- Private data scan of every added or changed file: no HF, OpenAI, Anthropic, GitHub
  or AWS keys, bearer tokens, private keys, or wallet or seed words. The only local
  paths are the three provenance paths the published release already contains
  (`/Users/spoho/Documents/prime/test/physim/outputs/phenomenology-20260913/{bf_s11001,xv_pair_coupled_s12001}`
  and `.../dist/hf-worlds-20260915-contributions/bundles/p4g2_044/0c133190…`, in
  origin.json, checks.json `source_origin` and run records). No
  `/Users/spoho/physim-release` or scorer-fix paths appear.

### Files changed vs the published revision bd77a0da

Compared with an anonymous snapshot in `/Users/spoho/physim-release/hf-bd77a0da`
(`logs/release-diff.json`): 424 files unchanged, 93 added, 93 removed, 7 changed.

- Added (93): three new `bundles/<name>/<new id>/` folders (21 + 25 + 21 files); 17
  registry artifacts; three each of `registry/world-record`, `registry/recipe` and
  `registry/generation-run`.
- Removed (93): the three old bundle folders (38d159a8, 0a1aa909, 440472fb); the 17
  exclusive old artifacts; the three old world records, recipes and runs.
- Changed (7): `README.md` (bundle table links only), `catalog.jsonl`,
  `worlds.jsonl`, `registry/availability.json`, `registry/index.json`,
  `release.json`, and `registry/README.md`. The registry README change is a paragraph
  already on physim main since September 28 about re-running the historical import;
  it is not part of this reseal.

## Release branch commits (step 6)

```
acc1d5a865f49d610ea139f631e9b9c748c26c31 Pin Physim to the fair-estimator scorer fix
a8e059e1d580f1adc272a4bf0008ffd8e6982602 Let registration check a historical bundle without its scorer
b4c1f4bb7be206352544328ff397571d6bba8f11 Register fair-scorer reseals of the three centered preparations
162b591b1bc1f5a2ae5c7f1d6745a928affc9d35 Keep only the current evaluation seals in the registry
6199f18c539dd1884174b178c9da829784244ad0 Rebuild the documentation registry data from the resealed catalog
```

37 files changed vs origin/main: `pyproject.toml`, `uv.lock`,
`configs/physim/release.toml`, `generators/physim/register_evaluation.py`,
`registry/{availability,index}.json`, `docs_source/registry.json`,
`docs/data/registry.json`, and the registry records and artifacts listed above.

## Commands run

From `/Users/spoho/physim-release/physim` unless noted. Full output is in `logs/`.

```sh
git -C /Users/spoho/Documents/prime/test/physim fetch origin   # remote-tracking refs only
git -C /Users/spoho/Documents/prime/test/physim worktree add -b release/fair-scorer-20261107 /Users/spoho/physim-release/physim origin/main
git branch --unset-upstream
sed -i '' 's/a124e9bdd9bc3dde9866153207658a64e98f82e8/c36626cabbb2c35273d6ed2fd97d3a67db4682da/g' pyproject.toml configs/physim/release.toml
uv lock && uv sync --locked
uv run --locked python -c 'import physim.blobround6_eval ...'   # sha256 == 9deb1738...
git commit   # acc1d5a86
# copy inputs (read-only source: outputs/eval-preparation-20260916/{bf,xv,p4g2_044})
rsync -a <src>/{preparation,programs.json,science,controls,causal,score_groups.json} /Users/spoho/physim-release/work/<w>/
rsync -a <src>/bundle/truth/ work/<w>/bundle/truth/; cp <src>/bundle/suite.json work/<w>/bundle/
rsync -a <src>/bundle/ /Users/spoho/physim-release/old/<w>/bundle/
uv run --locked python generators/physim/build_evaluation_bundle.py --source /Users/spoho/physim-release/work/<w> --output /Users/spoho/physim-release/work/<w>/bundle --resume   # x3
uv run --locked python /Users/spoho/physim-release/tools/compare_bundles.py
uv run --locked python /Users/spoho/physim-release/tools/crosscheck_controls.py
uv run --locked python generators/physim/validate_evaluation.py --source /Users/spoho/physim-release/work/<w>   # x3
uv run --locked python /Users/spoho/physim-release/tools/open_profiles.py
uv run --locked blobkit registry verify registry   # baseline
# executed sources restored from registry artifacts into /Users/spoho/physim-release/executed-sources
uv run --locked python generators/physim/register_evaluation.py add --source work/<w> --name <name> --registry registry --source-archive /Users/spoho/physim-release/executed-sources
#   first pass: bf, xv ok; p4 BundleError -> registry reset (git checkout/clean registry/), tool fixed, commit a8e059e1d
#   second pass: all three, with the fixed tool
uv run --locked python /Users/spoho/physim-release/tools/move_availability.py registry
uv run --locked blobkit registry verify registry
uv run --locked python generators/physim/export_registry_catalog.py --registry registry --sync-docs
git commit   # b4c1f4bb7
uv run --locked python /Users/spoho/physim-release/tools/prune_superseded.py registry           # dry run
uv run --locked python /Users/spoho/physim-release/tools/prune_superseded.py registry --apply
uv run --locked blobkit registry verify registry
uv run --locked python generators/physim/export_registry_catalog.py --registry registry --sync-docs
uv run --locked pytest -q tests/test_world_release.py tests/test_registry_catalog.py
git commit   # 162b591b1
uv run --locked python scripts/build_docs.py && uv run --locked python scripts/check_docs.py
git commit   # 6199f18c5
uv run --locked pytest -q -n 4 tests
uv run --locked python scripts/physim/prepare_world_release.py --registry registry --output /Users/spoho/physim-release/dist/hf-worlds-next
HF_HUB_DISABLE_IMPLICIT_TOKEN=1 uv run --locked python -c 'snapshot_download(..., revision="bd77a0da...", token=False, local_dir="/Users/spoho/physim-release/hf-bd77a0da")'
uv run --locked python /Users/spoho/physim-release/tools/diff_release.py /Users/spoho/physim-release/dist/hf-worlds-next /Users/spoho/physim-release/hf-bd77a0da
uv run --locked python /Users/spoho/physim-release/tools/verify_staged.py /Users/spoho/physim-release/dist/hf-worlds-next /Users/spoho/physim-release/verify-staged
HF_HUB_DISABLE_IMPLICIT_TOKEN=1 uv run --locked python /Users/spoho/physim-release/publish/publish_reseal.py   # anonymous dry run
```

## Publish step (not done)

`/Users/spoho/physim-release/publish/publish_reseal.py` is modeled on
`handoff/hf_release_20260914/publish.py` and
`handoff/registry_contribution_20260915/publish_hf_guide.py`. It re-verifies the
staged inventory, release id, exporter hashes, the c36626ca pin and the clean tree.
It requires the remote head to still be `bd77a0da…` and the exact add, change and
delete set in `publish/hf_changes.json` (93 added, 7 changed, 93 removed). Remote
"unchanged" files must match by LFS sha256 or git blob id. With `--publish` it also
requires the `seanpohorence` login, then makes one `create_commit` with
`parent_commit=bd77a0da…` (adds and deletes) and writes `publish/publication.json`.
The anonymous dry run passed against the live remote.

```sh
cd /Users/spoho/physim-release/physim
uv run --locked python /Users/spoho/physim-release/publish/publish_reseal.py --publish
```

Afterwards, verify the new revision anonymously the way
`handoff/hf_release_20260914/verify_published.py` does, pointing it at the new
`publication.json` and a fresh `/tmp` work directory.

### Follow-up edits after the new revision NEW_REV exists

Residency, on the fix branch before it merges, because the fixed scorer refuses
every bundle at bd77a0da:

- `environments/physim/physim/taskset.py` `DEFAULT_CATALOG.revision` -> NEW_REV.
- `configs/physim/{bf_trail_lab,xv_rotor_lab,p4g2_044}.toml`: set `revision` to NEW_REV
  and `path` to the new bundle paths (035caa2d…, 5119c0ef…, f1680d63…).
- `configs/physim/release.toml`: `dataset_revision`, `release_id`
  (`dataset-release:sha256:bc6c5833…`), `published_date`. Per its own comment, the
  `[code_packages]` pins move to the merge SHA.
- `configs/physim/README.md`, `environments/physim/DATA_SOURCES.md` and
  `environments/physim/README.md` still cite bd77a0da.

Physim, on this branch or a follow-up:

- `configs/physim/release.toml`: `dataset_revision = NEW_REV`, `release_id =
  "dataset-release:sha256:bc6c58337617647e487b61927ef7981fcbff18cddacc8b52b8a01e1409de34dd"`,
  `published_date`. After the residency merge, move `pyproject.toml`, `uv.lock` and
  `[code_packages]` to the merged commit, and first confirm `blobround6_eval.py` still
  hashes 9deb1738.
- `RELEASING.md`: a section for this release (fair estimator, bundle and record ids,
  the 1dce3735-style supersession, receipts). Update its "registry matches the
  September 28 release" paragraph and the bd77a0da links.
- Docs that cite the current revision or ids: `README.md`, `REPRODUCING.md`,
  `generators/physim/EVALUATION_WORKFLOW.md`, `docs_source/APPARATUS_UPDATE.md`.
  `environments/physim/README.md` and `PRIME_AGENT.md` still link residency a124e9bd.
  Historical results computed on the old bundles (`BF_CASE_STUDY.md`,
  `docs_source/data/{bf-case-study*,reward-calibration}.json`,
  `docs/assets/worlds/*-fields.json`, handoff STATE notes) should keep the old ids as
  provenance, with a note that those scores used the plug-in estimator.
- Add receipts under `handoff/` (a copy of this report, `publish/`, `logs/`).

### Does the repin have to wait for the PR merge?

Not to stage or publish the dataset. Bundles pin the scorer file hash (9deb1738),
not a commit, and c36626ca is reachable on swpo/residency-environments
(`fix/physim-fair-energy`). The release records c36626ca as the sealing code, which
stays correct provenance.

The final physim pin should wait for the merge. The fix branch still defaults to
bd77a0da, so it needs one more commit with NEW_REV before merging. After a squash or
rebase merge, or a deleted branch, c36626ca may stop being the canonical or
reachable commit.

Order: publish HF, update the residency PR to NEW_REV, merge, then repin physim to
the merged commit and record NEW_REV in physim. Keep this branch unmerged, or merge
it knowing it temporarily pins a fork-branch commit.

## Problems and open points

- `tests/test_campaign_transport.py::test_full_harness_error_is_saved_before_native_truncation`
  fails after the repin. It asserts `installation.vcs_info.commit_id`, but Verifiers
  now comes from the fix commit's wheel URL, and `direct_url.json` holds `url` plus an
  empty `archive_info`. This is unrelated to the dataset and was left unchanged. It
  needs either a test that accepts a pinned wheel or diagnostics that record the
  wheel hash.
- Replaying the p4 recipe (`prepare_centered_reference.py --source <original p4 bundle>`)
  would open the legacy 0c133190 bundle in the evaluation profile, which the fixed code
  refuses. The legacy bundle is out of scope, so this is recorded, not fixed.
- The causal evidence (`causal/result.json`, `causal/readings.npz`) and the science
  receipts are carried over unchanged. They come from the September runs and were not
  rescored.
- `~/.cache/physim/bundles` still holds copies of the old bundles. The fixed code
  refuses their evaluation profile; new fetches use the new paths.
