# Evidence pack: active-gel-fed-comets-twin (seed 1)

- world: `../../world_twin_global.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 55s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1046-c09-active-gel-bd-twin/world_twin_global.py --out collective/contrib/20261025T1046-c09-active-gel-bd-twin/pack_global --seeds 0 1 --frames 200 --no-movie`
- segmentation: matter > 0.32 of robust range [0.0, 3.0921], min area 6 px

## Measurements
- components: final 1, mean 5.6, max 45; occupancy final 0.00
- tracks: 194; persistent (alive >= 50% of run): 0; longest 97 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 2.71/time; max body lengths 9.9
- replication (lineage window K = 20 frames = time 20, default): splits 76, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 42
- channel total drift (end/start - 1): [-0.9795, -0.7901, -0.0807]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 193 at frame 153: holes 0, rim-vs-core 0.27, rim-vs-outside 0.19, heterogeneity 0.10; core [0.79, 0.244, 0.287] rim [0.529, 0.215, 0.366]
  - track 166 at frame 50: holes 0, rim-vs-core 0.14, rim-vs-outside 0.13, heterogeneity 0.06; core [0.641, 0.722, 0.166] rim [0.502, 0.719, 0.181]
  - track 171 at frame 52: holes 0, rim-vs-core 0.22, rim-vs-outside 0.57, heterogeneity 0.12; core [1.0, 0.688, 0.171] rim [0.784, 0.679, 0.2]
  - track 99 at frame 22: holes 0, rim-vs-core 0.32, rim-vs-outside 0.33, heterogeneity 0.09; core [0.913, 0.904, 0.012] rim [0.592, 0.895, 0.047]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 14 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.863, rim/outside 7.6 (aggregate of 14 individuals; 0/14 membrane-like individually; rim level 0.745)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.948, rim/outside 1.04 (aggregate of 14 individuals; 0/14 membrane-like individually; rim level 0.659)
  - radial substrate s: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.39, rim/outside 0.778 (aggregate of 14 individuals; 0/14 membrane-like individually; rim level 0.199)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #193 (t=153, R_eq 4.18): none; #166 (t=50, R_eq 2.99): none; #171 (t=52, R_eq 6.31): none; #99 (t=22, R_eq 6.02): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
