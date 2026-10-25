# Evidence pack: active-gel-fed-comets (seed 7)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1034-c09-active-gel-no-division/world_z45.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 301 frames x 100 steps x dt 0.01 = time 300; grid [128, 128]; wall 71s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1034-c09-active-gel-no-division/world_z45.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev14/z45 --seeds 6 7 --frames 300 --no-movie`
- segmentation: matter > 0.19 of robust range [0.0582, 5.0716], min area 6 px

## Measurements
- components: final 14, mean 15.9, max 54; occupancy final 0.03
- tracks: 121; persistent (alive >= 50% of run): 11; longest 291 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.68 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 14, 14], H1 [0, 0, 0]
- motion: 35 long-lived tracks moved >= 1 body length; max speed 0.508/time; max body lengths 12.6
- replication (lineage window K = 20 frames = time 20, default): splits 4, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 49, merge/split ratio 12.2, nucleations 66
- channel total drift (end/start - 1): [-0.6456, -0.5939, -0.3558]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 67 at frame 156: holes 0, rim-vs-core 0.48, rim-vs-outside 0.21, heterogeneity 0.16; core [0.803, 0.476, 0.04] rim [0.346, 0.38, 0.131]
  - track 93 at frame 164: holes 0, rim-vs-core 0.48, rim-vs-outside 0.21, heterogeneity 0.16; core [0.798, 0.513, 0.042] rim [0.339, 0.403, 0.137]
  - track 94 at frame 164: holes 0, rim-vs-core 0.39, rim-vs-outside 0.19, heterogeneity 0.12; core [0.71, 0.478, 0.101] rim [0.337, 0.407, 0.173]
  - track 102 at frame 171: holes 0, rim-vs-core 0.46, rim-vs-outside 0.20, heterogeneity 0.15; core [0.765, 0.575, 0.062] rim [0.328, 0.458, 0.156]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 87 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.609, rim/outside 16.6 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.579)
  - radial regulator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.84, rim/outside 1.76 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.554)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.43, rim/outside 0.665 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.231)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #67 (t=156, R_eq 3.57): none; #93 (t=164, R_eq 3.66): none; #94 (t=164, R_eq 3.24): none; #102 (t=171, R_eq 3.57): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
