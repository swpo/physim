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
M6 B-FIELD — DONE (scorecard + controller audit 2026-02-19; 180 runs):
   b as 4th dynamical field db/dt=(gamma*S-b)/tau_b + D_b lap b through the isok
   channel; vacuum exact with dynamics on; gamma=0 reproduces M4/machine to 0.02%.
   HEADLINE — SELF-LAUNCH (autophoresis): a parked blob BELOW the drift threshold
   (tau=5.7 < 5.748) spontaneously launches for gamma >= 0.005 by climbing its own
   lagging saturated hill; c = 0.209*gamma^0.341 (r2=.991). AUDIT: fresh seed
   g=0.05 c=0.0755 vs law 0.0752 (+0.3%); OOG g=0.15 -6.4%; sub-threshold creep
   under noise documented (their threshold is noiseless). Backreaction: drag -12%
   (g=-0.05), plow-boost +6% (g>0), SELF-TRAPPING g<=-0.07; trail law
   b(s)=B0 exp(-s/(c*tau_b)) to 0.002%. BF3 stigmergy certified w/ controls
   (trail-mediated attract/repel +-3px gates, 2 seeds each sign). BF4 honest
   partial: noiseless self-dug-channel mechanism certified; noisy confinement
   fails (weak transverse pumping); space-partition clean negative (wake
   clustering wins). BONUS replicated by audit: b-ASSEMBLY — 3 blobs beyond the
   bond basin (d0=24-26) collapse via shared halo well onto M4 shells (fresh
   seed/geometry: assembled by t=310); their n=1 noiseless trimer then
   SELF-LAUNCHED (c=0.076) — my noisy replica assembles but wanders (documented
   sensitivity). TEASER: one-way circulation writes an asymmetric sawtooth-like
   standing b (lap-decay 0.49 vs 0.46 predicted) — the M5 track shape is a natural
   fixed point of asymmetric motion + relaxation. (original brief follows)
   [BRIEF] promote the static isok background b to a 4th dynamical field db/dt=(gamma*S(u,w)-b)/tau_b + D_b lap b entering exactly through
   the isok channel (-b*(w-u0) in the u-equation = trilinear b-u-w vertex with vacuum
   counterterm). Questions: self-dug profiles (both gamma signs incl. possible
   self-launching), backreaction on motion c(gamma,tau_b) (effective mass), trails &
   stigmergy (mediated two-blob interaction with control), one emergent-structure
   demo, and a b_target teaser (can deposition produce asymmetric sawtooth-like b?).
