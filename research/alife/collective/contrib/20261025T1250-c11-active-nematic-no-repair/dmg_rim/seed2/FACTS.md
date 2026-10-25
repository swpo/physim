# Evidence pack: active-nematic-droplets (seed 2)

- world: `../../world6.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 353s; status ok
- command: `python -m labkit.run /tmp/claude-0/c11ex/world6.py --out /tmp/claude-0/c11ex/dmg_rim/seed2 --seeds 2 --damage 120:0.4:rim --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8227, 0.6223], min area 6 px

## Measurements
- components: final 29, mean 19.2, max 29; occupancy final 0.07
- tracks: 107; persistent (alive >= 50% of run): 4; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.43 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 29, 26], H1 [0, 0, 0]
- motion: 41 long-lived tracks moved >= 1 body length; max speed 0.0933/time; max body lengths 5.8
- replication (lineage window K = 20 frames = time 100, default): splits 42, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 3, merges 15, merge/split ratio 0.357, nucleations 8
- channel total drift (end/start - 1): [-0.5106, -0.3668, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 126: holes 0, rim-vs-core 0.50, rim-vs-outside 0.35, heterogeneity 0.17; core [0.944, 0.902, 0.42] rim [0.729, 0.598, 0.758]
  - track 28 at frame 121: holes 0, rim-vs-core 0.41, rim-vs-outside 0.29, heterogeneity 0.15; core [0.899, 0.704, 0.534] rim [0.711, 0.477, 0.813]
  - track 46 at frame 145: holes 0, rim-vs-core 0.46, rim-vs-outside 0.37, heterogeneity 0.16; core [0.95, 0.888, 0.398] rim [0.758, 0.619, 0.724]
  - track 62 at frame 158: holes 0, rim-vs-core 0.34, rim-vs-outside 0.42, heterogeneity 0.15; core [0.916, 0.837, 0.47] rim [0.759, 0.638, 0.694]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 126 components >= 12 px at frames [34, 67, 101, 133, 166, 200]; 3 components of the damaged lineage after the cut left out):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.802, rim/outside 4.87 (aggregate of 126 individuals; 0/126 membrane-like individually; rim level 0.758)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.747, rim/outside 8.38 (aggregate of 126 individuals; 0/126 membrane-like individually; rim level 0.646)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.62, rim/outside 2.13 (aggregate of 126 individuals; 96/126 membrane-like individually; rim level 0.648)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #24 (t=630, R_eq 3.14): ['surfactant s']; #28 (t=605, R_eq 3.66): none; #46 (t=725, R_eq 2.99): ['surfactant s']; #62 (t=790, R_eq 3.43): none
- damage `rim` (requested 0.40 of the area) at frame 120 (t=600): target = main-run track #45; the individual is one component of 19 px = 0.56x the median individual, aspect 1.17 (rule mature-compact: track age 32 frames vs K=20; 25 individuals from 25 components at that frame; open-ring individuals, not eligible: 0); mask 9 px (5 inside the individual)
- damage MEASURED: the target lost 130% of its matter (inside the individual: its components and what they enclose; 5 of 19 px lost > half their matter); net matter lost outside it = 63.1% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (rim mode: the disk has the requested area but is centred on the individual's outer boundary, so about half of it lies outside the individual and cuts the layer at the edge)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[600.0, 680.0, 760.0, 840.0, 920.0, 1000.0]: target [0.684, None, None, None, None, None] (matter [0.778, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; merged with another individual at t=[605.0]; last seen t=600); comparator [1.0, 1.0, 1.241, None, None, None] (matter [1.0, 0.939, 1.203, None, None, None]; pieces [1, 1, 1, 0, 0, 0]; merged with another individual at t=[840.0]; last seen t=835). Follow-up: pre-cut field at frame 120, then recorded frames 120..200 segmented with the TARGETING range [-0.816469, 0.611303] (threshold 0.5718), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
