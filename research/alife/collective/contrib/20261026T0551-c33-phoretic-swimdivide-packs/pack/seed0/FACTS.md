# Evidence pack: phoretic-colloids (seed 0)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 1601 frames x 1 steps x dt 0.5 = time 800; grid [128, 128]; wall 241s; status ok
- command: `python -m labkit.run collective/contrib/wip-c33-sdfix/world.py --out collective/contrib/wip-c33-sdfix/pack --seeds 0 2 --frames 1600 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5827], min area 6 px

## Measurements
- components: final 17, mean 16.9, max 26; occupancy final 0.06
- tracks: 663; persistent (alive >= 50% of run): 0; longest 576 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 19, 14], H1 [0, 0, 0]
- motion: 137 long-lived tracks moved >= 1 body length; max speed 0.599/time; max body lengths 9.3
- replication (lineage window K = 20 frames = time 10, default): splits 80, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 10, merges 93, merge/split ratio 1.16, nucleations 410
- channel total drift (end/start - 1): [0.4871, 0.26, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 213 at frame 645: holes 0, rim-vs-core 0.23, rim-vs-outside 0.27, heterogeneity 0.15; core [0.7, 0.415, 0.491] rim [0.561, 0.241, 0.422]
  - track 18 at frame 350: holes 0, rim-vs-core 0.18, rim-vs-outside 0.27, heterogeneity 0.05; core [0.835, 0.0, 0.388] rim [0.658, 0.0, 0.34]
  - track 308 at frame 847: holes 0, rim-vs-core 0.32, rim-vs-outside 0.32, heterogeneity 0.15; core [0.898, 0.06, 0.645] rim [0.614, 0.112, 0.51]
  - track 634 at frame 1573: holes 0, rim-vs-core 0.42, rim-vs-outside 0.33, heterogeneity 0.23; core [0.551, 0.651, 0.649] rim [0.576, 0.248, 0.542]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 90 components >= 12 px at frames [269, 538, 807, 1062, 1331, 1600]):
  - radial A density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.824, rim/outside 15 (aggregate of 90 individuals; 5/90 membrane-like individually; rim level 0.613)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 15.4 (aggregate of 90 individuals; 30/90 membrane-like individually; rim level 0.362)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 2.8 (aggregate of 90 individuals; 0/90 membrane-like individually; rim level 0.572)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #213 (t=322.5, R_eq 3.04): none; #18 (t=175, R_eq 2.39): none; #308 (t=423.5, R_eq 4.03): ['B density']; #634 (t=786.5, R_eq 4.41): none

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
