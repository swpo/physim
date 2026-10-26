# Evidence pack: active-nematic-marangoni-two-kinds (seed 20)

- world: `../../../../20261026T0655-c34-two-kinds-swap/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 687s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0655-c34-two-kinds-swap/world.py --out collective/contrib/wip-c37/twok/neutral/s20 --seeds 20 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8417, 0.5721], min area 6 px

## Measurements
- components: final 28, mean 22.4, max 30; occupancy final 0.09
- tracks: 104; persistent (alive >= 50% of run): 11; longest 169 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 29, 27], H1 [0, 0, 0]
- motion: 54 long-lived tracks moved >= 1 body length; max speed 0.326/time; max body lengths 7.8
- replication (lineage window K = 20 frames = time 100, default): splits 39, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 4, merges 17, merge/split ratio 0.436, nucleations 9
- channel total drift (end/start - 1): [-0.494, -0.4175, 6.3557, 12.148]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 116: holes 0, rim-vs-core 0.57, rim-vs-outside 0.33, heterogeneity 0.16; core [0.945, 0.583, 0.012, 0.448] rim [0.734, 0.387, 0.031, 0.945]
  - track 16 at frame 116: holes 0, rim-vs-core 0.55, rim-vs-outside 0.41, heterogeneity 0.14; core [0.943, 0.923, 0.016, 0.368] rim [0.732, 0.604, 0.035, 0.765]
  - track 17 at frame 118: holes 0, rim-vs-core 0.55, rim-vs-outside 0.38, heterogeneity 0.13; core [0.942, 0.915, 0.007, 0.393] rim [0.751, 0.59, 0.014, 0.789]
  - track 80 at frame 180: holes 0, rim-vs-core 0.61, rim-vs-outside 0.34, heterogeneity 0.16; core [0.944, 0.7, 0.464, 0.037] rim [0.724, 0.415, 0.959, 0.089]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 147 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 4.42 (aggregate of 147 individuals; 1/147 membrane-like individually; rim level 0.695)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.821, rim/outside 8.32 (aggregate of 147 individuals; 9/147 membrane-like individually; rim level 0.525)
  - radial surfactant A: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 3.05 (aggregate of 147 individuals; 39/147 membrane-like individually; rim level 0.238)
  - radial surfactant B: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 3.09 (aggregate of 147 individuals; 50/147 membrane-like individually; rim level 0.386)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #15 (t=580, R_eq 4.89): none; #16 (t=580, R_eq 4.07): none; #17 (t=590, R_eq 3.7): ['surfactant B']; #80 (t=900, R_eq 4.18): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 147 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
