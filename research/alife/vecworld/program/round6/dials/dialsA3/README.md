# Round 6, dials, study dialsA3: the zero-point rerun of the reopened gliders exam

**Question.** Study dialsA2 (the gliders exam with stress conversion hidden, triggered items, 8-16 ticks) ended
UNDECIDED: T1 to T5 held, but the zero point at eta 0 missed on all three pairs. This study reruns it on 16 new truths
with a re-declared zero point (`DECLARED.md`, commit 3e9026c7b, before any code): a true-form training family with as
many eta-0 points as the public family has points (768 of 1,536), the pair "G\* against S" in place of "G\* against
P0", and a presmoke stop rule. Does the zero point now hold, and do T1 to T5 hold on new truths?

**Answer: UNDECIDED by the declared rule** (`DECLARED.md` A3-11, row 2). T1 to T5 hold again, on 16 truths nobody
had seen. The zero point misses again, now in the **other direction**: with twice the training data, the true-form
net at eta 0 is *better* than the public-form net, by 0.105 of L(K) - L(public-form C), where dialsA2's was worse by
0.069. G\* against S holds (-0.004). The job was cut by the platform after the N = 8 stage and no output file came
back, so the verdict and point estimates come from the job's own first look (computed in the job by
`a3_stats.criteria` on the complete N = 8 scores) as it survives in the runner's heartbeat tails. The standard errors,
bounds, medians and leave-one-truth-out ranges were lost with the files.

PILOT ONLY. The truths are public pilot values; truths, Lab data, items and nets of this study must never be reused as
an exam. The form of the defect is public in this repository.

## What ran

| item | value |
|---|---|
| job | `r6-dialsa3-001`, code pinned at 37035b5c8; A100-SXM4-40GB (lambdalabs us-east-1, $1.99/h), jax 0.12.0.1, float64 world, float32 nets |
| time and cost | pod 04:18:54-07:59:33 UTC (3.68 h; ready 04:24); script 04:32 to about 07:50 (192 min logged); **`infra_error`: pod unreachable over SSH during the N = 32 fine-tunes, nothing collected; billed $7.1364** (conservative $7.3267) of the $9.60 cap and the study's $10 (`results/job/status.json` [cost], [pods]) |
| review | the runner's: 0 blocker, 0 major, 0 minor, fine to run (`results/job/review.md`; notes acted on in `DEVIATIONS.md` entry 1) |
| truths | 16 new: the first 16 viable of 48 box draws, seed [6631, 4] (43 of 48 viable); none equals a truth of dialsA2 |
| per world | as dialsA2: Lab of 32 aimed/regional + 32 input-free + 32 designed episodes; two exams of 48 items x 12 replicates (`sel`, `score`) |
| families | public 768 x 8 (385 s); true-form 1,536 x 8, eta 0 at 768, 4 at 256, uniform at 512 (802 s); designed 768 x 8 |
| nets | round 5's block net at 8, 12, 16 ticks, 3 seeds per net; base-net ladder 24k-192k; nets.npz sha256 68c8c24c...1a14 (the file was lost) |
| what ran / lost | ran: presmoke, families, worlds at eta 0 and 4, inference, base nets, N = 8 (FT, CFT, RES, S, H, H_mix, blind C), D(8). Lost: every output file; N = 32 and the eta 1/2 arm never finished (`DEVIATIONS.md` entry 2) |
| member-ticks | 3.58 million planned for the full pass (`results/job/progress_from_heartbeats.txt`) |

## The declared criteria, with dialsA2's numbers beside

Source: the job's first look after N = 8 (`results/summary.json` [headline], [skill_vs_O_N8]; job r6-dialsa3-001,
`status.json` heartbeat tails). eta 4, N = 8, horizons 8-16 pooled. dialsA2: `../dialsA2/results/summary.json`.

