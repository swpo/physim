# Evidence pack: phase-membrane-noise (seed 0)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: additive dynamics noise sd 0.03 per sqrt(t) on ['S', 'K', 'L', 'phi']
- run: 2 frames x 50 steps x dt 1.0 = time 50; grid [128, 128]; wall 0s; status non-finite fields at frame 2
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/noise_0.03_s0 --seeds 0 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0669, 2.0639], min area 6 px

## Measurements
- components: final 4, mean 13.5, max 23; occupancy final 0.89
- tracks: 27; persistent (alive >= 50% of run): 27; longest 1 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.00 (1 = constant size)
- enclosures: components with a hole mean 1.00, final 1; holes at thresholds 0.2/0.35/0.5 final [5, 78, 26]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [139, 40, 1], H1 [157, 60, 3]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 1000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 3
- channel total drift (end/start - 1): [-0.468, -0.2954, 4.6941, 1.407]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 1: holes 0, rim-vs-core 0.28, rim-vs-outside 0.33, heterogeneity 0.16; core [0.485, 0.23, 0.34, 0.528] rim [0.48, 0.307, 0.606, 0.475]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 3 components >= 12 px at frames [1]):
  - radial S: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.18, rim/outside 1.02 (aggregate of 3 individuals; 0/3 membrane-like individually; rim level 0.45)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.28, rim/outside 2.03 (aggregate of 3 individuals; 1/3 membrane-like individually; rim level 0.427)
  - radial L link: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.46, rim/outside 1.8 (aggregate of 3 individuals; 2/3 membrane-like individually; rim level 0.612)
  - radial membrane (wall): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 2.37 (aggregate of 3 individuals; 0/3 membrane-like individually; rim level 0.557)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #23 (t=50, R_eq 67.93): none; #24 (t=50, R_eq 1.78): none; #25 (t=50, R_eq 2.39): ['K catalyst', 'L link']; #26 (t=50, R_eq 2.26, ring): ['L link']

## Warnings
- RUN FAILED: non-finite fields at frame 2 (only 2 frames analysed)
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- fewer than 30 recorded frames: tracking statistics are weak
- lineage window K=20 frames is more than half the run: late splits cannot count as persistent
- radial: 1 of 3 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 1 of 3 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
