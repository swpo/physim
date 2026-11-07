# PhySim v1 scorer: fair (unbiased) ensemble estimator — status

Mac session ("PhySim macbook session"), 7 Nov 2026. Task from the cloud coordinator: fix the self-pair bias in
`blobround6_eval.py` (energy score and marginal CRPS), test it, re-seal, and measure the impact on saved results.

## Branches (swpo/residency-environments; nothing opened or updated upstream)

| branch | head | base | contents |
|---|---|---|---|
| `fix/physim-fair-energy-labworlds` (alias `physim-fair-energy-labworlds`) | `19f30c1` | `labworlds-adapter` 23f07a3 | 4529505 ruff format of labbundle.py/labworld.py (formatting only, ASTs identical) → 177a1f7 fair estimator → ef1f58c LABWORLDS.md note → 19f30c1 checks moved to a script, reward rounding tolerance |
| `fix/physim-fair-energy` (alias `physim-fair-energy`) | `c36626c` | upstream `main` 5149b69 | 4713d14 fair estimator → c36626c the same follow-up |

- The lab kit you re-sealed (physim a4410720a) pins ef1f58c's identity. 19f30c1 changes only `rewards.py` and moves the
  check file, neither of which is in any bundle identity, so the kit still opens. Identity at 19f30c1: blobround6
  d1b4a8b4, labworld 501fffd3, devices 43229b50, blobround6_eval 9deb1738, labbundle 060e39ae.
- Scorer sha256: `blobround6_eval.py` 3d8e3fb3 → 9deb1738; `legacy_v1/blobround6_eval.py` dcd1ab23 → d9277b60.
- The `fix/` names follow the repo's AGENTS.md prefix rule; the unprefixed names point at the same commits and can be deleted later.
- `labworlds-adapter` (PR #40 head) is still 23f07a3: pushing the formatting commit 4529505 there updates the upstream PR
  and is waiting for the user's OK. If approved it is a fast-forward and turns PR #40's Style check green.

## The change

- `estimator="fair"` (default) or `"plugin"` on `score_case`, `evaluate_trusted_predictor` and the CLI (`--estimator`),
  in both the current and `legacy_v1` scorers. Fair: energy = mean_rms(pred, truth) − ½·m/(m−1)·mean_rms(pred, pred);
  CRPS half_self divided by m(m−1) instead of m². Fair needs m ≥ 2 prediction members (EvaluationError otherwise); truth
  members may be 1. Reports carry `"estimator"` and the matching `scoring_convention`; `grade.json` carries
  `scoring_estimator` (evaluation.SCORING_ESTIMATOR = "fair").
- `plugin` is bit-identical to the old code: checked with `==` against the pre-change modules loaded from their git blobs
  (functions, whole `score_case` and `evaluate_trusted_predictor` reports), for both scorers. Perturbing the plugin weight
  by one ulp fails 8 checks.
- `rewards.precision_reward`: the fair estimate is ≥ 0 exactly (triangle inequality on the RMS metric, per truth draw)
  but can round to about −4e-16 where the exact score is 0 (for example 2 members bracketing the truth). Values within
  1e-12 of 0 now count as 0 instead of raising. Not seen in any real run (minimum fair primary 0.00648; minimum group
  energy per truth draw 2.7e-8).

## Tests (`scripts/physim/check_scoring.py`, 61 checks, run by hand)

The repo's AGENTS.md says not to add per-environment unit tests to `tests/`, and CI does not install physim (the module
was being skipped), so the checks live in `scripts/physim/` and run with
`uv pip install -e ./environments/physim pytest && pytest scripts/physim/check_scoring.py`. 61 passed on both branches.
CI's own `uv run pytest tests`: 13 passed (main), 12 passed (labworlds). `ruff check` and `ruff format --check` (0.15.20)
pass on the whole repo on both branches.

