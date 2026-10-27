# Evidence pack: barkley-puffs (seed 1)

- world: `../../world.py`, family `subcritical-turbulence`
- parent: None; mutation: -
- run: 151 frames x 200 steps x dt 0.05 = time 1500; grid [32, 512]; wall 26s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/bark/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/bark/pack --seeds 0 1 --frames 150 --no-movie`
- segmentation: matter > 0.20 of robust range [0.0, 2.0143], min area 6 px

## Measurements
- components: final 3, mean 3.1, max 12; occupancy final 0.15
- tracks: 28; persistent (alive >= 50% of run): 3; longest 151 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 9.58 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 3, 3], H1 [2, 2, 2]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 1.06/time; max body lengths 53.5
- replication (lineage window K = 20 frames = time 200, default): splits 5, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio 0.4, nucleations 0
- channel total drift (end/start - 1): [-0.4366, -0.3217]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 76: holes 0, rim-vs-core 0.18, rim-vs-outside 0.49, heterogeneity 0.24; core [0.613, 0.124] rim [0.527, 0.281]
  - track 17 at frame 54: holes 0, rim-vs-core 0.18, rim-vs-outside 0.50, heterogeneity 0.22; core [0.658, 0.14] rim [0.537, 0.275]
  - track 24 at frame 110: holes 0, rim-vs-core 0.19, rim-vs-outside 0.49, heterogeneity 0.23; core [0.62, 0.138] rim [0.525, 0.301]
  - track 21 at frame 35: holes 0, rim-vs-core 0.18, rim-vs-outside 0.49, heterogeneity 0.24; core [0.632, 0.155] rim [0.537, 0.313]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 18 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial turbulence q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside n/a (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.624)
  - radial centreline u: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 3.61, rim/outside n/a (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.478)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=760, R_eq 17.25): none; #17 (t=540, R_eq 15.73): none; #24 (t=1100, R_eq 16.23): none; #21 (t=350, R_eq 16.29): none

## Warnings
- radial: for 18 of 18 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
