# Evidence pack: phase-membrane (seed 13)

- world: `../../../../../../../../home/user/physim/research/alife/threads/autopoiesis/worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 21s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out collective/contrib/20261025T0721-c02-review-pm-damage/rerun/seed13 --seeds 13 --frames 160 --damage 120:0.5:rim --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5374], min area 6 px

## Measurements
- components: final 18, mean 14.7, max 24; occupancy final 0.34
- tracks: 154; persistent (alive >= 50% of run): 2; longest 101 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.12 (1 = constant size)
- enclosures: components with a hole mean 9.70, final 11; holes at thresholds 0.2/0.35/0.5 final [3, 11, 17]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [18, 18, 11]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0106/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 1000, default): splits 61, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 8, merge/split ratio 0.131, nucleations 0
- channel total drift (end/start - 1): [-0.5148, -0.6598, 0.1041, -0.0569]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 71 at frame 87: holes 1, rim-vs-core 0.19, rim-vs-outside 0.80, heterogeneity 0.17; core [0.067, 0.649, 0.373, 0.768] rim [0.144, 0.589, 0.483, 0.64]
  - track 87 at frame 89: holes 1, rim-vs-core 0.18, rim-vs-outside 0.87, heterogeneity 0.19; core [0.092, 0.792, 0.538, 0.59] rim [0.164, 0.63, 0.528, 0.613]
  - track 73 at frame 74: holes 1, rim-vs-core 0.30, rim-vs-outside 0.77, heterogeneity 0.20; core [0.108, 0.829, 0.619, 0.611] rim [0.204, 0.566, 0.505, 0.591]
  - track 138 at frame 148: holes 0, rim-vs-core 0.46, rim-vs-outside 0.93, heterogeneity 0.20; core [0.088, 0.813, 0.54, 0.539] rim [0.294, 0.451, 0.568, 0.721]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 85 components >= 12 px at frames [27, 54, 81, 106, 133, 160]; 5 components of the damaged lineage after the cut left out):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 13.1, rim/outside 0.838 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.465)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 4.95 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.735)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.77, rim/outside 3.99 (aggregate of 85 individuals; 76/85 membrane-like individually; rim level 0.575)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.5, rim/outside 4.05 (aggregate of 85 individuals; 75/85 membrane-like individually; rim level 0.619)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #71 (t=4350, R_eq 14.65): none; #87 (t=4450, R_eq 10.16, ring): ['L link', 'membrane (wall)']; #73 (t=3700, R_eq 9.15, ring): ['L link', 'membrane (wall)']; #138 (t=7400, R_eq 8.56): ['L link', 'membrane (wall)']
- damage `rim` (requested 0.50 of the area) at frame 120 (t=6000): target = main-run track #106; the individual is 1 component(s): outer component 674 px + 567 px it encloses (567 px of low-matter holes) = 1241 px = 4.32x the median individual, aspect 1.67 (rule fallback-largest: track age 34 frames vs K=20; 13 individuals from 13 components at that frame; open-ring individuals, not eligible: 0); mask 621 px (270 inside the individual)
- damage MEASURED: the target lost 22.7% of its matter (inside the individual: its components and what they enclose; 270 of 1241 px lost > half their matter); net matter lost outside it = 0.948% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (rim mode: the disk has the requested area but is centred on the individual's outer boundary, so about half of it lies outside the individual and cuts the layer at the edge)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[6000.0, 6400.0, 6800.0, 7200.0, 7600.0, 8000.0]: target [0.41, 0.811, 0.356, 0.413, 0.367, 0.371] (matter [0.585, 1.082, 1.031, 1.042, 1.277, 1.07]; pieces [1, 2, 3, 3, 3, 3]); comparator [1.0, 0.73, 0.223, 0.371, 0.427, 0.593] (matter [1.0, 1.256, 0.93, 1.287, 1.468, 1.88]; pieces [1, 2, 4, 5, 5, 5]). Follow-up: pre-cut field at frame 120, then recorded frames 120..160 segmented with the TARGETING range [0.0, 1.532707] (threshold 0.35), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 59 of 85 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- damage target is elongated (aspect 1.67 > 1.5; rule fallback-largest): it may be elongating or pinching (dividing) rather than a compact individual; check damage.png or damage at another frame
- damage target is NOT a mature compact individual (rule fallback-largest): no individual at frame 120 had a track >= K=20 frames, an area within [0.5, 1.6] x median and its centroid inside itself; damage later or lower --lineage-k

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
