# Evidence pack: cips-inhib (seed 6)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 601 frames x 100 steps x dt 0.1 = time 6000; grid [128, 128]; wall 106s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out /tmp/claude-0/c28ci/noI --seeds 5 6 --frames 600 --size 128 128 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0001, 0.9994], min area 6 px

## Measurements
- components: final 34, mean 45.2, max 78; occupancy final 0.14
- tracks: 126; persistent (alive >= 50% of run): 42; longest 581 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 34, 33], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00595/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 42, merge/split ratio n/a, nucleations 84
- channel total drift (end/start - 1): [0.0, -0.2622, 0.1808, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 313: holes 0, rim-vs-core 0.30, rim-vs-outside 0.51, heterogeneity 0.07; core [0.979, 0.863, 0.183, 0.0] rim [0.771, 0.683, 0.315, 0.0]
  - track 4 at frame 313: holes 0, rim-vs-core 0.23, rim-vs-outside 0.46, heterogeneity 0.06; core [0.975, 0.819, 0.256, 0.0] rim [0.811, 0.681, 0.35, 0.0]
  - track 10 at frame 313: holes 0, rim-vs-core 0.25, rim-vs-outside 0.55, heterogeneity 0.08; core [0.987, 0.9, 0.161, 0.0] rim [0.834, 0.741, 0.286, 0.0]
  - track 16 at frame 313: holes 0, rim-vs-core 0.21, rim-vs-outside 0.48, heterogeneity 0.05; core [0.981, 0.821, 0.296, 0.0] rim [0.844, 0.692, 0.382, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 267 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.956, rim/outside 52.3 (aggregate of 267 individuals; 0/267 membrane-like individually; rim level 0.949)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 4.25 (aggregate of 267 individuals; 0/267 membrane-like individually; rim level 0.817)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.62, rim/outside 0.695 (aggregate of 267 individuals; 0/267 membrane-like individually; rim level 0.47)
  - radial I: flat profile (no radial structure; level 0; aggregate of 267 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=3130, R_eq 3.74): none; #4 (t=3130, R_eq 2.99): none; #10 (t=3130, R_eq 3.78): none; #16 (t=3130, R_eq 2.76): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
