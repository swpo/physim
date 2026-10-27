# Evidence pack: driven-condensate-prey-predator (seed 16)

- world: `../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 238s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261027T0519-c51-review-hunting-controls/efork128_s16 --seeds 16 --frames 80 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.1446, 1.1718], min area 6 px

## Measurements
- components: final 12, mean 14.4, max 28; occupancy final 0.03
- tracks: 36; persistent (alive >= 50% of run): 11; longest 76 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 30
- channel total drift (end/start - 1): [-0.08, None, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 43: holes 0, rim-vs-core 0.32, rim-vs-outside 0.26, heterogeneity 0.05; core [0.004, 0.868, 0.602, 0.073] rim [0.016, 0.544, 0.6, 0.083]
  - track 4 at frame 44: holes 0, rim-vs-core 0.12, rim-vs-outside 0.39, heterogeneity 0.05; core [0.008, 0.812, 0.591, 0.076] rim [0.013, 0.693, 0.591, 0.079]
  - track 5 at frame 44: holes 0, rim-vs-core 0.31, rim-vs-outside 0.27, heterogeneity 0.05; core [0.009, 0.87, 0.589, 0.077] rim [0.021, 0.563, 0.587, 0.085]
  - track 7 at frame 44: holes 0, rim-vs-core 0.26, rim-vs-outside 0.32, heterogeneity 0.05; core [0.005, 0.867, 0.596, 0.074] rim [0.016, 0.605, 0.595, 0.082]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 87 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.82, rim/outside 3.04 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.286)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside 16.6 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.566)
  - radial fuel F: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.13, rim/outside 0.963 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.38)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.881, rim/outside 2.78 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.32)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=4300, R_eq 3.19): none; #4 (t=4400, R_eq 2.99): none; #5 (t=4400, R_eq 2.82): none; #7 (t=4400, R_eq 3.14): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 7.0, max 15; tracks 40, persistent 0; splits 5, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 4
- species `predator` (channels ['predator b'], own threshold): components final 12, mean 9.4, max 16; tracks 29, persistent 6; splits 3, persistent splits 0 (K=5), max generation 0, merges 2, merge/split 0.667; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
