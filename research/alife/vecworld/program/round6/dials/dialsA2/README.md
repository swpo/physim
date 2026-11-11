# Round 6, dials, study dialsA2: the gliders stress-conversion exam, reopened with a triggered bar

**Question.** Round 5's gliders exam with an incomplete public law: the hidden world turns channel 0 into channel 1
where the wind exceeds a threshold (`../defect_gliders/dlaw.py`, term XW; eta = 4). On an exam built only from the
items that trigger the term (aimed 200 nats, regional 300 nats), scored at 8, 12 and 16 ticks, does the best generic
repair still leave a science share of at least 0.15 (T1) and close at most 0.7 of the gap (T2), does a recipe told the
form close the gap (T3), do the actions matter (T4), and do the bars survive the heaviest truth and each end horizon
(T5)? The lead's choice "Reopen, triggered bar" (`../../../roadmap/DECISIONS.md`); declared in `DECLARED.md`
(commit 3fd4076c5, before any code).

**Answer: UNDECIDED by the declared rule.** T1 to T5 all hold, by wide margins: sigma_G = 0.260 (lower bound 0.243,
bar 0.15), rho_G = 0.448 (upper bound 0.470, bar 0.7), the told-form recipe H recovers 0.996 of the P0-to-C gap and
beats the best generic repair at t = 25, and C blind to the program loses 0.46 of L(K) - L(C). The zero point misses on
all three declared pairs (0.05 to 0.08 against a tolerance of 0.02), so this is not a pass; it is not a fail either.
Why it misses (diagnosed after the results, reported only): the true-form net is weaker at eta = 0 than the
public-form net, and theta inference legitimately gains 0.05 over P0 at eta = 0 on this exam, which the declared pair
"G* against P0" cannot absorb.

PILOT ONLY. The truths are public pilot values; truths, Lab data, items and nets of this study must never be reused as
an exam. The form of the defect is public in this repository.

## What ran

