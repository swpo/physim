# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 91)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 554s; status ok
- command: `python -m labkit.run /tmp/claude-0/se/world.py --out /tmp/claude-0/se/runs/S/seed91 --seeds 91 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.62 of robust range [-0.9326, 0.5719], min area 6 px

## Measurements
- components: final 23, mean 24.7, max 35; occupancy final 0.08
- tracks: 128; persistent (alive >= 50% of run): 12; longest 296 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 23, 23], H1 [0, 0, 0]
- motion: 79 long-lived tracks moved >= 1 body length; max speed 0.335/time; max body lengths 13.9
- replication (lineage window K = 20 frames = time 100, default): splits 46, persistent splits 31 (0 more failed only because the siblings re-merged within K), max generation 5, merges 25, merge/split ratio 0.543, nucleations 10
- channel total drift (end/start - 1): [-0.5702, -0.4639, None, -0.0278]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 169: holes 0, rim-vs-core 0.58, rim-vs-outside 0.31, heterogeneity 0.14; core [0.955, 0.609, 0.384, 1.0] rim [0.759, 0.368, 0.872, 1.0]
  - track 40 at frame 202: holes 0, rim-vs-core 0.57, rim-vs-outside 0.33, heterogeneity 0.14; core [0.955, 0.687, 0.379, 1.0] rim [0.764, 0.436, 0.859, 1.0]
  - track 19 at frame 159: holes 0, rim-vs-core 0.58, rim-vs-outside 0.30, heterogeneity 0.15; core [0.952, 0.533, 0.441, 1.0] rim [0.754, 0.339, 0.947, 1.0]
  - track 107 at frame 282: holes 0, rim-vs-core 0.66, rim-vs-outside 0.35, heterogeneity 0.16; core [0.953, 0.82, 0.363, 1.0] rim [0.748, 0.435, 0.859, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 154 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 3.52 (aggregate of 154 individuals; 1/154 membrane-like individually; rim level 0.725)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.752, rim/outside 8.9 (aggregate of 154 individuals; 8/154 membrane-like individually; rim level 0.546)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.34, rim/outside 3.32 (aggregate of 154 individuals; 88/154 membrane-like individually; rim level 0.615)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.999, rim/outside 1 (aggregate of 154 individuals; 0/154 membrane-like individually; rim level 0.999)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=845, R_eq 4.22): none; #40 (t=1010, R_eq 4.33): none; #19 (t=795, R_eq 4.41): ['order |Q|']; #107 (t=1410, R_eq 3.04): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 154 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
