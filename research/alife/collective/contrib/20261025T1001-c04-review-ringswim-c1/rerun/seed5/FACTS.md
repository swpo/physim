# Evidence pack: ringswim-waste (seed 5)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 125s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev4/claim --seeds 5 6 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5573], min area 6 px

## Measurements
- components: final 6, mean 9.5, max 18; occupancy final 0.20
- tracks: 479; persistent (alive >= 50% of run): 0; longest 28 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 6.71, final 4; holes at thresholds 0.2/0.35/0.5 final [0, 6, 6]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 6, 6], H1 [10, 7, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.0571/time; max body lengths 5.9
- replication (lineage window K = 20 frames = time 2000, default): splits 163, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 135, merge/split ratio 0.828, nucleations 2
- channel total drift (end/start - 1): [-0.345, -0.808, -0.2569, -0.5312]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 13: holes 1, rim-vs-core 0.19, rim-vs-outside 0.84, heterogeneity 0.21; core [0.127, 0.754, 0.652, 0.591] rim [0.208, 0.604, 0.575, 0.592]
  - track 48 at frame 20: holes 0, rim-vs-core 0.59, rim-vs-outside 0.99, heterogeneity 0.23; core [0.132, 0.908, 0.706, 0.483] rim [0.367, 0.459, 0.631, 0.778]
  - track 170 at frame 87: holes 1, rim-vs-core 0.26, rim-vs-outside 0.69, heterogeneity 0.18; core [0.086, 0.54, 0.426, 0.861] rim [0.154, 0.503, 0.458, 0.619]
  - track 442 at frame 188: holes 1, rim-vs-core 0.18, rim-vs-outside 0.82, heterogeneity 0.23; core [0.082, 0.736, 0.536, 0.552] rim [0.19, 0.595, 0.554, 0.578]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 49 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 7.51, rim/outside 0.817 (aggregate of 49 individuals; 0/49 membrane-like individually; rim level 0.549)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.962, rim/outside 8.86 (aggregate of 49 individuals; 2/49 membrane-like individually; rim level 0.648)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.45, rim/outside 6.56 (aggregate of 49 individuals; 31/49 membrane-like individually; rim level 0.608)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.11, rim/outside 7.53 (aggregate of 49 individuals; 34/49 membrane-like individually; rim level 0.615)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #5 (t=1300, R_eq 10.09, ring): ['K catalyst', 'L link', 'membrane (wall)']; #48 (t=2000, R_eq 6.65): ['L link', 'membrane (wall)']; #170 (t=8700, R_eq 10.75, ring): ['L link', 'membrane (wall)']; #442 (t=18800, R_eq 13.24): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 22 of 49 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
