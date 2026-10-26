# Evidence pack: cips-inhib (seed 8)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 601 frames x 100 steps x dt 0.1 = time 6000; grid [128, 128]; wall 107s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27k/world.py --out collective/contrib/wip-c27k/noI --seeds 7 8 --frames 600 --size 128 128 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0001, 0.9994], min area 6 px

## Measurements
- components: final 36, mean 44.3, max 76; occupancy final 0.14
- tracks: 118; persistent (alive >= 50% of run): 40; longest 581 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 37, 36], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 37, merge/split ratio n/a, nucleations 81
- channel total drift (end/start - 1): [0.0, -0.2502, 0.1724, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 313: holes 0, rim-vs-core 0.28, rim-vs-outside 0.52, heterogeneity 0.07; core [0.982, 0.868, 0.218, 0.0] rim [0.794, 0.695, 0.341, 0.0]
  - track 4 at frame 313: holes 0, rim-vs-core 0.29, rim-vs-outside 0.49, heterogeneity 0.07; core [0.975, 0.835, 0.271, 0.0] rim [0.767, 0.671, 0.383, 0.0]
  - track 5 at frame 313: holes 0, rim-vs-core 0.18, rim-vs-outside 0.56, heterogeneity 0.07; core [0.984, 0.861, 0.211, 0.0] rim [0.866, 0.749, 0.286, 0.0]
  - track 7 at frame 313: holes 0, rim-vs-core 0.30, rim-vs-outside 0.52, heterogeneity 0.07; core [0.983, 0.884, 0.159, 0.0] rim [0.784, 0.698, 0.296, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 264 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.958, rim/outside 55.4 (aggregate of 264 individuals; 0/264 membrane-like individually; rim level 0.95)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 4.36 (aggregate of 264 individuals; 0/264 membrane-like individually; rim level 0.816)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.4, rim/outside 0.699 (aggregate of 264 individuals; 0/264 membrane-like individually; rim level 0.468)
  - radial I: flat profile (no radial structure; level 0; aggregate of 264 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=3130, R_eq 3.57): none; #4 (t=3130, R_eq 3.29): none; #5 (t=3130, R_eq 3.43): none; #7 (t=3130, R_eq 3.99): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
