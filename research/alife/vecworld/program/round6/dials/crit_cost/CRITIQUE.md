# Cost and feasibility critique of the dial designs (round 6, `crit_cost`)

11 Nov 2026. `recompute.py` gives `results/recompute.json` (`R`; each entry names its source);
`net_cpu_cost.py`, one CPU timing, gives `results/net_cpu_cost.json` (`N`). "Estimate" marks what is not
measured. The designers' member-tick sums hold; rates, budgets and build time change.

## 1. Money and memory

A100 40GB at $1.99/h; cap = rate x (max_hours + 0.25) + $0.10 at my upper hours (`R`
`caps_by_rule_A100_40GB_at_upper_hours`).

| job | member-ticks | hours | dollars (designer) | cap, rule/declared |
|---|---|---|---|---|
| defect_gliders, stage 1 | 1.41-1.67 million | 0.65-1.2 | 1.3-2.4 (1.5) | 3.0/5 |
| defect_gliders, stage 2 | 1.9-2.2 million | 1.1-1.8 | 2.1-3.7 (3.5) | 4.3/15 |
| sublevel_second | 7.72 million | 1.9-2.8 | 3.8-5.5 (5-11) | 6.1/20 |
| compute_limit, stop rule | 0.74 million (64 px), 2.95 million (32 px) | 0.8-2.4 | 1.7-4.8 (2.5) | 5.4/5 |
| compute_limit, full | 1.6 million exam equivalents | 2.9-5.0 | 5.8-9.9 (5-7) | 10.5/12 |

- **Gliders.** The ladder's harness ran at 1,312 member-ticks/s on this card ($0.42 per million; $0.70 billed
  with nets), not 2.6 times below the 80 GB rate; bias2 and the cards job measured 617-734 (`R`
  `rates_member_ticks_per_s`). Stage 1's $5 cap gives an H200 0.48 h; it needs 0.5-0.7 (estimate): A100
  only, or cap $6.8.
- **Membrane.** The cards job measured 7,091 member-ticks/s at 128 px with the tracker (two 6-second runs);
  the designer's 598-2,717 is a batch of 64 with fields copied to the host. Simulation costs $0.6-1.3, not
  $1.6-7.1. Nets are the bill (1.5-2 h, the designer's estimate; no membrane net exists). "Stage 1, about
  $1" needs both training families: $1.3-2.2 (estimate).
- **Vortices.** At 64 px this card has one measurement, the cards job's 209/s (530-600 if the 128 px card ratio
  holds, estimate). The 32 px rate, 80% of the stop-rule job's member-ticks, is measured nowhere. At 209/s the
  rule gives $5.41, above its $5; an H200 gives $5.32. The full study's new zero arm costs $3.4.
- **Memory.** Simulation states are safe: largest arrays 2-7 x 10^7 elements, 1-3% of 2^31. Net validation
  memory is unchecked. defect_gliders can reuse `round5/ladder/check_shapes.py`; sublevel_second has no net,
  and its leave-one-episode-out fine-tuning is 10,440 trainings (`R` `sublevel_second.fine_tuning_F`). Each
  job should first run its full-shape validation pass on the GPU, with the platform allocator (round 5 lost
  slots-007 to fragmentation).

## 2. Decision 2: the two numbers

The port limits the predictor's CPU seconds per item; the agent's box has cpus, memory and time limits, and
its CPU use is "not studied" (`R` `enforcement_in_the_port`). So f is enforceable per item; R is a ceiling
(cpus x hours), never measured.

- **defect_gliders** (R 8,192 episodes, 28-31 core-hours; f 0.05). "8 times P0's set" is round 4's 1,024
  episodes; this design's P0 uses 6,144 and H needs 12,288: H does not fit. A question has no member count; at
  32 members f is 3.8 CPU-s per item.
- **sublevel_second** (R 8,192 episodes, 5.5 core-hours; f 0.1). Simulation fits (H 6,144). An episode costs
  2.4 CPU-s, so one net of the ladder's size (0.98 CPU-s per step, `N`) is 2,400 episode equivalents
  (estimate): R rations training, not simulation. f is 1.3 CPU-s per item; the port's item box alone uses 1.0.
- **compute_limit** (R 64 exam episodes, 3.8 core-hours; f 0.05, or 6.8-27 CPU-s per item, enforceable; a
  third number, r). The Lab can enforce r; the agent's box cannot, and R = 64 pays for 64 exam-size episodes.
  The pooled designs (256 exam equivalents) are 4 and 16 times R.

On gliders a 6,000-step conditioned net costs 476 episode equivalents (`N`): training fits. Each
design should report every reference policy's simulation and training CPU in episode equivalents, define a
question as members x ticks, and state f per exam where it is under 5 CPU-s per item.

## 3. What must be built (agent-hours, estimates)

Calibration, first to last commit: `round5/ladder` 4.1 h, `round5/vortexexam` (a new exam) 6.3 h (`R`
`build_time`).

- **defect_gliders:** stage 1, 4-5 h: a law switch around `ladder_lib`, the true-form
  family, fine-tuning and the residual on nets. Stage 2, 3-4 h more: H.
- **sublevel_second:** 10-14 h. No membrane exam exists: hidden set, viability scan, mix, focus view, net
  family, inference in 17 dimensions, R, F, H, H_mix, the control arm, and its risk table's three CPU tests.
- **compute_limit:** 3-4 h: pooling of the 14 level-1 summaries, pooled designs, re-scoring. Pilot B's design
  series are stored in `design_S_00/01.npz`, not `design.npz`, and suffice.

## 4. Verdict

- **defect_gliders:** two jobs, as declared. Stage 1 fits one and is the cheapest decisive test (about
  $2, 4-5 h); the statistician's eight truths and three seeds still fit $5. Cut first: N = 2, then stage 2's
  eta 1 and 2.
- **sublevel_second:** two jobs, not one: stage 1 (cap $2.9), then the rest (cap $7.6). Cut first:
  the arms 0.5 and 0.75 (28% of member-ticks), the state-given screen (19%) outside lam = 1 and the control,
  fine-tuning at budget 64. One $20 job leaves no rerun.
- **compute_limit:** one job, if its cap rises to $6 or the 32 px design halves, and it measures both rates
  first. The full study should reuse pilot B's truths as its zero arm. r needs a ruling first.
- Money does not bind: $4-10 for the three first jobs. Agent-hours and the unmetered R do.
