# Evidence pack: rdtrail_slow5 (seed 2)

- world: `../../../../home/user/physim/research/alife/collective/contrib/_c07wip/world_slow5.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 25s; status ok
- command: `python -m labkit.run collective/contrib/_c07wip/world_slow5.py --out /tmp/claude-0/c07/pk_slow5b --seeds 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9942], min area 6 px

## Measurements
- components: final 10, mean 5.8, max 11; occupancy final 0.15
- tracks: 49; persistent (alive >= 50% of run): 1; longest 111 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.15 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 13, 9], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.211/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 60, default): splits 20, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 4, merges 3, merge/split ratio 0.15, nucleations 0
- channel total drift (end/start - 1): [3.073, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 27 at frame 146: holes 0, rim-vs-core 0.36, rim-vs-outside 0.40, heterogeneity 0.17; core [0.845, 0.654, 0.638] rim [0.546, 0.501, 0.512]
  - track 33 at frame 163: holes 0, rim-vs-core 0.38, rim-vs-outside 0.31, heterogeneity 0.17; core [0.82, 0.584, 0.676] rim [0.501, 0.447, 0.529]
  - track 36 at frame 170: holes 0, rim-vs-core 0.34, rim-vs-outside 0.44, heterogeneity 0.18; core [0.854, 0.673, 0.673] rim [0.595, 0.536, 0.506]
  - track 39 at frame 176: holes 0, rim-vs-core 0.42, rim-vs-outside 0.41, heterogeneity 0.19; core [0.877, 0.671, 0.675] rim [0.55, 0.482, 0.498]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 38 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 7.62 (aggregate of 38 individuals; 4/38 membrane-like individually; rim level 0.555)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 3.46 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.519)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.797, rim/outside 2.78 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.64)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #27 (t=438, R_eq 17.99): none; #33 (t=489, R_eq 10.25): none; #36 (t=510, R_eq 16.74): none; #39 (t=528, R_eq 15.65): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 38 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