| item | value |
|---|---|
| job | `r6-dialsa2-001`, code pinned at e0df0c079; A100-SXM4-40GB (lambdalabs, $1.99/h), jax 0.12.0.1, float64 world, float32 nets |
| time and cost | pod 20:28-23:54 UTC (3.43 h, presmoke of 7.7 min included), 3.30 h on the script's clock; exit 0; nothing failed, skipped or cut by the clock; **billed $6.62** of the $8.40 cap (study cap $12; `results/job/status.json`) |
| review | the runner's review: 0 blocker, 0 major, 3 minor, fine to run (`results/job/review.md`; acted on in `DEVIATIONS.md` entry 3) |
| truths | 16 (round 5's 8; 8 more: the first viable of 48 box draws, seed [6601, 4]) x eta 0 and 4; eta 1 and 2 on truths 0-3 |
| per world | Lab of 32 aimed/regional + 32 input-free + 32 designed episodes (8 arms: dose series 50-200 nats and two controls); two exams of 48 items x 12 replicates (`sel` for picks, `score` for every number) |
| families | public, true-form (eta 0 at 1/4 of points, 4 at 1/4, uniform at 1/2), designed: 768 points x 8 episodes each |
| nets | round 5's block net at horizons 8, 12, 16; 3 seeds per net; base nets 50 steps per dispatch, fine-tunes 40 |
| member-ticks | 3.07 million in the main pass (the job's planned count), plus the presmoke |

## The declared criteria

Sources: `results/summary.json` [headline], [criteria] (`a2_stats.criteria` on `results/job/scores.npz`, job
r6-dialsa2-001). eta 4, N = 8, horizons 8-16 pooled; SE = truths as clusters + the seed term; one-sided 90% bounds,
t(0.90, 15) = 1.341.

| criterion | number | median over truths; leave-one-truth-out | verdict |
|---|---|---|---|
| T1 sigma_G >= 0.15 | 0.260 ± 0.013; bounds 0.243, 0.278; contrast L(G*) - 0.85 L(C) - 0.15 L(K): lower bound +0.071 | 0.257; 0.255 to 0.266 | holds |
| T2 rho_G <= 0.7 | 0.448 ± 0.017; bounds 0.425, 0.470; contrast upper bound -0.079; L(P0) - L(C) = 0.341 ± 0.011 (31 SE: read) | 0.464; 0.441 to 0.456 | holds |
| T3 H solvable | recovers 0.996 ± 0.004 of P0-to-C; L(G*) - L(H) = 0.187 ± 0.007, t = 25.4 | 0.996; 0.995 to 0.997 | holds |
| T4 actions matter | blind C loses 0.459 ± 0.009 of L(K) - L(C) | 0.454; 0.456 to 0.462 | holds |
| T5 heaviest truth (14) out | sigma_G 0.263, rho_G 0.444 | worst single leave-out: 0.255, 0.456 | holds |
| T5 at 8 ticks / at 16 ticks | sigma_G 0.201 / 0.336; rho_G 0.437 / 0.478 | | holds |
| zero point: true-form C - public-form C (eta 0) | +0.069 ± 0.005, tolerance 0.02 | 0.071; 0.066 to 0.071 | misses |
| zero point: G* - P0 (eta 0) | -0.052 ± 0.012 | -0.058; -0.057 to -0.047 | misses |
| zero point: H - S (eta 0) | +0.077 ± 0.007 | 0.075; 0.074 to 0.081 | misses |
| reported cross pairs | G* - S: -0.001 ± 0.003; H - P0: +0.025 ± 0.016 | | not in the rule |
| **verdict** | PASS needs T1-T5 and the zero point; FAIL needs T1's upper bound < 0.15 or T2's lower bound > 0.7 | | **UNDECIDED** |

G* was the residual RES(8) for 46 of 48 truth-seed pairs (FT twice). C was the fine-tuned true-form net for 54% of
them (it changes L by 0.003 of K-C).

**What the outcome means.** The declared table (`DECLARED.md` Part 1) has rows for PASS and two kinds of FAIL; none
applies. By R21 an undecided result makes no claim and the next step goes to the lead. What can be said without a
new rule: on the triggered exam at 8-16 ticks, everything the plan's PASS row requires of the science bars holds by
wide margins, at N = 8 and at N = 32 (sigma_G 0.221 [0.204, 0.238], rho_G 0.534 [0.511, 0.557]), at eta 1 and 2
(4 truths: sigma_G 0.196 and 0.226, rho_G 0.272 and 0.422), with every truth left out and at each horizon; and the
told-form recipe solves it.

## Why the zero point misses (written after the results; reported only)

`results/summary.json` [diagnosis_after_results]; units of L(K) - L(public-form C) at eta 0.
- **The true-form net is weaker at eta 0**: +0.068, +0.073, +0.054, +0.069 at the four rungs, positive for every
  truth (0.030 to 0.106). It is even worse than P0 there. The true-form family had a quarter of its points at eta 0
  (my R7, so that H's draws and the eta 1/2 arms lie inside the trained range); study A's had half and its pair was
  +0.007. H uses this net, so H - S inherits it (H - true-form C is only +0.012).
- **The pair G* - P0 cannot hold on this exam.** At eta 0 the true theta is worth 0.055 ± 0.013 of K-C (P0 against
  public-form C: this exam's type-(a) share); S recovers 0.052 and FT 0.039, and G* picks them. G* - S is -0.001.
  So as declared ("G* against P0 within 0.02") the zero point would miss in any rerun of this exam.
- The law switch itself holds: on the pod one tick at eta 0 differs from `gworld.tick` by 7.6e-11, against 5.2e-11
  between two runs of `gworld.tick` (`results/job/presmoke/zero_point.json`); bitwise on CPU (study A).
- A weaker C works against T1 and T2 (a stronger C lowers L(C), raising sigma_G and lowering rho_G), so the misses do
  not flatter the bars; this is reasoning, not a measurement.

## Reported, never criteria

Share of the P0-to-C gap closed at eta 4 (`summary.json` [reported.recovery_of_P0_to_C_eta4_N8], [..._N32]):

| policy | N = 8 | N = 32 |
|---|---|---|
| H (designed episodes, told the form) | 0.996 | 0.986 |
| H_mix (mix episodes, told the form) | 0.991 | 0.981 |
| G* (best generic, picked on `sel`) | 0.448 | 0.534 |
| RES, cross-validated ridge / A's fixed ridge | 0.451 / 0.468 | 0.537 / 0.538 |
| FT | 0.178 | 0.244 |
| S (public law) | -0.193 | -0.193 |
| public-form net at the true theta | 0.018 | 0.017 |
| D net / D ridge | -1.82 / -0.72 | -0.99 / -0.40 |

- **Designed experiments add nothing measurable here**: L(H_mix) - L(H) = +0.005 ± 0.005 of the gap. Eta's posterior
  mean at the truth 4 is 3.51 (H) and 3.57 (H_mix) at N = 8, 3.64 and 3.71 at N = 32; at eta 0 it is 0.19 and 0.05
  ([reported.identification]). The mix episodes reveal the rate as well as the dose series does.
- **The defect is large on this exam**: s = (L(P0) - L(C)) / (L(K) - L(C)) = 0.471 ± 0.013 (0.36, 0.50, 0.64 at 8,
  12, 16 ticks). Skill against the oracle: P0 0.252, S 0.208, FT 0.292, RES 0.353, C 0.476, H 0.475.
- **By class** (N = 8): aimed sigma_G 0.226, rho_G 0.264; regional 0.291, 0.528. **By horizon**: 8 ticks 0.201,
  0.437; 12 ticks 0.285, 0.430; 16 ticks 0.336, 0.478.
- **Actions matter only through the hidden term**: at eta 0 the true-form net blind to the program does better than
  with it (by 0.013 of K-C); at eta 4 the program is worth 0.46.
- **Scripted inference is misled** at eta 4: S's posterior sits 1.3 to 1.6 prior SD from the truth in three of four
  parameters (0.07 to 0.23 at eta 0); H's sits 0.14 to 0.52, H_mix's 0.11 to 0.36.
- **Study A's whole exam, quoted** (job r6-dialsa-003, 8 truths, all four classes, horizons 1-16;
  `../dialsA/results/summary.json`): sigma against P0 0.146, against its generic repair 0.077; on the triggered
  classes at 1-16 ticks 0.279 and 0.129. This study's triggered exam at 8-16 ticks: 0.471 and 0.260.

## Training

- **Base nets meet the plan's rule at 192,000 steps** (best validation steps 25,250 to 71,750). At 24,000 the best
  steps were 22,250 to 23,500; at 48,000 one net was past 80% (39,500); at 96,000 one (79,750). The validation
  minimum (about 0.40 public, 0.43 true-form) is reached by 30,000-50,000 steps; longer schedules overfit and the
  best-validation parameters are kept. Unlike study A, the length did not move the shares: s with the true-form net
  alone is 0.483, 0.488, 0.493, 0.470 at the four rungs ([reported.base_schedule_rungs]; curves in [training.base]).
- **Fine-tunes**: every group's cross-validated pick is interior. CFT at N = 8 added a rate (4e-6) once; FT at
  N = 32, eta 0 doubled to 800 steps once. The groups' best points for FT at N = 8 are 90 (eta 0) and 170 (eta 4)
  steps at rate 2e-5; a quarter of CFT nets pick 0 steps ([training.ft]).
- **D nets** meet the rule at 1,200 steps (best mostly at 100-150 steps); no group was stopped by the deadline.

## Limits

- H is told the threshold, the ramp and the rate's range [0, 4], with the truth at its top; that favours H. Whether an
  agent finds the form, only rollouts say.
- The verdict is relative to the generic recipes listed (P0, D, S, FT, RES). One world, one defect, the block view,
  triggered items only, 8-16 ticks, a Lab of 8 (32 reported) episodes, 16 truths.
- The whole exam was not re-sat (`DEVIATIONS.md` entry 1); A's numbers are quoted.
- Added after the results were seen, reported only: the diagnosis block in `make_summary.py`.

## Next step

For the lead (R21). The science and solvability bars are met with margin; what blocks a pass is the zero point, and
part of it (G* against P0) cannot hold on this exam. Two choices: (a) re-declare the zero point before a new run,
with G* read against S and a true-form family as large at eta 0 as the public family (one job, families, base nets
and both dial values again, about 3 h, about $6-7 at $1.99/h; the study has $5.38 of its $12 left, so the cap would
need raising); or (b) take this exam profile to rollouts as it stands, as an undecided design whose bars hold, since
only rollouts say whether an agent finds the form.

## Files

| file | content |
|---|---|
| `DECLARED.md` | the binding sizes, policies, criteria, outcome table, and Part 2 rules (commit 3fd4076c5) |
| `DEVIATIONS.md` | four entries, each written at the time |
| `results/summary.json` | every number above with its source (job id, file, key) |
| `results/job/` | the job's outputs, `status.json`, `review.md`, `sysinfo.txt`; `nets.npz` stays on the jobs branch |
| `a2_lib.py` | scanned trainers, rate-per-net fine-tunes, designed arms, H and H_mix |
| `a2_stats.py`, `make_summary.py` | the criteria; the summary (CPU, seconds) |
| `run_a2.py`, `job.sh` | the job: presmoke at full shapes, speed guard, full pass |
| `PROGRESS.md` | the log |
