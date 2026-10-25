# Evidence pack: active-gel-fed-comets (seed 0)

- world: `../world_res15.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [192, 192]; wall 97s; status ok
- command: `python -m labkit.run /tmp/claude-0/c09/ag/claim/world_res15.py --out /tmp/claude-0/c09/ag/claim/pack_res15 --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.13 of robust range [0.0245, 7.5357], min area 6 px

## Measurements
- components: final 10, mean 11.9, max 55; occupancy final 0.01
- tracks: 105; persistent (alive >= 50% of run): 6; longest 173 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.811/time; max body lengths 10.1
- replication (lineage window K = 20 frames = time 20, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 40, merge/split ratio 20, nucleations 61
- channel total drift (end/start - 1): [-0.84, -0.6875, -0.4212]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 92 at frame 114: holes 0, rim-vs-core 0.40, rim-vs-outside 0.17, heterogeneity 0.11; core [0.733, 0.461, 0.114] rim [0.344, 0.4, 0.158]
  - track 96 at frame 116: holes 0, rim-vs-core 0.44, rim-vs-outside 0.17, heterogeneity 0.12; core [0.767, 0.479, 0.092] rim [0.339, 0.403, 0.143]
  - track 97 at frame 119: holes 0, rim-vs-core 0.23, rim-vs-outside 0.34, heterogeneity 0.12; core [0.718, 0.465, 0.096] rim [0.486, 0.461, 0.12]
  - track 98 at frame 121: holes 0, rim-vs-core 0.45, rim-vs-outside 0.17, heterogeneity 0.13; core [0.76, 0.459, 0.093] rim [0.323, 0.388, 0.146]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 56 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.655, rim/outside 15 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.609)
  - radial regulator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.89, rim/outside 1.43 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.553)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.5, rim/outside 0.693 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.144)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #92 (t=114, R_eq 3.66): none; #96 (t=116, R_eq 3.83): none; #97 (t=119, R_eq 3.91): none; #98 (t=121, R_eq 3.91): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
