# Evidence pack: active-nematic-droplets (seed 6)

- world: `../../../20261025T1250-c11-active-nematic-no-repair/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 452s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1250-c11-active-nematic-no-repair/world.py --out collective/contrib/20261025T1523-c16-review-nematic-norepair/dmg20_core/seed6 --seeds 6 --damage 120:0.2:core --no-movie`
- segmentation: matter > 0.57 of robust range [-0.823, 0.6156], min area 6 px

## Measurements
- components: final 31, mean 17.0, max 31; occupancy final 0.06
- tracks: 91; persistent (alive >= 50% of run): 3; longest 110 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.56 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 31, 30], H1 [0, 0, 0]
- motion: 41 long-lived tracks moved >= 1 body length; max speed 0.0837/time; max body lengths 4.6
- replication (lineage window K = 20 frames = time 100, default): splits 37, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 5, merges 9, merge/split ratio 0.243, nucleations 7
- channel total drift (end/start - 1): [-0.4995, -0.4232, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 27 at frame 129: holes 0, rim-vs-core 0.52, rim-vs-outside 0.39, heterogeneity 0.17; core [0.962, 0.991, 0.441] rim [0.738, 0.758, 0.844]
  - track 37 at frame 150: holes 0, rim-vs-core 0.54, rim-vs-outside 0.36, heterogeneity 0.18; core [0.956, 0.942, 0.424] rim [0.736, 0.637, 0.812]
  - track 39 at frame 150: holes 0, rim-vs-core 0.43, rim-vs-outside 0.31, heterogeneity 0.15; core [0.915, 0.803, 0.493] rim [0.731, 0.548, 0.781]
  - track 74 at frame 187: holes 0, rim-vs-core 0.50, rim-vs-outside 0.39, heterogeneity 0.17; core [0.958, 0.942, 0.411] rim [0.751, 0.642, 0.754]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 118 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.818, rim/outside 4.7 (aggregate of 118 individuals; 0/118 membrane-like individually; rim level 0.755)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.765, rim/outside 7.85 (aggregate of 118 individuals; 1/118 membrane-like individually; rim level 0.631)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.47, rim/outside 2.15 (aggregate of 118 individuals; 81/118 membrane-like individually; rim level 0.659)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #27 (t=645, R_eq 4.26): ['surfactant s']; #37 (t=750, R_eq 3.29): ['surfactant s']; #39 (t=750, R_eq 3.57): none; #74 (t=935, R_eq 3.24): ['surfactant s']
- damage `core` (requested 0.20 of the area) at frame 120 (t=600): target = main-run track #23; the individual is one component of 22 px = 0.63x the median individual, aspect 1.58 (rule mature-compact: track age 50 frames vs K=20; 22 individuals from 22 components at that frame; open-ring individuals, not eligible: 0); mask 4 px (4 inside the individual)
- damage MEASURED: the target lost 94.2% of its matter (inside the individual: its components and what they enclose; 4 of 22 px lost > half their matter); net matter lost outside it = 0% of its matter; share of all matter that disappeared that was under labkit's mask 1
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[600.0, 680.0, 760.0, 840.0, 920.0, 1000.0]: target [0.955, None, None, None, None, None] (matter [0.054, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; last seen t=610); comparator [1.0, None, None, None, None, None] (matter [1.0, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; last seen t=670). Follow-up: pre-cut field at frame 120, then recorded frames 120..200 segmented with the TARGETING range [-0.81983, 0.603741] (threshold 0.5759), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- radial: 1 of 118 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- damage target is elongated (aspect 1.58 > 1.5; rule mature-compact): it may be elongating or pinching (dividing) rather than a compact individual; check damage.png or damage at another frame

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
