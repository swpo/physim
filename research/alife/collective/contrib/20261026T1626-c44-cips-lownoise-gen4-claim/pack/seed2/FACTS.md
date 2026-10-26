# Evidence pack: cips-layered-lownoise (seed 2)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c44: initial noise 0.03 -> 0.02 (fewer nucleations); otherwise c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 251 frames x 1000 steps x dt 0.1 = time 25000; grid [192, 192]; wall 1531s; status ok
- command: `python -m labkit.run world.py --out pack/seed2 --seeds 2 --frames 250 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0212, 0.9751], min area 6 px

## Measurements
- components: final 17, mean 8.3, max 17; occupancy final 0.09
- tracks: 32; persistent (alive >= 50% of run): 3; longest 159 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.64 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.00416/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 2000, default): splits 15, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 2
- channel total drift (end/start - 1): [0.0, -0.588, 0.6337, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 172: holes 0, rim-vs-core 0.54, rim-vs-outside 0.60, heterogeneity 0.16; core [0.976, 0.928, 0.043, 0.076] rim [0.775, 0.714, 0.204, 0.506]
  - track 11 at frame 172: holes 0, rim-vs-core 0.56, rim-vs-outside 0.60, heterogeneity 0.16; core [0.976, 0.928, 0.043, 0.078] rim [0.769, 0.709, 0.207, 0.525]
  - track 13 at frame 179: holes 0, rim-vs-core 0.37, rim-vs-outside 0.74, heterogeneity 0.17; core [0.975, 0.927, 0.043, 0.082] rim [0.839, 0.786, 0.152, 0.376]
  - track 24 at frame 223: holes 0, rim-vs-core 0.56, rim-vs-outside 0.61, heterogeneity 0.16; core [0.98, 0.938, 0.034, 0.08] rim [0.777, 0.711, 0.209, 0.514]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 59 components >= 12 px at frames [42, 84, 126, 166, 208, 250]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 30.4 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.854)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.869, rim/outside 11.4 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.831)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 23.7, rim/outside 0.644 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.477)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.28, rim/outside 16.8 (aggregate of 59 individuals; 53/59 membrane-like individually; rim level 0.511)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #8 (t=17200, R_eq 8.78): ['s']; #11 (t=17200, R_eq 8.7): ['s']; #13 (t=17900, R_eq 8.59): ['s']; #24 (t=22300, R_eq 8.65): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
