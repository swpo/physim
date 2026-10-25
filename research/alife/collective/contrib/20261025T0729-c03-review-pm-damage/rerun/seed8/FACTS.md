# Evidence pack: phase-membrane (seed 8)

- world: `../../../../../../../../home/user/physim/research/alife/threads/autopoiesis/worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 12s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/dmg/seed8 --seeds 8 --frames 160 --damage 120:0.5:rim --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5419], min area 6 px

## Measurements
- components: final 23, mean 16.2, max 24; occupancy final 0.32
- tracks: 152; persistent (alive >= 50% of run): 5; longest 149 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.38 (1 = constant size)
- enclosures: components with a hole mean 9.75, final 6; holes at thresholds 0.2/0.35/0.5 final [0, 6, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 23, 23], H1 [17, 15, 5]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0109/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 1000, default): splits 61, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 3, merges 6, merge/split ratio 0.098, nucleations 0
- channel total drift (end/start - 1): [-0.5004, -0.7165, 0.0988, -0.0574]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 42 at frame 77: holes 1, rim-vs-core 0.19, rim-vs-outside 0.78, heterogeneity 0.19; core [0.099, 0.783, 0.56, 0.615] rim [0.162, 0.614, 0.511, 0.601]
  - track 28 at frame 59: holes 1, rim-vs-core 0.16, rim-vs-outside 0.80, heterogeneity 0.20; core [0.102, 0.747, 0.563, 0.677] rim [0.167, 0.63, 0.524, 0.598]
  - track 77 at frame 101: holes 1, rim-vs-core 0.19, rim-vs-outside 0.78, heterogeneity 0.17; core [0.072, 0.671, 0.406, 0.691] rim [0.167, 0.544, 0.483, 0.634]
  - track 128 at frame 145: holes 1, rim-vs-core 0.42, rim-vs-outside 0.88, heterogeneity 0.24; core [0.112, 0.922, 0.657, 0.482] rim [0.257, 0.565, 0.541, 0.612]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 102 components >= 12 px at frames [27, 54, 81, 106, 133, 160]; 3 components of the damaged lineage after the cut left out):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 9.41, rim/outside 0.852 (aggregate of 102 individuals; 0/102 membrane-like individually; rim level 0.471)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1, rim/outside 6.05 (aggregate of 102 individuals; 0/102 membrane-like individually; rim level 0.722)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.64, rim/outside 4.66 (aggregate of 102 individuals; 80/102 membrane-like individually; rim level 0.597)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.1, rim/outside 4.79 (aggregate of 102 individuals; 77/102 membrane-like individually; rim level 0.643)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #42 (t=3850, R_eq 12.53, ring): ['L link', 'membrane (wall)']; #28 (t=2950, R_eq 11.66, ring): ['L link', 'membrane (wall)']; #77 (t=5050, R_eq 10.31, ring): ['L link', 'membrane (wall)']; #128 (t=7250, R_eq 8.37, ring): ['L link', 'membrane (wall)']
- damage `rim` (requested 0.50 of the area) at frame 120 (t=6000): target = main-run track #93; the individual is 1 component(s): outer component 383 px + 102 px it encloses (102 px of low-matter holes) = 485 px = 1.11x the median individual, aspect 1.12 (rule mature-compact: track age 46 frames vs K=20; 15 individuals from 15 components at that frame; open-ring individuals, not eligible: 1); mask 241 px (109 inside the individual)
- damage MEASURED: the target lost 24% of its matter (inside the individual: its components and what they enclose; 109 of 485 px lost > half their matter); net matter lost outside it = 1.15% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (rim mode: the disk has the requested area but is centred on the individual's outer boundary, so about half of it lies outside the individual and cuts the layer at the edge)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[6000.0, 6400.0, 6800.0, 7200.0, 7600.0, 8000.0]: target [0.581, 0.303, 0.608, 1.291, 1.619, 0.388] (matter [0.667, 0.389, 0.647, 1.143, 1.424, 0.91]; pieces [1, 1, 1, 1, 1, 2]); comparator [1.0, 0.542, None, None, None, None] (matter [1.0, 0.66, None, None, None, None]; pieces [1, 1, 0, 0, 0, 0]; last seen t=6500). Follow-up: pre-cut field at frame 120, then recorded frames 120..160 segmented with the TARGETING range [0.0, 1.539989] (threshold 0.35), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 49 of 102 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
