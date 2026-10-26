# Evidence pack: active-nematic-marangoni (seed 0)

- world: `../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 121 frames x 100 steps x dt 0.05 = time 600; grid [192, 192]; wall 608s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261026T0505-c34-nematic-marangoni/res15 --seeds 0 --size 192 192 --frames 120 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8402, 0.6526], min area 6 px

## Measurements
- components: final 29, mean 18.7, max 29; occupancy final 0.09
- tracks: 58; persistent (alive >= 50% of run): 13; longest 88 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.64 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 29, 28], H1 [0, 0, 0]
- motion: 35 long-lived tracks moved >= 1 body length; max speed 0.32/time; max body lengths 6.5
- replication (lineage window K = 20 frames = time 100, default): splits 24, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.083, nucleations 8
- channel total drift (end/start - 1): [-0.5023, -0.2372, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 77: holes 0, rim-vs-core 0.87, rim-vs-outside 0.41, heterogeneity 0.24; core [0.963, 0.716, 0.311, 0.666] rim [0.747, 0.456, 0.795, 0.029]
  - track 16 at frame 78: holes 0, rim-vs-core 0.79, rim-vs-outside 0.38, heterogeneity 0.23; core [0.955, 0.604, 0.333, 0.614] rim [0.757, 0.389, 0.781, 0.028]
  - track 18 at frame 79: holes 0, rim-vs-core 0.72, rim-vs-outside 0.37, heterogeneity 0.23; core [0.917, 0.61, 0.38, 0.573] rim [0.729, 0.39, 0.755, 0.028]
  - track 38 at frame 92: holes 0, rim-vs-core 0.82, rim-vs-outside 0.44, heterogeneity 0.23; core [0.943, 0.888, 0.309, 0.623] rim [0.737, 0.569, 0.719, 0.025]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 128 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.792, rim/outside 5.25 (aggregate of 128 individuals; 0/128 membrane-like individually; rim level 0.719)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.736, rim/outside 10.3 (aggregate of 128 individuals; 5/128 membrane-like individually; rim level 0.565)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.42, rim/outside 3.59 (aggregate of 128 individuals; 74/128 membrane-like individually; rim level 0.536)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.419, rim/outside 5.59 (aggregate of 128 individuals; 18/128 membrane-like individually; rim level 0.174)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #15 (t=385, R_eq 6.48): none; #16 (t=390, R_eq 6.68): ['order |Q|', 'cargo c']; #18 (t=395, R_eq 7.09): ['order |Q|', 'cargo c']; #38 (t=460, R_eq 6.13): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 128 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
