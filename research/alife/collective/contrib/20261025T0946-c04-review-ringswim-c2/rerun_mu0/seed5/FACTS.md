# Evidence pack: ringswim-waste-mu0 (seed 5)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0806-c07-ringswim-claim/world_mu0.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 38s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_mu0.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev4/mu0 --seeds 5 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5345], min area 6 px

## Measurements
- components: final 17, mean 16.2, max 22; occupancy final 0.27
- tracks: 228; persistent (alive >= 50% of run): 0; longest 94 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 10.07, final 10; holes at thresholds 0.2/0.35/0.5 final [1, 10, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 17, 17], H1 [16, 15, 10]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.00813/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 2000, default): splits 102, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 5, merges 3, merge/split ratio 0.029, nucleations 0
- channel total drift (end/start - 1): [-0.4327, -0.7569, -0.0844, -0.3192]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 53 at frame 84: holes 1, rim-vs-core 0.20, rim-vs-outside 0.85, heterogeneity 0.19; core [0.111, 0.783, 0.668, 0.647] rim [0.167, 0.615, 0.578, 0.618]
  - track 78 at frame 103: holes 0, rim-vs-core 0.58, rim-vs-outside 1.04, heterogeneity 0.23; core [0.098, 0.929, 0.694, 0.472] rim [0.323, 0.486, 0.651, 0.768]
  - track 66 at frame 82: holes 1, rim-vs-core 0.32, rim-vs-outside 0.86, heterogeneity 0.23; core [0.134, 0.882, 0.777, 0.593] rim [0.224, 0.629, 0.6, 0.576]
  - track 186 at frame 185: holes 0, rim-vs-core 0.59, rim-vs-outside 0.47, heterogeneity 0.16; core [0.298, 0.737, 0.959, 0.852] rim [0.384, 0.41, 0.74, 0.424]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 100 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 10.3, rim/outside 0.828 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.491)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 7.94 (aggregate of 100 individuals; 3/100 membrane-like individually; rim level 0.711)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.61, rim/outside 5.8 (aggregate of 100 individuals; 78/100 membrane-like individually; rim level 0.649)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.06, rim/outside 6.33 (aggregate of 100 individuals; 74/100 membrane-like individually; rim level 0.649)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #53 (t=8400, R_eq 10.97, ring): ['L link', 'membrane (wall)']; #78 (t=10300, R_eq 7.14): ['L link', 'membrane (wall)']; #66 (t=8200, R_eq 8.76, ring): ['L link', 'membrane (wall)']; #186 (t=18500, R_eq 3.66): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 51 of 100 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
