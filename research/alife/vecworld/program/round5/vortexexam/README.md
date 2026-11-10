# Round 5, study vortexexam (track 2): an exam pilot on the fed-vortex world

**PILOT: never to be reused as an exam.** The hidden parameters of the pilot truths are drawn inside the GPU
job from the public prior and written to its outputs (`truths.json`); every result file carries
`PILOT_NEVER_REUSE_AS_EXAM`. The 256-bit world secret is never written.

DRAFT of 10 Nov 2026, 02:15 UTC: jobs 1 and 2 are analysed; the follow-up exam job `r5-vortexexam-004` (pilot B)
is requested. State and next steps: `PROGRESS.md`.

Question: does a world whose level 2 has its own effective law give an exam where understanding matters more
than on the gliders, where a predictor trained on prior simulations (P0) takes nearly all the skill?

## World and exam shape

- Level 0: the fed-vortex world of `track1/vortex_world` at 128 x 128 px (float64, 250 native steps per tick,
  one tick = 5 time units), stirring channel with exact nats at sigma_a = 0.005. Level 1: the vortex list.
  Level 2: (N, s_b) = vortex count and share of kind b. Mutation is declared per unit area (`mut128`).
- `vxlib.py` wraps it without changing it: per-member hidden parameters, batched runner for the GPU, level-1
  summaries, block raster, programs. At default parameters it equals the `vw` world of track 1
  (`results/check_lib.json`).
- Episode: 404 ticks (2,020 time units) from the declared initial law, labelling at tick 60, a 200-nat program of
  the public mix (none / blind / aimed at the heaviest kind-b vortex / regional) at ticks 130, 210, 290, 370.
- Exam item: the level-1 history of a main run up to one of those ticks, the program that starts there, and the
  question "level 2 at 8, 16, 32 ticks ahead" (40, 80, 160 time units). Score: fair energy score of 64 samples
  against replicate truths from the hidden state; oracle-normalised skill; sigma and rho with the shared
  `round5/agentenv/evaluator/acceptance.py`.

## Files

| file | what |
|---|---|
| `vxlib.py`, `vxnet.py`, `vxsbi.py` | world runner and level-1/2 pipeline; predictor families net / ridge / law / lin2; identification (from `round4/sbi`) |
| `job1.py` | GPU job 1: throughput, law runs, one-at-a-time headroom scan (`--scan-only` repeats the scan) |
| `job2.py` | GPU job 2: the exam pilot (design, Lab, exam items, identification, policies K, D(N), P0, S(N), C, O) |
| `select_prior.py`, `prior.json`, `prior_B.json` | the hidden set and public constants; `prior.json` is what job 2 used |
| `fetch_job.py`, `analyse1.py`, `analyse2.py`, `make_summary.py` | from the gpu-jobs branch to `results/summary.json` |
| `check_lib.py`, `check_predictors.py`, `check_replay.py` | CPU checks run before the GPU jobs |
| `results/summary.json` | every number with its source |

GPU jobs: `r5-vortexexam-001` cancelled before start (cap too low for the only offer); `r5-vortexexam-002`
(job 1) done, H200, 0.33 h, $2.29 billed; `r5-vortexexam-003` (job 2, pilot A) done, A100 40GB, 0.65 h, $1.31
billed; `r5-vortexexam-004` (job 3, pilot B) requested.

## Results so far (job 1; sources in `results/summary.json`)

1. Throughput (H200, float64, with the vortex tracker): 1,388-1,577 member-ticks/s at 64^2, 599 at 96^2,
   374 / 425 / 444 at 128^2 for batch 64 / 256 / 1024. The tracker and the host level-1/2 summaries cost about 1%.