| criterion | dialsA3 | dialsA2 | verdict (dialsA3) |
|---|---|---|---|
| T1 sigma_G >= 0.15 (lower bound) | 0.337 | 0.260 [0.243, 0.278] | holds (bound computed in the job; its value lost) |
| T2 rho_G <= 0.7 (upper bound) | 0.380 | 0.448 [0.425, 0.470] | holds (as T1) |
| T3 H recovers >= 0.7 and beats G\* at t >= 3 | 0.992; t = 18.8 | 0.996; t = 25.4 | holds |
| T4 blind C loses >= 0.10 of K-C | about 0.48 (derived from skills) | 0.459 | holds |
| T5 heaviest truth out; 8 and 16 ticks alone | numbers lost | holds | holds |
| zero point (i) true-form C - public-form C | **-0.105** | +0.069 | misses |
| zero point (ii) G\* - S (new) | -0.004 | (-0.001, reported) | holds |
| zero point (iii) H - S | **-0.094** | +0.077 | misses |
| reported: G\* - P0 (dialsA2's pair); H - P0 | -0.062; -0.152 | -0.052; +0.025 | not in the rule |
| **verdict** | | UNDECIDED | **UNDECIDED** (PASS needs the zero point; FAIL needs T1 or T2 to fail) |

The presmoke's stop rule (A3-4; truth 0, 192-point families, 6,000 steps) read r = **-0.212 +- 0.024** against a
threshold of +0.067: go. It is one-sided (it stops only if the true-form C is worse), so it could not stop on this
direction; it did foretell the sign of the full pass's pair (+0.063 at 500 steps, -0.212 at 6,000).

## What the outcome means (DECLARED A3-11)

"The zero point misses again: the true-form machinery at eta 0 is in question; UNDECIDED, reported to the lead with the
presmoke and full numbers." Concretely, and written after the results (untested):
- **Pair (i) measures the training family, not the law.** The law switch at eta 0 equals `gworld.tick` to 5.4e-11 on
  this pod (presmoke). The pair was +0.069 with 768 true-form points, a quarter at eta 0 (dialsA2), +0.007 with 768,
  half at eta 0 (study A), and -0.105 with 1,536, half at eta 0 (here). The nets are data-limited: the true-form nets'
  best validation steps were 170,000-190,250 of 192,000 (score 0.385-0.388), the public-form nets' 39,750-77,750
  (0.406-0.410).
- **Pair (iii) inherits it.** H - true-form C is +0.011 at eta 0 (derived), close to dialsA2's +0.012.
- **G\* against S, the pair this study added, holds.** At eta 0 S matches the public-form C (0.000) and FT nearly does
  (+0.004); P0 trails it by 0.057 (dialsA2: 0.055), the type-(a) share of this exam at eta 0 (A3-5).
- **The bars are not like with like either.** C is trained on twice P0's data. If the true-form net's eta-0 advantage
  (0.050 of skill) carried to eta 4, a like-for-like C would give sigma_G about 0.27 and rho_G about 0.46
  (`results/summary.json` [derived_from_skills]), close to dialsA2's 0.260 and 0.448, and still inside the bars.

## Reported, never criteria

Skill against the oracle at N = 8 (`results/summary.json` [skill_vs_O_N8]):

| policy | eta 0 | eta 4 | | policy | eta 0 | eta 4 |
|---|---|---|---|---|---|---|
| public-form C | 0.473 | 0.260 | | S(8) | 0.473 | 0.224 |
| true-form net at truth | 0.523 | 0.569 | | FT(8) | 0.471 | 0.300 |
| CFT(8) | - | 0.569 | | RES(8) | 0.446 | 0.378 |
| P0 | 0.446 | 0.260 | | H(8), H_mix(8) | 0.518, 0.521 | 0.567, 0.567 |
| D net, D ridge (8) | -0.154, 0.162 | -0.126, 0.108 | | blind true-form net | 0.511 | 0.296 |

- At eta 4, share of the P0-to-C gap closed (derived): H 0.994, H_mix 0.994, RES 0.382, FT 0.129, S -0.117; s =
  (L(P0) - L(C)) / (L(K) - L(C)) = 0.543 (dialsA2 0.471).
- Designed experiments again add nothing measurable: H and H_mix both 0.567 at eta 4.
- Cost in episode equivalents (R19, from the declared sizes; simulated episodes of 82 ticks, Lab episodes of 33):
  P0, S, FT, RES and G\* use the public family (6,144) plus 8 Lab mix episodes; D 8 Lab episodes; H 18,432 simulated
  (designed 6,144 + true-form 12,288) plus 8 designed Lab episodes; H_mix 12,288 plus 8 mix; C the true-form family
  at the truth. The 192,000-step rung took 2,588 s for the six nets in lockstep.
- Lost: N = 32, the eta 1/2 arm, per class and per horizon, the identification table, H_mix against H's SE.

## Training

- **Base nets: not converged by the rule at 192,000, the declared maximum** (`DEVIATIONS.md` entry 3): best steps
  public-form 77,750, 59,750, 39,750; true-form 190,250, 170,000, 178,500. At 96,000: 30,000-55,000 and
  83,750-96,000. The 24,000 and 48,000 rungs also missed (the ladder climbed). 75 points of the validation curves
  survive ([training]).
- Fine-tunes at N = 8: every group's pick interior (CFT added the rate 4e-6). D(8) met the rule at 1,200 steps.

## What failed

The platform: the pod became unreachable during N = 32 and nothing was collected (`DEVIATIONS.md` entry 2). No second
job: the $2.86 left of the $10 buys at most 1.1 h; the declared required stages took about 166 min here.

## Next step (for the lead)

Two readings, both undecided by the rule: (a) the zero point as declared cannot hold while the reference nets are
data-limited, because pair (i) moves from +0.069 to -0.105 with the family alone; a zero point that compares like with
like needs both families at one size and composition and nets that converge by the rule (study A's balance, 768 points
half at eta 0, gave +0.007), or a pair read as a tolerance on the reference itself; one more job of about 3.5 h,
about $7-7.5 at $1.99/h, which needs a new cap. (b) Take the profile to rollouts as an undecided design: on two
independent sets of 16 truths T1 to T5 hold with margin, and only rollouts say whether an agent finds the form.

## Files

| file | content |
|---|---|
| `DECLARED.md` | dialsA2's declaration with the changes A3-1 to A3-11 (commit 3e9026c7b, before any code) |
| `DEVIATIONS.md` | three entries, each written at the time |
| `results/summary.json` | every number above with its source |
| `results/job/` | `status.json`, `manifest.json`, `review.md`, `heartbeat_commits.txt`, `progress_from_heartbeats.txt` |
| `run_a3.py`, `job.sh` | the job (dialsA2's with the declared changes) |
| `a3_stats.py`, `make_summary.py` | the criteria; the summary the job's files would have fed |
| `summarize_tails.py` | `results/summary.json` from the heartbeat tails |
| `PROGRESS.md` | the log |
