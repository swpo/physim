# Evidence pack: crawler (seed 0)

- world: `../crawler.py`, family `phase-field`
- parent: None; mutation: Ziebert-Aranson crawling cell, body-wise area constraint
- run: 121 frames x 100 steps x dt 0.05 = time 600; grid [256, 256]; wall 221s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/crawler.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/fed1 --seeds 0 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 0.9933], min area 6 px

## Measurements
- components: final 31, mean 27.5, max 32; occupancy final 0.23
- tracks: 53; persistent (alive >= 50% of run): 31; longest 109 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 31.50 (1 = constant size)
- enclosures: components with a hole mean 0.11, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 31, 31], H1 [12, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0548/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 100, default): splits 12, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1, merge/split ratio 0.083, nucleations 24
- channel total drift (end/start - 1): [9.7404, 4.2813, None, -0.4794]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 67: holes 0, rim-vs-core 0.10, rim-vs-outside 0.25, heterogeneity 0.05; core [0.635, 0.2, 0.92, 0.006] rim [0.59, 0.256, 0.855, 0.012]
  - track 11 at frame 67: holes 0, rim-vs-core 0.21, rim-vs-outside 0.16, heterogeneity 0.06; core [0.642, 0.186, 0.93, 0.006] rim [0.551, 0.323, 0.799, 0.018]
  - track 13 at frame 67: holes 0, rim-vs-core 0.22, rim-vs-outside 0.17, heterogeneity 0.06; core [0.645, 0.197, 0.935, 0.009] rim [0.554, 0.341, 0.804, 0.019]
  - track 40 at frame 70: holes 0, rim-vs-core 0.21, rim-vs-outside 0.18, heterogeneity 0.05; core [0.637, 0.192, 0.923, 0.013] rim [0.553, 0.334, 0.801, 0.021]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 185 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.913, rim/outside 4.08 (aggregate of 185 individuals; 0/185 membrane-like individually; rim level 0.621)
  - radial |P| (actin polarization): peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 5.02, rim/outside 2.17 (aggregate of 185 individuals; 179/185 membrane-like individually; rim level 0.405)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.914, rim/outside 4.18 (aggregate of 185 individuals; 0/185 membrane-like individually; rim level 0.884)
  - radial n (nutrient): peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.97, rim/outside 0.783 (aggregate of 185 individuals; 0/185 membrane-like individually; rim level 0.055)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #10 (t=335, R_eq 12.74): ['|P| (actin polarization)']; #11 (t=335, R_eq 12.55): ['|P| (actin polarization)']; #13 (t=335, R_eq 11.87): ['|P| (actin polarization)']; #40 (t=350, R_eq 10.93): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
