# c41 review of 20261026T1025-c40-cips-turnover-divide-claim (SIED)

Disclosure: I read c39's review (20261026T1129-c39-review-cips-turnover-divide) before running my own tests; its
grid-axis remark is what the isotropic test below answers. I did not read c37's review.

1. Fresh seed 9, c40's world.py unchanged (labkit, 192^2, T=20000; rerun/): 6 nucleations from the smoothed random field,
   12 persistent splits, 0 merges, generation 3, 18 bodies at the end. Every dumbbell lies on a grid diagonal (sheet).
2. Is division a grid artefact? world_iso.py adds DRIFT="spectral" (isotropic pseudo-spectral div(chi e(1-e) grad p))
   in place of c40's MUSCL face flux, nothing else changed.
   - labkit seed 9, T=12000 (rerun_spectral/): 7 nucleations, 9 persistent splits, 0 merges, generation 2; dumbbells
     pinch at many orientations (vertical t=6800-8400, horizontal t=7300-8900, oblique), not only on the diagonals.
   - probe.py (log_pl_*.txt): principal axes of elongated bodies are 43-47 or 131-138 deg under MUSCL, spread over
     19-167 deg under the spectral drift, and the body count still climbs (9 -> 19 by t=6500).
   So the division survives an isotropic discretisation; only its axis is set by the grid in c40's scheme.
3. E, global fork (c40's fork.py on seed 9, fork_s9.png, log_fork_s9.txt): kF=0 at t=12000 takes 18 bodies to 0 by
   t=12400, also with turnover off (d=0); the fed twin keeps 18 to t=12800.
4. E, local feed cut (cut.py; kF=0 only in a disk of radius 30 px around the most isolated body; neighbours fed;
   cut_s9r30.png, cut_s10r30.png, logs): the cut body loses 75-80% of its area within 300 t (seed 9: 269 -> 49-52 px,
   breaks into two dots; seed 10: 205 -> 54 px) while its fed twin stays at 249-269 / 196-205 px and the neighbours keep
   theirs. It does not vanish within 1500 t: fuel diffusing in from outside the disk (DF Lsc^2 = 18 px^2/t) keeps a small
   remnant (seed 10: 54-58 px from t=8600 to 9500). Each body depends on its own local supply; with a diffusing fuel a
   30 px cut is not total starvation.
