# Evidence pack: ad5-evolve (seed 3)

- world: `../../../../../../threads/active-droplets/worlds/ad5-evolve/world.py`, family `phase-field`
- parent: ad2-catalysts; mutation: N catalyst alleles with different rates, rare local mutation patches, random dilution disks
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 182s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5-evolve/world.py --out collective/contrib/wip-c22/rev_ad5/evolve/seed3 --seeds 3 --frames 200 --no-movie`
- segmentation: matter > 0.42 of robust range [-1.0679, 1.4511], min area 6 px

## Measurements
- components: final 11, mean 8.2, max 11; occupancy final 0.11
- tracks: 19; persistent (alive >= 50% of run): 7; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 3.55 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00175/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 2000, default): splits 6, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.167, nucleations 0
- channel total drift (end/start - 1): [0.0962, -0.5893, -0.5844, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 101: holes 0, rim-vs-core 0.41, rim-vs-outside 0.66, heterogeneity 0.07; core [0.966, 0.108, 0.87, 0.083, 0.0, 0.0] rim [0.715, 0.201, 0.564, 0.059, 0.0, 0.0]
  - track 5 at frame 101: holes 0, rim-vs-core 0.25, rim-vs-outside 0.84, heterogeneity 0.07; core [0.96, 0.122, 0.942, 0.0, 0.0, 0.0] rim [0.808, 0.166, 0.748, 0.0, 0.0, 0.0]
  - track 7 at frame 103: holes 0, rim-vs-core 0.43, rim-vs-outside 0.68, heterogeneity 0.07; core [0.969, 0.112, 0.957, 0.0, 0.0, 0.0] rim [0.714, 0.201, 0.624, 0.0, 0.0, 0.0]
  - track 15 at frame 165: holes 0, rim-vs-core 0.30, rim-vs-outside 0.81, heterogeneity 0.06; core [0.956, 0.009, 0.0, 0.0, 0.0, 0.973] rim [0.779, 0.057, 0.0, 0.0, 0.0, 0.733]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 52 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.94, rim/outside 55.4 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.917)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.01, rim/outside 0.721 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.256)
  - radial a0 (k=0.10): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 40.5 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.435)
  - radial a1 (k=0.12): peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.964, rim/outside 18.4 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.177)
  - radial a2 (k=0.14): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 9.52 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.0864)
  - radial a3 (k=0.16): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 24.2 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.266)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=10100, R_eq 7.9): none; #5 (t=10100, R_eq 7.59): none; #7 (t=10300, R_eq 7.65): none; #15 (t=16500, R_eq 7.9): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
