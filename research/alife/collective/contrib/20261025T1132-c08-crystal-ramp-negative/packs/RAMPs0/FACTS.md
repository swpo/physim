# Evidence pack: nrch (seed 0)

- world: `../../w/nrch.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 181 frames x 1000 steps x dt 0.05 = time 9000; grid [192, 192]; wall 1043s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/nrch.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/RAMPs0 --seeds 0 --frames 180 --spf 1000 --no-movie`
- segmentation: matter > 0.49 of robust range [-0.8959, 0.9282], min area 6 px

## Measurements
- components: final 25, mean 24.6, max 40; occupancy final 0.27
- tracks: 348; persistent (alive >= 50% of run): 25; longest 169 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.73 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 25, 25], H1 [0, 0, 0]
- motion: 29 long-lived tracks moved >= 1 body length; max speed 0.27/time; max body lengths 116.1
- replication (lineage window K = 20 frames = time 1000, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio 0.667, nucleations 340
- channel total drift (end/start - 1): [0.1566, 513.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 177 at frame 97: holes 0, rim-vs-core 0.27, rim-vs-outside 0.36, heterogeneity 0.20; core [0.92, 0.388] rim [0.655, 0.416]
  - track 250 at frame 100: holes 0, rim-vs-core 0.26, rim-vs-outside 0.36, heterogeneity 0.20; core [0.921, 0.387] rim [0.658, 0.412]
  - track 269 at frame 100: holes 0, rim-vs-core 0.27, rim-vs-outside 0.36, heterogeneity 0.21; core [0.92, 0.388] rim [0.651, 0.42]
  - track 275 at frame 101: holes 0, rim-vs-core 0.27, rim-vs-outside 0.36, heterogeneity 0.21; core [0.919, 0.392] rim [0.651, 0.416]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 148 components >= 12 px at frames [30, 61, 91, 119, 150, 180]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.825, rim/outside 11.1 (aggregate of 148 individuals; 0/148 membrane-like individually; rim level 0.807)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.3, rim/outside 0.959 (aggregate of 148 individuals; 0/148 membrane-like individually; rim level 0.583)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #177 (t=4850, R_eq 10.49): none; #250 (t=5000, R_eq 10.49): none; #269 (t=5000, R_eq 10.62): none; #275 (t=5050, R_eq 10.59): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
