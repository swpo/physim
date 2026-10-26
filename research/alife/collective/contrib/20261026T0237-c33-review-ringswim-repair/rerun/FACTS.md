# Evidence pack: ringswim-dl2 (seed 21)

- world: `../../20261025T2312-c27-ringswim-repair-claim/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 281 frames x 50 steps x dt 1.0 = time 14000; grid [256, 256]; wall 381s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2312-c27-ringswim-repair-claim/world.py --out collective/contrib/20261026T0330-c33-review-ringswim-repair/rerun --seeds 21 --frames 280 --damage 200:0.4:half --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5396], min area 6 px

## Measurements
- components: final 24, mean 36.3, max 91; occupancy final 0.17
- tracks: 1383; persistent (alive >= 50% of run): 0; longest 83 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 26.14, final 20; holes at thresholds 0.2/0.35/0.5 final [8, 21, 25]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 25, 24], H1 [26, 25, 19]
- motion: 95 long-lived tracks moved >= 1 body length; max speed 0.0531/time; max body lengths 4.0
- replication (lineage window K = 20 frames = time 1000, default): splits 460, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 373, merge/split ratio 0.811, nucleations 1
- channel total drift (end/start - 1): [-0.3152, -0.8255, -0.3402, -0.4989]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 244 at frame 54: holes 1, rim-vs-core 0.17, rim-vs-outside 0.75, heterogeneity 0.18; core [0.093, 0.605, 0.504, 0.749] rim [0.171, 0.543, 0.517, 0.616]
  - track 180 at frame 38: holes 0, rim-vs-core 0.35, rim-vs-outside 0.47, heterogeneity 0.16; core [0.139, 0.595, 0.527, 0.777] rim [0.248, 0.413, 0.507, 0.504]
  - track 193 at frame 38: holes 0, rim-vs-core 0.32, rim-vs-outside 0.64, heterogeneity 0.15; core [0.106, 0.62, 0.48, 0.818] rim [0.252, 0.428, 0.533, 0.62]
  - track 1288 at frame 264: holes 0, rim-vs-core 0.64, rim-vs-outside 0.60, heterogeneity 0.18; core [0.217, 0.794, 0.83, 0.83] rim [0.378, 0.314, 0.536, 0.575]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 174 components >= 12 px at frames [47, 94, 141, 186, 233, 280]; 26 components of the damaged lineage after the cut left out):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 12.3, rim/outside 0.763 (aggregate of 174 individuals; 0/174 membrane-like individually; rim level 0.519)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 8.97 (aggregate of 174 individuals; 18/174 membrane-like individually; rim level 0.653)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.67, rim/outside 6.68 (aggregate of 174 individuals; 141/174 membrane-like individually; rim level 0.559)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.61, rim/outside 7.61 (aggregate of 174 individuals; 138/174 membrane-like individually; rim level 0.587)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #244 (t=2700, R_eq 11.99, ring): ['L link', 'membrane (wall)']; #180 (t=1900, R_eq 8.16): none; #193 (t=1900, R_eq 7.74): ['L link']; #1288 (t=13200, R_eq 5.08, DAMAGED): ['membrane (wall)']
- damage `half` (requested 0.40 of the area) at frame 200 (t=10000): target = main-run track #997, #980; the individual is 1 component(s): outer component 919 px + 264 px it encloses (264 px of low-matter holes) = 1183 px = 3.26x the median individual, aspect 2.44 (rule fallback-largest: track age 1 frames vs K=20; 34 individuals from 34 components at that frame; open-ring individuals, not eligible: 2); mask 804 px (473 inside the individual)
- damage MEASURED: the target lost 39% of its matter (inside the individual: its components and what they enclose; 473 of 1183 px lost > half their matter); net matter lost outside it = 2.77% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 331 of the 804 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[10000.0, 10800.0, 11600.0, 12400.0, 13200.0, 14000.0]: target [0.592, None, None, None, None, None] (matter [0.604, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; merged with another individual at t=[10050.0, 10650.0]; re-nucleated pieces picked up at t=[10050.0]; last seen t=10600); comparator [1.0, None, None, None, None, None] (matter [1.0, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; merged with another individual at t=[10300.0]; last seen t=10250). Follow-up: pre-cut field at frame 200, then recorded frames 200..280 segmented with the TARGETING range [0.0, 1.540489] (threshold 0.35), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 113 of 174 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- damage target is elongated (aspect 2.44 > 1.5; rule fallback-largest): it may be elongating or pinching (dividing) rather than a compact individual; check damage.png or damage at another frame
- damage target is NOT a mature compact individual (rule fallback-largest): no individual at frame 200 had a track >= K=20 frames, an area within [0.5, 1.6] x median and its centroid inside itself; damage later or lower --lineage-k

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
