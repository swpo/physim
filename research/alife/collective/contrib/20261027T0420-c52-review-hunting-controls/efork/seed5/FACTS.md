# Evidence pack: driven-condensate-prey-predator (seed 5)

- world: `../../../../collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 71 frames x 500 steps x dt 0.2 = time 7000; grid [128, 128]; wall 238s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261027T0420-c52-review-hunting-controls/efork/seed5 --seeds 5 --frames 70 --lineage-k 5 --no-movie`
- segmentation: matter > 0.32 of robust range [0.1417, 1.2472], min area 6 px

## Measurements
- components: final 26, mean 22.5, max 35; occupancy final 0.08
- tracks: 44; persistent (alive >= 50% of run): 18; longest 70 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 27, 25], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 4, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 36
- channel total drift (end/start - 1): [-0.2747, None, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 36: holes 0, rim-vs-core 0.30, rim-vs-outside 0.24, heterogeneity 0.05; core [0.003, 0.817, 0.641, 0.063] rim [0.017, 0.515, 0.637, 0.075]
  - track 2 at frame 37: holes 0, rim-vs-core 0.12, rim-vs-outside 0.37, heterogeneity 0.05; core [0.009, 0.742, 0.601, 0.065] rim [0.016, 0.621, 0.599, 0.07]
  - track 3 at frame 37: holes 0, rim-vs-core 0.31, rim-vs-outside 0.26, heterogeneity 0.05; core [0.007, 0.85, 0.62, 0.066] rim [0.021, 0.536, 0.615, 0.076]
  - track 25 at frame 47: holes 0, rim-vs-core 0.22, rim-vs-outside 0.23, heterogeneity 0.04; core [0.028, 0.748, 0.612, 0.084] rim [0.035, 0.525, 0.611, 0.089]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 137 components >= 12 px at frames [12, 23, 35, 47, 58, 70]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.94, rim/outside 3.07 (aggregate of 137 individuals; 12/137 membrane-like individually; rim level 0.282)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 15.8 (aggregate of 137 individuals; 1/137 membrane-like individually; rim level 0.524)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.14, rim/outside 0.952 (aggregate of 137 individuals; 0/137 membrane-like individually; rim level 0.427)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.974, rim/outside 2.79 (aggregate of 137 individuals; 11/137 membrane-like individually; rim level 0.316)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3600, R_eq 3.74): none; #2 (t=3700, R_eq 3.61): none; #3 (t=3700, R_eq 3.24): none; #25 (t=4700, R_eq 2.33): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 9.6, max 21; tracks 53, persistent 0; splits 8, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 3
- species `predator` (channels ['predator b'], own threshold): components final 25, mean 15.2, max 27; tracks 48, persistent 12; splits 4, persistent splits 2 (K=5), max generation 1, merges 2, merge/split 0.5; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
