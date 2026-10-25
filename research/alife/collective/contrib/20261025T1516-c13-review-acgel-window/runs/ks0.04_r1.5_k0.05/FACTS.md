# Evidence pack: active-gel-fed-comets (seed 2)

- world: `../../world.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 301 frames x 100 steps x dt 0.01 = time 300; grid [128, 128]; wall 63s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1516-c13-review-acgel-window/world.py --out collective/contrib/20261025T1516-c13-review-acgel-window/runs/ks0.04_r1.5_k0.05 --seeds 2 --frames 300 --no-movie`
- segmentation: matter > 0.21 of robust range [0.0442, 4.5763], min area 6 px

## Measurements
- components: final 13, mean 13.0, max 39; occupancy final 0.03
- tracks: 191; persistent (alive >= 50% of run): 0; longest 124 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 13, 10], H1 [0, 0, 0]
- motion: 60 long-lived tracks moved >= 1 body length; max speed 2.04/time; max body lengths 21.2
- replication (lineage window K = 20 frames = time 20, default): splits 25, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 60, merge/split ratio 2.4, nucleations 80
- channel total drift (end/start - 1): [-0.6874, -0.6849, -0.3924]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 126 at frame 189: holes 0, rim-vs-core 0.54, rim-vs-outside 0.25, heterogeneity 0.20; core [0.908, 0.421, 0.104] rim [0.397, 0.291, 0.205]
  - track 82 at frame 76: holes 0, rim-vs-core 0.39, rim-vs-outside 0.20, heterogeneity 0.15; core [0.775, 0.447, 0.146] rim [0.402, 0.346, 0.204]
  - track 104 at frame 106: holes 0, rim-vs-core 0.51, rim-vs-outside 0.23, heterogeneity 0.19; core [0.877, 0.413, 0.129] rim [0.39, 0.299, 0.213]
  - track 174 at frame 282: holes 0, rim-vs-core 0.48, rim-vs-outside 0.24, heterogeneity 0.18; core [0.86, 0.368, 0.166] rim [0.398, 0.255, 0.247]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 69 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial generator a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.725, rim/outside 10.5 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.646)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.812, rim/outside 1.8 (aggregate of 69 individuals; 1/69 membrane-like individually; rim level 0.432)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.81, rim/outside 0.788 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.257)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #126 (t=189, R_eq 3.91): none; #82 (t=76, R_eq 3.14): none; #104 (t=106, R_eq 3.7): none; #174 (t=282, R_eq 3.43): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
