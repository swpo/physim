Physim portability and Hugging Face release verification — 15 September 2026

**Accepted ownership plan:** Blobkit source and releases remain in the personal repository. The intended Prime contribution adds portable evaluation-specific generation/preparation workflows to the verified 35-file environment subset. Those workflows and their clean-checkout verification remain outstanding. See [the accepted plan](../architecture/PLAN.md).

**The code and data are published, and the environment subset of the residency contribution is prepared.** Use [Physim 0.12.2](https://github.com/swpo/physim/releases/tag/physim-v0.12.2) and [Blobkit 0.3.5](https://github.com/swpo/physim/releases/tag/blobkit-v0.3.5). Both have public wheels and source distributions. Physim declares the exact Blobkit wheel URL and SHA-256, so it installs without this research checkout. The PyPI project named `physim` belongs to unrelated software; the release includes explicit installation requirements and a checksummed setup archive.

The release's Python package files match their isolated source commits: Blobkit `bfdd4319fbbbf1fe92e20afad3c5e9118c8d862e`, Physim `eb6647cb429226dc43b27db6950329ed849b92d9`. The development checkout remains unstaged. A stale sentence in the packaged README about missing predictors is corrected in the current source README and explicitly clarified in the release notes; the tested implementation gives zero reward. Scientific simulator, scoring, world, preparation and suite identities are unchanged.

**Public installation and physical checks passed.** A fresh Linux runner downloaded only public release assets and anonymous HF data, installed the wheels into a new environment outside a checkout, and verified all three preparations. It checked serialized task configuration, evaluation and simulation bundle profiles, offline reuse, the native loader, reference predictions and a fresh 0.02-tu experiment in every world. These short experiments establish portability; they do not repeat the earlier phenomenology studies. [Linux CI](https://github.com/swpo/physim/actions/runs/34970845043) completed successfully.

| Preparation | Public ports | Persistence control: joint energy | Native experiment |
| --- | ---: | ---: | --- |
| p4g2_044 | 12 | 0.8271209896216252 | Pass |
| bf_trail_lab | 4 | 0.4600106637754149 | Pass |
| xv_rotor_lab | 6 | 0.4298978335198635 | Pass |

All reference scores agree within the specified `1e-10` tolerance. On macOS, a fresh public 0.12.1 installation passed the same three-world checks; that environment was upgraded from the public 0.12.2 wheel for the final live smoke. Its modules load from the new environment's site-packages, with no editable installs or research-directory imports. Evidence: [Linux installation](public_install_linux_0122.json), [macOS initial installation](public_install.json), [macOS upgrade](public_0122_install.log).

**The live smoke found and resolved one deployment issue.** Physim 0.12.1's first rollout completed, but its second failed before any model call: stock Verifiers' bash harness timed out while installing dependencies in a fresh container. The error remained a native `HarnessError`. Following Prime's existing `pmpp-hard` image pattern, the 0.12.2 agent Dockerfile pre-caches the harness dependencies and disables runtime package-index access. The host still uses the stock Verifiers 0.3.1 harness and Docker runtime.

The exact stock harness preparation now passes with Docker networking disabled: 2.20 seconds on macOS and 3.13 seconds on Linux. Full rollout setup includes the task, model and tool connections and therefore takes longer. Both Docker images build. A separate Docker grading check accepted the example executable predictor and completed its grade with joint energy `1.0845872705112614`. Evidence: [macOS offline startup](harness_offline.json), [Linux offline startup](harness_offline_linux_0122.json), [Docker grade](docker_grade.json).

**Two live rollouts of the published 0.12.2 environment completed successfully.** Model: `deepseek/deepseek-v4-flash`; preparation: BF; two independent rollouts, four turns each. This was an integration smoke, not a capability evaluation.

| Rollout | Model calls | Full setup | Stop condition | Reward | Infrastructure errors |
| --- | ---: | ---: | --- | ---: | --- |
| 69d1c942 | 4 | 21.89 s | max_turns | 0 | None |
| 0a08ea60 | 4 | 19.31 s | max_turns | 0 | None |

Both ended without a predictor. As requested, each records `score_reason=no_predictor` and earns zero reward; neither becomes a task error. Invalid predictors also earn zero, while infrastructure failures remain Verifiers errors. The final two-rollout API cost was $0.0020; including the earlier attempt, reported model usage was $0.0044. All four rollout containers were cleaned up. No GPUs were rented. Original and corrected traces are retained in [the smoke receipt](model_smoke_results.json) and the adjacent trace files.

The full configs retain generous ceilings: 1,024 turns, 1,048,576 output tokens, 24 hours, 1,000 experiments and 50,000 integrated tu. They impose no reward penalty for inefficient exploration. Each config selects exactly one immutable world preparation. Omitting a world is an error; the environment does not silently choose a world or expand to all eval-ready entries.

**Hugging Face's bot notice is expected.** HF generates a derived Parquet branch to power its viewer; it does not require replacing our simulation arrays with Parquet. The dataset follows HF's [explicit configuration guidance](https://huggingface.co/docs/hub/datasets-manual-configuration) with separate `worlds` and `evaluations` catalogs. All 24 world rows and three evaluation rows in the converted Parquet tables exactly match their source JSONL, including nulls and nested references. NPZ arrays and content-addressed registry records remain the scientific payloads. [HF's conversion documentation](https://huggingface.co/docs/dataset-viewer/parquet) describes this arrangement.

The card now documents catalog fields, the difference between preserved and eval-ready worlds, separate world/apparatus/suite identities, immutable loading examples, licenses, provenance gaps, and the fact that `train` is a viewer partition for disclosed development material. Available generation recipes and evidence remain with the registry. There are 24 world records, 19 genomes, 21 preserved worlds, three eval-ready preparations, and 204 provenance artifacts.

The latest [HF publication](https://huggingface.co/datasets/seanpohorence/physim-worlds/tree/0813ee4d0a4e97a12bbf598d5d43a45eddf5492f) is `0813ee4d0a4e97a12bbf598d5d43a45eddf5492f`. Its changed README and release manifest were downloaded anonymously and verified byte for byte. Across the two documentation updates, only the dataset card, registry README and release manifest changed. Runtime configs deliberately retain scientific revision `dcd6abd5eae76a47f326c70518315d2d1e101d86`; every world, recipe and catalog row is unchanged. See [Parquet comparison](hf_catalog_audit.json) and [latest publication verification](hf_verification_0122.json).

After the latest metadata commit, HF queued regeneration of both catalog views. Its API reports two pending conversions and no failed conversions; the previous converted catalogs already passed the exact comparison above. This is a service-side refresh. The pinned data downloads and offline environment use are verified and do not depend on that refresh.

**The environment subset is prepared for review.** [The patch](residency.patch) adds 35 files under `environments/physim`, `configs/physim` and supporting `scripts/physim`. It depends on the published Blobkit wheel and published data. It includes the explicit world configs, both Docker recipes, offline harness check, installation check and small examples. The historical R5 implementation brief is excluded. It applies cleanly to Prime's snapshot `01d9f5f80572b7ec82575b10d45a800ed844e496`; their two generic package checks and Ruff checks pass. No upstream PR or maintainer message has been sent.

Validation also includes 67 Blobkit CPU tests, 48 Physim/bundle/roster tests plus 13 subtests, 20 native tests plus six subtests after the final image change, 12 export/catalog tests, and a documentation check of 67 pages and 678 local links with no errors. Accelerator-specific tests were not rerun for these packaging and host-wiring changes.

The remaining external decision is which explicit config and model panel Prime's evaluation runner should use. Their public maintainer notes state that repository CI does not run model evaluations; PR #20 links a separate evaluation workflow whose implementation is not publicly accessible. The patch supplies runnable configs and smoke instructions, but our checks do not certify that private runner. The suggested PR description is [here](residency-pr-description.md).
