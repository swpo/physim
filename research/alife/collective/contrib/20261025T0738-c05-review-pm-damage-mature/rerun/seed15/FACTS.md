# Evidence pack: phase-membrane (seed 15)

- world: `../../../../../threads/autopoiesis/worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 12s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out collective/contrib/20261025T0738-c05-review-pm-damage-mature/rerun/seed15 --seeds 15 --frames 160 --damage 120:0.5:rim --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5389], min area 6 px

## Measurements
- components: final 16, mean 15.6, max 21; occupancy final 0.27
- tracks: 137; persistent (alive >= 50% of run): 3; longest 124 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.39 (1 = constant size)
- enclosures: components with a hole mean 9.81, final 9; holes at thresholds 0.2/0.35/0.5 final [0, 9, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 16, 16], H1 [15, 14, 9]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0133/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 1000, default): splits 55, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 8, merge/split ratio 0.145, nucleations 0
- channel total drift (end/start - 1): [-0.4482, -0.7435, -0.0503, -0.2764]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 50 at frame 73: holes 1, rim-vs-core 0.18, rim-vs-outside 0.84, heterogeneity 0.19; core [0.102, 0.789, 0.57, 0.617] rim [0.175, 0.627, 0.533, 0.605]
  - track 80 at frame 109: holes 0, rim-vs-core 0.59, rim-vs-outside 0.98, heterogeneity 0.24; core [0.138, 0.972, 0.733, 0.548] rim [0.338, 0.467, 0.602, 0.748]
  - track 83 at frame 109: holes 1, rim-vs-core 0.27, rim-vs-outside 0.77, heterogeneity 0.19; core [0.106, 0.788, 0.586, 0.637] rim [0.202, 0.55, 0.5, 0.592]
  - track 101 at frame 130: holes 1, rim-vs-core 0.17, rim-vs-outside 0.79, heterogeneity 0.17; core [0.091, 0.743, 0.523, 0.672] rim [0.147, 0.588, 0.49, 0.624]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 86 components >= 12 px at frames [27, 54, 81, 106, 133, 160]; 2 components of the damaged lineage after the cut left out):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 15, rim/outside 0.843 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.468)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 4.97 (aggregate of 86 individuals; 1/86 membrane-like individually; rim level 0.724)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.83, rim/outside 4.07 (aggregate of 86 individuals; 73/86 membrane-like individually; rim level 0.569)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.08, rim/outside 4.02 (aggregate of 86 individuals; 73/86 membrane-like individually; rim level 0.637)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #50 (t=3650, R_eq 10.43, ring): ['L link', 'membrane (wall)']; #80 (t=5450, R_eq 6.05): ['L link', 'membrane (wall)']; #83 (t=5450, R_eq 9.36, ring): ['L link', 'membrane (wall)']; #101 (t=6500, R_eq 11.48, ring): ['L link', 'membrane (wall)']
- damage `rim` (requested 0.50 of the area) at frame 120 (t=6000): target = main-run track #100; the individual is one component of 195 px = 0.55x the median individual, aspect 1.02 (rule mature-compact: track age 26 frames vs K=20; 18 individuals from 18 components at that frame; open-ring individuals, not eligible: 0); mask 97 px (47 inside the individual)
- damage MEASURED: the target lost 25.2% of its matter (inside the individual: its components and what they enclose; 47 of 195 px lost > half their matter); net matter lost outside it = 1.45% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (rim mode: the disk has the requested area but is centred on the individual's outer boundary, so about half of it lies outside the individual and cuts the layer at the edge)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[6000.0, 6400.0, 6800.0, 7200.0, 7600.0, 8000.0]: target [0.708, 1.41, 1.918, 2.528, 2.19, 0.487] (matter [0.718, 1.354, 1.702, 2.144, 2.212, 0.546]; pieces [1, 1, 1, 1, 1, 1]); comparator [1.0, 1.283, 1.389, 1.777, 2.099, 1.014] (matter [1.0, 1.227, 1.314, 1.556, 1.858, 1.126]; pieces [1, 1, 1, 1, 1, 1]). Follow-up: pre-cut field at frame 120, then recorded frames 120..160 segmented with the TARGETING range [0.0, 1.539405] (threshold 0.35), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 62 of 86 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
