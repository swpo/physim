# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 72s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/screen/chi5kd12 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5649], min area 6 px

## Measurements
- components: final 70, mean 54.5, max 70; occupancy final 0.37
- tracks: 217; persistent (alive >= 50% of run): 64; longest 173 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.18 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [70, 70, 70], H1 [1, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.026/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 1000, default): splits 86, persistent splits 55 (0 more failed only because the siblings re-merged within K), max generation 4, merges 6, merge/split ratio 0.07, nucleations 0
- channel total drift (end/start - 1): [-0.5451, -0.7201, 0.373, 0.2638]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 108 at frame 114: holes 0, rim-vs-core 0.66, rim-vs-outside 0.50, heterogeneity 0.18; core [0.112, 0.75, 0.694, 0.874] rim [0.275, 0.337, 0.383, 0.492]
  - track 124 at frame 118: holes 0, rim-vs-core 0.62, rim-vs-outside 0.55, heterogeneity 0.18; core [0.113, 0.781, 0.727, 0.878] rim [0.258, 0.374, 0.422, 0.546]
  - track 126 at frame 118: holes 0, rim-vs-core 0.64, rim-vs-outside 0.53, heterogeneity 0.17; core [0.112, 0.762, 0.706, 0.877] rim [0.269, 0.356, 0.403, 0.518]
  - track 161 at frame 126: holes 0, rim-vs-core 0.62, rim-vs-outside 0.58, heterogeneity 0.17; core [0.112, 0.797, 0.744, 0.882] rim [0.252, 0.387, 0.43, 0.563]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 354 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 8.97, rim/outside 0.943 (aggregate of 354 individuals; 0/354 membrane-like individually; rim level 0.388)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.895, rim/outside 11.7 (aggregate of 354 individuals; 3/354 membrane-like individually; rim level 0.748)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.72, rim/outside 10.9 (aggregate of 354 individuals; 298/354 membrane-like individually; rim level 0.835)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 8.48 (aggregate of 354 individuals; 2/354 membrane-like individually; rim level 0.932)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link
- membrane-like channels per top track at mid-life: #108 (t=5700, R_eq 5.81): ['L link']; #124 (t=5900, R_eq 5.26): ['L link']; #126 (t=5900, R_eq 5.61): ['L link']; #161 (t=6300, R_eq 5.08): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 354 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
