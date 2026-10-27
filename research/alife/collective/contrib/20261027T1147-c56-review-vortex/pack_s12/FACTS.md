# Evidence pack: fed-vortices (seed 12)

- world: `../../../collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1001 frames x 150 steps x dt 0.02 = time 3000; grid [128, 128]; wall 324s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py --out c56work/vx/pack_s12 --seeds 12 --frames 1000 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2056], min area 6 px

## Measurements
- components: final 28, mean 31.7, max 36; occupancy final 0.13
- tracks: 208; persistent (alive >= 50% of run): 20; longest 1001 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 6.97 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 29], H1 [0, 0, 0]
- motion: 119 long-lived tracks moved >= 1 body length; max speed 0.329/time; max body lengths 33.6
- replication (lineage window K = 20 frames = time 60, default): splits 61, persistent splits 32 (0 more failed only because the siblings re-merged within K), max generation 7, merges 51, merge/split ratio 0.836, nucleations 0
- channel total drift (end/start - 1): [-0.5725, 0.1824, 197231.2656, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 504: holes 0, rim-vs-core 0.71, rim-vs-outside 0.31, heterogeneity 0.19; core [0.8, 0.14, 0.066, 0.7] rim [0.416, 0.311, 0.26, 0.155]
  - track 28 at frame 504: holes 0, rim-vs-core 0.48, rim-vs-outside 0.56, heterogeneity 0.20; core [0.814, 0.122, 0.061, 0.684] rim [0.547, 0.256, 0.196, 0.337]
  - track 46 at frame 504: holes 0, rim-vs-core 0.79, rim-vs-outside 0.31, heterogeneity 0.20; core [0.83, 0.138, 0.922, 0.754] rim [0.414, 0.318, 0.705, 0.145]
  - track 190 at frame 966: holes 0, rim-vs-core 0.78, rim-vs-outside 0.29, heterogeneity 0.20; core [0.818, 0.121, 0.917, 0.696] rim [0.388, 0.336, 0.692, 0.124]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 185 components >= 12 px at frames [168, 336, 504, 664, 832, 1000]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.772, rim/outside 19.5 (aggregate of 185 individuals; 2/185 membrane-like individually; rim level 0.703)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 13.7, rim/outside 0.774 (aggregate of 185 individuals; 0/185 membrane-like individually; rim level 0.489)
  - radial vorticity (signed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.945, rim/outside 1.07 (aggregate of 185 individuals; 0/185 membrane-like individually; rim level 0.52)
  - radial eating: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.726, rim/outside 33.8 (aggregate of 185 individuals; 6/185 membrane-like individually; rim level 0.559)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=1512, R_eq 4.11): none; #28 (t=1512, R_eq 4.62): none; #46 (t=1512, R_eq 4.11): none; #190 (t=2898, R_eq 4.62): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
