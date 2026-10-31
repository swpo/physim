# Evidence pack: active-nematic-marangoni-noise (seed 0)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.1 per sqrt(t): additive on ['q1', 'q2'], proportional on ['s', 'c'], conserved (div of white flux) on ['phi']
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 225s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_phys_0.1_s0 --seeds 0 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8512, 0.5962], min area 6 px

## Measurements
- components: final 32, mean 24.8, max 34; occupancy final 0.09
- tracks: 93; persistent (alive >= 50% of run): 17; longest 86 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 32, 32], H1 [0, 0, 0]
- motion: 41 long-lived tracks moved >= 1 body length; max speed 0.179/time; max body lengths 6.9
- replication (lineage window K = 20 frames = time 100, default): splits 26, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 17, merge/split ratio 0.654, nucleations 24
- channel total drift (end/start - 1): [-0.5031, 0.327, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 58: holes 0, rim-vs-core 0.69, rim-vs-outside 0.35, heterogeneity 0.21; core [0.9, 0.723, 0.493, 0.522] rim [0.716, 0.549, 0.889, 0.022]
  - track 13 at frame 59: holes 0, rim-vs-core 0.66, rim-vs-outside 0.36, heterogeneity 0.21; core [0.925, 0.77, 0.393, 0.444] rim [0.742, 0.548, 0.804, 0.016]
  - track 14 at frame 59: holes 0, rim-vs-core 0.60, rim-vs-outside 0.28, heterogeneity 0.21; core [0.9, 0.729, 0.485, 0.414] rim [0.731, 0.496, 0.857, 0.042]
  - track 67 at frame 87: holes 0, rim-vs-core 0.74, rim-vs-outside 0.34, heterogeneity 0.24; core [0.963, 0.831, 0.315, 0.394] rim [0.739, 0.467, 0.791, 0.014]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 163 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.802, rim/outside 4.38 (aggregate of 163 individuals; 1/163 membrane-like individually; rim level 0.721)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.752, rim/outside 3.54 (aggregate of 163 individuals; 10/163 membrane-like individually; rim level 0.525)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.4, rim/outside 3.35 (aggregate of 163 individuals; 94/163 membrane-like individually; rim level 0.553)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.396, rim/outside 1.61 (aggregate of 163 individuals; 24/163 membrane-like individually; rim level 0.135)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=290, R_eq 3.66): ['surfactant s']; #13 (t=295, R_eq 4.26): none; #14 (t=295, R_eq 4.15): none; #67 (t=435, R_eq 2.82): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 163 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
