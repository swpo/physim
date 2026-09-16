# Campaign continuation state

Checkpoint: September 16, 2026. Main implementation checkpoint is local commit
`6248405`; it has not been pushed. Subsequent changes retain per-snapshot and
per-attempt provenance manifests. No new package or HF dataset release has been
published in this campaign.

## Active paid rollout

- Model: `z-ai/glm-5.3-flash`, BF, repetition 1, attempt 1.
- Process is already running. Do not launch a duplicate or another paid rollout
  while the campaign lock is held.
- Root: `outputs/evaluation-campaign-20260916`.
- Attempt: `attempts/z-ai--glm-5.3-flash-bf-r1-attempt1`.
- Trace/container: `427e18f284854bd5843d3a3dd9a67a1b`.
- Runner log: `glm-bf.log`; native log: attempt's `eval.log`.
- The current runner admits only this one rollout and exits afterward.
- Tool process session: `69573` (if still available in the current session).
- Live costs and counters are in the trace's `spend_state.json` and
  `laboratory_state.json`. `ledger.json` is updated at rollout boundaries;
  the `ledger()` helper recomputes it from live receipts.
- Last observed checkpoint was 41 model calls, 18 experiments, about $0.125
  reported inference cost. This is a historical progress observation, not a
  final cost. No predictor had been submitted yet.

No other paid run has started. No GPU has been rented. All preparation and
baseline work used local CPU. Do not interrupt a rollout at the $50 target;
review spending after it finishes, and admit no next rollout if total spend
has reached $50. The task's native dollar hook reserves the next call against
the $150 campaign ceiling.

## Follow-up authorization

An attempted ten-minute heartbeat was rejected by automatic approval review:
the campaign is authorized, but unattended recurring paid execution needs
explicit approval for that mechanism. A text question is pending with choices
to approve background follow-ups or keep work in the active session. **No
automation was created.** Do not recreate it or arrange an equivalent unattended
workaround without the user's approval. Active-session work and the existing
authorized rollout can continue.

The proposed initial open-model batch is one rollout per world for GLM 5.3
Flash, Qwen 3.5 35B A3B, DeepSeek V4.1 Flash, and Kimi K2.6. Model IDs/prices
are in PLAN.md and `catalog.json`. Review completed traces for limits/provider
faults, then run the next selected world with `--max-new-runs 1`. Pause for
review before closed models, expensive tiers, or repetitions.

## Completed preparation work

All new bundles live at `outputs/eval-preparation-20260916/WORLD/bundle` and
have matching `native_validation.json`, references, control summaries, and
registry round-trip receipts:

| World | Cases | Bundle SHA-256 suffix |
| --- | ---: | --- |
| BF | 15 | `38d159a8052bb0fc24d0d8feefe3985ac645fb19954f2c84aa54954a948b561e` |
| XV | 15 | `440472fb5868d80d7a94cdb74f615ea1525a71b3387147ab394059f815b37bf6` |
| p4g2_044 | 19 | `0a1aa9090d76b7ef30e4a1ada082309324ccb45321d34bf3af49cee4663d7775` |

The new records/recipes are in the separate `registry-staging` under the
campaign root, not yet merged into the main registry or published to HF.
Names: `bf_trail_lab_centered_v2`, `xv_rotor_lab_centered_v2`, and
`p4g2_044_centered_v2`. All three export/reload successfully. Preserve historical
fixed-source bundles and source archives. The p4 baseline recovery and science
formatting provenance are documented in SCIENCE.md.

The BF Worlds/Evaluation figures and text now use the fresh centered-source
evidence. Desktop/mobile figures were inspected and documentation link checks
pass. `SCIENCE.md` summarizes the measured effects and all-world baseline.

## Verification and reproduction

- `/tmp/physim-residency-dev/bin/python` is the development Python; its Verifiers
  client uses native Prime authentication. Do not put credentials in configs.
- Full offline scripted-model/Docker smoke on the new BF bundle passed:
  `offline-smoke-centered/report.json`.
- Clean wheel install outside checkout passed with the public Blobkit dependency:
  `clean-install.json`; isolated venv `/tmp/physim-centered-clean-install-02`.
- `clean-install-all-worlds.json` records the same installed wheel's checks
  across all three worlds when that check completes.
- Unit/integration/build checks and the new control/aggregation tests pass.
- Source ZIPs are retained under the campaign root. First BF source ID:
  `5c28d6845b5d2a06dc3b94170de675e3900d2351b004abed1197456397bb6d2d`.
  The first manifest was reconstructed from that retained ZIP; its metadata
  labels the dependency/image inventory as observed again after launch.
- Before the next rollout run `scripts/physim/freeze_campaign.py` to capture
  the latest source state. The runner rejects edits after a source snapshot.
  Runtime code and numeric implementations have not changed during BF's run;
  later edits repaired preparation diagnostics and preserved metadata.

## Remaining delivery

Inspect each completed trace before expanding. Natural completed attempts with
no valid predictor receive zero; do not retry or omit them. Provider faults and
binding operational limits require classification; retain every incurred cost.
Aggregate with `scripts/campaign_results.py`. A model gets no headline aggregate
until all three worlds are represented; average reward within world, then
equally across worlds. Initial persistence's equal-world reward is
`0.6340856666038858`. Other native controls use four forecast members and are
privileged diagnostics; persistence is member-count invariant.

After the initial batch, create the requested Pareto figure and per-world
tables and replace the historical Results page. Decide further model coverage
or repetitions with the user. Keep release work attached: merge/publish the
new registry records/bundles, update pinned configs and public environment
release, verify installed packages, synchronize the Prime draft PR, and push
the reviewed documentation and other personal-repository changes.
