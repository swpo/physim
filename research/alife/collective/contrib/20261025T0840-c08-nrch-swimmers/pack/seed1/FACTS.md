# Evidence pack: nrch (seed 1)

- world: `../world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 670s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/world.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/pack_s1 --seeds 1 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-1.0641, 1.0644], min area 6 px

## Measurements
- components: final 5, mean 5.8, max 14; occupancy final 0.22
- tracks: 147; persistent (alive >= 50% of run): 0; longest 40 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.192/time; max body lengths 13.4
- replication (lineage window K = 20 frames = time 1000, default): splits 38, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 24, merge/split ratio 0.632, nucleations 51
- channel total drift (end/start - 1): [0.0, 142.2414]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 121 at frame 101: holes 0, rim-vs-core 0.21, rim-vs-outside 0.55, heterogeneity 0.18; core [0.956, 0.327] rim [0.746, 0.323]
  - track 88 at frame 77: holes 0, rim-vs-core 0.19, rim-vs-outside 0.49, heterogeneity 0.19; core [0.94, 0.394] rim [0.782, 0.493]
  - track 93 at frame 74: holes 0, rim-vs-core 0.25, rim-vs-outside 0.34, heterogeneity 0.19; core [0.916, 0.374] rim [0.671, 0.439]
  - track 128 at frame 101: holes 0, rim-vs-core 0.22, rim-vs-outside 0.50, heterogeneity 0.17; core [0.943, 0.374] rim [0.722, 0.377]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 31 components >= 12 px at frames [40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.818, rim/outside 5.2 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.724)
  - radial psi: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.41, rim/outside 0.951 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.536)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #121 (t=5050, R_eq 22.42): none; #88 (t=3850, R_eq 17.26): none; #93 (t=3700, R_eq 11.64): none; #128 (t=5050, R_eq 19.53): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
