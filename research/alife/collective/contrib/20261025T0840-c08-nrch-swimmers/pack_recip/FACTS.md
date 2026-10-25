# Evidence pack: nrch (seed 0)

- world: `../world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 606s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/world.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/pack_recip --seeds 0 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.49 of robust range [-1.347, 1.4246], min area 6 px

## Measurements
- components: final 18, mean 32.9, max 67; occupancy final 0.30
- tracks: 80; persistent (alive >= 50% of run): 26; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 30.63 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 1000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 13, merge/split ratio n/a, nucleations 67
- channel total drift (end/start - 1): [0.0, 1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 61: holes 0, rim-vs-core 0.40, rim-vs-outside 0.53, heterogeneity 0.15; core [0.96, 0.037] rim [0.676, 0.313]
  - track 4 at frame 61: holes 0, rim-vs-core 0.32, rim-vs-outside 0.73, heterogeneity 0.14; core [0.985, 0.023] rim [0.753, 0.249]
  - track 8 at frame 61: holes 0, rim-vs-core 0.34, rim-vs-outside 0.72, heterogeneity 0.15; core [0.983, 0.021] rim [0.743, 0.256]
  - track 9 at frame 61: holes 0, rim-vs-core 0.32, rim-vs-outside 0.73, heterogeneity 0.14; core [0.984, 0.021] rim [0.752, 0.247]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 176 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.945, rim/outside 11.1 (aggregate of 176 individuals; 0/176 membrane-like individually; rim level 0.938)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 35.9, rim/outside 0.969 (aggregate of 176 individuals; 0/176 membrane-like individually; rim level 0.869)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=3050, R_eq 9.52): none; #4 (t=3050, R_eq 12.22): none; #8 (t=3050, R_eq 11.35): none; #9 (t=3050, R_eq 12.26): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
