# Evidence pack: fch-allee-micelles (seed 0)

- world: `../../wb1.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 800 steps x dt 0.02 = time 2400; grid [128, 128]; wall 993s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/wb1.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/al_wb1/seed0 --seeds 0 --frames 150 --spf 800 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1223, 2.9655], min area 6 px

## Measurements
- components: final 40, mean 39.4, max 40; occupancy final 0.19
- tracks: 58; persistent (alive >= 50% of run): 40; longest 151 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 12.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 40, 40], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 320, default): splits 15, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 23
- channel total drift (end/start - 1): [0.2834, -0.6151, None, -0.7694]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 76: holes 0, rim-vs-core 0.32, rim-vs-outside 0.45, heterogeneity 0.27; core [0.575, 0.491, 0.424, 0.056] rim [0.365, 0.257, 0.389, 0.086]
  - track 5 at frame 76: holes 0, rim-vs-core 0.29, rim-vs-outside 0.42, heterogeneity 0.25; core [0.58, 0.389, 0.422, 0.047] rim [0.36, 0.2, 0.398, 0.075]
  - track 6 at frame 76: holes 0, rim-vs-core 0.69, rim-vs-outside 0.29, heterogeneity 0.26; core [0.614, 0.5, 0.373, 0.048] rim [0.159, 0.0, 0.463, 0.111]
  - track 52 at frame 79: holes 0, rim-vs-core 0.67, rim-vs-outside 0.36, heterogeneity 0.26; core [0.621, 0.46, 0.35, 0.043] rim [0.175, 0.0, 0.548, 0.098]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 240 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.497, rim/outside 24.2 (aggregate of 240 individuals; 0/240 membrane-like individually; rim level 0.47)
  - radial catalyst c: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.113, rim/outside 8.64 (aggregate of 240 individuals; 0/240 membrane-like individually; rim level 0.0835)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 14.2, rim/outside 6.47 (aggregate of 240 individuals; 240/240 membrane-like individually; rim level 0.85)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 10.5, rim/outside 0.855 (aggregate of 240 individuals; 0/240 membrane-like individually; rim level 0.138)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #2 (t=1216, R_eq 4.98): ['shell q']; #5 (t=1216, R_eq 4.98): ['shell q']; #6 (t=1216, R_eq 4.98): ['shell q']; #52 (t=1264, R_eq 4.92): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
