# Evidence pack: fch-metabolic-micelles (seed 0)

- world: `../../wm4_cut.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 400 steps x dt 0.02 = time 1200; grid [128, 128]; wall 456s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/wm4_cut.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/m4cut/seed0 --seeds 0 --frames 150 --spf 400 --no-movie`
- segmentation: matter > 0.17 of robust range [0.0106, 2.8911], min area 6 px

## Measurements
- components: final 0, mean 23.6, max 43; occupancy final 0.00
- tracks: 65; persistent (alive >= 50% of run): 12; longest 104 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 160, default): splits 18, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 24
- channel total drift (end/start - 1): [-0.9649, -0.9971, None, -0.9656]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 27 at frame 53: holes 0, rim-vs-core 0.88, rim-vs-outside 0.32, heterogeneity 0.27; core [0.69, 0.744, 0.314, 0.086] rim [0.225, 0.014, 0.465, 0.122]
  - track 17 at frame 53: holes 0, rim-vs-core 0.82, rim-vs-outside 0.27, heterogeneity 0.26; core [0.68, 0.721, 0.326, 0.091] rim [0.212, 0.048, 0.407, 0.127]
  - track 6 at frame 48: holes 0, rim-vs-core 0.67, rim-vs-outside 0.45, heterogeneity 0.25; core [0.725, 0.762, 0.236, 0.204] rim [0.293, 0.303, 0.448, 0.26]
  - track 45 at frame 81: holes 0, rim-vs-core 0.48, rim-vs-outside 0.53, heterogeneity 0.15; core [0.619, 0.122, 0.463, 0.0] rim [0.244, 0.046, 0.746, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 129 components >= 12 px at frames [25, 50, 76, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.524, rim/outside 9.94 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.486)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.503, rim/outside 10.6 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.258)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 11.7, rim/outside 6.67 (aggregate of 129 individuals; 129/129 membrane-like individually; rim level 0.777)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.3, rim/outside 0.942 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.249)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #27 (t=424, R_eq 4.85): ['shell q']; #17 (t=424, R_eq 4.92): ['shell q']; #6 (t=384, R_eq 4.69): ['shell q']; #45 (t=648, R_eq 3.39): ['shell q']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
