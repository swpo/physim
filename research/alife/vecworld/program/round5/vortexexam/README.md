# Round 5, study vortexexam (track 2): an exam pilot on the fed-vortex world

**PILOT: never to be reused as an exam.** The hidden parameters of the pilot truths are drawn inside the GPU
jobs from the public prior and written to their outputs (`truths.json`); the copies under `results/` carry
`PILOT_NEVER_REUSE_AS_EXAM`. The 256-bit world secret is never written, only its commitment.

Question: does a world whose level 2 has its own effective law give an exam where understanding matters more
than on the gliders, where a predictor trained on prior simulations (P0) takes nearly all the skill?

**Answer** (10 Nov 2026; three GPU jobs, $7.32 billed of $25). The hidden parameters matter far more here than
on the gliders (the prior-mean plug-in loses 0.21 and 0.53 of oracle skill in the two pilots, against 0.03-0.09),
and level 2 has a law an agent could find. The exam still fails both acceptance bars. With the item's full
history a net trained on prior simulations is within 0.00-0.03 of the net given the true parameters (sigma
-0.003 +- 0.029 and 0.061 +- 0.048; 0.14 +- 0.05 against the best parameter-aware predictor of any family). Where
knowing the parameters does pay (items that show only the last three ticks: sigma 0.23 +- 0.16), scripted
inference from one Lab episode recovers 0.92 of it.

Every number here is in `results/summary.json` (section `headline`) with its job, file and key.

## Exam shape

- World: `track1/vortex_world` at 128 x 128 px (float64; one tick = 250 native steps = 5 time units), stirring
  channel with exact nats. Level 1 = vortex list, level 2 = (N, s_b). `vxlib.py` adds per-member hidden
  parameters and a batched runner; at default parameters it equals the track-1 world (`results/check_lib.json`).
- Episode: 404 ticks, labelling at tick 60, a 200-nat program of the public mix (none / blind / aimed / regional)
  at ticks 130, 210, 290, 370. Item: the level-1 history up to one of those ticks, the program starting there,
  and level 2 at 8, 16, 32 ticks ahead (40-160 time units). Fair energy score against replicate truths;
  skill = share of the climatology-to-oracle gap; sigma and rho from `round5/agentenv/evaluator/acceptance.py`.
- Policies: K, D(n), P0, S(n), C, O as in the roadmap, and T = the level-2 law with constants fitted to n Lab
  episodes. Families: net, ridge (linear in level-1 summaries), law, lin2 (linear in level 2); `net~3` and
  `ridge~3` see only the last three ticks of an item.

## Files

| file | what |
|---|---|
| `vxlib.py`, `vxnet.py`, `vxsbi.py` | runner and level-1/2 pipeline; predictor families; identification (from `round4/sbi`) |
| `job1.py` | GPU job 1: throughput, law runs, headroom scan |
| `job2.py` | GPU jobs 2 and 3: the exam pilot |
| `select_prior.py`, `prior.json`, `prior_B.json` | hidden set and public constants of pilot A and pilot B |
| `fetch_job.py`, `analyse1.py`, `analyse2.py`, `offline_views.py`, `make_summary.py` | from the gpu-jobs branch to `results/summary.json` |
| `check_*.py` | CPU checks run before the GPU jobs |
| `results/` | `summary.json`; `job1`, `job2`, `job3` = small files of the three jobs |

## GPU jobs

| job | what | GPU | pod hours | billed |
|---|---|---|---|---|
| `r5-vortexexam-002` | job 1: throughput, law, scan | H200 (nebius, $6.69/h) | 0.38 | $2.29 |
| `r5-vortexexam-003` | job 2: pilot A (eps, mut128, nu, e), 6 truths | A100 40GB (lambdalabs, $1.99/h) | 0.73 | $1.31 |
| `r5-vortexexam-006` | job 3: pilot B (eps, mu, e), 10 truths | A100 40GB (lambdalabs, $1.99/h) | 1.94 | $3.72 |

`001` was cancelled, `004` rejected and `005` stopped at provisioning (at most $0.35), all before any job time.

## Results

1. **Throughput.** 444 member-ticks/s at 128^2 on the H200 (1,577 at 64^2), 169 on the A100; the tracker and
   level-1/2 summaries cost 1%. $3.3-4.2 per million member-ticks, eight to ten times the gliders. P0's training
   set costs 23 (pilot A) and 61 (pilot B) core-hours on CPU, against 96 in a 4-core, 24-hour sandbox.
