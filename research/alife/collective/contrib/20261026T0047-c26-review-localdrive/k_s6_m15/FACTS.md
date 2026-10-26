# Evidence pack: ringswim-dl2 (seed 3)

- world: `../../../20261025T2209-c28-ringswim-sibmd-claim/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 57s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2209-c28-ringswim-sibmd-claim/world.py --out collective/contrib/_c26work/rev4/k_s6_m15 --seeds 3 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5724], min area 6 px

## Measurements
- components: final 1, mean 2.5, max 24; occupancy final 0.28
- tracks: 129; persistent (alive >= 50% of run): 0; longest 41 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.37, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 1], H1 [2, 1, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.282/time; max body lengths 5.4
- replication (lineage window K = 20 frames = time 1000, default): splits 35, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 27, merge/split ratio 0.771, nucleations 2
- channel total drift (end/start - 1): [-0.4493, -0.7445, 0.0338, -0.2946]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 128 at frame 180: holes 0, rim-vs-core 0.33, rim-vs-outside 0.96, heterogeneity 0.21; core [0.008, 0.668, 0.363, 0.34] rim [0.142, 0.593, 0.471, 0.613]
  - track 120 at frame 126: holes 0, rim-vs-core 0.38, rim-vs-outside 0.95, heterogeneity 0.20; core [0.002, 0.533, 0.295, 0.327] rim [0.141, 0.575, 0.467, 0.638]
  - track 6 at frame 10: holes 0, rim-vs-core 0.62, rim-vs-outside 0.44, heterogeneity 0.16; core [0.293, 0.671, 0.824, 0.905] rim [0.428, 0.324, 0.565, 0.487]
  - track 20 at frame 10: holes 0, rim-vs-core 0.61, rim-vs-outside 0.45, heterogeneity 0.16; core [0.281, 0.677, 0.768, 0.891] rim [0.45, 0.314, 0.536, 0.488]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 10 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.59, rim/outside 0.865 (aggregate of 10 individuals; 0/10 membrane-like individually; rim level 0.528)
  - radial K catalyst: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.835, rim/outside 2.61 (aggregate of 10 individuals; 3/10 membrane-like individually; rim level 0.321)
  - radial L link: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.982, rim/outside 2.38 (aggregate of 10 individuals; 3/10 membrane-like individually; rim level 0.337)
  - radial membrane (wall): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.907, rim/outside 3.07 (aggregate of 10 individuals; 3/10 membrane-like individually; rim level 0.378)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #128 (t=9000, R_eq 38.16): none; #120 (t=6300, R_eq 39.38, ring): none; #6 (t=500, R_eq 4.48): none; #20 (t=500, R_eq 5.14): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 10 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 4 of 10 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
