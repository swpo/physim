# Evidence pack: phase-membrane (seed 16)

- world: `../../../../../../../../home/user/physim/research/alife/threads/autopoiesis/worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 21s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out collective/contrib/20261025T0721-c02-review-pm-damage/rerun/seed16 --seeds 16 --frames 160 --damage 120:0.5:rim --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5465], min area 6 px

## Measurements
- components: final 19, mean 18.0, max 23; occupancy final 0.35
- tracks: 149; persistent (alive >= 50% of run): 3; longest 96 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.22 (1 = constant size)
- enclosures: components with a hole mean 10.11, final 13; holes at thresholds 0.2/0.35/0.5 final [2, 13, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 19, 19], H1 [17, 17, 10]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00466/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 1000, default): splits 57, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 3, merges 8, merge/split ratio 0.14, nucleations 0
- channel total drift (end/start - 1): [-0.5458, -0.6607, 0.1756, 0.0874]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 64 at frame 75: holes 0, rim-vs-core 0.86, rim-vs-outside 0.54, heterogeneity 0.24; core [0.298, 0.884, 0.943, 0.784] rim [0.478, 0.245, 0.431, 0.574]
  - track 56 at frame 56: holes 0, rim-vs-core 0.64, rim-vs-outside 0.45, heterogeneity 0.17; core [0.197, 0.742, 0.717, 0.848] rim [0.351, 0.315, 0.499, 0.453]
  - track 80 at frame 98: holes 0, rim-vs-core 0.42, rim-vs-outside 0.84, heterogeneity 0.20; core [0.103, 0.818, 0.565, 0.599] rim [0.303, 0.456, 0.564, 0.695]
  - track 125 at frame 140: holes 1, rim-vs-core 0.33, rim-vs-outside 0.81, heterogeneity 0.21; core [0.115, 0.822, 0.615, 0.578] rim [0.239, 0.539, 0.518, 0.604]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 111 components >= 12 px at frames [27, 54, 81, 106, 133, 160]; 3 components of the damaged lineage after the cut left out):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 11.7, rim/outside 0.887 (aggregate of 111 individuals; 0/111 membrane-like individually; rim level 0.475)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 5.37 (aggregate of 111 individuals; 0/111 membrane-like individually; rim level 0.732)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.73, rim/outside 4.42 (aggregate of 111 individuals; 93/111 membrane-like individually; rim level 0.607)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.66, rim/outside 4.26 (aggregate of 111 individuals; 94/111 membrane-like individually; rim level 0.68)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #64 (t=3750, R_eq 4.51): ['membrane (wall)']; #56 (t=2800, R_eq 5.89): none; #80 (t=4900, R_eq 7.69): ['L link', 'membrane (wall)']; #125 (t=7000, R_eq 8.92, ring): ['L link', 'membrane (wall)']
- damage `rim` (requested 0.50 of the area) at frame 120 (t=6000): target = main-run track #100; the individual is one component of 133 px = 0.67x the median individual, aspect 1.02 (rule mature-compact: track age 28 frames vs K=20; 21 individuals from 21 components at that frame; open-ring individuals, not eligible: 0); mask 69 px (37 inside the individual)
- damage MEASURED: the target lost 28.8% of its matter (inside the individual: its components and what they enclose; 37 of 133 px lost > half their matter); net matter lost outside it = 1.91% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (rim mode: the disk has the requested area but is centred on the individual's outer boundary, so about half of it lies outside the individual and cuts the layer at the edge)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[6000.0, 6400.0, 6800.0, 7200.0, 7600.0, 8000.0]: target [0.677, None, None, None, None, None] (matter [0.686, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; merged with another individual at t=[6200.0]; last seen t=6150); comparator [1.0, 1.547, 2.0, 1.925, 2.008, 0.587] (matter [1.0, 1.42, 1.771, 1.783, 1.931, 0.982]; pieces [1, 1, 1, 1, 1, 2]). Follow-up: pre-cut field at frame 120, then recorded frames 120..160 segmented with the TARGETING range [0.0, 1.547817] (threshold 0.35), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 61 of 111 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
