# Evidence pack: active-nematic-marangoni-two-kinds (seed 7)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0655-c34-two-kinds-swap/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 186 frames x 100 steps x dt 0.05 = time 925; grid [128, 128]; wall 638s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0655-c34-two-kinds-swap/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/rev14/swap_s7 --seeds 7 --frames 185 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8403, 0.5762], min area 6 px

## Measurements
- components: final 30, mean 22.6, max 32; occupancy final 0.09
- tracks: 92; persistent (alive >= 50% of run): 17; longest 147 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.93 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 30], H1 [0, 0, 0]
- motion: 47 long-lived tracks moved >= 1 body length; max speed 0.295/time; max body lengths 6.3
- replication (lineage window K = 20 frames = time 100, default): splits 36, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 4, merges 12, merge/split ratio 0.333, nucleations 8
- channel total drift (end/start - 1): [-0.4954, -0.4392, -0.9843, 18.4992]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 112: holes 0, rim-vs-core 0.54, rim-vs-outside 0.40, heterogeneity 0.13; core [0.96, 0.93, 0.002, 0.295] rim [0.761, 0.604, 0.005, 0.673]
  - track 23 at frame 113: holes 0, rim-vs-core 0.53, rim-vs-outside 0.42, heterogeneity 0.14; core [0.936, 0.871, 0.028, 0.441] rim [0.755, 0.598, 0.061, 0.859]
  - track 27 at frame 115: holes 0, rim-vs-core 0.52, rim-vs-outside 0.33, heterogeneity 0.15; core [0.939, 0.672, 0.004, 0.456] rim [0.751, 0.452, 0.009, 0.889]
  - track 56 at frame 137: holes 0, rim-vs-core 0.57, rim-vs-outside 0.36, heterogeneity 0.14; core [0.956, 0.796, 0.006, 0.359] rim [0.764, 0.505, 0.015, 0.806]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 154 components >= 12 px at frames [31, 62, 93, 123, 154, 185]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.8, rim/outside 4.67 (aggregate of 154 individuals; 0/154 membrane-like individually; rim level 0.72)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.792, rim/outside 9.39 (aggregate of 154 individuals; 11/154 membrane-like individually; rim level 0.544)
  - radial surfactant A: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 2.15 (aggregate of 154 individuals; 30/154 membrane-like individually; rim level 0.0519)
  - radial surfactant B: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 3.17 (aggregate of 154 individuals; 65/154 membrane-like individually; rim level 0.573)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #20 (t=560, R_eq 3.48): ['surfactant B']; #23 (t=565, R_eq 4.79): none; #27 (t=575, R_eq 4.69, ring): ['order |Q|']; #56 (t=685, R_eq 3.91): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 154 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
