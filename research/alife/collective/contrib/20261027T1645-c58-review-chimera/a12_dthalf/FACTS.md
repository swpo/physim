# Evidence pack: chimera-field (seed 5)

- world: `../../20261027T1049-c55-chimera-field-negative/world.py`, family `nonlocal-oscillators`
- parent: None; mutation: -
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 54s; status ok
- command: `python -m labkit.run collective/contrib/20261027T1049-c55-chimera-field-negative/world.py --out collective/contrib/20261027T1645-c58-review-chimera/a12_dthalf --seeds 5 --frames 300 --spf 100 --no-movie`
- segmentation: matter > 0.31 of robust range [0.0, 0.9673], min area 6 px

## Measurements
- components: final 1, mean 1.8, max 5; occupancy final 0.65
- tracks: 319; persistent (alive >= 50% of run): 0; longest 13 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.54, final 1; holes at thresholds 0.2/0.35/0.5 final [3, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 8, 2], H1 [4, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 200, default): splits 120, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 72, merge/split ratio 0.6, nucleations 1
- channel total drift (end/start - 1): [None, 6.3124, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 122 at frame 116: holes 0, rim-vs-core 0.33, rim-vs-outside 0.47, heterogeneity 0.18; core [0.842, 0.478, 0.0, 0.535] rim [0.566, 0.52, 0.0, 0.355]
  - track 187 at frame 176: holes 0, rim-vs-core 0.14, rim-vs-outside 0.43, heterogeneity 0.18; core [0.632, 0.552, 0.0, 0.447] rim [0.536, 0.524, 0.0, 0.356]
  - track 248 at frame 242: holes 3, rim-vs-core 0.17, rim-vs-outside 0.45, heterogeneity 0.18; core [0.687, 0.565, 0.0, 0.436] rim [0.551, 0.491, 0.0, 0.373]
  - track 246 at frame 234: holes 2, rim-vs-core 0.21, rim-vs-outside 0.40, heterogeneity 0.18; core [0.704, 0.471, 0.0, 0.447] rim [0.522, 0.522, 0.0, 0.358]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 9 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial incoherence 1-|Z|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 1.6 (aggregate of 9 individuals; 0/9 membrane-like individually; rim level 0.413)
  - radial cos phase: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.1, rim/outside 0.998 (aggregate of 9 individuals; 0/9 membrane-like individually; rim level 0.459)
  - radial fuel Y: flat profile (no radial structure; level 0; aggregate of 9 individuals)
  - radial local frequency: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 1.86 (aggregate of 9 individuals; 1/9 membrane-like individually; rim level 0.328)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #122 (t=1160, R_eq 53.62): none; #187 (t=1760, R_eq 55.52): none; #248 (t=2420, R_eq 58.02): none; #246 (t=2340, R_eq 58.54, ring): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 6 of 9 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
