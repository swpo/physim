# Evidence pack: active-nematic-marangoni-turnover (seed 82)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) plus a trait-blind random dilution of whole bodies every 10 frames (serial-transfer turnover)
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 689s; status ok
- command: `python -m labkit.run /tmp/claude-0/mt/world.py --out /tmp/claude-0/mt/runs/long_p0.10_redist/seed82 --seeds 82 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8285, 0.5824], min area 6 px

## Measurements
- components: final 17, mean 20.5, max 29; occupancy final 0.07
- tracks: 288; persistent (alive >= 50% of run): 0; longest 156 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 18, 17], H1 [1, 0, 0]
- motion: 125 long-lived tracks moved >= 1 body length; max speed 0.361/time; max body lengths 7.7
- replication (lineage window K = 20 frames = time 100, default): splits 123, persistent splits 51 (0 more failed only because the siblings re-merged within K), max generation 9, merges 30, merge/split ratio 0.244, nucleations 10
- channel total drift (end/start - 1): [-0.5029, -0.568, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 118 at frame 235: holes 0, rim-vs-core 0.55, rim-vs-outside 0.34, heterogeneity 0.13; core [0.957, 0.706, 0.361, 0.0] rim [0.761, 0.456, 0.813, 0.0]
  - track 174 at frame 289: holes 0, rim-vs-core 0.75, rim-vs-outside 0.35, heterogeneity 0.18; core [0.973, 0.875, 0.387, 0.0] rim [0.742, 0.453, 0.958, 0.0]
  - track 198 at frame 326: holes 0, rim-vs-core 0.43, rim-vs-outside 0.38, heterogeneity 0.14; core [0.947, 0.601, 0.42, 0.0] rim [0.784, 0.498, 0.8, 0.0]
  - track 238 at frame 376: holes 0, rim-vs-core 0.53, rim-vs-outside 0.32, heterogeneity 0.14; core [0.96, 0.617, 0.357, 0.0] rim [0.762, 0.385, 0.787, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 127 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.768, rim/outside 3.9 (aggregate of 127 individuals; 1/127 membrane-like individually; rim level 0.659)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.759, rim/outside 6.96 (aggregate of 127 individuals; 12/127 membrane-like individually; rim level 0.486)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 3 (aggregate of 127 individuals; 53/127 membrane-like individually; rim level 0.583)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 127 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #118 (t=1175, R_eq 4.03): none; #174 (t=1445, R_eq 4.44): ['surfactant s']; #198 (t=1630, R_eq 4.22): ['order |Q|']; #238 (t=1880, R_eq 4.22): ['order |Q|']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 127 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
