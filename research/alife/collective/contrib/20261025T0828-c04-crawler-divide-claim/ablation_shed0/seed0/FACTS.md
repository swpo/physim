# Evidence pack: crawler (seed 0)

- world: `../../crawler.py`, family `phase-field`
- parent: None; mutation: Ziebert-Aranson crawling cell, body-wise area constraint
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 217s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/crawler.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/C --seeds 0 1 --frames 240 --threshold 0.25 --no-movie`
- segmentation: matter > 0.26 of robust range [-0.0, 0.9678], min area 6 px

## Measurements
- components: final 26, mean 17.9, max 26; occupancy final 0.22
- tracks: 157; persistent (alive >= 50% of run): 26; longest 165 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.96 (1 = constant size)
- enclosures: components with a hole mean 0.12, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 26, 26], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 50, default): splits 65, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 32, merge/split ratio 0.492, nucleations 2
- channel total drift (end/start - 1): [3.9366, 0.8804, None, -0.7637]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 106 at frame 159: holes 0, rim-vs-core 0.30, rim-vs-outside 0.17, heterogeneity 0.05; core [0.652, 0.131, 0.001, 0.039] rim [0.356, 0.15, 0.0, 0.043]
  - track 109 at frame 159: holes 0, rim-vs-core 0.31, rim-vs-outside 0.22, heterogeneity 0.05; core [0.689, 0.128, 0.001, 0.039] rim [0.38, 0.154, 0.001, 0.043]
  - track 114 at frame 159: holes 0, rim-vs-core 0.30, rim-vs-outside 0.17, heterogeneity 0.05; core [0.647, 0.132, 0.001, 0.04] rim [0.348, 0.15, 0.0, 0.045]
  - track 146 at frame 165: holes 0, rim-vs-core 0.18, rim-vs-outside 0.26, heterogeneity 0.05; core [0.628, 0.13, 0.0, 0.049] rim [0.448, 0.147, 0.0, 0.052]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 125 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.77, rim/outside 4.62 (aggregate of 125 individuals; 0/125 membrane-like individually; rim level 0.602)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.42, rim/outside 3.48 (aggregate of 125 individuals; 109/125 membrane-like individually; rim level 0.179)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.937, rim/outside 1.14 (aggregate of 125 individuals; 1/125 membrane-like individually; rim level 0.0865)
  - radial n (nutrient): peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.13, rim/outside 0.992 (aggregate of 125 individuals; 0/125 membrane-like individually; rim level 0.0948)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #106 (t=397.5, R_eq 13.75): ['|P| (actin polarization)']; #109 (t=397.5, R_eq 14.18): ['|P| (actin polarization)']; #114 (t=397.5, R_eq 13.89): ['|P| (actin polarization)']; #146 (t=412.5, R_eq 13.15): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 125 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 1 of 125 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
