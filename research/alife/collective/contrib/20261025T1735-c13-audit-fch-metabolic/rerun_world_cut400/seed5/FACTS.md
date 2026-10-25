# Evidence pack: fch-metabolic-micelles (seed 5)

- world: `../../world_cut400.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 311s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1735-c13-audit-fch-metabolic/world_cut400.py --out collective/contrib/20261025T1735-c13-audit-fch-metabolic/rerun_world_cut400/seed5 --seeds 5 --spf 400 --frames 100 --no-movie`
- segmentation: matter > 0.16 of robust range [0.0289, 2.9366], min area 6 px

## Measurements
- components: final 14, mean 31.9, max 39; occupancy final 0.03
- tracks: 58; persistent (alive >= 50% of run): 39; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 14, 14], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 160, default): splits 17, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 20
- channel total drift (end/start - 1): [-0.7415, -0.8399, None, -0.9612]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 51: holes 0, rim-vs-core 0.82, rim-vs-outside 0.33, heterogeneity 0.26; core [0.697, 0.734, 0.254, 0.107] rim [0.251, 0.077, 0.434, 0.16]
  - track 7 at frame 50: holes 0, rim-vs-core 0.73, rim-vs-outside 0.26, heterogeneity 0.25; core [0.654, 0.647, 0.297, 0.179] rim [0.196, 0.088, 0.37, 0.234]
  - track 17 at frame 50: holes 0, rim-vs-core 0.81, rim-vs-outside 0.25, heterogeneity 0.26; core [0.661, 0.692, 0.278, 0.171] rim [0.199, 0.033, 0.364, 0.237]
  - track 30 at frame 69: holes 0, rim-vs-core 0.38, rim-vs-outside 0.41, heterogeneity 0.18; core [0.638, 0.266, 0.41, 0.008] rim [0.309, 0.113, 0.52, 0.01]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 181 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.519, rim/outside 11.4 (aggregate of 181 individuals; 0/181 membrane-like individually; rim level 0.478)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.575, rim/outside 14 (aggregate of 181 individuals; 0/181 membrane-like individually; rim level 0.27)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 12.4, rim/outside 6.89 (aggregate of 181 individuals; 181/181 membrane-like individually; rim level 0.736)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.23, rim/outside 0.952 (aggregate of 181 individuals; 0/181 membrane-like individually; rim level 0.255)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #19 (t=408, R_eq 5.08): ['shell q']; #7 (t=400, R_eq 5.05): ['shell q']; #17 (t=400, R_eq 5.11): ['shell q']; #30 (t=552, R_eq 4.22): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
