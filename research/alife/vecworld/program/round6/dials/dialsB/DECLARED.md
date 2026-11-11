# dialsB: stage 0 of the membrane carrier (study B of `../PLAN.md`), declared before any run

11 Nov 2026. This file is committed before any job is requested and before any decisive run. It is not edited
afterwards: anything that turns out impossible or wrong goes to `DEVIATIONS.md` with the reason, at the time.
Every hidden value in this study is a PILOT value, never to be reused as an exam.

Part 1 is copied from the plan. Part 2 is what the plan leaves open and this study fixes now, before any result:
every item of part 2 is this study's choice, not the plan's, and is marked so in the report.

## 1. Copied from `../PLAN.md` (section 2, B)

Stage row: "0, CPU, about 5 CPU-hours (estimate) | state given, 64 px, 8 fresh seeds, main and control arm, per
horizon, with the cell-resolved list as a second view; the told-form recipe with truths off its grid; a
history-only stand-in as in A; the scans that fix the hidden parameter set and the ranges of rho, D_X, a0,
committed with a hash | build only if, pooled over seeds and 8-32 ticks: the better of the gains and A_act, picked
on the Lab episodes, closes <= 0.7 in the main arm, both with all start states and with each seed's heaviest left
out, and >= 0.7 in the control arm; the told-form recipe closes >= 0.7; and, if A found its stand-in to hold, the
stand-in's P0-to-C share is >= 0.10".

Also from the plan: horizons 8, 16 and 32 ticks; the focus view (cell mass and catalyst mass within 16 px of the
item's focus cell); main arm = the carrier converted at cells with the saturating route (`sublevel.py`, candidate
`pro`, cat = 1) at lam = 1; control arm = the carrier that converts everywhere (cat = 0), the same hidden draws;
a Lab of 16 episodes; "the gains" = the designer's gains on the public response (`gvh.py` G2, G3); A_act = the
adversary's policy (`crit_adversary/adv_act.py`): the public law under a delayed, blurred copy of the command,
four fitted numbers; the pilot centre of (rho, D_X, a0) is (0.02, 0.5, 0.03); standard errors with truths as
clusters, the median and the leave-one-truth-out range beside every mean; a result that is neither a pass nor a
fail is reported as undecided. Section 3 of the plan: "B: stage 0 fails | A filter on the command repairs the
carrier except in rare start states. B is not built, at no GPU cost. ..."; "B: main arm and control arm both
resist generic repair | The recipes are too weak to serve as a null; no pass is recorded until they are
strengthened."

