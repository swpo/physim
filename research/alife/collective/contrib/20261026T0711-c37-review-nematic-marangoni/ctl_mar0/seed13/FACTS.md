# Evidence pack: active-nematic-marangoni (seed 13)

- world: `../../../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 655s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/wip-c37/mar/ctl_mar0/seed13 --seeds 13 --no-movie`
- segmentation: matter > 0.58 of robust range [-0.8238, 0.6061], min area 6 px

## Measurements
- components: final 30, mean 17.5, max 32; occupancy final 0.06
- tracks: 96; persistent (alive >= 50% of run): 4; longest 125 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.38 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 30, 30], H1 [1, 0, 0]
- motion: 39 long-lived tracks moved >= 1 body length; max speed 0.0932/time; max body lengths 4.9
- replication (lineage window K = 20 frames = time 100, default): splits 41, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 3, merges 7, merge/split ratio 0.171, nucleations 7
- channel total drift (end/start - 1): [-0.5021, -0.4113, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 97: holes 0, rim-vs-core 0.70, rim-vs-outside 0.38, heterogeneity 0.21; core [0.948, 0.917, 0.318, 0.562] rim [0.756, 0.648, 0.631, 0.032]
  - track 20 at frame 104: holes 0, rim-vs-core 0.75, rim-vs-outside 0.39, heterogeneity 0.21; core [0.966, 0.944, 0.25, 0.609] rim [0.778, 0.685, 0.603, 0.024]
  - track 27 at frame 143: holes 0, rim-vs-core 0.68, rim-vs-outside 0.35, heterogeneity 0.20; core [0.959, 0.932, 0.288, 0.506] rim [0.77, 0.647, 0.625, 0.022]
  - track 53 at frame 160: holes 0, rim-vs-core 0.72, rim-vs-outside 0.39, heterogeneity 0.21; core [0.957, 0.925, 0.315, 0.551] rim [0.765, 0.664, 0.685, 0.027]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 119 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.829, rim/outside 4.68 (aggregate of 119 individuals; 0/119 membrane-like individually; rim level 0.76)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 7.8 (aggregate of 119 individuals; 4/119 membrane-like individually; rim level 0.641)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.62, rim/outside 2.93 (aggregate of 119 individuals; 91/119 membrane-like individually; rim level 0.546)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.275, rim/outside 1.69 (aggregate of 119 individuals; 17/119 membrane-like individually; rim level 0.155)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #15 (t=485, R_eq 3.39): ['surfactant s']; #20 (t=520, R_eq 2.93): ['surfactant s']; #27 (t=715, R_eq 3.04): ['surfactant s']; #53 (t=800, R_eq 3.34): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 119 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
