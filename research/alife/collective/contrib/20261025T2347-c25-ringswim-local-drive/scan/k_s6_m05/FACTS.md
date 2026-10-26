# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../../20261025T2209-c28-ringswim-sibmd-claim/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 79s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T2209-c28-ringswim-sibmd-claim/world.py --out /home/user/physim/research/alife/collective/contrib/20261025T2347-c25-ringswim-local-drive/scan/k_s6_m05 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5615], min area 6 px

## Measurements
- components: final 17, mean 16.0, max 32; occupancy final 0.19
- tracks: 272; persistent (alive >= 50% of run): 0; longest 70 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.29, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 17, 16], H1 [8, 2, 0]
- motion: 20 long-lived tracks moved >= 1 body length; max speed 0.0194/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 1000, default): splits 115, persistent splits 28 (0 more failed only because the siblings re-merged within K), max generation 4, merges 7, merge/split ratio 0.061, nucleations 0
- channel total drift (end/start - 1): [-0.3536, -0.8314, -0.1322, -0.3973]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 195 at frame 163: holes 0, rim-vs-core 0.41, rim-vs-outside 0.98, heterogeneity 0.18; core [0.082, 0.75, 0.559, 0.611] rim [0.337, 0.463, 0.644, 0.745]
  - track 204 at frame 168: holes 0, rim-vs-core 0.44, rim-vs-outside 0.92, heterogeneity 0.19; core [0.13, 0.853, 0.706, 0.731] rim [0.334, 0.472, 0.662, 0.709]
  - track 138 at frame 111: holes 0, rim-vs-core 0.39, rim-vs-outside 0.71, heterogeneity 0.16; core [0.105, 0.681, 0.571, 0.869] rim [0.276, 0.451, 0.589, 0.61]
  - track 128 at frame 103: holes 0, rim-vs-core 0.34, rim-vs-outside 0.87, heterogeneity 0.17; core [0.088, 0.713, 0.552, 0.731] rim [0.309, 0.468, 0.626, 0.696]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 97 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 7.12, rim/outside 0.868 (aggregate of 97 individuals; 0/97 membrane-like individually; rim level 0.541)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.965, rim/outside 7.01 (aggregate of 97 individuals; 2/97 membrane-like individually; rim level 0.7)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.42, rim/outside 5.61 (aggregate of 97 individuals; 57/97 membrane-like individually; rim level 0.708)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.29, rim/outside 6.77 (aggregate of 97 individuals; 50/97 membrane-like individually; rim level 0.767)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #195 (t=8150, R_eq 9.76): ['L link', 'membrane (wall)']; #204 (t=8400, R_eq 6.58): ['L link', 'membrane (wall)']; #138 (t=5550, R_eq 8.18): ['L link']; #128 (t=5150, R_eq 9.24): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 97 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
