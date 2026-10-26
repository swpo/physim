# Evidence pack: swimevo (seed 7)

- world: `../../../../../threads/chemotaxis-motility/worlds/swimevo/world.py`, family `chemotaxis`
- parent: swimfission + active-droplets/ad5-evolve (confined alleles); mutation: split rho into two heritable alleles with own-density cooperative growth (body purification), symmetric patch mutations, allele B grows (1+s) faster
- run: 201 frames x 120 steps x dt 0.05 = time 1200; grid [160, 160]; wall 161s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/swimevo/world.py --out collective/contrib/wip-c33-se/pack --seeds 7 8 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.996], min area 6 px

## Measurements
- components: final 10, mean 14.6, max 30; occupancy final 0.04
- tracks: 191; persistent (alive >= 50% of run): 0; longest 81 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 55 long-lived tracks moved >= 1 body length; max speed 0.335/time; max body lengths 12.8
- replication (lineage window K = 20 frames = time 120, default): splits 48, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 3, merges 62, merge/split ratio 1.29, nucleations 36
- channel total drift (end/start - 1): [-0.5293, None, -0.206, -0.0519]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 45: holes 0, rim-vs-core 0.54, rim-vs-outside 0.46, heterogeneity 0.16; core [0.954, 0.0, 0.779, 0.084] rim [0.518, 0.0, 0.564, 0.32]
  - track 46 at frame 62: holes 0, rim-vs-core 0.53, rim-vs-outside 0.42, heterogeneity 0.16; core [0.943, 0.0, 0.622, 0.15] rim [0.513, 0.0, 0.439, 0.4]
  - track 150 at frame 166: holes 0, rim-vs-core 0.50, rim-vs-outside 0.47, heterogeneity 0.19; core [0.806, 0.482, 0.709, 0.157] rim [0.475, 0.287, 0.503, 0.404]
  - track 156 at frame 171: holes 0, rim-vs-core 0.50, rim-vs-outside 0.60, heterogeneity 0.20; core [0.59, 0.996, 0.694, 0.167] rim [0.347, 0.657, 0.532, 0.395]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 83 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.802, rim/outside 35.1 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.68)
  - radial B: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.862, rim/outside 15.5 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.174)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 5.03 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.654)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.9, rim/outside 0.742 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.627)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=270, R_eq 5.32): none; #46 (t=372, R_eq 4.55): none; #150 (t=996, R_eq 4.92): none; #156 (t=1026, R_eq 4.79): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
