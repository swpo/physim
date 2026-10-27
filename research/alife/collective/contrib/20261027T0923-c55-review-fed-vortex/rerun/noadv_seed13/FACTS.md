# Evidence pack: fed-vortices (seed 13)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1001 frames x 150 steps x dt 0.02 = time 3000; grid [128, 128]; wall 321s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/vort/noadv --seeds 13 --frames 1000 --spf 150 --no-movie`
- segmentation: matter > 0.28 of robust range [0.0, 0.2106], min area 6 px

## Measurements
- components: final 54, mean 53.1, max 54; occupancy final 0.16
- tracks: 79; persistent (alive >= 50% of run): 54; longest 1001 frames; alive start-to-end: 28
- size of persistent tracks: max/min area ratio 4.56 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [54, 54, 54], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00333/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 60, default): splits 15, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.4317, 0.0131, 13193.6016, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 504: holes 0, rim-vs-core 0.33, rim-vs-outside 0.63, heterogeneity 0.21; core [0.748, 0.174, 0.881, 0.636] rim [0.569, 0.271, 0.786, 0.389]
  - track 1 at frame 504: holes 0, rim-vs-core 0.74, rim-vs-outside 0.31, heterogeneity 0.19; core [0.804, 0.127, 0.069, 0.699] rim [0.412, 0.366, 0.269, 0.149]
  - track 2 at frame 504: holes 0, rim-vs-core 0.72, rim-vs-outside 0.33, heterogeneity 0.20; core [0.797, 0.124, 0.906, 0.68] rim [0.411, 0.369, 0.704, 0.161]
  - track 63 at frame 513: holes 0, rim-vs-core 0.53, rim-vs-outside 0.56, heterogeneity 0.21; core [0.81, 0.141, 0.911, 0.739] rim [0.535, 0.293, 0.769, 0.338]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 322 components >= 12 px at frames [168, 336, 504, 664, 832, 1000]):
  - radial |vorticity|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.709, rim/outside 38.8 (aggregate of 322 individuals; 0/322 membrane-like individually; rim level 0.688)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 23.5, rim/outside 0.789 (aggregate of 322 individuals; 0/322 membrane-like individually; rim level 0.553)
  - radial vorticity (signed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.951, rim/outside 1.05 (aggregate of 322 individuals; 0/322 membrane-like individually; rim level 0.513)
  - radial eating: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.576, rim/outside 54.9 (aggregate of 322 individuals; 0/322 membrane-like individually; rim level 0.539)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1512, R_eq 3.91): none; #1 (t=1512, R_eq 4.07): none; #2 (t=1512, R_eq 4.3): none; #63 (t=1539, R_eq 3.78): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
