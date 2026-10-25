# Evidence pack: fch-protocell (seed 0)

- world: `../../world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0745-c03-fch-vesicles/world.py; mutation: add a solute made by the bilayer, excluded from it by chi c u (barrier), decaying everywhere
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 199s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0726-c03-fch-protocell/world.py --out collective/contrib/20261025T0726-c03-fch-protocell/pack_damage/seed0 --seeds 0 --frames 100 --damage 40:0.3:rim --no-movie`
- segmentation: matter > 0.23 of robust range [0.1078, 1.835], min area 6 px

## Measurements
- components: final 6, mean 6.0, max 6; occupancy final 0.16
- tracks: 10; persistent (alive >= 50% of run): 6; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 43.89 (1 = constant size)
- enclosures: components with a hole mean 2.47, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 1, 5]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 6], H1 [6, 6, 5]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 160, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 5
- channel total drift (end/start - 1): [-0.0148, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 50: holes 1, rim-vs-core 0.44, rim-vs-outside 0.38, heterogeneity 0.26; core [0.879, 0.015] rim [0.457, 0.131]
  - track 5 at frame 51: holes 1, rim-vs-core 0.43, rim-vs-outside 0.39, heterogeneity 0.25; core [0.882, 0.013] rim [0.471, 0.13]
  - track 6 at frame 51: holes 0, rim-vs-core 0.13, rim-vs-outside 0.56, heterogeneity 0.13; core [0.745, 0.066] rim [0.623, 0.03]
  - track 7 at frame 51: holes 1, rim-vs-core 0.45, rim-vs-outside 0.38, heterogeneity 0.25; core [0.89, 0.008] rim [0.461, 0.129]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 32 components >= 12 px at frames [17, 33, 50, 67, 83, 100]; 4 components of the damaged lineage after the cut left out):
  - radial amphiphile u (u + 1.6): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 2.42, rim/outside 81 (aggregate of 32 individuals; 26/32 membrane-like individually; rim level 0.929)  MEMBRANE-LIKE
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.14, rim/outside 0.893 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.0754)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): amphiphile u (u + 1.6)
- membrane-like channels per top track at mid-life: #3 (t=400, R_eq 10.34, ring): ['amphiphile u (u + 1.6)']; #5 (t=408, R_eq 10.22, ring): ['amphiphile u (u + 1.6)']; #6 (t=408, R_eq 16.97): none; #7 (t=408, R_eq 10.49, ring): ['amphiphile u (u + 1.6)']
- damage `rim` (requested 0.30 of the area) at frame 40 (t=320): target = main-run track #9; the individual is 1 component(s): outer component 380 px + 16 px it encloses (16 px of low-matter holes) = 396 px = 1.02x the median individual, aspect 1 (rule mature-compact: track age 40 frames vs K=20; 6 individuals from 6 components at that frame; open-ring individuals, not eligible: 0); mask 121 px (58 inside the individual)
- damage MEASURED: the target lost 14.8% of its matter (inside the individual: its components and what they enclose; 58 of 396 px lost > half their matter); net matter lost outside it = 1.2% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (rim mode: the disk has the requested area but is centred on the individual's outer boundary, so about half of it lies outside the individual and cuts the layer at the edge)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[320.0, 416.0, 512.0, 608.0, 704.0, 800.0]: target [0.869, 0.803, 0.795, 0.77, 0.745, 0.722] (matter [0.838, 0.834, 0.826, 0.801, 0.772, 0.744]; pieces [1, 1, 1, 1, 1, 1]); comparator [1.0, 0.894, 0.799, 0.742, 0.698, 0.671] (matter [1.0, 0.904, 0.821, 0.766, 0.725, 0.697]; pieces [1, 1, 1, 1, 1, 1]). Follow-up: pre-cut field at frame 40, then recorded frames 40..100 segmented with the TARGETING range [0.109162, 1.839154] (threshold 0.2259), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- radial: 14 of 32 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
