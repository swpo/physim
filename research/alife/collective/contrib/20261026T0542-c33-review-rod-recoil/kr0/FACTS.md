# Evidence pack: active-nematic-rodsource (seed 9)

- world: `../../20261026T0400-c34-rod-motion-recoil/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm
- run: 301 frames x 100 steps x dt 0.05 = time 1500; grid [128, 128]; wall 675s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0400-c34-rod-motion-recoil/world.py --out collective/contrib/wip-c33-rr/kr0 --seeds 9 --frames 300 --no-movie`
- segmentation: matter > 0.49 of robust range [-0.9326, 0.9546], min area 6 px

## Measurements
- components: final 31, mean 31.5, max 62; occupancy final 0.24
- tracks: 2445; persistent (alive >= 50% of run): 0; longest 38 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [45, 36, 23], H1 [5, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.108/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 100, default): splits 893, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 717, merge/split ratio 0.803, nucleations 62
- channel total drift (end/start - 1): [0.0, 1.5445, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 866 at frame 124: holes 0, rim-vs-core 0.29, rim-vs-outside 0.26, heterogeneity 0.08; core [0.812, 0.591, 0.002] rim [0.618, 0.376, 0.007]
  - track 450 at frame 76: holes 0, rim-vs-core 0.23, rim-vs-outside 0.24, heterogeneity 0.07; core [0.777, 0.447, 0.001] rim [0.605, 0.288, 0.004]
  - track 1147 at frame 156: holes 0, rim-vs-core 0.27, rim-vs-outside 0.25, heterogeneity 0.08; core [0.78, 0.509, 0.008] rim [0.594, 0.319, 0.024]
  - track 1049 at frame 144: holes 0, rim-vs-core 0.17, rim-vs-outside 0.31, heterogeneity 0.07; core [0.795, 0.531, 0.007] rim [0.674, 0.42, 0.022]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 181 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.803, rim/outside 3.49 (aggregate of 181 individuals; 8/181 membrane-like individually; rim level 0.628)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.694, rim/outside 5.14 (aggregate of 181 individuals; 10/181 membrane-like individually; rim level 0.414)
  - radial surfactant s: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.75, rim/outside 2 (aggregate of 181 individuals; 88/181 membrane-like individually; rim level 0.122)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #866 (t=620, R_eq 3.19): none; #450 (t=380, R_eq 2.76): none; #1147 (t=780, R_eq 3.04): ['surfactant s']; #1049 (t=720, R_eq 3.83): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 18 of 181 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
