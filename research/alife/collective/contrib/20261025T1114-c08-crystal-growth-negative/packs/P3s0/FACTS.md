# Evidence pack: nrch (seed 0)

- world: `../../w/nrch.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 241 frames x 500 steps x dt 0.05 = time 6000; grid [192, 192]; wall 682s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/nrch.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/P3s0 --seeds 0 --frames 240 --spf 500 --lineage-k 40 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.9219, 0.935], min area 6 px

## Measurements
- components: final 25, mean 24.1, max 45; occupancy final 0.27
- tracks: 549; persistent (alive >= 50% of run): 25; longest 194 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.30 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 25, 25], H1 [0, 0, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.271/time; max body lengths 64.6
- replication (lineage window K = 40 frames = time 1000, --lineage-k): splits 157, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 140, merge/split ratio 0.892, nucleations 116
- channel total drift (end/start - 1): [0.1566, 29.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 443 at frame 145: holes 0, rim-vs-core 0.26, rim-vs-outside 0.37, heterogeneity 0.20; core [0.927, 0.401] rim [0.671, 0.421]
  - track 461 at frame 145: holes 0, rim-vs-core 0.18, rim-vs-outside 0.43, heterogeneity 0.20; core [0.921, 0.401] rim [0.736, 0.412]
  - track 467 at frame 145: holes 0, rim-vs-core 0.27, rim-vs-outside 0.37, heterogeneity 0.20; core [0.924, 0.396] rim [0.66, 0.427]
  - track 536 at frame 161: holes 0, rim-vs-core 0.19, rim-vs-outside 0.43, heterogeneity 0.20; core [0.927, 0.408] rim [0.736, 0.407]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 145 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.831, rim/outside 7.52 (aggregate of 145 individuals; 0/145 membrane-like individually; rim level 0.795)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.25, rim/outside 0.96 (aggregate of 145 individuals; 0/145 membrane-like individually; rim level 0.578)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #443 (t=3625, R_eq 11.3): none; #461 (t=3625, R_eq 11.23): none; #467 (t=3625, R_eq 11.33): none; #536 (t=4025, R_eq 11.23): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 145 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
