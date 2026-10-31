# Evidence pack: active-nematic-marangoni-noise (seed 0)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.003 per sqrt(t): additive on ['phi', 'q1', 'q2', 's', 'c'], proportional on [], conserved (div of white flux) on []
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 209s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_plain_0.003_s0 --seeds 0 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8304, 0.578], min area 6 px

## Measurements
- components: final 29, mean 17.2, max 29; occupancy final 0.09
- tracks: 57; persistent (alive >= 50% of run): 11; longest 73 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.16 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 30, 27], H1 [0, 0, 0]
- motion: 32 long-lived tracks moved >= 1 body length; max speed 0.395/time; max body lengths 6.0
- replication (lineage window K = 20 frames = time 100, default): splits 22, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 3, merges 3, merge/split ratio 0.136, nucleations 10
- channel total drift (end/start - 1): [-0.5033, -0.3832, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 64: holes 0, rim-vs-core 0.75, rim-vs-outside 0.33, heterogeneity 0.25; core [0.957, 0.641, 0.421, 0.505] rim [0.743, 0.397, 0.9, 0.024]
  - track 12 at frame 64: holes 0, rim-vs-core 1.01, rim-vs-outside 0.41, heterogeneity 0.26; core [0.964, 0.878, 0.338, 0.806] rim [0.765, 0.561, 0.837, 0.011]
  - track 15 at frame 66: holes 0, rim-vs-core 0.74, rim-vs-outside 0.33, heterogeneity 0.22; core [0.96, 0.652, 0.392, 0.505] rim [0.764, 0.42, 0.854, 0.013]
  - track 42 at frame 83: holes 0, rim-vs-core 0.78, rim-vs-outside 0.37, heterogeneity 0.25; core [0.941, 0.756, 0.472, 0.478] rim [0.709, 0.414, 0.943, 0.017]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 118 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 4.43 (aggregate of 118 individuals; 0/118 membrane-like individually; rim level 0.715)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 8.33 (aggregate of 118 individuals; 9/118 membrane-like individually; rim level 0.543)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 3.23 (aggregate of 118 individuals; 56/118 membrane-like individually; rim level 0.569)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.476, rim/outside 2.18 (aggregate of 118 individuals; 20/118 membrane-like individually; rim level 0.161)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=320, R_eq 4.26): none; #12 (t=320, R_eq 3.39): ['surfactant s']; #15 (t=330, R_eq 4.51): none; #42 (t=415, R_eq 3.95): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 118 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
