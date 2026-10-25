# Evidence pack: fch-turnover-test (seed 0)

- world: `../../wturn_a5.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 121 frames x 400 steps x dt 0.02 = time 960; grid [128, 128]; wall 430s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/wturn_a5.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/turn_a5/seed0 --seeds 0 --frames 120 --spf 400 --no-movie`
- segmentation: matter > 0.15 of robust range [0.059, 2.9755], min area 6 px

## Measurements
- components: final 26, mean 25.0, max 26; occupancy final 0.13
- tracks: 31; persistent (alive >= 50% of run): 25; longest 121 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 12.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 26, 26], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 160, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 24
- channel total drift (end/start - 1): [0.0582, -0.0494, None, -0.4292]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 61: holes 0, rim-vs-core 0.24, rim-vs-outside 0.44, heterogeneity 0.23; core [0.588, 0.405, 0.315, 0.051] rim [0.417, 0.244, 0.281, 0.082]
  - track 5 at frame 61: holes 0, rim-vs-core 0.35, rim-vs-outside 0.40, heterogeneity 0.23; core [0.627, 0.451, 0.283, 0.043] rim [0.383, 0.209, 0.301, 0.088]
  - track 6 at frame 61: holes 0, rim-vs-core 0.35, rim-vs-outside 0.38, heterogeneity 0.23; core [0.626, 0.408, 0.318, 0.033] rim [0.362, 0.185, 0.309, 0.067]
  - track 7 at frame 61: holes 0, rim-vs-core 0.66, rim-vs-outside 0.23, heterogeneity 0.23; core [0.641, 0.466, 0.278, 0.04] rim [0.183, 0.001, 0.341, 0.115]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 151 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.514, rim/outside 14.5 (aggregate of 151 individuals; 0/151 membrane-like individually; rim level 0.488)
  - radial catalyst c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.313, rim/outside 17.9 (aggregate of 151 individuals; 0/151 membrane-like individually; rim level 0.204)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 11.9, rim/outside 6.37 (aggregate of 151 individuals; 151/151 membrane-like individually; rim level 0.699)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.99, rim/outside 0.855 (aggregate of 151 individuals; 0/151 membrane-like individually; rim level 0.323)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #2 (t=488, R_eq 5.05): ['shell q']; #5 (t=488, R_eq 5.05): ['shell q']; #6 (t=488, R_eq 5.08): ['shell q']; #7 (t=488, R_eq 5.08): ['shell q']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
