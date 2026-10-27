# Evidence pack: cips-layered-chemostat (seed 2)

- world: `../../20261026T1819-c44-cips-chemostat-sighting/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c44: initial noise 0.03 -> 0.02 (fewer nucleations); otherwise c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 301 frames x 1000 steps x dt 0.1 = time 30000; grid [192, 192]; wall 1307s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1819-c44-cips-chemostat-sighting/world.py --out collective/contrib/20261027T0321-c51-review-cips-chemostat/nowash_s2 --seeds 2 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0227, 0.9742], min area 6 px

## Measurements
- components: final 17, mean 14.7, max 17; occupancy final 0.09
- tracks: 27; persistent (alive >= 50% of run): 17; longest 294 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.11 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.00414/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 10, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [0.0, -0.5874, 0.6344, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 154: holes 0, rim-vs-core 0.54, rim-vs-outside 0.63, heterogeneity 0.16; core [0.989, 0.948, 0.065, 0.077] rim [0.786, 0.703, 0.251, 0.468]
  - track 9 at frame 169: holes 0, rim-vs-core 0.54, rim-vs-outside 0.62, heterogeneity 0.16; core [0.988, 0.946, 0.063, 0.078] rim [0.787, 0.703, 0.249, 0.473]
  - track 10 at frame 169: holes 0, rim-vs-core 0.57, rim-vs-outside 0.63, heterogeneity 0.16; core [0.986, 0.939, 0.058, 0.081] rim [0.769, 0.69, 0.25, 0.507]
  - track 19 at frame 187: holes 0, rim-vs-core 0.55, rim-vs-outside 0.62, heterogeneity 0.16; core [0.985, 0.937, 0.057, 0.08] rim [0.777, 0.696, 0.245, 0.484]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 94 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.96, rim/outside 54.1 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.951)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.902, rim/outside 15.4 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.886)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 32.5, rim/outside 0.663 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.515)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 6.37, rim/outside 32 (aggregate of 94 individuals; 90/94 membrane-like individually; rim level 0.698)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #5 (t=15400, R_eq 7.61): ['s']; #9 (t=16900, R_eq 7.69): ['s']; #10 (t=16900, R_eq 8): ['s']; #19 (t=18700, R_eq 8.02): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
