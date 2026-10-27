# Evidence pack: digestion-driven-predators (seed 0)

- world: `../../wswim.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 510s; status ok
- command: `python -m labkit.run c56work/wswim.py --out c56work/sw/w5 --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.26 of robust range [0.156, 1.4795], min area 6 px

## Measurements
- components: final 54, mean 45.6, max 57; occupancy final 0.26
- tracks: 175; persistent (alive >= 50% of run): 26; longest 116 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [53, 53, 46], H1 [0, 0, 0]
- motion: 72 long-lived tracks moved >= 1 body length; max speed 0.00654/time; max body lengths 5.5
- replication (lineage window K = 20 frames = time 2000, default): splits 22, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 1, merges 22, merge/split ratio 1, nucleations 108
- channel total drift (end/start - 1): [-0.0551, None, -0.6151, -0.605, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 63: holes 0, rim-vs-core 0.46, rim-vs-outside 0.17, heterogeneity 0.18; core [0.446, 0.547, 0.161, 0.51, 0.314, 0.47] rim [0.271, 0.264, 0.191, 0.308, 0.073, 0.477]
  - track 33 at frame 57: holes 0, rim-vs-core 0.28, rim-vs-outside 0.45, heterogeneity 0.17; core [0.567, 0.455, 0.09, 0.589, 0.456, 0.446] rim [0.406, 0.373, 0.112, 0.418, 0.322, 0.453]
  - track 57 at frame 78: holes 0, rim-vs-core 0.46, rim-vs-outside 0.16, heterogeneity 0.18; core [0.392, 0.595, 0.147, 0.425, 0.322, 0.423] rim [0.257, 0.273, 0.169, 0.272, 0.075, 0.429]
  - track 89 at frame 85: holes 0, rim-vs-core 0.35, rim-vs-outside 0.12, heterogeneity 0.10; core [0.256, 0.591, 0.172, 0.268, 0.188, 0.436] rim [0.255, 0.266, 0.175, 0.263, 0.061, 0.436]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 293 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.865, rim/outside 4.03 (aggregate of 293 individuals; 4/293 membrane-like individually; rim level 0.465)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.517, rim/outside 4.38 (aggregate of 293 individuals; 1/293 membrane-like individually; rim level 0.35)
  - radial fuel F: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.53, rim/outside 0.881 (aggregate of 293 individuals; 0/293 membrane-like individually; rim level 0.181)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.85, rim/outside 4.17 (aggregate of 293 individuals; 3/293 membrane-like individually; rim level 0.484)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.353, rim/outside 11.8 (aggregate of 293 individuals; 2/293 membrane-like individually; rim level 0.17)
  - radial soluble predator u: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 0.993 (aggregate of 293 individuals; 0/293 membrane-like individually; rim level 0.403)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #21 (t=6300, R_eq 4.98): none; #33 (t=5700, R_eq 4.92): none; #57 (t=7800, R_eq 5.23): none; #89 (t=8500, R_eq 4.48): none
- species `prey` (channels ['prey a'], own threshold): components final 50, mean 41.5, max 54; tracks 174, persistent 22; splits 9, persistent splits 1 (K=20), max generation 1, merges 5, merge/split 0.556; moving tracks 72
- species `predator` (channels ['predator b'], own threshold): components final 51, mean 36.8, max 52; tracks 145, persistent 18; splits 4, persistent splits 1 (K=20), max generation 1, merges 1, merge/split 0.25; moving tracks 74

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
