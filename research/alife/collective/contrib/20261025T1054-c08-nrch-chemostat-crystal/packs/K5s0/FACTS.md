# Evidence pack: nrch (seed 0)

- world: `../../w/nrch.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 241 frames x 500 steps x dt 0.05 = time 6000; grid [192, 192]; wall 702s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/nrch.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/K5s0 --seeds 0 --frames 240 --spf 500 --lineage-k 40 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.9038, 0.8984], min area 6 px

## Measurements
- components: final 25, mean 24.4, max 40; occupancy final 0.22
- tracks: 172; persistent (alive >= 50% of run): 25; longest 231 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.15 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 25, 25], H1 [0, 0, 0]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 0.276/time; max body lengths 90.7
- replication (lineage window K = 40 frames = time 1000, --lineage-k): splits 18, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 11, merge/split ratio 0.611, nucleations 127
- channel total drift (end/start - 1): [-0.0792, 1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 125: holes 0, rim-vs-core 0.26, rim-vs-outside 0.37, heterogeneity 0.20; core [0.932, 0.376] rim [0.673, 0.415]
  - track 32 at frame 127: holes 0, rim-vs-core 0.26, rim-vs-outside 0.36, heterogeneity 0.20; core [0.927, 0.369] rim [0.668, 0.41]
  - track 67 at frame 127: holes 0, rim-vs-core 0.25, rim-vs-outside 0.39, heterogeneity 0.21; core [0.937, 0.371] rim [0.693, 0.42]
  - track 79 at frame 129: holes 0, rim-vs-core 0.26, rim-vs-outside 0.34, heterogeneity 0.20; core [0.928, 0.376] rim [0.669, 0.414]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 151 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 9.74 (aggregate of 151 individuals; 0/151 membrane-like individually; rim level 0.796)
  - radial psi: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.39, rim/outside 0.952 (aggregate of 151 individuals; 0/151 membrane-like individually; rim level 0.58)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=3125, R_eq 10.26): none; #32 (t=3175, R_eq 10.01): none; #67 (t=3175, R_eq 10.42): none; #79 (t=3225, R_eq 10.16): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