2. Effective law (128^2, 5 selection coefficients x 64 members x 440 ticks, no stirring). The 80-time-unit change
   of the kind share has the replicator-mutator form b1 s (1 - s) + b2 (1 - 2 s): the fitted drift matches the
   binned mean change (R^2 0.95-0.98), and iterating it from tick 100 predicts the ensemble mean to tick 436
   within 0.015-0.053 (out of sample 0.026-0.056, up to 6.8 standard errors of the mean). The rate is linear in eps
   above 0.1 (b1 = -0.086 + 1.44 eps) but not proportional to it: b1 is zero at eps = 0 (-0.006 +- 0.009) and the
   line crosses zero at eps = 0.06. For one trajectory the law explains 6% (eps 0) to 49% (eps 0.4) of the
   variance of the change, the same as any function of s_b alone.
3. Headroom (13 candidates, both box edges, 12 members x 2 anchors, 4 truths and 4 controls per state): given
   the true state, plugging in the default parameters costs, in units of the climatology-to-oracle gap at
   level 2: e 8.4 / 0.9 (low / high edge), mu 4.3 / 1.0, kF 0.7 / 4.9, k 0.5 / 3.2, eps 0.4 / 2.7, nu 0.9 / 0.3;
   adv, kl, kY, dl, Dl and the mutation interval are at the noise floor (0.10 +- 0.05). On the level-1 block
   raster the largest are e 0.94, eps 0.55, k 0.53, mu 0.52, kF 0.30 (one edge each); the others are below 0.15.
   wi fails viability.
4. The hidden set. The declared rule needs the plug-in deficits, which were not available when job 2 had to be
   requested (job 1's branch file was too large for the branch). Job 2 therefore uses a proxy choice plus the
   mutation interval: (eps, mut128, nu, e). With the deficits the rule picks (eps, mu, e) (`prior_B.json`); the
   mutation interval has no headroom and nu little.

## Exam pilot A (job 2, hidden set eps, mut128, nu, e; SMALL: 6 truths, 192 design points, 192 items)

The A100 it ran on gave 169 member-ticks/s (the H200 of job 1: 444), and the sizing rule then fell to the
smallest preset: no dedicated models, Lab budgets up to 8 episodes. First reading (skill = share of the
climatology-to-oracle gap of the pooled fair energy score; unit of the errors = truth):

- P0 (net trained on prior simulations) 0.559, C (the same net given the true parameters) 0.557, S (posterior
  from 1-8 Lab episodes) 0.55-0.56: science share sigma = -0.003 +- 0.029. The exam fails the bar (0.15) as the
  gliders did. rho is undefined when P0 equals C.
- The parameters do matter: the prior-mean plug-in scores 0.351 (0.21 below C, 5 of 6 truths; gliders: 0.03-0.09
  below), and the prior climatology is 3 skill units worse than the truth's own. P0 reads them off the item's
  history.
- Theory policy T (the replicator-mutator law with constants fitted to n Lab episodes; never runs level 0):
  0.38, 0.46, 0.48, 0.50 at n = 1, 2, 4, 8, against -0.38, -0.49, 0.06, 0.21 for the data-only net. T closes
  81-91% of the gap between the data-only net and C.
- The test programs matter: an oracle that ignores them reaches 0.77 (1.02 without a program, 0.56 under a
  regional one).
- Identification from 1 Lab episode (posterior sd / prior sd): level-1 summaries eps 0.23, mut128 0.44, nu 0.28,
  e 0.06; from (N, s_b) only 0.38, 0.65, 0.37, 0.21. 88-100% of truths inside the 90% intervals.
- Share of the oracle-predictable change of s_b reached (pooled over items as in round 3) at 40 / 80 / 160 time
  units: linear level-2 predictor 0.03 / 0.08 / -0.03 (P0) and 0.06 / 0.24 / 0.25 (given the true parameters); net
  0.16 / 0.43 / 0.54 (P0). The oracle-predictable share itself is 0.48 / 0.47 / 0.47.

## Exam pilot B (job 3)

Pending (`r5-vortexexam-004`): hidden set (eps, mu, e), planned size, dedicated and fine-tuned models at the true
parameters, and a short-history view of every item (the last three ticks only).
