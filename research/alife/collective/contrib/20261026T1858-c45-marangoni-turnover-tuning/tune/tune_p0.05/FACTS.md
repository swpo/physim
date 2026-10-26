# Evidence pack: active-nematic-marangoni-turnover (seed 80)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) plus a trait-blind random dilution of whole bodies every 10 frames (serial-transfer turnover)
- run: 151 frames x 100 steps x dt 0.05 = time 750; grid [128, 128]; wall 269s; status ok
- command: `python -m labkit.run /tmp/claude-0/mt/world.py --out /tmp/claude-0/mt/runs/tune_p0.05/seed80 --seeds 80 --size 128 128 --frames 150 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8349, 0.5723], min area 6 px

## Measurements
- components: final 26, mean 20.5, max 28; occupancy final 0.08
- tracks: 95; persistent (alive >= 50% of run): 11; longest 111 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 26, 25], H1 [0, 0, 0]
- motion: 46 long-lived tracks moved >= 1 body length; max speed 0.295/time; max body lengths 9.2
- replication (lineage window K = 20 frames = time 100, default): splits 38, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 3, merges 5, merge/split ratio 0.132, nucleations 14
- channel total drift (end/start - 1): [-0.5237, -0.4897, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 86: holes 0, rim-vs-core 0.58, rim-vs-outside 0.33, heterogeneity 0.15; core [0.949, 0.695, 0.419, 0.0] rim [0.745, 0.439, 0.895, 0.0]
  - track 13 at frame 74: holes 0, rim-vs-core 0.59, rim-vs-outside 0.34, heterogeneity 0.15; core [0.963, 0.751, 0.363, 0.0] rim [0.771, 0.487, 0.853, 0.0]
  - track 35 at frame 98: holes 0, rim-vs-core 0.52, rim-vs-outside 0.39, heterogeneity 0.13; core [0.946, 0.912, 0.361, 0.0] rim [0.748, 0.613, 0.741, 0.0]
  - track 71 at frame 134: holes 0, rim-vs-core 0.56, rim-vs-outside 0.39, heterogeneity 0.14; core [0.946, 0.911, 0.368, 0.0] rim [0.751, 0.583, 0.778, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 134 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 4.44 (aggregate of 134 individuals; 0/134 membrane-like individually; rim level 0.7)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 8.32 (aggregate of 134 individuals; 3/134 membrane-like individually; rim level 0.545)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 3.2 (aggregate of 134 individuals; 56/134 membrane-like individually; rim level 0.571)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 134 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #30 (t=430, R_eq 4.37): none; #13 (t=370, R_eq 4.22): none; #35 (t=490, R_eq 3.78): ['surfactant s']; #71 (t=670, R_eq 3.87): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 134 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
