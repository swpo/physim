# Evidence pack: driven-condensate-prey-predator (seed 0)

- world: `../../world3.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 71 frames x 500 steps x dt 0.2 = time 7000; grid [128, 128]; wall 214s; status ok
- command: `python -m labkit.run collective/work_c46/world3.py --out collective/work_c46/lk/efork_s0 --seeds 0 --frames 70 --lineage-k 5 --no-movie`
- segmentation: matter > 0.34 of robust range [0.1385, 1.211], min area 6 px

## Measurements
- components: final 21, mean 20.6, max 35; occupancy final 0.06
- tracks: 40; persistent (alive >= 50% of run): 15; longest 67 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 22, 20], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio 1, nucleations 37
- channel total drift (end/start - 1): [-0.188, None, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 37: holes 0, rim-vs-core 0.32, rim-vs-outside 0.25, heterogeneity 0.05; core [0.002, 0.842, 0.639, 0.063] rim [0.016, 0.524, 0.635, 0.075]
  - track 5 at frame 37: holes 0, rim-vs-core 0.29, rim-vs-outside 0.23, heterogeneity 0.05; core [0.003, 0.812, 0.629, 0.063] rim [0.016, 0.522, 0.625, 0.074]
  - track 6 at frame 38: holes 0, rim-vs-core 0.34, rim-vs-outside 0.24, heterogeneity 0.05; core [0.006, 0.849, 0.603, 0.065] rim [0.021, 0.505, 0.6, 0.076]
  - track 0 at frame 35: holes 0, rim-vs-core 0.33, rim-vs-outside 0.24, heterogeneity 0.05; core [0.002, 0.857, 0.63, 0.06] rim [0.015, 0.529, 0.626, 0.074]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 128 components >= 12 px at frames [12, 23, 35, 47, 58, 70]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside 3.22 (aggregate of 128 individuals; 12/128 membrane-like individually; rim level 0.284)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.834, rim/outside 15.8 (aggregate of 128 individuals; 0/128 membrane-like individually; rim level 0.552)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 0.959 (aggregate of 128 individuals; 0/128 membrane-like individually; rim level 0.446)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.945, rim/outside 2.83 (aggregate of 128 individuals; 11/128 membrane-like individually; rim level 0.323)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=3700, R_eq 3.78): none; #5 (t=3700, R_eq 3.66): none; #6 (t=3800, R_eq 3.34): none; #0 (t=3500, R_eq 3.78): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 9.2, max 17; tracks 52, persistent 0; splits 7, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 20, mean 14.0, max 26; tracks 30, persistent 13; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
