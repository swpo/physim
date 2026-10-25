# Evidence pack: fch-allee-micelles (seed 0)

- world: `../../wb2.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 800 steps x dt 0.02 = time 2400; grid [128, 128]; wall 996s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/wb2.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/al_wb2/seed0 --seeds 0 --frames 150 --spf 800 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1217, 2.9577], min area 6 px

## Measurements
- components: final 37, mean 36.3, max 37; occupancy final 0.17
- tracks: 52; persistent (alive >= 50% of run): 37; longest 151 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 12.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 37, 37], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 320, default): splits 12, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 23
- channel total drift (end/start - 1): [0.2076, -0.4244, None, -0.7564]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 76: holes 0, rim-vs-core 0.28, rim-vs-outside 0.46, heterogeneity 0.27; core [0.549, 0.479, 0.441, 0.061] rim [0.38, 0.272, 0.367, 0.089]
  - track 6 at frame 76: holes 0, rim-vs-core 0.67, rim-vs-outside 0.30, heterogeneity 0.26; core [0.608, 0.482, 0.37, 0.049] rim [0.159, 0.0, 0.462, 0.112]
  - track 7 at frame 76: holes 0, rim-vs-core 0.69, rim-vs-outside 0.30, heterogeneity 0.27; core [0.609, 0.515, 0.364, 0.05] rim [0.16, 0.0, 0.459, 0.117]
  - track 32 at frame 79: holes 0, rim-vs-core 0.61, rim-vs-outside 0.30, heterogeneity 0.25; core [0.604, 0.405, 0.387, 0.044] rim [0.157, 0.0, 0.474, 0.097]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 222 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.498, rim/outside 25 (aggregate of 222 individuals; 0/222 membrane-like individually; rim level 0.472)
  - radial catalyst c: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.159, rim/outside 12.3 (aggregate of 222 individuals; 0/222 membrane-like individually; rim level 0.122)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 14.1, rim/outside 6.56 (aggregate of 222 individuals; 222/222 membrane-like individually; rim level 0.85)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 11.3, rim/outside 0.837 (aggregate of 222 individuals; 0/222 membrane-like individually; rim level 0.144)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #2 (t=1216, R_eq 4.98): ['shell q']; #6 (t=1216, R_eq 4.98): ['shell q']; #7 (t=1216, R_eq 4.98): ['shell q']; #32 (t=1264, R_eq 4.98): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
