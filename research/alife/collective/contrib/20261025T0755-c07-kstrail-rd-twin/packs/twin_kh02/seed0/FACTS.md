# Evidence pack: rdtrail_slow (seed 0)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/_c07wip/world_slow.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 27s; status ok
- command: `python -m labkit.run collective/contrib/_c07wip/world_slow.py --out /tmp/claude-0/c07/pk_slow --seeds 0 1 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9951], min area 6 px

## Measurements
- components: final 18, mean 8.7, max 19; occupancy final 0.23
- tracks: 68; persistent (alive >= 50% of run): 2; longest 125 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.42 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 19, 17], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.184/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 60, default): splits 28, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 4, merges 5, merge/split ratio 0.179, nucleations 0
- channel total drift (end/start - 1): [5.3065, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 96: holes 0, rim-vs-core 0.57, rim-vs-outside 0.49, heterogeneity 0.20; core [0.946, 0.738, 0.645] rim [0.591, 0.457, 0.308]
  - track 25 at frame 129: holes 0, rim-vs-core 0.46, rim-vs-outside 0.32, heterogeneity 0.19; core [0.862, 0.649, 0.671] rim [0.499, 0.447, 0.463]
  - track 31 at frame 156: holes 0, rim-vs-core 0.50, rim-vs-outside 0.34, heterogeneity 0.17; core [0.84, 0.586, 0.796] rim [0.49, 0.408, 0.484]
  - track 44 at frame 180: holes 0, rim-vs-core 0.28, rim-vs-outside 0.64, heterogeneity 0.19; core [0.882, 0.644, 0.693] rim [0.679, 0.542, 0.537]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 59 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.811, rim/outside 7.04 (aggregate of 59 individuals; 2/59 membrane-like individually; rim level 0.676)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 3.08 (aggregate of 59 individuals; 1/59 membrane-like individually; rim level 0.561)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 3.49 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.652)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #17 (t=288, R_eq 18.33): none; #25 (t=387, R_eq 13.9): none; #31 (t=468, R_eq 12.32): none; #44 (t=540, R_eq 15.07): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 59 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
