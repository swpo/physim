# Evidence pack: active-gel-fed-comets (seed 6)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1016-c09-active-gel-comets-claim/world.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 301 frames x 100 steps x dt 0.01 = time 300; grid [128, 128]; wall 76s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1016-c09-active-gel-comets-claim/world.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev14/ks05 --seeds 6 --frames 300 --no-movie`
- segmentation: matter > 0.03 of robust range [0.0, 32.8792], min area 6 px

## Measurements
- components: final 12, mean 15.4, max 50; occupancy final 0.03
- tracks: 327; persistent (alive >= 50% of run): 3; longest 175 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.85 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 12, 10], H1 [0, 0, 0]
- motion: 56 long-lived tracks moved >= 1 body length; max speed 1.78/time; max body lengths 11.7
- replication (lineage window K = 20 frames = time 20, default): splits 30, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 136, merge/split ratio 4.53, nucleations 141
- channel total drift (end/start - 1): [-0.6767, 0.1496, -0.3249]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 61 at frame 93: holes 0, rim-vs-core 0.19, rim-vs-outside 0.09, heterogeneity 0.07; core [0.221, 0.251, 0.325] rim [0.064, 0.197, 0.415]
  - track 77 at frame 103: holes 0, rim-vs-core 0.21, rim-vs-outside 0.12, heterogeneity 0.09; core [0.254, 0.258, 0.284] rim [0.101, 0.158, 0.387]
  - track 89 at frame 116: holes 0, rim-vs-core 0.22, rim-vs-outside 0.09, heterogeneity 0.08; core [0.252, 0.217, 0.304] rim [0.067, 0.157, 0.404]
  - track 91 at frame 108: holes 0, rim-vs-core 0.21, rim-vs-outside 0.07, heterogeneity 0.08; core [0.219, 0.218, 0.304] rim [0.049, 0.157, 0.407]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 89 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.329, rim/outside 10.8 (aggregate of 89 individuals; 1/89 membrane-like individually; rim level 0.169)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.76, rim/outside 1.49 (aggregate of 89 individuals; 0/89 membrane-like individually; rim level 0.264)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.37, rim/outside 0.828 (aggregate of 89 individuals; 0/89 membrane-like individually; rim level 0.438)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #61 (t=93, R_eq 3.14): none; #77 (t=103, R_eq 3.34): none; #89 (t=116, R_eq 3.19): none; #91 (t=108, R_eq 3.39): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