M7 ROTOR — DONE (scorecard + controller audit 2026-02-19; 108 runs):
   ROTATION IS AN ATTRACTOR. xv arch (6 fields; ONLY coupling = cross-v eta drive;
   eta=0 exactly M4; vacuum exact for any eta). Heterodimer M(tau1)+S(tau2=2.5),
   eta=0.1, d0=8: SPONTANEOUS steady rotation (noiseless self-start from round-off;
   CW/CCW degenerate). omega(tau1) 10 locked pts 0.0035->0.0259 (5.52-6.10),
   monotone; grid 0.009%; 10ktu longrun 17.4 revs, sep 8.437+-0.004; survives
   sigma=0.04. AUDIT: fresh seed omega=0.011114 vs 0.011062 (+0.5%), sep 8.439,
   anchor net 0.6px; onset-region tau1=5.60 -> omega=0.0074 on-curve; cross-bond
   eta=0.05 from d0=12 -> d*=7.976 EXACT (sep_std=0.0). ROTOR-ONLY ZONE: spins at
   tau1=5.52 < pair tau_c 5.636 < single 5.748 (hierarchy: single-static <
   pair-travel < rotor-spin). Mechanism certified by decomposition (eta12-only
   rotates = passive pivot; eta21-only static): anchor's v-halo = self-assembled
   circular rail, predicted from stamp math BEFORE first run (d* pred 7-9, obs
   7.5-8.0). RT2: first cross-species bond in program; eta usable [0.05,0.125];
   HONEST: static eta=0.1 slow-slow dimer metastable (balloons ~1700tu) but the
   ROTATING dimer never balloons (rotation stabilizes the bond); no-go quantified
   (w monotone repel-only; v is the unique sign-changing mediator). Same-species
   3-rotor exists but knife-edged (+-20deg converts to translation — frustration
   hypothesis confirmed as basin property). RT3 honest negative: at machine-safe
   eps the bond outcompetes the ring valley (planetary film IS the heterodimer).
   (original brief follows)
   [BRIEF] rotation as an ATTRACTOR (>=3 revolutions, +-20deg
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


## LEVELS DOCTRINE (user, 2026-02-19 — program operating structure)
L1 field level: everything dynamical incl. b; study what the physics grows.
L2 background level: hand-written static b; study what landscapes can host.
L3 molecule level: certified components (bonds/trains/rotors); study composition.
Rule: higher-level findings must be REDUCIBLE one level down by a learned process —
L2 landscapes reachable as L1 fixed points (inverse problem; teaser: sawtooth IS a
natural L1 attractor), L3 components carry L2/L1 certificates. Higher levels buy
exploration speed; reduction buys legitimacy. The two phase-2 tracks are stacked,
not merged: L2 discovers what is worth wanting, L1 discovers what can be grown,
and the reduction map is itself a research object.


## PHASE 3 (user, 2026-02-19): bottom-up AND top-down in parallel
Bottom-up (L0, probes/blobs/l0/): equation-space search through the G0 algebraic
funnel (temporal stability, bistability, spatial-tail eigenvalues — shell spacing
predicted to 1%) + assay battery; l0-sampler (random + theory-guided) and l0-evolver
(merge = block composition validated by RECONSTRUCTING our own vvw/xv jumps;
mutation = theory-coord jitter). Fan-out to rented Prime compute after local
validation. Learn: density + geography of interesting physics in equation space.
Top-down (L3->L2->L1 reductions): blob-factory (fulfillment-center primitives:
roller->cargo advection — rotation as LOCAL drive in rotor-only zones where nothing
translates; unload via static eta(x) null zones — eta enters like isok, vacuum-exact;
species fork/sorter; one glued two-mechanism demo) and blob-genesis (close the
teaser loop: does the self-written sawtooth FUNCTION as a track? does an orbiter
dig its own ring racetrack? what infrastructure self-organizes from blobs + noise
+ dynamical b alone). Learn: which landscapes/machines are growable (reduction maps).
Grounding target: the "Amazon fulfillment center" world (conveyor network with
forks, merges, control arms, rollers) — north star for L3 composition and for L0
behavior descriptors. Bottom-up and top-down teach different things; run both.


### blob-genesis — DONE (scorecard + controller audit 2026-02-20)
REDUCTION MAP (L2 features growable at L1?): tooth YES (functions native: parks
+ brakes; audit: fresh noisy park slid 16.9px to trough, stopped, 0.6px residual);
ramp YES (trail law); rail YES and FREE (groove transverse profile self-rails,
FWHM 5.5px — hand-built world needed a separate chan term); ring YES (rotor writes
closed ring r=8.4 depth .0055 closure .62 at g=-0.05 tb=1000; deeper rings must be
dug slowly — greedy g self-traps into C-arcs); dock YES (trough=brake); racetrack
conveyor YES at 4x amplitude (SHAPE-ONLY label; audit: fresh immobile blob parked
on frozen ring at NEW angle self-launched into 5.7-rev orbit r=8.45 omega=.0091);
BLOB-FROM-NOISE NO (theory-backed null: vacuum-exact coupling is quadratic in
deviations -> gamma cannot destabilize vacuum; nucleation window sigma>(0.2..0.5]
lands directly in 54-comp soup while blob-death is 0.09 — no trails-beget-blobs
channel in this coupling class).
KEY NEW LAWS: chi=v/slope 10-40x better for self-written (near-onset response
sublinear in slope — hand tracks WASTE slope); amplitude ladder park->mush->
circulate->diode (boundary in (2,4)x native); speed-matching rule (guide depth must
scale with traveler momentum); one-way DIODE at machine amplitude (kicked against
tooth: reverses).
M5 landscape CONFIRMED a natural L1 fixed-point family; the single exogenous step
in the reduction is the FREEZE itself (gamma->0 limit). Films shipped.


### l0-sampler — STAGE 1 DONE (scorecard + controller audit 2026-02-20)
Parity 5/5 (rotor omega to 5 digits); G0c validated (M4 shell 0.5%). Yield curves
(the deliverable): uniform 2 alive/100 (funnel 2ms, assay dominates 40s), jitter 49
alive/100 + 14 bond/100; throughput 30 cand/hr/core mixed; ~1 novel world per 50
core-hours uniform. Jitter-by-ref: VVW 74%, XV 76%, M0 38%, BFIELD 36%, M4 23% alive.
HEADLINES: (1) transferable chemistry law d*/wl(G0c) — their n=30 gives 1.348+-0.075;
controller fresh-jitter audit: 1.208-1.210 two-sided (1.8sig low) -> law is real but
band wider (~1.2-1.5); order-of-shell physics confirmed. (2) uni_3034 NON-OSCILLATORY
BINDING (monotone tails yet clean bond) — AUDITED: d0=14 -> d*=27.857 (3rd-decimal
match), d0=24 -> 28.75 (wide/flat well or 2nd shell), d0=10 merges. New mechanism
class (competing monotone tails), n=2 worlds (uni_3050 exciting-K also novel).
(3) u0-designation is a GENE (certified vacua = MIDDLE root, channel-stabilized).
(4) blobs live near the cubic fold (fold-dist ~0.03) -> log-jitter fold distance.
Stage-2 fixes queued: chem_box recall bug, adaptive tau ladder (A3 +-20% too coarse
for +-1% drift windows), A2 wrap filter. POD FAN-OUT: controller decision pending
(economics: jitter maps islands 25x faster than uniform finds new ones).


## LIT REVIEW (2026-02-21, litreview/ — 132 sources; verified spot-checks by controller)
REINVENTION DISCLOSURE (now on public page): our system IS Schenk/Or-Guil/Bode/
Purwins PRL 78:3781 (1997); blobs = dissipative solitons (Adv.Phys 59:485 review).
Known: M0 existence, M1 drift bif + sqrt law, M2 tail-quantized molecules (+ bond
forces measured experimentally in gas discharges), rotating bound states incl.
rotation-before-drift (Moskalenko EPL 63:361 — anticipates rotor-only ordering),
labyrinthine instability (Hagberg-Meron), self-replicating spots (Pearson),
self-launch mechanism class (camphor/autophoresis/walkers/delayed-feedback DS),
trail formation dials (Schweitzer active walkers), diode (chemical diode).
SURVIVING NOVELTY: pair-only TRANSLATION zone as transport selector; nonreciprocal
heterodimer rotor design + omega(tau1) law + 3-level motion hierarchy; RELAY TUG
(no published soliton-train hauling soliton cargo upstream w/ shedding/self-heal);
self-dug ring that later guides fresh blobs; chi=v/slope 10-40x self-written law;
c=0.209 gamma^0.341 + trail-memory law as RD-blob quantitative results; G0 funnel
as 20,000x QD pre-filter (spatial dynamics is standard THEORY, unused as search
filter); d*/wl band matches theory (core-phase-set band).
FRAMING FIXES ADOPTED: active-particle ratchet (Curie principle — passive transport
impossible; our machine works because blobs are active); Buryak-Akhmediev
stable/saddle alternation => "stable bond at predicted saddle distance" = pinning
alarm (adopted as artifact detector).
TOP STEALS QUEUED: S1 numerical continuation/freezing method (pde2path, Beyn-
Thummler) -> machine-precision tau_c/d*/omega branches + fold certificates
(upgrades l0 funnel + replaces bisection hunts); S2 Kramers-Moyal drift
reconstruction from noisy tracks (Bodeker PRE 67:056220 — their exact use case was
noise-covered drift bifurcations) -> free bond curves + sub-threshold
certification from longruns; S3 merge-milestone pipelines: differentiable-RD
inverse design (our IMEX step is differentiable) + POET transfer gate; Flow-Lenia
parameter localization = the TAMED replication-with-inheritance mechanism if we
ever want evolution inside a blob world.


### l0-evolver — DONE (scorecard + controller audit 2026-02-21)
Validation gate PASSED both directions (merge ops reconstruct vvw AND xv exactly,
including the honest historical dead-end for M0+M0 share-w). RESEARCH ANSWER:
recombination >> perturbation — merge 7.7 alive-cells/100assays vs jitter 5.3 vs
mutate-only 3.2 vs uniform 1.9; multi-species coexistence cells are MERGE-ONLY
(13 vs 4 vs 0); all cross-species physics cells (5 cross-bond, 2 rotor, 5 drift)
are evolver-found. ROTOR REDISCOVERED without the recipe: rh1_7000 (asymmetric
eta=0.202, taus 5.9/5.0, omega=-0.0324, sep 8.72) — CONTROLLER AUDIT: exact
replication (omega -0.0324, sep 8.7207) after applying their dressed-poke
convention (bare pokes die in this world; dress=0.6 channel bumps required —
4TH convention-faithfulness lesson, now standard audit practice). Also: first
3-species triple-persist world (e1_9508), slow_tanh-merge rotor (e1_9513).
Honest negatives: share_chan fails G0a ~50% on random pairs (background matching
is structural), cross_edge eta>~0.15 replicates (certified window generalizes).

### Stage-2 pod fleet (2026-02-21): 8 CPU pods live (l0s2-a..h), 32 workers,
seeds 100-131, ~2500 candidates in flight; ~5% at first check — ETA 8-10h
(full-battery candidates slower than smoke estimate). Harvest+merge = controller.
Costs: a=datacrunch $0.028/hr, b-h=nebius $0.099/hr => ~$0.72/hr total.


### blob-factory — DONE (scorecard + controller audit 2026-02-21)
Fulfillment-center primitives, L3->L2. Engine: rotor/sim.py + vacuum-exact static
FIELDS eta_i(x,y) (coupling geography — enters v_i like isok enters u) and
per-species b_i(x,y). Smoke = M7 anchor to 6 digits.
1) ROLLER split verdict: brief-config advection NULL (|vtan|<=6e-5; cargo reels to
   anchor ring instead; rotor converts to S-M-S PENDULUM librator T~307tu —
   hierarchy extended bond<travel<rotate<librate). CERTIFIED advection at deep
   coupling (tau1=6.0, eta21=0.2, cargo on-ring): vtan=1.4e-3 sign-locked, null
   exactly 0 — positioner (~0.07px/rev), not circulator. Roller also EXTENDS
   same-species capture range (d0=20-22 vs basin 19.5).
