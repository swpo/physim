# Evidence pack: phase-membrane-noise (seed 2)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: additive dynamics noise sd 0.03 per sqrt(t) on ['S', 'K', 'L', 'phi']
- run: 2 frames x 50 steps x dt 1.0 = time 50; grid [128, 128]; wall 0s; status non-finite fields at frame 2
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/noise_0.03_s2 --seeds 2 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0717, 2.0833], min area 6 px

## Measurements
- components: final 1, mean 11.0, max 21; occupancy final 0.88
- tracks: 22; persistent (alive >= 50% of run): 22; longest 1 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.00 (1 = constant size)
- enclosures: components with a hole mean 1.00, final 1; holes at thresholds 0.2/0.35/0.5 final [3, 79, 31]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [141, 43, 2], H1 [147, 60, 4]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 1000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.4785, -0.2669, 4.7341, 1.1753]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 1: holes 79, rim-vs-core 0.40, rim-vs-outside 0.51, heterogeneity 0.20; core [0.065, 0.645, 0.49, 0.765] rim [0.353, 0.392, 0.485, 0.664]
  - track 0 at frame 0: holes 0, rim-vs-core 0.11, rim-vs-outside 0.28, heterogeneity 0.12; core [1.0, 0.485, 0.074, 0.738] rim [1.0, 0.534, 0.082, 0.642]
  - track 1 at frame 0: holes 0, rim-vs-core 0.09, rim-vs-outside 0.18, heterogeneity 0.11; core [1.0, 0.584, 0.08, 0.642] rim [1.0, 0.532, 0.07, 0.571]
  - track 2 at frame 0: holes 0, rim-vs-core 0.22, rim-vs-outside 0.39, heterogeneity 0.12; core [1.0, 0.518, 0.085, 0.823] rim [1.0, 0.549, 0.077, 0.605]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1 components >= 12 px at frames [1]):
  - radial S: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 1.53, rim/outside n/a (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 0.435)
  - radial K catalyst: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.894, rim/outside n/a (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 0.382)
  - radial L link: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside n/a (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 0.476)
  - radial membrane (wall): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside n/a (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 0.649)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #21 (t=50, R_eq 67.7): none; #0 (t=0, R_eq 4.79): none; #1 (t=0, R_eq 5.23): none; #2 (t=0, R_eq 9.1): none

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
