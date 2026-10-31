# Evidence pack: active-nematic-marangoni-noise (seed 2)

- world: `../../../marangoni/mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.0 per sqrt(t): additive on ['phi', 'q1', 'q2', 's', 'c'], proportional on [], conserved (div of white flux) on []
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 184s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni_review/packs/b128_base_0_s2 --seeds 2 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8328, 0.5662], min area 6 px

## Measurements
- components: final 26, mean 16.8, max 28; occupancy final 0.09
- tracks: 63; persistent (alive >= 50% of run): 6; longest 78 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 28, 26], H1 [0, 0, 0]
- motion: 35 long-lived tracks moved >= 1 body length; max speed 0.249/time; max body lengths 8.2
- replication (lineage window K = 20 frames = time 100, default): splits 24, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 3, merges 5, merge/split ratio 0.208, nucleations 10
- channel total drift (end/start - 1): [-0.5093, -0.4413, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 62: holes 0, rim-vs-core 0.57, rim-vs-outside 0.30, heterogeneity 0.20; core [0.913, 0.74, 0.45, 0.437] rim [0.737, 0.489, 0.737, 0.046]
  - track 12 at frame 63: holes 0, rim-vs-core 0.79, rim-vs-outside 0.40, heterogeneity 0.24; core [0.944, 0.938, 0.47, 0.581] rim [0.75, 0.654, 0.927, 0.034]
  - track 19 at frame 67: holes 0, rim-vs-core 0.49, rim-vs-outside 0.37, heterogeneity 0.19; core [0.911, 0.687, 0.433, 0.42] rim [0.777, 0.526, 0.711, 0.069]
  - track 36 at frame 78: holes 0, rim-vs-core 0.72, rim-vs-outside 0.37, heterogeneity 0.23; core [0.951, 0.916, 0.373, 0.476] rim [0.74, 0.563, 0.757, 0.022]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 114 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 4.33 (aggregate of 114 individuals; 0/114 membrane-like individually; rim level 0.714)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.775, rim/outside 8.44 (aggregate of 114 individuals; 7/114 membrane-like individually; rim level 0.559)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 3.19 (aggregate of 114 individuals; 50/114 membrane-like individually; rim level 0.573)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.432, rim/outside 2.09 (aggregate of 114 individuals; 12/114 membrane-like individually; rim level 0.158)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=310, R_eq 3.87): none; #12 (t=315, R_eq 4.51): none; #19 (t=335, R_eq 4.26): ['cargo c']; #36 (t=390, R_eq 3.7): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 114 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