2) UNLOAD DOCK certified 3/3+controls via eta-xbox null zone. KEY NEW PRIMITIVE:
   NEAR-ONSET CARGO — deep-static S is untowable (well ceiling << carrier speed;
   mutual-eta carriers replicate; eta is a ~100x machine-scale |k1| kick), but
   tau2=5.60 (rotor-only zone) cargo still parks alone yet responds 7-8x stronger:
   locks at 8.46, tows at FULL pair speed 155px; eta21 0.1 tows / 0.05 drops.
   (M5's near-onset adversary physics inverted into the tow mechanism.)
3) SPECIES FORK certified: per-species rails 24/24 purity + timescale-asymmetry
   speed-sorting dial (M 0.074 vs S 0.0047 px/tu).
4) GLUE certified (v4 3 seeds + mirror; CONTROLLER AUDIT fresh seed 9: full chain
   reproduced — tow, dock release 4px past x1, fork-sort to 17.75px off-lane park,
   carrier laps 293px, ncomp frozen). INTERFERENCE MAPPED: composition rule =
   interaction footprints (tow-well reach 15px / rail walls / carrier lane) must
   be DISJOINT at every handoff; violations reproduce as fly-by drag, re-capture,
   or crotch-trap head-on split. Glue design = geometric margins, not new physics.
DESIGN LAWS: near-onset cargo (tau2 dial = cargo hot/cold switch); eta(x,y) legal;
eta12<=0.05 budget for traveling carriers; 15px parking rule; crotches are traps.


## PHASE 4 (2026-02-21): machine v2 spawned; L0 harvest pending
blob-machine-v2 (sub-6e468dbb): multi-cargo logistics line from certified parts —
V2a throughput (3 deliveries, queue integrity via 15px rule), V2b two-way sort
(mixed cargo, both branches), V2c closed loop (dock-to-dock series composition),
V2d stretch: first L1-GROWN component (genesis groove) inside an L2 machine.
Reuses factory/sim.py; glue anchor must reproduce before building.
Pod fleet: 23/32 shards done at spawn time; harvest + MAP-Elites merge + pod
termination = controller work when workers finish.


### l0-sampler stage-2 ANALYSIS — accepted with controller audit notes (2026-02-21)
Yields v2: jitter 51.2%/24.1% alive/bond (stage-1 prediction confirmed); uniform
0.47% alive (novelty ~1/600); best line e1_9508 (evolver 3-act elite) 89.8%/41.8%.
Fold-shell law at n=3195: alive median fold-dist 0.020 vs dead 0.2.
Atlas: 404 cells, top-10 tour incl. T1 first 3-flavor bonded matter (4 cells),
T2 plateau-bond family (41 cells), T3 SPEED RECORD c=0.204 — CONTROLLER AUDIT
CONFIRMED EXACTLY (kicked act-1 poke: c=0.2038; 5th convention lesson: poke the
right SPECIES — act 0 of that world replicates), T4 13 self-launching M6 jitters.
d*/wl law v2 (830 bonds): first shell 1.369+-0.126, ladder d*=(1.37+0.55k)*wl.
A3 postmortem: ladder works (M4 control 0.05%); "0 travelers" was A1 masking —
22 already-travelers unmasked by kicks (stage-3 fix: kick_px=0.5 always).
AUDIT CORRECTION on the plateau-bond mechanism: their tanh-ablation attributes
binding for the uni_3034 FAMILY; my ablation of the INDEPENDENT invention
s2_128_26 still bonds with tanh zeroed (d* 14.06->14.95) — that world's binding
is NOT tanh-driven; mechanism unattributed (possibly a second non-osc route).
Their "unablated" caveat was correct; family claim stands, exemplar corrected.
Onset-point s2_101_61 partially verified (coast not steady under my poke protocol;
ladder-internal protocol differs — flagged, not blocking).
STAGE-3 approved-in-principle (targeted ~100-150 core-hr): kicked-A1 travel census,
plateau-bond design rule, 3-flavor encounter tables; blind uniform only with
fold-dist logU sampling. PENDING machine-v2 fan-in first.


### blob-machine-v2 — HONEST PARTIAL, accepted (scorecard + controller audit 2026-02-22)
V2a FUNCTION CERTIFIED (3/3 seeds + controller fresh-seed 7 audit: 3 cargoes swept
into a 4-convoy behind a sacrificial PLUG, dock-released, fork-sorted to the y=20
floor as a 15.3-15.5px bond-shell stack; census frozen; cycle 215+-5tu; functional
throughput 0.6 deliveries/1000tu; anchor reproduced bit-exact first).
FAILED GATE (why partial): the delivered bonded 3-stack is itself a SELF-PROPELLED
TRAIN (shuttles +-9px; isolation control proves intrinsic). Fix blocked by a
3-law cascade (all quantified w/ seeds+controls):
- STACK-SAFETY: parked n-stacks self-propel unless tau2 < tau_c(n); tau_c3 in
  (5.55,5.60] (sqrt-law extrapolation consistent).
- BLADE-LOAD: blade core-gap compresses with chain-load x speed / cargo mobility;
  split floor ~5.3-5.4px (tau2=5.50 at c=0.072 splits 3/3).
