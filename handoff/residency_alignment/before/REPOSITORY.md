# Repository boundaries

The supported release consists of the Physim runtime, optional native Verifiers
adapter, explicit blobkit dependency, examples, Dockerfiles, schemas, and static
documentation. `handoff/repo_cleanup/package_boundary.json` lists source-only
Physim modules excluded from the wheel.

The large research tree remains at its original paths. Historical scripts and
frozen scientific manifests still reference those paths, so renaming or deleting
them would break provenance. The new runtime imports none of them. The migration
exporter is the one explicit bridge from that history into a standalone bundle.

The existing R6 scheduler, scoring module, experiment service, and blobkit CPU
kernels retain their original bytes. Five device definitions were extracted with
identical syntax trees. `handoff/repo_cleanup/original_source/` and its source
manifest preserve the active implementation before cleanup. Research caches,
truths, old rollouts, and their source snapshots are retained unchanged.

## Working on the current runtime

```sh
uv sync --locked
uv run python environments/physim/tools/test_blob_round6.py --gates toy native
uv run python environments/physim/tools/test_blob_round6_eval.py
uv run python environments/physim/tools/test_blob_round6_explore.py
uv run python -m unittest discover -s environments/physim/tools -p test_r6_verifiers.py
uv run python -m unittest discover -s environments/physim/tools -p test_bundles.py
python3 scripts/build_docs.py
python3 scripts/check_docs.py
```

Set `PHYSIM_TEST_BUNDLE` to a verified evaluation bundle for the additional bundle,
cache, truth-freeze, and reference-score integration tests. Those tests explicitly
skip when no bundle is supplied. CI runs the data-independent tests; release
validation also requires the full bundle and Docker checks in `RELEASING.md`.

Only native research compatibility tests and migration scripts read the old tree.
The installed wheel uses `Bundle.make_oracle()` and explicit bundle-driven grading.
Changes to physical semantics, preparation, truth, or grading need new identities
and scientific validation; packaging checks do not recertify a modified law.

## Documentation and historical material

Edit `docs_source/`, then rebuild and check `docs/`. World metadata is updated from
the prepared release manifest by `scripts/prepare_world_release.py --sync-docs`.
Historical benchmarks and articles remain in `docs/archive/`. Old documentation
generators are redirected there, keeping the current site under one builder.

`handoff/` contains historical working notes and audits, not executable runtime
configuration. The cleanup receipts live in `handoff/repo_cleanup/`. Generated
runs and binary release products go in ignored `outputs/` and `dist/` directories.
Do not stage historical logs, process IDs, caches, or bulk output by accident.

## Compatibility limits

Earlier root tasksets are source-checkout only. Their interfaces and scoring differ
from the current prediction task. The old blobkit lock table is also preserved:
two pre-existing GPU/batched-assay files differ from its 0.3.4 record. They are
outside the CPU reference workflow and have not been recertified by this cleanup.
