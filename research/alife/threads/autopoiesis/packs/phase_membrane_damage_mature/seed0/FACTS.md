# Evidence pack: phase-membrane (seed 0)

- world: `../../../worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 13s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out threads/autopoiesis/packs/phase_membrane_damage_mature/seed0 --seeds 0 --frames 160 --damage 120:0.3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.544], min area 6 px

## Measurements
- components: final 20, mean 14.4, max 27; occupancy final 0.33
- tracks: 170; persistent (alive >= 50% of run): 0; longest 77 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 9.14, final 13; holes at thresholds 0.2/0.35/0.5 final [0, 13, 17]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 20, 20], H1 [17, 17, 12]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00729/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 1000, default): splits 61, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 3, merges 10, merge/split ratio 0.164, nucleations 0
- channel total drift (end/start - 1): [-0.5042, -0.6733, 0.1134, -0.0947]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 106 at frame 116: holes 1, rim-vs-core 0.26, rim-vs-outside 0.82, heterogeneity 0.21; core [0.116, 0.875, 0.628, 0.528] rim [0.175, 0.65, 0.536, 0.592]
  - track 78 at frame 87: holes 1, rim-vs-core 0.36, rim-vs-outside 0.80, heterogeneity 0.22; core [0.117, 0.873, 0.646, 0.561] rim [0.235, 0.561, 0.511, 0.596]
  - track 67 at frame 44: holes 1, rim-vs-core 0.18, rim-vs-outside 0.76, heterogeneity 0.18; core [0.098, 0.727, 0.534, 0.7] rim [0.155, 0.597, 0.491, 0.606]
  - track 133 at frame 144: holes 1, rim-vs-core 0.19, rim-vs-outside 0.83, heterogeneity 0.20; core [0.097, 0.79, 0.554, 0.591] rim [0.17, 0.619, 0.519, 0.606]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 89 components >= 12 px at frames [27, 54, 81, 106, 133, 160]; 2 components of the damaged lineage after the cut left out):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 8.13, rim/outside 0.834 (aggregate of 89 individuals; 0/89 membrane-like individually; rim level 0.481)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.99, rim/outside 7.06 (aggregate of 89 individuals; 1/89 membrane-like individually; rim level 0.707)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.52, rim/outside 5.25 (aggregate of 89 individuals; 56/89 membrane-like individually; rim level 0.58)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.81, rim/outside 5.45 (aggregate of 89 individuals; 63/89 membrane-like individually; rim level 0.622)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #106 (t=5800, R_eq 11.16, ring): ['L link', 'membrane (wall)']; #78 (t=4350, R_eq 8.57, ring): ['L link', 'membrane (wall)']; #67 (t=2200, R_eq 13.37, ring): ['L link', 'membrane (wall)']; #133 (t=7200, R_eq 10.28, ring): ['L link', 'membrane (wall)']
- damage `core` (requested 0.30 of the area) at frame 120 (t=6000): target track #111 (rule mature-compact: track age 39 frames vs K=20, area 436 px = 1.14x median, aspect 1.14); mask 131 px (0 inside the component)
- damage MEASURED: the target lost 30.3% of its matter (135 of 436 px lost > half their matter); matter lost outside it = 12.4% of its matter; share of all lost matter that was under labkit's mask 0.111
- after damage, area of the individual's largest piece / area before the cut at t=[6000.0, 6400.0, 6800.0, 7200.0, 7600.0, 8000.0]: target #111 [0.691, 1.44, 1.951, 0.351, 0.546, 0.719]; comparator #116 [1.012, 0.814, 0.426, 0.559, 0.562, 0.816] (followed through its own splits and re-merges; None = died or merged with another individual); target lineage tracks [152, 153, 154]; baseline recorded frame 119 (damage.png)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 38 of 89 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- the world's damage() hook did not erase where labkit's mask was (only 11% of the lost matter was under it): the MEASURED loss is what counts

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, damage.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
