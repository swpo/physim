# Evidence pack: active-gel-fed-comets (seed 6)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T1016-c09-active-gel-comets-claim/world_starve.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 43s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1016-c09-active-gel-comets-claim/world_starve.py --out /tmp/claude-0/c11rev9/world_starve --seeds 6 --frames 200 --no-movie`
- segmentation: matter > 0.12 of robust range [0.0, 8.0089], min area 6 px

## Measurements
- components: final 0, mean 9.0, max 50; occupancy final 0.00
- tracks: 99; persistent (alive >= 50% of run): 0; longest 97 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.592/time; max body lengths 5.5
- replication (lineage window K = 20 frames = time 20, default): splits 6, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 37, merge/split ratio 6.17, nucleations 52
- channel total drift (end/start - 1): [-0.9999, -0.7731, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 89 at frame 77: holes 0, rim-vs-core 0.25, rim-vs-outside 0.21, heterogeneity 0.05; core [0.665, 0.607, 0.355] rim [0.421, 0.573, 0.373]
  - track 91 at frame 81: holes 0, rim-vs-core 0.26, rim-vs-outside 0.22, heterogeneity 0.07; core [0.664, 0.587, 0.368] rim [0.408, 0.565, 0.387]
  - track 93 at frame 81: holes 0, rim-vs-core 0.19, rim-vs-outside 0.20, heterogeneity 0.05; core [0.608, 0.613, 0.373] rim [0.425, 0.575, 0.389]
  - track 94 at frame 91: holes 0, rim-vs-core 0.33, rim-vs-outside 0.24, heterogeneity 0.08; core [0.747, 0.571, 0.354] rim [0.417, 0.526, 0.38]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 31 components >= 12 px at frames [34, 67, 101]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.668, rim/outside 13.5 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.632)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.902, rim/outside 1.27 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.719)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.45, rim/outside 0.873 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.338)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #89 (t=77, R_eq 1.95): none; #91 (t=81, R_eq 2.11): none; #93 (t=81, R_eq 1.87): none; #94 (t=91, R_eq 2.26): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
