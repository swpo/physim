# World cards: deviations from HYPOTHESES.md and gates.py as first committed

HYPOTHESES.md is as it stood when the first GPU request was made (commit d27c3c6ba, 11 Nov 2026, 11:42 UTC). It is
not edited after that. gates.py as declared is at the same commit (`git show d27c3c6ba:<path>/gates.py`); its
thresholds (`TH`) have not changed. Everything that differs from those two files is listed here, with when it was
decided and what had been seen by then.

## A. After the runner's code review of r6-cards-001, before any result was read

The review (`origin/gpu-jobs:jobs/r6-cards-001/review.md`, copy in `results/jobs/r6-cards-001/`) arrived at
12:06 UTC while the job ran. These changes were committed at 12:12 UTC (320ce1a22). The first result lines of the
job (its heartbeat) were read at 12:13 UTC; the cards were fetched at 12:26 UTC. Seen before that: CPU cards of
foundry draw 4470 at full size and of membrane and vortices at small size (run with the uncorrected estimators).

1. **Tick share (review item 1).** The level's tick share is the mean of the per-channel shares. The first version
   pooled the channels before the covariance, which reads about s / d^2 when one of d channels carries the tick
   function: at the population level even a pure clock would have passed the 0.1 bar, and H6 would have been
   refuted by construction. The per-channel shares are in every card of the first job, so its cards are re-derived
   offline by `gates.derive`; `check_cardlib.py` has a world with one trending channel. Effect: the `stationary`
   gate and H6 use the corrected value everywhere in the results.
2. **Response difference (item 2).** The estimator subtracted var(d) + var(d') although the two responses share
   their noise, which biases it low. Corrected to the variance of the per-replica difference. It cannot be
   recomputed from the first job's cards: for gliders, vortices and membrane the first job's value is a lower
   bound, and the second job reruns their run A. For foundry worlds the neighbour is an independent weight draw
   and the bias is near zero. H2 is judged on corrected values only.
3. **Non-finite runs (item 4)** get the verdict "invalid" and are left out of the tables. No run was non-finite.
4. **Diffusion controls (item 5).** `ctl_diffusion_0/1` of the first job keep the mobility gain: they are
   no-affinity worlds, not round 5's diffusion controls. They stay in the tables under their name and are not
   counted in the card's own test. The second job runs two true diffusion controls (`ctl_puredif_0/1`), which are.
5. **Size check (item 6).** Body counts and events are compared per area, the action entries are left out, and
   the 128-px vortex world is rerun with 8-px blocks (`vortex128g16`).
6. The reviewer notes that the pure-noise field and the diffusion worlds are dull almost by construction: they
   test the plumbing. The controls that could have failed are the frozen draws and the free bodies.

## B. Second job (`worlds2.json`), declared before its runs

Written after CPU runs at small size of membrane and vortices at their real parameters, and before any card of
either job was read (commit c2eb0af2b, 12:00 UTC; extended in 320ce1a22):
- the same worlds on a slower clock (4 world ticks per card tick): round 5 studied the membrane world at 40 time
  units per tick, and a cell cycle is about 1,850 time units, beyond the 320 the first card reaches;
- gliders with round 5's 1- and 8-parameter hidden sets: with the 4-parameter card, six cells whose science share
  round 5 measured, for a rank test of H1.

## C. After the first job's cards were read

1. **Block-level verdict.** The declared verdict takes the larger sigma_hat of the block view and the population
   level. The population level's ceiling turned out not to be robust (it agrees between run seeds in 60% of the
   worlds and between sizes in 25%), so the tables also give sigma_hat at the block level alone, and the README
   says which verdicts rest on the population level only. The declared verdict is reported unchanged.
2. **Action reach in units of the cheap family's error** (`act_ms_over_vcheap`, added to `gates.derive` after the
   first full-size card, no gate). The declared actions gate (predictable shift of an aimed 200-nat input of at
   least 0.1 oracle variances) passes in every world, the uniform controls included: it does not discriminate.
3. **Figures** are palette-quantised (about a third of the bytes).

## D. After the runner's review of r6-cards-002 (read at 12:47 UTC, before that job's results)

1. **Slow-clock late windows are not counted** (review item 1). On the 4-tick clock the late window shares 62% to
   75% of its ticks with run A's (same seed, same trajectory), so "late = early" there is largely a self-comparison.
   `make_cards.py` reports the overlap and leaves those worlds out of the late-window counts.
2. **Seed check and the response difference** (item 2). Where run A comes from the second job (corrected estimator)
   and run B from the first (biased), the response difference is left out of the seed comparison.
3. **Units on the slower clock** (note). The structure gate's thresholds are in card ticks; a half-life of 51 world
   ticks reads as 13 card ticks at 4 world ticks per card tick. The README compares clocks in world ticks and says
   where a gate changes for that reason alone.
4. Not changed: a presmoke failure of the 128-px size check would have ended the second job (item 3); the
   non-finite flag covers the main run, not the branches (note).
