# Evidence pack: neural-field-dep (seed 1)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: (c24 copy with a damage hook) c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/comrep/world.py --out /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/comrep/core --seeds 0 1 --spf 50 --damage 100:0.3:core --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 50, mean 42.5, max 70; occupancy final 0.10
- tracks: 779; persistent (alive >= 50% of run): 1; longest 106 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.31 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [50, 50, 50], H1 [0, 0, 0]
- motion: 132 long-lived tracks moved >= 1 body length; max speed 0.577/time; max body lengths 38.2
- replication (lineage window K = 20 frames = time 100, default): splits 311, persistent splits 34 (0 more failed only because the siblings re-merged within K), max generation 7, merges 79, merge/split ratio 0.254, nucleations 9
- channel total drift (end/start - 1): [1.0, None, -0.4682, -0.2006]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 365 at frame 103: holes 0, rim-vs-core 0.22, rim-vs-outside 0.80, heterogeneity 0.15; core [0.948, 0.528, 1.0, 0.286] rim [0.748, 0.453, 0.968, 0.345]
  - track 516 at frame 134: holes 0, rim-vs-core 0.27, rim-vs-outside 0.89, heterogeneity 0.17; core [0.924, 0.513, 1.0, 0.27] rim [0.69, 0.437, 0.937, 0.352]
  - track 527 at frame 138: holes 0, rim-vs-core 0.27, rim-vs-outside 0.90, heterogeneity 0.17; core [0.937, 0.577, 1.0, 0.404] rim [0.687, 0.495, 0.94, 0.407]
  - track 705 at frame 187: holes 0, rim-vs-core 0.32, rim-vs-outside 0.85, heterogeneity 0.16; core [0.903, 0.585, 1.0, 0.277] rim [0.667, 0.436, 0.917, 0.413]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 232 components >= 12 px at frames [34, 67, 100, 133, 166, 200]; 9 components of the damaged lineage after the cut left out):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 3.01 (aggregate of 232 individuals; 0/232 membrane-like individually; rim level 0.714)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.886, rim/outside 1.98 (aggregate of 232 individuals; 9/232 membrane-like individually; rim level 0.557)
  - radial firing f(u): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.859, rim/outside 34.2 (aggregate of 232 individuals; 0/232 membrane-like individually; rim level 0.836)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.5, rim/outside 0.867 (aggregate of 232 individuals; 8/232 membrane-like individually; rim level 0.411)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #365 (t=515, R_eq 3.24): none; #516 (t=670, R_eq 3.04): none; #527 (t=690, R_eq 3.57): none; #705 (t=935, R_eq 3.48): none
- damage `core` (requested 0.30 of the area) at frame 100 (t=500): target = main-run track #423; the individual is one component of 30 px = 0.80x the median individual, aspect 1.37 (rule mature-compact: track age 33 frames vs K=20; 36 individuals from 36 components at that frame; open-ring individuals, not eligible: 0); mask 8 px (8 inside the individual)
- damage MEASURED: the target lost 28.8% of its matter (inside the individual: its components and what they enclose; 8 of 30 px lost > half their matter); net matter lost outside it = 0% of its matter; share of all matter that disappeared that was under labkit's mask 1
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[500.0, 600.0, 700.0, 800.0, 900.0, 1000.0]: target [1.0, 1.967, 1.0, 1.267, 2.8, 1.2] (matter [0.712, 2.986, 1.043, 1.332, 4.491, 2.136]; pieces [1, 2, 1, 1, 2, 2]; merged with another individual at t=[660.0]); comparator [1.0, 1.379, 1.517, 0.793, 0.897, 1.172] (matter [1.0, 2.396, 1.485, 0.752, 1.72, 3.191]; pieces [1, 2, 1, 1, 2, 3]; merged with another individual at t=[615.0]). Follow-up: pre-cut field at frame 100, then recorded frames 100..200 segmented with the TARGETING range [0.0, 1.0] (threshold 0.5), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 232 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
