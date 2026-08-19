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
M4 composite dynamics — DONE (scorecard + controller audit 2026-02-18):
   RESOLUTION of the round-1 tension: statics depend on (tau,Dv) only via A=tau*Dv
   (exact: steady v gives u = v - tau*Dv*lap v). Binding lived at A=5, motility at
   A~3.2; M4 family fixes A=4 and dials tau (Dv=4/tau) into drift.
   TRAVELING BOND certified: pair bifurcation tau_c=5.636, c_pair=sqrt(0.0560(tau-
   5.636)) r2=.996, OOW tau=6.1 pred/meas 6.3%; bond sep 15.4->14.76 under motion,
   sep_std<0.006px; 3 seeds spontaneous take-off (c spread 0.15%); unpinned (dx
   0.5 vs 0.25: 0.02%); wake-locked tandem shells at sep*=14.78 & 25.68 (~tail
   wavelength 10.9); 3-blob train c=0.143 > pair 0.141 > single 0.123.
   PAIR-ONLY DRIFT ZONE tau in (5.636, 5.748): molecule moves while lone blob
   cannot (audit: pair c=0.0595 vs single c=0.001 at tau=5.7) — natural
   selectivity dial for M5. AUDIT: fresh seed tau=5.8 c=0.0985 vs law 0.0958 (3%);
   off-path A=4 (tau=8, Dv=0.5) replication cascade confirms the mapped ceiling.
   HONEST NEGATIVES: M2's A=5 family can never travel (replication preempts);
   rotation NOT observed (curl-kicks lock or convert to translation); breathing
   dimer metastable ~1500tu then reorganizes to tandem.
