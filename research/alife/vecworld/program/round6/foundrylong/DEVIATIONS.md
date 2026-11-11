# foundrylong: deviations from DECLARED.md and dated addenda

Nothing yet. Every change of a size, a policy or a rule after `DECLARED.md` was committed is listed here with its
date, what had been seen by then, and why. The declaration itself is never edited.

## Addendum 1, 11 Nov 2026, before request r6-foundrylong-001 (nothing of the study had run on a GPU; seen: CPU smoke runs at tiny size)

Details the declaration left open, fixed now. No criterion, threshold, policy or size of `DECLARED.md` changes.

1. FT(N) starts, for all three horizons, from the P0(1,000) parameters that were best at 16 ticks (the declared
   horizon). At 8 and 32 ticks "0 steps" is therefore that checkpoint, not P0's own best for the horizon; the null
   still contains P0 itself at every horizon.
2. Held-out rows: at most 1,024 per horizon per net, scored with 8 draws. Fold of a Lab episode in the
   cross-validation: its index modulo 4.
3. Every C(n) trains in two groups of 8 hidden worlds (the 2^31 rule needs it only at 16,384 episodes).
4. The screen runs in chunks of 128 draws (round 5's size, on larger cards); if that does not fit on the 40 GB card,
   `job2.run_arm` halves the chunk and the full pass starts from the chunk that fitted in the presmoke.
5. The new prior worlds' gate uses simulation seed 102 (the pilot's gate used 101 on its pool); training simulations
   of the prior worlds use seed 2000 (the pilot's 1000), so no simulated episode repeats one of the pilot's.
6. Job limits: job.sh stops new work at 2.9 h (declared 2.75), max_hours 3.15 (declared 3.0): the presmoke at full
   shapes is estimated at 15 minutes, which the declared figure did not include. Expected bill about $5.3.
7. The pre-screen selected 15,040 of the 160,000 pool draws (9.40%; the seed-2027 arm: 9.375%); all are screened.
8. items.npz holds the items' histories and test programs only; replicate futures stay on the machine, as in the
   pilot. The parameters of P0(1,000) (3 seeds) and of C(16,384) seed 0 are written, for stage 2.

## Addendum 2, 11 Nov 2026 18:55 UTC, while r6-foundrylong-001 runs (seen: the Mac's review; no result of the job)

The review (`origin/gpu-jobs:jobs/r6-foundrylong-001/review.md`: fine to run, 0 blocker, 0 major, 2 minor):
1. The outputs are about 53 MB against the 50 MB git cap, so 3-4 MB may stay on the Mac (`in_git: false`). Before the
   analysis the manifest is checked for scores.npz, train_info.json, info.json and the parameter files; a missing file is
   asked for. A stage-2 job writes parameters as float16 or omits histories.
2. `make_summary.py` now marks S1 with the list `incomplete` (a declared null candidate or seed missing, a net cut by
   the deadline, P0 below 1,000 worlds) and reads S1a as "incomplete" unless P0x2, the second P0 size and the second
   C size are present and not cut. The declared rule is unchanged; the marks say when its inputs were not all there.

## Addendum 3, 11 Nov 2026 21:10 UTC, before request r6-foundrylong-002 (seen: ALL of stage 1, results/analysis_stage1.json; the CPU tests of W in PROGRESS.md)

Stage 1 says S1 SURVIVES (sigma(16, 32) = 0.218, lower bound 0.187, min over leave-one-out 0.178), so stage 2 runs.
The declared criteria T1-T6 and their thresholds are unchanged. Fixed now:

1. **Deviation: W's fit loss.** The declaration says the fit loss is "the fair energy score of the ensemble's short
   forecasts against the next observed frames". On CPU (public world seed2027-46, before any stage-1 result) a fit on
   one-tick forecasts reached the truth's loss level from a 30% neighbour while W's skill at the fit fell to 0.24 at
   16 ticks (0.78 at the true weights): the one-tick loss does not pin what matters at 8 to 32 ticks. The fit loss is
   therefore the exam's own score at 16 ticks on the Lab: from the assimilated ensemble at an anchor tick a, a free
   16-tick forecast under the episode's commands, fair energy score against the observed frame a + 16 (gradient through
   the 16 forecast ticks, recomputed in the backward pass; not through the assimilation). On CPU this fit took W from
   0.37 to 0.68 at 16 ticks from a 30% start in 40 steps on 8 episodes. (The first CPU fits also used a wrong fair score,
   spread term doubled; fixed before these numbers.)
