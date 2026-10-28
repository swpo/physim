# Evidence pack: phase-membrane-noise (seed 1)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: additive dynamics noise sd 0.03 per sqrt(t) on ['S', 'K', 'L', 'phi']
- run: 2 frames x 50 steps x dt 1.0 = time 50; grid [128, 128]; wall 0s; status non-finite fields at frame 2
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/noise_0.03_s1 --seeds 1 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0654, 2.0857], min area 6 px

## Measurements
- components: final 2, mean 17.5, max 33; occupancy final 0.85
- tracks: 35; persistent (alive >= 50% of run): 35; longest 1 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.00 (1 = constant size)
- enclosures: components with a hole mean 0.50, final 1; holes at thresholds 0.2/0.35/0.5 final [6, 90, 28]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [149, 57, 1], H1 [142, 58, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 1000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 1
- channel total drift (end/start - 1): [-0.4532, -0.3258, 4.6556, 1.8526]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 0: holes 0, rim-vs-core 0.10, rim-vs-outside 0.17, heterogeneity 0.10; core [1.0, 0.611, 0.056, 0.603] rim [1.0, 0.603, 0.093, 0.515]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1 components >= 12 px at frames [1]):
  - radial S: peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside n/a (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 0.36)
  - radial K catalyst: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 0.986, rim/outside n/a (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 0.348)
  - radial L link: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside n/a (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 0.459)
  - radial membrane (wall): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.954, rim/outside n/a (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 0.607)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #33 (t=50, R_eq 66.68): none; #34 (t=50, R_eq 1.6): none; #0 (t=0, R_eq 2.39): ['K catalyst', 'L link']; #1 (t=0, R_eq 1.38): ['K catalyst', 'L link']

## Warnings
- RUN FAILED: non-finite fields at frame 2 (only 2 frames analysed)
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- fewer than 30 recorded frames: tracking statistics are weak
- lineage window K=20 frames is more than half the run: late splits cannot count as persistent
- radial: for 1 of 1 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
