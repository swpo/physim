# Evidence pack: ringswim-dl2 (seed 7)

- world: `../../../20261026T0227-c29-kernel-ring-screen/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 49 frames x 50 steps x dt 1.0 = time 2400; grid [256, 256]; wall 109s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T1030-c38-review-lonecell/rerun/pack_seed7 --seeds 7 --frames 48 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6012], min area 6 px

## Measurements
- components: final 129, mean 88.9, max 131; occupancy final 0.27
- tracks: 725; persistent (alive >= 50% of run): 14; longest 43 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.94 (1 = constant size)
- enclosures: components with a hole mean 0.98, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [145, 136, 128], H1 [37, 1, 0]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 0.0288/time; max body lengths 2.8
- replication (lineage window K = 20 frames = time 1000, default): splits 242, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 70, merge/split ratio 0.289, nucleations 1
- channel total drift (end/start - 1): [-0.4186, -0.7806, 0.1192, -0.0016]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 70 at frame 22: holes 0, rim-vs-core 0.35, rim-vs-outside 0.74, heterogeneity 0.16; core [0.106, 0.573, 0.473, 0.855] rim [0.327, 0.363, 0.454, 0.694]
  - track 85 at frame 19: holes 0, rim-vs-core 0.35, rim-vs-outside 0.84, heterogeneity 0.15; core [0.127, 0.577, 0.489, 0.873] rim [0.39, 0.398, 0.491, 0.73]
  - track 317 at frame 33: holes 0, rim-vs-core 0.51, rim-vs-outside 0.58, heterogeneity 0.16; core [0.176, 0.665, 0.637, 0.859] rim [0.342, 0.301, 0.402, 0.648]
  - track 451 at frame 38: holes 0, rim-vs-core 0.30, rim-vs-outside 0.75, heterogeneity 0.13; core [0.103, 0.553, 0.522, 0.916] rim [0.244, 0.394, 0.464, 0.707]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 556 components >= 12 px at frames [8, 16, 24, 32, 40, 48]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 5, rim/outside 0.881 (aggregate of 556 individuals; 0/556 membrane-like individually; rim level 0.492)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.922, rim/outside 7.05 (aggregate of 556 individuals; 2/556 membrane-like individually; rim level 0.542)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.41, rim/outside 6.12 (aggregate of 556 individuals; 282/556 membrane-like individually; rim level 0.611)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 7.42 (aggregate of 556 individuals; 4/556 membrane-like individually; rim level 0.854)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #70 (t=1100, R_eq 8.02): ['L link']; #85 (t=950, R_eq 8.23): ['L link']; #317 (t=1650, R_eq 5.11): ['L link']; #451 (t=1900, R_eq 6.15): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 556 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
