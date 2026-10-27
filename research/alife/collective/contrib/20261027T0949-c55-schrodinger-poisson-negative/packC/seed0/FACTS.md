# Evidence pack: fed-wave-matter (seed 0)

- world: `../../world.py`, family `schrodinger-poisson`
- parent: None; mutation: -
- run: 201 frames x 50 steps x dt 0.2 = time 2000; grid [128, 128]; wall 27s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/sp/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/sp/packC --seeds 0 1 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.06 of robust range [0.0001, 4.7426], min area 6 px

## Measurements
- components: final 8, mean 6.1, max 18; occupancy final 0.05
- tracks: 711; persistent (alive >= 50% of run): 0; longest 14 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.12, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 3, 2], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 3.8
- replication (lineage window K = 20 frames = time 200, default): splits 176, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 172, merge/split ratio 0.977, nucleations 198
- channel total drift (end/start - 1): [-0.9282, -0.0283, None, 1.1659]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 187 at frame 44: holes 0, rim-vs-core 0.54, rim-vs-outside 0.22, heterogeneity 0.21; core [0.716, 0.223, 0.629, 0.33] rim [0.227, 0.409, 0.557, 0.46]
  - track 536 at frame 156: holes 0, rim-vs-core 0.11, rim-vs-outside 0.12, heterogeneity 0.11; core [0.273, 0.595, 0.615, 0.512] rim [0.178, 0.629, 0.591, 0.538]
  - track 654 at frame 190: holes 0, rim-vs-core 0.05, rim-vs-outside 0.33, heterogeneity 0.03; core [0.196, 0.619, 0.39, 0.064] rim [0.15, 0.638, 0.383, 0.069]
  - track 682 at frame 197: holes 0, rim-vs-core 0.33, rim-vs-outside 0.19, heterogeneity 0.18; core [0.495, 0.527, 0.636, 0.701] rim [0.197, 0.617, 0.583, 0.603]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 38 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial density |psi|^2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.538, rim/outside 4.31 (aggregate of 38 individuals; 1/38 membrane-like individually; rim level 0.265)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.76, rim/outside 0.86 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.535)
  - radial potential -V: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 1.2 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.68)
  - radial phase cos: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.04 (aggregate of 38 individuals; 1/38 membrane-like individually; rim level 0.484)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #187 (t=440, R_eq 6.77): none; #536 (t=1560, R_eq 7.84): none; #654 (t=1900, R_eq 5.47): none; #682 (t=1970, R_eq 9.74): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
