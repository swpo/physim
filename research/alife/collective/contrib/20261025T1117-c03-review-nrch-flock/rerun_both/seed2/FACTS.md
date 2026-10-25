# Evidence pack: nrch (seed 2)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0938-c08-nrch-ambplus-flock/world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 998s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0938-c08-nrch-ambplus-flock/world.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/nrch/A3/seed2 --seeds 2 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.49 of robust range [-1.0504, 1.0767], min area 6 px

## Measurements
- components: final 15, mean 11.4, max 20; occupancy final 0.20
- tracks: 293; persistent (alive >= 50% of run): 1; longest 66 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.34 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.264/time; max body lengths 35.0
- replication (lineage window K = 20 frames = time 1000, default): splits 53, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 26, merge/split ratio 0.491, nucleations 173
- channel total drift (end/start - 1): [-0.0913, -35.5714]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 123 at frame 88: holes 0, rim-vs-core 0.21, rim-vs-outside 0.49, heterogeneity 0.19; core [0.952, 0.449] rim [0.751, 0.379]
  - track 171 at frame 92: holes 0, rim-vs-core 0.25, rim-vs-outside 0.46, heterogeneity 0.19; core [0.943, 0.436] rim [0.693, 0.414]
  - track 199 at frame 97: holes 0, rim-vs-core 0.27, rim-vs-outside 0.41, heterogeneity 0.18; core [0.933, 0.306] rim [0.672, 0.38]
  - track 204 at frame 95: holes 0, rim-vs-core 0.27, rim-vs-outside 0.40, heterogeneity 0.19; core [0.937, 0.374] rim [0.672, 0.403]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 79 components >= 12 px at frames [40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.864, rim/outside 9.2 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.839)
  - radial psi: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.42, rim/outside 1 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.604)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #123 (t=4400, R_eq 12.48): none; #171 (t=4600, R_eq 15.7): none; #199 (t=4850, R_eq 11.4): none; #204 (t=4750, R_eq 13.22): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
