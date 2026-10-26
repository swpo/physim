# Evidence pack: active-nematic-marangoni-turnover (seed 80)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) plus a trait-blind random dilution of whole bodies every 10 frames (serial-transfer turnover)
- run: 151 frames x 100 steps x dt 0.05 = time 750; grid [128, 128]; wall 272s; status ok
- command: `python -m labkit.run /tmp/claude-0/mt/world.py --out /tmp/claude-0/mt/runs/tune_p0.20/seed80 --seeds 80 --size 128 128 --frames 150 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8092, 0.5503], min area 6 px

## Measurements
- components: final 7, mean 10.6, max 20; occupancy final 0.02
- tracks: 82; persistent (alive >= 50% of run): 1; longest 81 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 8, 7], H1 [1, 0, 0]
- motion: 30 long-lived tracks moved >= 1 body length; max speed 0.354/time; max body lengths 6.1
- replication (lineage window K = 20 frames = time 100, default): splits 33, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.03, nucleations 14
- channel total drift (end/start - 1): [-0.5663, -0.8106, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 61: holes 0, rim-vs-core 0.61, rim-vs-outside 0.42, heterogeneity 0.15; core [0.977, 0.94, 0.415, 0.0] rim [0.784, 0.644, 0.908, 0.0]
  - track 42 at frame 87: holes 0, rim-vs-core 0.59, rim-vs-outside 0.35, heterogeneity 0.15; core [0.968, 0.707, 0.477, 0.0] rim [0.763, 0.448, 0.96, 0.0]
  - track 60 at frame 127: holes 0, rim-vs-core 0.50, rim-vs-outside 0.42, heterogeneity 0.14; core [0.963, 0.931, 0.421, 0.0] rim [0.778, 0.689, 0.815, 0.0]
  - track 58 at frame 116: holes 0, rim-vs-core 0.52, rim-vs-outside 0.43, heterogeneity 0.13; core [0.975, 0.948, 0.381, 0.0] rim [0.787, 0.697, 0.792, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 65 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 4.35 (aggregate of 65 individuals; 0/65 membrane-like individually; rim level 0.709)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.82, rim/outside 7.44 (aggregate of 65 individuals; 3/65 membrane-like individually; rim level 0.572)
  - radial surfactant s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.11, rim/outside 3.28 (aggregate of 65 individuals; 29/65 membrane-like individually; rim level 0.606)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 65 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #12 (t=305, R_eq 3.57): ['surfactant s']; #42 (t=435, R_eq 4.37): none; #60 (t=635, R_eq 3.83): ['surfactant s']; #58 (t=580, R_eq 3.95): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 65 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
