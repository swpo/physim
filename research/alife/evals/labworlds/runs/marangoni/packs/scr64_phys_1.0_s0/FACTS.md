# Evidence pack: active-nematic-marangoni-noise (seed 0)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 1.0 per sqrt(t): additive on ['q1', 'q2'], proportional on ['s', 'c'], conserved (div of white flux) on ['phi']
- run: 5 frames x 100 steps x dt 0.05 = time 20; grid [64, 64]; wall 3s; status non-finite fields at frame 5
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/scr64_phys_1.0_s0 --seeds 0 --frames 100 --size 64 64 --no-movie`
- segmentation: matter > 0.61 of robust range [-1.015, 0.6497], min area 6 px

## Measurements
- components: final 19, mean 15.2, max 20; occupancy final 0.06
- tracks: 43; persistent (alive >= 50% of run): 11; longest 4 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [36, 4, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [56, 20, 2], H1 [44, 6, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 100, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 43
- channel total drift (end/start - 1): [-0.1041, 8.0084, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 3: holes 0, rim-vs-core 0.27, rim-vs-outside 0.32, heterogeneity 0.21; core [0.978, 0.577, 0.298, 0.41] rim [0.845, 0.466, 0.371, 0.599]
  - track 8 at frame 3: holes 0, rim-vs-core 0.31, rim-vs-outside 0.35, heterogeneity 0.21; core [0.998, 0.459, 0.272, 0.446] rim [0.859, 0.44, 0.491, 0.272]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 32 components >= 12 px at frames [1, 2, 3, 4]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.865, rim/outside 2.09 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.767)
  - radial order |Q|: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 1.25 (aggregate of 32 individuals; 12/32 membrane-like individually; rim level 0.496)
  - radial surfactant s: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.27, rim/outside 2.18 (aggregate of 32 individuals; 20/32 membrane-like individually; rim level 0.242)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.737, rim/outside 1.21 (aggregate of 32 individuals; 5/32 membrane-like individually; rim level 0.326)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=15, R_eq 2.71): ['surfactant s']; #2 (t=15, R_eq 1.69): ['surfactant s']; #6 (t=15, R_eq 1.6): none; #8 (t=15, R_eq 2.65): ['order |Q|', 'surfactant s']

## Warnings
- RUN FAILED: non-finite fields at frame 5 (only 5 frames analysed)
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- fewer than 30 recorded frames: tracking statistics are weak
- lineage window K=20 frames is more than half the run: late splits cannot count as persistent
- radial: 2 of 32 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
