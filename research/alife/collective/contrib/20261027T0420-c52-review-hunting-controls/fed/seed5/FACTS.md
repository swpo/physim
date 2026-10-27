# Evidence pack: driven-condensate-prey-predator (seed 5)

- world: `../../../../collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 71 frames x 500 steps x dt 0.2 = time 7000; grid [128, 128]; wall 235s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261027T0420-c52-review-hunting-controls/fed/seed5 --seeds 5 --frames 70 --lineage-k 5 --no-movie`
- segmentation: matter > 0.33 of robust range [0.1413, 1.2136], min area 6 px

## Measurements
- components: final 23, mean 22.0, max 35; occupancy final 0.08
- tracks: 51; persistent (alive >= 50% of run): 16; longest 68 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.67 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 24, 17], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 7, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 37
- channel total drift (end/start - 1): [-0.1821, None, -0.4464, -0.618]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 35: holes 0, rim-vs-core 0.32, rim-vs-outside 0.25, heterogeneity 0.05; core [0.004, 0.852, 0.543, 0.003] rim [0.017, 0.535, 0.537, 0.014]
  - track 3 at frame 37: holes 0, rim-vs-core 0.33, rim-vs-outside 0.27, heterogeneity 0.05; core [0.008, 0.893, 0.509, 0.006] rim [0.022, 0.565, 0.504, 0.017]
  - track 10 at frame 38: holes 0, rim-vs-core 0.35, rim-vs-outside 0.28, heterogeneity 0.06; core [0.006, 0.901, 0.523, 0.006] rim [0.022, 0.555, 0.518, 0.018]
  - track 25 at frame 47: holes 0, rim-vs-core 0.24, rim-vs-outside 0.24, heterogeneity 0.04; core [0.029, 0.789, 0.499, 0.024] rim [0.036, 0.553, 0.498, 0.03]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 131 components >= 12 px at frames [12, 23, 35, 47, 58, 70]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.929, rim/outside 3.49 (aggregate of 131 individuals; 12/131 membrane-like individually; rim level 0.318)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.789, rim/outside 11.3 (aggregate of 131 individuals; 2/131 membrane-like individually; rim level 0.489)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.22, rim/outside 0.933 (aggregate of 131 individuals; 0/131 membrane-like individually; rim level 0.399)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.969, rim/outside 4.01 (aggregate of 131 individuals; 14/131 membrane-like individually; rim level 0.322)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3500, R_eq 3.87): none; #3 (t=3700, R_eq 3.24): none; #10 (t=3800, R_eq 3.34): none; #25 (t=4700, R_eq 2.33): none
- species `prey` (channels ['prey a'], own threshold): components final 3, mean 10.2, max 21; tracks 63, persistent 0; splits 12, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 5
- species `predator` (channels ['predator b'], own threshold): components final 18, mean 14.6, max 27; tracks 53, persistent 12; splits 7, persistent splits 2 (K=5), max generation 1, merges 2, merge/split 0.286; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
