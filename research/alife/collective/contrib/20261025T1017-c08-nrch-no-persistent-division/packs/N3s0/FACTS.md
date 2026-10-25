# Evidence pack: nrch (seed 0)

- world: `../../w/nrch.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 241 frames x 500 steps x dt 0.05 = time 6000; grid [192, 192]; wall 1140s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/nrch.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/N3s0 --seeds 0 --frames 240 --spf 500 --lineage-k 40 --no-movie`
- segmentation: matter > 0.49 of robust range [-1.0947, 1.1225], min area 6 px

## Measurements
- components: final 15, mean 17.8, max 31; occupancy final 0.19
- tracks: 323; persistent (alive >= 50% of run): 5; longest 177 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.24 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [2, 0, 0]
- motion: 31 long-lived tracks moved >= 1 body length; max speed 0.263/time; max body lengths 45.0
- replication (lineage window K = 40 frames = time 1000, --lineage-k): splits 64, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 55, merge/split ratio 0.859, nucleations 151
- channel total drift (end/start - 1): [-0.0871, -383.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 33 at frame 95: holes 0, rim-vs-core 0.25, rim-vs-outside 0.39, heterogeneity 0.17; core [0.917, 0.321] rim [0.675, 0.372]
  - track 160 at frame 121: holes 0, rim-vs-core 0.24, rim-vs-outside 0.40, heterogeneity 0.18; core [0.896, 0.321] rim [0.668, 0.406]
  - track 227 at frame 173: holes 0, rim-vs-core 0.25, rim-vs-outside 0.39, heterogeneity 0.18; core [0.926, 0.427] rim [0.673, 0.455]
  - track 203 at frame 143: holes 0, rim-vs-core 0.26, rim-vs-outside 0.39, heterogeneity 0.20; core [0.925, 0.338] rim [0.667, 0.374]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 104 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.854, rim/outside 6.83 (aggregate of 104 individuals; 0/104 membrane-like individually; rim level 0.815)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.47, rim/outside 0.977 (aggregate of 104 individuals; 0/104 membrane-like individually; rim level 0.595)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #33 (t=2375, R_eq 12.59): none; #160 (t=3025, R_eq 12.44): none; #227 (t=4325, R_eq 11.18): none; #203 (t=3575, R_eq 11.3): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