2. **Effective law** (5 values of eps x 64 members x 440 ticks). The 80-time-unit change of the kind share
   follows b1 s (1 - s) + b2 (1 - 2 s) (R^2 0.95-0.98 against the binned mean change); iterated over 1,680 time
   units it predicts the ensemble mean within 0.015-0.053. The rate is linear in eps above 0.1 (-0.086 + 1.44
   eps) but not proportional: zero at eps = 0, crossing zero at 0.06. Over both priors eps alone carries the
   rate. For one trajectory the law explains 6-49% of the change, as much as any function of s_b.
3. **Headroom** (13 candidates, 12 members x 2 anchors). Plugging in default parameters from the true state
   costs, in units of the climatology-to-oracle gap at level 2: e 8.4 / 0.9 (low / high edge), mu 4.3 / 1.0,
   kF 0.7 / 4.9, k 0.5 / 3.2, eps 0.4 / 2.7, nu 0.9 / 0.3; six others, the mutation interval among them, are at
   the noise floor (0.10 +- 0.05). Level 1 (block raster): at most 0.94 (e). Pilot A's hidden set was fixed on a
   proxy before this table existed; the declared rule on the table gives pilot B's.
4. **The exam, full-history items.**

   | skill | P0 | C | prior mean | S(1) | D(max) | T(1) / T(max) | sigma (net) |
   |---|---|---|---|---|---|---|---|
   | pilot A (8 Lab episodes at most) | 0.559 | 0.557 | 0.351 | 0.562 | 0.21 | 0.38 / 0.50 | -0.003 +- 0.029 |
   | pilot B (16) | 0.488 | 0.519 | -0.013 | 0.517 | 0.28 | 0.16 / 0.44 | 0.061 +- 0.048 |

   Net family; errors over truths. In B a net fine-tuned from P0 on 32 simulations at the truth scores 0.521 and
   one trained from scratch on them 0.387. Against the best null and the best C of any family sigma is
   0.136 +- 0.051 up to 8 Lab episodes and 0.093 +- 0.013 at 16. A CPU recomputation of A with other seeds gives
   0.045 +- 0.034.
5. **Short-history items** (last three ticks). B: P0 0.433, C 0.564, S(1) 0.554, so sigma 0.232 +- 0.157 and rho
   0.85-0.96 at every budget; at 16 Lab episodes a ridge fitted to the Lab data alone reaches 0.512 and sigma
   falls to 0.093. A (CPU): P0 0.47, C 0.57, sigma 0.18 +- 0.20. Given the true parameters the long history hurts
   (B: 0.045, 10 of 10 truths).
6. **T** beats every data-only family up to 4 Lab episodes (by 0.8-0.9 at one, 0.1-0.2 at four) and closes
   64-91% of the gap from the data-only net to C; P0 stays 0.05-0.33 above it.
7. **Other.** Identification from one Lab episode shrinks the posterior sd to 0.06-0.44 of the prior from
   level-1 summaries and 0.21-0.74 from level 2 alone, with 87-100% coverage of the 90% intervals. An oracle that
   ignores the test program reaches 0.75-0.77. Of the oracle-predictable change of s_b at 40 / 80 / 160 time
   units a linear level-2 predictor reaches 0.09 / 0.08 / 0.20 and the net 0.30 / 0.49 / 0.72 (B, within truths).
   Both pilots order the net above the linear level-2 predictor at z 4.8 and 5.2 with the truth as the unit.

## What this decides

- A level 2 with its own law, and parameters that matter several times more, do not make the exam test
  science: with the simulator, P0 carries it.
- What an item reveals is the stronger dial (hiding the history raises sigma to 0.2); the Lab budget is the
  second (at 16 episodes a data-only fit closes most of that gap).
- Inferring the hidden parameters is scriptable here as on the gliders.
- Without a simulator the level-2 law is what pays, at small budgets.

## What failed

- Job 2's sizing rule fell to its smallest preset on a slow A100 (the next one missed by 43 s); its inner scan
  shrank to 3 members. Fixed for job 3; the headroom table uses job 1's branches, cut down by the runner.
- Pilot A's hidden set holds a parameter without headroom (the mutation interval).
- Three requests failed on form: a cap below the only offer, a purpose line over 300 characters, a cap 0.1 cent
  short.
- Nets trained from scratch on 32 simulations are worse than P0; rho on full-history items is ill-defined.
- With 6 and 10 truths the short-history shares carry errors of 0.10-0.20.
