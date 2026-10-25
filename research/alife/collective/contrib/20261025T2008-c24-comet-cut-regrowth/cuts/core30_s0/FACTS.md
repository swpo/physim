# Evidence pack: neural-field-dep (seed 0)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: (c24 copy with a damage hook) c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/comrep/world.py --out /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/comrep/core --seeds 0 1 --spf 50 --damage 100:0.3:core --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 37, mean 37.2, max 69; occupancy final 0.10
- tracks: 608; persistent (alive >= 50% of run): 2; longest 106 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.18 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 38, 38], H1 [0, 0, 0]
- motion: 123 long-lived tracks moved >= 1 body length; max speed 0.6/time; max body lengths 45.7
- replication (lineage window K = 20 frames = time 100, default): splits 238, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 5, merges 60, merge/split ratio 0.252, nucleations 11
- channel total drift (end/start - 1): [-1.0, None, -0.5646, -0.1891]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 433 at frame 148: holes 0, rim-vs-core 0.26, rim-vs-outside 0.85, heterogeneity 0.15; core [0.847, 0.576, 1.0, 0.109] rim [0.661, 0.472, 0.872, 0.2]
  - track 440 at frame 145: holes 0, rim-vs-core 0.28, rim-vs-outside 0.85, heterogeneity 0.17; core [0.924, 0.595, 1.0, 0.433] rim [0.681, 0.491, 0.914, 0.49]
  - track 453 at frame 151: holes 0, rim-vs-core 0.23, rim-vs-outside 0.90, heterogeneity 0.17; core [0.908, 0.383, 1.0, 0.438] rim [0.692, 0.406, 0.927, 0.414]
  - track 574 at frame 187: holes 0, rim-vs-core 0.23, rim-vs-outside 0.89, heterogeneity 0.16; core [0.882, 0.621, 1.0, 0.151] rim [0.75, 0.477, 0.944, 0.253]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 207 components >= 12 px at frames [34, 67, 100, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.787, rim/outside 2.9 (aggregate of 207 individuals; 0/207 membrane-like individually; rim level 0.698)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 1.91 (aggregate of 207 individuals; 6/207 membrane-like individually; rim level 0.532)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.84, rim/outside 24.2 (aggregate of 207 individuals; 2/207 membrane-like individually; rim level 0.792)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.44, rim/outside 0.881 (aggregate of 207 individuals; 12/207 membrane-like individually; rim level 0.415)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #433 (t=740, R_eq 2.33): none; #440 (t=725, R_eq 3.74): none; #453 (t=755, R_eq 4.72): none; #574 (t=935, R_eq 3.14): none
- damage `core` (requested 0.30 of the area) at frame 100 (t=500): target = main-run track #400; the individual is one component of 33 px = 0.92x the median individual, aspect 1.57 (rule mature-compact: track age 29 frames vs K=20; 28 individuals from 28 components at that frame; open-ring individuals, not eligible: 1); mask 12 px (12 inside the individual)
- damage MEASURED: the target lost 37.9% of its matter (inside the individual: its components and what they enclose; 12 of 33 px lost > half their matter); net matter lost outside it = 0% of its matter; share of all matter that disappeared that was under labkit's mask 1
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[500.0, 600.0, 700.0, 800.0, 900.0, 1000.0]: target [0.303, 2.0, None, None, None, None] (matter [0.562, 2.009, None, None, None, None]; pieces [2, 1, 0, 0, 0, 0]; last seen t=660); comparator [1.0, 1.865, 1.351, 1.081, 1.703, 1.108] (matter [1.0, 3.556, 5.235, 2.613, 3.539, 1.936]; pieces [1, 2, 5, 3, 3, 2]; merged with another individual at t=[680.0, 715.0, 760.0, 905.0]). Follow-up: pre-cut field at frame 100, then recorded frames 100..200 segmented with the TARGETING range [0.0, 1.0] (threshold 0.5), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 207 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- damage target is elongated (aspect 1.57 > 1.5; rule mature-compact): it may be elongating or pinching (dividing) rather than a compact individual; check damage.png or damage at another frame

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
