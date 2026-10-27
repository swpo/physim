# Evidence pack: digestion-predators-competition (seed 1)

- world: `../../world2p.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 101 frames x 500 steps x dt 0.2 = time 10000; grid [128, 128]; wall 491s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0457-c52-predator-competition-taxis/world2p.py --out collective/contrib/20261027T0457-c52-predator-competition-taxis/comp/same_s1 --seeds 1 --size 128 128 --frames 100 --no-movie`
- segmentation: matter > 0.18 of robust range [0.1513, 2.0788], min area 6 px

## Measurements
- components: final 45, mean 41.1, max 50; occupancy final 0.18
- tracks: 138; persistent (alive >= 50% of run): 22; longest 98 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [45, 41, 32], H1 [0, 0, 0]
- motion: 62 long-lived tracks moved >= 1 body length; max speed 0.00688/time; max body lengths 5.9
- replication (lineage window K = 20 frames = time 2000, default): splits 29, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 2, merges 11, merge/split ratio 0.379, nucleations 69
- channel total drift (end/start - 1): [-0.0431, None, -0.6084, -0.5968, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 52: holes 0, rim-vs-core 0.61, rim-vs-outside 0.15, heterogeneity 0.19; core [0.393, 0.192, 0.204, 0.468, 0.049, 0.533, 0.478] rim [0.298, 0.119, 0.224, 0.347, 0.017, 0.101, 0.09]
  - track 11 at frame 52: holes 0, rim-vs-core 0.52, rim-vs-outside 0.13, heterogeneity 0.16; core [0.407, 0.482, 0.164, 0.445, 0.397, 0.126, 0.023] rim [0.321, 0.098, 0.18, 0.344, 0.076, 0.087, 0.01]
  - track 12 at frame 52: holes 0, rim-vs-core 0.54, rim-vs-outside 0.16, heterogeneity 0.16; core [0.343, 0.596, 0.212, 0.395, 0.414, 0.082, 0.017] rim [0.275, 0.179, 0.223, 0.31, 0.096, 0.052, 0.008]
  - track 97 at frame 85: holes 0, rim-vs-core 0.58, rim-vs-outside 0.13, heterogeneity 0.22; core [0.322, 0.417, 0.188, 0.356, 0.151, 0.399, 0.431] rim [0.288, 0.145, 0.2, 0.307, 0.041, 0.046, 0.087]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 261 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.921, rim/outside 4.01 (aggregate of 261 individuals; 13/261 membrane-like individually; rim level 0.474)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.374, rim/outside 5.5 (aggregate of 261 individuals; 3/261 membrane-like individually; rim level 0.151)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.45, rim/outside 0.855 (aggregate of 261 individuals; 0/261 membrane-like individually; rim level 0.189)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 4.12 (aggregate of 261 individuals; 13/261 membrane-like individually; rim level 0.497)
  - radial digestion q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.338, rim/outside 9.45 (aggregate of 261 individuals; 5/261 membrane-like individually; rim level 0.104)
  - radial predator e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.371, rim/outside 5.4 (aggregate of 261 individuals; 5/261 membrane-like individually; rim level 0.151)
  - radial digestion q2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.333, rim/outside 9.83 (aggregate of 261 individuals; 6/261 membrane-like individually; rim level 0.106)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=5200, R_eq 4.33): none; #11 (t=5200, R_eq 4.37): none; #12 (t=5200, R_eq 4.3): none; #97 (t=8500, R_eq 4.62): none
- species `prey` (channels ['prey a'], own threshold): components final 39, mean 39.5, max 46; tracks 157, persistent 18; splits 31, persistent splits 18 (K=20), max generation 2, merges 7, merge/split 0.226; moving tracks 69
- species `predator` (channels ['predator b'], own threshold): components final 19, mean 17.1, max 27; tracks 128, persistent 0; splits 4, persistent splits 1 (K=20), max generation 1, merges 0, merge/split 0; moving tracks 31
- species `predator_e` (channels ['predator e'], own threshold): components final 28, mean 17.7, max 28; tracks 146, persistent 0; splits 2, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 26

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
