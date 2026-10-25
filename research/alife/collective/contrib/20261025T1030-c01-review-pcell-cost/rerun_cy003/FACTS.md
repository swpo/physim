# Evidence pack: pcell (seed 3)

- world: `../world_cy003.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 61 frames x 50 steps x dt 1.0 = time 3000; grid [128, 128]; wall 10s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1030-c01-review-pcell-cost/world_cy003.py --out collective/contrib/20261025T1030-c01-review-pcell-cost/rerun_cy003 --seeds 3 --frames 60 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7175], min area 6 px

## Measurements
- components: final 17, mean 13.0, max 38; occupancy final 0.31
- tracks: 87; persistent (alive >= 50% of run): 13; longest 54 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.43 (1 = constant size)
- enclosures: components with a hole mean 9.15, final 15; holes at thresholds 0.2/0.35/0.5 final [2, 15, 17]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 17, 17], H1 [17, 17, 3]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 1000, default): splits 22, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio 0.273, nucleations 7
- channel total drift (end/start - 1): [-0.4681, -0.6584, 0.0454, -0.2023]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 55 at frame 34: holes 1, rim-vs-core 0.46, rim-vs-outside 0.68, heterogeneity 0.23; core [0.117, 0.739, 0.515, 0.423] rim [0.275, 0.365, 0.474, 0.63]
  - track 59 at frame 36: holes 1, rim-vs-core 0.24, rim-vs-outside 0.59, heterogeneity 0.20; core [0.163, 0.553, 0.503, 0.584] rim [0.259, 0.343, 0.426, 0.595]
  - track 61 at frame 36: holes 1, rim-vs-core 0.21, rim-vs-outside 0.64, heterogeneity 0.20; core [0.151, 0.593, 0.542, 0.58] rim [0.235, 0.423, 0.464, 0.585]
  - track 64 at frame 36: holes 1, rim-vs-core 0.19, rim-vs-outside 0.68, heterogeneity 0.19; core [0.164, 0.588, 0.493, 0.535] rim [0.226, 0.427, 0.459, 0.597]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [10, 20, 30, 40, 50, 60]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 7.52, rim/outside 0.817 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.553)
  - radial K particles: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.865, rim/outside 17.2 (aggregate of 78 individuals; 2/78 membrane-like individually; rim level 0.568)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.48, rim/outside 12.2 (aggregate of 78 individuals; 52/78 membrane-like individually; rim level 0.503)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 5.28, rim/outside 11.7 (aggregate of 78 individuals; 69/78 membrane-like individually; rim level 0.678)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #55 (t=1700, R_eq 9.25, ring): ['L link', 'membrane (wall)']; #59 (t=1800, R_eq 9.62, ring): ['L link', 'membrane (wall)']; #61 (t=1800, R_eq 9.84, ring): ['L link', 'membrane (wall)']; #64 (t=1800, R_eq 10.08, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 50 of 78 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 1 of 78 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
