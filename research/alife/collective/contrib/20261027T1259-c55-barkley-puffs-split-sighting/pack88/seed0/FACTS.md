# Evidence pack: barkley-puffs (seed 0)

- world: `../world.py`, family `subcritical-turbulence`
- parent: None; mutation: -
- run: 151 frames x 400 steps x dt 0.05 = time 3000; grid [16, 4096]; wall 232s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/bark/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/bark/pack88_s0 --seeds 0 --size 16 4096 --frames 150 --spf 400 --no-movie`
- segmentation: matter > 0.20 of robust range [0.0, 1.9948], min area 6 px

## Measurements
- components: final 71, mean 57.3, max 72; occupancy final 0.50
- tracks: 326; persistent (alive >= 50% of run): 43; longest 151 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 7.89 (1 = constant size)
- enclosures: components with a hole mean 1.22, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 12, 42]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [141, 74, 71], H1 [113, 70, 70]
- motion: 105 long-lived tracks moved >= 1 body length; max speed 0.841/time; max body lengths 83.5
- replication (lineage window K = 20 frames = time 400, default): splits 152, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 2, merges 2, merge/split ratio 0.013, nucleations 0
- channel total drift (end/start - 1): [16.6235, -0.6664]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 76: holes 0, rim-vs-core 0.16, rim-vs-outside 0.45, heterogeneity 0.17; core [0.665, 0.082] rim [0.52, 0.158]
  - track 5 at frame 76: holes 0, rim-vs-core 0.12, rim-vs-outside 0.45, heterogeneity 0.16; core [0.623, 0.078] rim [0.521, 0.147]
  - track 22 at frame 77: holes 0, rim-vs-core 0.11, rim-vs-outside 0.51, heterogeneity 0.17; core [0.644, 0.09] rim [0.57, 0.171]
  - track 150 at frame 92: holes 0, rim-vs-core 0.09, rim-vs-outside 0.46, heterogeneity 0.14; core [0.607, 0.068] rim [0.543, 0.134]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 370 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial turbulence q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.972, rim/outside 12 (aggregate of 370 individuals; 0/370 membrane-like individually; rim level 0.615)
  - radial centreline u: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 3.8, rim/outside 0.924 (aggregate of 370 individuals; 0/370 membrane-like individually; rim level 0.206)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=1520, R_eq 11.6): none; #5 (t=1520, R_eq 11.6): none; #22 (t=1540, R_eq 11.55): none; #150 (t=1840, R_eq 10.73): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 369 of 370 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
