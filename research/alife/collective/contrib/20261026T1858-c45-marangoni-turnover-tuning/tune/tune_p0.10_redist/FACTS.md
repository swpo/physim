# Evidence pack: active-nematic-marangoni-turnover (seed 80)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) plus a trait-blind random dilution of whole bodies every 10 frames (serial-transfer turnover)
- run: 151 frames x 100 steps x dt 0.05 = time 750; grid [128, 128]; wall 271s; status ok
- command: `python -m labkit.run /tmp/claude-0/mt/world.py --out /tmp/claude-0/mt/runs/tune_p0.10_redist/seed80 --seeds 80 --size 128 128 --frames 150 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8337, 0.579], min area 6 px

## Measurements
- components: final 24, mean 20.0, max 28; occupancy final 0.08
- tracks: 120; persistent (alive >= 50% of run): 3; longest 84 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.07 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 24, 22], H1 [0, 0, 0]
- motion: 52 long-lived tracks moved >= 1 body length; max speed 0.321/time; max body lengths 6.7
- replication (lineage window K = 20 frames = time 100, default): splits 50, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 3, merges 6, merge/split ratio 0.12, nucleations 14
- channel total drift (end/start - 1): [-0.5046, -0.4701, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 47 at frame 102: holes 0, rim-vs-core 0.60, rim-vs-outside 0.33, heterogeneity 0.14; core [0.949, 0.687, 0.441, 0.0] rim [0.744, 0.418, 0.935, 0.0]
  - track 31 at frame 72: holes 0, rim-vs-core 0.61, rim-vs-outside 0.36, heterogeneity 0.15; core [0.953, 0.906, 0.391, 0.0] rim [0.75, 0.544, 0.842, 0.0]
  - track 49 at frame 100: holes 0, rim-vs-core 0.72, rim-vs-outside 0.38, heterogeneity 0.18; core [0.963, 0.873, 0.412, 0.0] rim [0.723, 0.507, 0.986, 0.0]
  - track 73 at frame 124: holes 0, rim-vs-core 0.50, rim-vs-outside 0.33, heterogeneity 0.14; core [0.934, 0.637, 0.435, 0.0] rim [0.735, 0.44, 0.852, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 134 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.777, rim/outside 4.27 (aggregate of 134 individuals; 1/134 membrane-like individually; rim level 0.688)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.745, rim/outside 8.15 (aggregate of 134 individuals; 5/134 membrane-like individually; rim level 0.533)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.27, rim/outside 3.26 (aggregate of 134 individuals; 65/134 membrane-like individually; rim level 0.582)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 134 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #47 (t=510, R_eq 4.37): none; #31 (t=360, R_eq 3.52): ['surfactant s']; #49 (t=500, R_eq 4.75): ['surfactant s']; #73 (t=620, R_eq 4.48): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 134 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
