# Evidence pack: phase-membrane-noise (seed 0)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: dynamics noise sd 0.03 per sqrt(t): additive on ['phi'], multiplicative (sd x value) on []
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 15s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/phi_0.03_s0 --seeds 0 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5281], min area 6 px

## Measurements
- components: final 14, mean 7.6, max 16; occupancy final 0.29
- tracks: 481; persistent (alive >= 50% of run): 0; longest 47 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 2.60, final 5; holes at thresholds 0.2/0.35/0.5 final [0, 8, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 15, 14], H1 [16, 13, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 1000, default): splits 40, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 27, merge/split ratio 0.675, nucleations 348
- channel total drift (end/start - 1): [-0.4209, -0.7452, -0.0641, -0.1525]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 439 at frame 137: holes 0, rim-vs-core 0.38, rim-vs-outside 0.81, heterogeneity 0.19; core [0.103, 0.82, 0.56, 0.705] rim [0.285, 0.485, 0.589, 0.667]
  - track 441 at frame 134: holes 1, rim-vs-core 0.20, rim-vs-outside 0.82, heterogeneity 0.21; core [0.091, 0.851, 0.566, 0.543] rim [0.167, 0.674, 0.541, 0.585]
  - track 443 at frame 133: holes 1, rim-vs-core 0.19, rim-vs-outside 0.82, heterogeneity 0.20; core [0.062, 0.725, 0.434, 0.568] rim [0.182, 0.623, 0.532, 0.593]
  - track 446 at frame 145: holes 1, rim-vs-core 0.20, rim-vs-outside 0.83, heterogeneity 0.19; core [0.09, 0.767, 0.543, 0.715] rim [0.169, 0.61, 0.523, 0.62]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 38 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 8.38, rim/outside 0.783 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.426)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 0.992, rim/outside 4 (aggregate of 38 individuals; 1/38 membrane-like individually; rim level 0.674)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 3.79 (aggregate of 38 individuals; 22/38 membrane-like individually; rim level 0.498)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.47, rim/outside 3.58 (aggregate of 38 individuals; 20/38 membrane-like individually; rim level 0.51)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #439 (t=6850, R_eq 8.04): ['L link']; #441 (t=6700, R_eq 11.97, ring): ['L link', 'membrane (wall)']; #443 (t=6650, R_eq 12.75, ring): ['L link', 'membrane (wall)']; #446 (t=7250, R_eq 10.37, ring): ['L link', 'membrane (wall)']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 38 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
