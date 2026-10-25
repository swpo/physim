# Evidence pack: ad5-evolve (seed 11)

- world: `../../world.py`, family `phase-field`
- parent: ad2-catalysts; mutation: N catalyst alleles with different rates, rare local mutation patches, random dilution disks
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 206s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27g/world.py --out collective/contrib/wip-c27g/rerun --seeds 11 12 --frames 200`
- segmentation: matter > 0.43 of robust range [-1.0671, 1.4399], min area 6 px

## Measurements
- components: final 12, mean 7.9, max 12; occupancy final 0.12
- tracks: 18; persistent (alive >= 50% of run): 6; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 3.20 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00211/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 2000, default): splits 6, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1006, -0.5972, -0.6973, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.28, rim-vs-outside 0.83, heterogeneity 0.07; core [0.965, 0.133, 0.952, 0.0, 0.0, 0.0] rim [0.792, 0.176, 0.736, 0.0, 0.0, 0.0]
  - track 4 at frame 101: holes 0, rim-vs-core 0.33, rim-vs-outside 0.77, heterogeneity 0.06; core [0.954, 0.061, 0.0, 1.0, 0.0, 0.0] rim [0.717, 0.156, 0.0, 0.784, 0.0, 0.0]
  - track 5 at frame 71: holes 0, rim-vs-core 0.28, rim-vs-outside 0.84, heterogeneity 0.07; core [0.971, 0.111, 0.971, 0.0, 0.0, 0.0] rim [0.805, 0.174, 0.759, 0.0, 0.0, 0.0]
  - track 14 at frame 183: holes 0, rim-vs-core 0.44, rim-vs-outside 0.67, heterogeneity 0.07; core [0.965, 0.018, 0.0, 0.0, 0.0, 0.956] rim [0.7, 0.086, 0.0, 0.0, 0.0, 0.606]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 51 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 49.4 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.92)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 6.19, rim/outside 0.711 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.248)
  - radial a0 (k=0.10): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.917, rim/outside 26.9 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.273)
  - radial a1 (k=0.12): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.954, rim/outside 13.9 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.131)
  - radial a2 (k=0.14): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.917, rim/outside 20.4 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.199)
  - radial a3 (k=0.16): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.896, rim/outside 23.2 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.321)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=10100, R_eq 7.72): none; #4 (t=10100, R_eq 8.67): none; #5 (t=7100, R_eq 8.57): none; #14 (t=18300, R_eq 6.86): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
