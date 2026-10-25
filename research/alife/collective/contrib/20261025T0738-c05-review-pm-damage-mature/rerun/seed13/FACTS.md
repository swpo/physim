# Evidence pack: phase-membrane (seed 13)

- world: `../../../../../threads/autopoiesis/worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 12s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out collective/contrib/20261025T0738-c05-review-pm-damage-mature/rerun/seed13 --seeds 13 --frames 160 --damage 100:0.5:rim --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5409], min area 6 px

## Measurements
- components: final 18, mean 15.0, max 24; occupancy final 0.33
- tracks: 152; persistent (alive >= 50% of run): 1; longest 101 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.15 (1 = constant size)
- enclosures: components with a hole mean 9.66, final 13; holes at thresholds 0.2/0.35/0.5 final [2, 13, 16]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [16, 16, 10]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0106/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 1000, default): splits 60, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 2, merges 8, merge/split ratio 0.133, nucleations 0
- channel total drift (end/start - 1): [-0.5214, -0.6635, 0.1147, -0.0649]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 71 at frame 89: holes 1, rim-vs-core 0.19, rim-vs-outside 0.74, heterogeneity 0.17; core [0.07, 0.631, 0.37, 0.747] rim [0.148, 0.574, 0.473, 0.622]
  - track 73 at frame 78: holes 1, rim-vs-core 0.25, rim-vs-outside 0.74, heterogeneity 0.18; core [0.099, 0.744, 0.546, 0.675] rim [0.192, 0.535, 0.489, 0.582]
  - track 87 at frame 85: holes 1, rim-vs-core 0.24, rim-vs-outside 0.78, heterogeneity 0.19; core [0.108, 0.774, 0.587, 0.66] rim [0.187, 0.582, 0.501, 0.577]
  - track 100 at frame 93: holes 1, rim-vs-core 0.19, rim-vs-outside 0.85, heterogeneity 0.21; core [0.104, 0.816, 0.584, 0.586] rim [0.184, 0.647, 0.543, 0.588]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 89 components >= 12 px at frames [27, 54, 81, 106, 133, 160]; 2 components of the damaged lineage after the cut left out):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 13.7, rim/outside 0.843 (aggregate of 89 individuals; 0/89 membrane-like individually; rim level 0.459)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 4.71 (aggregate of 89 individuals; 0/89 membrane-like individually; rim level 0.728)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.8, rim/outside 3.86 (aggregate of 89 individuals; 78/89 membrane-like individually; rim level 0.573)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.22, rim/outside 3.81 (aggregate of 89 individuals; 78/89 membrane-like individually; rim level 0.621)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #71 (t=4450, R_eq 13.28): ['L link']; #73 (t=3900, R_eq 9.64, ring): ['L link', 'membrane (wall)']; #87 (t=4250, R_eq 9.89, ring): ['L link', 'membrane (wall)']; #100 (t=4650, R_eq 10.31, ring): ['L link', 'membrane (wall)']
- damage `rim` (requested 0.50 of the area) at frame 100 (t=5000): target = main-run track #73; the individual is 1 component(s): outer component 387 px + 121 px it encloses (121 px of low-matter holes) = 508 px = 1.02x the median individual, aspect 1.05 (rule mature-compact: track age 64 frames vs K=20; 12 individuals from 12 components at that frame; open-ring individuals, not eligible: 0); mask 249 px (108 inside the individual)
- damage MEASURED: the target lost 22.7% of its matter (inside the individual: its components and what they enclose; 108 of 508 px lost > half their matter); net matter lost outside it = 1.06% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (rim mode: the disk has the requested area but is centred on the individual's outer boundary, so about half of it lies outside the individual and cuts the layer at the edge)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[5000.0, 5600.0, 6200.0, 6800.0, 7400.0, 8000.0]: target [0.573, 0.805, 0.226, 0.445, 0.508, None] (matter [0.67, 0.922, 0.292, 0.545, 0.605, None]; pieces [1, 1, 1, 1, 1, 0]; last seen t=7650); comparator [1.0, 1.462, 0.513, 1.206, 1.621, 1.986] (matter [1.0, 1.398, 0.674, 1.217, 1.532, 1.884]; pieces [1, 1, 1, 1, 1, 1]). Follow-up: pre-cut field at frame 100, then recorded frames 100..160 segmented with the TARGETING range [0.0, 1.532609] (threshold 0.35), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 64 of 89 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
