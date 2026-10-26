# Evidence pack: phoretic-colloids (seed 3)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0254-c33-phoretic-janus-claim/world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 401 frames x 1 steps x dt 0.5 = time 200; grid [128, 128]; wall 98s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0254-c33-phoretic-janus-claim/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/rev13/u20 --seeds 3 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.2992], min area 6 px

## Measurements
- components: final 44, mean 45.5, max 63; occupancy final 0.09
- tracks: 402; persistent (alive >= 50% of run): 38; longest 391 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.43 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [58, 50, 40], H1 [0, 0, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.105/time; max body lengths 2.6
- replication (lineage window K = 20 frames = time 10, default): splits 9, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 39, merge/split ratio 4.33, nucleations 345
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 205: holes 0, rim-vs-core 0.45, rim-vs-outside 0.44, heterogeneity 0.19; core [0.889, 0.538, 0.873] rim [0.593, 0.313, 0.616]
  - track 7 at frame 212: holes 0, rim-vs-core 0.34, rim-vs-outside 0.41, heterogeneity 0.21; core [0.913, 0.365, 0.753] rim [0.643, 0.25, 0.572]
  - track 11 at frame 212: holes 0, rim-vs-core 0.30, rim-vs-outside 0.44, heterogeneity 0.11; core [0.556, 1.0, 0.556] rim [0.398, 0.765, 0.463]
  - track 12 at frame 215: holes 0, rim-vs-core 0.36, rim-vs-outside 0.37, heterogeneity 0.13; core [0.773, 0.643, 0.619] rim [0.568, 0.379, 0.496]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 221 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 15.8 (aggregate of 221 individuals; 1/221 membrane-like individually; rim level 0.693)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.722, rim/outside 20.3 (aggregate of 221 individuals; 5/221 membrane-like individually; rim level 0.498)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 3.75 (aggregate of 221 individuals; 0/221 membrane-like individually; rim level 0.654)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=102.5, R_eq 3.7): none; #7 (t=106, R_eq 3.14): none; #11 (t=106, R_eq 2.19): none; #12 (t=107.5, R_eq 2.52): none

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
