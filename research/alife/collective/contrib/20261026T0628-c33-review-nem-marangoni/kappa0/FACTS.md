# Evidence pack: active-nematic-marangoni (seed 7)

- world: `../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 508s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/wip-c33-nm/kappa0 --seeds 7 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8394, 0.5678], min area 6 px

## Measurements
- components: final 32, mean 23.6, max 32; occupancy final 0.09
- tracks: 115; persistent (alive >= 50% of run): 11; longest 147 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 31, 29], H1 [0, 0, 0]
- motion: 59 long-lived tracks moved >= 1 body length; max speed 0.278/time; max body lengths 9.9
- replication (lineage window K = 20 frames = time 100, default): splits 45, persistent splits 30 (0 more failed only because the siblings re-merged within K), max generation 4, merges 16, merge/split ratio 0.356, nucleations 8
- channel total drift (end/start - 1): [-0.4954, -0.4137, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 29 at frame 128: holes 0, rim-vs-core 0.53, rim-vs-outside 0.37, heterogeneity 0.16; core [0.952, 0.715, 0.421, 0.921] rim [0.785, 0.441, 0.837, 0.889]
  - track 31 at frame 128: holes 0, rim-vs-core 0.46, rim-vs-outside 0.33, heterogeneity 0.14; core [0.922, 0.634, 0.484, 0.908] rim [0.752, 0.426, 0.859, 0.878]
  - track 33 at frame 129: holes 0, rim-vs-core 0.62, rim-vs-outside 0.37, heterogeneity 0.17; core [0.947, 0.853, 0.446, 0.942] rim [0.751, 0.548, 0.943, 0.904]
  - track 74 at frame 160: holes 0, rim-vs-core 0.61, rim-vs-outside 0.37, heterogeneity 0.16; core [0.935, 0.884, 0.452, 0.981] rim [0.74, 0.577, 0.942, 0.944]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 160 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 4.59 (aggregate of 160 individuals; 0/160 membrane-like individually; rim level 0.715)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.779, rim/outside 8.87 (aggregate of 160 individuals; 12/160 membrane-like individually; rim level 0.536)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 3.32 (aggregate of 160 individuals; 83/160 membrane-like individually; rim level 0.62)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.948, rim/outside 1.27 (aggregate of 160 individuals; 0/160 membrane-like individually; rim level 0.791)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #29 (t=640, R_eq 4.22): none; #31 (t=640, R_eq 4.72): none; #33 (t=645, R_eq 4.58): none; #74 (t=800, R_eq 4.26): none

## Warnings
- radial: 2 of 160 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
