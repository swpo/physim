# Evidence pack: cips-layered-chemostat (seed 2)

- world: `../../20261026T1819-c44-cips-chemostat-sighting/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c44: initial noise 0.03 -> 0.02 (fewer nucleations); otherwise c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 301 frames x 1000 steps x dt 0.1 = time 30000; grid [192, 192]; wall 1687s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1819-c44-cips-chemostat-sighting/world.py --out collective/contrib/c49rev6/W800s2 --seeds 2 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0213, 0.9754], min area 6 px

## Measurements
- components: final 11, mean 11.9, max 17; occupancy final 0.07
- tracks: 61; persistent (alive >= 50% of run): 1; longest 162 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.72 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.00414/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 27, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [-0.0157, -0.6492, 0.7006, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 124: holes 0, rim-vs-core 0.47, rim-vs-outside 0.67, heterogeneity 0.16; core [0.982, 0.944, 0.046, 0.08] rim [0.807, 0.74, 0.211, 0.426]
  - track 12 at frame 116: holes 0, rim-vs-core 0.56, rim-vs-outside 0.63, heterogeneity 0.16; core [0.989, 0.956, 0.059, 0.079] rim [0.779, 0.707, 0.244, 0.494]
  - track 5 at frame 76: holes 0, rim-vs-core 0.59, rim-vs-outside 0.61, heterogeneity 0.17; core [0.98, 0.934, 0.055, 0.079] rim [0.757, 0.691, 0.238, 0.538]
  - track 53 at frame 285: holes 0, rim-vs-core 0.56, rim-vs-outside 0.61, heterogeneity 0.16; core [0.985, 0.944, 0.047, 0.084] rim [0.773, 0.697, 0.231, 0.506]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 75 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.902, rim/outside 34.1 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.88)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 12.8 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.841)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 23.2, rim/outside 0.652 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.487)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.47, rim/outside 19.3 (aggregate of 75 individuals; 68/75 membrane-like individually; rim level 0.522)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #11 (t=12400, R_eq 8.08): ['s']; #12 (t=11600, R_eq 7.63): ['s']; #5 (t=7600, R_eq 8.29): ['s']; #53 (t=28500, R_eq 8.06): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
