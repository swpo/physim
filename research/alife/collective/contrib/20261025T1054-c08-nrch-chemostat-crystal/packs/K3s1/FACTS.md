# Evidence pack: nrch (seed 1)

- world: `../../w/nrch.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 241 frames x 500 steps x dt 0.05 = time 6000; grid [192, 192]; wall 706s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/nrch.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/K3s1 --seeds 1 --frames 240 --spf 500 --lineage-k 40 --no-movie`
- segmentation: matter > 0.51 of robust range [-0.9477, 0.9238], min area 6 px

## Measurements
- components: final 17, mean 16.2, max 24; occupancy final 0.18
- tracks: 110; persistent (alive >= 50% of run): 9; longest 205 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 22.68 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 32 long-lived tracks moved >= 1 body length; max speed 0.29/time; max body lengths 62.4
- replication (lineage window K = 40 frames = time 1000, --lineage-k): splits 15, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 11, merge/split ratio 0.733, nucleations 69
- channel total drift (end/start - 1): [-0.0653, -16.6552]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 45 at frame 135: holes 0, rim-vs-core 0.27, rim-vs-outside 0.36, heterogeneity 0.20; core [0.92, 0.307] rim [0.664, 0.406]
  - track 3 at frame 121: holes 0, rim-vs-core 0.30, rim-vs-outside 0.26, heterogeneity 0.19; core [0.894, 0.284] rim [0.619, 0.398]
  - track 61 at frame 145: holes 0, rim-vs-core 0.25, rim-vs-outside 0.35, heterogeneity 0.20; core [0.911, 0.349] rim [0.666, 0.419]
  - track 55 at frame 119: holes 0, rim-vs-core 0.26, rim-vs-outside 0.36, heterogeneity 0.20; core [0.931, 0.381] rim [0.673, 0.42]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 107 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 6.91 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.768)
  - radial psi: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.47, rim/outside 0.944 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.551)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #45 (t=3375, R_eq 10.87): none; #3 (t=3025, R_eq 9.93): none; #61 (t=3625, R_eq 12.84): none; #55 (t=2975, R_eq 10.66): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 107 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
