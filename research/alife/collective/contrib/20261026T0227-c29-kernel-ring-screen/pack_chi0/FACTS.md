# Evidence pack: ringswim-dl2 (seed 0)

- world: `../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 293s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/pack_chi0 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5307], min area 6 px

## Measurements
- components: final 20, mean 17.6, max 115; occupancy final 0.14
- tracks: 538; persistent (alive >= 50% of run): 0; longest 59 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.10, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 21, 20], H1 [22, 1, 0]
- motion: 41 long-lived tracks moved >= 1 body length; max speed 0.0529/time; max body lengths 5.8
- replication (lineage window K = 20 frames = time 1000, default): splits 185, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 4, merges 32, merge/split ratio 0.173, nucleations 0
- channel total drift (end/start - 1): [-0.2007, -0.8837, -0.4515, -0.59]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 328 at frame 143: holes 0, rim-vs-core 0.68, rim-vs-outside 0.59, heterogeneity 0.20; core [0.188, 0.849, 0.938, 0.803] rim [0.413, 0.338, 0.665, 0.537]
  - track 350 at frame 145: holes 0, rim-vs-core 0.78, rim-vs-outside 0.54, heterogeneity 0.21; core [0.414, 0.788, 1.0, 0.902] rim [0.564, 0.245, 0.718, 0.444]
  - track 58 at frame 27: holes 0, rim-vs-core 0.74, rim-vs-outside 0.52, heterogeneity 0.21; core [0.271, 0.839, 0.98, 0.833] rim [0.494, 0.286, 0.682, 0.501]
  - track 337 at frame 134: holes 0, rim-vs-core 0.68, rim-vs-outside 0.54, heterogeneity 0.19; core [0.174, 0.815, 0.934, 0.845] rim [0.347, 0.328, 0.66, 0.488]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 97 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 6.43, rim/outside 0.813 (aggregate of 97 individuals; 0/97 membrane-like individually; rim level 0.55)
  - radial K catalyst: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.823, rim/outside 6.79 (aggregate of 97 individuals; 8/97 membrane-like individually; rim level 0.596)
  - radial L link: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.983, rim/outside 5.15 (aggregate of 97 individuals; 3/97 membrane-like individually; rim level 0.7)
  - radial membrane (wall): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 7.53 (aggregate of 97 individuals; 36/97 membrane-like individually; rim level 0.702)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #328 (t=7150, R_eq 5.56): ['membrane (wall)']; #350 (t=7250, R_eq 3.83): none; #58 (t=1350, R_eq 5.23): ['membrane (wall)']; #337 (t=6700, R_eq 5.01): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 97 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
