# Evidence pack: digestion-predators-competition (seed 1)

- world: `../../world2p.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 101 frames x 500 steps x dt 0.2 = time 10000; grid [128, 128]; wall 490s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0457-c52-predator-competition-taxis/world2p.py --out collective/contrib/20261027T0457-c52-predator-competition-taxis/comp/halfE_s1 --seeds 1 --size 128 128 --frames 100 --no-movie`
- segmentation: matter > 0.19 of robust range [0.1513, 1.9707], min area 6 px

## Measurements
- components: final 46, mean 40.0, max 47; occupancy final 0.21
- tracks: 130; persistent (alive >= 50% of run): 21; longest 99 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.44 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [50, 44, 40], H1 [0, 0, 0]
- motion: 55 long-lived tracks moved >= 1 body length; max speed 0.00797/time; max body lengths 7.0
- replication (lineage window K = 20 frames = time 2000, default): splits 33, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 3, merges 10, merge/split ratio 0.303, nucleations 54
- channel total drift (end/start - 1): [-0.0451, None, -0.6103, -0.5956, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 51: holes 0, rim-vs-core 0.30, rim-vs-outside 0.44, heterogeneity 0.20; core [0.597, 0.258, 0.14, 0.666, 0.299, 0.081, 0.023] rim [0.404, 0.322, 0.173, 0.451, 0.246, 0.066, 0.015]
  - track 3 at frame 52: holes 0, rim-vs-core 0.44, rim-vs-outside 0.33, heterogeneity 0.18; core [0.525, 0.404, 0.178, 0.599, 0.414, 0.078, 0.012] rim [0.28, 0.339, 0.216, 0.32, 0.198, 0.058, 0.004]
  - track 5 at frame 52: holes 0, rim-vs-core 0.57, rim-vs-outside 0.17, heterogeneity 0.20; core [0.413, 0.127, 0.182, 0.467, 0.019, 0.528, 0.473] rim [0.327, 0.083, 0.199, 0.364, 0.007, 0.125, 0.102]
  - track 91 at frame 83: holes 0, rim-vs-core 0.49, rim-vs-outside 0.19, heterogeneity 0.18; core [0.494, 0.438, 0.145, 0.54, 0.365, 0.082, 0.018] rim [0.332, 0.133, 0.171, 0.355, 0.073, 0.054, 0.007]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 251 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.942, rim/outside 4.64 (aggregate of 251 individuals; 25/251 membrane-like individually; rim level 0.48)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.318, rim/outside 6.49 (aggregate of 251 individuals; 3/251 membrane-like individually; rim level 0.152)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.48, rim/outside 0.851 (aggregate of 251 individuals; 0/251 membrane-like individually; rim level 0.196)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 4.71 (aggregate of 251 individuals; 22/251 membrane-like individually; rim level 0.499)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.271, rim/outside 9.98 (aggregate of 251 individuals; 10/251 membrane-like individually; rim level 0.105)
  - radial predator e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.449, rim/outside 3.11 (aggregate of 251 individuals; 5/251 membrane-like individually; rim level 0.122)
  - radial digestion q2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.412, rim/outside 7.46 (aggregate of 251 individuals; 13/251 membrane-like individually; rim level 0.082)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=5100, R_eq 4.79): none; #3 (t=5200, R_eq 4.3): none; #5 (t=5200, R_eq 4.55): none; #91 (t=8300, R_eq 4.55): none
- species `prey` (channels ['prey a'], own threshold): components final 48, mean 40.4, max 48; tracks 155, persistent 21; splits 40, persistent splits 17 (K=20), max generation 3, merges 7, merge/split 0.175; moving tracks 60
- species `predator` (channels ['predator b'], own threshold): components final 28, mean 22.9, max 35; tracks 102, persistent 9; splits 2, persistent splits 0 (K=20), max generation 0, merges 1, merge/split 0.5; moving tracks 48
- species `predator_e` (channels ['predator e'], own threshold): components final 16, mean 9.5, max 19; tracks 63, persistent 2; splits 3, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 16

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