- SLOW-CONVOY BUCKLING: c~0.044 blade contact transversely unstable (~2 laps).
=> for n=3+plug the tau2 window is empty/knife-edge IN THIS ARCHITECTURE.
KEY DISCOVERIES: PUSH-CAPTURE BLADE (head-on meets at eta 0.05-0.08 = stable FRONT
capture riding 7.1px ahead at full speed; railed lanes make swing-around
impossible -> bulldozer convoy is THE throughput machine on rails); PLUG primitive
(sacrificial blade rider converts the never-sortable blade slot into
infrastructure; 4 blade trap limit-cycles mapped); interference map extended to
7 entries / 3 new footprint types. n=1 end-to-end certified in 3 geometries.
V2b/c/d not reached (law cascade consumed budget; V2b needs species-tagged rails
or per-cargo eta — tau-contrast cannot split one blade's chain).
CONTROLLER NOTE: "machine physics" is now producing laws faster than machines —
stack-safety/blade-load/buckling are exactly the content an agent-facing world
would examine. World-ification calculus improved.


### Stage-3 launched (2026-02-22): 4 pods (l0s3-a..d), 17 shards
Census (996 kicked act-indexed pokes) on a-c; island+plateau+encounters on d.
EARLY HEADLINE (local, controller-verified exactly): s2_107_48 DECOMPOSED —
act1+2chans is a STANDALONE 3-FIELD ENGINE, c=0.2038 bit-identical alone
(act0 = slaved cargo via one W entry). Statics A=2.53 (NOT M4's A=4; NOT
near-onset — a different motility mechanism). NEW SPEED RECORD c=0.2516 at
Dv*0.9 (verified). Robust +-10% all dials. Machine-v3 carrier candidate:
3 fields, 1.8x M4 pair speed, cargo attachable by one W entry.
V4 assays validated on certified anchors (a2_cross reproduces XV d*=7.85;
stack_probe reproduces M2 3-chain 15.66px parked; M4 shuttle control).


### Phase 4b (2026-02-22): blob-loop spawned — track-dependency clarification
User correctly flagged: top-down need not wait for stage-3. Dependency truth:
stage-3 census/island = bottom-up; plateau STACK PROBES + encounter tables =
top-down QUESTIONS routed through L0 tooling (machine-v3's n>=3 throughput fix
shops there). But V2c (closed loop) and V2d (first L1-grown component in an L2
machine) need only certified parts -> blob-loop (sub-8a8acb27) runs them NOW,
n=1 cargo regime, machinev2 engine reused. v3 (n>=3 convoy) waits for harvest.


### Stage-3 pod-d results harvested early (2026-02-22; census still running on a-c)
STACK PROBES (the machine-v3 gate) — ANSWERED:
- s2_128_26 plateau stacks (14.1px): PARKED at n=2 AND n=3, INCLUDING under working
  noise. THE STACK-SAFETY FIX EXISTS: plateau-bonded cargo stacks do not shuttle.
- M4 control: parked noiseless but SHUTTLES under noise at n=3 — reproduces
  machine-v2's failure exactly (control validates the assay).
- uni_3034 (27.9px): DIES in the stack assay (both n, both noise) — its blobs
  do not survive this assay geometry; family usable only via s2_128_26-class
  members. Honest mixed result.
ISLAND (engine_10748 composite): 19/33 points travel; tau +-10% flat at c=0.2038;
NEW SPEED RECORD c=0.2788 at Du*1.1. Engine is robust and has headroom.
=> machine-v3 parts list forming: engine carrier (c 0.20-0.28) + plateau-bond
cargo stacks (park-safe) + species rails pending encounter tables.


### l0-sampler stage-3 CENSUS — accepted (controller audits 2026-02-23)
Carrier catalog: 24 travelers ranked; RECORD c=0.3036 (s2_118_41) verified; ENGINE
COMBINED-DIAL RECORD c=0.3439 (Du*1.1 + Dv*0.9) CONTROLLER-VERIFIED EXACT — 3-field
world, cheapest sim cost, 2.4x hand-designed best. BFIELD-line catalog entries are
lower bounds (still accelerating at assay T). Motility geography: BFIELD 16.4% >>
e1_9513 4.3% > rh1 3.9% > XV 1.5% > M0/M4/VVW 0% — exactly 2 mechanisms (stigmergic
self-launch; two-timescale engines A=2.5-4.5); census rate 2.4% matches stage-2 A3
onset 2.7% (independent protocols agree). 6 stage-2 masked travelers honestly
reclassified as coast-edge.
PLATEAU DESIGN RULE: tanh = existence+capture gate; d* SET BY THE SLOW ID CHANNEL
(tau_slow dial -> d* 20-30px menu; shells 20.8/24.5/28.5 at tau_slow*0.5); spacing
decoupled from tail wavelength. s2_128_26 attribution SETTLED as same family (two
parallel tanh paths — W-drive and K-feedback; cutting either alone keeps the bond;
explains my earlier single-cut counter-result. Flagged not blocking).
STACKS: uni_3034 pod-death was a DRESSING-OVERDOSE job-spec artifact — bare re-run
parks at 29.34px n=3+noise; CONTROLLER RE-VERIFIED (com_net 1e-4). Cargo menu:
d*=14.0px (s2_128_26) or 20-30px (tau_slow dial). M4 control shuttles 86px (law
reproduced).
ENCOUNTERS: NOMINEE s2_111_17 (zero replication in 18 assays; cross-bond d*=11.1;
species 0 = pure repeller = fence/blade material). s2_101_58 = PREDATION (conserved
kill direction) — world-catalog primitive, parked.


### blob-machine-v3 — ACCEPTED (scorecard + controller audits 2026-02-23)
FIRST MACHINE FROM SEARCHED PARTS. V3-0 PASS: combined world = direct-sum(engine_
10748, s2_128_26) + ONE coupling move found by systematic search: "mimic eta=0.6"
(engine act writes 60% phantom-cargo imprint into cargo channels, one-way).
Engine c unchanged to 4 digits; cargo parks (1e-3px); tow = PUSH blade at 4.3px
standoff (pull impossible: engine ahead runs away). Coupling no-go table: weak
cross-v 0.05 no grip / 0.10 splits engine; binder-only, repeller-only, and
pairwise channel writes all fail or kill cargo — binder+repeller TRIPLE imprint
is the minimal grip. RELEASE certified: eta->0 mid-run parks cargo instantly
(7e-15 px) + architectural flyby immunity.
CONTROLLER AUDITS: exact noiseless tow replicated (drag 131.27px, dur 660 —
deterministic, 5-digit match); fresh noisy seed 9: lock exists (sep 5.0+-0.9,
cargo at c=0.144) but lock windows shorten to ~100-200tu under sigma=2e-3
(NOISE CAVEAT recorded: noiseless locks indefinitely; noisy tows are
lock-slip-relock — the certified sequential assembly ran noisy and still
delivered, so functionally tolerated).
V3-1 PASS (amended metric, documented): pre-bonded 3-stack tow is a mapped no-go
(merge/tear/slip, 9 variants); amended mode = SEQUENTIAL single-cargo pushes +
dock assembly: 3 noisy seeds delivered a parked bonded 3-stack (spacings
13.55-14.02 = certified d* well; hold drift <2e-3 px/800tu). Release timing =
outer control loop (in-genome docks mapped: stall dial holds grip; frozen-rail
amp 0.35 nucleates engine copies / 0.03 harmless-weak).
COST: 6.3 core-hr, 69 sims, all L=96. The engine and cargo came from blind
uniform search; only the coupling was designed-by-search here.


## PHASE 5 (user, 2026-02-23): metrics-gated complexity search + bounding structures
User verdict on bottom-up: mechanisms found, complexity not — BECAUSE the assays
only see single/pair short-horizon behavior (measurement-limited negative). Plan:
(1) l0-metrics (sub-827fc746): design + VALIDATE complexity descriptors (soup assay
    d1-d6: population dynamics, emergent-timescale ratio, spatial order, motion
    structure, bond-network churn, b-memory) against 7 ground-truth worlds spanning
    boring->designed-complex. Hierarchy toolkit reused from world-search
    (hier_metrics.py — finally pointed at the atlas). Deep evolutionary search FOR
    complexity is GATED on this validation ("metrics that cannot rank known
    complexity are worthless").
(2) blob-membrane (sub-287b3736): bounding structures ladder — R1 closed rings
    (N-blob molecules with pi_1 != 0; square4 exists but is PINNING-ERA — continuum
    check mandatory; alternating-species xv rings as fallback brace), R2 operational
    membrane definition (in/out asymmetry + crossing barrier curve), R3 cargo-in-
    cell (confined blob, the film target), R4 coupled interior->membrane motion.
    User's long arc: composition inside a membrane affecting membrane motion =
    cell-like compartments.


### l0-metrics — ACCEPTED (scorecard + controller audit 2026-02-23)
Complexity battery v1 LOCKED and validated: 7 ground truths ranked sanely
(m0 3.1 << coex 23 < m4 28 < xv 35 < bf 40 ~ pred 41 < mv3 43), zero seed
overlap between groups, seed-3 out-of-sample, T=2500 half-cost mode preserves
ordering. CONTROLLER AUDIT fresh seed 7: m0=3.1 (exact), xv=37.5 (top of band).
Honest disagreements documented (static coexistence scores low absent dynamics —
gate on n_species if wanted; mv3 wins via division-of-labor roles component C7).
Known limits: late-assembling rotors missed, tracking breaks >1.2px/tu, 12-blob
calibration. DEEP SEARCH NOW UNGATED.


### blob-membrane MID-RUN findings (2026-02-23; final scorecard pending)
R1 CERTIFIED: closed rings N=4..12 all pass (5000tu + noise, bond-graph == C_N
cycle every record, R(N)=d*/(2 sin(pi/N)) exact, two-sided attractor, dx->0.25
shift 0.023%). Pinning-era square4 doubt RETIRED: rings are continuum objects.
Membrane material = A4s family (tau=2.5, Dv=1.6).
NUMERICS TRAP (important, retroactive): A=5 statics (tau=2.5 Dv=2.0) are
DT-ARTIFACTED under IMEX dt=0.02 (pair slides through d*, replicates ~2600tu;
reproduced in two engines; dt<=0.005 freezes d*=15.71). EXPLAINS composite's
"integrator band" 15.43-vs-15.70 discrepancy (was dt artifact). M2's original
certs are SAFE (explicit Euler dt=0.0025). Rule adopted: A=5 IMEX work needs
dt<=0.005; A=4 at dt=0.02 verified exact.
R2a: rings enclose — interior u-pool asymmetry +0.035 (N5) decaying with N.
R2b: v-channel walls are POROUS (gaps are attractive channels — honest negative,
20/20 transmit) BUT cross-w wiring (etaw12, vacuum-exact) gives a REAL BARRIER:
V_w = k4*etaw*0.046 at the gap saddle; etaw=1.0 confines a tau1=5.8 cargo
(bounces 2500tu, never crosses, census frozen) while tau=6.0 still transmits —
a speed-dependent crossing curve is being mapped. FIRST CONFINEMENT ACHIEVED.


### l0-deepsearch: child died post-setup; CONTROLLER DRIVING the generation loop
Infrastructure complete and operational (ds_lib eval pipeline, MAP-Elites archive
keyed species x motion x graph-phase x memory, gen.py breed/ingest/confirm driver,
idempotent workers). Gen-0 (35 evals) done, gen-1 breeding launched by child before
death; controller driver.sh now runs gens 1-6 + confirms autonomously.
EARLY SIGNAL: e1_9513 seed soup-scores 57.8 and a first-gen jitter (g0_jit_11) 66.5
— both ABOVE machinev3's 43: the evolver's slow-tanh merge line is richer in soup
than anything we designed. Archive already spans 14+ behavior cells.


### blob-membrane — CERTIFIED (scorecard + controller audits 2026-02-24)
R1 rings N=4-12 (bond-graph C_N every record, ring law R=d*/2sin(pi/N), attractor,
grid 0.023%; AUDIT: N=8 from out-of-set chord 17.0 + fresh noisy seed -> ncomp 8
throughout). A5-dt trap logged. R2a enclosure (interior pool +0.035 N5 -> +6e-4
N12). R2b: v-channel porous (gaps attract!); ONE-WAY CROSS-W closes pores:
V_w = 0.046*etaw (saddle) / 0.82*etaw (core); SPEED-SELECTIVE: tau=5.8 confined
at etaw>=0.9, tau>=5.9 passes at all stable etaw; nucleation ceiling etaw>=1.05.
R3 CARGO-IN-CELL 4/4 + film (AUDIT: fresh seed/position/kick -> confined, rc_max
8.3, ring closed 100% of records). R4 honest null: one-way membrane rigid (COM =
noise floor); backreaction map (2-way wirings cascade/split/replicate; legal
eta21=0.01 response < noise); noiseless hammer: sub-pixel deterministic PULL
certified (wiring moves the light thing). BONUS: alternating-species xv ring
(A-B-A-B, cross-chords 8.1, double-braced, topologically enforced composition).
NEW PRIMITIVES: prerelax-before-cargo (IC-artifact killer), speed-selective
membrane (cell wall with channels), second membrane material.
PHASE-6 HANDLES: certified CELL = closed membrane + distinct interior + confined
cargo; canonical states MEMBRANE_N10/N6.npz.


### l0-deepsearch — ACCEPTED (scorecard + controller audits 2026-02-24; overload-interrupted
audits completed anyway: everything survived)
LOOP VALIDATION PASS: mean interest monotone g0-g5 29.9->44.6 (+49%), g6 flat
(honest saturation); max 66.5->73.7 (+ driver-era ds6_019 at 68.6). 35 archive
cells, 28 NEW vs ground truths — incl. SIX 4-species cells (sampling ceiling was
2-3), flicker-phase bonds (never-before-occupied graph phase), and 4-species
rotor+memory (ds3_014). CONTROLLER FRESH-SEED AUDITS: ds3_017 = 76.3 (their 75.1),
ds3_014 = 60.7 (their 57.3) — both confirmed. ds3_017 (merge_slow_tanh of a
BFIELD-mutant x weak XV-jitter; weak parent contributed STRUCTURE not fitness —
the open-endedness signature) scores +75% above the best designed world.
OPERATOR LAW SHARPENED: merges OPEN cells (12/21 first-touches), mutations CLIMB
(17 holders + both top scores); share_chan fragile (same-vacuum law).
COST MODEL: 3.2 evals per archive event; 196 evals / 48 core-h local.
POD PLAN (approved shape): 1x 32-vCPU day = 20 gens x pop 48 + confirms, with 20%
immigration, richer descriptor key (n_act + memory-grade), MAX_FIELDS 14, 2-seed
elite screens. PENDING: mechanism autopsies of ds3_017/ds3_014 before any
world-catalog use; metric-drift note (mobile|liquid|m1 attractor) for metrics v2.
USER QUESTION ANSWERED: with validated metrics + iteration, the search DOES climb
past designed complexity and colonize behavior classes sampling never reached.


### ds3_014 mechanism deep-dive (user-driven, 2026-02-25)
FIELD EQUATIONS transcribed (12 fields, ~30 constants; on post 7). Interaction graph
verified quantitatively: blue-red mutual v-crosstalk (red suppression ~100% near
blue); green loses via asymmetric shared-halo (2.46 vs 1.67); yellow-blue association
(68% touching vs 19% null) is MEDIATED (zero direct coupling — habitat, not
conveyor: motion along blue ridges = 35% ~ random). Morphology division from
self-halo strengths: yellow strong+long-range (spheres), blue half-strength
(networks), red full-halo + deformable slow-v (spot/path hybrid).
THE FOSSIL VERTEX: ds3_014's single bilinear term -m*w_R traces through FIVE
generations (ds3_014 <- g0_jit_11 <- rail_111_17 <- s2_111_17 <- e1_9508 <-
ref_BFIELD): it is the DESIGNED isok/stigmergy vertex -b*(w-u0) from M6, inherited
verbatim (operators cannot mint bilinears — creation rate is structurally ZERO;
founder gene). EXAPTATION: trail-steering vertex repurposed as replication enabler.
ABLATION (T=12000, same seed): WITHOUT the vertex there is NO succession at all —
no red boom (3->7 vs 3->71), no yellow boom (3 vs 75), near-stasis. The one
inherited nonlinear term is load-bearing for everything interesting in the world.
AUTOPSY CORRECTION: "write-only recorder = vestigial" was wrong — K=0 channels can
act through bilinears; genome-anatomy tooling must treat bilin as first-class wiring.
USER TAKEAWAYS ADOPTED (evolutionary program v2 pillars):
 T1 dynamics: operator alphabet matters — bilinear minting is impossible today
    (audited: mutation cannot append chans/acts/bilin); add structural moves.
 T2 metrics: metric-audit loop is iterative BY NATURE (run -> inspect worlds ->
    find unrewarded interesting behavior -> extend metric -> rerun). ds3_014's
    succession was invisible to metrics until films showed it.
 T3 observation horizon: T is a moving target as complexity grows (ds3_014 needed
    12000tu vs the 2500tu screen); need cycle/steady-state detection to decide
    prune-vs-extend (adaptive-T assays); likely also larger L.


## PHASE 6 (user, 2026-02-25): EVOLUTIONARY RUN V2 — applying T1/T2/T3
Two searchers spawned:
- l0-metrics-v2 (sub-b7724bdc): metric fixes traceable to v1 audit failures —
  M1 interaction-gated ecology (sphere-passenger fix), M2 segment-vs-organism
  (worm fix), M3 bilinear-aware anatomy/memory (ds3_014 lesson), M4 ADAPTIVE
  HORIZON (extend-on-trend/charging/unconverged-ACF, stop-on-stationary; ds3_014
  must auto-extend and gain, m0 must stay cheap), M5 succession/staging detector,
  M6 box-limit flag (L-graduation). Locks gate the main run.
- l0-evolve-v2 (sub-4a4d4304): operator alphabet v2 — mint_bilin/delete_bilin
  (vertex research question: does evolution USE mintable nonlinearity?), add_chan
  (slow channels allowed), dup_act (speciation move), + v1 moves; bilinear-
  preserving merges tested; 2-seed elite confirmation before block library; 20%
  immigration. Local validation first; controller rents pods for the 20-gen run.
Membrane/top-down discussion queued after v2 is in motion (user).


### l0-metrics-v2 — LOCKED & ACCEPTED (scorecard + controller audit 2026-02-25)
All M1-M6 delivered, validation 10 worlds x 3 seeds, seed-3 out-of-sample clean,
SHA256-pinned lock. v2 rank: m0 2.8 << coex 15 < m4 24 < xv 31 < bf 34 < mv3 41 ~
pred 45 << ds3_017 65 ~ ds6_000 66 < ds3_014 76 — the succession world is now the
corpus top (v1 had it 8 BELOW ds3_017; the horizon founnd what the fixed screen
missed). CONTROLLER AUDIT fresh seed 13: ds3_014 auto-extends 2500->5000->10000
(fires a_mem+b_org then converges) landing 77.9; m0 stops at 2500 scoring 2.8.
Honest notes: mv3 soup bimodal across seeds (machine assembles or not — recommend
org_model cell keys); statics pay ~8% C8 dilution by design; pred +5 from horizon
(undervalued in v1). Continuation sim bitwise-identical (parity gate).
GREENLIT: evolve-v2 local gens on assay_v2, then pod main run.


### Budget update (user, 2026-02-25): main-run ceiling raised to "few hundred $"
(check-in near $1k). v2 main run upgraded: pop 96 x 25 gens, 3-seed confirms,
in-run L=192 graduation lane (box-flagged elites), long-horizon confirm lane
(T cap 40k for top-3/gen), 20% immigration. Fleet plan: ~10x 16-vCPU nebius
(~160 cores, ~$4/hr, ~25h wall, est. $100-250). Speed > thrift.


### blob-gpu spawned (2026-02-25, infrastructure track)
JAX accelerator port: batched-population stepping (a generation as one tensor) +
large-world mode; correctness gates (f64 L2 < 1e-5 @ T=100, descriptor parity on
the locked v1 battery, bond anchors incl. the A5-dt trap); roofline analysis +
optimization log; drop-in run_soup_gpu(); public post accelerating-blobs.html
(the path others will use). One GPU pod authorized, target < $50, terminate when
idle. Independent of the CPU main run.


### Patchworlds probes spawned (2026-02-25): blob-patchworlds (P1 identity, P2
aligned-vacuum seam w/ traveler-at-seam, P3 non-aligned ramp, P4 halo leak, P5
chemistry near seams) + patch-lit (domain decomposition / heterogeneous-RD /
multi-model coupling review; the D(x) discretization red-flag question).
Both parallel to the v2 main-run pipeline and blob-gpu.


