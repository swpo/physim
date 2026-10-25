# Evidence pack: nrch (seed 0)

- world: `../../w/nrch.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 979s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/nrch.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/A3s0 --seeds 0 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.49 of robust range [-1.0499, 1.0786], min area 6 px

## Measurements
- components: final 16, mean 11.8, max 20; occupancy final 0.19
- tracks: 326; persistent (alive >= 50% of run): 1; longest 87 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.61 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.244/time; max body lengths 39.2
- replication (lineage window K = 20 frames = time 1000, default): splits 46, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 38, merge/split ratio 0.826, nucleations 207
- channel total drift (end/start - 1): [-0.0894, 1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 78: holes 0, rim-vs-core 0.26, rim-vs-outside 0.42, heterogeneity 0.20; core [0.949, 0.429] rim [0.686, 0.425]
  - track 170 at frame 92: holes 0, rim-vs-core 0.27, rim-vs-outside 0.40, heterogeneity 0.19; core [0.933, 0.367] rim [0.671, 0.415]
  - track 203 at frame 96: holes 0, rim-vs-core 0.17, rim-vs-outside 0.51, heterogeneity 0.18; core [0.92, 0.4] rim [0.758, 0.435]
  - track 220 at frame 98: holes 0, rim-vs-core 0.26, rim-vs-outside 0.39, heterogeneity 0.19; core [0.917, 0.349] rim [0.663, 0.417]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 84 components >= 12 px at frames [40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.861, rim/outside 8.98 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.835)
  - radial psi: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.43, rim/outside 0.996 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.609)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=3900, R_eq 12.15): none; #170 (t=4600, R_eq 11.51): none; #203 (t=4800, R_eq 14.71): none; #220 (t=4900, R_eq 12.53): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
