# Round 5, study vortexexam (track 2): an exam pilot on the fed-vortex world

**PILOT: never to be reused as an exam.** The hidden parameters of the pilot truths are drawn inside the GPU
jobs from the public prior and written to their outputs (`truths.json`); the copies under `results/` carry
`PILOT_NEVER_REUSE_AS_EXAM`. The 256-bit world secret is never written, only its commitment.

Question: does a world whose level 2 has its own effective law give an exam where understanding matters more
than on the gliders, where a predictor trained on prior simulations (P0) takes nearly all the skill?

Status (10 Nov 2026): jobs 1 and 2 (pilot A, small) are analysed; job 3 (pilot B, planned size) is running as
`r5-vortexexam-006`. `PROGRESS.md` has the state and the next steps. Every number below is in
`results/summary.json` (section `headline`) with its source.

## World and exam shape

- Level 0: the fed-vortex world of `track1/vortex_world` at 128 x 128 px (float64, 250 native steps per tick,
  one tick = 5 time units), stirring channel with exact nats at sigma_a = 0.005. Level 1: the vortex list.
  Level 2: (N, s_b) = vortex count and share of kind b. Mutation is declared per unit area (`mut128`).
- `vxlib.py` wraps it without changing it: per-member hidden parameters, a batched runner for the GPU, level-1
  summaries, a block raster, programs. At default parameters it equals the `vw` world of track 1
  (`results/check_lib.json`).
- Episode: 404 ticks (2,020 time units) from the declared initial law, labelling at tick 60, a 200-nat program of
  the public mix (none / blind / aimed at the heaviest kind-b vortex / regional) at ticks 130, 210, 290, 370.
- Exam item: the level-1 history of a main run up to one of those ticks, the program that starts there, and the
  question "level 2 at 8, 16, 32 ticks ahead" (40, 80, 160 time units). Score: fair energy score of 64 samples
  against replicate truths from the hidden state; skill = share of the climatology-to-oracle gap; sigma and rho
  from the shared `round5/agentenv/evaluator/acceptance.py`.
- Policies: K (the truth's other main runs at the same tick), D(n) (fitted to n Lab episodes), P0 (trained on
  prior simulations), S(n) (posterior from n Lab episodes, then the parameter-conditional predictor), T (the
  level-2 law with constants fitted to n Lab episodes), C (given the true parameters), O (replicates from the
  hidden state). Families: net, ridge (linear in level-1 summaries), law, lin2 (linear in level 2 only).

## Files

| file | what |
|---|---|
| `vxlib.py`, `vxnet.py`, `vxsbi.py` | world runner and level-1/2 pipeline; predictor families; identification (from `round4/sbi`) |
| `job1.py` | GPU job 1: throughput, law runs, one-at-a-time headroom scan (`--scan-only` repeats the scan) |
| `job2.py` | GPU jobs 2 and 3: the exam pilot (design, Lab, exam items, identification, policies, sigma and rho) |
| `select_prior.py`, `prior.json`, `prior_B.json` | hidden set and public constants: `prior.json` for job 2 (pilot A), `prior_B.json` for job 3 (pilot B) |
| `fetch_job.py`, `analyse1.py`, `analyse2.py`, `offline_views.py`, `make_summary.py` | from the gpu-jobs branch to `results/summary.json` |
| `check_lib.py`, `check_predictors.py`, `check_replay.py` | CPU checks run before the GPU jobs |
| `results/summary.json` | every number with its source; `results/job1`, `job2`, `job3`: small files of the jobs |

## GPU jobs

| job | what | GPU | pod hours | billed |
|---|---|---|---|---|
| `r5-vortexexam-001` | cancelled before start (cap too low for the only offer) | - | 0 | $0 |
| `r5-vortexexam-002` | job 1: throughput, law, scan | H200 (nebius, $6.69/h) | 0.38 | $2.29 |
| `r5-vortexexam-003` | job 2: pilot A, preset small, and a scan rerun | A100 40GB (lambdalabs, $1.99/h) | 0.73 | $1.31 |
| `r5-vortexexam-004` | rejected (purpose line over 300 characters) | - | 0 | $0 |
| `r5-vortexexam-005` | infra error at provisioning (cap 0.1 cent under rate x (max_hours + 0.25)) | H200 | 0.05 | $0 (at most $0.35) |
| `r5-vortexexam-006` | job 3: pilot B | A100 40GB | running | |

## Results (jobs 1 and 2)

1. **Throughput** (float64, with the vortex tracker). H200: 1,388-1,577 member-ticks/s at 64^2, 599 at 96^2,
   374 / 425 / 444 at 128^2 for batch 64 / 256 / 1024. A100 40GB: 169 at 128^2. The tracker and the host
   level-1/2 summaries cost 1%. $4.18 (H200) and $3.26 (A100) per million member-ticks, eight to ten times the
   gliders. P0's training set of pilot A (384 episodes) costs $0.51 on the A100 and 23 core-hours on CPU
   (gliders: 3.2), against 96 core-hours in a 4-core, 24-hour sandbox.
