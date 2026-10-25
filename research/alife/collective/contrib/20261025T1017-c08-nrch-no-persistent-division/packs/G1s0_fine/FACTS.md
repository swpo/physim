# Evidence pack: nrch (seed 0)

- world: `../../w/nrch.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 241 frames x 500 steps x dt 0.05 = time 6000; grid [192, 192]; wall 951s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/nrch.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/G1s0_fine --seeds 0 --frames 240 --spf 500 --lineage-k 40 --no-movie`
- segmentation: matter > 0.49 of robust range [-1.0553, 1.0926], min area 6 px

## Measurements
- components: final 16, mean 13.3, max 24; occupancy final 0.22
- tracks: 234; persistent (alive >= 50% of run): 6; longest 168 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.263/time; max body lengths 40.1
- replication (lineage window K = 40 frames = time 1000, --lineage-k): splits 69, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 54, merge/split ratio 0.783, nucleations 61
- channel total drift (end/start - 1): [0.0953, 385.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 123 at frame 157: holes 0, rim-vs-core 0.17, rim-vs-outside 0.46, heterogeneity 0.18; core [0.91, 0.282] rim [0.75, 0.349]
  - track 147 at frame 159: holes 0, rim-vs-core 0.15, rim-vs-outside 0.50, heterogeneity 0.19; core [0.923, 0.36] rim [0.775, 0.37]
  - track 142 at frame 151: holes 0, rim-vs-core 0.24, rim-vs-outside 0.48, heterogeneity 0.19; core [0.951, 0.367] rim [0.711, 0.378]
  - track 208 at frame 210: holes 0, rim-vs-core 0.27, rim-vs-outside 0.39, heterogeneity 0.18; core [0.91, 0.263] rim [0.664, 0.362]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 82 components >= 12 px at frames [81, 121, 159, 200, 240]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.857, rim/outside 7.76 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.83)
  - radial psi: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.34, rim/outside 0.992 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.597)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #123 (t=3925, R_eq 11.98): none; #147 (t=3975, R_eq 11.77): none; #142 (t=3775, R_eq 14.69): none; #208 (t=5250, R_eq 11.89): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
