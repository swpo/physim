# Evidence pack: neural-field-dep (seed 2)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: (c24 copy with a damage hook) c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 701 frames x 10 steps x dt 0.1 = time 700; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/comrep/world.py --out /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/comrep/core50 --seeds 2 3 --spf 10 --frames 700 --lineage-k 50 --damage 500:0.5:core --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 41, mean 42.1, max 75; occupancy final 0.10
- tracks: 727; persistent (alive >= 50% of run): 2; longest 541 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 41, 40], H1 [0, 0, 0]
- motion: 189 long-lived tracks moved >= 1 body length; max speed 0.605/time; max body lengths 54.3
- replication (lineage window K = 50 frames = time 50, --lineage-k): splits 285, persistent splits 43 (0 more failed only because the siblings re-merged within K), max generation 8, merges 87, merge/split ratio 0.305, nucleations 3
- channel total drift (end/start - 1): [-1.0, None, -0.5837, -0.1903]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 194 at frame 318: holes 0, rim-vs-core 0.31, rim-vs-outside 0.91, heterogeneity 0.16; core [0.904, 0.659, 1.0, 0.158] rim [0.726, 0.451, 0.941, 0.293]
  - track 144 at frame 247: holes 0, rim-vs-core 0.27, rim-vs-outside 0.83, heterogeneity 0.15; core [0.856, 0.53, 1.0, 0.144] rim [0.643, 0.456, 0.868, 0.225]
  - track 322 at frame 253: holes 0, rim-vs-core 0.27, rim-vs-outside 0.88, heterogeneity 0.16; core [0.902, 0.504, 1.0, 0.282] rim [0.656, 0.469, 0.891, 0.29]
  - track 603 at frame 624: holes 0, rim-vs-core 0.25, rim-vs-outside 0.86, heterogeneity 0.16; core [0.924, 0.595, 1.0, 0.376] rim [0.687, 0.526, 0.951, 0.409]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 245 components >= 12 px at frames [118, 235, 353, 465, 582, 700]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.797, rim/outside 3.1 (aggregate of 245 individuals; 0/245 membrane-like individually; rim level 0.718)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 1.95 (aggregate of 245 individuals; 7/245 membrane-like individually; rim level 0.549)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 33.8 (aggregate of 245 individuals; 2/245 membrane-like individually; rim level 0.843)
  - radial synaptic resource r: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.49, rim/outside 0.895 (aggregate of 245 individuals; 10/245 membrane-like individually; rim level 0.417)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #194 (t=318, R_eq 3.24): none; #144 (t=247, R_eq 2.65): none; #322 (t=253, R_eq 2.99): none; #603 (t=624, R_eq 3.48): none
- damage `core` (requested 0.50 of the area) at frame 500 (t=500): target = main-run track #504; the individual is one component of 18 px = 0.58x the median individual, aspect 1.21 (rule mature-compact: track age 76 frames vs K=50; 43 individuals from 43 components at that frame; open-ring individuals, not eligible: 2); mask 9 px (9 inside the individual)
- damage MEASURED: the target lost 54.6% of its matter (inside the individual: its components and what they enclose; 9 of 18 px lost > half their matter); net matter lost outside it = 0% of its matter; share of all matter that disappeared that was under labkit's mask 1
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[500.0, 540.0, 580.0, 620.0, 660.0, 700.0]: target [None, None, None, None, None, None] (matter [None, None, None, None, None, None]; pieces [0, 0, 0, 0, 0, 0]; not seen after the cut); comparator [1.0, None, None, None, None, None] (matter [1.0, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; last seen t=503). Follow-up: pre-cut field at frame 500, then recorded frames 500..700 segmented with the TARGETING range [0.0, 1.0] (threshold 0.5), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 245 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
