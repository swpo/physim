# Evidence pack: neural-field-dep (seed 14)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py`, family `neural-field`
- parent: None; mutation: (c24 copy with a damage hook) c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 701 frames x 10 steps x dt 0.1 = time 700; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py --out /tmp/claude-0/c28rev/core30 --seeds 11 12 13 14 --spf 10 --frames 700 --lineage-k 50 --damage 500:0.3:core --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 40, mean 43.2, max 71; occupancy final 0.09
- tracks: 710; persistent (alive >= 50% of run): 1; longest 374 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.81 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 40, 40], H1 [0, 0, 0]
- motion: 205 long-lived tracks moved >= 1 body length; max speed 0.616/time; max body lengths 33.8
- replication (lineage window K = 50 frames = time 50, --lineage-k): splits 281, persistent splits 57 (0 more failed only because the siblings re-merged within K), max generation 7, merges 86, merge/split ratio 0.306, nucleations 5
- channel total drift (end/start - 1): [-1.0, None, -0.6236, -0.1771]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 460 at frame 518: holes 0, rim-vs-core 0.29, rim-vs-outside 0.87, heterogeneity 0.17; core [0.912, 0.54, 1.0, 0.381] rim [0.669, 0.42, 0.908, 0.444]
  - track 494 at frame 541: holes 0, rim-vs-core 0.27, rim-vs-outside 0.85, heterogeneity 0.16; core [0.878, 0.476, 1.0, 0.201] rim [0.667, 0.409, 0.901, 0.317]
  - track 299 at frame 241: holes 0, rim-vs-core 0.24, rim-vs-outside 0.81, heterogeneity 0.15; core [0.923, 0.605, 1.0, 0.304] rim [0.711, 0.534, 0.944, 0.369]
  - track 619 at frame 594: holes 0, rim-vs-core 0.29, rim-vs-outside 0.85, heterogeneity 0.19; core [0.919, 0.607, 1.0, 0.439] rim [0.675, 0.527, 0.875, 0.508]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 239 components >= 12 px at frames [118, 235, 353, 465, 582, 700]; 5 components of the damaged lineage after the cut left out):
  - radial activity u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 3.05 (aggregate of 239 individuals; 0/239 membrane-like individually; rim level 0.713)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.898, rim/outside 2.03 (aggregate of 239 individuals; 6/239 membrane-like individually; rim level 0.565)
  - radial firing f(u): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.846, rim/outside 37.7 (aggregate of 239 individuals; 0/239 membrane-like individually; rim level 0.826)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.48, rim/outside 0.863 (aggregate of 239 individuals; 11/239 membrane-like individually; rim level 0.411)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #460 (t=518, R_eq 4.07): none; #494 (t=541, R_eq 3.66): none; #299 (t=241, R_eq 2.52): none; #619 (t=594, R_eq 3.66): none
- damage `core` (requested 0.30 of the area) at frame 500 (t=500): target = main-run track #519; the individual is one component of 26 px = 0.81x the median individual, aspect 1.19 (rule mature-compact: track age 76 frames vs K=50; 42 individuals from 42 components at that frame; open-ring individuals, not eligible: 1); mask 8 px (8 inside the individual)
- damage MEASURED: the target lost 32.4% of its matter (inside the individual: its components and what they enclose; 8 of 26 px lost > half their matter); net matter lost outside it = 0% of its matter; share of all matter that disappeared that was under labkit's mask 1
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[500.0, 540.0, 580.0, 620.0, 660.0, 700.0]: target [1.0, 1.615, 1.538, 1.615, 1.346, 1.077] (matter [0.676, 1.618, 1.568, 1.638, 1.345, 1.063]; pieces [1, 1, 1, 1, 1, 1]; merged with another individual at t=[659.0]); comparator [1.0, 1.708, 1.542, 1.542, 2.917, 3.167] (matter [1.0, 1.713, 1.521, 1.553, 2.945, 3.18]; pieces [1, 1, 1, 1, 1, 1]). Follow-up: pre-cut field at frame 500, then recorded frames 500..700 segmented with the TARGETING range [0.0, 1.0] (threshold 0.5), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
