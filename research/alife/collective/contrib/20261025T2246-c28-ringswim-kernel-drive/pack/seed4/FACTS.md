# Evidence pack: ringswim-dl2 (seed 4)

- world: `../../code/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 249s; status ok
- command: `python -m labkit.run /tmp/claude-0/c28sd/code/world.py --out /tmp/claude-0/c28sd/kpack --seeds 3 4 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.563], min area 6 px

## Measurements
- components: final 77, mean 72.4, max 105; occupancy final 0.18
- tracks: 1002; persistent (alive >= 50% of run): 1; longest 131 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.59 (1 = constant size)
- enclosures: components with a hole mean 0.25, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [86, 77, 77], H1 [50, 7, 0]
- motion: 186 long-lived tracks moved >= 1 body length; max speed 0.0302/time; max body lengths 4.5
- replication (lineage window K = 20 frames = time 1000, default): splits 433, persistent splits 123 (0 more failed only because the siblings re-merged within K), max generation 7, merges 13, merge/split ratio 0.03, nucleations 0
- channel total drift (end/start - 1): [-0.2981, -0.8554, -0.2137, -0.4183]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 310 at frame 111: holes 0, rim-vs-core 0.37, rim-vs-outside 0.86, heterogeneity 0.17; core [0.082, 0.761, 0.636, 0.777] rim [0.311, 0.478, 0.645, 0.714]
  - track 600 at frame 151: holes 0, rim-vs-core 0.45, rim-vs-outside 0.88, heterogeneity 0.19; core [0.106, 0.826, 0.719, 0.774] rim [0.342, 0.462, 0.653, 0.683]
  - track 619 at frame 155: holes 0, rim-vs-core 0.61, rim-vs-outside 0.50, heterogeneity 0.18; core [0.209, 0.781, 0.887, 0.884] rim [0.344, 0.395, 0.626, 0.508]
  - track 814 at frame 175: holes 0, rim-vs-core 0.41, rim-vs-outside 0.80, heterogeneity 0.16; core [0.105, 0.722, 0.671, 0.898] rim [0.301, 0.479, 0.65, 0.639]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 445 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 8.75, rim/outside 0.838 (aggregate of 445 individuals; 0/445 membrane-like individually; rim level 0.541)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.919, rim/outside 11.5 (aggregate of 445 individuals; 1/445 membrane-like individually; rim level 0.709)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.36, rim/outside 8.04 (aggregate of 445 individuals; 185/445 membrane-like individually; rim level 0.784)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 11.9 (aggregate of 445 individuals; 151/445 membrane-like individually; rim level 0.856)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #310 (t=5550, R_eq 7.57): ['L link']; #600 (t=7550, R_eq 6.51): ['L link', 'membrane (wall)']; #619 (t=7750, R_eq 4.41): none; #814 (t=8750, R_eq 6.77): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 445 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
