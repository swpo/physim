# Evidence pack: digestion-predators-turnover (seed 6)

- world: `../../../collective/contrib/20261027T0637-c52-turnover-cycles-three-seeds/world2g.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 161 frames x 500 steps x dt 0.2 = time 16000; grid [128, 128]; wall 904s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0637-c52-turnover-cycles-three-seeds/world2g.py --out c56work/cy/neu_s6 --seeds 6 --size 128 128 --frames 160 --no-movie`
- segmentation: matter > 0.16 of robust range [0.1567, 2.2773], min area 6 px

## Measurements
- components: final 42, mean 32.6, max 46; occupancy final 0.15
- tracks: 226; persistent (alive >= 50% of run): 1; longest 84 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.90 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 26, 16], H1 [0, 0, 0]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 0.00635/time; max body lengths 6.0
- replication (lineage window K = 20 frames = time 2000, default): splits 26, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 6, merge/split ratio 0.231, nucleations 168
- channel total drift (end/start - 1): [-0.0615, None, -0.6019, -0.6089, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 105 at frame 118: holes 0, rim-vs-core 0.69, rim-vs-outside 0.20, heterogeneity 0.26; core [0.26, 0.577, 0.258, 0.338, 0.495, 0.486, 0.389] rim [0.183, 0.232, 0.28, 0.235, 0.118, 0.179, 0.078]
  - track 82 at frame 99: holes 0, rim-vs-core 0.50, rim-vs-outside 0.17, heterogeneity 0.18; core [0.298, 0.601, 0.196, 0.344, 0.406, 0.184, 0.043] rim [0.243, 0.226, 0.208, 0.277, 0.11, 0.09, 0.014]
  - track 94 at frame 104: holes 0, rim-vs-core 0.47, rim-vs-outside 0.16, heterogeneity 0.07; core [0.103, 0.724, 0.26, 0.117, 0.324, 0.096, 0.006] rim [0.124, 0.304, 0.256, 0.137, 0.111, 0.081, 0.005]
  - track 149 at frame 117: holes 0, rim-vs-core 0.66, rim-vs-outside 0.18, heterogeneity 0.11; core [0.115, 0.793, 0.309, 0.15, 0.527, 0.191, 0.03] rim [0.14, 0.257, 0.306, 0.173, 0.147, 0.109, 0.015]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 200 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 1.64 (aggregate of 200 individuals; 38/200 membrane-like individually; rim level 0.261)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.488, rim/outside 5.94 (aggregate of 200 individuals; 0/200 membrane-like individually; rim level 0.26)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 0.952 (aggregate of 200 individuals; 0/200 membrane-like individually; rim level 0.215)
  - radial product p: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 1.65 (aggregate of 200 individuals; 35/200 membrane-like individually; rim level 0.28)
  - radial digestion q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.492, rim/outside 13.5 (aggregate of 200 individuals; 4/200 membrane-like individually; rim level 0.172)
  - radial predator e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.508, rim/outside 6.88 (aggregate of 200 individuals; 0/200 membrane-like individually; rim level 0.297)
  - radial digestion q2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.482, rim/outside 14.6 (aggregate of 200 individuals; 2/200 membrane-like individually; rim level 0.191)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #105 (t=11800, R_eq 5.23): ['prey a', 'product p']; #82 (t=9900, R_eq 4.79): ['prey a']; #94 (t=10400, R_eq 4.15): none; #149 (t=11700, R_eq 4.44): none
- species `prey` (channels ['prey a'], own threshold): components final 27, mean 18.2, max 36; tracks 253, persistent 0; splits 22, persistent splits 0 (K=20), max generation 0, merges 1, merge/split 0.045; moving tracks 18
- species `predator` (channels ['predator b'], own threshold): components final 19, mean 11.4, max 25; tracks 198, persistent 0; splits 9, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 15
- species `predator_e` (channels ['predator e'], own threshold): components final 17, mean 12.9, max 30; tracks 192, persistent 0; splits 2, persistent splits 0 (K=20), max generation 0, merges 1, merge/split 0.5; moving tracks 13

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