- Unbiasedness by Monte Carlo (N(0, I₃) forecasts and truths, n_truth = 2): fair energy at m = 2/4/16/64 is
  0.6523/0.6529/0.6584/0.6371 ± (0.002–0.006) against the exact 0.6515; plugin − fair = 0.3252/0.1629/0.0409/0.0102
  against E|X−X'|/(2m) = 0.3257/0.1629/0.0407/0.0102. Fair CRPS for N(0,1): 0.5588/0.5628/0.5652/0.5661 against
  1/√π = 0.5642. All within 4 SE.
- Gaussian closed form for the fair CRPS at m = 2, 4, 16, 64 and y = −1.0, 0.3, 2.5: within 4 SE.
- Plugin bit-identity as above; fair with m = 1 raises; plugin with m = 1 unchanged; unknown estimators raise; grading
  uses and records fair; the CLI passes `--estimator` through. Mutations (fair dividing by m², SCORING_ESTIMATOR =
  "plugin") are caught.

## Seals

- Lab bundles pin the scorer in the world identity and in `suite.scoring_source_sha256`; Blobkit bundles pin it in
  `suite.scoring_source_sha256`. Every bundle sealed before the fix is refused by the fixed scorer.
- Lab kit: re-sealed by the coordinator (physim a4410720a, pinned to ef1f58c; data and truth files byte-identical,
  truth member 0 re-simulated bit for bit in your container, fed-vortex reference demo = 1.0263418694456978). A Mac
  cross-check opened the re-sealed kit with the fixed code (evaluation profile, all 15 truths read) and re-simulated
  all 15 fed-vortex truth cases: deterministic across code versions, but on macOS arm64 the global-sensor readout differs
  from the x86_64-built truths by ≤ 4.8e-15 (numpy reduction order), so bit-identity holds only on the build platform.
- **Blobkit registry (user decision):** the default catalog (`taskset.DEFAULT_CATALOG`, seanpohorence/physim-worlds@
  bd77a0da) holds bf 38d159a8, xv 440472fb and p4g2_044 0a1aa909, all pinning 3d8e3fb3 (plus legacy 0c133190 pinning
  dcd1ab23 at older revisions). On the fix branches the default taskset cannot grade until these are re-sealed and a
  new dataset revision is published with `DEFAULT_CATALOG` and `configs/physim/*.toml` bumped in the same change. A
  scratch re-seal (not published) showed reference demos reproduce `checks.json` exactly under fair (persistence has
  zero spread). Nothing was published.
- **physim repo pin:** `pyproject.toml`, `configs/physim/release.toml` and `uv.lock` pin residency-environments a124e9b
  (old scorer, unformatted lab files), so that environment refuses the re-sealed kit until the pin moves to the fix.

## Impact (full table: `scorer-fix-impact-table.md` next to this file)

Re-scored 165 runs from saved forecasts and stored truths with both estimators, plus 10 control/calibration ensembles and
35 eval-calibration scratch variants. `plugin` equals the recorded numbers bit for bit on 158 of 165 runs and on every
ensemble table; the other 7 were graded on Linux x86_64 and differ by ≤ 3.5e-15 relative (reduction order; the
pre-fix scorer on this Mac gives the same numbers as the fixed plugin path). The per-case difference fair − plugin
matches −½·mean_all_pairs/(m−1) to 5.6e-15.

