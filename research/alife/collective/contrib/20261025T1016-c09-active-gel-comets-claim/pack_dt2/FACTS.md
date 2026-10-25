# Evidence pack: active-gel-fed-comets (seed 0)

- world: `../world_dt2.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 200 steps x dt 0.005 (--dt; world META dt 0.01) = time 200; grid [128, 128]; wall 83s; status ok
- command: `python -m labkit.run /tmp/claude-0/c09/ag/claim/world_dt2.py --out /tmp/claude-0/c09/ag/claim/pack_dt2 --seeds 0 --frames 200 --spf 200 --dt 0.005 --no-movie`
- segmentation: matter > 0.12 of robust range [0.0202, 8.405], min area 6 px

## Measurements
- components: final 10, mean 11.0, max 49; occupancy final 0.01
- tracks: 104; persistent (alive >= 50% of run): 5; longest 180 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.60 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 26 long-lived tracks moved >= 1 body length; max speed 0.536/time; max body lengths 9.2
- replication (lineage window K = 20 frames = time 20, default): splits 5, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 37, merge/split ratio 7.4, nucleations 52
- channel total drift (end/start - 1): [-0.8431, -0.6849, -0.4209]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 82 at frame 111: holes 0, rim-vs-core 0.42, rim-vs-outside 0.24, heterogeneity 0.11; core [0.774, 0.495, 0.109] rim [0.364, 0.412, 0.159]
  - track 86 at frame 113: holes 0, rim-vs-core 0.44, rim-vs-outside 0.21, heterogeneity 0.11; core [0.749, 0.488, 0.102] rim [0.317, 0.41, 0.154]
  - track 90 at frame 114: holes 0, rim-vs-core 0.46, rim-vs-outside 0.22, heterogeneity 0.12; core [0.791, 0.524, 0.096] rim [0.34, 0.449, 0.149]
  - track 95 at frame 123: holes 0, rim-vs-core 0.48, rim-vs-outside 0.23, heterogeneity 0.12; core [0.807, 0.466, 0.092] rim [0.34, 0.387, 0.146]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 50 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.609, rim/outside 17.7 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.579)
  - radial regulator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.873, rim/outside 1.54 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.536)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.91, rim/outside 0.697 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.155)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #82 (t=111, R_eq 2.52): none; #86 (t=113, R_eq 2.65): none; #90 (t=114, R_eq 2.59): none; #95 (t=123, R_eq 2.59): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
