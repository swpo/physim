# Evidence pack: rdtrail_slow (seed 2)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/_c07wip/world_slow.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 25s; status ok
- command: `python -m labkit.run collective/contrib/_c07wip/world_slow.py --out /tmp/claude-0/c07/pk_slow --seeds 0 1 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.995], min area 6 px

## Measurements
- components: final 17, mean 11.1, max 19; occupancy final 0.23
- tracks: 64; persistent (alive >= 50% of run): 2; longest 111 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.66 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.199/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 60, default): splits 27, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 4, merges 4, merge/split ratio 0.148, nucleations 0
- channel total drift (end/start - 1): [5.2684, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 31 at frame 146: holes 0, rim-vs-core 0.41, rim-vs-outside 0.32, heterogeneity 0.17; core [0.821, 0.602, 0.755] rim [0.496, 0.452, 0.56]
  - track 33 at frame 146: holes 0, rim-vs-core 0.46, rim-vs-outside 0.34, heterogeneity 0.15; core [0.825, 0.567, 0.825] rim [0.494, 0.419, 0.534]
  - track 35 at frame 156: holes 0, rim-vs-core 0.28, rim-vs-outside 0.43, heterogeneity 0.16; core [0.81, 0.591, 0.709] rim [0.561, 0.499, 0.624]
  - track 53 at frame 178: holes 0, rim-vs-core 0.44, rim-vs-outside 0.53, heterogeneity 0.20; core [0.915, 0.731, 0.752] rim [0.637, 0.526, 0.479]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 74 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.794, rim/outside 8.51 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.7)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.807, rim/outside 3.29 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.57)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.78, rim/outside 3.65 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.674)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #31 (t=438, R_eq 11.4): none; #33 (t=438, R_eq 10.93): none; #35 (t=468, R_eq 13.39): none; #53 (t=534, R_eq 15.47): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
