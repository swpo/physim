# Evidence pack: digestion-predators-smell (seed 72)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261027T2152-c60-smell-predators/world.py`, family `active-emulsion`
- parent: collective/contrib/20261027T0325-c52-digestion-ecology-claim; mutation: predator fuel-depletion drift chiF 0.5 -> 0.25; before (c52): predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 2113s; status ok
- command: `python -m labkit.run collective/contrib/20261027T2152-c60-smell-predators/world.py --out /tmp/claude-0/smell/big0.5 --seeds 72 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1572, 1.7648], min area 6 px

## Measurements
- components: final 201, mean 178.1, max 204; occupancy final 0.19
- tracks: 797; persistent (alive >= 50% of run): 83; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 23.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [202, 195, 170], H1 [0, 0, 0]
- motion: 333 long-lived tracks moved >= 1 body length; max speed 0.00883/time; max body lengths 9.5
- replication (lineage window K = 20 frames = time 2000, default): splits 123, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 2, merges 175, merge/split ratio 1.42, nucleations 374
- channel total drift (end/start - 1): [-0.0537, None, -0.6126, -0.6027, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 61: holes 0, rim-vs-core 0.45, rim-vs-outside 0.12, heterogeneity 0.20; core [0.346, 0.538, 0.158, 0.379, 0.318] rim [0.293, 0.165, 0.171, 0.313, 0.071]
  - track 39 at frame 62: holes 0, rim-vs-core 0.43, rim-vs-outside 0.13, heterogeneity 0.20; core [0.306, 0.573, 0.177, 0.342, 0.283] rim [0.277, 0.198, 0.188, 0.301, 0.072]
  - track 56 at frame 63: holes 0, rim-vs-core 0.53, rim-vs-outside 0.16, heterogeneity 0.26; core [0.438, 0.54, 0.152, 0.507, 0.434] rim [0.34, 0.166, 0.175, 0.384, 0.096]
  - track 504 at frame 89: holes 0, rim-vs-core 0.41, rim-vs-outside 0.13, heterogeneity 0.20; core [0.312, 0.536, 0.166, 0.342, 0.269] rim [0.277, 0.185, 0.174, 0.296, 0.07]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1133 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.976, rim/outside 3.47 (aggregate of 1133 individuals; 127/1133 membrane-like individually; rim level 0.446)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.368, rim/outside 7.07 (aggregate of 1133 individuals; 16/1133 membrane-like individually; rim level 0.25)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.38, rim/outside 0.856 (aggregate of 1133 individuals; 0/1133 membrane-like individually; rim level 0.164)
  - radial product p: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 3.55 (aggregate of 1133 individuals; 73/1133 membrane-like individually; rim level 0.467)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.315, rim/outside 13.3 (aggregate of 1133 individuals; 22/1133 membrane-like individually; rim level 0.156)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=6100, R_eq 4.33): none; #39 (t=6200, R_eq 4.69): none; #56 (t=6300, R_eq 4.48): none; #504 (t=8900, R_eq 4.58): none
- species `prey` (channels ['prey a'], own threshold): components final 190, mean 174.1, max 194; tracks 733, persistent 92; splits 107, persistent splits 45 (K=20), max generation 3, merges 53, merge/split 0.495; moving tracks 336
- species `predator` (channels ['predator b'], own threshold): components final 191, mean 146.4, max 191; tracks 610, persistent 77; splits 42, persistent splits 23 (K=20), max generation 2, merges 22, merge/split 0.524; moving tracks 322

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 1133 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
