# Evidence pack: cips-layered-divide-audit-tagged (seed 53)

- world: `../../world_tag.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 61 frames x 1000 steps x dt 0.1 = time 6000; grid [192, 192]; wall 756s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/cips-layered/construction/world_tag.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/cips-layered/construction/tagrun/pack --seeds 53 --frames 60 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0224, 0.9746], min area 6 px

## Measurements
- components: final 11, mean 7.1, max 11; occupancy final 0.06
- tracks: 16; persistent (alive >= 50% of run): 4; longest 59 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.79 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 11, 11], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00346/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 2000, default): splits 5, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [0.0, -0.648, 0.6992, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 31: holes 0, rim-vs-core 0.87, rim-vs-outside 0.62, heterogeneity 0.20; core [0.982, 0.944, 0.026, 0.106, 0.112, 0.05] rim [0.767, 0.698, 0.209, 0.554, 0.557, 0.524]
  - track 2 at frame 29: holes 0, rim-vs-core 0.85, rim-vs-outside 0.62, heterogeneity 0.20; core [0.982, 0.942, 0.025, 0.103, 0.109, 0.054] rim [0.777, 0.705, 0.204, 0.531, 0.532, 0.531]
  - track 3 at frame 26: holes 0, rim-vs-core 0.81, rim-vs-outside 0.63, heterogeneity 0.20; core [0.983, 0.946, 0.025, 0.1, 0.105, 0.053] rim [0.786, 0.713, 0.2, 0.507, 0.507, 0.512]
  - track 6 at frame 46: holes 0, rim-vs-core 0.91, rim-vs-outside 0.63, heterogeneity 0.22; core [0.988, 0.958, 0.041, 0.094, 0.099, 0.049] rim [0.763, 0.706, 0.23, 0.563, 0.568, 0.531]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 46 components >= 12 px at frames [10, 20, 30, 40, 50, 60]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 25.7 (aggregate of 46 individuals; 0/46 membrane-like individually; rim level 0.838)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.874, rim/outside 11.5 (aggregate of 46 individuals; 0/46 membrane-like individually; rim level 0.823)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 18.3, rim/outside 0.639 (aggregate of 46 individuals; 0/46 membrane-like individually; rim level 0.486)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 3.35, rim/outside 12.8 (aggregate of 46 individuals; 40/46 membrane-like individually; rim level 0.517)  MEMBRANE-LIKE
  - radial s_body: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 3.22, rim/outside 13.6 (aggregate of 46 individuals; 40/46 membrane-like individually; rim level 0.518)  MEMBRANE-LIKE
  - radial s_band: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 5.42, rim/outside 12.5 (aggregate of 46 individuals; 40/46 membrane-like individually; rim level 0.517)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s, s_body, s_band
- membrane-like channels per top track at mid-life: #1 (t=3100, R_eq 8.74): ['s', 's_body', 's_band']; #2 (t=2900, R_eq 8.78): ['s', 's_body', 's_band']; #3 (t=2600, R_eq 8.65): ['s', 's_body', 's_band']; #6 (t=4600, R_eq 8.04): ['s', 's_body', 's_band']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
