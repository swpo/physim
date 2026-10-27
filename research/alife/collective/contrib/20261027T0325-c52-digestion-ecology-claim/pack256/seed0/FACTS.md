# Evidence pack: digestion-driven-predators (seed 0)

- world: `../../world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1706s; status ok
- command: `python -m labkit.run c52work/world.py --out c52work/pack256/seed0 --seeds 0 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1565, 1.7936], min area 6 px

## Measurements
- components: final 197, mean 175.2, max 203; occupancy final 0.20
- tracks: 775; persistent (alive >= 50% of run): 80; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 22.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [205, 191, 162], H1 [0, 0, 0]
- motion: 321 long-lived tracks moved >= 1 body length; max speed 0.00809/time; max body lengths 8.8
- replication (lineage window K = 20 frames = time 2000, default): splits 152, persistent splits 48 (0 more failed only because the siblings re-merged within K), max generation 3, merges 157, merge/split ratio 1.03, nucleations 314
- channel total drift (end/start - 1): [-0.0514, None, -0.6157, -0.602, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 62: holes 0, rim-vs-core 0.46, rim-vs-outside 0.16, heterogeneity 0.26; core [0.468, 0.459, 0.133, 0.519, 0.368] rim [0.361, 0.147, 0.161, 0.39, 0.069]
  - track 29 at frame 62: holes 0, rim-vs-core 0.45, rim-vs-outside 0.16, heterogeneity 0.26; core [0.481, 0.441, 0.118, 0.512, 0.345] rim [0.358, 0.147, 0.146, 0.371, 0.068]
  - track 56 at frame 63: holes 0, rim-vs-core 0.56, rim-vs-outside 0.25, heterogeneity 0.27; core [0.654, 0.353, 0.102, 0.711, 0.406] rim [0.331, 0.259, 0.157, 0.364, 0.127]
  - track 550 at frame 104: holes 0, rim-vs-core 0.46, rim-vs-outside 0.13, heterogeneity 0.26; core [0.464, 0.443, 0.123, 0.501, 0.35] rim [0.348, 0.139, 0.154, 0.365, 0.061]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1120 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 0.986, rim/outside 3.98 (aggregate of 1120 individuals; 129/1120 membrane-like individually; rim level 0.463)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.343, rim/outside 6.11 (aggregate of 1120 individuals; 12/1120 membrane-like individually; rim level 0.229)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.43, rim/outside 0.854 (aggregate of 1120 individuals; 0/1120 membrane-like individually; rim level 0.175)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.956, rim/outside 4.04 (aggregate of 1120 individuals; 73/1120 membrane-like individually; rim level 0.479)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.292, rim/outside 12.2 (aggregate of 1120 individuals; 17/1120 membrane-like individually; rim level 0.145)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #12 (t=6200, R_eq 4.92): none; #29 (t=6200, R_eq 5.01): none; #56 (t=6300, R_eq 4.72): none; #550 (t=10400, R_eq 5.11): ['prey a']
- species `prey` (channels ['prey a'], own threshold): components final 195, mean 174.8, max 200; tracks 736, persistent 97; splits 150, persistent splits 65 (K=20), max generation 5, merges 58, merge/split 0.387; moving tracks 321
- species `predator` (channels ['predator b'], own threshold): components final 189, mean 145.2, max 196; tracks 581, persistent 81; splits 76, persistent splits 49 (K=20), max generation 4, merges 15, merge/split 0.197; moving tracks 311

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 1120 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
