# Evidence pack: ringswim-waste-chi0 (seed 5)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0806-c07-ringswim-claim/world_chi0.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 114s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_chi0.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev4/chi0 --seeds 5 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5621], min area 6 px

## Measurements
- components: final 22, mean 18.2, max 23; occupancy final 0.23
- tracks: 308; persistent (alive >= 50% of run): 0; longest 85 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 3.58, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 3, 18]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 22, 22], H1 [23, 20, 1]
- motion: 58 long-lived tracks moved >= 1 body length; max speed 0.0211/time; max body lengths 5.3
- replication (lineage window K = 20 frames = time 2000, default): splits 107, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 71, merge/split ratio 0.664, nucleations 0
- channel total drift (end/start - 1): [-0.3684, -0.7966, -0.13, -0.4336]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 213 at frame 158: holes 0, rim-vs-core 0.48, rim-vs-outside 0.96, heterogeneity 0.20; core [0.101, 0.827, 0.802, 0.54] rim [0.321, 0.467, 0.67, 0.738]
  - track 204 at frame 141: holes 0, rim-vs-core 0.54, rim-vs-outside 0.93, heterogeneity 0.22; core [0.073, 0.802, 0.775, 0.45] rim [0.306, 0.435, 0.607, 0.73]
  - track 88 at frame 71: holes 0, rim-vs-core 0.60, rim-vs-outside 0.93, heterogeneity 0.24; core [0.096, 0.85, 0.83, 0.457] rim [0.361, 0.426, 0.607, 0.71]
  - track 239 at frame 168: holes 0, rim-vs-core 0.50, rim-vs-outside 0.91, heterogeneity 0.22; core [0.092, 0.818, 0.777, 0.5] rim [0.318, 0.465, 0.634, 0.728]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 109 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 12.9, rim/outside 0.837 (aggregate of 109 individuals; 0/109 membrane-like individually; rim level 0.539)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.964, rim/outside 10.5 (aggregate of 109 individuals; 0/109 membrane-like individually; rim level 0.71)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.13, rim/outside 8.66 (aggregate of 109 individuals; 0/109 membrane-like individually; rim level 0.732)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.16, rim/outside 9.95 (aggregate of 109 individuals; 96/109 membrane-like individually; rim level 0.781)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #213 (t=15800, R_eq 6.7): ['membrane (wall)']; #204 (t=14100, R_eq 7.82): ['membrane (wall)']; #88 (t=7100, R_eq 7.59): ['membrane (wall)']; #239 (t=16800, R_eq 7.38): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 22 of 109 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
