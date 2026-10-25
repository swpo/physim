# Evidence pack: rdtrail (seed 1)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/_c07wip/world.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 27s; status ok
- command: `python -m labkit.run collective/contrib/_c07wip/world.py --out /tmp/claude-0/c07/pk_matched --seeds 0 1 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9926], min area 6 px

## Measurements
- components: final 24, mean 13.3, max 25; occupancy final 0.24
- tracks: 59; persistent (alive >= 50% of run): 7; longest 160 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.28 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 24, 24], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0859/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 60, default): splits 24, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 3, merges 4, merge/split ratio 0.167, nucleations 1
- channel total drift (end/start - 1): [5.7357, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 121: holes 0, rim-vs-core 0.53, rim-vs-outside 0.45, heterogeneity 0.19; core [0.886, 0.813, 0.888] rim [0.524, 0.557, 0.59]
  - track 18 at frame 123: holes 0, rim-vs-core 0.43, rim-vs-outside 0.33, heterogeneity 0.15; core [0.797, 0.663, 0.857] rim [0.475, 0.492, 0.628]
  - track 13 at frame 104: holes 0, rim-vs-core 0.62, rim-vs-outside 0.53, heterogeneity 0.20; core [0.943, 0.781, 0.802] rim [0.588, 0.502, 0.38]
  - track 37 at frame 163: holes 0, rim-vs-core 0.34, rim-vs-outside 0.47, heterogeneity 0.14; core [0.823, 0.63, 0.881] rim [0.587, 0.513, 0.67]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 89 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 7.23 (aggregate of 89 individuals; 0/89 membrane-like individually; rim level 0.725)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 2.93 (aggregate of 89 individuals; 0/89 membrane-like individually; rim level 0.574)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.75, rim/outside 5.43 (aggregate of 89 individuals; 0/89 membrane-like individually; rim level 0.673)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=363, R_eq 17.37): none; #18 (t=369, R_eq 12.78): none; #13 (t=312, R_eq 18.09): none; #37 (t=489, R_eq 10.59): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
