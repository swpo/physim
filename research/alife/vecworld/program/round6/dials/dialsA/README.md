# Round 6, dials, study A: the gliders calibration

**Status: the job is requested, no result yet.** This file describes the study as built; the results sections
are filled in when `r6-dialsa-002` ends. What is declared is in `DECLARED.md` (committed before any run).

**Question.** The public law of the gliders wind world lacks one term: where the wind exceeds a threshold,
channel 0 turns into channel 1 (`../defect_gliders/dlaw.py`, term XW; eta = 4, threshold 0.12, ramp 0.05). Does a
generic repair with no idea of what is wrong close the gap between P0 (a net trained on simulations of the
public prior) and C (a net trained on the true form at the truth)? The repairs are FT(N), P0's net fine-tuned on
N Lab episodes, and RES(N), P0 plus a per-block residual fitted on N Lab episodes. The designer's CPU stand-in
says one or two episodes per class close 0.70 to 1.46 of the gap.

PILOT ONLY. The truths are round 5's public pilot truths. Truths, Lab data, items and nets of this study must
never be reused as an exam. A has no pass bar: whatever it finds, it cannot record an exam as passing.

## How it is built

| piece | file | what it does |
|---|---|---|
| law switch | `xlaw.py` | `dlaw.tick` behind `gworld.tick`'s signature; the strength eta rides in the parameters as a traced scalar, so one compiled program runs eta = 0 and 4 and the public law is the same program at 0. The world for Lab and exams, the batched simulator and the family simulator are round 5's with this tick |
| zero point of the switch | `check_a.py`, `results/check_a.json` | on CPU one tick, a family of 8 members x 10 ticks and a Lab batch are bitwise equal to round 5's code at eta = 0; at eta = 4 only the aimed and regional episodes differ |
| families | `run_a.py` | public: 768 points x 8 mix episodes with round 5's simulator. True-form: 768 points x 8, eta = 0 at 384 points and 4 at 384; the net is conditioned on (theta, eta / 4) |
| fine-tuning | `a_nets.py` | lockstep fine-tunes (16 at a time), constant rate 1e-4, steps by 4-fold cross-validation over episodes on a 40-step grid that includes 0; folds stratified by the Lab program class |
| residual | `a_nets.py` | the designer's `res_scores` on P0's predictive mean: per program class, horizon and region class a ridge from a block's three numbers to the residual of its three numbers |
| criteria | `a_stats.py`, `make_summary.py` | every declared criterion from the per-item scores; truths as clusters plus the training-seed term |
| job | `job.sh`, `run_a.py` | presmoke at full shapes in the same process, a speed guard, then the full pass |

Each world (truth x eta) has a Lab of 32 mix and 32 input-free episodes and two exams of 48 items x 12
replicates: `sel`, on which every pick is made, and `score`, on which every reported number is computed.

## Files

| file | content |
|---|---|
| `DECLARED.md` | the plan's sizes, policies, criteria and thresholds for A, and the readings fixed before any run |
| `DEVIATIONS.md` | what was done differently, written at the time |
| `PROGRESS.md` | the log |
| `results/check_a.json` | CPU checks of the law switch and of the residual |
| `results/summary.json` | every number with its source (after the job) |
