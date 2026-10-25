# Evidence pack: apfc (seed 0)

- world: `../../world.py`, family `active-pfc`
- parent: new class (Menzel & Loewen 2013 active phase-field crystal); mutation: none (benchmark model)
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 56s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/f76d4b70-94d3-54e6-8e9a-d0072da2d452/scratchpad/apfc/world.py --out /tmp/claude-0/-home-user-physim/f76d4b70-94d3-54e6-8e9a-d0072da2d452/scratchpad/apfc/pack --seeds 0 1 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.6272], min area 6 px

## Measurements
- components: final 6, mean 7.3, max 10; occupancy final 0.15
- tracks: 79; persistent (alive >= 50% of run): 2; longest 155 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.30 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 7, 6], H1 [0, 0, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.301/time; max body lengths 23.6
- replication (lineage window K = 20 frames = time 100, default): splits 23, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 24, merge/split ratio 1.04, nucleations 6
- channel total drift (end/start - 1): [-0.6787, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 79: holes 0, rim-vs-core 0.58, rim-vs-outside 0.17, heterogeneity 0.26; core [0.701, 0.45, 0.689] rim [0.444, 0.065, 0.338]
  - track 22 at frame 94: holes 0, rim-vs-core 0.59, rim-vs-outside 0.15, heterogeneity 0.26; core [0.694, 0.45, 0.691] rim [0.442, 0.061, 0.324]
  - track 37 at frame 136: holes 0, rim-vs-core 0.59, rim-vs-outside 0.16, heterogeneity 0.25; core [0.67, 0.462, 0.706] rim [0.442, 0.064, 0.339]
  - track 60 at frame 171: holes 0, rim-vs-core 0.60, rim-vs-outside 0.15, heterogeneity 0.25; core [0.669, 0.459, 0.701] rim [0.434, 0.058, 0.327]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 43 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial crystal amplitude (smoothed (phi - mean)^2): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.742, rim/outside 8.41 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.632)
  - radial density phi: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.437, rim/outside 1.44 (aggregate of 43 individuals; 7/43 membrane-like individually; rim level 0.273)
  - radial |P|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.824, rim/outside 9.39 (aggregate of 43 individuals; 3/43 membrane-like individually; rim level 0.569)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=395, R_eq 5.23): none; #22 (t=470, R_eq 5.17): none; #37 (t=680, R_eq 5.01): none; #60 (t=855, R_eq 5.08): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
