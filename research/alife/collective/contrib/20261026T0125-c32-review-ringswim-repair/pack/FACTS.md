# Evidence pack: ringswim-dl2 (seed 12)

- world: `../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 261 frames x 50 steps x dt 1.0 = time 13000; grid [256, 256]; wall 265s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0125-c32-review-ringswim-repair/world.py --out collective/contrib/20261026T0125-c32-review-ringswim-repair/pack --seeds 12 --frames 260 --damage 200:0.4:half --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5386], min area 6 px

## Measurements
- components: final 33, mean 33.6, max 104; occupancy final 0.19
- tracks: 1296; persistent (alive >= 50% of run): 0; longest 62 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 24.12, final 23; holes at thresholds 0.2/0.35/0.5 final [8, 25, 32]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 34, 34], H1 [35, 33, 21]
- motion: 79 long-lived tracks moved >= 1 body length; max speed 0.0612/time; max body lengths 4.3
- replication (lineage window K = 20 frames = time 1000, default): splits 435, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 337, merge/split ratio 0.775, nucleations 1
- channel total drift (end/start - 1): [-0.3301, -0.8147, -0.3016, -0.485]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 197 at frame 37: holes 1, rim-vs-core 0.24, rim-vs-outside 0.66, heterogeneity 0.15; core [0.081, 0.548, 0.399, 0.823] rim [0.156, 0.463, 0.432, 0.614]
  - track 983 at frame 218: holes 0, rim-vs-core 0.37, rim-vs-outside 0.79, heterogeneity 0.19; core [0.105, 0.717, 0.529, 0.678] rim [0.308, 0.412, 0.559, 0.659]
  - track 43 at frame 31: holes 1, rim-vs-core 0.17, rim-vs-outside 0.77, heterogeneity 0.18; core [0.094, 0.616, 0.524, 0.753] rim [0.171, 0.545, 0.511, 0.619]
  - track 269 at frame 46: holes 1, rim-vs-core 0.34, rim-vs-outside 0.73, heterogeneity 0.23; core [0.138, 0.783, 0.656, 0.63] rim [0.265, 0.502, 0.523, 0.565]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 172 components >= 12 px at frames [44, 87, 131, 175, 216, 260]; 20 components of the damaged lineage after the cut left out):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 8.45, rim/outside 0.763 (aggregate of 172 individuals; 0/172 membrane-like individually; rim level 0.516)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 8.54 (aggregate of 172 individuals; 15/172 membrane-like individually; rim level 0.632)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 5.91 (aggregate of 172 individuals; 116/172 membrane-like individually; rim level 0.531)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.94, rim/outside 6.98 (aggregate of 172 individuals; 119/172 membrane-like individually; rim level 0.544)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #197 (t=1850, R_eq 10.17, ring): ['L link', 'membrane (wall)']; #983 (t=10900, R_eq 7.94): ['L link', 'membrane (wall)']; #43 (t=1550, R_eq 11.2, ring): ['L link', 'membrane (wall)']; #269 (t=2300, R_eq 9.49, ring): ['L link', 'membrane (wall)']
- damage `half` (requested 0.40 of the area) at frame 200 (t=10000): target = main-run track #1038, #936, #1037; the individual is 1 component(s): outer component 1735 px + 592 px it encloses (592 px of low-matter holes) = 2327 px = 5.98x the median individual, aspect 1.54 (rule fallback-largest: track age 1 frames vs K=20; 35 individuals from 35 components at that frame; open-ring individuals, not eligible: 0); mask 1830 px (931 inside the individual)
- damage MEASURED: the target lost 41% of its matter (inside the individual: its components and what they enclose; 931 of 2327 px lost > half their matter); net matter lost outside it = 3.03% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 899 of the 1830 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[10000.0, 10600.0, 11200.0, 11800.0, 12400.0, 13000.0]: target [0.557, 0.357, 0.15, None, None, None] (matter [0.569, 0.382, 0.16, None, None, None]; pieces [1, 1, 1, 0, 0, 0]; merged with another individual at t=[10500.0, 10950.0, 11450.0]; last seen t=11400); comparator [1.0, None, None, None, None, None] (matter [1.0, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; merged with another individual at t=[10400.0]; last seen t=10350). Follow-up: pre-cut field at frame 200, then recorded frames 200..260 segmented with the TARGETING range [0.0, 1.538711] (threshold 0.35), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 93 of 172 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- damage target is elongated (aspect 1.54 > 1.5; rule fallback-largest): it may be elongating or pinching (dividing) rather than a compact individual; check damage.png or damage at another frame
- damage target is NOT a mature compact individual (rule fallback-largest): no individual at frame 200 had a track >= K=20 frames, an area within [0.5, 1.6] x median and its centroid inside itself; damage later or lower --lineage-k

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
