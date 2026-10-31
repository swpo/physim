# Evidence pack: active-nematic-marangoni-noise (seed 1)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.1 per sqrt(t): additive on ['phi', 'q1', 'q2', 's', 'c'], proportional on [], conserved (div of white flux) on []
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 202s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_plain_0.1_s1 --seeds 1 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8461, 0.5905], min area 6 px

## Measurements
- components: final 23, mean 26.9, max 36; occupancy final 0.06
- tracks: 167; persistent (alive >= 50% of run): 11; longest 94 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 23, 21], H1 [1, 0, 0]
- motion: 51 long-lived tracks moved >= 1 body length; max speed 0.587/time; max body lengths 14.9
- replication (lineage window K = 20 frames = time 100, default): splits 37, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 26, merge/split ratio 0.703, nucleations 70
- channel total drift (end/start - 1): [-0.5156, 0.1499, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 54: holes 0, rim-vs-core 0.51, rim-vs-outside 0.25, heterogeneity 0.19; core [0.87, 0.585, 0.529, 0.453] rim [0.72, 0.467, 0.784, 0.052]
  - track 24 at frame 55: holes 0, rim-vs-core 0.41, rim-vs-outside 0.24, heterogeneity 0.17; core [0.876, 0.403, 0.449, 0.324] rim [0.731, 0.38, 0.707, 0.047]
  - track 33 at frame 57: holes 0, rim-vs-core 0.54, rim-vs-outside 0.37, heterogeneity 0.18; core [0.9, 0.902, 0.382, 0.351] rim [0.739, 0.687, 0.719, 0.023]
  - track 72 at frame 55: holes 0, rim-vs-core 0.51, rim-vs-outside 0.33, heterogeneity 0.17; core [0.848, 0.877, 0.593, 0.384] rim [0.73, 0.666, 0.912, 0.063]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 171 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.823, rim/outside 3.87 (aggregate of 171 individuals; 0/171 membrane-like individually; rim level 0.731)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.756, rim/outside 3.01 (aggregate of 171 individuals; 18/171 membrane-like individually; rim level 0.497)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.29, rim/outside 2.42 (aggregate of 171 individuals; 79/171 membrane-like individually; rim level 0.574)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.533, rim/outside 0.757 (aggregate of 171 individuals; 24/171 membrane-like individually; rim level 0.14)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=270, R_eq 2.59): ['surfactant s']; #24 (t=275, R_eq 3.83): ['cargo c']; #33 (t=285, R_eq 3.83): ['cargo c']; #72 (t=275, R_eq 3.52): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 171 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
