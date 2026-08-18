# BLOBS program — dissipative-soliton matter and blob machines
(user-directed redirect 2026-02-18; supersedes immediate engine build of slime/teacup —
slime-lifecycle remains the parked fallback shipping candidate)

## Vision (user's ladder, verbatim spirit)
1. Blobs = persistent localized excitations of continuum fields (dissipative solitons /
   "instanton-like" objects), not painted sprites.
2. Multi-component fields -> multiple FLAVORS of blob.
3. Field-mediated interactions -> mechanisms for blobs to affect each other.
4. A BINDING mechanism -> bound pairs / larger structures at preferred separations.
5. Composite structures get NEW dynamics in background fields (e.g. single blob spins;
   bound pair shows visible mutual rotation).
6. Self-assembled MACHINES: blob configurations that do work — e.g. transport a target
   flavor UPSTREAM against a background field/potential.

## Physics anchor
Three-component reaction-diffusion (Purwins/Schenk gas-discharge class):
  du/dt = Du lap(u) + lam*u - u^3 - k3*v - k4*w + k1     (activator)
  dv/dt = (u - v)/tau   + Dv lap(v)                      (slow inhibitor)
  dw/dt = (u - w)/theta + Dw lap(w)                      (fast long-range inhibitor)
Known phenomenology in the literature (real-world anchor: planar gas discharges,
also BZ microemulsions, semiconductor resonators): stationary & traveling spots,
drift bifurcation, oscillatory tails -> soliton "molecules" at discrete separations,
rotating bound states, scattering/annihilation/generation. This is exactly the ladder.

## Honesty rules (inherit program-wide + new)
- Blobs may be SEEDED as initial conditions, but persistence, motion, interactions,
  binding, and machine function must be autonomous physics. No scripted events.
- No per-blob bookkeeping in the dynamics: fields only. Blob identity is a MEASURED
  emergent property (connected components / tracking), never a state variable.
- Machines must be assembled from the same field physics (possibly with static
  background/boundary fields as the "environment"), not special-cased code paths.
- Negative results are first-class deliverables. Known traps: lattice pinning of
  small blobs (Day-0 finding), explicit-Euler dt blowup at high Dw (dt<dx^2/(4Dw)),
  replication cascades (spot soup), threshold-metric artifacts.

## Gates (this program measures OBJECTS + INTERACTIONS, not layer hierarchies)
- B1 EXISTENCE: single blob lifetime >= 1e4 tu, noise-robust (survives sigma such that
  sigma/amp >= 1e-3), non-replicating; parameter window width >= 1.3x in >= 2 dials.
- B2 MOBILITY: a traveling regime with steady measurable speed c(dial) smooth+monotone
  near the drift bifurcation; stationary<->traveling reachable by ONE dial; unpinned
  (speed survives grid-refinement check dx -> dx/2).
- B3 FLAVORS: >= 2 blob species coexisting in one world, port-distinguishable
  signatures; flavor conserved under encounter OR documented conversion rules.
- B4 BINDING: bound pair at discrete separation(s) d*; lifetime >= 10x single-blob
  relaxation; measurable bond strength (escape time vs noise, or restoring-force
  curve F(d) with a zero crossing + negative slope).
- B5 COMPOSITE DYNAMICS: bound structure shows qualitatively new motion absent in
  singles (mutual rotation / co-propagation / spinning in a background field);
  measurable order parameter (angular velocity, pair speed).
- B6 MACHINE: a configuration that transports a target blob AGAINST an imposed
  background gradient, repeatedly (>= 3 transport cycles), with efficiency metric
  (net upstream displacement per cycle / gradient strength). Assembly itself may be
  manual configuration FIRST (existence), self-assembly is the stretch goal.
- B7 BUDGET: <= 5 min/candidate single-core at the working L; document tu/sec.

## Milestones
M0 existence (DONE Day-0, controller probe): persistent blob at
   (lam=2, k1=-0.7, k3=1, k4=1.5, tau=3, theta=0.7, Du=Dv=1, Dw=20, L=96, dt=0.01);
   area~26px stable 2000 tu, noise-robust to 2e-3; neighbors: k1=-0.9 dies,
   k1=-0.5 & k4=2.5 replicate into spot soup. Blob is LATTICE-PINNED (disp=0 under
   noise) — motility is not free, needs drift bifurcation (M1).
M1 motility + un-pinning (searcher: blob-motility)
M2 binding / molecules (searcher: blob-binding)
M3 flavors / multi-species architecture (searcher: blob-flavors)
M4 composite dynamics in background fields (round 2)
M5 machines: upstream transport (round 3)

## Roles
Controller (parent): briefs, audits (fresh seeds + convention-faithful reruns),
PROCESS-style ledger in this file, user checkpoints with films.
Searchers: local loops, metric-lock before certification, results.json + SUMMARY.md
+ strips/ in probes/blobs/<name>/, scorecard message to parent when done.
