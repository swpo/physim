# Evidence pack: active-nematic-droplets-audit-source-split3 (seed 2)

- world: `../world_srcsplit3.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 494s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2125-c21-review-c11-ring-source/world_srcsplit3.py --out collective/contrib/20261025T2125-c21-review-c11-ring-source/split2 --seeds 2 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8223, 0.6152], min area 6 px

## Measurements
- components: final 30, mean 19.3, max 30; occupancy final 0.07
- tracks: 114; persistent (alive >= 50% of run): 4; longest 144 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 31, 28], H1 [0, 0, 0]
- motion: 40 long-lived tracks moved >= 1 body length; max speed 0.0787/time; max body lengths 5.7
- replication (lineage window K = 20 frames = time 100, default): splits 44, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 3, merges 18, merge/split ratio 0.409, nucleations 8
- channel total drift (end/start - 1): [-0.5106, -0.3431, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 124: holes 0, rim-vs-core 0.62, rim-vs-outside 0.36, heterogeneity 0.16; core [0.951, 0.919, 0.52, 0.286, 0.407] rim [0.744, 0.622, 0.779, 0.54, 0.755]
  - track 28 at frame 121: holes 0, rim-vs-core 0.51, rim-vs-outside 0.31, heterogeneity 0.14; core [0.901, 0.708, 0.648, 0.397, 0.48] rim [0.709, 0.472, 0.848, 0.63, 0.753]
  - track 46 at frame 145: holes 0, rim-vs-core 0.57, rim-vs-outside 0.36, heterogeneity 0.15; core [0.94, 0.874, 0.528, 0.319, 0.414] rim [0.728, 0.577, 0.736, 0.558, 0.715]
  - track 64 at frame 161: holes 0, rim-vs-core 0.59, rim-vs-outside 0.35, heterogeneity 0.16; core [0.929, 0.856, 0.558, 0.339, 0.426] rim [0.715, 0.562, 0.794, 0.594, 0.734]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 130 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 4.88 (aggregate of 130 individuals; 0/130 membrane-like individually; rim level 0.76)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.757, rim/outside 8.44 (aggregate of 130 individuals; 1/130 membrane-like individually; rim level 0.658)
  - radial s rod-made (phi>0): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 2.76 (aggregate of 130 individuals; 70/130 membrane-like individually; rim level 0.714)
  - radial s interface-made (-0.5<phi<=0): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.67, rim/outside 1.88 (aggregate of 130 individuals; 100/130 membrane-like individually; rim level 0.486)  MEMBRANE-LIKE
  - radial s far-bath-made (phi<=-0.5): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.72, rim/outside 1.41 (aggregate of 130 individuals; 76/130 membrane-like individually; rim level 0.616)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s interface-made (-0.5<phi<=0)
- membrane-like channels per top track at mid-life: #24 (t=620, R_eq 3.09): ['s rod-made (phi>0)', 's interface-made (-0.5<phi<=0)', 's far-bath-made (phi<=-0.5)']; #28 (t=605, R_eq 3.7): none; #46 (t=725, R_eq 3.09): ['s rod-made (phi>0)', 's interface-made (-0.5<phi<=0)', 's far-bath-made (phi<=-0.5)']; #64 (t=805, R_eq 3.14): ['s rod-made (phi>0)', 's interface-made (-0.5<phi<=0)', 's far-bath-made (phi<=-0.5)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
