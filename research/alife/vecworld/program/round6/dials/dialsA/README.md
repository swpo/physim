# Round 6, dials, study A: the gliders calibration

**Question.** The public law of the gliders wind world lacks one term: where the wind exceeds a threshold,
channel 0 turns into channel 1 (`../defect_gliders/dlaw.py`, term XW; eta = 4, threshold 0.12, ramp 0.05). Does a
generic repair with no idea of what is wrong close the gap between P0 (a net trained on simulations of the
public prior) and C (a net trained on the true form at the truth)? The repairs are FT(N), P0's net fine-tuned on
N Lab episodes, and RES(N), P0 plus a per-block residual fitted on N Lab episodes. The designer's CPU stand-in
said one or two episodes per class close 0.70 to 1.46 of the gap.

**Answer.** No: by the declared rule, "generic repair wins" is **refuted** on nets. With 8 Lab episodes (2 per
program class) the better of FT and RES closes g = 0.47 ± 0.03 of the P0-to-C gap (one-sided 90% bounds 0.43
and 0.52, against the bar of 0.7). With 32 episodes it closes 0.61 ± 0.03. The residual does all of it;
fine-tuning closes 0.08. The defect reaches a net as forecast (s = 0.28 ± 0.01 on the aimed and regional
classes; forecast 0.20), and the zero point holds. In the plan's table this is "A: refuted", with s >= 0.15:
stress conversion is reopened as an exam design. One reported number limits what that reopening can claim: after
generic repair the science share left is 0.08 on the whole exam and 0.13 on the two triggered classes, below
the roadmap's 0.15.

PILOT ONLY. The truths are round 5's public pilot truths. Truths, Lab data, items and nets of this study must
never be reused as an exam. A has no pass bar: nothing here records an exam as passing.

## What ran

One GPU job, `r6-dialsa-003` (code pinned at f38f88ac0): A100-SXM4-40GB (lambdalabs, $1.99/h), jax 0.12.0.1,
float64 world and float32 nets, 62 minutes on the pod (1.03 h on the script's clock, the presmoke's 6 minutes
included), exit 0, nothing failed, nothing cut by the clock. **Billed $2.08** of the $5 cap. Three earlier
requests cost nothing: one dropped for a capital letter in its id, one rejected for the length of its notes,
one held by the runner's review and replaced by the coordinator (`DEVIATIONS.md`, entry 5). No extension was
requested: the rule did not come out undecided. No model call.

| size | value |
|---|---|
| truths | round 5's 8 pilot truths (4 hidden parameters), each at eta 0 and 4: 16 hidden worlds |
| per world | Lab of 32 mix + 32 input-free episodes; two exams of 48 items x 12 replicates: `sel` (picks only) and `score` (every number below) |
| training | public family and true-form family, 768 points x 8 mix episodes each; the true-form family has eta = 0 at 384 points and 4 at 384 |
| nets | round 5's block-view net; 3 seeds of each base net; fine-tunes and D nets per world and seed |
| member-ticks | 1.79 million, plus 0.18 million in the presmoke (the plan: 1.80) |
| horizons, score | 1, 2, 4, 8, 16 ticks; L = fair energy score summed over horizons, mean over items |

## The declared criteria

Sources: `results/summary.json` [headline] and [criteria], computed by `a_stats.criteria` from
`results/job/scores.npz` (job r6-dialsa-003). Standard errors hold the truths as clusters and the training-seed
term; bounds are one-sided 90% (t, 7 df).

| criterion | number | median over truths; leave-one-truth-out | verdict |
|---|---|---|---|
| zero point: round 5's sigma (0.018 ± 0.004) at eta = 0 | 0.017 ± 0.004 | 0.016; 0.015 to 0.019 | holds (also by the stricter reading) |
| zero point: true-form C against public-form C, in units of L(K) - L(C) | +0.007 ± 0.001 | 0.008; 0.007 to 0.008 | holds (tolerance 0.02) |
| zero point: FT(8) against P0 | -0.005 ± 0.003 | -0.002; -0.006 to -0.003 | holds |
| zero point: RES(8) against P0 | +0.015 ± 0.001 | 0.016; 0.015 to 0.016 | holds, near the tolerance |
| s on the aimed and regional classes, eta = 4 | 0.279 ± 0.006 | 0.278; 0.276 to 0.282 | the stand-in holds (0.10 to 0.30; forecast 0.20) |
| g, all classes (primary) | 0.471 ± 0.031; bounds 0.427, 0.515 | 0.442; 0.444 to 0.482 | **refuted** (upper bound below 0.7); read, since L(P0) - L(C) = 0.308 ± 0.009 |
| g, aimed and regional (secondary) | 0.538 ± 0.027; bounds 0.500, 0.575 | 0.530; 0.517 to 0.550 | refuted |
| the study itself fails | zero point holds, s >= 0.05 | | no |

