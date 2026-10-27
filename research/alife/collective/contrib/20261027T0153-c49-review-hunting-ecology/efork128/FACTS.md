# Evidence pack: driven-condensate-prey-predator (seed 9)

- world: `../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 71 frames x 500 steps x dt 0.2 = time 7000; grid [128, 128]; wall 241s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/c49rev4/efork128 --seeds 9 --frames 70 --lineage-k 5 --no-movie`
- segmentation: matter > 0.33 of robust range [0.1376, 1.2376], min area 6 px

## Measurements
- components: final 27, mean 22.3, max 39; occupancy final 0.08
- tracks: 41; persistent (alive >= 50% of run): 18; longest 68 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 28, 27], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 41
- channel total drift (end/start - 1): [-0.2747, None, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 37: holes 0, rim-vs-core 0.28, rim-vs-outside 0.22, heterogeneity 0.05; core [0.006, 0.77, 0.617, 0.063] rim [0.02, 0.491, 0.613, 0.074]
  - track 1 at frame 37: holes 0, rim-vs-core 0.31, rim-vs-outside 0.27, heterogeneity 0.05; core [0.003, 0.859, 0.635, 0.063] rim [0.018, 0.547, 0.631, 0.074]
  - track 3 at frame 38: holes 0, rim-vs-core 0.31, rim-vs-outside 0.24, heterogeneity 0.05; core [0.006, 0.82, 0.624, 0.065] rim [0.021, 0.515, 0.62, 0.075]
  - track 4 at frame 38: holes 0, rim-vs-core 0.32, rim-vs-outside 0.23, heterogeneity 0.05; core [0.008, 0.789, 0.609, 0.064] rim [0.023, 0.472, 0.605, 0.075]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 142 components >= 12 px at frames [12, 23, 35, 47, 58, 70]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.989, rim/outside 2.7 (aggregate of 142 individuals; 10/142 membrane-like individually; rim level 0.255)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.789, rim/outside 17.9 (aggregate of 142 individuals; 0/142 membrane-like individually; rim level 0.567)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.11, rim/outside 0.976 (aggregate of 142 individuals; 0/142 membrane-like individually; rim level 0.437)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 2.57 (aggregate of 142 individuals; 9/142 membrane-like individually; rim level 0.298)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3700, R_eq 3.78): none; #1 (t=3700, R_eq 3.43): none; #3 (t=3800, R_eq 3.34): none; #4 (t=3800, R_eq 3.52): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 9.1, max 19; tracks 56, persistent 0; splits 6, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 4
- species `predator` (channels ['predator b'], own threshold): components final 27, mean 15.9, max 32; tracks 39, persistent 15; splits 0, persistent splits 0 (K=5), max generation 0, merges 1, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
