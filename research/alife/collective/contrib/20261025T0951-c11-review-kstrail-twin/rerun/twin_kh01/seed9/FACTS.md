# Evidence pack: rdtrail_slow5 (seed 9)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0755-c07-kstrail-rd-twin/world_slow5.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 20s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0755-c07-kstrail-rd-twin/world_slow5.py --out /tmp/claude-0/c11rev7/twin_kh01 --seeds 9 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9937], min area 6 px

## Measurements
- components: final 8, mean 7.3, max 14; occupancy final 0.13
- tracks: 56; persistent (alive >= 50% of run): 1; longest 110 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.32 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 8, 8], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.24/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 60, default): splits 22, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 5, merge/split ratio 0.227, nucleations 0
- channel total drift (end/start - 1): [2.6584, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 146: holes 0, rim-vs-core 0.39, rim-vs-outside 0.30, heterogeneity 0.18; core [0.825, 0.631, 0.662] rim [0.497, 0.484, 0.52]
  - track 32 at frame 156: holes 0, rim-vs-core 0.49, rim-vs-outside 0.42, heterogeneity 0.20; core [0.914, 0.699, 0.688] rim [0.553, 0.464, 0.453]
  - track 39 at frame 161: holes 0, rim-vs-core 0.30, rim-vs-outside 0.50, heterogeneity 0.20; core [0.86, 0.701, 0.719] rim [0.628, 0.564, 0.585]
  - track 43 at frame 163: holes 0, rim-vs-core 0.44, rim-vs-outside 0.30, heterogeneity 0.19; core [0.859, 0.633, 0.643] rim [0.502, 0.44, 0.47]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 46 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.789, rim/outside 8.39 (aggregate of 46 individuals; 2/46 membrane-like individually; rim level 0.593)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 3.53 (aggregate of 46 individuals; 0/46 membrane-like individually; rim level 0.535)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 2.69 (aggregate of 46 individuals; 0/46 membrane-like individually; rim level 0.657)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #30 (t=438, R_eq 10.98): none; #32 (t=468, R_eq 14.72): none; #39 (t=483, R_eq 14.59): none; #43 (t=489, R_eq 12.93): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 46 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
