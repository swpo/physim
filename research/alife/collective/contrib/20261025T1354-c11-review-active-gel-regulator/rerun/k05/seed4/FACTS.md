# Evidence pack: active-gel-fed-comets (seed 4)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T1016-c09-active-gel-comets-claim/world.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 301 frames x 100 steps x dt 0.01 = time 300; grid [128, 128]; wall 62s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1016-c09-active-gel-comets-claim/world.py --out /tmp/claude-0/c11rev28/k05 --seeds 4 --frames 300 --no-movie`
- segmentation: matter > 0.19 of robust range [0.0433, 5.0898], min area 6 px

## Measurements
- components: final 15, mean 15.0, max 36; occupancy final 0.04
- tracks: 278; persistent (alive >= 50% of run): 0; longest 143 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 15, 13], H1 [0, 0, 0]
- motion: 71 long-lived tracks moved >= 1 body length; max speed 2.01/time; max body lengths 23.5
- replication (lineage window K = 20 frames = time 20, default): splits 52, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 92, merge/split ratio 1.77, nucleations 86
- channel total drift (end/start - 1): [-0.6245, -0.6289, -0.3732]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 41 at frame 81: holes 0, rim-vs-core 0.43, rim-vs-outside 0.20, heterogeneity 0.16; core [0.767, 0.451, 0.102] rim [0.362, 0.332, 0.176]
  - track 84 at frame 88: holes 0, rim-vs-core 0.42, rim-vs-outside 0.20, heterogeneity 0.17; core [0.757, 0.393, 0.145] rim [0.347, 0.307, 0.214]
  - track 244 at frame 270: holes 0, rim-vs-core 0.50, rim-vs-outside 0.21, heterogeneity 0.20; core [0.815, 0.485, 0.103] rim [0.349, 0.351, 0.204]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 85 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.682, rim/outside 12.4 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.584)
  - radial regulator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 2 (aggregate of 85 individuals; 1/85 membrane-like individually; rim level 0.461)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.17, rim/outside 0.756 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.281)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #41 (t=81, R_eq 3.48): none; #84 (t=88, R_eq 3.39): none; #183 (t=204, R_eq 1.69): none; #244 (t=270, R_eq 3.99): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
