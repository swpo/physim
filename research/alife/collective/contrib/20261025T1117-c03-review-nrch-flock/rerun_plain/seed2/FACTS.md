# Evidence pack: nrch (seed 2)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0938-c08-nrch-ambplus-flock/world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 670s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0938-c08-nrch-ambplus-flock/world.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/nrch/plain/seed2 --seeds 2 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-1.0437, 1.0612], min area 6 px

## Measurements
- components: final 6, mean 5.7, max 12; occupancy final 0.22
- tracks: 41; persistent (alive >= 50% of run): 3; longest 91 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.176/time; max body lengths 21.6
- replication (lineage window K = 20 frames = time 1000, default): splits 6, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio 1, nucleations 24
- channel total drift (end/start - 1): [0.0, -108.7143]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 76: holes 0, rim-vs-core 0.21, rim-vs-outside 0.54, heterogeneity 0.18; core [0.956, 0.385] rim [0.751, 0.357]
  - track 24 at frame 77: holes 0, rim-vs-core 0.22, rim-vs-outside 0.50, heterogeneity 0.18; core [0.943, 0.43] rim [0.72, 0.416]
  - track 26 at frame 77: holes 0, rim-vs-core 0.17, rim-vs-outside 0.49, heterogeneity 0.17; core [0.921, 0.368] rim [0.754, 0.378]
  - track 38 at frame 93: holes 0, rim-vs-core 0.25, rim-vs-outside 0.42, heterogeneity 0.19; core [0.928, 0.419] rim [0.682, 0.414]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 34 components >= 12 px at frames [40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.853, rim/outside 7.21 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.808)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.21, rim/outside 0.985 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.556)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #16 (t=3800, R_eq 23.06): none; #24 (t=3850, R_eq 20.22): none; #26 (t=3850, R_eq 14.65): none; #38 (t=4650, R_eq 17.96): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 34 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
