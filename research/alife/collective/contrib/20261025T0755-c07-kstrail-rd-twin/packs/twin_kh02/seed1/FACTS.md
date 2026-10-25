# Evidence pack: rdtrail_slow (seed 1)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/_c07wip/world_slow.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 28s; status ok
- command: `python -m labkit.run collective/contrib/_c07wip/world_slow.py --out /tmp/claude-0/c07/pk_slow --seeds 0 1 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9945], min area 6 px

## Measurements
- components: final 20, mean 11.2, max 20; occupancy final 0.23
- tracks: 76; persistent (alive >= 50% of run): 3; longest 136 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 94.65 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 20, 20], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.186/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 60, default): splits 31, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 4, merges 8, merge/split ratio 0.258, nucleations 0
- channel total drift (end/start - 1): [5.3655, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 96: holes 0, rim-vs-core 0.48, rim-vs-outside 0.32, heterogeneity 0.19; core [0.862, 0.642, 0.676] rim [0.497, 0.449, 0.428]
  - track 36 at frame 143: holes 0, rim-vs-core 0.35, rim-vs-outside 0.52, heterogeneity 0.18; core [0.886, 0.647, 0.707] rim [0.614, 0.502, 0.542]
  - track 38 at frame 145: holes 0, rim-vs-core 0.46, rim-vs-outside 0.33, heterogeneity 0.17; core [0.842, 0.616, 0.741] rim [0.495, 0.45, 0.493]
  - track 60 at frame 180: holes 0, rim-vs-core 0.53, rim-vs-outside 0.41, heterogeneity 0.19; core [0.908, 0.724, 0.704] rim [0.546, 0.5, 0.396]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 75 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.782, rim/outside 7.77 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.712)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.794, rim/outside 3.24 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.577)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.773, rim/outside 3.55 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.652)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=288, R_eq 13.47): none; #36 (t=429, R_eq 14.87): none; #38 (t=435, R_eq 11.87): none; #60 (t=540, R_eq 15.64): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
