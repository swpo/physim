# Evidence pack: nrch (seed 4)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0840-c08-nrch-swimmers/world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 651s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0840-c08-nrch-swimmers/world.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev6/recip --seeds 4 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.49 of robust range [-1.3435, 1.4243], min area 6 px

## Measurements
- components: final 21, mean 32.2, max 68; occupancy final 0.30
- tracks: 79; persistent (alive >= 50% of run): 30; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.25 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 21, 21], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 1000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 11, merge/split ratio n/a, nucleations 68
- channel total drift (end/start - 1): [0.0, 641.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 0, rim-vs-core 0.34, rim-vs-outside 0.72, heterogeneity 0.15; core [0.983, 0.021] rim [0.744, 0.255]
  - track 4 at frame 61: holes 0, rim-vs-core 0.35, rim-vs-outside 0.72, heterogeneity 0.14; core [0.983, 0.041] rim [0.736, 0.284]
  - track 9 at frame 61: holes 0, rim-vs-core 0.34, rim-vs-outside 0.72, heterogeneity 0.15; core [0.983, 0.026] rim [0.742, 0.26]
  - track 10 at frame 61: holes 0, rim-vs-core 0.33, rim-vs-outside 0.72, heterogeneity 0.15; core [0.983, 0.027] rim [0.743, 0.26]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 175 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.953, rim/outside 11.3 (aggregate of 175 individuals; 0/175 membrane-like individually; rim level 0.949)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 41.2, rim/outside 0.981 (aggregate of 175 individuals; 0/175 membrane-like individually; rim level 0.882)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3050, R_eq 10.36): none; #4 (t=3050, R_eq 13.4): none; #9 (t=3050, R_eq 11.38): none; #10 (t=3050, R_eq 11.55): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
