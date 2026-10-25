# Evidence pack: active-nematic-droplets (seed 4)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 570s; status ok
- command: `python -m labkit.run /root/rev2/world.py --out /root/rev2/dmg20_core/seed4 --seeds 4 --damage 140:0.2:core --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8258, 0.6294], min area 6 px

## Measurements
- components: final 29, mean 21.9, max 31; occupancy final 0.07
- tracks: 101; persistent (alive >= 50% of run): 11; longest 176 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.78 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 29, 29], H1 [1, 0, 0]
- motion: 45 long-lived tracks moved >= 1 body length; max speed 0.128/time; max body lengths 4.3
- replication (lineage window K = 20 frames = time 100, default): splits 38, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 4, merges 14, merge/split ratio 0.368, nucleations 11
- channel total drift (end/start - 1): [-0.5085, -0.3858, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 114: holes 0, rim-vs-core 0.46, rim-vs-outside 0.31, heterogeneity 0.14; core [0.94, 0.766, 0.482] rim [0.752, 0.526, 0.831]
  - track 28 at frame 118: holes 0, rim-vs-core 0.50, rim-vs-outside 0.38, heterogeneity 0.17; core [0.956, 0.936, 0.396] rim [0.76, 0.665, 0.763]
  - track 43 at frame 133: holes 0, rim-vs-core 0.52, rim-vs-outside 0.34, heterogeneity 0.18; core [0.938, 0.881, 0.444] rim [0.722, 0.578, 0.807]
  - track 87 at frame 185: holes 0, rim-vs-core 0.49, rim-vs-outside 0.37, heterogeneity 0.17; core [0.94, 0.92, 0.421] rim [0.733, 0.641, 0.769]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 147 components >= 12 px at frames [34, 67, 101, 134, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 4.8 (aggregate of 147 individuals; 0/147 membrane-like individually; rim level 0.755)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.756, rim/outside 8.09 (aggregate of 147 individuals; 0/147 membrane-like individually; rim level 0.62)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.58, rim/outside 2.15 (aggregate of 147 individuals; 110/147 membrane-like individually; rim level 0.644)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #11 (t=570, R_eq 2.52): ['surfactant s']; #28 (t=590, R_eq 3.24): ['surfactant s']; #43 (t=665, R_eq 3.14): ['surfactant s']; #87 (t=925, R_eq 3.29): ['surfactant s']
- damage `core` (requested 0.20 of the area) at frame 140 (t=700): target = main-run track #49; the individual is one component of 23 px = 0.68x the median individual, aspect 1.5 (rule mature-compact: track age 69 frames vs K=20; 27 individuals from 27 components at that frame; open-ring individuals, not eligible: 0); mask 5 px (5 inside the individual)
- damage MEASURED: the target lost 109% of its matter (inside the individual: its components and what they enclose; 5 of 23 px lost > half their matter); net matter lost outside it = 0% of its matter; share of all matter that disappeared that was under labkit's mask 1
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[700.0, 760.0, 820.0, 880.0, 940.0, 1000.0]: target [0.348, None, None, None, None, None] (matter [0.608, None, None, None, None, None]; pieces [2, 0, 0, 0, 0, 0]; last seen t=715); comparator [1.0, 1.074, 1.074, 1.0, 0.963, None] (matter [1.0, 1.293, 1.197, 1.014, 1.101, None]; pieces [1, 1, 1, 1, 1, 0]; merged with another individual at t=[975.0]; last seen t=970). Follow-up: pre-cut field at frame 140, then recorded frames 140..200 segmented with the TARGETING range [-0.824056, 0.646051] (threshold 0.5605), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 147 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- damage target is elongated (aspect 1.50 > 1.5; rule mature-compact): it may be elongating or pinching (dividing) rather than a compact individual; check damage.png or damage at another frame

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
