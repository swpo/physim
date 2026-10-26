# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 77s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/screen/chi4kd08 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5937], min area 6 px

## Measurements
- components: final 39, mean 34.0, max 51; occupancy final 0.17
- tracks: 389; persistent (alive >= 50% of run): 0; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [41, 39, 39], H1 [6, 0, 0]
- motion: 33 long-lived tracks moved >= 1 body length; max speed 0.034/time; max body lengths 3.4
- replication (lineage window K = 20 frames = time 1000, default): splits 173, persistent splits 63 (0 more failed only because the siblings re-merged within K), max generation 7, merges 9, merge/split ratio 0.052, nucleations 0
- channel total drift (end/start - 1): [-0.3766, -0.8591, -0.1406, -0.4249]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 128 at frame 92: holes 0, rim-vs-core 0.27, rim-vs-outside 0.97, heterogeneity 0.16; core [0.058, 0.71, 0.51, 0.782] rim [0.235, 0.521, 0.586, 0.767]
  - track 238 at frame 156: holes 0, rim-vs-core 0.51, rim-vs-outside 0.35, heterogeneity 0.14; core [0.152, 0.603, 0.66, 0.889] rim [0.268, 0.409, 0.509, 0.455]
  - track 104 at frame 82: holes 0, rim-vs-core 0.31, rim-vs-outside 0.91, heterogeneity 0.15; core [0.07, 0.715, 0.569, 0.846] rim [0.232, 0.48, 0.563, 0.722]
  - track 354 at frame 187: holes 0, rim-vs-core 0.41, rim-vs-outside 0.64, heterogeneity 0.16; core [0.167, 0.668, 0.734, 0.898] rim [0.23, 0.479, 0.524, 0.613]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 203 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 6.19, rim/outside 0.889 (aggregate of 203 individuals; 0/203 membrane-like individually; rim level 0.496)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 10.1 (aggregate of 203 individuals; 1/203 membrane-like individually; rim level 0.718)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 8.69 (aggregate of 203 individuals; 132/203 membrane-like individually; rim level 0.786)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 8.81 (aggregate of 203 individuals; 26/203 membrane-like individually; rim level 0.897)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link
- membrane-like channels per top track at mid-life: #128 (t=4600, R_eq 7.98): ['L link']; #238 (t=7800, R_eq 5.53): none; #104 (t=4100, R_eq 6.77): ['L link']; #354 (t=9350, R_eq 5.2): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 203 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
