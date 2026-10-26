# Audit of 20261026T1100-c40-cips-layered-divide-claim (SIBED, C:metabolic-cell), c41

## Construction (world.py read line by line, with the parent world it extends)
- e (enzyme): drift up the product p with a volume-filling MUSCL face flux, implicit diffusion, uniform turnover
  d (e0 - e). No division, death, growth or shape rule anywhere; bodies are e > 0.5 regions of a continuous field.
- p: made by catalysis kc F e^2 (1-p), decays. F: consumed by catalysis, regrown toward 1 at kF. No term keyed to bodies.
- s (amphiphile): made at ks_s * cat everywhere (catalysis also runs in the bath, at e^2 ~ 0.014 of the body rate per
  area), decays at 0.02, and drifts up grad 4e(1-e). That drift is written against the body field, so by RUBRIC L3's
  quasi-equilibrium clause B counts only if the bodies make most of s. s acts back on nothing.
- E: body matter comes from the uniform turnover feed, not from fuel; fuel drives the catalysis that makes the product the
  enzyme climbs, so a body depends on fuel through its own drive. The dependence is not written in as a decay keyed to F.

## Deciding controls (seed 13, unused)
- B, source share (share.py, original world): fraction of s made inside bodies (e > 0.5) is 0.45 over t=0-2000
  (nucleation), 0.64 over 2000-4000, 0.76 over 4000-6000, 0.83 over 6000-8000; cumulative 0.68 by t=8000.
- B, body-restricted source (world.py SRC_BODY=1: s made only where e > 0.5; ring.py, signed distance): every body
  passes at every sampled time, 6 / 12 / 19 / 19 bodies at t=3000 / 6000 / 9000 / 12000, rim/core 6.8-8.4, rim/out 25-29
  (ring_srcbody_s13.json), as high as the original (claim: >= 5.8, >= 24.5). The layer is the bodies' own.
- E: c40's fork.py on seed 13 from one state at t=12000: fed 21 -> 21 bodies at t=12800; kF=0 21 -> 0 by t=12400;
  kF=0 with turnover off 21 -> 0 by t=12400 (fork_s13.png, log_fork.txt).

## Replication
- labkit pack, seed 13, T=14000 (rerun/): 6 nucleations from the smoothed random field, 13 persistent splits, 0 merges,
  generation 2, 19 bodies; radial s rim/core 6.13, rim/out 25.5, 84/87 individuals membrane-like.
- Numerical variant: s does not act back, so e, p, F and the division history are the parent world's; the parent's
  division survives an isotropic spectral drift (c41 review 20261026T1200, c39's isotropy finding) and dt/2 (c40).

## Flaws and limits
- Divisions stop once the box fills at the lever-rule area fraction (after t~10000 here): the fed steady state is a static
  lattice with no births or deaths, so the life cycle runs only while there is room.
- The layer does no work (s acts back on nothing): it is a boundary layer the body makes, not a wall or a gate.
- E rests on the global fork; growth matter is the uniform enzyme feed, so "eats" means the body needs fuel to run the
  catalysis that holds it together, not that it is built from fuel.
- One unused seed for the pack and the fork.