2. **W, sizes.** N = 32 Lab episodes only (every criterion is at N = 32; N = 8 is not run in stage 2). Starts: the
   weights of the first 32 of the pilot's 210 screened training worlds, scored by the fit loss on 8 Lab episodes (4
   members, anchors 0, 8, 16, 24, 32); the best 4 are refined: Adam, 200 steps, rate 0.03 then 0.01 for the last
   quarter; each step 8 random episodes x 4 members x 2 random anchors; noise keys fixed per episode; members drawn
   from a pool of 16 spun at the current weights (burn-in 300), renewed every 50 steps. Coordinates: fl_w.to_z (net
   weights in prior SD units; scalars as positions in their prior ranges, kappa from 1e-6). dens is not fitted (the
   nudge makes the loss independent of it): it is the Lab's observed mean mass per kind. Two fits per world and Lab
   ("seeds" for the bootstrap): seed 0 is the better of starts 1 and 3, seed 1 of starts 2 and 4, by the fit loss on
   all 32 episodes. Prediction: 24 members spun at the fitted weights, held to the item's 17 frames, then simulated
   under its program. W(true) and W(prior): the same predictor at the true weights and at the plugPrior world's.
3. **W+**: seed 0's fitted weights; 4,096 mix episodes; the C recipe at 4,096 episodes (8,000 steps, batch 128, the
   training rule), one net per world and Lab.
4. **Designed Lab**: the declared rule (fl_w.designed_prog): 12.5 nats in every one of the 32 test ticks (400 per
   episode), aimed on the densest block of the last revealed frame at even ticks, regional on its 3 x 3 blocks at odd
   ticks, direction 2 pi (e mod 8) / 8. Paired: designed episode e starts from the same state with the same free-tick
   noise as mix episode e (same secret and labels), so the two Labs differ only in their programs.
5. **G\* on each Lab**: P0(1,000) (stage 1's 3 seeds, scored again), FT(32), D(32), Dr(32), picked on the unscored half
   separately for each Lab. FT's rate grid becomes {1.25e-5, 5e-5, 2e-4} (declared {5e-5, 2e-4, 8e-4}): in stage 1 the
   cross-validation chose the grid's lowest rate in 122 of 144 (world, seed, horizon) cases at N = 32 and 8e-4 once, so
   the declared grid did not bracket the optimum; a tuned null needs the lower rate. C is stage 1's C(16,384) seed 0
   (one seed in stage 2).
6. **Reading of T2-T4, T6** (make_summary2.py): T2 "pass" if the 90th percentile of rho_G is <= 0.7, "fail" if the
   10th is > 0.7; W* and G* are picked separately on each Lab for T4; T6 uses the point estimates of T1 and T3 at 8 and
   32 ticks and at 16 ticks with each world left out (T3 recomputed with the picks redone).
7. **Job**: job_s2.sh: presmoke (2 worlds, every stage, the full fit shapes; a speed guard after W on the mix Lab exits
   4 if the projection exceeds 1.25 x the time left), then the full pass; order: data, stage-1 nets, W mix, W(true),
   W(prior), FT mix, D mix, W designed, FT designed, D designed, W+ mix, W+ designed. Stage 1's public parameters are
   copied to inputs/stage1/ (P0(1,000) 3 seeds, C(16,384) seed 0, worlds.json). No platform allocator (the W fit
   dispatches one step at a time). Expected about 2.2 h, about $4.5; cap $8.10.

## Addendum 4, 11 Nov 2026 21:30 UTC, before request r6-foundrylong-003 (seen: job 002's presmoke log, 2 worlds)

Job r6-foundrylong-002 stopped itself at its presmoke speed guard after 1.6 min (exit 4; $0.10 billed): the guard
divided the wall time of 10 fit steps, JIT compilation included, by the steps, and projected 4.9 h. Seen in its log
(2 hidden worlds, presmoke sizes, not a result): skills at 16 ticks C 0.745, P0 0.533, ridge 0.43, W after 10 Adam
steps 0.25. Changes, for job 003 (the study's last):

1. `fl_w.fit_batch` times the first step (compilation) apart from the steady steps; the guard uses the steady time.
2. **A size now set by the measured speed**: W's Adam steps in the full pass are the largest number, at most the
   declared 200, that fits the time left after every other part (projected from stage 1's timings and the presmoke's)
   with a 10% margin; the presmoke exits 4 if fewer than 80 fit. The number is written to the presmoke's
   shape_test.json and passed to the full pass; it is reported with the results. Nothing else changes.