2. **Effective law** (128^2, 5 selection coefficients x 64 members x 440 ticks, no stirring). The
   80-time-unit change of the kind share has the replicator-mutator form b1 s (1 - s) + b2 (1 - 2 s): the
   fitted drift matches the binned mean change (R^2 0.95-0.98), and iterating it from tick 100 predicts the
   ensemble mean to tick 436 within 0.015-0.053 (out of sample 0.026-0.056, up to 6.8 standard errors of the
   mean). The rate is linear in eps above 0.1 (b1 = -0.086 + 1.44 eps) but not proportional to it: b1 is zero
   at eps = 0 (-0.006 +- 0.009) and the line crosses zero at eps = 0.06. For one trajectory the law explains
   6% (eps 0) to 49% (eps 0.4) of the variance of the change, the same as any function of s_b alone. Over the
   prior of pilot A (192 parameter points), eps alone carries the variation of the rate (R^2 0.74 with eps,
   0.74 with all four parameters).
3. **Headroom** (13 candidates, both box edges, 12 members x 2 anchors, 4 truths and 4 controls per state).
   Given the true state, plugging in the default parameters costs, in units of the climatology-to-oracle gap
   at level 2: e 8.4 / 0.9 (low / high edge), mu 4.3 / 1.0, kF 0.7 / 4.9, k 0.5 / 3.2, eps 0.4 / 2.7,
   nu 0.9 / 0.3; adv, kl, kY, dl, Dl and the mutation interval are at the noise floor (0.10 +- 0.05). On the
   level-1 block raster the largest are e 0.94, eps 0.55, k 0.53, mu 0.52, kF 0.30 (one edge each); the others
   are below 0.15. wi fails viability.
4. **Hidden sets.** The declared rule needs the plug-in deficits, and job 1's branch file was too large for the
   branch, so pilot A uses a proxy choice plus the mutation interval: (eps, mut128, nu, e). With the deficits
   (the runner cut the file down later) the rule picks (eps, mu, e): pilot B.
5. **Pilot A** (job 2; small: 6 truths, 192 design points x 2 episodes, 8 Lab episodes, 192 items, 6 replicate
   truths). Errors are over truths.
   - Full-history items: P0 0.559, C 0.557, S(1-8 episodes) 0.55-0.56; sigma = -0.003 +- 0.029. The exam fails
     the bar of 0.15, as the gliders did; rho is undefined when P0 equals C.
   - The parameters matter more than on the gliders: the prior-mean plug-in scores 0.351 (0.21 below C,
     5 of 6 truths; gliders 0.03-0.09), and the prior climatology is 3 skill units worse than the truth's own.
     P0 reads the parameters off the item's history.
   - Short-history items (CPU recomputation, `offline_views.py`; the pod's full-history scores reproduce): with
     the last three ticks only, the net's P0 falls to 0.47 and C stays at 0.57: sigma 0.18 +- 0.20, and S from
     one Lab episode recovers all of C (rho 1.0-1.15). At 8 Lab episodes a ridge fitted to the Lab data alone
     reaches 0.53 and sigma against that null is 0.06 +- 0.10.
   - T: 0.38, 0.46, 0.48, 0.50 at 1, 2, 4, 8 Lab episodes, against -0.38, -0.49, 0.06, 0.21 for the data-only
     net; T closes 81-91% of the gap from the data-only net to C. P0 is 0.06-0.18 above T.
   - Identification from 1 Lab episode (posterior sd / prior sd): eps 0.23, mut128 0.44, nu 0.28, e 0.06 from
     level-1 summaries; 0.38, 0.65, 0.37, 0.21 from (N, s_b) alone; 88-100% of the (truth, parameter) pairs lie
     inside the 90% intervals.
   - The test programs matter: an oracle that ignores them reaches 0.77 (1.02 without a program, 0.56 under a
     regional one).
   - Share of the oracle-predictable change of s_b reached at 40 / 80 / 160 time units (pooled over items as
     in round 3; the oracle-predictable share is 0.48 / 0.47 / 0.47): linear level-2 predictor 0.03 / 0.08 /
     -0.03 (P0) and 0.06 / 0.24 / 0.25 (true parameters); net P0 0.16 / 0.43 / 0.54; ridge P0 0.16 / 0.40 / 0.43.

## Pilot B (job 3)

Pending (`r5-vortexexam-006`): hidden set (eps, mu, e), planned size, dedicated and fine-tuned models at the
true parameters (a stronger C), and the short-history view scored on the pod.

## What failed

- Job 2's sizing rule fell from the planned 773 thousand member-ticks to 294 thousand on a slow A100 (the next
  preset missed its budget by 43 s). Fixed for job 3 (finer presets, measured stage timings).
- The scan inside job 2 shrank to 3 members and one anchor (rate table); not used for the headroom table.
- The hidden set of pilot A was fixed before the headroom was known and holds one parameter without any.
- Three requests cost time: a cap below the only offer, a purpose line over 300 characters, a cap 0.1 cent short.
