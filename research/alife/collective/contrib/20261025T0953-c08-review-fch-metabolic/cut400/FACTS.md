# Evidence pack: fch-metabolic-micelles (seed 5)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0922-c03-fch-metabolic/world_cut400.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 400 steps x dt 0.02 = time 1200; grid [128, 128]; wall 464s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c03-fch-metabolic/world_cut400.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/rev2/cut400 --seeds 5 --frames 150 --spf 400 --no-movie`
- segmentation: matter > 0.17 of robust range [0.0107, 2.9115], min area 6 px

## Measurements
- components: final 0, mean 22.3, max 39; occupancy final 0.00
- tracks: 58; persistent (alive >= 50% of run): 16; longest 107 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 160, default): splits 17, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 20
- channel total drift (end/start - 1): [-0.965, -0.997, None, -0.9615]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 54: holes 0, rim-vs-core 0.82, rim-vs-outside 0.35, heterogeneity 0.27; core [0.705, 0.733, 0.301, 0.052] rim [0.253, 0.076, 0.477, 0.082]
  - track 28 at frame 55: holes 0, rim-vs-core 0.84, rim-vs-outside 0.29, heterogeneity 0.27; core [0.679, 0.71, 0.317, 0.068] rim [0.213, 0.019, 0.434, 0.1]
  - track 7 at frame 50: holes 0, rim-vs-core 0.75, rim-vs-outside 0.27, heterogeneity 0.26; core [0.674, 0.684, 0.315, 0.179] rim [0.209, 0.098, 0.392, 0.234]
  - track 30 at frame 78: holes 0, rim-vs-core 0.46, rim-vs-outside 0.49, heterogeneity 0.16; core [0.663, 0.188, 0.382, 0.0] rim [0.314, 0.101, 0.662, 0.001]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 117 components >= 12 px at frames [25, 50, 76, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.529, rim/outside 9.54 (aggregate of 117 individuals; 0/117 membrane-like individually; rim level 0.495)
  - radial catalyst c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.524, rim/outside 12.1 (aggregate of 117 individuals; 0/117 membrane-like individually; rim level 0.273)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 11.9, rim/outside 6.44 (aggregate of 117 individuals; 117/117 membrane-like individually; rim level 0.756)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.4, rim/outside 0.952 (aggregate of 117 individuals; 0/117 membrane-like individually; rim level 0.251)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #19 (t=432, R_eq 5.08): ['shell q']; #28 (t=440, R_eq 5.05): ['shell q']; #7 (t=400, R_eq 5.05): ['shell q']; #30 (t=624, R_eq 3.61): ['shell q']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
