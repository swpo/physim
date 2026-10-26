# Evidence pack: active-nematic-marangoni-two-kinds (seed 7)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0655-c34-two-kinds-swap/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 186 frames x 100 steps x dt 0.05 = time 925; grid [128, 128]; wall 632s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0655-c34-two-kinds-swap/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/rev14/neut_s7 --seeds 7 --frames 185 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8401, 0.5772], min area 6 px

## Measurements
- components: final 29, mean 22.6, max 32; occupancy final 0.09
- tracks: 89; persistent (alive >= 50% of run): 14; longest 154 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.72 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 29, 29], H1 [0, 0, 0]
- motion: 47 long-lived tracks moved >= 1 body length; max speed 0.28/time; max body lengths 6.2
- replication (lineage window K = 20 frames = time 100, default): splits 34, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 4, merges 12, merge/split ratio 0.353, nucleations 8
- channel total drift (end/start - 1): [-0.4954, -0.3866, -0.9721, 18.8664]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 109: holes 0, rim-vs-core 0.63, rim-vs-outside 0.38, heterogeneity 0.15; core [0.938, 0.765, 0.003, 0.44] rim [0.705, 0.437, 0.006, 0.92]
  - track 22 at frame 113: holes 0, rim-vs-core 0.61, rim-vs-outside 0.40, heterogeneity 0.15; core [0.933, 0.876, 0.007, 0.434] rim [0.737, 0.571, 0.016, 0.92]
  - track 28 at frame 115: holes 0, rim-vs-core 0.64, rim-vs-outside 0.33, heterogeneity 0.16; core [0.952, 0.745, 0.004, 0.4] rim [0.737, 0.438, 0.01, 0.918]
  - track 53 at frame 137: holes 0, rim-vs-core 0.60, rim-vs-outside 0.36, heterogeneity 0.15; core [0.934, 0.855, 0.014, 0.408] rim [0.728, 0.527, 0.034, 0.86]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 149 components >= 12 px at frames [31, 62, 93, 123, 154, 185]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.785, rim/outside 4.56 (aggregate of 149 individuals; 0/149 membrane-like individually; rim level 0.699)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.797, rim/outside 8.73 (aggregate of 149 individuals; 13/149 membrane-like individually; rim level 0.534)
  - radial surfactant A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.12, rim/outside 2.13 (aggregate of 149 individuals; 31/149 membrane-like individually; rim level 0.0519)
  - radial surfactant B: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 3.25 (aggregate of 149 individuals; 64/149 membrane-like individually; rim level 0.58)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #17 (t=545, R_eq 4.11): none; #22 (t=565, R_eq 4.3): none; #28 (t=575, R_eq 4.51): none; #53 (t=685, R_eq 3.57): ['surfactant A', 'surfactant B']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 149 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
