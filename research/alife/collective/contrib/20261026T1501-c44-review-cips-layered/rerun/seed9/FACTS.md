# Evidence pack: cips-layered-divide (seed 9)

- world: `../world_claim.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 161 frames x 1000 steps x dt 0.1 = time 16000; grid [192, 192]; wall 1121s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1405-c44-review-cips-layered/world_claim.py --out collective/contrib/20261026T1405-c44-review-cips-layered/rerun --seeds 9 --frames 160 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0209, 0.9753], min area 6 px

## Measurements
- components: final 17, mean 11.5, max 17; occupancy final 0.09
- tracks: 28; persistent (alive >= 50% of run): 9; longest 158 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.54 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 17, 17], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.00318/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 2000, default): splits 11, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [0.0, -0.5858, 0.6327, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 82: holes 0, rim-vs-core 0.58, rim-vs-outside 0.60, heterogeneity 0.17; core [0.979, 0.925, 0.057, 0.075] rim [0.763, 0.695, 0.232, 0.526]
  - track 8 at frame 101: holes 0, rim-vs-core 0.60, rim-vs-outside 0.63, heterogeneity 0.17; core [0.987, 0.95, 0.055, 0.082] rim [0.76, 0.693, 0.249, 0.54]
  - track 11 at frame 104: holes 0, rim-vs-core 0.58, rim-vs-outside 0.63, heterogeneity 0.17; core [0.987, 0.95, 0.054, 0.082] rim [0.768, 0.697, 0.245, 0.519]
  - track 16 at frame 120: holes 0, rim-vs-core 0.58, rim-vs-outside 0.62, heterogeneity 0.17; core [0.986, 0.946, 0.056, 0.079] rim [0.771, 0.698, 0.242, 0.515]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 74 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.907, rim/outside 32.3 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.878)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 12.7 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.838)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 19.6, rim/outside 0.653 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.498)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.18, rim/outside 19.2 (aggregate of 74 individuals; 68/74 membrane-like individually; rim level 0.525)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #4 (t=8200, R_eq 8.39): ['s']; #8 (t=10100, R_eq 7.9): ['s']; #11 (t=10400, R_eq 7.88): ['s']; #16 (t=12000, R_eq 7.78): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
