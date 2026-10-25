# Evidence pack: active-gel-fed-comets (seed 7)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1016-c09-active-gel-comets-claim/world.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 46s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1016-c09-active-gel-comets-claim/world.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev8/fed --seeds 6 7 --frames 200 --no-movie`
- segmentation: matter > 0.12 of robust range [0.0201, 7.901], min area 6 px

## Measurements
- components: final 9, mean 12.4, max 46; occupancy final 0.01
- tracks: 95; persistent (alive >= 50% of run): 7; longest 187 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.54 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 31 long-lived tracks moved >= 1 body length; max speed 0.534/time; max body lengths 7.9
- replication (lineage window K = 20 frames = time 20, default): splits 8, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 28, merge/split ratio 3.5, nucleations 56
- channel total drift (end/start - 1): [-0.8382, -0.6882, -0.4156]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 72 at frame 108: holes 0, rim-vs-core 0.32, rim-vs-outside 0.22, heterogeneity 0.08; core [0.68, 0.476, 0.128] rim [0.369, 0.426, 0.163]
  - track 73 at frame 109: holes 0, rim-vs-core 0.39, rim-vs-outside 0.22, heterogeneity 0.10; core [0.739, 0.524, 0.113] rim [0.352, 0.463, 0.157]
  - track 74 at frame 109: holes 0, rim-vs-core 0.43, rim-vs-outside 0.21, heterogeneity 0.11; core [0.751, 0.518, 0.1] rim [0.328, 0.444, 0.149]
  - track 86 at frame 131: holes 0, rim-vs-core 0.43, rim-vs-outside 0.27, heterogeneity 0.12; core [0.837, 0.465, 0.092] rim [0.415, 0.382, 0.142]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 57 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.6, rim/outside 16.8 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.58)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.881, rim/outside 1.45 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.543)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.94, rim/outside 0.687 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.146)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #72 (t=108, R_eq 2.26): none; #73 (t=109, R_eq 2.46): none; #74 (t=109, R_eq 2.59): none; #86 (t=131, R_eq 2.46): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
