# Evidence pack: ringswim-dl2 (seed 5)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0434-c29-kernel-ring-seed2/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 0.5 (--dt; world META dt 1.0) = time 10000; grid [256, 256]; wall 966s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0434-c29-kernel-ring-seed2/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/rev10/dthalf_s5 --seeds 5 --frames 200 --spf 100 --dt 0.5 --size 256 256 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5881], min area 6 px

## Measurements
- components: final 291, mean 189.3, max 291; occupancy final 0.38
- tracks: 1395; persistent (alive >= 50% of run): 101; longest 158 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 26.75 (1 = constant size)
- enclosures: components with a hole mean 0.42, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [292, 292, 291], H1 [0, 0, 0]
- motion: 107 long-lived tracks moved >= 1 body length; max speed 0.0347/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 1000, default): splits 551, persistent splits 225 (0 more failed only because the siblings re-merged within K), max generation 6, merges 121, merge/split ratio 0.22, nucleations 3
- channel total drift (end/start - 1): [-0.5576, -0.7063, 0.4267, 0.3457]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 576 at frame 123: holes 0, rim-vs-core 0.60, rim-vs-outside 0.52, heterogeneity 0.16; core [0.134, 0.719, 0.705, 0.901] rim [0.276, 0.368, 0.422, 0.536]
  - track 608 at frame 123: holes 0, rim-vs-core 0.58, rim-vs-outside 0.46, heterogeneity 0.15; core [0.126, 0.685, 0.694, 0.904] rim [0.25, 0.386, 0.429, 0.509]
  - track 612 at frame 123: holes 0, rim-vs-core 0.61, rim-vs-outside 0.50, heterogeneity 0.17; core [0.139, 0.731, 0.716, 0.887] rim [0.285, 0.357, 0.418, 0.531]
  - track 1231 at frame 158: holes 0, rim-vs-core 0.55, rim-vs-outside 0.57, heterogeneity 0.16; core [0.122, 0.743, 0.702, 0.883] rim [0.261, 0.388, 0.442, 0.581]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1244 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 5.76, rim/outside 0.933 (aggregate of 1244 individuals; 0/1244 membrane-like individually; rim level 0.402)
  - radial K catalyst: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 10.4 (aggregate of 1244 individuals; 3/1244 membrane-like individually; rim level 0.699)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.55, rim/outside 9.44 (aggregate of 1244 individuals; 878/1244 membrane-like individually; rim level 0.794)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 8.26 (aggregate of 1244 individuals; 5/1244 membrane-like individually; rim level 0.915)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link
- membrane-like channels per top track at mid-life: #576 (t=6150, R_eq 5.73): none; #608 (t=6150, R_eq 5.23): ['L link']; #612 (t=6150, R_eq 5.29): ['L link']; #1231 (t=7900, R_eq 5.35): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.5 only relabels time (world META dt 1.0): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 1 of 1244 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
