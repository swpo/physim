# Evidence pack: rdtrail (seed 0)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/_c07wip/world.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 27s; status ok
- command: `python -m labkit.run collective/contrib/_c07wip/world.py --out /tmp/claude-0/c07/pk_matched --seeds 0 1 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9934], min area 6 px

## Measurements
- components: final 18, mean 9.4, max 18; occupancy final 0.25
- tracks: 52; persistent (alive >= 50% of run): 1; longest 103 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.53 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 19, 18], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.133/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 60, default): splits 21, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 4, merges 4, merge/split ratio 0.19, nucleations 0
- channel total drift (end/start - 1): [5.8772, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 150: holes 0, rim-vs-core 0.55, rim-vs-outside 0.52, heterogeneity 0.20; core [0.921, 0.808, 0.867] rim [0.572, 0.545, 0.532]
  - track 26 at frame 156: holes 0, rim-vs-core 0.30, rim-vs-outside 0.49, heterogeneity 0.15; core [0.808, 0.659, 0.871] rim [0.581, 0.556, 0.707]
  - track 27 at frame 156: holes 0, rim-vs-core 0.49, rim-vs-outside 0.46, heterogeneity 0.17; core [0.879, 0.721, 0.866] rim [0.536, 0.51, 0.579]
  - track 39 at frame 180: holes 0, rim-vs-core 0.58, rim-vs-outside 0.45, heterogeneity 0.19; core [0.906, 0.767, 0.827] rim [0.536, 0.521, 0.447]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 66 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 8.46 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.713)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.795, rim/outside 3.41 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.594)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.762, rim/outside 5.85 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.682)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #25 (t=450, R_eq 18.28): none; #26 (t=468, R_eq 13.11): none; #27 (t=468, R_eq 14.57): none; #39 (t=540, R_eq 16.35): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
