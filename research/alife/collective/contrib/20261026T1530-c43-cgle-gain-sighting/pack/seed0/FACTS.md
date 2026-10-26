# Evidence pack: cgle-gain (seed 0)

- world: `../../world.py`, family `cgle`
- parent: collective/contrib/20261025T0841-c03-cgle-solitons; mutation: the CGLE linear gain becomes a local gain medium g, depleted by |A|^2 and regrowing toward g0
- run: 201 frames x 500 steps x dt 0.01 = time 1000; grid [96, 96]; wall 338s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1530-c43-cgle-gain-sighting/world.py --out collective/contrib/20261026T1530-c43-cgle-gain-sighting/pack/seed0 --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.21 of robust range [0.0, 2.3614], min area 6 px

## Measurements
- components: final 2, mean 1.8, max 3; occupancy final 0.13
- tracks: 12; persistent (alive >= 50% of run): 0; longest 64 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.08, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 2, 2], H1 [1, 1, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.433/time; max body lengths 6.5
- replication (lineage window K = 20 frames = time 100, default): splits 4, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 3, merge/split ratio 0.75, nucleations 0
- channel total drift (end/start - 1): [-0.8305, 0.2178, -0.3264]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 79: holes 0, rim-vs-core 0.54, rim-vs-outside 0.28, heterogeneity 0.25; core [0.871, 0.611, 0.485] rim [0.373, 0.463, 0.626]
  - track 5 at frame 79: holes 0, rim-vs-core 0.33, rim-vs-outside 0.61, heterogeneity 0.26; core [0.903, 0.254, 0.153] rim [0.623, 0.412, 0.247]
  - track 10 at frame 171: holes 0, rim-vs-core 0.49, rim-vs-outside 0.30, heterogeneity 0.23; core [0.834, 0.451, 0.229] rim [0.378, 0.456, 0.396]
  - track 11 at frame 171: holes 0, rim-vs-core 0.55, rim-vs-outside 0.29, heterogeneity 0.20; core [0.853, 0.769, 0.339] rim [0.365, 0.572, 0.49]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 11 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial |A|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.781, rim/outside 18.1 (aggregate of 11 individuals; 0/11 membrane-like individually; rim level 0.537)
  - radial Re A: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 1.04 (aggregate of 11 individuals; 0/11 membrane-like individually; rim level 0.464)
  - radial g: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.48, rim/outside 0.806 (aggregate of 11 individuals; 0/11 membrane-like individually; rim level 0.569)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=395, R_eq 7.76): none; #5 (t=395, R_eq 18.24, ring): ['|A|']; #10 (t=855, R_eq 7.11): none; #11 (t=855, R_eq 8.08): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
