# Evidence pack: active-nematic-marangoni-noise (seed 1)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.003 per sqrt(t): additive on ['q1', 'q2'], proportional on ['s', 'c'], conserved (div of white flux) on ['phi']
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 215s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_phys_0.003_s1 --seeds 1 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8107, 0.5452], min area 6 px

## Measurements
- components: final 23, mean 9.9, max 23; occupancy final 0.07
- tracks: 52; persistent (alive >= 50% of run): 0; longest 48 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 25, 21], H1 [0, 0, 0]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.264/time; max body lengths 4.0
- replication (lineage window K = 20 frames = time 100, default): splits 23, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 4, merges 3, merge/split ratio 0.13, nucleations 3
- channel total drift (end/start - 1): [-0.4915, -0.5011, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 68: holes 0, rim-vs-core 0.75, rim-vs-outside 0.31, heterogeneity 0.25; core [0.97, 0.611, 0.453, 0.514] rim [0.764, 0.37, 0.929, 0.027]
  - track 7 at frame 61: holes 0, rim-vs-core 0.73, rim-vs-outside 0.31, heterogeneity 0.23; core [0.936, 0.745, 0.48, 0.546] rim [0.743, 0.437, 0.85, 0.029]
  - track 18 at frame 79: holes 0, rim-vs-core 0.74, rim-vs-outside 0.33, heterogeneity 0.24; core [0.962, 0.639, 0.475, 0.59] rim [0.768, 0.429, 0.897, 0.053]
  - track 25 at frame 87: holes 0, rim-vs-core 0.85, rim-vs-outside 0.43, heterogeneity 0.23; core [0.965, 0.933, 0.402, 0.717] rim [0.766, 0.66, 0.782, 0.03]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 71 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.789, rim/outside 4.5 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.715)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.775, rim/outside 8.16 (aggregate of 71 individuals; 1/71 membrane-like individually; rim level 0.605)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.27, rim/outside 3.23 (aggregate of 71 individuals; 32/71 membrane-like individually; rim level 0.641)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.421, rim/outside 1.92 (aggregate of 71 individuals; 6/71 membrane-like individually; rim level 0.208)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=340, R_eq 4.18): none; #7 (t=305, R_eq 4.62, ring): ['order |Q|', 'cargo c']; #18 (t=395, R_eq 4.55): ['order |Q|']; #25 (t=435, R_eq 4.11): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 71 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
