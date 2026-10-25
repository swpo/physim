# Evidence pack: nrch (seed 3)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0938-c08-nrch-ambplus-flock/world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 1693s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0938-c08-nrch-ambplus-flock/world.py --out collective/contrib/20261025T1118-c02-review-c08-nrch-flock/both/seed3 --seeds 3 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.49 of robust range [-1.0501, 1.0764], min area 6 px

## Measurements
- components: final 16, mean 11.9, max 19; occupancy final 0.19
- tracks: 317; persistent (alive >= 50% of run): 0; longest 53 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 15], H1 [0, 0, 0]
- motion: 20 long-lived tracks moved >= 1 body length; max speed 0.258/time; max body lengths 23.5
- replication (lineage window K = 20 frames = time 1000, default): splits 44, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 18, merge/split ratio 0.409, nucleations 216
- channel total drift (end/start - 1): [-0.0896, 1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 140 at frame 85: holes 0, rim-vs-core 0.24, rim-vs-outside 0.40, heterogeneity 0.20; core [0.922, 0.414] rim [0.686, 0.411]
  - track 187 at frame 95: holes 0, rim-vs-core 0.15, rim-vs-outside 0.58, heterogeneity 0.17; core [0.925, 0.359] rim [0.78, 0.407]
  - track 211 at frame 98: holes 0, rim-vs-core 0.26, rim-vs-outside 0.41, heterogeneity 0.18; core [0.927, 0.262] rim [0.676, 0.346]
  - track 214 at frame 95: holes 0, rim-vs-core 0.26, rim-vs-outside 0.42, heterogeneity 0.19; core [0.944, 0.326] rim [0.684, 0.378]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 81 components >= 12 px at frames [40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.861, rim/outside 8.93 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.83)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.45, rim/outside 0.991 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.606)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #140 (t=4250, R_eq 13.66): none; #187 (t=4750, R_eq 19): none; #211 (t=4900, R_eq 10.16): none; #214 (t=4750, R_eq 10.66): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
