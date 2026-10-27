# Evidence pack: digestion-driven-predators (seed 9)

- world: `../../../collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 71 frames x 1000 steps x dt 0.2 = time 14000; grid [128, 128]; wall 492s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out c56work/dh/halffork_s9 --seeds 9 --size 128 128 --frames 70 --spf 1000 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1504, 1.789], min area 6 px

## Measurements
- components: final 42, mean 40.9, max 52; occupancy final 0.11
- tracks: 104; persistent (alive >= 50% of run): 32; longest 69 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [43, 41, 38], H1 [0, 0, 0]
- motion: 41 long-lived tracks moved >= 1 body length; max speed 0.00277/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 4000, default): splits 14, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 12, merge/split ratio 0.857, nucleations 64
- channel total drift (end/start - 1): [-0.0144, None, -1.0, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 36: holes 0, rim-vs-core 0.49, rim-vs-outside 0.14, heterogeneity 0.24; core [0.363, 0.555, 0.352, 0.453, 0.407] rim [0.303, 0.197, 0.368, 0.38, 0.093]
  - track 1 at frame 36: holes 0, rim-vs-core 0.43, rim-vs-outside 0.16, heterogeneity 0.17; core [0.216, 0.636, 0.404, 0.31, 0.272] rim [0.23, 0.247, 0.403, 0.316, 0.09]
  - track 3 at frame 36: holes 0, rim-vs-core 0.48, rim-vs-outside 0.15, heterogeneity 0.24; core [0.399, 0.527, 0.362, 0.501, 0.391] rim [0.285, 0.191, 0.378, 0.376, 0.092]
  - track 65 at frame 55: holes 0, rim-vs-core 0.42, rim-vs-outside 0.14, heterogeneity 0.25; core [0.495, 0.398, 0.313, 0.562, 0.32] rim [0.348, 0.149, 0.341, 0.412, 0.053]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 262 components >= 12 px at frames [12, 23, 35, 47, 58, 70]):
  - radial prey a: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.939, rim/outside 3.54 (aggregate of 262 individuals; 25/262 membrane-like individually; rim level 0.446)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.394, rim/outside 5.38 (aggregate of 262 individuals; 3/262 membrane-like individually; rim level 0.256)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.14, rim/outside 0.932 (aggregate of 262 individuals; 0/262 membrane-like individually; rim level 0.311)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.913, rim/outside 2.95 (aggregate of 262 individuals; 11/262 membrane-like individually; rim level 0.476)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.371, rim/outside 15.2 (aggregate of 262 individuals; 4/262 membrane-like individually; rim level 0.186)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=7200, R_eq 4.92): ['prey a']; #1 (t=7200, R_eq 4.41): ['prey a']; #3 (t=7200, R_eq 4.55): none; #65 (t=11000, R_eq 5.41): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 35.2, max 50; tracks 90, persistent 26; splits 8, persistent splits 4 (K=20), max generation 1, merges 4, merge/split 0.5; moving tracks 47
- species `predator` (channels ['predator b'], own threshold): components final 35, mean 28.7, max 48; tracks 78, persistent 19; splits 3, persistent splits 2 (K=20), max generation 1, merges 3, merge/split 1; moving tracks 47

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
