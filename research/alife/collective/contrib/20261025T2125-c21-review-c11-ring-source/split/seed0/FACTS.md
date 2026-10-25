# Evidence pack: active-nematic-droplets-audit-source-split3 (seed 0)

- world: `../../world_srcsplit3.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 492s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2125-c21-review-c11-ring-source/world_srcsplit3.py --out collective/contrib/20261025T2125-c21-review-c11-ring-source/split --seeds 0 1 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8191, 0.6117], min area 6 px

## Measurements
- components: final 30, mean 18.2, max 30; occupancy final 0.06
- tracks: 80; persistent (alive >= 50% of run): 13; longest 167 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 29], H1 [0, 0, 0]
- motion: 36 long-lived tracks moved >= 1 body length; max speed 0.0797/time; max body lengths 3.8
- replication (lineage window K = 20 frames = time 100, default): splits 33, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 3, merges 5, merge/split ratio 0.152, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.4345, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 118: holes 0, rim-vs-core 0.62, rim-vs-outside 0.38, heterogeneity 0.16; core [0.947, 0.922, 0.521, 0.3, 0.463] rim [0.715, 0.604, 0.744, 0.537, 0.817]
  - track 23 at frame 128: holes 0, rim-vs-core 0.50, rim-vs-outside 0.34, heterogeneity 0.13; core [0.914, 0.789, 0.613, 0.356, 0.433] rim [0.732, 0.539, 0.798, 0.577, 0.694]
  - track 24 at frame 128: holes 0, rim-vs-core 0.65, rim-vs-outside 0.33, heterogeneity 0.17; core [0.948, 0.798, 0.623, 0.477, 0.453] rim [0.74, 0.527, 0.907, 0.819, 0.78]
  - track 58 at frame 182: holes 0, rim-vs-core 0.64, rim-vs-outside 0.34, heterogeneity 0.16; core [0.951, 0.888, 0.511, 0.313, 0.473] rim [0.732, 0.577, 0.752, 0.574, 0.849]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 126 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.825, rim/outside 4.92 (aggregate of 126 individuals; 0/126 membrane-like individually; rim level 0.774)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.771, rim/outside 8.39 (aggregate of 126 individuals; 0/126 membrane-like individually; rim level 0.662)
  - radial s rod-made (phi>0): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.28, rim/outside 2.71 (aggregate of 126 individuals; 67/126 membrane-like individually; rim level 0.714)
  - radial s interface-made (-0.5<phi<=0): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.64, rim/outside 1.91 (aggregate of 126 individuals; 99/126 membrane-like individually; rim level 0.495)  MEMBRANE-LIKE
  - radial s far-bath-made (phi<=-0.5): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.71, rim/outside 1.43 (aggregate of 126 individuals; 74/126 membrane-like individually; rim level 0.634)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s interface-made (-0.5<phi<=0)
- membrane-like channels per top track at mid-life: #15 (t=590, R_eq 3.24): ['s rod-made (phi>0)', 's interface-made (-0.5<phi<=0)', 's far-bath-made (phi<=-0.5)']; #23 (t=640, R_eq 3.48): none; #24 (t=640, R_eq 2.71): ['s rod-made (phi>0)', 's interface-made (-0.5<phi<=0)', 's far-bath-made (phi<=-0.5)']; #58 (t=910, R_eq 2.88): ['s rod-made (phi>0)', 's interface-made (-0.5<phi<=0)', 's far-bath-made (phi<=-0.5)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
