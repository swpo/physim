# Evidence pack: barkley-puffs (seed 0)

- world: `../../world.py`, family `subcritical-turbulence`
- parent: None; mutation: -
- run: 151 frames x 200 steps x dt 0.05 = time 1500; grid [32, 512]; wall 29s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/bark/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/bark/pack --seeds 0 1 --frames 150 --no-movie`
- segmentation: matter > 0.20 of robust range [0.0, 2.0112], min area 6 px

## Measurements
- components: final 4, mean 4.1, max 12; occupancy final 0.19
- tracks: 32; persistent (alive >= 50% of run): 4; longest 149 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.71 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 4, 4], H1 [5, 3, 3]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.973/time; max body lengths 51.0
- replication (lineage window K = 20 frames = time 200, default): splits 5, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio 0.6, nucleations 0
- channel total drift (end/start - 1): [-0.2867, -0.3947]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 77: holes 0, rim-vs-core 0.19, rim-vs-outside 0.48, heterogeneity 0.23; core [0.633, 0.126] rim [0.528, 0.287]
  - track 24 at frame 77: holes 0, rim-vs-core 0.17, rim-vs-outside 0.50, heterogeneity 0.22; core [0.653, 0.137] rim [0.538, 0.261]
  - track 26 at frame 77: holes 0, rim-vs-core 0.22, rim-vs-outside 0.46, heterogeneity 0.23; core [0.675, 0.132] rim [0.52, 0.283]
  - track 10 at frame 40: holes 0, rim-vs-core 0.21, rim-vs-outside 0.47, heterogeneity 0.22; core [0.663, 0.127] rim [0.528, 0.288]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 24 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial turbulence q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.844, rim/outside n/a (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.589)
  - radial centreline u: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 3.39, rim/outside n/a (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.471)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #21 (t=770, R_eq 15.91): none; #24 (t=770, R_eq 15.69): none; #26 (t=770, R_eq 15.83): none; #10 (t=400, R_eq 15.39): none

## Warnings
- radial: for 24 of 24 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
