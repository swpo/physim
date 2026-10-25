# Evidence pack: rdtrail_slow5 (seed 0)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/_c07wip/world_slow5.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 26s; status ok
- command: `python -m labkit.run collective/contrib/_c07wip/world_slow5.py --out /tmp/claude-0/c07/pk_slow5 --seeds 0 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9942], min area 6 px

## Measurements
- components: final 8, mean 5.3, max 10; occupancy final 0.08
- tracks: 48; persistent (alive >= 50% of run): 0; longest 82 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 8, 7], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.223/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 60, default): splits 20, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.1, nucleations 0
- channel total drift (end/start - 1): [1.2734, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 31 at frame 160: holes 0, rim-vs-core 0.35, rim-vs-outside 0.39, heterogeneity 0.18; core [0.844, 0.645, 0.638] rim [0.552, 0.5, 0.51]
  - track 30 at frame 156: holes 0, rim-vs-core 0.33, rim-vs-outside 0.49, heterogeneity 0.17; core [0.885, 0.651, 0.648] rim [0.602, 0.52, 0.543]
  - track 36 at frame 170: holes 0, rim-vs-core 0.42, rim-vs-outside 0.33, heterogeneity 0.18; core [0.852, 0.627, 0.672] rim [0.52, 0.461, 0.476]
  - track 38 at frame 175: holes 0, rim-vs-core 0.42, rim-vs-outside 0.41, heterogeneity 0.19; core [0.875, 0.686, 0.702] rim [0.548, 0.491, 0.521]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 6.73 (aggregate of 35 individuals; 3/35 membrane-like individually; rim level 0.524)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.843, rim/outside 2.96 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.501)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.806, rim/outside 2.53 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.653)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #31 (t=480, R_eq 17.71): none; #30 (t=468, R_eq 20.3): none; #36 (t=510, R_eq 11.28): none; #38 (t=525, R_eq 15.81): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 35 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
