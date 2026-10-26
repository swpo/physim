# Evidence pack: active-nematic-rodsource (seed 2)

- world: `../../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 347s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0200-c34-rodsource/world.py --out collective/contrib/20261026T0200-c34-rodsource/pack --seeds 0 1 2 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8223, 0.6152], min area 6 px

## Measurements
- components: final 30, mean 19.3, max 30; occupancy final 0.07
- tracks: 114; persistent (alive >= 50% of run): 4; longest 144 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 31, 28], H1 [0, 0, 0]
- motion: 40 long-lived tracks moved >= 1 body length; max speed 0.0787/time; max body lengths 5.7
- replication (lineage window K = 20 frames = time 100, default): splits 44, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 3, merges 18, merge/split ratio 0.409, nucleations 8
- channel total drift (end/start - 1): [-0.5106, -0.3431, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 124: holes 0, rim-vs-core 0.54, rim-vs-outside 0.34, heterogeneity 0.17; core [0.951, 0.919, 0.309] rim [0.744, 0.622, 0.709]
  - track 28 at frame 121: holes 0, rim-vs-core 0.45, rim-vs-outside 0.30, heterogeneity 0.16; core [0.901, 0.708, 0.444] rim [0.709, 0.472, 0.781]
  - track 46 at frame 145: holes 0, rim-vs-core 0.49, rim-vs-outside 0.35, heterogeneity 0.16; core [0.94, 0.874, 0.332] rim [0.728, 0.577, 0.664]
  - track 64 at frame 161: holes 0, rim-vs-core 0.52, rim-vs-outside 0.34, heterogeneity 0.17; core [0.929, 0.856, 0.354] rim [0.715, 0.562, 0.72]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 130 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 4.88 (aggregate of 130 individuals; 0/130 membrane-like individually; rim level 0.76)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.757, rim/outside 8.44 (aggregate of 130 individuals; 1/130 membrane-like individually; rim level 0.658)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.85, rim/outside 2.98 (aggregate of 130 individuals; 99/130 membrane-like individually; rim level 0.594)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #24 (t=620, R_eq 3.09): ['surfactant s']; #28 (t=605, R_eq 3.7): none; #46 (t=725, R_eq 3.09): ['surfactant s']; #64 (t=805, R_eq 3.14): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
