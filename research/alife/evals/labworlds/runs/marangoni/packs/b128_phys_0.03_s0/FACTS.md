# Evidence pack: active-nematic-marangoni-noise (seed 0)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.03 per sqrt(t): additive on ['q1', 'q2'], proportional on ['s', 'c'], conserved (div of white flux) on ['phi']
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 213s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_phys_0.03_s0 --seeds 0 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8343, 0.566], min area 6 px

## Measurements
- components: final 30, mean 16.6, max 30; occupancy final 0.09
- tracks: 64; persistent (alive >= 50% of run): 9; longest 64 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 31, 29], H1 [0, 0, 0]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.425/time; max body lengths 8.8
- replication (lineage window K = 20 frames = time 100, default): splits 24, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 2, merges 5, merge/split ratio 0.208, nucleations 11
- channel total drift (end/start - 1): [-0.5031, -0.2493, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 69: holes 0, rim-vs-core 0.90, rim-vs-outside 0.38, heterogeneity 0.25; core [0.969, 0.913, 0.362, 0.649] rim [0.77, 0.53, 0.844, 0.027]
  - track 19 at frame 69: holes 0, rim-vs-core 0.89, rim-vs-outside 0.36, heterogeneity 0.24; core [0.962, 0.85, 0.414, 0.68] rim [0.764, 0.545, 0.9, 0.031]
  - track 21 at frame 71: holes 0, rim-vs-core 0.62, rim-vs-outside 0.30, heterogeneity 0.24; core [0.925, 0.49, 0.509, 0.397] rim [0.736, 0.291, 0.911, 0.017]
  - track 36 at frame 81: holes 0, rim-vs-core 0.75, rim-vs-outside 0.38, heterogeneity 0.22; core [0.959, 0.878, 0.374, 0.573] rim [0.777, 0.578, 0.761, 0.034]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 115 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.8, rim/outside 4.49 (aggregate of 115 individuals; 0/115 membrane-like individually; rim level 0.724)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.762, rim/outside 7.13 (aggregate of 115 individuals; 5/115 membrane-like individually; rim level 0.573)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.3, rim/outside 3.33 (aggregate of 115 individuals; 62/115 membrane-like individually; rim level 0.587)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.369, rim/outside 1.86 (aggregate of 115 individuals; 11/115 membrane-like individually; rim level 0.146)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=345, R_eq 3.48): ['surfactant s']; #19 (t=345, R_eq 3.78): ['surfactant s']; #21 (t=355, R_eq 4.51): ['cargo c']; #36 (t=405, R_eq 3.78): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 115 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