From the assignment: one job on a rented CPU machine (16 vCPU), cap about $3, total cap of the study $5; no GPU
job; stages 1 and 2 are not built; the last condition (the stand-in's share) is reported and left marked
"depends on A".

## 2. Fixed here, before any run (this study's choices)

### 2.1 Sizes

| item | value |
|---|---|
| world | `sublevel.small_cfg(64)`: 64 x 64 px, 8 x 8 bumps, tick = 10 time units; public parameters at their defaults (`membrane_jax.THETA`) in every gate run and known to every policy, as in `gvh.py` and the adversary's runs |
| seeds | 31, 32, ..., 38 (the designer used 1, 5, 6; the adversary 5, 6, 7, 8) |
| arms | main: lam = 1, cat = 1; control: lam = 1, cat = 0; the same (rho, D_X, a0) per seed in both |
| hidden values per seed | (rho, D_X, a0) drawn log-uniformly from the ranges that scan C fixes (2.6), `numpy.random.default_rng([20261111, seed])`, in that order |
| start states | per seed and arm: 16 members formed for 150 ticks under the arm's hidden law, ensemble seed (78, seed) (`gvh.py`); members without a focus cell are dropped; members 0-7 are Lab states, 8-15 test states |
| programs | `gvh.py`'s family: one aimed pulse of 300 nats, sign +-, 2 / 5 / 10 / 20 ticks, onset 0 / 4 / 8, centre 0 / 8 / 16 px off the focus cell in a random direction; drawn from `default_rng(seed)` in `gvh.py`'s order |
| Lab | 16 episodes on the Lab states in turn, ONE hidden-world future each, 32 ticks, the level-1 list at every tick |
| test | 4 programs per test state (32 items if all 8 have cells), 6 replicate truths each; every policy forecasts with a 6-member ensemble (the stand-in: 2.5) |
| horizons | 8, 16, 32 ticks; L is the fair energy score (`vw.scoring.energy_fair`) summed over the three; 4 ticks is reported for comparison with the designer's table and enters no rule |
| scoring scale | per view, horizon and coordinate: SD over the test truths of the seed and arm, floored at a tenth of the median positive SD (`gvh.py`) |
| fitting scale | every recipe is fitted with scales from the Lab outcomes only (`adv_act.py`'s rule). `gvh.py` fitted its gains with the test truths' scale; here they use the Lab's |

### 2.2 Views

- **focus** (primary; every rule below is read on it): `screen.focus_view`, 2 numbers.
- **cell-resolved list** (second view; reported beside, not gating): anchors are the cells of the item's start
  state whose centroid is within 24 px of the focus point, the 4 nearest at most, ordered by distance (the first
  is the focus cell). Per anchor: cell mass and catalyst mass of the cells at the horizon whose centroid is within
  12 px of the anchor's start position and nearer to it than to any other anchor. Missing anchors are zeros:
  8 numbers. The anchors are read from the start state's level-1 list, which the exam's last history frame shows.
  Every recipe is fitted on the Lab's data in the view it is scored in.

### 2.3 Policies (all given the state, as in `gvh.py`)

| policy | what it is |
|---|---|
| pub | the public law from the projected state under the program (P0's law given the state) |
| pub0 | the same, ignoring the program (reported) |
| O | the hidden law at the true values from the full state: leave-one-out over the 6 truths (`energy_loo`) |
| G2, G3 | the designer's gains (`gvh.py`): per-horizon gain on the public response; the gain linear in duration, onset, offset |
| G1, G4 | the designer's ridge on program features and G3 + ridge (reported; not in the rule, which names the gains and A_act) |
| A_act | `adv_act.py` unchanged in substance: its 39-point grid (direct gain, lagged gain, lag time, blur), 2 public futures per Lab episode with common random numbers, least squares on the Lab's view at ticks 1-32; forecast = the public law under the filtered command at the best grid point |
| G* | **the better generic recipe, picked on the Lab episodes**: of G2, G3 and A_act, the one with the lowest leave-one-episode-out score on the Lab: each recipe is refitted without episode i and forecasts episode i (the gains move the 6 public futures of the episode; A_act uses its 2 simulated futures at the grid point chosen without episode i); score = fair energy score of the episode's single hidden future, Lab scale, summed over 8, 16, 32 ticks, mean over the 16 episodes. One pick per seed, arm and view |
| H | told the form (the arm's own: cat = 1 in the main arm, cat = 0 in the control), not the values: fits (lam, rho, D_X, a0). Box: lam in [0.25, 1]; rho, D_X, a0 log-uniform over scan C's ranges widened by a factor 1.5 at each end (D_X capped at 0.5, the stability limit of the explicit step). 48 points of a scrambled Sobol sequence (`scipy.stats.qmc.Sobol(4, seed=1000 + seed)`), then 24 points uniform in the bounding box of the best 6 widened by 10% a side; 3 hidden-law futures per Lab episode and point, common random numbers; least squares on the Lab's view at ticks 1-32, Lab scale; forecast = the hidden law from the full state at the best of the 72 points. No truth lies on this grid: truths are continuous draws, the grid is a quasi-random design that does not see them |

### 2.4 The quantities and the go rule

closed(P) = sum(L(pub) - L(P)) / sum(L(pub) - L(O)), the sums over the test items of all 8 seeds (the three
horizons already summed in L). "Heaviest left out": per seed and arm, the test state with the largest summed
L(pub) - L(O) (focus view, 8-32 ticks) is dropped with all its items; the picks of G* are unchanged.

| condition | number (focus view, pooled over seeds and 8-32 ticks) |
|---|---|
| C1 | closed(G*) <= 0.7, main arm, all start states |
| C2 | closed(G*) <= 0.7, main arm, each seed's heaviest start state left out |
| C3 | closed(G*) >= 0.7, control arm, all start states |
| C4 | closed(H) >= 0.7, main arm, all start states |
| C5 | the stand-in's share s (2.5) >= 0.10, main arm: **reported, marked "depends on A"**, in no verdict here |

**The plan's rule, read literally:** build only if C1, C2, C3 and C4 hold at the point estimate.

**The three-way verdict** (added here, before any run; the plan gives the point rule only). For each condition
the per-seed contrast is formed whose mean is >= 0 exactly when the condition holds (C1, C2: sum over the seed's
items of L(G*) - 0.3 L(pub) - 0.7 L(O); C3, C4: its negative with G* or H), and the mean over the 8 seeds gets a
one-sided 90% bound by Student's t with 7 degrees of freedom. A condition **holds clearly** if its lower bound is
>= 0, **fails clearly** if its upper bound is < 0, and is **close** otherwise.
- **GO**: C1 to C4 all hold clearly.
- **NO-GO**: at least one of C1 to C4 fails clearly.
- **CLOSE CALL**: anything else. The literal point-rule outcome is reported beside it.
A share is read only if its denominator, the mean per-seed sum of L(pub) - L(O), exceeds 2 standard errors over
seeds; otherwise the condition is "not readable" and counts as close.

Reported beside every pooled share: the per-seed shares, their median, the leave-one-seed-out range of the pooled
share, a cluster bootstrap over seeds (2,000 resamples, 5%-95%), and the same per horizon (8, 16, 32; and 4), per
view, with and without the heaviest start state, for G2, G3, A_act, G*, G1, G4, H and pub0. No net is trained in
this stage, so there is no training-seed term; the random numbers of every fit are inside the seed.

### 2.5 The history-only stand-in (after `defect_gliders/surrogate.py`, LLR)

Items per test state: its 4 aimed items, 1 item without input, 1 blind item (`screen.programs`' blind class,
300 nats), 6 truths each. Class weights of the declared mix: none 1/8, blind 1/8, aimed 3/4.
LLR(law), for a test item of state i: training futures are 2 futures under `law` from each OTHER state j of the
seed (Lab and test states alike), under the item's program re-aimed at j's focus cell (same sign, duration,
onset, offset distance and direction, 300 nats; blind: the same program; none: no input). Features of a state,
all from the level-1 list of the history (no micro-state, no future of the item): 1, focus mass and focus
catalyst mass at the start, the change of the focus mass over the last 8 history ticks, the cell mass between 16
and 32 px of the focus. Per horizon a ridge (strength 0.01 x rows, standardised features) from the features to
the focus view; the forecast ensemble is the map at the item's own features plus the training residuals.
P0s = LLR(public law from the projected state), Cs = LLR(hidden law at the true values from the full state),
K = the other states' no-input hidden futures.
s = (L(P0s) - L(Cs)) / (L(K) - L(Cs)) over the weighted mix, pooled over seeds and 8-32 ticks (C5: s >= 0.10).
Also reported: s per class, per seed, per horizon; the state-given gap (L(pub) - L(O)) / (L(K) - L(O)) on the
same items; kept = (L(P0s) - L(Cs)) / (L(pub) - L(O)); the stand-in's skill (L(K) - L(Cs)) / (L(K) - L(O)).

### 2.6 The scans (rules fixed now; their output is `ranges.json`, hashed inside the job before the gate starts)

**Scan V, the hidden parameter set** (public law, 64 px, 8 members, ensemble seed (79, 1)). Candidates: the 13
law parameters of `membrane_jax.THETA` (the four initial-noise parameters are not candidates). Each at 0.8, 0.9,
1.1, 1.2 times its default; formation 150 ticks at that value.
- A member is viable if all fields are finite, it has 2 to 15 cells and an inside-phase area of 2% to 50% of the
  box at the end of formation and after 32 more ticks without input, and a focus cell. A value is viable if at
  least 6 of 8 members are.
- Box of a parameter: on each side the outermost scanned factor such that it and the factor inside it are
  viable; no box if a 10% step is not viable on either side.
- Headroom of a value: from each viable member's state, an item without input and an aimed pulse (300 nats, 10
  ticks, on the focus cell, + for even members, - for odd), 4 truths at the value and 4 futures of the
  default-parameter law from the same state; (L(plug) - L(O)) / (L(K) - L(O)), focus view, 8-32 ticks, K = the
  other members' no-input truths. Headroom of a parameter: the smaller of its two box edges' values.
- Families: transport (DS, DK, DL, Dp), phase (r, a, th), metabolism (F, c, b), decay (dK, dL), link (chi).
  Eligible: has a box and headroom >= 0.02. Within a family the eligible parameter with the largest headroom;
  **the hidden set is that parameter of the 4 families with the largest headroom** (fewer if fewer are
  eligible), each uniform on its box.

**Scan C, the ranges of rho, D_X, a0** (hidden law, lam = 1, cat = 1, 64 px, 16 members, ensemble seed (77, 2),
6 truths, the four classes of `screen.py` at 300 nats, its screen gap in the focus view over 8-32 ticks).
One at a time about the pilot centre (0.02, 0.5, 0.03): a0 in 0.02, 0.025, 0.03, 0.04, 0.05; rho in 0.005, 0.01,
0.02, 0.04, 0.08; D_X in 0.05, 0.1, 0.2, 0.35, 0.5 (0.5 is the stability limit of the 5-point explicit step at
dt = 0.5; nothing above it is scanned or drawn).
- A value is admissible if it is silent (gap without input <= 0.03 and under blind input <= 0.05), effective
  (gap pooled over the two aimed classes >= 0.10) and at least 14 of 16 members have a focus cell.
- Range of a parameter: from the smallest to the largest value of the longest run of consecutive admissible
  scanned values that contains the pilot centre. If the centre is not admissible, the range is the centre alone
  and the scan is recorded as failed for that parameter; the gate still runs.

`ranges.json` holds the hidden set with its boxes and the three ranges; its SHA-256 is written to
`ranges.sha256` and to stdout before the first gate run starts, every gate process checks it, and both files are
committed here from the job's output.

### 2.7 Job

One job, `r6-dialsB-001`: CPU_NODE, 16 vCPU / 64 GB, max_hours 3.5, cap $2.50. Presmoke (every stage once at
full array shapes with short counts; non-zero exit within minutes on failure), speed guard (the measured
member-tick rate must project the whole job inside 2.5 hours, else exit 3), deadline inside the script. One more
job (cap <= $2.50) only if the first fails for a reason that is not a result; job ids are never reused.
