# Evidence pack: active-nematic-droplets (seed 0)

- world: `../../world6.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 499s; status ok
- command: `python -m labkit.run /tmp/claude-0/c11ex/world6.py --out /tmp/claude-0/c11ex/dmg20_half/seed0 --seeds 0 --damage 120:0.2:half --no-movie`
- segmentation: matter > 0.57 of robust range [-0.819, 0.6147], min area 6 px

## Measurements
- components: final 28, mean 18.1, max 29; occupancy final 0.06
- tracks: 80; persistent (alive >= 50% of run): 13; longest 167 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 28, 26], H1 [0, 0, 0]
- motion: 38 long-lived tracks moved >= 1 body length; max speed 0.0797/time; max body lengths 3.7
- replication (lineage window K = 20 frames = time 100, default): splits 32, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 3, merges 7, merge/split ratio 0.219, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.4171, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 118: holes 0, rim-vs-core 0.52, rim-vs-outside 0.37, heterogeneity 0.17; core [0.946, 0.92, 0.438] rim [0.715, 0.603, 0.776]
  - track 23 at frame 126: holes 0, rim-vs-core 0.39, rim-vs-outside 0.32, heterogeneity 0.15; core [0.915, 0.803, 0.477] rim [0.746, 0.565, 0.739]
  - track 24 at frame 126: holes 0, rim-vs-core 0.47, rim-vs-outside 0.32, heterogeneity 0.15; core [0.945, 0.743, 0.524] rim [0.756, 0.515, 0.888]
  - track 58 at frame 180: holes 0, rim-vs-core 0.53, rim-vs-outside 0.35, heterogeneity 0.18; core [0.94, 0.888, 0.476] rim [0.71, 0.567, 0.826]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 123 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 4.91 (aggregate of 123 individuals; 0/123 membrane-like individually; rim level 0.765)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.763, rim/outside 8.24 (aggregate of 123 individuals; 0/123 membrane-like individually; rim level 0.656)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.58, rim/outside 2.13 (aggregate of 123 individuals; 92/123 membrane-like individually; rim level 0.653)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #15 (t=590, R_eq 3.24): ['surfactant s']; #23 (t=630, R_eq 3.39): none; #24 (t=630, R_eq 2.52): ['surfactant s']; #58 (t=900, R_eq 3.04): ['surfactant s']
- damage `half` (requested 0.20 of the area) at frame 120 (t=600): target = main-run track #13; the individual is one component of 22 px = 0.59x the median individual, aspect 1.26 (rule mature-compact: track age 90 frames vs K=20; 19 individuals from 19 components at that frame; open-ring individuals, not eligible: 0); mask 12 px (5 inside the individual)
- damage MEASURED: the target lost 101% of its matter (inside the individual: its components and what they enclose; 5 of 22 px lost > half their matter); net matter lost outside it = 96.5% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 7 of the 12 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[600.0, 680.0, 760.0, 840.0, 920.0, 1000.0]: target [0.682, None, None, None, None, None] (matter [0.776, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; last seen t=605); comparator [1.0, 1.045, 0.773, 1.091, 1.182, None] (matter [1.0, 1.103, 0.848, 1.012, 1.271, None]; pieces [1, 1, 1, 1, 1, 0]; merged with another individual at t=[995.0]; last seen t=990). Follow-up: pre-cut field at frame 120, then recorded frames 120..200 segmented with the TARGETING range [-0.816183, 0.614719] (threshold 0.5704), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 123 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
