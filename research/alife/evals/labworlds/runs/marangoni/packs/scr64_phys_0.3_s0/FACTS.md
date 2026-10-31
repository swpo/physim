# Evidence pack: active-nematic-marangoni-noise (seed 0)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.3 per sqrt(t): additive on ['q1', 'q2'], proportional on ['s', 'c'], conserved (div of white flux) on ['phi']
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [64, 64]; wall 56s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/scr64_phys_0.3_s0 --seeds 0 --frames 100 --size 64 64 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.8906, 0.7373], min area 6 px

## Measurements
- components: final 9, mean 8.0, max 10; occupancy final 0.07
- tracks: 41; persistent (alive >= 50% of run): 4; longest 84 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.30 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [4, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.223/time; max body lengths 11.7
- replication (lineage window K = 20 frames = time 100, default): splits 10, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 6, merge/split ratio 0.6, nucleations 15
- channel total drift (end/start - 1): [-0.4868, 2.0037, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 48: holes 0, rim-vs-core 0.56, rim-vs-outside 0.24, heterogeneity 0.20; core [0.905, 0.536, 0.348, 0.432] rim [0.724, 0.45, 0.703, 0.046]
  - track 8 at frame 51: holes 0, rim-vs-core 0.47, rim-vs-outside 0.23, heterogeneity 0.17; core [0.83, 0.446, 0.336, 0.404] rim [0.697, 0.371, 0.62, 0.065]
  - track 16 at frame 60: holes 0, rim-vs-core 0.73, rim-vs-outside 0.29, heterogeneity 0.25; core [0.946, 0.817, 0.223, 0.417] rim [0.744, 0.506, 0.739, 0.051]
  - track 18 at frame 56: holes 0, rim-vs-core 0.46, rim-vs-outside 0.21, heterogeneity 0.18; core [0.826, 0.466, 0.339, 0.529] rim [0.689, 0.358, 0.504, 0.139]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 51 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.823, rim/outside 4.03 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.757)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 1.49 (aggregate of 51 individuals; 4/51 membrane-like individually; rim level 0.451)
  - radial surfactant s: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.35, rim/outside 3.67 (aggregate of 51 individuals; 39/51 membrane-like individually; rim level 0.546)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.337, rim/outside 0.786 (aggregate of 51 individuals; 2/51 membrane-like individually; rim level 0.172)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #3 (t=240, R_eq 3.14): ['surfactant s']; #8 (t=255, R_eq 3.48): ['surfactant s']; #16 (t=300, R_eq 3.78): ['surfactant s']; #18 (t=280, R_eq 3.43): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
