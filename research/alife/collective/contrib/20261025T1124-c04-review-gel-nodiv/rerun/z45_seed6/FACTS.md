# Evidence pack: active-gel-fed-comets (seed 6)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1034-c09-active-gel-no-division/world_z45.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 301 frames x 100 steps x dt 0.01 = time 300; grid [128, 128]; wall 75s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1034-c09-active-gel-no-division/world_z45.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev14/z45 --seeds 6 7 --frames 300 --no-movie`
- segmentation: matter > 0.19 of robust range [0.0572, 4.952], min area 6 px

## Measurements
- components: final 15, mean 16.1, max 51; occupancy final 0.03
- tracks: 139; persistent (alive >= 50% of run): 11; longest 285 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [0, 0, 0]
- motion: 36 long-lived tracks moved >= 1 body length; max speed 0.481/time; max body lengths 10.6
- replication (lineage window K = 20 frames = time 20, default): splits 9, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 53, merge/split ratio 5.89, nucleations 68
- channel total drift (end/start - 1): [-0.6463, -0.5986, -0.3518]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 102 at frame 159: holes 0, rim-vs-core 0.45, rim-vs-outside 0.19, heterogeneity 0.15; core [0.737, 0.629, 0.065] rim [0.316, 0.5, 0.159]
  - track 106 at frame 159: holes 0, rim-vs-core 0.49, rim-vs-outside 0.21, heterogeneity 0.16; core [0.81, 0.526, 0.04] rim [0.342, 0.42, 0.134]
  - track 113 at frame 164: holes 0, rim-vs-core 0.36, rim-vs-outside 0.31, heterogeneity 0.15; core [0.775, 0.489, 0.081] rim [0.421, 0.492, 0.139]
  - track 120 at frame 182: holes 0, rim-vs-core 0.47, rim-vs-outside 0.21, heterogeneity 0.16; core [0.79, 0.557, 0.05] rim [0.351, 0.43, 0.145]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 87 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial generator a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.601, rim/outside 17.2 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.576)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.84, rim/outside 1.73 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.533)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.61, rim/outside 0.668 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.237)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #102 (t=159, R_eq 3.61): none; #106 (t=159, R_eq 3.66): none; #113 (t=164, R_eq 3.48): none; #120 (t=182, R_eq 3.52): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