### patch-lit — ACCEPTED (2026-02-25; van Heijster refs spot-verified)
Verdict: MODIFIED PoU on one grid. Load-bearing: (1) D(x) discretization — only
div(D grad u) is safe; our spectral integrator supports none of the D(x) forms =>
v1 patches keep ALL D global, blend reaction/wiring only (A-contrast via tau at
fixed Dv — A=tau*Dv saves the M0-vs-M4 test); (2) ghost-force principle validates
our vacuum-safe-wiring + iso-vacuum recipe independently; (3) seam phenomenology
pre-catalogued by our own model class's literature (penetrate/rebound/pin/
oscillate/slide/one-way/refract/HIOPs) => P2 assay checklist + both directions;
(4) R2 homotopy pre-flight MANDATORY (convex mix of two good worlds can be lethal;
wide seams don't fix bad paths); (5) generative-PoU gap is real (FBPINNs/POUnet/
Flow-Lenia adjacent; static-geography PoU over dissipative-soliton RD = our claim).
Seam rule w>=32-48px; seam-strip masking in metrics; fitness in patch cores for
any evolve-v3 use (Flow-Lenia seam-parasite lesson). Relayed to blob-patchworlds
BEFORE its first physics run (only conventions written).


### blob-gpu — ACCEPTED (scorecard + controller inspection 2026-02-25)
JAX port certified: f64 trajectory parity 7.9e-13 worst (gate 1e-5) on all 7 GTs
single+batched; bond anchors pass INCLUDING the A5-dt trap reproduction (the port
reproduces the physics AND the artifact — the right kind of fidelity); descriptor
parity 6/7 in 3-seed bands + mv3 resolved by pre-registered 8v8 protocol (seed-
bimodal on BOTH engines, MW p=0.88 — parity at distribution level; lesson: 3-seed
bands are the wrong estimator for switch-regime worlds, flagged to metrics-v2).
PERF: bandwidth-bound (AI 2.4-3.3 vs A100 ridge 12.5), 25-30% nominal BW;
5.0-5.7 us/field-step FLAT from 72 to 2016 batched fields (CPU core: 440 us) =
~80x; honest optimization log incl. CUDA-graphs REJECTED (+6% slower).
HEADLINES: pop-96 T=2500 assay = 858 s (403 worlds/h, $0.005/world); 512^2 T=10k
= 264 s (35x CPU); 1024^2 T=10k = 1171 s. A 6-gen deepsearch = 90 min / $3.
Pod bill $5.71 total (2.87 h, terminated). Post 9 accelerating-blobs.html live.
IMPLICATION: v3-scale searches (pop 200+, L=512+, T=40k lanes) are now $10-30
problems; the CPU-fleet era ends after the current v2 run.


