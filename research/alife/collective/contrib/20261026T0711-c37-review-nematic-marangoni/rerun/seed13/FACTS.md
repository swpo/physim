# Evidence pack: active-nematic-marangoni (seed 13)

- world: `../../../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 690s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/wip-c37/mar/rerun/seed13 --seeds 13 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8401, 0.57], min area 6 px

## Measurements
- components: final 29, mean 21.8, max 30; occupancy final 0.10
- tracks: 91; persistent (alive >= 50% of run): 20; longest 158 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.18 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 30, 29], H1 [0, 0, 0]
- motion: 45 long-lived tracks moved >= 1 body length; max speed 0.253/time; max body lengths 8.2
- replication (lineage window K = 20 frames = time 100, default): splits 36, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 4, merges 12, merge/split ratio 0.333, nucleations 7
- channel total drift (end/start - 1): [-0.5021, -0.4276, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 123: holes 0, rim-vs-core 0.75, rim-vs-outside 0.35, heterogeneity 0.22; core [0.942, 0.739, 0.408, 0.468] rim [0.744, 0.461, 0.89, 0.008]
  - track 23 at frame 124: holes 0, rim-vs-core 0.62, rim-vs-outside 0.28, heterogeneity 0.22; core [0.93, 0.483, 0.517, 0.462] rim [0.747, 0.377, 0.917, 0.034]
  - track 27 at frame 129: holes 0, rim-vs-core 0.78, rim-vs-outside 0.33, heterogeneity 0.27; core [0.963, 0.661, 0.389, 0.459] rim [0.758, 0.417, 0.938, 0.012]
  - track 69 at frame 163: holes 0, rim-vs-core 0.76, rim-vs-outside 0.34, heterogeneity 0.24; core [0.955, 0.72, 0.385, 0.457] rim [0.755, 0.436, 0.904, 0.018]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 143 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 4.74 (aggregate of 143 individuals; 2/143 membrane-like individually; rim level 0.712)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.849, rim/outside 9.02 (aggregate of 143 individuals; 11/143 membrane-like individually; rim level 0.528)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 3.29 (aggregate of 143 individuals; 53/143 membrane-like individually; rim level 0.586)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.494, rim/outside 1.94 (aggregate of 143 individuals; 19/143 membrane-like individually; rim level 0.127)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=615, R_eq 4.03): none; #23 (t=620, R_eq 4.41): ['order |Q|', 'cargo c']; #27 (t=645, R_eq 4.26): ['surfactant s']; #69 (t=815, R_eq 4.11): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 143 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