Per seed g is 0.465, 0.479 and 0.470; per truth it runs from 0.39 to 0.64. RES(8) was picked over FT(8) for
every truth and seed. C is the true-form net: its fine-tuned variant never improved on it (cross-validation
chose zero steps every time).

**What the outcome means** (the plan's table, row "A: refuted"): with s >= 0.15, stress conversion is reopened:
16 truths and a recipe told the form (the designer's stage 2, about $4) before any pass is claimed. The rows
for "confirmed" do not apply: fine-tuning and a residual are not shown to carry the exam, and the designer's
third CPU screen (the generic residual) overstated the repair. The stand-in for s held, so study B's stage 0
keeps its clause on the stand-in's P0-to-C share.

## Reported, never criteria

Share of the P0-to-C gap closed at eta = 4 (`summary.json` [reported.closure_of_P0_to_C_eta4]):

| policy | all classes | aimed + regional | aimed | regional |
|---|---|---|---|---|
| RES(2) | 0.17 ± 0.08 | 0.22 ± 0.07 | 0.04 ± 0.03 | 0.30 ± 0.09 |
| RES(8) | 0.47 ± 0.03 | 0.54 ± 0.03 | 0.36 ± 0.05 | 0.62 ± 0.02 |
| RES(32) | 0.61 ± 0.03 | 0.65 ± 0.02 | 0.58 ± 0.03 | 0.69 ± 0.01 |
| FT(2), FT(8), FT(32) | -0.01 ± 0.01, 0.08 ± 0.03, 0.12 ± 0.03 | 0.01, 0.07, 0.11 | 0.01, 0.09, 0.16 | 0.02, 0.07, 0.09 |
| better of FT, RES and the cross-validated residual, N = 8 | 0.48 ± 0.03 | 0.53 ± 0.03 | | |
| S(8), scripted inference with the public law | 0.03 ± 0.03 | 0.00 ± 0.02 | | |
| public-form net at the true parameters | 0.10 ± 0.03 | 0.05 ± 0.02 | | |
| control: FT, RES on 8 input-free Lab episodes | 0.06, 0.00 | 0.04, 0.00 | | |

- **Against the stand-in.** With 2 Lab episodes per class the stand-in gave 1.46 (aimed) and 0.93 (regional); the
  nets give 0.36 and 0.62. With 8 per class they give 0.58 and 0.69.
- **By horizon** (N = 8, all classes; [reported.g_per_horizon_eta4]): g is 0.73, 0.66, 0.50, 0.24, 0.27 at 1, 2,
  4, 8, 16 ticks. The residual repairs the conversion where it happens and not what follows from it.
- **What is left for science** ([reported.science_share_eta4]): sigma against P0 is 0.146 ± 0.004 on the whole exam
  and 0.279 on the triggered classes. Against the generic repair G it is 0.077 ± 0.006 and 0.129 ± 0.008 at
  N = 8, and 0.057 and 0.098 at N = 32. By horizon on the triggered classes at N = 8: 0.04, 0.07, 0.12, 0.25, 0.41.
- **Screens** ([reported.screens_eta4]): given the state the public law loses 0.33 (aimed) and 0.59 (regional) of
  the climatology-to-oracle range, 0.23 over the mix; a history-only net keeps 0.39 and 0.48 of that (the
  stand-in: 0.19 and 0.38).
- **The repair needs the Lab's actions**: fitted on input-free episodes it closes nothing. The Lab's own
  bookkeeping shows the term: the channel-0 block sum falls by 10% (aimed) and 27% (regional) over a program.
- **Scripted inference is misled.** With the public law at eta = 4 its posterior narrows as at eta = 0 but sits
  0.6 to 0.9 prior SD from the truth in three of four parameters (0.15 to 0.3 at eta = 0;
  `results/job/identification.json`).
- **Skill relative to the oracle**, all classes: at eta = 0, P0 0.701 and C 0.713; at eta = 4, P0 0.620, RES(8)
  0.669, RES(32) 0.684, C 0.726, the state-given public law 0.773. D(32) reaches 0.52 to 0.57.

## Training

- **Base nets are not converged by the plan's rule.** Best validation steps are 22,750 to 24,000 of 24,000, the
  cap set in `DECLARED.md` R16 (the research budget told to the agent: P0 costs 8,048 of 8,192 episode
  equivalents at this length). Each doubling still moved the numbers: s with the true-form net alone is 0.247,
  0.267, 0.279 at 6,000, 12,000, 24,000 steps, and sigma at the zero point 0.013, 0.015, 0.017
  ([reported.base_schedule_rungs]; validation curves in [training.base]). C gains faster than P0, so a longer
  schedule would widen the gap that RES must close.
- **Fine-tunes meet the rule**: the mean cross-validation curve has its minimum at 40 steps for N = 8 and at 40 to
  120 steps for N = 32, then rises ([training.fine_tunes]). The 40-step grid is coarse against that: the minimum
  is the first grid point. D nets meet the rule (best step 250 of 1,200).

## Limits

- The verdict is about two recipes as declared. Fine-tuning all weights at a rate of 1e-4 overfits within 40
  steps; a finer grid, a smaller rate, or a residual on the wind field itself (the adversary's untried idea) may
  close more. A pass of any reopened design is relative to the generic recipes tried.
- The residual's ridge is the designer's (0.05). It costs 0.015 of K-to-C at eta = 0 and harms the blind and
  input-free items at eta = 4; a ridge chosen by leave-one-episode-out removes the harm and closes the same
  share (0.46).
- C saw half as many triggered true-law episodes (1,536) as P0 saw public ones (3,072), because one true-form
  family serves both dial values. A stronger C would lower g further.
- 8 truths, one world, a Lab of at most 32 episodes, 1 to 16 ticks, the block view.
- Added to `make_summary.py` after the results were seen, reported only: the science share by budget and by
  horizon, the cross-validation gain, the counts of chosen ridges.

## Next step

By the plan's table: the designer's stage 2 on stress conversion, 16 truths and a recipe told the form, about
$4. Before it is requested I would settle two things at no GPU cost, since they decide what it can show: (1)
the bar it is read against, because with RES in the null the science share is 0.08 on the exam as sat and 0.13
on the triggered classes, so a pass is possible only as a claim about the triggered classes at 8 to 16 ticks or
with a stronger trigger; (2) a base schedule beyond 24,000 steps, which the told research budget does not
cover. The six base nets of this job are kept at `origin/gpu-jobs:jobs/r6-dialsa-003/out/nets.npz`, and
`run_a.py --extension` adds truths without retraining them.

## Files

| file | content |
|---|---|
| `DECLARED.md` | the plan's sizes, policies, criteria and thresholds for A, and the readings fixed before any run (commit 94451e27c) |
| `DEVIATIONS.md` | six entries, each written at the time |
| `results/summary.json` | every number above with its source (job id, file, key) |
| `results/job/` | the job's outputs, its `status.json`, `review.md`, `sysinfo.txt`; `nets.npz` stays on the jobs branch |
| `results/check_a.json` | CPU checks: at eta = 0 one tick, a family and a Lab batch are bitwise equal to round 5's code |
| `recheck.py`, `results/recheck.json` | the headline recomputed in plain numpy from the saved scores (agrees to 2e-9) |
| `xlaw.py` | the law switch around `ladder_lib`: `dlaw.tick` behind `gworld.tick`'s signature, eta as a traced parameter |
| `a_nets.py` | cross-validated fine-tuning in lockstep, the residual, program classes |
| `a_stats.py`, `make_summary.py` | the criteria; the summary (CPU, seconds) |
| `run_a.py`, `job.sh` | the job: presmoke at full shapes, speed guard, full pass; `--extension` for more truths |
| `check_a.py` | the CPU checks |
| `PROGRESS.md` | the log |
