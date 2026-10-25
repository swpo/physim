# Evidence pack: fch-metabolic-micelles (seed 7)

- world: `../../../20261025T0922-c03-fch-metabolic/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 464s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c03-fch-metabolic/world.py --out collective/contrib/_c07f2/full/seed7 --seeds 7 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.0797, 2.981], min area 6 px

## Measurements
- components: final 56, mean 37.9, max 56; occupancy final 0.28
- tracks: 92; persistent (alive >= 50% of run): 30; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 18.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [56, 56, 56], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 160, default): splits 31, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.032, nucleations 22
- channel total drift (end/start - 1): [0.7457, 3.5035, None, -0.7262]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 51: holes 0, rim-vs-core 0.81, rim-vs-outside 0.22, heterogeneity 0.25; core [0.628, 0.681, 0.225, 0.051] rim [0.179, 0.019, 0.308, 0.125]
  - track 25 at frame 51: holes 0, rim-vs-core 0.43, rim-vs-outside 0.39, heterogeneity 0.22; core [0.663, 0.482, 0.217, 0.073] rim [0.308, 0.264, 0.328, 0.113]
  - track 10 at frame 49: holes 0, rim-vs-core 0.84, rim-vs-outside 0.21, heterogeneity 0.25; core [0.63, 0.718, 0.208, 0.069] rim [0.18, 0.021, 0.285, 0.154]
  - track 59 at frame 79: holes 0, rim-vs-core 0.57, rim-vs-outside 0.33, heterogeneity 0.21; core [0.64, 0.309, 0.306, 0.09] rim [0.191, 0.009, 0.493, 0.13]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 243 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.515, rim/outside 9 (aggregate of 243 individuals; 0/243 membrane-like individually; rim level 0.488)
  - radial catalyst c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.407, rim/outside 8.92 (aggregate of 243 individuals; 0/243 membrane-like individually; rim level 0.243)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 12.5, rim/outside 4.78 (aggregate of 243 individuals; 243/243 membrane-like individually; rim level 0.704)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.9, rim/outside 0.922 (aggregate of 243 individuals; 0/243 membrane-like individually; rim level 0.247)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #22 (t=408, R_eq 5.08): ['shell q']; #25 (t=408, R_eq 5.01): ['shell q']; #10 (t=392, R_eq 5.05): ['shell q']; #59 (t=632, R_eq 4.98): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
