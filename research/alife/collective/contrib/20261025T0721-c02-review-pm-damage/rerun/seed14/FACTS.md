# Evidence pack: phase-membrane (seed 14)

- world: `../../../../../../../../home/user/physim/research/alife/threads/autopoiesis/worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 20s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out collective/contrib/20261025T0721-c02-review-pm-damage/rerun/seed14 --seeds 14 --frames 160 --damage 120:0.5:rim --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5376], min area 6 px

## Measurements
- components: final 20, mean 16.0, max 23; occupancy final 0.29
- tracks: 129; persistent (alive >= 50% of run): 5; longest 112 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.39 (1 = constant size)
- enclosures: components with a hole mean 10.04, final 9; holes at thresholds 0.2/0.35/0.5 final [1, 9, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 21, 20], H1 [19, 17, 5]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00894/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 1000, default): splits 49, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 2, merges 4, merge/split ratio 0.082, nucleations 0
- channel total drift (end/start - 1): [-0.469, -0.7177, 0.0275, -0.2558]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 63 at frame 98: holes 1, rim-vs-core 0.18, rim-vs-outside 0.86, heterogeneity 0.18; core [0.081, 0.742, 0.489, 0.619] rim [0.167, 0.595, 0.525, 0.634]
  - track 45 at frame 52: holes 1, rim-vs-core 0.37, rim-vs-outside 0.85, heterogeneity 0.22; core [0.111, 0.867, 0.633, 0.554] rim [0.247, 0.542, 0.519, 0.601]
  - track 79 at frame 117: holes 1, rim-vs-core 0.16, rim-vs-outside 0.80, heterogeneity 0.19; core [0.089, 0.744, 0.527, 0.653] rim [0.163, 0.615, 0.518, 0.6]
  - track 98 at frame 132: holes 1, rim-vs-core 0.17, rim-vs-outside 0.81, heterogeneity 0.19; core [0.102, 0.775, 0.571, 0.625] rim [0.169, 0.623, 0.525, 0.602]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 97 components >= 12 px at frames [27, 54, 81, 106, 133, 160]; 3 components of the damaged lineage after the cut left out):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 11.6, rim/outside 0.855 (aggregate of 97 individuals; 0/97 membrane-like individually; rim level 0.492)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 6.33 (aggregate of 97 individuals; 1/97 membrane-like individually; rim level 0.76)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.75, rim/outside 4.98 (aggregate of 97 individuals; 84/97 membrane-like individually; rim level 0.629)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.68, rim/outside 5.01 (aggregate of 97 individuals; 82/97 membrane-like individually; rim level 0.682)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #63 (t=4900, R_eq 10.84, ring): ['L link', 'membrane (wall)']; #45 (t=2600, R_eq 8.63, ring): ['L link', 'membrane (wall)']; #79 (t=5850, R_eq 12.02, ring): ['L link', 'membrane (wall)']; #98 (t=6600, R_eq 11.31, ring): ['L link', 'membrane (wall)']
- damage `rim` (requested 0.50 of the area) at frame 120 (t=6000): target = main-run track #93; the individual is 1 component(s): outer component 301 px + 38 px it encloses (38 px of low-matter holes) = 339 px = 0.83x the median individual, aspect 1.11 (rule mature-compact: track age 23 frames vs K=20; 17 individuals from 17 components at that frame; open-ring individuals, not eligible: 0); mask 177 px (85 inside the individual)
- damage MEASURED: the target lost 24.9% of its matter (inside the individual: its components and what they enclose; 85 of 339 px lost > half their matter); net matter lost outside it = 1.12% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (rim mode: the disk has the requested area but is centred on the individual's outer boundary, so about half of it lies outside the individual and cuts the layer at the edge)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[6000.0, 6400.0, 6800.0, 7200.0, 7600.0, 8000.0]: target [0.643, 0.923, 1.336, 1.422, 0.496, 0.953] (matter [0.699, 0.952, 1.246, 1.491, 1.052, 1.854]; pieces [1, 1, 1, 1, 2, 2]); comparator [1.0, 0.092, None, None, None, None] (matter [1.0, 0.086, None, None, None, None]; pieces [1, 1, 0, 0, 0, 0]; last seen t=6400). Follow-up: pre-cut field at frame 120, then recorded frames 120..160 segmented with the TARGETING range [0.0, 1.537345] (threshold 0.35), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 56 of 97 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
