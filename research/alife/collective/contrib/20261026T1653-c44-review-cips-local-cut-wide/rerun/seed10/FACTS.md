# Evidence pack: cips-layered-divide (seed 10)

- world: `../../world_claim.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 866s; status ok
- command: `python -m labkit.run world_claim.py --out rerun/seed10 --seeds 10 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0215, 0.9747], min area 6 px

## Measurements
- components: final 16, mean 10.9, max 16; occupancy final 0.09
- tracks: 26; persistent (alive >= 50% of run): 7; longest 89 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.25 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00262/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 2000, default): splits 10, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [-0.0, -0.5957, 0.6433, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 77: holes 0, rim-vs-core 0.55, rim-vs-outside 0.62, heterogeneity 0.16; core [0.986, 0.949, 0.052, 0.08] rim [0.786, 0.709, 0.235, 0.489]
  - track 9 at frame 77: holes 0, rim-vs-core 0.55, rim-vs-outside 0.63, heterogeneity 0.16; core [0.989, 0.955, 0.058, 0.079] rim [0.784, 0.71, 0.243, 0.481]
  - track 10 at frame 77: holes 0, rim-vs-core 0.58, rim-vs-outside 0.62, heterogeneity 0.17; core [0.985, 0.946, 0.058, 0.079] rim [0.771, 0.7, 0.244, 0.522]
  - track 18 at frame 97: holes 0, rim-vs-core 0.59, rim-vs-outside 0.61, heterogeneity 0.17; core [0.984, 0.942, 0.053, 0.082] rim [0.764, 0.694, 0.241, 0.534]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 72 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.913, rim/outside 38 (aggregate of 72 individuals; 0/72 membrane-like individually; rim level 0.895)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.882, rim/outside 13.6 (aggregate of 72 individuals; 0/72 membrane-like individually; rim level 0.852)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 27.4, rim/outside 0.652 (aggregate of 72 individuals; 0/72 membrane-like individually; rim level 0.496)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.54, rim/outside 20.8 (aggregate of 72 individuals; 69/72 membrane-like individually; rim level 0.507)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #6 (t=7700, R_eq 7.96): ['s']; #9 (t=7700, R_eq 7.69): ['s']; #10 (t=7700, R_eq 7.96): ['s']; #18 (t=9700, R_eq 8.14): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
