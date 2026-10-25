# Evidence pack: cips-nr (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim/world.py; mutation: two conserved enzymes with non-reciprocal cross-chemotaxis (e1 chases p2, e2 flees p1)
- run: 251 frames x 100 steps x dt 0.1 = time 2500; grid [256, 256]; wall 499s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2002-c23-cips-nonreciprocal-sighting/world.py --out collective/contrib/20261025T2002-c23-cips-nonreciprocal-sighting/pack --seeds 0 --frames 250 --no-movie`
- segmentation: matter > 0.40 of robust range [0.0013, 0.9947], min area 6 px

## Measurements
- components: final 179, mean 185.0, max 320; occupancy final 0.20
- tracks: 2157; persistent (alive >= 50% of run): 73; longest 197 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.67 (1 = constant size)
- enclosures: components with a hole mean 0.30, final 0; holes at thresholds 0.2/0.35/0.5 final [3, 1, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [222, 194, 169], H1 [4, 0, 0]
- motion: 166 long-lived tracks moved >= 1 body length; max speed 0.0513/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 200, default): splits 581, persistent splits 52 (0 more failed only because the siblings re-merged within K), max generation 3, merges 444, merge/split ratio 0.764, nucleations 562
- channel total drift (end/start - 1): [-0.0, 0.0, -0.5402, -0.5612, -0.4082]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 50 at frame 153: holes 0, rim-vs-core 0.34, rim-vs-outside 0.46, heterogeneity 0.06; core [0.94, 0.0, 0.833, 0.026, 0.238] rim [0.649, 0.0, 0.666, 0.032, 0.29]
  - track 90 at frame 153: holes 0, rim-vs-core 0.37, rim-vs-outside 0.48, heterogeneity 0.07; core [0.967, 0.0, 0.931, 0.024, 0.158] rim [0.666, 0.0, 0.722, 0.033, 0.231]
  - track 6 at frame 145: holes 0, rim-vs-core 0.30, rim-vs-outside 0.44, heterogeneity 0.05; core [0.921, 0.0, 0.776, 0.014, 0.309] rim [0.652, 0.0, 0.638, 0.017, 0.352]
  - track 2058 at frame 237: holes 0, rim-vs-core 0.32, rim-vs-outside 0.57, heterogeneity 0.10; core [0.226, 0.894, 0.25, 0.908, 0.006] rim [0.138, 0.666, 0.204, 0.721, 0.076]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1095 components >= 12 px at frames [84, 126, 166, 208, 250]):
  - radial e1: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.891, rim/outside 11.5 (aggregate of 1095 individuals; 8/1095 membrane-like individually; rim level 0.518)
  - radial e2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.795, rim/outside 5.46 (aggregate of 1095 individuals; 61/1095 membrane-like individually; rim level 0.292)
  - radial p1: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 2.56 (aggregate of 1095 individuals; 0/1095 membrane-like individually; rim level 0.519)
  - radial p2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.832, rim/outside 1.95 (aggregate of 1095 individuals; 1/1095 membrane-like individually; rim level 0.363)
  - radial F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.52, rim/outside 0.799 (aggregate of 1095 individuals; 0/1095 membrane-like individually; rim level 0.285)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #50 (t=1530, R_eq 2.88): none; #90 (t=1530, R_eq 3.66): none; #6 (t=1450, R_eq 2.39): none; #2058 (t=2370, R_eq 7.4): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 1095 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
