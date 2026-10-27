# Evidence pack: digestion-predators-smell (seed 71)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261027T2200-c60-smell-tmp/world.py`, family `active-emulsion`
- parent: collective/contrib/20261027T0325-c52-digestion-ecology-claim; mutation: predator fuel-depletion drift chiF 0.5 -> 0.25; before (c52): predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 273s; status ok
- command: `python -m labkit.run collective/contrib/20261027T2200-c60-smell-tmp/world.py --out /tmp/claude-0/smell/chiS0 --seeds 71 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1527, 1.8176], min area 6 px

## Measurements
- components: final 43, mean 38.5, max 48; occupancy final 0.21
- tracks: 108; persistent (alive >= 50% of run): 26; longest 77 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [45, 44, 42], H1 [0, 0, 0]
- motion: 48 long-lived tracks moved >= 1 body length; max speed 0.00787/time; max body lengths 5.2
- replication (lineage window K = 20 frames = time 2000, default): splits 17, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 1, merges 15, merge/split ratio 0.882, nucleations 59
- channel total drift (end/start - 1): [-0.0552, None, -0.611, -0.5997, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 42: holes 0, rim-vs-core 0.40, rim-vs-outside 0.13, heterogeneity 0.26; core [0.451, 0.411, 0.153, 0.492, 0.3] rim [0.319, 0.172, 0.189, 0.34, 0.058]
  - track 9 at frame 42: holes 0, rim-vs-core 0.40, rim-vs-outside 0.14, heterogeneity 0.19; core [0.292, 0.557, 0.212, 0.326, 0.246] rim [0.276, 0.199, 0.218, 0.3, 0.068]
  - track 13 at frame 42: holes 0, rim-vs-core 0.34, rim-vs-outside 0.14, heterogeneity 0.20; core [0.325, 0.492, 0.2, 0.361, 0.212] rim [0.254, 0.206, 0.213, 0.277, 0.057]
  - track 47 at frame 59: holes 0, rim-vs-core 0.50, rim-vs-outside 0.14, heterogeneity 0.26; core [0.389, 0.527, 0.171, 0.43, 0.395] rim [0.304, 0.16, 0.194, 0.324, 0.082]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 247 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.949, rim/outside 4.43 (aggregate of 247 individuals; 39/247 membrane-like individually; rim level 0.47)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.35, rim/outside 5.33 (aggregate of 247 individuals; 4/247 membrane-like individually; rim level 0.226)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.53, rim/outside 0.849 (aggregate of 247 individuals; 0/247 membrane-like individually; rim level 0.189)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.928, rim/outside 4.51 (aggregate of 247 individuals; 25/247 membrane-like individually; rim level 0.489)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.287, rim/outside 12.1 (aggregate of 247 individuals; 3/247 membrane-like individually; rim level 0.142)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=4200, R_eq 5.5): none; #9 (t=4200, R_eq 4.41): ['prey a', 'product p']; #13 (t=4200, R_eq 4.55): none; #47 (t=5900, R_eq 4.82): none
- species `prey` (channels ['prey a'], own threshold): components final 46, mean 39.2, max 46; tracks 130, persistent 23; splits 27, persistent splits 11 (K=20), max generation 3, merges 8, merge/split 0.296; moving tracks 51
- species `predator` (channels ['predator b'], own threshold): components final 44, mean 28.3, max 46; tracks 94, persistent 19; splits 12, persistent splits 4 (K=20), max generation 1, merges 2, merge/split 0.167; moving tracks 50

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 247 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
