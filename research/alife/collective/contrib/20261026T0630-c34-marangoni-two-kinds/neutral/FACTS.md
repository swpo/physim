# Evidence pack: active-nematic-marangoni-two-kinds (seed 0)

- world: `../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 442s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0630-c34-marangoni-two-kinds/world.py --out collective/contrib/20261026T0630-c34-marangoni-two-kinds/neutral --seeds 0 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8388, 0.5673], min area 6 px

## Measurements
- components: final 29, mean 22.1, max 32; occupancy final 0.09
- tracks: 98; persistent (alive >= 50% of run): 13; longest 173 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.20 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 29, 29], H1 [0, 0, 0]
- motion: 60 long-lived tracks moved >= 1 body length; max speed 0.367/time; max body lengths 7.5
- replication (lineage window K = 20 frames = time 100, default): splits 38, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 4, merges 12, merge/split ratio 0.316, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.4405, 6.578, 11.2979]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 114: holes 0, rim-vs-core 0.56, rim-vs-outside 0.33, heterogeneity 0.14; core [0.931, 0.638, 0.007, 0.463] rim [0.721, 0.412, 0.016, 0.925]
  - track 12 at frame 114: holes 0, rim-vs-core 0.56, rim-vs-outside 0.38, heterogeneity 0.15; core [0.95, 0.873, 0.025, 0.367] rim [0.753, 0.56, 0.054, 0.783]
  - track 31 at frame 133: holes 0, rim-vs-core 0.55, rim-vs-outside 0.37, heterogeneity 0.15; core [0.937, 0.816, 0.009, 0.447] rim [0.742, 0.533, 0.02, 0.875]
  - track 62 at frame 156: holes 0, rim-vs-core 0.57, rim-vs-outside 0.37, heterogeneity 0.15; core [0.935, 0.79, 0.015, 0.46] rim [0.737, 0.507, 0.033, 0.911]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 149 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 4.68 (aggregate of 149 individuals; 0/149 membrane-like individually; rim level 0.713)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.766, rim/outside 9.3 (aggregate of 149 individuals; 9/149 membrane-like individually; rim level 0.544)
  - radial surfactant A: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 3.13 (aggregate of 149 individuals; 57/149 membrane-like individually; rim level 0.257)
  - radial surfactant B: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 3.24 (aggregate of 149 individuals; 66/149 membrane-like individually; rim level 0.404)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=570, R_eq 4.33): none; #12 (t=570, R_eq 3.48): ['surfactant A', 'surfactant B']; #31 (t=665, R_eq 3.78): ['surfactant B']; #62 (t=780, R_eq 3.95): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 149 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
