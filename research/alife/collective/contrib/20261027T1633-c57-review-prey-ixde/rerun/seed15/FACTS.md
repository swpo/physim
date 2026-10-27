# Evidence pack: digestion-driven-predators (seed 15)

- world: `../../20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1767s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out collective/contrib/c57-w12/rerun --seeds 15 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1574, 1.7972], min area 6 px

## Measurements
- components: final 185, mean 175.8, max 203; occupancy final 0.21
- tracks: 751; persistent (alive >= 50% of run): 80; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [197, 188, 156], H1 [0, 0, 0]
- motion: 318 long-lived tracks moved >= 1 body length; max speed 0.00851/time; max body lengths 8.4
- replication (lineage window K = 20 frames = time 2000, default): splits 132, persistent splits 43 (0 more failed only because the siblings re-merged within K), max generation 3, merges 164, merge/split ratio 1.24, nucleations 323
- channel total drift (end/start - 1): [-0.0535, None, -0.6158, -0.6048, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 61: holes 0, rim-vs-core 0.42, rim-vs-outside 0.13, heterogeneity 0.21; core [0.351, 0.52, 0.17, 0.386, 0.272] rim [0.323, 0.16, 0.178, 0.344, 0.062]
  - track 97 at frame 63: holes 0, rim-vs-core 0.43, rim-vs-outside 0.17, heterogeneity 0.26; core [0.468, 0.448, 0.123, 0.501, 0.31] rim [0.369, 0.133, 0.145, 0.387, 0.058]
  - track 94 at frame 63: holes 0, rim-vs-core 0.24, rim-vs-outside 0.12, heterogeneity 0.16; core [0.386, 0.355, 0.156, 0.42, 0.116] rim [0.321, 0.153, 0.17, 0.343, 0.032]
  - track 553 at frame 103: holes 0, rim-vs-core 0.49, rim-vs-outside 0.20, heterogeneity 0.26; core [0.462, 0.492, 0.157, 0.528, 0.421] rim [0.286, 0.249, 0.195, 0.321, 0.091]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1111 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.985, rim/outside 3.95 (aggregate of 1111 individuals; 150/1111 membrane-like individually; rim level 0.463)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.344, rim/outside 5.77 (aggregate of 1111 individuals; 29/1111 membrane-like individually; rim level 0.225)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.43, rim/outside 0.854 (aggregate of 1111 individuals; 0/1111 membrane-like individually; rim level 0.173)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.954, rim/outside 4.02 (aggregate of 1111 individuals; 84/1111 membrane-like individually; rim level 0.478)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.297, rim/outside 12 (aggregate of 1111 individuals; 34/1111 membrane-like individually; rim level 0.143)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=6100, R_eq 4.41): none; #97 (t=6300, R_eq 5.01): none; #94 (t=6300, R_eq 4.51): none; #553 (t=10300, R_eq 4.79): ['prey a', 'product p']
- species `prey` (channels ['prey a'], own threshold): components final 186, mean 175.7, max 198; tracks 713, persistent 97; splits 139, persistent splits 54 (K=20), max generation 4, merges 62, merge/split 0.446; moving tracks 313
- species `predator` (channels ['predator b'], own threshold): components final 182, mean 146.2, max 194; tracks 571, persistent 90; splits 66, persistent splits 40 (K=20), max generation 3, merges 25, merge/split 0.379; moving tracks 304

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 1111 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
