# Evidence pack: reacting-thermals (seed 39)

- world: `../../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 201 frames x 25 steps x dt 0.04 = time 200; grid [128, 128]; wall 13s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/c53-audit-work/screen --seeds 35 36 37 38 39 40 41 42 43 44 45 46 --frames 200 --spf 25 --no-movie`
- segmentation: matter > 0.34 of robust range [0.0, 0.7368], min area 6 px

## Measurements
- components: final 15, mean 10.8, max 40; occupancy final 0.02
- tracks: 177; persistent (alive >= 50% of run): 0; longest 85 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.10, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 17, 14], H1 [0, 0, 0]
- motion: 37 long-lived tracks moved >= 1 body length; max speed 1.03/time; max body lengths 14.2
- replication (lineage window K = 20 frames = time 20, default): splits 47, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 14, merge/split ratio 0.298, nucleations 35
- channel total drift (end/start - 1): [-0.8913, -0.2364, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 116 at frame 97: holes 0, rim-vs-core 0.23, rim-vs-outside 0.52, heterogeneity 0.14; core [0.734, 0.217, 0.509, 0.84] rim [0.588, 0.268, 0.621, 0.719]
  - track 113 at frame 91: holes 0, rim-vs-core 0.17, rim-vs-outside 0.44, heterogeneity 0.13; core [0.669, 0.203, 0.54, 0.734] rim [0.541, 0.253, 0.507, 0.632]
  - track 126 at frame 136: holes 0, rim-vs-core 0.18, rim-vs-outside 0.46, heterogeneity 0.13; core [0.708, 0.237, 0.412, 0.844] rim [0.584, 0.271, 0.438, 0.723]
  - track 168 at frame 190: holes 0, rim-vs-core 0.15, rim-vs-outside 0.36, heterogeneity 0.12; core [0.636, 0.219, 0.428, 0.72] rim [0.551, 0.252, 0.522, 0.644]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 48 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial heat T: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 5.45 (aggregate of 48 individuals; 2/48 membrane-like individually; rim level 0.499)
  - radial fuel Y: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.65, rim/outside 0.764 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.369)
  - radial vorticity: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 1.17 (aggregate of 48 individuals; 13/48 membrane-like individually; rim level 0.533)
  - radial burn r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.924, rim/outside 6.51 (aggregate of 48 individuals; 4/48 membrane-like individually; rim level 0.561)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #116 (t=97, R_eq 2.39): none; #113 (t=91, R_eq 2.88): ['burn r']; #126 (t=136, R_eq 2.33): none; #168 (t=190, R_eq 1.95): ['vorticity']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 48 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
