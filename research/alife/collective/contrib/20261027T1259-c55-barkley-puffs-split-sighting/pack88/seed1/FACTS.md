# Evidence pack: barkley-puffs (seed 1)

- world: `../world.py`, family `subcritical-turbulence`
- parent: None; mutation: -
- run: 151 frames x 400 steps x dt 0.05 = time 3000; grid [16, 4096]; wall 231s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/bark/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/bark/pack88_s1 --seeds 1 --size 16 4096 --frames 150 --spf 400 --no-movie`
- segmentation: matter > 0.20 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 73, mean 61.5, max 74; occupancy final 0.49
- tracks: 279; persistent (alive >= 50% of run): 54; longest 151 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 5.64 (1 = constant size)
- enclosures: components with a hole mean 1.19, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 10, 42]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [137, 74, 73], H1 [102, 72, 72]
- motion: 107 long-lived tracks moved >= 1 body length; max speed 0.799/time; max body lengths 86.7
- replication (lineage window K = 20 frames = time 400, default): splits 129, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [16.6466, -0.6656]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 76: holes 0, rim-vs-core 0.16, rim-vs-outside 0.41, heterogeneity 0.14; core [0.645, 0.078] rim [0.492, 0.129]
  - track 9 at frame 76: holes 0, rim-vs-core 0.10, rim-vs-outside 0.49, heterogeneity 0.17; core [0.629, 0.095] rim [0.56, 0.16]
  - track 35 at frame 79: holes 0, rim-vs-core 0.10, rim-vs-outside 0.49, heterogeneity 0.14; core [0.624, 0.064] rim [0.551, 0.128]
  - track 219 at frame 103: holes 0, rim-vs-core 0.07, rim-vs-outside 0.47, heterogeneity 0.15; core [0.573, 0.065] rim [0.536, 0.124]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 392 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial turbulence q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.974, rim/outside 9.17 (aggregate of 392 individuals; 0/392 membrane-like individually; rim level 0.62)
  - radial centreline u: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 3.9, rim/outside 1.51 (aggregate of 392 individuals; 0/392 membrane-like individually; rim level 0.214)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): centreline u
- membrane-like channels per top track at mid-life: #7 (t=1520, R_eq 11.03): none; #9 (t=1520, R_eq 11.48): none; #35 (t=1580, R_eq 12.41): none; #219 (t=2060, R_eq 12.79): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 391 of 392 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
