# Evidence pack: digestion-driven-predators (seed 0)

- world: `../../../collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 440s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out c56work/ma/p0.5 --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.25 of robust range [0.1537, 1.5405], min area 6 px

## Measurements
- components: final 0, mean 13.7, max 29; occupancy final 0.00
- tracks: 60; persistent (alive >= 50% of run): 4; longest 107 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.62 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 2, 1], H1 [0, 0, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.00668/time; max body lengths 7.5
- replication (lineage window K = 20 frames = time 2000, default): splits 11, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 2, merge/split ratio 0.182, nucleations 36
- channel total drift (end/start - 1): [-0.0053, None, -0.543, -0.5274, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 61: holes 0, rim-vs-core 0.61, rim-vs-outside 0.26, heterogeneity 0.28; core [0.428, 0.703, 0.138, 0.476, 0.67] rim [0.321, 0.296, 0.159, 0.351, 0.24]
  - track 0 at frame 48: holes 0, rim-vs-core 0.63, rim-vs-outside 0.24, heterogeneity 0.27; core [0.361, 0.749, 0.191, 0.429, 0.654] rim [0.281, 0.306, 0.21, 0.329, 0.231]
  - track 27 at frame 77: holes 0, rim-vs-core 0.62, rim-vs-outside 0.20, heterogeneity 0.25; core [0.334, 0.737, 0.202, 0.396, 0.588] rim [0.281, 0.286, 0.218, 0.327, 0.171]
  - track 7 at frame 43: holes 0, rim-vs-core 0.64, rim-vs-outside 0.24, heterogeneity 0.29; core [0.415, 0.715, 0.153, 0.471, 0.685] rim [0.337, 0.272, 0.173, 0.378, 0.237]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 82 components >= 12 px at frames [20, 40, 61, 80, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.925, rim/outside 3.56 (aggregate of 82 individuals; 13/82 membrane-like individually; rim level 0.416)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.606, rim/outside 4.28 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.364)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.32, rim/outside 0.831 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.174)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 3.62 (aggregate of 82 individuals; 13/82 membrane-like individually; rim level 0.429)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.546, rim/outside 12.5 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.233)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=6100, R_eq 4.03): none; #0 (t=4800, R_eq 4.15): none; #27 (t=7700, R_eq 4.03): ['prey a']; #7 (t=4300, R_eq 4.18): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 9.7, max 22; tracks 44, persistent 5; splits 6, persistent splits 2 (K=20), max generation 1, merges 0, merge/split 0; moving tracks 18
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 9.0, max 25; tracks 49, persistent 4; splits 7, persistent splits 2 (K=20), max generation 1, merges 1, merge/split 0.143; moving tracks 18

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
