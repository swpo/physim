# Evidence pack: fch-metabolic-micelles (seed 5)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0922-c03-fch-metabolic/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 800 steps x dt 0.02 = time 2400; grid [128, 128]; wall 968s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c03-fch-metabolic/world.py --out /tmp/claude-0/c11rev16/F0.01 --seeds 5 --frames 150 --spf 800 --no-movie`
- segmentation: matter > 0.14 of robust range [0.0807, 2.9984], min area 6 px

## Measurements
- components: final 64, mean 54.3, max 64; occupancy final 0.33
- tracks: 108; persistent (alive >= 50% of run): 62; longest 150 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.73 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [64, 64, 64], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00505/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 320, default): splits 42, persistent splits 39 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 20
- channel total drift (end/start - 1): [0.9588, 3.9857, None, -0.7949]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 76: holes 0, rim-vs-core 0.62, rim-vs-outside 0.28, heterogeneity 0.23; core [0.617, 0.412, 0.316, 0.036] rim [0.173, 0.001, 0.431, 0.072]
  - track 10 at frame 76: holes 0, rim-vs-core 0.65, rim-vs-outside 0.26, heterogeneity 0.24; core [0.617, 0.467, 0.317, 0.045] rim [0.168, 0.001, 0.399, 0.087]
  - track 16 at frame 76: holes 0, rim-vs-core 0.66, rim-vs-outside 0.28, heterogeneity 0.24; core [0.623, 0.477, 0.317, 0.036] rim [0.174, 0.0, 0.427, 0.078]
  - track 78 at frame 96: holes 0, rim-vs-core 0.57, rim-vs-outside 0.29, heterogeneity 0.23; core [0.617, 0.339, 0.344, 0.031] rim [0.171, 0.0, 0.457, 0.06]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 350 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.519, rim/outside 8.31 (aggregate of 350 individuals; 0/350 membrane-like individually; rim level 0.492)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.176, rim/outside 7.41 (aggregate of 350 individuals; 1/350 membrane-like individually; rim level 0.123)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 13.7, rim/outside 4.79 (aggregate of 350 individuals; 350/350 membrane-like individually; rim level 0.751)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 3.49, rim/outside 0.935 (aggregate of 350 individuals; 0/350 membrane-like individually; rim level 0.123)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #7 (t=1216, R_eq 5.08): ['shell q']; #10 (t=1216, R_eq 5.11): ['shell q']; #16 (t=1216, R_eq 5.05): ['shell q']; #78 (t=1536, R_eq 5.11): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
