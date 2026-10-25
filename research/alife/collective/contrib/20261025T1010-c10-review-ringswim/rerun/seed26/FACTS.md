# Evidence pack: ringswim-waste (seed 26)

- world: `../../../20261025T0806-c07-ringswim-claim/world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 132s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py --out collective/contrib/20261025T1010-c10-review-ringswim/rerun --seeds 25 26 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5578], min area 6 px

## Measurements
- components: final 2, mean 6.1, max 18; occupancy final 0.13
- tracks: 286; persistent (alive >= 50% of run): 0; longest 71 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 3.75, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [1, 1, 1]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.0807/time; max body lengths 16.2
- replication (lineage window K = 20 frames = time 2000, default): splits 89, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 85, merge/split ratio 0.955, nucleations 2
- channel total drift (end/start - 1): [-0.2654, -0.8494, -0.4609, -0.6949]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 13: holes 1, rim-vs-core 0.28, rim-vs-outside 0.67, heterogeneity 0.21; core [0.133, 0.705, 0.606, 0.649] rim [0.212, 0.493, 0.466, 0.577]
  - track 243 at frame 101: holes 1, rim-vs-core 0.20, rim-vs-outside 0.68, heterogeneity 0.16; core [0.088, 0.533, 0.382, 0.803] rim [0.158, 0.456, 0.411, 0.637]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 28 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 2.89, rim/outside 0.835 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.594)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 8.64 (aggregate of 28 individuals; 2/28 membrane-like individually; rim level 0.494)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 5.95 (aggregate of 28 individuals; 16/28 membrane-like individually; rim level 0.405)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.83, rim/outside 6.77 (aggregate of 28 individuals; 16/28 membrane-like individually; rim level 0.419)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #284 (t=16600, R_eq 18, ring): none; #285 (t=17100, R_eq 17.91, ring): none; #22 (t=1300, R_eq 10, ring): ['L link', 'membrane (wall)']; #243 (t=10100, R_eq 10.63, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 19 of 28 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
