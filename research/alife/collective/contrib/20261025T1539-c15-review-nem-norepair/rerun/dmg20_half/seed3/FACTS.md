# Evidence pack: active-nematic-droplets (seed 3)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 570s; status ok
- command: `python -m labkit.run /root/rev2/world.py --out /root/rev2/dmg20_half/seed3 --seeds 3 --damage 140:0.2:half --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8229, 0.6135], min area 6 px

## Measurements
- components: final 31, mean 19.4, max 33; occupancy final 0.07
- tracks: 106; persistent (alive >= 50% of run): 3; longest 135 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 31, 30], H1 [0, 0, 0]
- motion: 54 long-lived tracks moved >= 1 body length; max speed 0.0982/time; max body lengths 3.9
- replication (lineage window K = 20 frames = time 100, default): splits 45, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 4, merges 10, merge/split ratio 0.222, nucleations 6
- channel total drift (end/start - 1): [-0.5035, -0.4097, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 94: holes 0, rim-vs-core 0.54, rim-vs-outside 0.41, heterogeneity 0.18; core [0.975, 0.986, 0.426] rim [0.77, 0.767, 0.875]
  - track 14 at frame 89: holes 0, rim-vs-core 0.40, rim-vs-outside 0.39, heterogeneity 0.14; core [0.929, 0.948, 0.472] rim [0.751, 0.727, 0.757]
  - track 15 at frame 86: holes 0, rim-vs-core 0.37, rim-vs-outside 0.30, heterogeneity 0.13; core [0.898, 0.665, 0.558] rim [0.727, 0.479, 0.828]
  - track 64 at frame 163: holes 0, rim-vs-core 0.28, rim-vs-outside 0.41, heterogeneity 0.14; core [0.917, 0.764, 0.476] rim [0.789, 0.621, 0.673]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 131 components >= 12 px at frames [34, 67, 101, 134, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.804, rim/outside 4.63 (aggregate of 131 individuals; 0/131 membrane-like individually; rim level 0.748)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.749, rim/outside 8.03 (aggregate of 131 individuals; 1/131 membrane-like individually; rim level 0.628)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.53, rim/outside 2.13 (aggregate of 131 individuals; 90/131 membrane-like individually; rim level 0.653)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #7 (t=470, R_eq 3.61): ['surfactant s']; #14 (t=445, R_eq 4.03): none; #15 (t=430, R_eq 4.15): none; #64 (t=815, R_eq 3.52): none
- damage `half` (requested 0.20 of the area) at frame 140 (t=700): target = main-run track #27; the individual is one component of 26 px = 0.70x the median individual, aspect 1.56 (rule mature-compact: track age 65 frames vs K=20; 26 individuals from 26 components at that frame; open-ring individuals, not eligible: 0); mask 13 px (6 inside the individual)
- damage MEASURED: the target lost 103% of its matter (inside the individual: its components and what they enclose; 6 of 26 px lost > half their matter); net matter lost outside it = 84% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 7 of the 13 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[700.0, 760.0, 820.0, 880.0, 940.0, 1000.0]: target [0.692, None, None, None, None, None] (matter [0.783, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; last seen t=715); comparator [1.0, 1.04, 1.12, 1.16, 1.16, 1.2] (matter [1.0, 1.074, 1.119, 1.204, 1.24, 1.171]; pieces [1, 1, 1, 1, 1, 1]). Follow-up: pre-cut field at frame 140, then recorded frames 140..200 segmented with the TARGETING range [-0.822326, 0.610395] (threshold 0.574), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 131 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- damage target is elongated (aspect 1.56 > 1.5; rule mature-compact): it may be elongating or pinching (dividing) rather than a compact individual; check damage.png or damage at another frame

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
