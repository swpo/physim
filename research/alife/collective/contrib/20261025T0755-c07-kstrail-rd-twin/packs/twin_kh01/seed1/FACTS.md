# Evidence pack: rdtrail_slow5 (seed 1)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/_c07wip/world_slow5.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 25s; status ok
- command: `python -m labkit.run collective/contrib/_c07wip/world_slow5.py --out /tmp/claude-0/c07/pk_slow5 --seeds 0 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9936], min area 6 px

## Measurements
- components: final 9, mean 7.2, max 13; occupancy final 0.16
- tracks: 61; persistent (alive >= 50% of run): 1; longest 117 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.31 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 9], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.264/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 60, default): splits 26, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 5, merges 3, merge/split ratio 0.115, nucleations 0
- channel total drift (end/start - 1): [3.2275, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 143: holes 0, rim-vs-core 0.40, rim-vs-outside 0.22, heterogeneity 0.15; core [0.77, 0.537, 0.738] rim [0.454, 0.403, 0.537]
  - track 29 at frame 160: holes 0, rim-vs-core 0.43, rim-vs-outside 0.33, heterogeneity 0.17; core [0.831, 0.582, 0.782] rim [0.504, 0.422, 0.555]
  - track 26 at frame 145: holes 0, rim-vs-core 0.43, rim-vs-outside 0.32, heterogeneity 0.19; core [0.852, 0.623, 0.655] rim [0.504, 0.439, 0.485]
  - track 53 at frame 183: holes 0, rim-vs-core 0.36, rim-vs-outside 0.32, heterogeneity 0.16; core [0.783, 0.574, 0.718] rim [0.493, 0.45, 0.552]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 47 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 8.73 (aggregate of 47 individuals; 3/47 membrane-like individually; rim level 0.59)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.813, rim/outside 3.63 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.535)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.8, rim/outside 2.74 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.666)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #20 (t=429, R_eq 9.89): none; #29 (t=480, R_eq 11.75): none; #26 (t=435, R_eq 12.99): none; #53 (t=549, R_eq 11.89): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 47 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
