# Evidence pack: digestion-driven-predators (seed 5)

- world: `../../20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1469s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out collective/contrib/c53-rev-dig/twin256 --seeds 5 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.49 of robust range [0.1413, 0.879], min area 6 px

## Measurements
- components: final 158, mean 152.0, max 162; occupancy final 0.18
- tracks: 165; persistent (alive >= 50% of run): 158; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [158, 158, 158], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.000756/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 164
- channel total drift (end/start - 1): [-0.0, None, -0.6467, -0.5827, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 0, rim-vs-core 0.29, rim-vs-outside 0.41, heterogeneity 0.07; core [0.902, 0.0, 0.039, 0.889, 0.0] rim [0.701, 0.0, 0.08, 0.687, 0.0]
  - track 1 at frame 61: holes 0, rim-vs-core 0.40, rim-vs-outside 0.29, heterogeneity 0.07; core [0.88, 0.0, 0.036, 0.851, 0.0] rim [0.597, 0.0, 0.094, 0.578, 0.0]
  - track 2 at frame 61: holes 0, rim-vs-core 0.38, rim-vs-outside 0.28, heterogeneity 0.06; core [0.883, 0.0, 0.028, 0.837, 0.0] rim [0.607, 0.0, 0.091, 0.585, 0.0]
  - track 3 at frame 61: holes 0, rim-vs-core 0.36, rim-vs-outside 0.30, heterogeneity 0.06; core [0.901, 0.0, 0.036, 0.882, 0.0] rim [0.649, 0.0, 0.089, 0.631, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 950 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 22.3 (aggregate of 950 individuals; 0/950 membrane-like individually; rim level 0.856)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 950 individuals)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 8.26, rim/outside 0.702 (aggregate of 950 individuals; 0/950 membrane-like individually; rim level 0.162)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 20.5 (aggregate of 950 individuals; 0/950 membrane-like individually; rim level 0.84)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 950 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=6100, R_eq 4.65): none; #1 (t=6100, R_eq 5.05): none; #2 (t=6100, R_eq 5.5): none; #3 (t=6100, R_eq 4.69): none
- species `prey` (channels ['prey a'], own threshold): components final 158, mean 155.9, max 163; tracks 178, persistent 157; splits 0, persistent splits 0 (K=20), max generation 0, merges 3, merge/split n/a; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
