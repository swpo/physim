# Evidence pack: fed-vortices-noise (seed 0)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.1 per sqrt(t): additive on ['om'], proportional on ['Y']
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 149s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/B0.1_s0 --seeds 0 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.16 of robust range [0.0014, 0.3622], min area 6 px

## Measurements
- components: final 1, mean 1.2, max 49; occupancy final 0.88
- tracks: 184; persistent (alive >= 50% of run): 0; longest 30 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.00, final 1; holes at thresholds 0.2/0.35/0.5 final [131, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [222, 92, 9], H1 [127, 2, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 3.66/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 60, default): splits 45, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 47, merge/split ratio 1.04, nucleations 1
- channel total drift (end/start - 1): [0.8212, -0.6566, -1383.6124, None]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 0.993, rim/outside n/a (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.283)
  - radial fuel Y: peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside n/a (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.172)
  - radial vorticity (signed): peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside n/a (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.479)
  - radial eating: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 0.992, rim/outside n/a (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.113)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #84 (t=384, R_eq 67.89): none; #66 (t=213, R_eq 67.78): none; #125 (t=807, R_eq 67.46): none; #133 (t=927, R_eq 67.16): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 6 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 6 of 6 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
