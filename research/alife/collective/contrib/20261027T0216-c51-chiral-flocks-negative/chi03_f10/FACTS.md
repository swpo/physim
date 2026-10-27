# Evidence pack: chiral-eating-flocks (seed 0)

- world: `../../w2.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 301 frames x 40 steps x dt 0.25 = time 3000; grid [128, 128]; wall 20s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/tt/w2.py --out /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/tt/packs/chi03_f10 --seeds 0 --frames 300 --spf 40 --threshold 0.45 --no-movie`
- segmentation: matter > 0.59 of robust range [0.0, 0.7625], min area 6 px

## Measurements
- components: final 22, mean 17.4, max 24; occupancy final 0.06
- tracks: 1658; persistent (alive >= 50% of run): 0; longest 30 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 17, 9], H1 [4, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.226/time; max body lengths 9.5
- replication (lineage window K = 20 frames = time 200, default): splits 313, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 227, merge/split ratio 0.725, nucleations 788
- channel total drift (end/start - 1): [0.5239, -0.4547, -0.3363, 0.7591]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 483 at frame 91: holes 0, rim-vs-core 0.10, rim-vs-outside 0.23, heterogeneity 0.05; core [0.833, 0.061, 0.96, 0.006] rim [0.757, 0.117, 0.927, 0.025]
  - track 1288 at frame 245: holes 0, rim-vs-core 0.15, rim-vs-outside 0.19, heterogeneity 0.09; core [0.855, 0.056, 0.918, 0.022] rim [0.74, 0.111, 0.86, 0.077]
  - track 794 at frame 146: holes 0, rim-vs-core 0.05, rim-vs-outside 0.15, heterogeneity 0.03; core [0.774, 0.135, 0.911, 0.997] rim [0.737, 0.158, 0.897, 0.974]
  - track 1370 at frame 255: holes 0, rim-vs-core 0.12, rim-vs-outside 0.24, heterogeneity 0.10; core [0.855, 0.06, 0.953, 0.586] rim [0.764, 0.125, 0.92, 0.611]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 92 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial density rho: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.894, rim/outside 2.23 (aggregate of 92 individuals; 2/92 membrane-like individually; rim level 0.664)
  - radial food c: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.34, rim/outside 0.731 (aggregate of 92 individuals; 0/92 membrane-like individually; rim level 0.292)
  - radial |p|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.973, rim/outside 1.87 (aggregate of 92 individuals; 2/92 membrane-like individually; rim level 0.841)
  - radial p_x: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 1.05 (aggregate of 92 individuals; 0/92 membrane-like individually; rim level 0.519)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #483 (t=910, R_eq 3.95): none; #1288 (t=2450, R_eq 3.52): none; #794 (t=1460, R_eq 2.93): none; #1370 (t=2550, R_eq 6, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 15 of 92 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
