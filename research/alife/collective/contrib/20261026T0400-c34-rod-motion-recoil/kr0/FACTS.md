# Evidence pack: active-nematic-rodsource (seed 0)

- world: `../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm
- run: 301 frames x 100 steps x dt 0.05 = time 1500; grid [128, 128]; wall 518s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0400-c34-rod-motion-recoil/world.py --out collective/contrib/20261026T0400-c34-rod-motion-recoil/kr0 --seeds 0 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.9132, 0.9251], min area 6 px

## Measurements
- components: final 45, mean 38.5, max 62; occupancy final 0.22
- tracks: 3364; persistent (alive >= 50% of run): 0; longest 53 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [57, 43, 28], H1 [13, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.107/time; max body lengths 2.8
- replication (lineage window K = 20 frames = time 100, default): splits 1264, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 953, merge/split ratio 0.754, nucleations 66
- channel total drift (end/start - 1): [0.0, 1.2417, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1112 at frame 126: holes 0, rim-vs-core 0.12, rim-vs-outside 0.16, heterogeneity 0.04; core [0.68, 0.234, 0.086] rim [0.575, 0.178, 0.122]
  - track 1007 at frame 111: holes 0, rim-vs-core 0.22, rim-vs-outside 0.22, heterogeneity 0.08; core [0.75, 0.464, 0.075] rim [0.605, 0.332, 0.167]
  - track 1165 at frame 121: holes 0, rim-vs-core 0.15, rim-vs-outside 0.21, heterogeneity 0.05; core [0.712, 0.378, 0.073] rim [0.596, 0.291, 0.125]
  - track 1138 at frame 118: holes 0, rim-vs-core 0.20, rim-vs-outside 0.23, heterogeneity 0.07; core [0.728, 0.473, 0.081] rim [0.592, 0.345, 0.158]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 225 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 3.23 (aggregate of 225 individuals; 6/225 membrane-like individually; rim level 0.62)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.698, rim/outside 4.74 (aggregate of 225 individuals; 9/225 membrane-like individually; rim level 0.403)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.4, rim/outside 2.03 (aggregate of 225 individuals; 142/225 membrane-like individually; rim level 0.242)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1112 (t=630, R_eq 2.11): ['surfactant s']; #1007 (t=555, R_eq 3.34): ['surfactant s']; #1165 (t=605, R_eq 3.48): none; #1138 (t=590, R_eq 4.07): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 17 of 225 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
