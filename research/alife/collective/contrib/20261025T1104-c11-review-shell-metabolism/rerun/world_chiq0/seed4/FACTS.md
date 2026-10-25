# Evidence pack: fch-metabolic-micelles (seed 4)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0922-c03-fch-metabolic/world_chiq0.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 313s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c03-fch-metabolic/world_chiq0.py --out /tmp/claude-0/c11rev15/world_chiq0 --seeds 4 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.19 of robust range [0.006, 2.6337], min area 6 px

## Measurements
- components: final 0, mean 10.1, max 25; occupancy final 0.00
- tracks: 38; persistent (alive >= 50% of run): 4; longest 53 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.52 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 160, default): splits 8, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 16
- channel total drift (end/start - 1): [-0.9801, -0.9994, None, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 27: holes 0, rim-vs-core 0.46, rim-vs-outside 0.18, heterogeneity 0.07; core [0.768, 0.235, 1.0, 0.483] rim [0.311, 0.222, 1.0, 0.497]
  - track 11 at frame 27: holes 0, rim-vs-core 0.17, rim-vs-outside 0.40, heterogeneity 0.07; core [0.719, 0.217, 1.0, 0.511] rim [0.554, 0.214, 0.991, 0.514]
  - track 15 at frame 27: holes 0, rim-vs-core 0.46, rim-vs-outside 0.20, heterogeneity 0.08; core [0.782, 0.215, 0.985, 0.532] rim [0.328, 0.205, 0.935, 0.548]
  - track 17 at frame 27: holes 0, rim-vs-core 0.46, rim-vs-outside 0.20, heterogeneity 0.08; core [0.784, 0.221, 0.993, 0.527] rim [0.327, 0.21, 0.953, 0.544]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 55 components >= 12 px at frames [17, 33, 50]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.595, rim/outside 16.8 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.584)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.829, rim/outside 1.11 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.255)
  - radial shell q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.944, rim/outside 1.14 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.909)
  - radial precursor p: peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 1.02 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.542)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=216, R_eq 3.39): none; #11 (t=216, R_eq 3.19): none; #15 (t=216, R_eq 3.34): none; #17 (t=216, R_eq 3.34): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
