# Evidence pack: digestion-driven-predators (seed 13)

- world: `../../20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 255s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out collective/contrib/c57-work/dfork13_128 --seeds 13 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.28 of robust range [0.0148, 1.7609], min area 6 px

## Measurements
- components: final 0, mean 29.8, max 50; occupancy final 0.00
- tracks: 102; persistent (alive >= 50% of run): 14; longest 62 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 18.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 7, 1], H1 [6, 0, 0]
- motion: 40 long-lived tracks moved >= 1 body length; max speed 0.00833/time; max body lengths 3.4
- replication (lineage window K = 20 frames = time 2000, default): splits 18, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 13, merge/split ratio 0.722, nucleations 54
- channel total drift (end/start - 1): [-0.9999, None, 0.0, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 33: holes 0, rim-vs-core 0.46, rim-vs-outside 0.14, heterogeneity 0.24; core [0.463, 0.55, 0.189, 0.452, 0.368] rim [0.429, 0.186, 0.2, 0.399, 0.088]
  - track 11 at frame 33: holes 0, rim-vs-core 0.49, rim-vs-outside 0.26, heterogeneity 0.25; core [0.423, 0.551, 0.18, 0.389, 0.323] rim [0.54, 0.145, 0.157, 0.522, 0.102]
  - track 13 at frame 33: holes 0, rim-vs-core 0.48, rim-vs-outside 0.14, heterogeneity 0.25; core [0.539, 0.5, 0.137, 0.529, 0.395] rim [0.48, 0.156, 0.159, 0.446, 0.077]
  - track 46 at frame 47: holes 0, rim-vs-core 0.56, rim-vs-outside 0.18, heterogeneity 0.24; core [0.632, 0.471, 0.12, 0.646, 0.498] rim [0.513, 0.127, 0.147, 0.491, 0.11]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 162 components >= 12 px at frames [13, 27, 40, 53]):
  - radial prey a: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 0.985, rim/outside 1.98 (aggregate of 162 individuals; 8/162 membrane-like individually; rim level 0.562)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.39, rim/outside 7.52 (aggregate of 162 individuals; 2/162 membrane-like individually; rim level 0.257)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.41, rim/outside 0.845 (aggregate of 162 individuals; 0/162 membrane-like individually; rim level 0.18)
  - radial product p: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 0.965, rim/outside 2.57 (aggregate of 162 individuals; 16/162 membrane-like individually; rim level 0.534)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.339, rim/outside 14.3 (aggregate of 162 individuals; 3/162 membrane-like individually; rim level 0.165)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=3300, R_eq 5.14): none; #11 (t=3300, R_eq 5.73): none; #13 (t=3300, R_eq 5.23): none; #46 (t=4700, R_eq 4.37): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 31.4, max 50; tracks 222, persistent 6; splits 73, persistent splits 7 (K=20), max generation 1, merges 31, merge/split 0.425; moving tracks 35
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 21.5, max 47; tracks 80, persistent 15; splits 8, persistent splits 4 (K=20), max generation 1, merges 3, merge/split 0.375; moving tracks 43

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
