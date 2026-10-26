# Evidence pack: active-nematic-marangoni-turnover (seed 80)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) plus a trait-blind random dilution of whole bodies every 10 frames (serial-transfer turnover)
- run: 151 frames x 100 steps x dt 0.05 = time 750; grid [128, 128]; wall 260s; status ok
- command: `python -m labkit.run /tmp/claude-0/mt/world.py --out /tmp/claude-0/mt/runs/tune_p0.10_pb-0.56/seed80 --seeds 80 --size 128 128 --frames 150 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8423, 0.5926], min area 6 px

## Measurements
- components: final 23, mean 24.2, max 35; occupancy final 0.08
- tracks: 157; persistent (alive >= 50% of run): 6; longest 104 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 24, 22], H1 [2, 0, 0]
- motion: 52 long-lived tracks moved >= 1 body length; max speed 0.214/time; max body lengths 6.7
- replication (lineage window K = 20 frames = time 100, default): splits 58, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 3, merges 17, merge/split ratio 0.293, nucleations 25
- channel total drift (end/start - 1): [-0.4798, -0.4775, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 67: holes 0, rim-vs-core 0.68, rim-vs-outside 0.36, heterogeneity 0.17; core [0.962, 0.79, 0.384, 0.0] rim [0.759, 0.483, 0.957, 0.0]
  - track 42 at frame 81: holes 0, rim-vs-core 0.51, rim-vs-outside 0.38, heterogeneity 0.14; core [0.928, 0.878, 0.387, 0.0] rim [0.726, 0.576, 0.747, 0.0]
  - track 44 at frame 81: holes 0, rim-vs-core 0.55, rim-vs-outside 0.30, heterogeneity 0.14; core [0.94, 0.565, 0.431, 0.0] rim [0.742, 0.348, 0.892, 0.0]
  - track 110 at frame 121: holes 0, rim-vs-core 0.60, rim-vs-outside 0.35, heterogeneity 0.17; core [0.949, 0.81, 0.403, 0.0] rim [0.75, 0.528, 0.894, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 155 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.795, rim/outside 4 (aggregate of 155 individuals; 0/155 membrane-like individually; rim level 0.679)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.795, rim/outside 7.27 (aggregate of 155 individuals; 13/155 membrane-like individually; rim level 0.494)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 3 (aggregate of 155 individuals; 63/155 membrane-like individually; rim level 0.54)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 155 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #16 (t=335, R_eq 4.48): ['surfactant s']; #42 (t=405, R_eq 4.03): none; #44 (t=405, R_eq 4.65): ['order |Q|']; #110 (t=605, R_eq 4.55): none

## Warnings
- radial: 8 of 155 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
