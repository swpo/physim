# Evidence pack: swimevo (seed 8)

- world: `../../../../../threads/chemotaxis-motility/worlds/swimevo/world.py`, family `chemotaxis`
- parent: swimfission + active-droplets/ad5-evolve (confined alleles); mutation: split rho into two heritable alleles with own-density cooperative growth (body purification), symmetric patch mutations, allele B grows (1+s) faster
- run: 201 frames x 120 steps x dt 0.05 = time 1200; grid [160, 160]; wall 162s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/swimevo/world.py --out collective/contrib/wip-c33-se/pack --seeds 7 8 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9959], min area 6 px

## Measurements
- components: final 10, mean 14.3, max 32; occupancy final 0.04
- tracks: 190; persistent (alive >= 50% of run): 1; longest 106 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.04 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 50 long-lived tracks moved >= 1 body length; max speed 0.376/time; max body lengths 16.0
- replication (lineage window K = 20 frames = time 120, default): splits 49, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 63, merge/split ratio 1.29, nucleations 38
- channel total drift (end/start - 1): [-0.7756, None, -0.3445, -0.0438]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 126 at frame 148: holes 0, rim-vs-core 0.49, rim-vs-outside 0.38, heterogeneity 0.18; core [0.439, 0.669, 0.621, 0.214] rim [0.235, 0.357, 0.44, 0.467]
  - track 144 at frame 158: holes 0, rim-vs-core 0.42, rim-vs-outside 0.63, heterogeneity 0.15; core [0.0, 1.0, 0.786, 0.034] rim [0.0, 0.74, 0.533, 0.253]
  - track 96 at frame 94: holes 0, rim-vs-core 0.55, rim-vs-outside 0.46, heterogeneity 0.17; core [0.958, 0.0, 0.719, 0.109] rim [0.526, 0.0, 0.497, 0.369]
  - track 169 at frame 175: holes 0, rim-vs-core 0.32, rim-vs-outside 0.70, heterogeneity 0.17; core [0.198, 0.977, 0.766, 0.084] rim [0.146, 0.725, 0.649, 0.226]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 76 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.806, rim/outside 28.9 (aggregate of 76 individuals; 2/76 membrane-like individually; rim level 0.58)
  - radial B: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 17.3 (aggregate of 76 individuals; 1/76 membrane-like individually; rim level 0.24)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.813, rim/outside 5.08 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.656)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.6, rim/outside 0.735 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.622)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #126 (t=888, R_eq 4.58): none; #144 (t=948, R_eq 5.67): none; #96 (t=564, R_eq 5.29): none; #169 (t=1050, R_eq 5.5): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 76 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
