# Evidence pack: ringswim-waste (seed 7)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 117s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/rev3/rerun --seeds 7 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5556], min area 6 px

## Measurements
- components: final 2, mean 4.6, max 22; occupancy final 0.13
- tracks: 169; persistent (alive >= 50% of run): 0; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 2.65, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [1, 1, 1]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.082/time; max body lengths 21.7
- replication (lineage window K = 20 frames = time 2000, default): splits 52, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 50, merge/split ratio 0.962, nucleations 2
- channel total drift (end/start - 1): [-0.2649, -0.8506, -0.4593, -0.6558]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 49 at frame 24: holes 1, rim-vs-core 0.25, rim-vs-outside 0.65, heterogeneity 0.20; core [0.112, 0.671, 0.521, 0.67] rim [0.214, 0.483, 0.445, 0.574]
  - track 2 at frame 13: holes 1, rim-vs-core 0.33, rim-vs-outside 0.77, heterogeneity 0.22; core [0.124, 0.776, 0.607, 0.553] rim [0.24, 0.5, 0.484, 0.605]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 19 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.64, rim/outside 0.887 (aggregate of 19 individuals; 0/19 membrane-like individually; rim level 0.614)
  - radial K catalyst: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.973, rim/outside 3.39 (aggregate of 19 individuals; 0/19 membrane-like individually; rim level 0.332)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.32, rim/outside 3.26 (aggregate of 19 individuals; 7/19 membrane-like individually; rim level 0.281)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.81, rim/outside 3.35 (aggregate of 19 individuals; 6/19 membrane-like individually; rim level 0.298)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #167 (t=15100, R_eq 18.42, ring): none; #168 (t=16600, R_eq 18.51, ring): none; #49 (t=2400, R_eq 10, ring): ['L link', 'membrane (wall)']; #2 (t=1300, R_eq 8.16, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 19 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
