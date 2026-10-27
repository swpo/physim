# Evidence pack: active-nematic-marangoni-turnover (seed 84)

- world: `../../20261026T1858-c45-marangoni-turnover-tuning/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) plus a trait-blind random dilution of whole bodies every 10 frames (serial-transfer turnover)
- run: 151 frames x 100 steps x dt 0.05 = time 750; grid [128, 128]; wall 209s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1858-c45-marangoni-turnover-tuning/world.py --out collective/contrib/20261027T0311-c51-review-marangoni-turnover/p0.10_redist --seeds 84 --size 128 128 --frames 150 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8287, 0.56], min area 6 px

## Measurements
- components: final 25, mean 15.1, max 26; occupancy final 0.09
- tracks: 94; persistent (alive >= 50% of run): 0; longest 64 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 25, 23], H1 [0, 0, 0]
- motion: 47 long-lived tracks moved >= 1 body length; max speed 0.308/time; max body lengths 7.7
- replication (lineage window K = 20 frames = time 100, default): splits 41, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 5, merges 4, merge/split ratio 0.098, nucleations 8
- channel total drift (end/start - 1): [-0.5044, -0.4215, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 73: holes 0, rim-vs-core 0.65, rim-vs-outside 0.35, heterogeneity 0.16; core [0.966, 0.759, 0.377, 0.0] rim [0.777, 0.482, 0.937, 0.0]
  - track 49 at frame 121: holes 0, rim-vs-core 0.62, rim-vs-outside 0.34, heterogeneity 0.16; core [0.969, 0.636, 0.425, 0.0] rim [0.742, 0.37, 0.937, 0.0]
  - track 51 at frame 121: holes 0, rim-vs-core 0.54, rim-vs-outside 0.40, heterogeneity 0.13; core [0.961, 0.943, 0.346, 0.0] rim [0.749, 0.615, 0.713, 0.0]
  - track 65 at frame 134: holes 0, rim-vs-core 0.65, rim-vs-outside 0.40, heterogeneity 0.15; core [0.97, 0.939, 0.392, 0.0] rim [0.757, 0.571, 0.89, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 105 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.787, rim/outside 4.28 (aggregate of 105 individuals; 0/105 membrane-like individually; rim level 0.695)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.773, rim/outside 8.03 (aggregate of 105 individuals; 5/105 membrane-like individually; rim level 0.552)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 3.16 (aggregate of 105 individuals; 42/105 membrane-like individually; rim level 0.603)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 105 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #16 (t=365, R_eq 4.48): none; #49 (t=605, R_eq 4.44): ['surfactant s']; #51 (t=605, R_eq 3.7): ['surfactant s']; #65 (t=670, R_eq 3.61): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 105 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
