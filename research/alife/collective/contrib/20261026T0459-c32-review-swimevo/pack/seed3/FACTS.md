# Evidence pack: swimevo (seed 3)

- world: `../../world.py`, family `chemotaxis`
- parent: swimfission + active-droplets/ad5-evolve (confined alleles); mutation: split rho into two heritable alleles with own-density cooperative growth (body purification), symmetric patch mutations, allele B grows (1+s) faster
- run: 201 frames x 120 steps x dt 0.05 = time 1200; grid [160, 160]; wall 98s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0459-c32-review-swimevo/world.py --out collective/contrib/20261026T0459-c32-review-swimevo/pack --seeds 3 4 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9962], min area 6 px

## Measurements
- components: final 10, mean 14.9, max 31; occupancy final 0.04
- tracks: 225; persistent (alive >= 50% of run): 1; longest 176 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.90 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 45 long-lived tracks moved >= 1 body length; max speed 0.282/time; max body lengths 23.8
- replication (lineage window K = 20 frames = time 120, default): splits 60, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 74, merge/split ratio 1.23, nucleations 41
- channel total drift (end/start - 1): [-0.9623, None, -0.3361, -0.0448]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 49 at frame 113: holes 0, rim-vs-core 0.53, rim-vs-outside 0.50, heterogeneity 0.17; core [0.0, 0.991, 0.753, 0.051] rim [0.0, 0.576, 0.517, 0.286]
  - track 53 at frame 71: holes 0, rim-vs-core 0.53, rim-vs-outside 0.47, heterogeneity 0.16; core [0.96, 0.0, 0.696, 0.124] rim [0.551, 0.0, 0.478, 0.383]
  - track 177 at frame 158: holes 0, rim-vs-core 0.53, rim-vs-outside 0.51, heterogeneity 0.16; core [0.022, 0.992, 0.746, 0.055] rim [0.012, 0.588, 0.511, 0.296]
  - track 2 at frame 40: holes 0, rim-vs-core 0.48, rim-vs-outside 0.51, heterogeneity 0.16; core [0.97, 0.0, 0.712, 0.112] rim [0.597, 0.0, 0.521, 0.348]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 81 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 27 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.523)
  - radial B: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 19.2 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.274)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.81, rim/outside 5.04 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.659)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 12.7, rim/outside 0.746 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.629)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #49 (t=678, R_eq 5.7): none; #53 (t=426, R_eq 5.14): none; #177 (t=948, R_eq 5.53): none; #2 (t=240, R_eq 5.17): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
