# Evidence pack: digestion-predators-turnover (seed 7)

- world: `../../../collective/contrib/20261027T0637-c52-turnover-cycles-three-seeds/world2g.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 161 frames x 500 steps x dt 0.2 = time 16000; grid [128, 128]; wall 901s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0637-c52-turnover-cycles-three-seeds/world2g.py --out c56work/cy/neu_s7 --seeds 7 --size 128 128 --frames 160 --no-movie`
- segmentation: matter > 0.16 of robust range [0.1534, 2.2871], min area 6 px

## Measurements
- components: final 36, mean 32.8, max 42; occupancy final 0.12
- tracks: 215; persistent (alive >= 50% of run): 1; longest 84 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.62 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 24, 13], H1 [0, 0, 0]
- motion: 33 long-lived tracks moved >= 1 body length; max speed 0.00642/time; max body lengths 6.0
- replication (lineage window K = 20 frames = time 2000, default): splits 18, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 3, merge/split ratio 0.167, nucleations 176
- channel total drift (end/start - 1): [-0.0193, None, -0.6182, -0.5936, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 106 at frame 118: holes 0, rim-vs-core 0.46, rim-vs-outside 0.11, heterogeneity 0.18; core [0.18, 0.485, 0.28, 0.224, 0.196, 0.394, 0.276] rim [0.185, 0.228, 0.281, 0.225, 0.068, 0.109, 0.059]
  - track 115 at frame 121: holes 0, rim-vs-core 0.54, rim-vs-outside 0.13, heterogeneity 0.22; core [0.183, 0.565, 0.289, 0.238, 0.294, 0.386, 0.335] rim [0.184, 0.244, 0.292, 0.233, 0.09, 0.097, 0.084]
  - track 87 at frame 98: holes 0, rim-vs-core 0.61, rim-vs-outside 0.18, heterogeneity 0.16; core [0.19, 0.75, 0.25, 0.232, 0.501, 0.11, 0.014] rim [0.228, 0.267, 0.248, 0.268, 0.137, 0.069, 0.007]
  - track 118 at frame 104: holes 0, rim-vs-core 0.65, rim-vs-outside 0.14, heterogeneity 0.25; core [0.224, 0.492, 0.291, 0.301, 0.322, 0.548, 0.43] rim [0.188, 0.178, 0.302, 0.249, 0.078, 0.147, 0.11]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 196 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial prey a: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.02, rim/outside 1.79 (aggregate of 196 individuals; 35/196 membrane-like individually; rim level 0.28)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.5, rim/outside 5.92 (aggregate of 196 individuals; 0/196 membrane-like individually; rim level 0.257)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 0.946 (aggregate of 196 individuals; 0/196 membrane-like individually; rim level 0.217)
  - radial product p: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.993, rim/outside 1.78 (aggregate of 196 individuals; 30/196 membrane-like individually; rim level 0.297)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.514, rim/outside 13.6 (aggregate of 196 individuals; 2/196 membrane-like individually; rim level 0.17)
  - radial predator e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.508, rim/outside 7.28 (aggregate of 196 individuals; 0/196 membrane-like individually; rim level 0.298)
  - radial digestion q2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.517, rim/outside 15.6 (aggregate of 196 individuals; 1/196 membrane-like individually; rim level 0.193)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #106 (t=11800, R_eq 5.67): ['prey a', 'product p']; #115 (t=12100, R_eq 5.29): ['prey a', 'product p']; #87 (t=9800, R_eq 4.85): ['prey a', 'product p']; #118 (t=10400, R_eq 5.29): ['prey a', 'product p']
- species `prey` (channels ['prey a'], own threshold): components final 24, mean 18.3, max 41; tracks 250, persistent 1; splits 24, persistent splits 0 (K=20), max generation 0, merges 1, merge/split 0.042; moving tracks 25
- species `predator` (channels ['predator b'], own threshold): components final 13, mean 10.9, max 24; tracks 174, persistent 0; splits 2, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 18
- species `predator_e` (channels ['predator e'], own threshold): components final 17, mean 13.0, max 31; tracks 199, persistent 0; splits 7, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 17

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
