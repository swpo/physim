# Evidence pack: cips-layered-lownoise (seed 1)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c44: initial noise 0.03 -> 0.02 (fewer nucleations); otherwise c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 251 frames x 1000 steps x dt 0.1 = time 25000; grid [192, 192]; wall 1908s; status ok
- command: `python -m labkit.run world.py --out pack/seed1 --seeds 1 --frames 250 --no-movie`
- segmentation: matter > 0.50 of robust range [0.021, 0.9757], min area 6 px

## Measurements
- components: final 18, mean 13.1, max 18; occupancy final 0.09
- tracks: 32; persistent (alive >= 50% of run): 12; longest 215 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.49 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [0, 0, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.00374/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 2000, default): splits 14, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 4
- channel total drift (end/start - 1): [0.0, -0.5813, 0.6264, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 143: holes 0, rim-vs-core 0.58, rim-vs-outside 0.62, heterogeneity 0.17; core [0.983, 0.935, 0.048, 0.083] rim [0.767, 0.691, 0.236, 0.519]
  - track 13 at frame 162: holes 0, rim-vs-core 0.52, rim-vs-outside 0.63, heterogeneity 0.16; core [0.987, 0.947, 0.052, 0.078] rim [0.791, 0.707, 0.234, 0.458]
  - track 14 at frame 162: holes 0, rim-vs-core 0.52, rim-vs-outside 0.62, heterogeneity 0.15; core [0.986, 0.942, 0.05, 0.078] rim [0.794, 0.707, 0.23, 0.453]
  - track 26 at frame 191: holes 0, rim-vs-core 0.46, rim-vs-outside 0.69, heterogeneity 0.16; core [0.989, 0.955, 0.049, 0.079] rim [0.819, 0.739, 0.216, 0.402]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 87 components >= 12 px at frames [42, 84, 126, 166, 208, 250]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.939, rim/outside 45.4 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.926)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.891, rim/outside 14.2 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.869)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 29.4, rim/outside 0.659 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.5)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 6.05, rim/outside 27.6 (aggregate of 87 individuals; 82/87 membrane-like individually; rim level 0.651)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #6 (t=14300, R_eq 8.16): ['s']; #13 (t=16200, R_eq 7.69): ['s']; #14 (t=16200, R_eq 7.84): ['s']; #26 (t=19100, R_eq 7.61): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
