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
M1 motility + un-pinning — DONE (controller fan-in 2026-02-18): drift bifurcation
   at Dv=0.65, c=sqrt(0.0299(tau-4.78)) r2=0.993; unpinned (IMEX-FFT dx=0.5, c
   converged 0.6% vs dx=0.25; directions isotropic 0/8 lattice-clustered); 10ktu
   lifetime; corridor k1(-0.75,-0.68) Dv(0.55,0.67] tau(4.78,~5.45); wall
   reflection + soft blob-blob scattering (no merge) logged. AUDITED seeds 23/31.
   TRAP for future: at tau=5 the plain u-only Gaussian IC dies — use symmetric
   centered v,w bumps (kick_d=0) or an explicit kick. Convention documented.
M2 binding / molecules — DONE (scorecard + controller audit 2026-02-18): working
   point P7s = M0 + Dv=2.0, tau=2.5. Bond curve (dx=0.5): TWO-SIDED convergence to
   d1*=15.70+-0.02, basin ~[14.5,19.5], no 2nd minimum <=20; unpinning d* shift
   dx=1->0.5 = 1.8%. AUDIT (controller): fresh stamps on L=64 (periodic-image-safe),
   d0=16.5 & 18.5 -> d*=15.67/15.70. CONFIRMED. Strength: escapes censored >4000tu
   at sigma up to 0.075 (blob itself dies at 0.09) >> 10x relax (36tu). Molecules:
   stable 3-chain [16,16] and equilateral triangle [16.0,16.1,16.1] 3000tu.
   HONEST NEGATIVES: tau=3.0 d*=14.65 is a continuum SADDLE (dx=1 stability was
   lattice pinning — trap confirmed); all M0 (Dv=1) "bonds" are pinned artifacts;
   osc-dominant corners (Dv>=4, k4>=1.7) replicate on pairing; binding window sits
   ~0.1 in k1 from the replication edge. B5 rotation NOT observed (triangle static).
M3 flavors — DONE (scorecard + controller audit 2026-02-18): arch "vvw" = private
   u_i,v_i + ONE shared long-range w (drive (u1+u2)/2); iso-background line
   k1_i=-1.0+d_i*ub, k4_i=1.4+d_i keeps one stable background for all species.
   Species A (k1=-1.0,k4=1.40, 169px broad) and B (k1=-1.651,k4=2.15, 25px sharp),
   both Du=0.65. B1 both species 1e4 tu + noise (audit: fresh seed 41 persistent,
   3000tu). B3 port-classification 20/20 full & w-only & size (audit: A+B d0=8
   repel to 12.1, flavor conserved, seeds 51/52). Encounter table: pure repulsion
   at d0>=6 except AA d0=6 deterministic MERGE (only non-conserving event).
   HONEST: blobs non-oscillatory (frequency not a signature); B's k1/k4 windows
   1.28-1.29x (marginally under 1.3 on 2 dials, >=1.3x on 3 others).
   FOR M4/M5: B = natural cargo (small, weak w-print); per-species tau windows
   (A 1.5-4.0, B 1.5-6.0+) leave room for species-selective drift.
M4 composite dynamics in background fields (round 2)
M5 machines: upstream transport (round 3)

## Roles
Controller (parent): briefs, audits (fresh seeds + convention-faithful reruns),
PROCESS-style ledger in this file, user checkpoints with films.
Searchers: local loops, metric-lock before certification, results.json + SUMMARY.md
+ strips/ in probes/blobs/<name>/, scorecard message to parent when done.
