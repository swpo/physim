# Evidence pack: ringswim-waste-chi0 (seed 9)

- world: `../../../20261025T0806-c07-ringswim-claim/world_chi0.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 141s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_chi0.py --out collective/contrib/20261025T1350-c16-review-ringswim-c2/rerun_chi0/seed9 --seeds 9 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5579], min area 6 px

## Measurements
- components: final 22, mean 20.4, max 25; occupancy final 0.23
- tracks: 257; persistent (alive >= 50% of run): 4; longest 177 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.97 (1 = constant size)
- enclosures: components with a hole mean 2.97, final 2; holes at thresholds 0.2/0.35/0.5 final [0, 2, 19]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 23, 22], H1 [21, 21, 0]
- motion: 61 long-lived tracks moved >= 1 body length; max speed 0.0245/time; max body lengths 7.2
- replication (lineage window K = 20 frames = time 2000, default): splits 88, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 55, merge/split ratio 0.625, nucleations 2
- channel total drift (end/start - 1): [-0.3742, -0.7929, -0.1081, -0.3119]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 44 at frame 91: holes 0, rim-vs-core 0.44, rim-vs-outside 0.96, heterogeneity 0.19; core [0.085, 0.783, 0.738, 0.535] rim [0.299, 0.463, 0.662, 0.739]
  - track 90 at frame 109: holes 0, rim-vs-core 0.39, rim-vs-outside 0.87, heterogeneity 0.19; core [0.081, 0.736, 0.681, 0.577] rim [0.293, 0.426, 0.628, 0.683]
  - track 107 at frame 118: holes 0, rim-vs-core 0.39, rim-vs-outside 0.87, heterogeneity 0.19; core [0.08, 0.753, 0.704, 0.558] rim [0.292, 0.457, 0.642, 0.693]
  - track 69 at frame 82: holes 0, rim-vs-core 0.43, rim-vs-outside 0.88, heterogeneity 0.19; core [0.09, 0.782, 0.747, 0.597] rim [0.293, 0.428, 0.631, 0.689]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 129 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 14.2, rim/outside 0.845 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.539)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.951, rim/outside 12.5 (aggregate of 129 individuals; 1/129 membrane-like individually; rim level 0.733)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.13, rim/outside 9.77 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.766)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.53, rim/outside 11 (aggregate of 129 individuals; 121/129 membrane-like individually; rim level 0.82)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #44 (t=9100, R_eq 7.18): ['membrane (wall)']; #90 (t=10900, R_eq 7.78): ['membrane (wall)']; #107 (t=11800, R_eq 7.84): ['membrane (wall)']; #69 (t=8200, R_eq 7.09): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 18 of 129 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
