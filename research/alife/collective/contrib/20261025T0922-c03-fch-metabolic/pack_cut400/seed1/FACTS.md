# Evidence pack: fch-metabolic-micelles (seed 1)

- world: `../../wm4_cut.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 400 steps x dt 0.02 = time 1200; grid [128, 128]; wall 470s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/wm4_cut.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/m4cut/seed1 --seeds 1 --frames 150 --spf 400 --no-movie`
- segmentation: matter > 0.17 of robust range [0.0106, 2.9056], min area 6 px

## Measurements
- components: final 0, mean 22.1, max 39; occupancy final 0.00
- tracks: 61; persistent (alive >= 50% of run): 13; longest 107 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 160, default): splits 21, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 18
- channel total drift (end/start - 1): [-0.9642, -0.997, None, -0.9602]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 54: holes 0, rim-vs-core 0.72, rim-vs-outside 0.27, heterogeneity 0.27; core [0.667, 0.687, 0.352, 0.09] rim [0.2, 0.139, 0.39, 0.122]
  - track 5 at frame 54: holes 0, rim-vs-core 0.82, rim-vs-outside 0.29, heterogeneity 0.27; core [0.678, 0.699, 0.323, 0.068] rim [0.216, 0.035, 0.436, 0.1]
  - track 7 at frame 54: holes 0, rim-vs-core 0.76, rim-vs-outside 0.28, heterogeneity 0.26; core [0.672, 0.716, 0.34, 0.077] rim [0.204, 0.123, 0.395, 0.108]
  - track 49 at frame 81: holes 0, rim-vs-core 0.50, rim-vs-outside 0.55, heterogeneity 0.16; core [0.628, 0.11, 0.442, 0.0] rim [0.255, 0.056, 0.777, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 116 components >= 12 px at frames [25, 50, 76, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.524, rim/outside 8.98 (aggregate of 116 individuals; 0/116 membrane-like individually; rim level 0.492)
  - radial catalyst c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.505, rim/outside 11 (aggregate of 116 individuals; 0/116 membrane-like individually; rim level 0.276)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 12, rim/outside 6.4 (aggregate of 116 individuals; 116/116 membrane-like individually; rim level 0.762)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.4, rim/outside 0.943 (aggregate of 116 individuals; 0/116 membrane-like individually; rim level 0.245)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #2 (t=432, R_eq 5.05): ['shell q']; #5 (t=432, R_eq 5.01): ['shell q']; #7 (t=432, R_eq 5.05): ['shell q']; #49 (t=648, R_eq 3.39): ['shell q']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
