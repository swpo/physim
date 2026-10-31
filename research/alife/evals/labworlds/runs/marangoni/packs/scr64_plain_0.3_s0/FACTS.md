# Evidence pack: active-nematic-marangoni-noise (seed 0)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.3 per sqrt(t): additive on ['phi', 'q1', 'q2', 's', 'c'], proportional on [], conserved (div of white flux) on []
- run: 7 frames x 100 steps x dt 0.05 = time 30; grid [64, 64]; wall 4s; status non-finite fields at frame 7
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/scr64_plain_0.3_s0 --seeds 0 --frames 100 --size 64 64 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8941, 0.708], min area 6 px

## Measurements
- components: final 12, mean 9.1, max 14; occupancy final 0.13
- tracks: 33; persistent (alive >= 50% of run): 5; longest 5 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.44 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [3, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 12, 5], H1 [13, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 100, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio 2.5, nucleations 25
- channel total drift (end/start - 1): [-0.1153, 2.6265, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 4: holes 0, rim-vs-core 0.31, rim-vs-outside 0.27, heterogeneity 0.17; core [0.908, 0.398, 0.26, 0.161] rim [0.714, 0.512, 0.458, 0.084]
  - track 14 at frame 5: holes 0, rim-vs-core 0.38, rim-vs-outside 0.18, heterogeneity 0.16; core [0.887, 0.578, 0.497, 0.204] rim [0.719, 0.364, 0.738, 0.079]
  - track 16 at frame 5: holes 0, rim-vs-core 0.47, rim-vs-outside 0.22, heterogeneity 0.20; core [0.932, 0.392, 0.309, 0.352] rim [0.746, 0.497, 0.634, 0.083]
  - track 1 at frame 3: holes 0, rim-vs-core 0.24, rim-vs-outside 0.18, heterogeneity 0.14; core [0.867, 0.405, 0.244, 0.241] rim [0.739, 0.401, 0.385, 0.094]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 52 components >= 12 px at frames [2, 3, 4, 5, 6]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.838, rim/outside 2.37 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.719)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 1.35 (aggregate of 52 individuals; 11/52 membrane-like individually; rim level 0.445)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 1.71 (aggregate of 52 individuals; 25/52 membrane-like individually; rim level 0.494)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.718, rim/outside 0.741 (aggregate of 52 individuals; 5/52 membrane-like individually; rim level 0.178)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=20, R_eq 3.14): ['surfactant s']; #14 (t=25, R_eq 2.88): ['cargo c']; #16 (t=25, R_eq 3.61): ['surfactant s']; #1 (t=15, R_eq 2.33): ['order |Q|', 'surfactant s']

## Warnings
- RUN FAILED: non-finite fields at frame 7 (only 7 frames analysed)
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- fewer than 30 recorded frames: tracking statistics are weak
- lineage window K=20 frames is more than half the run: late splits cannot count as persistent
- radial: 2 of 52 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
