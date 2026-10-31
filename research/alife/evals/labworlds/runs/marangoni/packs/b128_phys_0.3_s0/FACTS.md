# Evidence pack: active-nematic-marangoni-noise (seed 0)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.3 per sqrt(t): additive on ['q1', 'q2'], proportional on ['s', 'c'], conserved (div of white flux) on ['phi']
- run: 62 frames x 100 steps x dt 0.05 = time 305; grid [128, 128]; wall 130s; status non-finite fields at frame 62
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_phys_0.3_s0 --seeds 0 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.8874, 0.7251], min area 6 px

## Measurements
- components: final 30, mean 33.9, max 44; occupancy final 0.07
- tracks: 201; persistent (alive >= 50% of run): 18; longest 59 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 29, 26], H1 [15, 0, 0]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.244/time; max body lengths 9.8
- replication (lineage window K = 20 frames = time 100, default): splits 43, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 33, merge/split ratio 0.767, nucleations 85
- channel total drift (end/start - 1): [-0.4914, 2.0073, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 32: holes 0, rim-vs-core 0.65, rim-vs-outside 0.26, heterogeneity 0.25; core [0.897, 0.747, 0.293, 0.474] rim [0.7, 0.529, 0.697, 0.054]
  - track 18 at frame 34: holes 0, rim-vs-core 0.71, rim-vs-outside 0.26, heterogeneity 0.26; core [0.922, 0.529, 0.308, 0.487] rim [0.714, 0.4, 0.815, 0.05]
  - track 20 at frame 34: holes 0, rim-vs-core 0.61, rim-vs-outside 0.29, heterogeneity 0.21; core [0.84, 0.768, 0.251, 0.594] rim [0.704, 0.54, 0.465, 0.087]
  - track 89 at frame 39: holes 0, rim-vs-core 0.64, rim-vs-outside 0.34, heterogeneity 0.23; core [0.928, 0.808, 0.221, 0.497] rim [0.721, 0.633, 0.593, 0.051]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 210 components >= 12 px at frames [10, 20, 30, 41, 51, 61]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.824, rim/outside 3.75 (aggregate of 210 individuals; 0/210 membrane-like individually; rim level 0.756)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.802, rim/outside 1.54 (aggregate of 210 individuals; 34/210 membrane-like individually; rim level 0.473)
  - radial surfactant s: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.93, rim/outside 3.29 (aggregate of 210 individuals; 164/210 membrane-like individually; rim level 0.444)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.33, rim/outside 0.838 (aggregate of 210 individuals; 7/210 membrane-like individually; rim level 0.153)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #2 (t=160, R_eq 3.99): ['surfactant s']; #18 (t=170, R_eq 3.39): ['surfactant s']; #20 (t=170, R_eq 3.52): none; #89 (t=195, R_eq 3.39): ['surfactant s']

## Warnings
- RUN FAILED: non-finite fields at frame 62 (only 62 frames analysed)
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 210 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
