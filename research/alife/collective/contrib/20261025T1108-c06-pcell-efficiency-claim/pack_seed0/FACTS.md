# Evidence pack: pcell-yeff-cap (seed 0)

- world: `../world_cap_pack.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 617s; status ok
- command: `python -m labkit.run collective/work/pcell/yeff/world_cap_pack.py --out collective/work/pcell/yeff/pack_s0 --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5758], min area 6 px

## Measurements
- components: final 13, mean 18.2, max 26; occupancy final 0.38
- tracks: 64; persistent (alive >= 50% of run): 17; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.83 (1 = constant size)
- enclosures: components with a hole mean 7.17, final 8; holes at thresholds 0.2/0.35/0.5 final [27, 9, 9]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 13, 13], H1 [9, 8, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.000737/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 10000, default): splits 16, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.062, nucleations 9
- channel total drift (end/start - 1): [-0.6774, -0.4662, 0.6664, -0.0698, -0.2914]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 101: holes 1, rim-vs-core 0.34, rim-vs-outside 0.94, heterogeneity 0.22; core [0.178, 0.646, 0.618, 0.397, 0.942] rim [0.259, 0.4, 0.599, 0.581, 0.834]
  - track 29 at frame 103: holes 2, rim-vs-core 0.48, rim-vs-outside 1.19, heterogeneity 0.21; core [0.147, 0.693, 0.493, 0.256, 0.95] rim [0.247, 0.414, 0.603, 0.603, 0.866]
  - track 32 at frame 104: holes 2, rim-vs-core 0.40, rim-vs-outside 0.98, heterogeneity 0.22; core [0.16, 0.69, 0.526, 0.261, 0.948] rim [0.243, 0.432, 0.59, 0.535, 0.88]
  - track 53 at frame 139: holes 0, rim-vs-core 0.58, rim-vs-outside 1.15, heterogeneity 0.22; core [0.187, 0.632, 0.631, 0.469, 0.939] rim [0.364, 0.2, 0.628, 0.779, 0.774]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 106 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 2.95, rim/outside 0.956 (aggregate of 106 individuals; 0/106 membrane-like individually; rim level 0.485)
  - radial K particles: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.713, rim/outside 5.35 (aggregate of 106 individuals; 1/106 membrane-like individually; rim level 0.508)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.32, rim/outside 4.57 (aggregate of 106 individuals; 47/106 membrane-like individually; rim level 0.729)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3, rim/outside 3.98 (aggregate of 106 individuals; 82/106 membrane-like individually; rim level 0.676)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.963, rim/outside 4.34 (aggregate of 106 individuals; 0/106 membrane-like individually; rim level 0.855)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #23 (t=50500, R_eq 11.2, ring): ['membrane (wall)']; #29 (t=51500, R_eq 15.04): none; #32 (t=52000, R_eq 14.69, ring): none; #53 (t=69500, R_eq 7.94): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 38 of 106 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
