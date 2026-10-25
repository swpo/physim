# Evidence pack: cips-inhib (seed 6)

- world: `../../../20261025T2130-c23-cips-inhibitor-arrest/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 66s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out collective/contrib/20261025T2223-c25-review-cipsinhib/noI --seeds 5 6 --frames 300 --size 128 128 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0, 0.999], min area 6 px

## Measurements
- components: final 45, mean 50.9, max 78; occupancy final 0.14
- tracks: 115; persistent (alive >= 50% of run): 46; longest 282 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [45, 45, 45], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00595/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 31, merge/split ratio n/a, nucleations 84
- channel total drift (end/start - 1): [0.0, -0.2227, 0.1536, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 161: holes 0, rim-vs-core 0.25, rim-vs-outside 0.49, heterogeneity 0.07; core [0.974, 0.835, 0.221, 0.0] rim [0.797, 0.689, 0.327, 0.0]
  - track 1 at frame 161: holes 0, rim-vs-core 0.20, rim-vs-outside 0.45, heterogeneity 0.05; core [0.981, 0.829, 0.233, 0.0] rim [0.857, 0.706, 0.321, 0.0]
  - track 3 at frame 161: holes 0, rim-vs-core 0.30, rim-vs-outside 0.51, heterogeneity 0.07; core [0.98, 0.888, 0.13, 0.0] rim [0.784, 0.705, 0.273, 0.0]
  - track 4 at frame 161: holes 0, rim-vs-core 0.26, rim-vs-outside 0.49, heterogeneity 0.07; core [0.976, 0.838, 0.197, 0.0] rim [0.797, 0.69, 0.305, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 320 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.948, rim/outside 46.1 (aggregate of 320 individuals; 0/320 membrane-like individually; rim level 0.94)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 3.91 (aggregate of 320 individuals; 0/320 membrane-like individually; rim level 0.812)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.84, rim/outside 0.684 (aggregate of 320 individuals; 0/320 membrane-like individually; rim level 0.449)
  - radial I: flat profile (no radial structure; level 0; aggregate of 320 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1610, R_eq 2.99): none; #1 (t=1610, R_eq 2.65): none; #3 (t=1610, R_eq 3.7): none; #4 (t=1610, R_eq 3.04): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
