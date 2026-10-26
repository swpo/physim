# Evidence pack: swimevo (seed 4)

- world: `../../world.py`, family `chemotaxis`
- parent: swimfission + active-droplets/ad5-evolve (confined alleles); mutation: split rho into two heritable alleles with own-density cooperative growth (body purification), symmetric patch mutations, allele B grows (1+s) faster
- run: 201 frames x 120 steps x dt 0.05 = time 1200; grid [160, 160]; wall 98s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0459-c32-review-swimevo/world.py --out collective/contrib/20261026T0459-c32-review-swimevo/pack --seeds 3 4 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9958], min area 6 px

## Measurements
- components: final 12, mean 15.9, max 32; occupancy final 0.04
- tracks: 204; persistent (alive >= 50% of run): 2; longest 138 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.84 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 49 long-lived tracks moved >= 1 body length; max speed 0.321/time; max body lengths 20.5
- replication (lineage window K = 20 frames = time 120, default): splits 50, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 3, merges 65, merge/split ratio 1.3, nucleations 43
- channel total drift (end/start - 1): [-0.3744, None, -0.2584, -0.0476]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 106 at frame 133: holes 0, rim-vs-core 0.40, rim-vs-outside 0.83, heterogeneity 0.16; core [0.988, 0.009, 0.902, 0.019] rim [0.746, 0.008, 0.649, 0.208]
  - track 0 at frame 57: holes 0, rim-vs-core 0.55, rim-vs-outside 0.47, heterogeneity 0.17; core [0.957, 0.0, 0.718, 0.112] rim [0.526, 0.0, 0.499, 0.371]
  - track 156 at frame 160: holes 0, rim-vs-core 0.52, rim-vs-outside 0.49, heterogeneity 0.17; core [0.959, 0.0, 0.714, 0.113] rim [0.549, 0.0, 0.51, 0.361]
  - track 183 at frame 176: holes 0, rim-vs-core 0.53, rim-vs-outside 0.47, heterogeneity 0.17; core [0.959, 0.0, 0.72, 0.109] rim [0.545, 0.0, 0.506, 0.361]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 94 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 34.1 (aggregate of 94 individuals; 1/94 membrane-like individually; rim level 0.733)
  - radial B: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.937, rim/outside 11.4 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.128)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 5.28 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.64)
  - radial n: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 11.5, rim/outside 0.751 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.642)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #106 (t=798, R_eq 6.58): none; #0 (t=342, R_eq 5.29): none; #156 (t=960, R_eq 5.26): none; #183 (t=1056, R_eq 5.23): none

## Warnings
- radial: 1 of 94 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
