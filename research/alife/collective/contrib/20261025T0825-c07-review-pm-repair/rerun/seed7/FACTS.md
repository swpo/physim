# Evidence pack: phase-membrane (seed 7)

- world: `../../../../../threads/autopoiesis/worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 16s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out collective/contrib/_c07rev5/rerun/seed7 --seeds 7 --frames 160 --damage 120:0.5:rim --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5415], min area 6 px

## Measurements
- components: final 15, mean 14.6, max 21; occupancy final 0.29
- tracks: 140; persistent (alive >= 50% of run): 3; longest 104 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.55 (1 = constant size)
- enclosures: components with a hole mean 9.44, final 11; holes at thresholds 0.2/0.35/0.5 final [1, 11, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [16, 14, 10]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00686/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 1000, default): splits 58, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 4, merges 4, merge/split ratio 0.069, nucleations 0
- channel total drift (end/start - 1): [-0.4503, -0.703, -0.0172, -0.0842]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 60 at frame 91: holes 1, rim-vs-core 0.18, rim-vs-outside 0.80, heterogeneity 0.19; core [0.097, 0.769, 0.565, 0.65] rim [0.163, 0.614, 0.516, 0.61]
  - track 84 at frame 118: holes 1, rim-vs-core 0.17, rim-vs-outside 0.80, heterogeneity 0.18; core [0.093, 0.73, 0.503, 0.702] rim [0.159, 0.593, 0.499, 0.627]
  - track 88 at frame 118: holes 1, rim-vs-core 0.30, rim-vs-outside 0.74, heterogeneity 0.20; core [0.115, 0.803, 0.617, 0.633] rim [0.213, 0.552, 0.497, 0.582]
  - track 117 at frame 141: holes 1, rim-vs-core 0.23, rim-vs-outside 0.78, heterogeneity 0.20; core [0.107, 0.792, 0.597, 0.635] rim [0.188, 0.597, 0.518, 0.595]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 86 components >= 12 px at frames [27, 54, 81, 106, 133, 160]; 2 components of the damaged lineage after the cut left out):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 11.6, rim/outside 0.818 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.488)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 6.39 (aggregate of 86 individuals; 1/86 membrane-like individually; rim level 0.75)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.67, rim/outside 5.15 (aggregate of 86 individuals; 73/86 membrane-like individually; rim level 0.586)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.09, rim/outside 4.86 (aggregate of 86 individuals; 75/86 membrane-like individually; rim level 0.632)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #60 (t=4550, R_eq 10.22, ring): ['L link', 'membrane (wall)']; #84 (t=5900, R_eq 11.89, ring): ['L link', 'membrane (wall)']; #88 (t=5900, R_eq 9.51, ring): ['L link', 'membrane (wall)']; #117 (t=7050, R_eq 9.44, ring): ['L link', 'membrane (wall)']
- damage `rim` (requested 0.50 of the area) at frame 120 (t=6000): target = main-run track #88; the individual is 1 component(s): outer component 306 px + 61 px it encloses (61 px of low-matter holes) = 367 px = 1.00x the median individual, aspect 1.16 (rule mature-compact: track age 44 frames vs K=20; 16 individuals from 16 components at that frame; open-ring individuals, not eligible: 0); mask 185 px (88 inside the individual)
- damage MEASURED: the target lost 24.6% of its matter (inside the individual: its components and what they enclose; 88 of 367 px lost > half their matter); net matter lost outside it = 1.18% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (rim mode: the disk has the requested area but is centred on the individual's outer boundary, so about half of it lies outside the individual and cuts the layer at the edge)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[6000.0, 6400.0, 6800.0, 7200.0, 7600.0, 8000.0]: target [0.605, 1.139, 1.518, 1.676, 1.602, 1.605] (matter [0.676, 1.129, 1.383, 1.52, 1.512, 1.573]; pieces [1, 1, 1, 1, 1, 1]); comparator [1.0, 1.246, 1.468, None, None, None] (matter [1.0, 1.184, 1.385, None, None, None]; pieces [1, 1, 1, 0, 0, 0]; last seen t=7150). Follow-up: pre-cut field at frame 120, then recorded frames 120..160 segmented with the TARGETING range [0.0, 1.538765] (threshold 0.35), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 51 of 86 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
