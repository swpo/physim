# Evidence pack: nrch (seed 1)

- world: `../../w/nrch.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 181 frames x 1000 steps x dt 0.05 = time 9000; grid [192, 192]; wall 1070s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/nrch.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/KILLs1 --seeds 1 --frames 180 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.9098, 0.9005], min area 6 px

## Measurements
- components: final 19, mean 20.6, max 37; occupancy final 0.20
- tracks: 438; persistent (alive >= 50% of run): 13; longest 165 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.62 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 19, 19], H1 [0, 0, 0]
- motion: 41 long-lived tracks moved >= 1 body length; max speed 0.252/time; max body lengths 97.2
- replication (lineage window K = 20 frames = time 1000, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio 0.5, nucleations 433
- channel total drift (end/start - 1): [-0.118, -122.5862]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 191 at frame 98: holes 0, rim-vs-core 0.27, rim-vs-outside 0.36, heterogeneity 0.20; core [0.926, 0.361] rim [0.662, 0.403]
  - track 262 at frame 103: holes 0, rim-vs-core 0.27, rim-vs-outside 0.35, heterogeneity 0.20; core [0.923, 0.381] rim [0.66, 0.412]
  - track 307 at frame 106: holes 0, rim-vs-core 0.26, rim-vs-outside 0.36, heterogeneity 0.20; core [0.922, 0.387] rim [0.659, 0.421]
  - track 322 at frame 107: holes 0, rim-vs-core 0.27, rim-vs-outside 0.36, heterogeneity 0.20; core [0.924, 0.364] rim [0.661, 0.408]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 124 components >= 12 px at frames [30, 61, 91, 119, 150, 180]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.803, rim/outside 8.24 (aggregate of 124 individuals; 0/124 membrane-like individually; rim level 0.776)
  - radial psi: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.34, rim/outside 0.942 (aggregate of 124 individuals; 0/124 membrane-like individually; rim level 0.554)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #191 (t=4900, R_eq 11.11): none; #262 (t=5150, R_eq 11.69): none; #307 (t=5300, R_eq 11): none; #322 (t=5350, R_eq 10.9): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