M5-prep transport primitives — DONE (scorecard + controller audit 2026-02-18):
   P1 GRADIENT: two couplings. k1-mode: B v=+2.64eps+27eps^2 (r2 .999998), DOWNSTREAM
   = up-gradient, flip bifurcation at eps*~0.01 (B reverses on a second soliton
   branch); level-not-slope limits (safe |b|<=0.03). isod-mode (displace along M3
   iso-line): ZERO-FOOTPRINT force, B v=-0.906eps linear to 0.03, safe to 0.02.
   AUDIT: eps=0.01 fresh seed v=-0.00917 (law -0.00906, 1.2%); OOG eps=0.025
   v=-0.0258 (14% superlinear, area growing — approaching safe edge as they said).
   P2 SELECTIVITY partial: same sign both species; magnitudes 1.3-1.7x; conditional
   sorting via flip window or per-species coupling c_i (B +0.015 vs A' -0.006).
   P3 OBSTACLES: chains don't exist in vvw (pure repulsion) — WALLS SELF-ASSEMBLE
   instead (parked blob at tri-ridge -> static y-spanning stripe; defect->tool).
   Blocking: monotone standoff(eps) 15.7->12.9px. Channeling: two A'-rails center
   B cargo from any y0>=10. AUDIT: y0=14 -> y_rms 0.50px while conveyed 16.6px.
   P4 noise ratchet honest NEGATIVE (soliton too stiff for Kramers hops; positional
   diffusion ~0); deterministic saw conveys one-shot ~12px; circulation redesign
   deferred to round 3 in isod mode.
   FOUNDATIONAL NEGATIVE: species A (169px) is lattice-stabilized at dx=1, grows a
   labyrinth at dx=0.5 — NOT a continuum object (same trap class as M2's dx=1
   ladder). B is continuum-clean (10ktu). Replacement A' (iso-line d=0.65, 36px)
   is compact-metastable (8600tu horizon), usable <=2000tu documented.
   CONTROLLER DECISION (2026-02-18): adopt B + A' at dx=0.5 as the canonical
   working pair for M4/M5; M3's A-species claims get a continuum caveat note
   (port-classification results stand at dx=1, flavor architecture unchanged);
   re-engineering a big continuum species is PARKED (IDEAS) unless a machine
   needs the 6.8x size contrast.

M5 MACHINE — DONE, B6 CERTIFIED (scorecard + controller audit 2026-02-19):
   "RELAY TUG": 3-train locomotive on a 5-tooth isok saw track (L=160, eps=5e-4,
   tau=5.7 pair-only zone, y-channel rails chan_eps=0.002) picks up 3 trough-parked
   cargoes head-on (each locks at the 14.9px shell as NEW LEADER, pusher-tug;
   train speed grows per pickup 0.059->0.073->0.085) and carries them net UPSTREAM
   against the load field. Cert: 3 seeds 3/3 pickups, net_up 757-759px (gate 30),
   efficiency 5.6x do-nothing baseline; jitter 3/3; null drifts -0.5px down.
   CONTROLLER AUDIT fresh seed 71: 6/6 blobs +243..+297px upstream (cargo sum
   ~780px, eff ~5.8x), ncomp frozen at 6, end-spacings 14.7-15.4px (M4 shell);
   null -0.5px. Film run seed 72 identical; god-view film rendered
   (strips/machine_film_audit_s72.gif).
   MECHANISM NOTES: adversary ~50x stronger than vvw at same eps (near-onset
   susceptibility); pair CANNOT climb (dynamic reversal b~0.000-0.005) -> 3-train
   minimum; v1-without-rails BUCKLES after 1-2 pickups (honest negative -> rails);
   6-train sheds rear blob at power ceiling, shed blob PARKS at trough (pair-only
   zone = parking brake) and is re-collected next lap — self-healing relay.
   OPEN (parked): unbinding/unload primitive (delivery = displacement, not
   release); vvw B-B binding for flavor-selective machines; max-train-length law.

THE LADDER IS CLIMBED: M0 existence -> M1 motility -> M2 binding -> M3 flavors ->
M4 composite dynamics -> M5 machine. Every rung certified with controller audits,
honest negatives mapped at each level.

## Phase 2 (user-directed, 2026-02-19): two parallel tracks toward genuine emergence
M6 B-FIELD (searcher blob-bfield): promote the static isok background b to a 4th
   dynamical field db/dt=(gamma*S(u,w)-b)/tau_b + D_b lap b entering exactly through
   the isok channel (-b*(w-u0) in the u-equation = trilinear b-u-w vertex with vacuum
   counterterm). Questions: self-dug profiles (both gamma signs incl. possible
   self-launching), backreaction on motion c(gamma,tau_b) (effective mass), trails &
   stigmergy (mediated two-blob interaction with control), one emergent-structure
   demo, and a b_target teaser (can deposition produce asymmetric sawtooth-like b?).
M7 ROTOR (searcher blob-rotor): rotation as an ATTRACTOR (>=3 revolutions, +-20deg
   kick basin — not a fine-tuned trajectory). Working hypothesis: symmetric pairs are
   wake-frustrated for rotation -> break symmetry structurally. Designs: heterodimer
   rotor (motile species tethered to anchored species; requires CROSS-SPECIES BINDING
   — cross-wired v-channel or second shared inhibitor w2; no-go map acceptable),
   same-species 3-rotor scan, engineered isok ring orbit (planetary demo, labeled
   background-guided).
MERGE MILESTONE (later): "b_target inverse problem" — evolve dynamical b from
   primitive initial conditions into the machine landscape (sawtooth + rails) that
   we hand-built in M5. If reachable, the full machine becomes emergent from initial
   conditions. Parked until M6 characterizes the b-dynamics forward map.
User's labyrinth note parked in IDEAS: labyrinth-prone species + dynamical b ~
   growth/vasculature/territory phenomenology (space-filling curves in living
   systems).

Next phase after M6/M7: world-ification (ports, contracts, alienization) —
controller + user checkpoint.

## Roles
Controller (parent): briefs, audits (fresh seeds + convention-faithful reruns),
PROCESS-style ledger in this file, user checkpoints with films.
Searchers: local loops, metric-lock before certification, results.json + SUMMARY.md
+ strips/ in probes/blobs/<name>/, scorecard message to parent when done.
