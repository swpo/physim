# Evidence pack: nrch (seed 0)

- world: `../../w/nrch.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 181 frames x 1000 steps x dt 0.05 = time 9000; grid [192, 192]; wall 1070s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/nrch.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/KILLs0 --seeds 0 --frames 180 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.8998, 0.8983], min area 6 px

## Measurements
- components: final 24, mean 24.5, max 40; occupancy final 0.21
- tracks: 374; persistent (alive >= 50% of run): 20; longest 161 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.73 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 24, 24], H1 [0, 0, 0]
- motion: 38 long-lived tracks moved >= 1 body length; max speed 0.271/time; max body lengths 121.1
- replication (lineage window K = 20 frames = time 1000, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio 0.667, nucleations 366
- channel total drift (end/start - 1): [-0.112, -255.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 269 at frame 100: holes 0, rim-vs-core 0.28, rim-vs-outside 0.26, heterogeneity 0.20; core [0.89, 0.369] rim [0.616, 0.437]
  - track 275 at frame 101: holes 0, rim-vs-core 0.27, rim-vs-outside 0.36, heterogeneity 0.21; core [0.916, 0.357] rim [0.653, 0.421]
  - track 283 at frame 101: holes 0, rim-vs-core 0.27, rim-vs-outside 0.36, heterogeneity 0.21; core [0.924, 0.384] rim [0.663, 0.426]
  - track 294 at frame 103: holes 0, rim-vs-core 0.28, rim-vs-outside 0.26, heterogeneity 0.20; core [0.894, 0.38] rim [0.625, 0.437]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 145 components >= 12 px at frames [30, 61, 91, 119, 150, 180]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 10.8 (aggregate of 145 individuals; 0/145 membrane-like individually; rim level 0.8)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.39, rim/outside 0.956 (aggregate of 145 individuals; 0/145 membrane-like individually; rim level 0.584)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #269 (t=5000, R_eq 10): none; #275 (t=5050, R_eq 10.19): none; #283 (t=5050, R_eq 10.16): none; #294 (t=5150, R_eq 10): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
