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