### blob-patchworlds — ACCEPTED (scorecard + controller audit 2026-02-25)
VERDICT: PoU world composition WORKS (modified-PoU per litreview; engine =
patch_lib.run_patched with conservative div(dD grad f) deviation split, P1-gated).
- P1 bit-identity PASS; P0 chord healthy for M0->M4 + NEW TRAP: linear stability
  of the chord is NOT enough — an existence CLIFF can kill blobs at s>=0.9 while
  the vacuum stays stable => P0 protocol now includes existence pokes along s.
- P2: traveler PENETRATES M4->M0 at all widths, converts to static-with-creep;
  45-deg incidence refracts to NORMAL exit (seams collimate). CONTROLLER AUDIT:
  fresh geometry, 10-deg oblique, w=12: crossed, exit 0.0 deg off-normal, parked
  at x=4.4 lu. CONFIRMED. One-way by construction (statics cannot approach).
- P7 CONTRAST (the design dial): tau-only seam (Dv global) = traveler PARKS at
  8.7 lu standoff — wiring-only seams are REPELLING FENCES; tau+Dv seams are
  PENETRABLE MEMBRANES. Seam composition mode is a world-design instrument.
- P3: non-aligned vacua settle to smooth ramps (source 1.25e-3 ~ predicted 2e-3),
  no nucleation; blobs expelled NORMAL to seam (no along-seam drift — honest
  negative vs controller's highway conjecture); habitable|lethal patching works.
- P4: aligned seams are structurally invisible (<1e-6); halos cross seams
  unscreened (cross-world force == same-world force at 20 lu; nothing invented).
- P5: bonds straddling seams survive; d* shift -0.9% at w=24; at w=4 the whole
  molecule is expelled intact.
- NEW LAW: seam body force v ~ -0.4*grad(rho_B) on every localized object =>
  ecotone-depopulation prediction for evolve-v3 spatial merges; design rule
  w >= 12 lu (force <= 1e-2, d* shift < 1%).
NOT tested (scope, queued): species-union padding, bilin blends, noise-driven
crossing statistics, membrane x tissue patch (the natural showcase).


### v2 MAIN RUN GREENLIT (2026-02-26)
evolve-v2 local validation ACCEPTED: T1 answered — evolution USES minted vertices
(15/15 evaluable, 9 fixations, 8/34 archive cells carry mints, all 2-seed
confirmed; best bred child of g12 IS a mint, I2=70.1, CONTROLLER AUDIT fresh seed
67.6 in-band; a second vertex was minted alongside ds3_014's fossil; delete_bilin
reproduces the fossil ablation in-search 66.5->9.5). Operator law v2: cross_edge
still the opener (12 events), mint 8, mutate 8, add_chan 4; dup_act weak (vacuum
destabilization, kept low); immigration works (64% alive, 3 cells).
LIVE FIX adopted both sides: confirm seeds inherit incumbent T_used as t0 floor
(naive seed-2 confirms falsely failed extended elites). Cost model: 1399s/bred
screen incl. rejects; T_used dist 74/11/13/3% at 2500/5000/10000/20000.
Pod plan: 10x16 vCPU island model (archive-union by cell-max every 2 gens),
~1985 core-h, $76-99 base, ceiling $250. Bundle prep -> controller provisions.


### V2 MAIN RUN LAUNCHED (2026-02-26)
Fleet: 6 pods (2x FI e2-16vCPU + 4x FR d3-16vCPU; 10-pod plan cut to 6 by provider
stock — islands 0-5, ~96 vCPU, ~$2.4/h, wall estimate stretches 1.6x to ~30-40h,
cost ~$75-120). Bundle hash-verified per pod; smoke 3/3 PASS gates on every
launched island (bit-identical anchor values); islands 0-4 RUNNING (25 gens,
pop 96 fleet-equivalent via island mix), island 5 dep-fix in flight. Merge
cadence: controller pulls archives every ~2 gens, merge_islands.py union
(cell-max, lineage-preserving), pushes union back. evolve-v2 dormant until
harvest.


### Pipeline speed analysis + GPU shadow run (2026-02-26)
END-TO-END TIMING AUDIT (measured): the v2 cycle spent ~65-81h of SIMULATION wall
(metrics validation 10-12h local, evolve local gens 14h, main run 30-40h remote,
audits/autopsies ~5-10h) vs ~2-3 agent-days of dev. GPU compresses every sim
stage ~15-25x (validation battery ~40 min, local-gen equivalent ~1h, main run
12-15h on one A100, audits/films ~1h) => pipeline potential ~10-19h sim wall.
Biggest non-sim losses: session-death respawns (agent), pod provisioning + per-pod
smoke (~1.5h, stock-limited), and LOCAL stages that predate fleet rental (the
metrics validation + evolve local gens ran on 4 laptop cores — should have been
podded or GPU'd from the start; rule adopted: any >2h sim batch goes remote).
ACTION: l0-gpu-run spawned — wires the certified GPU backend into assay_v2/ds2
behind a backend switch (locked logic untouched), re-runs ALL gates on GPU
(~25x faster), then launches a GPU SHADOW RUN (islands 6-11, one A100, one-way
immigration from CPU-fleet unions) racing the live CPU fleet. CPU fleet keeps
running; harvest merges both.


### FLEET INCIDENT + FIX (2026-02-26): OpenBLAS thread thrash
Symptom: ~7h into the run, islands had completed only 3-11 evals each (model said
~50-90). Diagnosis: each of 14 workers spawned 31 threads (OpenBLAS DYNAMIC_ARCH
defaulting to 16 threads for numpy pointwise ops) -> load 113 on 16 vCPU ->
5-10x slowdown from cache/scheduler thrash. The bundle pinned scipy-FFT workers=1
correctly but nobody pinned BLAS. FIX: rolling restart with OMP/OPENBLAS/MKL
_NUM_THREADS=1 injected into pod_run.sh (workers idempotent; in-flight evals
restarted). Load 113 -> 14; eval completion rate jumped ~10x immediately.
LESSON (bundle checklist): ALWAYS export thread pins in worker launch scripts;
a local smoke on a 10-core laptop does not reproduce 16-vCPU contention.
Run clock impact: ~6h lost; revised ETA ~30-40h from restart.


### Fleet decision policy (user, 2026-08-26)
Discovered: deployed config runs 96 cand/island/gen = 6x the fleet-wide-96 plan
(6 independent full evolutions; ~93h/island, ~$220 — accepted as more science).
Policy: CPU fleet continues as-is. If the GPU shadow run (islands 6-11, same
per-island mix) certifies + completes first with sane results, present side-by-
side and stop the CPU fleet early at a clean generation boundary WITH user
confirmation. GPU racer on revival #2 (execute-only orders; controller takes
over inline if it dies at setup again).


### Sweep log 2026-08-27 ~05:00
LANE BOTTLENECK FOUND+FIXED (infrastructure discretion): the deployed config ran
L192 + longH-40000 lanes EVERY generation as blocking one-offs (~14h serial tail
per gen => plan infeasible ~16 days). Fix: l192_per_gen=0, longh_top=0 on all
islands (live for subsequent gens); in-flight lane jobs killed + shards emptied
(the drain-step restart trap documented); lane science reassigned to the GPU
where L192/T40k costs minutes. All islands immediately bred their next gens
(96 jobs each, full worker load).
FIRST UNION MERGED+PUSHED: 77 cells from 6 islands (26 minted-vertex cells, 39
block-eligible); TOP = 81.3 in 4|grow|rotor|liquid (above ds3_014's 76!).
XV PARITY (CPU side complete): seeds 4-8 = {35.8, 33.7, 37.5, 25.6, 4.0} — xv is
heavy-tailed seed-variable on CPU too; GPU 50.2 excursion pending distribution
comparison (GPU parity seeds queued after battery, 16/30 rows done).
Budget: ~$75 cumulative (CPU ~20h x $2.38 + GPU ~5h x $1.20 + priors). OK.


### blobkit spawned (2026-08-27): packaging the certified core
Diagnosis: flat modules + sys.path chains + tree-walking data loads (worlds.py
BLOBS=dirname(dirname()) + machinev3 imports) make every remote deployment an
archaeology dig — 3 GPU-pod breakages from missing implicit deps. Fix: blobkit
installable package (locked files verbatim w/ SHA256 import self-check, worlds
as packaged data via importlib.resources, cpu/gpu backend switch, MANIFEST
provenance). Additive only; running fleet untouched. Also the "repo ripe for
contribution" prerequisite for the decentralized-agents phase.


### Sweep 2026-08-27 ~13:00
Fleet: islands 2-5 healthy (+22-30/2h, mid gen-2 confirms); islands 0-1 lag ~1 gen
(slower e2 CPUs + heavy t0-floored seed3 confirms running 4h each single-core —
legitimate; v3 lesson: batch confirms on GPU). GPU GATE BATTERY COMPLETE for the
7 ground truths, ZERO errors, ALL bands overlap CPU (champion worlds skipped on
pod — registry lacks deepsearch files; gate via blobkit later). XV RESOLUTION:
GPU extra seeds cluster 33.9-35.5 vs CPU's heavy-tailed {35.8,33.7,37.5,25.6,4.0}
— the 50.2 was the same distribution's upper tail (H2 confirmed, parity holding).
Awaiting xv seeds 7-8 for formal acceptance -> shadow-run launch decision.
Budget ~$100/$250.
