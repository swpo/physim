# Evidence pack: ringswim-dl2 (seed 12)

- world: `../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 286s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0135-c29-review-ringswim-repair/world.py --out collective/contrib/20261026T0135-c29-review-ringswim-repair/pack --seeds 12 --damage 200:0.4:half --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5387], min area 6 px

## Measurements
- components: final 35, mean 34.4, max 104; occupancy final 0.19
- tracks: 1056; persistent (alive >= 50% of run): 0; longest 62 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 24.17, final 25; holes at thresholds 0.2/0.35/0.5 final [5, 28, 32]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 37, 35], H1 [35, 32, 21]
- motion: 63 long-lived tracks moved >= 1 body length; max speed 0.0612/time; max body lengths 3.8
- replication (lineage window K = 20 frames = time 1000, default): splits 349, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 268, merge/split ratio 0.768, nucleations 1
- channel total drift (end/start - 1): [-0.3123, -0.8199, -0.3271, -0.4869]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 197 at frame 35: holes 1, rim-vs-core 0.20, rim-vs-outside 0.71, heterogeneity 0.16; core [0.086, 0.571, 0.46, 0.815] rim [0.152, 0.495, 0.471, 0.638]
  - track 43 at frame 30: holes 1, rim-vs-core 0.18, rim-vs-outside 0.78, heterogeneity 0.18; core [0.102, 0.65, 0.563, 0.734] rim [0.17, 0.543, 0.513, 0.621]
  - track 269 at frame 47: holes 1, rim-vs-core 0.35, rim-vs-outside 0.72, heterogeneity 0.23; core [0.141, 0.789, 0.666, 0.62] rim [0.267, 0.501, 0.524, 0.567]
  - track 219 at frame 34: holes 1, rim-vs-core 0.18, rim-vs-outside 0.83, heterogeneity 0.20; core [0.11, 0.733, 0.579, 0.609] rim [0.197, 0.576, 0.553, 0.613]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 195 components >= 12 px at frames [34, 67, 101, 133, 166, 200]; 1 components of the damaged lineage after the cut left out):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 9.75, rim/outside 0.767 (aggregate of 195 individuals; 0/195 membrane-like individually; rim level 0.504)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 7.44 (aggregate of 195 individuals; 21/195 membrane-like individually; rim level 0.623)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.6, rim/outside 5.47 (aggregate of 195 individuals; 144/195 membrane-like individually; rim level 0.528)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.12, rim/outside 6.21 (aggregate of 195 individuals; 141/195 membrane-like individually; rim level 0.56)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #197 (t=1750, R_eq 11.71, ring): ['L link', 'membrane (wall)']; #43 (t=1500, R_eq 11.08, ring): ['L link', 'membrane (wall)']; #269 (t=2350, R_eq 9.77, ring): ['L link', 'membrane (wall)']; #219 (t=1700, R_eq 10.54, ring): ['L link', 'membrane (wall)']
- damage `half` (requested 0.40 of the area) at frame 200 (t=10000): target = main-run track #1038, #936, #1037; the individual is 1 component(s): outer component 1735 px + 592 px it encloses (592 px of low-matter holes) = 2327 px = 5.98x the median individual, aspect 1.54 (rule fallback-largest: track age 1 frames vs K=20; 35 individuals from 35 components at that frame; open-ring individuals, not eligible: 0); mask 1830 px (931 inside the individual)
- damage MEASURED: the target lost 41% of its matter (inside the individual: its components and what they enclose; 931 of 2327 px lost > half their matter); net matter lost outside it = 3.03% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 899 of the 1830 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[10000.0]: target [0.557] (matter [0.569]; pieces [1]); comparator [1.0] (matter [1.0]; pieces [1]). Follow-up: pre-cut field at frame 200, then recorded frames 200..200 segmented with the TARGETING range [0.0, 1.538711] (threshold 0.35), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 120 of 195 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- damage target is elongated (aspect 1.54 > 1.5; rule fallback-largest): it may be elongating or pinching (dividing) rather than a compact individual; check damage.png or damage at another frame
- damage target is NOT a mature compact individual (rule fallback-largest): no individual at frame 200 had a track >= K=20 frames, an area within [0.5, 1.6] x median and its centroid inside itself; damage later or lower --lineage-k

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
