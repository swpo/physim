# Evidence pack: active-nematic-rodsource (seed 1)

- world: `../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm
- run: 301 frames x 100 steps x dt 0.05 = time 1500; grid [128, 128]; wall 521s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0400-c34-rod-motion-recoil/world.py --out collective/contrib/20261026T0400-c34-rod-motion-recoil/kr0_s1 --seeds 1 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.9104, 0.9243], min area 6 px

## Measurements
- components: final 39, mean 39.0, max 66; occupancy final 0.22
- tracks: 3505; persistent (alive >= 50% of run): 0; longest 37 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [48, 40, 27], H1 [6, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.197/time; max body lengths 2.8
- replication (lineage window K = 20 frames = time 100, default): splits 1322, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1001, merge/split ratio 0.757, nucleations 68
- channel total drift (end/start - 1): [0.0, 1.3594, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2850 at frame 262: holes 0, rim-vs-core 0.25, rim-vs-outside 0.23, heterogeneity 0.08; core [0.776, 0.468, 0.047] rim [0.608, 0.301, 0.132]
  - track 2177 at frame 207: holes 0, rim-vs-core 0.14, rim-vs-outside 0.19, heterogeneity 0.06; core [0.68, 0.398, 0.175] rim [0.604, 0.329, 0.274]
  - track 1263 at frame 124: holes 0, rim-vs-core 0.26, rim-vs-outside 0.21, heterogeneity 0.09; core [0.787, 0.242, 0.101] rim [0.615, 0.15, 0.267]
  - track 31 at frame 20: holes 0, rim-vs-core 0.20, rim-vs-outside 0.20, heterogeneity 0.07; core [0.721, 0.433, 0.047] rim [0.587, 0.291, 0.079]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 221 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 3.05 (aggregate of 221 individuals; 6/221 membrane-like individually; rim level 0.602)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.701, rim/outside 4.31 (aggregate of 221 individuals; 13/221 membrane-like individually; rim level 0.38)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 1.93 (aggregate of 221 individuals; 133/221 membrane-like individually; rim level 0.248)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2850 (t=1310, R_eq 3.19): ['surfactant s']; #2177 (t=1035, R_eq 2.82): none; #1263 (t=620, R_eq 2.71): ['surfactant s']; #31 (t=100, R_eq 4.26): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 20 of 221 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
