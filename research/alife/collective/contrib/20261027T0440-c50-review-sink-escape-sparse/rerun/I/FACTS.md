# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 94)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 708s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py --out /tmp/claude-0/se3/runs/I/seed94 --seeds 94 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.62 of robust range [-0.9439, 0.5693], min area 6 px

## Measurements
- components: final 24, mean 20.5, max 26; occupancy final 0.08
- tracks: 128; persistent (alive >= 50% of run): 6; longest 254 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.08 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 25, 23], H1 [1, 0, 0]
- motion: 78 long-lived tracks moved >= 1 body length; max speed 0.293/time; max body lengths 8.7
- replication (lineage window K = 20 frames = time 100, default): splits 52, persistent splits 36 (0 more failed only because the siblings re-merged within K), max generation 5, merges 17, merge/split ratio 0.327, nucleations 7
- channel total drift (end/start - 1): [-0.6384, -0.5539, None, -0.1643]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 32 at frame 183: holes 0, rim-vs-core 0.53, rim-vs-outside 0.31, heterogeneity 0.13; core [0.947, 0.741, 0.415, 1.0] rim [0.763, 0.472, 0.838, 1.0]
  - track 30 at frame 175: holes 0, rim-vs-core 0.60, rim-vs-outside 0.33, heterogeneity 0.14; core [0.951, 0.833, 0.414, 1.0] rim [0.766, 0.509, 0.879, 1.0]
  - track 53 at frame 218: holes 0, rim-vs-core 0.64, rim-vs-outside 0.32, heterogeneity 0.16; core [0.966, 0.731, 0.393, 1.0] rim [0.759, 0.419, 0.918, 1.0]
  - track 95 at frame 282: holes 0, rim-vs-core 0.41, rim-vs-outside 0.46, heterogeneity 0.15; core [0.941, 0.865, 0.388, 1.0] rim [0.801, 0.625, 0.692, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 129 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 3.36 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.72)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.796, rim/outside 8.47 (aggregate of 129 individuals; 9/129 membrane-like individually; rim level 0.524)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 3.19 (aggregate of 129 individuals; 47/129 membrane-like individually; rim level 0.601)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #32 (t=915, R_eq 4.03): none; #30 (t=875, R_eq 3.78): ['surfactant s']; #53 (t=1090, R_eq 4.37): ['surfactant s']; #95 (t=1410, R_eq 3.34): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 129 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
