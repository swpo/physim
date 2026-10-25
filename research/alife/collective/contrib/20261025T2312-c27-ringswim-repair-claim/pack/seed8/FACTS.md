# Evidence pack: ringswim-dl2 (seed 8)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 281 frames x 50 steps x dt 1.0 = time 14000; grid [256, 256]; wall 269s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27j/world.py --out collective/contrib/wip-c27j/pack --seeds 6 8 --frames 280 --damage 200:0.4:half --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5403], min area 6 px

## Measurements
- components: final 21, mean 32.9, max 95; occupancy final 0.20
- tracks: 1352; persistent (alive >= 50% of run): 0; longest 60 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 23.90, final 18; holes at thresholds 0.2/0.35/0.5 final [6, 22, 24]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 23, 21], H1 [29, 25, 17]
- motion: 84 long-lived tracks moved >= 1 body length; max speed 0.0599/time; max body lengths 4.6
- replication (lineage window K = 20 frames = time 1000, default): splits 452, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 364, merge/split ratio 0.805, nucleations 0
- channel total drift (end/start - 1): [-0.3327, -0.8095, -0.3072, -0.4375]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 143 at frame 33: holes 1, rim-vs-core 0.20, rim-vs-outside 0.82, heterogeneity 0.21; core [0.121, 0.747, 0.605, 0.614] rim [0.2, 0.575, 0.547, 0.602]
  - track 120 at frame 28: holes 1, rim-vs-core 0.18, rim-vs-outside 0.83, heterogeneity 0.21; core [0.107, 0.696, 0.566, 0.678] rim [0.206, 0.575, 0.546, 0.599]
  - track 603 at frame 125: holes 1, rim-vs-core 0.18, rim-vs-outside 0.74, heterogeneity 0.18; core [0.095, 0.61, 0.511, 0.759] rim [0.162, 0.528, 0.495, 0.616]
  - track 160 at frame 26: holes 1, rim-vs-core 0.26, rim-vs-outside 0.75, heterogeneity 0.20; core [0.12, 0.727, 0.601, 0.67] rim [0.217, 0.515, 0.507, 0.589]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 166 components >= 12 px at frames [47, 94, 141, 186, 233, 280]; 15 components of the damaged lineage after the cut left out):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 8.31, rim/outside 0.767 (aggregate of 166 individuals; 0/166 membrane-like individually; rim level 0.514)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 7.97 (aggregate of 166 individuals; 12/166 membrane-like individually; rim level 0.618)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 5.68 (aggregate of 166 individuals; 114/166 membrane-like individually; rim level 0.517)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.95, rim/outside 6.42 (aggregate of 166 individuals; 112/166 membrane-like individually; rim level 0.553)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #143 (t=1650, R_eq 11.13, ring): ['K catalyst', 'L link', 'membrane (wall)']; #120 (t=1400, R_eq 10.05, ring): ['L link', 'membrane (wall)']; #603 (t=6250, R_eq 12.27, ring): ['L link', 'membrane (wall)']; #160 (t=1300, R_eq 9.36, ring): ['L link', 'membrane (wall)']
- damage `half` (requested 0.40 of the area) at frame 200 (t=10000): target = main-run track #981; the individual is 1 component(s): outer component 371 px + 153 px it encloses (153 px of low-matter holes) = 524 px = 1.10x the median individual, aspect 1.09 (rule mature-compact: track age 22 frames vs K=20; 33 individuals from 33 components at that frame; open-ring individuals, not eligible: 1); mask 319 px (210 inside the individual)
- damage MEASURED: the target lost 41.9% of its matter (inside the individual: its components and what they enclose; 210 of 524 px lost > half their matter); net matter lost outside it = 2.3% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 109 of the 319 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[10000.0, 10800.0, 11600.0, 12400.0, 13200.0, 14000.0]: target [0.395, None, None, None, None, None] (matter [0.487, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; merged with another individual at t=[10450.0]; last seen t=10400); comparator [1.0, None, None, None, None, None] (matter [1.0, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; merged with another individual at t=[10200.0]; last seen t=10150). Follow-up: pre-cut field at frame 200, then recorded frames 200..280 segmented with the TARGETING range [0.0, 1.541732] (threshold 0.35), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 89 of 166 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
