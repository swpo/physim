# Preparing the first reference release

Code and documentation belong in GitHub; world payloads belong in a separate HF
dataset repository. The local candidate has not been uploaded. Choose the code
license, data license, and HF namespace before public distribution; blobkit's
existing metadata still says Proprietary.

## Rebuild the local candidate

From the development workspace, with the preserved historical inputs available:

```sh
uv run python scripts/export_reference_bundle.py --output dist/reference-bundle
uv run python scripts/check_reference_parity.py --bundle dist/reference-bundle \
  --output handoff/repo_cleanup/native_parity.json
PHYSIM_TEST_BUNDLE=dist/reference-bundle uv run python -m unittest discover \
  -s environments/physim/tools -p test_bundles.py
uv run python scripts/check_clean_install.py --bundle dist/reference-bundle \
  --workdir /tmp/physim-clean-release --report handoff/repo_cleanup/clean_install.json
uv run python scripts/prepare_world_release.py --bundle dist/reference-bundle \
  --output dist/hf-worlds-candidate --sync-docs
python3 scripts/build_docs.py
python3 scripts/check_docs.py
```

Output directories must be fresh. The exporter never regenerates truths or makes
model calls. It extracts one field from the historical cache, serializes apparatus,
and copies only the 15 verified native truth files. The staging command produces
a data-only HF directory, dataset card, catalog, and exact file inventory.

Build both wheels and source distributions with `uv build --package blobkit` and
`uv build --package physim`. Inspect their payloads; the Physim wheel excludes old
tasksets, research files, arrays, and model outputs. Keep wheels as code release
assets, separate from the world dataset.

Build the Docker images using `docker/predictor.Dockerfile` and
`docker/agent.Dockerfile`. Validate `examples/predictor`, then grade it on the
reference bundle. The zero predictor should pass the interface gate while scoring
poorly. Native model runs are not needed for release validation.

## Publication decisions and final checks

1. Apply the chosen code and data licenses consistently to package metadata,
   root license files, bundle metadata, and the HF dataset card.
2. Review and commit the intended source set, excluding caches and historical
   logs. Record the resulting code commit and wheel hashes in the release receipt.
3. Publish the staged data-only directory to the chosen **worlds** dataset. Keep
   the existing rollout dataset separate. Retain the exact returned commit.
4. Fetch that full commit through `physim fetch`, repeat it with `--offline`, and
   run the clean reference check on the downloaded bundle.
5. Update the catalog/docs to published status, the exact repository commit, and
   working download commands. Rebuild/check the static site and publish the code
   release and GitHub Pages changes.

Example commands after a dataset revision exists:

```sh
physim catalog --repo OWNER/physim-worlds --revision FULL_40_CHARACTER_COMMIT
physim fetch --repo OWNER/physim-worlds --revision FULL_40_CHARACTER_COMMIT \
  --path bundles/p4g2_044/BUNDLE_SHA256 --profile evaluation
physim fetch --repo OWNER/physim-worlds --revision FULL_40_CHARACTER_COMMIT \
  --path bundles/p4g2_044/BUNDLE_SHA256 --profile evaluation --offline
```

These placeholders are deliberate: there is no published revision yet.
The reference suite is disclosed development material. Future held-out suites
need distinct identities and an explicit exposure/access policy.
