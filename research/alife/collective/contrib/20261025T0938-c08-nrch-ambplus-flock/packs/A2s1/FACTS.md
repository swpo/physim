# Evidence pack: nrch (seed 1)

- world: `../../w/nrch.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 922s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/nrch.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/A2s1 --seeds 1 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.49 of robust range [-1.0804, 1.1086], min area 6 px

## Measurements
- components: final 12, mean 9.8, max 20; occupancy final 0.23
- tracks: 287; persistent (alive >= 50% of run): 1; longest 61 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 12, 12], H1 [0, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.243/time; max body lengths 17.8
- replication (lineage window K = 20 frames = time 1000, default): splits 58, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 43, merge/split ratio 0.741, nucleations 138
- channel total drift (end/start - 1): [0.0, 1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 193 at frame 91: holes 0, rim-vs-core 0.22, rim-vs-outside 0.46, heterogeneity 0.17; core [0.911, 0.318] rim [0.697, 0.365]
  - track 166 at frame 73: holes 0, rim-vs-core 0.26, rim-vs-outside 0.48, heterogeneity 0.20; core [0.96, 0.46] rim [0.709, 0.409]
  - track 86 at frame 56: holes 0, rim-vs-core 0.26, rim-vs-outside 0.40, heterogeneity 0.18; core [0.923, 0.35] rim [0.673, 0.408]
  - track 163 at frame 70: holes 0, rim-vs-core 0.24, rim-vs-outside 0.45, heterogeneity 0.20; core [0.94, 0.486] rim [0.7, 0.492]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 60 components >= 12 px at frames [40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.846, rim/outside 5.98 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.797)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.41, rim/outside 0.977 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.568)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #193 (t=4550, R_eq 17.41): none; #166 (t=3650, R_eq 14.85): none; #86 (t=2800, R_eq 11.99): none; #163 (t=3500, R_eq 15.76): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
