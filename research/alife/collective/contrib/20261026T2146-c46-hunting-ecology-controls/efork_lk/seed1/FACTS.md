# Evidence pack: driven-condensate-prey-predator (seed 1)

- world: `../../world3.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 71 frames x 500 steps x dt 0.2 = time 7000; grid [128, 128]; wall 216s; status ok
- command: `python -m labkit.run collective/work_c46/world3.py --out collective/work_c46/lk/efork_s1 --seeds 1 --frames 70 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.1474, 1.1589], min area 6 px

## Measurements
- components: final 4, mean 11.2, max 20; occupancy final 0.01
- tracks: 29; persistent (alive >= 50% of run): 10; longest 56 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 26.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 4], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 2, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 25
- channel total drift (end/start - 1): [-0.0279, None, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 32: holes 0, rim-vs-core 0.32, rim-vs-outside 0.28, heterogeneity 0.05; core [0.0, 0.955, 0.643, 0.06] rim [0.001, 0.638, 0.638, 0.072]
  - track 5 at frame 36: holes 0, rim-vs-core 0.29, rim-vs-outside 0.26, heterogeneity 0.04; core [0.0, 0.937, 0.617, 0.067] rim [0.002, 0.643, 0.612, 0.076]
  - track 3 at frame 31: holes 0, rim-vs-core 0.32, rim-vs-outside 0.32, heterogeneity 0.05; core [0.0, 0.974, 0.635, 0.053] rim [0.0, 0.653, 0.63, 0.066]
  - track 13 at frame 43: holes 0, rim-vs-core 0.32, rim-vs-outside 0.29, heterogeneity 0.05; core [0.001, 0.94, 0.614, 0.079] rim [0.01, 0.617, 0.613, 0.086]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 67 components >= 12 px at frames [12, 23, 35, 47, 58, 70]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 4.84 (aggregate of 67 individuals; 5/67 membrane-like individually; rim level 0.421)
  - radial predator b: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.91, rim/outside 11.5 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.466)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.23, rim/outside 0.94 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.464)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.929, rim/outside 3.33 (aggregate of 67 individuals; 5/67 membrane-like individually; rim level 0.47)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=3200, R_eq 3.95): none; #5 (t=3600, R_eq 3.29): none; #3 (t=3100, R_eq 4.07): none; #13 (t=4300, R_eq 2.59): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 6.6, max 13; tracks 37, persistent 1; splits 6, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 3
- species `predator` (channels ['predator b'], own threshold): components final 4, mean 6.5, max 14; tracks 21, persistent 4; splits 3, persistent splits 2 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
