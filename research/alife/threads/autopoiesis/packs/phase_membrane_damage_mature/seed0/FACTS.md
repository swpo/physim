# Evidence pack: phase-membrane (seed 0)

- world: `../../../worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 12s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out threads/autopoiesis/packs/phase_membrane_damage_mature/seed0 --seeds 0 --frames 160 --damage 120:0.5:rim --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5428], min area 6 px

## Measurements
- components: final 15, mean 14.2, max 27; occupancy final 0.31
- tracks: 165; persistent (alive >= 50% of run): 0; longest 78 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 9.07, final 11; holes at thresholds 0.2/0.35/0.5 final [1, 11, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 16, 15], H1 [14, 14, 9]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0126/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 1000, default): splits 59, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 10, merge/split ratio 0.169, nucleations 0
- channel total drift (end/start - 1): [-0.4899, -0.6912, 0.0521, -0.182]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 106 at frame 117: holes 1, rim-vs-core 0.26, rim-vs-outside 0.81, heterogeneity 0.21; core [0.104, 0.865, 0.586, 0.492] rim [0.174, 0.641, 0.531, 0.595]
  - track 78 at frame 87: holes 1, rim-vs-core 0.37, rim-vs-outside 0.79, heterogeneity 0.23; core [0.118, 0.872, 0.649, 0.565] rim [0.236, 0.556, 0.505, 0.591]
  - track 67 at frame 44: holes 1, rim-vs-core 0.18, rim-vs-outside 0.76, heterogeneity 0.18; core [0.098, 0.727, 0.535, 0.7] rim [0.155, 0.597, 0.491, 0.607]
  - track 133 at frame 144: holes 1, rim-vs-core 0.19, rim-vs-outside 0.82, heterogeneity 0.20; core [0.108, 0.812, 0.594, 0.599] rim [0.171, 0.645, 0.532, 0.591]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 84 components >= 12 px at frames [27, 54, 81, 106, 133, 160]; 3 components of the damaged lineage after the cut left out):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 8.05, rim/outside 0.829 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.484)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.991, rim/outside 7.27 (aggregate of 84 individuals; 1/84 membrane-like individually; rim level 0.703)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.51, rim/outside 5.35 (aggregate of 84 individuals; 54/84 membrane-like individually; rim level 0.572)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.86, rim/outside 5.48 (aggregate of 84 individuals; 61/84 membrane-like individually; rim level 0.607)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #106 (t=5850, R_eq 11.41, ring): ['L link', 'membrane (wall)']; #78 (t=4350, R_eq 8.59, ring): ['L link', 'membrane (wall)']; #67 (t=2200, R_eq 13.37, ring): ['L link', 'membrane (wall)']; #133 (t=7200, R_eq 10.85, ring): ['L link', 'membrane (wall)']
- damage `rim` (requested 0.50 of the area) at frame 120 (t=6000): target track #111 (rule mature-compact: track age 39 frames vs K=20, area 436 px = 1.14x median, aspect 1.14); mask 221 px (96 inside the component)
- damage MEASURED: the target lost 21.4% of its matter (96 of 436 px lost > half their matter); matter lost outside it = 8.54% of its matter; share of all lost matter that was under labkit's mask 1
- (rim mode: the disk has the requested area but is centred on the boundary, so about half of it lies outside the matter component and cuts the layer at the edge)
- after damage, area of the individual's largest piece / area before the cut at t=[6000.0, 6400.0, 6800.0, 7200.0, 7600.0, 8000.0]: target #111 [0.787, 0.986, 0.637, 0.763, 0.925, 1.112]; comparator #116 [1.01, 0.812, 0.425, 0.558, 0.568, 0.843] (followed through its own splits and re-merges; None = died or merged with another individual); target lineage tracks [141, 142]; baseline recorded frame 119 (damage.png)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 37 of 84 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, damage.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
