# Evidence pack: digestion-driven-predators (seed 8)

- world: `../../../collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1828s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out c56work/py/pack256_s8 --seeds 8 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1578, 1.7947], min area 6 px

## Measurements
- components: final 187, mean 174.0, max 204; occupancy final 0.21
- tracks: 804; persistent (alive >= 50% of run): 80; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [197, 182, 153], H1 [0, 0, 0]
- motion: 307 long-lived tracks moved >= 1 body length; max speed 0.00828/time; max body lengths 9.0
- replication (lineage window K = 20 frames = time 2000, default): splits 159, persistent splits 47 (0 more failed only because the siblings re-merged within K), max generation 3, merges 167, merge/split ratio 1.05, nucleations 322
- channel total drift (end/start - 1): [-0.0519, None, -0.6151, -0.6028, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 59 at frame 62: holes 0, rim-vs-core 0.50, rim-vs-outside 0.17, heterogeneity 0.25; core [0.416, 0.525, 0.177, 0.485, 0.392] rim [0.333, 0.162, 0.198, 0.38, 0.08]
  - track 67 at frame 63: holes 0, rim-vs-core 0.48, rim-vs-outside 0.16, heterogeneity 0.22; core [0.403, 0.524, 0.186, 0.468, 0.351] rim [0.318, 0.152, 0.202, 0.363, 0.085]
  - track 69 at frame 63: holes 0, rim-vs-core 0.49, rim-vs-outside 0.18, heterogeneity 0.26; core [0.461, 0.497, 0.154, 0.522, 0.388] rim [0.366, 0.144, 0.175, 0.406, 0.079]
  - track 518 at frame 100: holes 0, rim-vs-core 0.50, rim-vs-outside 0.18, heterogeneity 0.27; core [0.512, 0.464, 0.128, 0.567, 0.405] rim [0.374, 0.146, 0.158, 0.405, 0.086]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1105 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.979, rim/outside 4.06 (aggregate of 1105 individuals; 152/1105 membrane-like individually; rim level 0.462)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.345, rim/outside 5.87 (aggregate of 1105 individuals; 13/1105 membrane-like individually; rim level 0.227)
  - radial fuel F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.43, rim/outside 0.854 (aggregate of 1105 individuals; 0/1105 membrane-like individually; rim level 0.178)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.953, rim/outside 4.12 (aggregate of 1105 individuals; 94/1105 membrane-like individually; rim level 0.481)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.293, rim/outside 12 (aggregate of 1105 individuals; 25/1105 membrane-like individually; rim level 0.144)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #59 (t=6200, R_eq 4.48): none; #67 (t=6300, R_eq 4.07): none; #69 (t=6300, R_eq 4.51): none; #518 (t=10000, R_eq 4.82): none
- species `prey` (channels ['prey a'], own threshold): components final 182, mean 172.7, max 197; tracks 762, persistent 94; splits 160, persistent splits 63 (K=20), max generation 3, merges 66, merge/split 0.412; moving tracks 307
- species `predator` (channels ['predator b'], own threshold): components final 177, mean 144.3, max 191; tracks 583, persistent 84; splits 77, persistent splits 39 (K=20), max generation 3, merges 15, merge/split 0.195; moving tracks 305

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 1105 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
