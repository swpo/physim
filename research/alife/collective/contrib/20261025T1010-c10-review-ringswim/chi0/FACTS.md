# Evidence pack: ringswim-waste-chi0 (seed 25)

- world: `../../20261025T0806-c07-ringswim-claim/world_chi0.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 144s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_chi0.py --out collective/contrib/20261025T1010-c10-review-ringswim/chi0 --seeds 25 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5592], min area 6 px

## Measurements
- components: final 25, mean 22.8, max 27; occupancy final 0.24
- tracks: 257; persistent (alive >= 50% of run): 2; longest 141 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.83 (1 = constant size)
- enclosures: components with a hole mean 2.05, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 17]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 25, 25], H1 [25, 20, 1]
- motion: 62 long-lived tracks moved >= 1 body length; max speed 0.0234/time; max body lengths 6.4
- replication (lineage window K = 20 frames = time 2000, default): splits 90, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 3, merges 58, merge/split ratio 0.644, nucleations 0
- channel total drift (end/start - 1): [-0.3881, -0.7841, -0.0534, -0.2924]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 95 at frame 131: holes 0, rim-vs-core 0.56, rim-vs-outside 0.98, heterogeneity 0.22; core [0.095, 0.864, 0.836, 0.482] rim [0.335, 0.471, 0.658, 0.747]
  - track 110 at frame 139: holes 0, rim-vs-core 0.43, rim-vs-outside 0.86, heterogeneity 0.20; core [0.081, 0.766, 0.714, 0.555] rim [0.293, 0.431, 0.612, 0.682]
  - track 96 at frame 114: holes 0, rim-vs-core 0.45, rim-vs-outside 0.88, heterogeneity 0.19; core [0.12, 0.824, 0.819, 0.669] rim [0.307, 0.443, 0.668, 0.686]
  - track 236 at frame 190: holes 0, rim-vs-core 0.31, rim-vs-outside 0.92, heterogeneity 0.19; core [0.102, 0.768, 0.735, 0.657] rim [0.242, 0.507, 0.639, 0.64]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 142 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 16.4, rim/outside 0.852 (aggregate of 142 individuals; 0/142 membrane-like individually; rim level 0.536)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.945, rim/outside 13.1 (aggregate of 142 individuals; 0/142 membrane-like individually; rim level 0.751)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 10.4 (aggregate of 142 individuals; 0/142 membrane-like individually; rim level 0.785)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.84, rim/outside 11.7 (aggregate of 142 individuals; 138/142 membrane-like individually; rim level 0.848)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #95 (t=13100, R_eq 7.11): ['membrane (wall)']; #110 (t=13900, R_eq 7.53): ['membrane (wall)']; #96 (t=11400, R_eq 6.18): ['membrane (wall)']; #236 (t=19000, R_eq 7.74): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 142 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
