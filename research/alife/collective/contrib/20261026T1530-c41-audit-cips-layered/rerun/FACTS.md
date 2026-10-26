# Evidence pack: cips-layered-divide (seed 13)

- world: `../../20261026T1100-c40-cips-layered-divide-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 141 frames x 1000 steps x dt 0.1 = time 14000; grid [192, 192]; wall 1045s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py --out collective/contrib/20261026T1530-c41-audit-cips-layered/rerun --seeds 13 --frames 140 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0205, 0.977], min area 6 px

## Measurements
- components: final 19, mean 13.1, max 19; occupancy final 0.09
- tracks: 32; persistent (alive >= 50% of run): 5; longest 109 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.51 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 19, 19], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00358/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 13, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [0.0, -0.573, 0.619, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 86: holes 0, rim-vs-core 0.58, rim-vs-outside 0.59, heterogeneity 0.17; core [0.971, 0.904, 0.064, 0.076] rim [0.754, 0.69, 0.226, 0.538]
  - track 10 at frame 89: holes 0, rim-vs-core 0.54, rim-vs-outside 0.63, heterogeneity 0.16; core [0.986, 0.944, 0.048, 0.08] rim [0.785, 0.701, 0.235, 0.48]
  - track 13 at frame 89: holes 0, rim-vs-core 0.54, rim-vs-outside 0.62, heterogeneity 0.16; core [0.986, 0.944, 0.051, 0.08] rim [0.783, 0.702, 0.235, 0.482]
  - track 18 at frame 109: holes 0, rim-vs-core 0.32, rim-vs-outside 0.79, heterogeneity 0.16; core [0.985, 0.937, 0.069, 0.077] rim [0.862, 0.801, 0.165, 0.327]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 87 components >= 12 px at frames [24, 47, 71, 93, 116, 140]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.92, rim/outside 43.2 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.907)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.883, rim/outside 13.4 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.856)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 29.7, rim/outside 0.656 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.496)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 6.13, rim/outside 25.5 (aggregate of 87 individuals; 84/87 membrane-like individually; rim level 0.637)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #8 (t=8600, R_eq 8.88): ['s']; #10 (t=8900, R_eq 7.84): ['s']; #13 (t=8900, R_eq 7.74): ['s']; #18 (t=10900, R_eq 7.59): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
