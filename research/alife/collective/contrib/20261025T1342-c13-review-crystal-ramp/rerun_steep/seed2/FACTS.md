# Evidence pack: nrch (seed 2)

- world: `../../world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 182 frames x 1000 steps x dt 0.05 = time 9050; grid [192, 192]; wall 1002s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1342-c13-review-crystal-ramp/world.py --out collective/contrib/20261025T1342-c13-review-crystal-ramp/rerun_steep/seed2 --seeds 2 --spf 1000 --frames 181 --no-movie`
- segmentation: matter > 0.49 of robust range [-0.9166, 0.9679], min area 6 px

## Measurements
- components: final 24, mean 22.9, max 36; occupancy final 0.36
- tracks: 448; persistent (alive >= 50% of run): 15; longest 166 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.35 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 24, 24], H1 [0, 0, 0]
- motion: 44 long-lived tracks moved >= 1 body length; max speed 0.27/time; max body lengths 103.7
- replication (lineage window K = 20 frames = time 1000, default): splits 10, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 3, merge/split ratio 0.3, nucleations 425
- channel total drift (end/start - 1): [0.5191, 0.5714]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 200 at frame 99: holes 0, rim-vs-core 0.27, rim-vs-outside 0.36, heterogeneity 0.20; core [0.912, 0.38] rim [0.647, 0.398]
  - track 282 at frame 105: holes 0, rim-vs-core 0.27, rim-vs-outside 0.35, heterogeneity 0.20; core [0.917, 0.425] rim [0.65, 0.415]
  - track 323 at frame 110: holes 0, rim-vs-core 0.27, rim-vs-outside 0.36, heterogeneity 0.20; core [0.923, 0.42] rim [0.648, 0.412]
  - track 445 at frame 146: holes 0, rim-vs-core 0.28, rim-vs-outside 0.36, heterogeneity 0.20; core [0.923, 0.43] rim [0.647, 0.412]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 137 components >= 12 px at frames [30, 61, 91, 120, 151, 181]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.834, rim/outside 5.04 (aggregate of 137 individuals; 0/137 membrane-like individually; rim level 0.793)
  - radial psi: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.16, rim/outside 0.97 (aggregate of 137 individuals; 0/137 membrane-like individually; rim level 0.567)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #200 (t=4950, R_eq 12.33): none; #282 (t=5250, R_eq 12.85): none; #323 (t=5500, R_eq 12.55): none; #445 (t=7300, R_eq 13.17): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 137 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
