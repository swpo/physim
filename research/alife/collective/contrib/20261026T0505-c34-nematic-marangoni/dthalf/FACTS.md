# Evidence pack: active-nematic-marangoni (seed 0)

- world: `../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 121 frames x 200 steps x dt 0.05 = time 1200; grid [128, 128]; wall 490s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261026T0505-c34-nematic-marangoni/dthalf --seeds 0 --frames 120 --spf 200 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.833, 0.5731], min area 6 px

## Measurements
- components: final 30, mean 17.5, max 30; occupancy final 0.09
- tracks: 89; persistent (alive >= 50% of run): 6; longest 96 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 30, 30], H1 [0, 0, 0]
- motion: 40 long-lived tracks moved >= 1 body length; max speed 0.224/time; max body lengths 5.9
- replication (lineage window K = 20 frames = time 200, default): splits 34, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 3, merges 12, merge/split ratio 0.353, nucleations 9
- channel total drift (end/start - 1): [-0.504, -0.4099, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 73: holes 0, rim-vs-core 0.54, rim-vs-outside 0.28, heterogeneity 0.20; core [0.913, 0.54, 0.5, 0.39] rim [0.743, 0.39, 0.821, 0.021]
  - track 12 at frame 67: holes 0, rim-vs-core 0.73, rim-vs-outside 0.38, heterogeneity 0.21; core [0.931, 0.827, 0.421, 0.563] rim [0.75, 0.566, 0.797, 0.017]
  - track 25 at frame 87: holes 0, rim-vs-core 0.65, rim-vs-outside 0.33, heterogeneity 0.22; core [0.937, 0.713, 0.435, 0.413] rim [0.732, 0.46, 0.839, 0.016]
  - track 44 at frame 100: holes 0, rim-vs-core 0.82, rim-vs-outside 0.39, heterogeneity 0.24; core [0.973, 0.916, 0.326, 0.558] rim [0.767, 0.542, 0.777, 0.026]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 119 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.82, rim/outside 4.53 (aggregate of 119 individuals; 0/119 membrane-like individually; rim level 0.711)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 8.1 (aggregate of 119 individuals; 9/119 membrane-like individually; rim level 0.536)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 3.23 (aggregate of 119 individuals; 56/119 membrane-like individually; rim level 0.568)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.487, rim/outside 2.11 (aggregate of 119 individuals; 19/119 membrane-like individually; rim level 0.165)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=730, R_eq 4.79, ring): ['order |Q|', 'cargo c']; #12 (t=670, R_eq 4.22): ['cargo c']; #25 (t=870, R_eq 4.41): none; #44 (t=1000, R_eq 3.14): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 119 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
