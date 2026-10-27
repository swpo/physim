# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 95)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 619s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/mar/S --seeds 95 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0094, 0.5495], min area 6 px

## Measurements
- components: final 10, mean 11.0, max 22; occupancy final 0.04
- tracks: 94; persistent (alive >= 50% of run): 2; longest 213 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.25 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 11, 9], H1 [0, 0, 0]
- motion: 43 long-lived tracks moved >= 1 body length; max speed 0.316/time; max body lengths 12.1
- replication (lineage window K = 20 frames = time 100, default): splits 35, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 4, merges 13, merge/split ratio 0.371, nucleations 11
- channel total drift (end/start - 1): [-0.9093, -0.7267, None, -0.312]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 126: holes 0, rim-vs-core 0.46, rim-vs-outside 0.44, heterogeneity 0.26; core [0.963, 0.96, 0.414, 0.636] rim [0.812, 0.732, 0.782, 0.71]
  - track 8 at frame 113: holes 0, rim-vs-core 0.48, rim-vs-outside 0.40, heterogeneity 0.13; core [0.968, 0.967, 0.348, 1.0] rim [0.8, 0.675, 0.689, 1.0]
  - track 43 at frame 156: holes 0, rim-vs-core 0.52, rim-vs-outside 0.31, heterogeneity 0.14; core [0.972, 0.703, 0.401, 1.0] rim [0.797, 0.482, 0.836, 1.0]
  - track 68 at frame 285: holes 0, rim-vs-core 0.56, rim-vs-outside 0.44, heterogeneity 0.14; core [0.969, 0.946, 0.396, 1.0] rim [0.791, 0.728, 0.885, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 68 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.812, rim/outside 2.88 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.745)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.775, rim/outside 7.76 (aggregate of 68 individuals; 5/68 membrane-like individually; rim level 0.578)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.27, rim/outside 3.18 (aggregate of 68 individuals; 28/68 membrane-like individually; rim level 0.608)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.03 (aggregate of 68 individuals; 1/68 membrane-like individually; rim level 0.99)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=630, R_eq 4.11): none; #8 (t=565, R_eq 3.61): ['surfactant s']; #43 (t=780, R_eq 4.11): none; #68 (t=1425, R_eq 4.41): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 68 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