| world / bundle | rows | m / n | S change (min / median / max) | reward K=2 change |
|---|---|---|---|---|
| fedvortex lab (Astra pilot, Qwen 9B mechanics) | 2 agents | 64 / 2 | Astra 0.10661 → 0.10597 (−0.60%); Qwen 349.8 unchanged (zero spread) | Astra 0.4861 → 0.4874; Qwen 0 |
| bf 38d159a8 | 35 agents | 64 / 2 | −2.99% / −0.03% / 0 | 0 … +0.0066 |
| xv 440472fb | 13 agents | 64 / 2 | −1.82% / −0.01% / 0 | 0 … +0.0040 |
| p4g2_044 0a1aa909 | 13 agents | 64 / 2 | −1.71% / −0.01% / 0 | 0 … +0.0013 |
| worked p4g2_044 legacy 0c133190 | 24 agents | 64 / 2 | −1.86% / −0.02% / 0 | 0 … +0.0040 |
| reference demos (initial persistence) | 15 | 4 / 2 | 0 (zero spread) | 0 |
| control tables bf/xv/p4 centered_v2, bf/xv legacy | 25 | 4 / 2 | independent_native −13% … −24%; others ≤ −0.25% | ≤ +0.0009 |
| reward calibration bf/xv/p4 | 9 | 4,16,64 / 2 | −20% / −5.5…−6% / −1.5% (the (m+1)/m rule) | 0 (S < 0.01) |
| worked-example predictor sanity | 13 | 4 / 2 | spread_x100 0.04747 → 0.02100 (−56%); others ≈ 0 | spread_x100 0.662 → 0.839 |

- **Rankings:** no flip inside any campaign or write-up table, no agent-vs-control flip on any bundle, no flip among
  controls. Two cross-campaign pairs on bf swap, each gap < 1.1%: qwen3.5-397b (campaign 0916) now edges terra (bf case
  study), and sonnet-5 (prime-agent-bf retries) now edges luna (bf scoring recovery).
- **Rewards:** agents only rise, by at most +0.0066 (sonnet-5 bf interface-v2, S 0.2221 → 0.2155). No row crosses S = 1
  or S = 0.01, so no reward leaves 0 or reaches 1 because of the estimator.
- **Calibration:** the integer-K rule (`reward-calibration.json`) stays K = 2 (worst native 0.0017935 → 0.0017663). The
  fractional rule (bf case study) moves K 2.7463 → 2.7529; rewards there change by ≤ ±0.003. The 4 > 16 > 64-member
  ordering of the calibration means was the plugin bias; under fair they agree (bf 0.001783 / 0.001784 / 0.001766).
  Control ratios against the 4-member independent native rise 1.15–1.32× (bf persistence 224.7 → 281.7), so separations
  only grow and no acceptance or curation verdict flips. LABWORLDS' fed-vortex K = 1 rule still holds.
- **Not re-scorable (ratio tables only, ensembles not kept):** labworlds reports (round2, worlds_round, battery,
  curation, converge) and runs_out tables. By the (m+1)/m rule, ratios to the native rise about 1.125× (m = 8) or 1.25×
  (m = 4): round2 fed-vortex persistence/native 15.9 → about 17.9; worlds_round 23.6 → about 29.5. Kit README native
  rewards rise about +0.0034 each. Please re-score the gc_suites specificity tables in your container as planned.
- Some inputs (bf case study, p4-astra) were iCloud-only and were materialised on the Mac (`brctl download`, about
  168 MB of the user's own files). No Sol labworld pilot exists on the Mac; the Sol rows are PhySim v1 (bf) runs.

## Open questions

1. **Design (please weigh in):** the fair score is unbiased for i.i.d. members but is not proper over member sets the
   predictor chooses. A deterministic, over-dispersed ensemble can beat the oracle: a fixed 64-quantile ensemble scores
   0.5554 fair CRPS against the oracle's 0.5642 for N(0,1) truths (plugin gives 0.5643); with m = 2 members bracketing a
   U(0,1) truth the fair CRPS is exactly 0. At m = 64 the reward effect is about 0.0035 at K = 2. Options: accept
   (document, keep m = 64 fixed in grading), or require/verify i.i.d. sampling, or keep plugin for agent grading and use
   fair only for controls.
2. `VERSION` stays `r6-offline-score-v1` (bumping it would break the bit-identical plugin comparison); an absent
   `estimator` key means plugin. The fair convention string still starts "empirical distribution", which is loose.
3. The worked-example `validate_native.py` / `evaluate.py` score m = 1 forecasts, which now raise under the default;
   they need `estimator="plugin"` (or a 2-member broadcast, which reproduces plugin exactly).
4. Registry re-seal and re-release, physim pin bump, and the PR #40 formatting push: all waiting for the user.
