# Evidence pack: active-nematic-droplets (seed 1)

- world: `../../world6.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 506s; status ok
- command: `python -m labkit.run /tmp/claude-0/c11ex/world6.py --out /tmp/claude-0/c11ex/dmg20_half/seed1 --seeds 1 --damage 150:0.2:half --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8144, 0.5773], min area 6 px

## Measurements
- components: final 20, mean 9.8, max 21; occupancy final 0.04
- tracks: 55; persistent (alive >= 50% of run): 0; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 20, 20], H1 [0, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.114/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 100, default): splits 25, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 5, merges 1, merge/split ratio 0.04, nucleations 4
- channel total drift (end/start - 1): [-0.4929, -0.5839, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 155: holes 0, rim-vs-core 0.46, rim-vs-outside 0.42, heterogeneity 0.17; core [0.971, 0.955, 0.445] rim [0.776, 0.707, 0.785]
  - track 8 at frame 87: holes 0, rim-vs-core 0.49, rim-vs-outside 0.36, heterogeneity 0.16; core [0.967, 0.945, 0.46] rim [0.766, 0.65, 0.801]
  - track 5 at frame 71: holes 0, rim-vs-core 0.49, rim-vs-outside 0.37, heterogeneity 0.17; core [0.973, 0.913, 0.438] rim [0.783, 0.625, 0.784]
  - track 39 at frame 182: holes 0, rim-vs-core 0.54, rim-vs-outside 0.41, heterogeneity 0.18; core [0.974, 0.968, 0.455] rim [0.767, 0.695, 0.872]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 67 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.823, rim/outside 4.48 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.75)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 7.17 (aggregate of 67 individuals; 1/67 membrane-like individually; rim level 0.67)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 2.07 (aggregate of 67 individuals; 39/67 membrane-like individually; rim level 0.667)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #21 (t=775, R_eq 3.43): ['surfactant s']; #8 (t=435, R_eq 3.14): ['surfactant s']; #5 (t=355, R_eq 2.88): ['surfactant s']; #39 (t=910, R_eq 3.09): ['surfactant s']
- damage `half` (requested 0.20 of the area) at frame 150 (t=750): target = main-run track #23; the individual is one component of 26 px = 0.65x the median individual, aspect 1.71 (rule mature-compact: track age 34 frames vs K=20; 13 individuals from 13 components at that frame; open-ring individuals, not eligible: 2); mask 12 px (6 inside the individual)
- damage MEASURED: the target lost 100% of its matter (inside the individual: its components and what they enclose; 6 of 26 px lost > half their matter); net matter lost outside it = 73.5% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 6 of the 12 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[750.0, 800.0, 850.0, 900.0, 950.0, 1000.0]: target [0.769, None, None, None, None, None] (matter [0.833, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; last seen t=770); comparator [1.0, 1.0, 1.0, 0.971, 0.882, 0.735] (matter [1.0, 1.004, 1.013, 0.974, 0.848, 0.714]; pieces [1, 1, 1, 1, 1, 1]). Follow-up: pre-cut field at frame 150, then recorded frames 150..200 segmented with the TARGETING range [-0.808483, 0.566601] (threshold 0.588), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 67 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- damage target is elongated (aspect 1.71 > 1.5; rule mature-compact): it may be elongating or pinching (dividing) rather than a compact individual; check damage.png or damage at another frame

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
