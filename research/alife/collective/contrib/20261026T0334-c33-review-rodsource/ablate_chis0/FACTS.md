# Evidence pack: active-nematic-rodsource (seed 5)

- world: `../../20261026T0200-c34-rodsource/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5
- run: 121 frames x 100 steps x dt 0.05 = time 600; grid [128, 128]; wall 270s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0200-c34-rodsource/world.py --out collective/contrib/wip-c33-rod/ablate_chis0 --seeds 5 --frames 120 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8251, 0.6327], min area 6 px

## Measurements
- components: final 26, mean 17.3, max 26; occupancy final 0.06
- tracks: 64; persistent (alive >= 50% of run): 8; longest 88 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.25 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 26, 26], H1 [0, 0, 0]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 0.0755/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 100, default): splits 25, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 2, merges 4, merge/split ratio 0.16, nucleations 10
- channel total drift (end/start - 1): [-0.5097, -0.4045, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 77: holes 0, rim-vs-core 0.27, rim-vs-outside 0.34, heterogeneity 0.12; core [0.888, 0.649, 0.982] rim [0.717, 0.452, 0.92]
  - track 18 at frame 78: holes 0, rim-vs-core 0.41, rim-vs-outside 0.38, heterogeneity 0.13; core [0.938, 0.888, 0.94] rim [0.713, 0.569, 0.807]
  - track 28 at frame 85: holes 0, rim-vs-core 0.27, rim-vs-outside 0.36, heterogeneity 0.11; core [0.914, 0.702, 0.98] rim [0.745, 0.509, 0.894]
  - track 24 at frame 78: holes 0, rim-vs-core 0.41, rim-vs-outside 0.38, heterogeneity 0.13; core [0.946, 0.903, 0.908] rim [0.733, 0.584, 0.774]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 115 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 4.76 (aggregate of 115 individuals; 0/115 membrane-like individually; rim level 0.753)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.782, rim/outside 8.17 (aggregate of 115 individuals; 0/115 membrane-like individually; rim level 0.625)
  - radial surfactant s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.861, rim/outside 2.26 (aggregate of 115 individuals; 0/115 membrane-like individually; rim level 0.782)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=385, R_eq 4.82): none; #18 (t=390, R_eq 3.43): none; #28 (t=425, R_eq 4.37): none; #24 (t=390, R_eq 3.57): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 115 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
