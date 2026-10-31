# Evidence pack: active-nematic-marangoni-noise (seed 2)

- world: `../../../marangoni/mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.01 per sqrt(t): additive on ['q1', 'q2'], proportional on ['s', 'c'], conserved (div of white flux) on ['phi']
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 203s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni_review/packs/b128_phys_0.01_s2 --seeds 2 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.832, 0.5706], min area 6 px

## Measurements
- components: final 30, mean 17.7, max 30; occupancy final 0.09
- tracks: 71; persistent (alive >= 50% of run): 10; longest 77 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 30, 28], H1 [0, 0, 0]
- motion: 30 long-lived tracks moved >= 1 body length; max speed 0.259/time; max body lengths 5.6
- replication (lineage window K = 20 frames = time 100, default): splits 28, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 3, merges 6, merge/split ratio 0.214, nucleations 9
- channel total drift (end/start - 1): [-0.5093, -0.3834, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 62: holes 0, rim-vs-core 0.70, rim-vs-outside 0.36, heterogeneity 0.22; core [0.934, 0.743, 0.455, 0.478] rim [0.744, 0.507, 0.889, 0.017]
  - track 15 at frame 64: holes 0, rim-vs-core 0.76, rim-vs-outside 0.36, heterogeneity 0.24; core [0.948, 0.793, 0.464, 0.507] rim [0.746, 0.517, 0.943, 0.025]
  - track 19 at frame 70: holes 0, rim-vs-core 0.93, rim-vs-outside 0.42, heterogeneity 0.29; core [0.993, 0.954, 0.298, 0.558] rim [0.783, 0.584, 0.937, 0.029]
  - track 38 at frame 74: holes 0, rim-vs-core 0.74, rim-vs-outside 0.38, heterogeneity 0.23; core [0.964, 0.899, 0.305, 0.51] rim [0.772, 0.577, 0.707, 0.021]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 123 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 4.42 (aggregate of 123 individuals; 0/123 membrane-like individually; rim level 0.722)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 8.18 (aggregate of 123 individuals; 12/123 membrane-like individually; rim level 0.553)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 3.16 (aggregate of 123 individuals; 58/123 membrane-like individually; rim level 0.567)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.493, rim/outside 2.25 (aggregate of 123 individuals; 21/123 membrane-like individually; rim level 0.172)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=310, R_eq 4.79): none; #15 (t=320, R_eq 4.89): ['cargo c']; #19 (t=350, R_eq 4.41): ['surfactant s']; #38 (t=370, R_eq 3.24): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 123 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
