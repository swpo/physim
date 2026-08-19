# machine searcher — WORKING NOTES (M5, round 3)

## World decision (round-3 core question resolved FIRST, by argument + controls)
Machine world = SINGLE-SPECIES (u,v,w) A=4 family (M4's certified traveling-bond
world), NOT the vvw two-species world. Reasons:
1. The machine's motor is the wake-locked tandem/train (M4-certified). In the vvw
   world NO binding exists at all ("all pairs repel", transport P3 + M3 encounter
   table) — porting the tandem to vvw means re-engineering B's v-tail (a new M4
   campaign, tau_B/Dv_B search at B's k-params), not an integration step.
2. The isod gradient DOES port to the single-species world exactly: shift (k1,k4)
   along the line k1 -> k1 + u0*b, k4 -> k4 + b (u0=-0.70354 = uniform state).
   The cubic for the uniform state keeps root u0 for ALL b EXACTLY (checked
   numerically to 1e-15). Reaction perturbation = b*(u0-w) -> vanishes identically
   on background: the SAME zero-footprint trick as transport's isod, ported.
   (Here it is even cleaner: the uniform state is an EXACT fixed point of the
   driven system, no 1D base relax needed. Call this mode "isok".)
3. Cargo = same species as carrier: "flavor" is NOT needed for machine v1. The
   machine function (net upstream transport against an imposed load) never uses
   flavor distinction; cargo identity is positional (which blob was parked where),
   measured by tracking, not by species. Honest cost: no species-selective
   sorting in v1 (parked as vvw open item: does B-B bind at some tau_B?).

## Machine concept (design (a) TUG + torus circulation = repeatable cycles)
- tau = 5.70 (PAIR-ONLY drift zone (5.636, 5.748)): lone cargo CANNOT self-move
  (c_single ~ 0); the tandem travels at c_pair ~ 0.06 >> expected drift.
- Load field: saw profile (n_teeth=1, frac 0.85-0.9), isok mode: drift is
  DOWNSTREAM = -x on ~85-90%% of the track (rising branch); UPSTREAM = +x.
- Machine = locomotive tandem kicked +x once at t=0 (IC, allowed), circulates
  the periodic domain forever; parked cargoes on the track get picked up HEAD-ON:
  leader front tail pushes cargo -> cargo accelerates -> locks into the front
  shell (M4 two-sided shell convergence to sep*=14.78) -> train grows 2->3->4->5.
  Each pickup = one cycle; every captured cargo is then carried upstream lap
  after lap. No unbinding needed for v1 (train-growth machine).
- Why not (b) pure conveyor: the isok/isod field is a STATIC potential for a
  passive blob (down-b force everywhere + no noise-activated hops, P4 negative):
  a lone blob on any saw ends in the trough and stays: deterministic circulation
  of a PASSIVE particle in a static potential is impossible. The saw "circulation
  redesign" needs a self-propelled structure — which is exactly design (a)'s train.
  So (b) collapses into (a) here. (c) binding/unbinding gates: unbinding is the
  known missing primitive (M4: bonds never break below replication) — parked.

## Integration risks to clear by controls BEFORE machine assembly
C0 engine anchor: pair tau=6.0 flat -> c=0.14075, sep 14.78 (M4 cert values).
C1 background exactness: no-blob saw world stays at u0 to 1e-12 (isok exactness).
C2 pair-only zone in THIS engine: tau=5.7 single kicked -> c~0; pair kicked ->
   c~0.0595 (M4 audit values).
C3 level ladder (the (k1,k4) iso-line window of the A=4 blob/pair): bconst in
   {-0.15,-0.1,+0.05,+0.1,+0.15,+0.2}: alive? bound? c_pair(bconst)? -> sets the
   usable tooth height b_amp (and reveals d(tau_c)/db stall risk near tooth top).
C4 drift curve (the adversary): parked single at mid-branch, eps ladder ->
   v_drift(eps), sign (expect -x = down-b), area stability. NOTE tau=5.7 is
   0.048 below single onset: near-onset susceptibility may amplify drift vs the
   vvw -0.906eps coefficient. Whatever it is, MEASURE it; baseline uses measured v.
C5 traveling pair upstream through the gradient: c_up(eps), unbind?, cliff cross.
C6 head-on pickup at b=0: traveling pair + parked single 25-30px ahead ->
   3-train? c_3? (THE critical primitive; if it scatters/reverses, map it.)
C7 pickup under gradient (eps at working point).

## Working-point selection logic
eps chosen so b_amp = eps*L*frac/2 stays <= ~60%% of the C3 level window edge;
prefer the largest eps that passes -> strongest honest adversary. n_teeth=1
maximizes the continuous upstream runway (~84 px).

## Budget
192x192 IMEX-FFT: ~25 tu/s measured -> T=1500 ~ 60 s, machine run T=3200 ~ 130 s.


## UPDATE after C0-C4b, C6 (all controls PASS, physics mapped)
- C0/C1/C2: engine anchors PASS (c_pair tau6=0.139-0.141, single 5.7 decays to rest,
  pair 5.7 c=0.0592 sep 15.23; isok background exact to 1e-16).
- C3 c_pair(b) at tau=5.7: +0.094@-0.05, +0.085@-0.025, +0.059@0, +0.0044@+0.025,
  ~0@+0.05 (stall b* in (0.025,0.05)); REPLICATION at b=-0.1 (pair, t=70).
  Level window for machine: b in [-0.05, +0.025] active, park side up to +0.2 static.
- C4: the adversary is NEAR-ONSET UNLEASHING, not linear vvw drift: parked single on
  slope runs DOWN-B at 0.05-0.08 px/tu (comparable to c_pair!), then PARKS AT THE
  TROUGH (saw trough = natural cargo parking). eps>=0.0025 n1 saw: trough deeper
  than b=-0.09 -> down-running blob replicates. Machine tracks must keep
  b_min > -0.06.
- C6 PICKUP PRIMITIVE (flat): PASS. Traveling pair approaches parked cargo,
  wake-locks it at gap 14.95 as the NEW LEADER (pusher-tug: cargo rides ahead),
  3-train c=0.0731 (+23% vs pair 0.0592). ncomp==3 throughout. Same at gap 30.
- Design consequence: train SPEED GROWS with each pickup (M4 trimer + C6):
  the machine gets stronger as it loads. Climb ceiling: the b-level where c->0;
  eps must keep apex level below ~+0.02 for the initial pair.

## MACHINE WORKING POINT (v1, pending C5 lap verification)
L=128 (N=256), n_teeth=4, P=32, frac=0.85, saw isok; eps chosen from C5
(0.001 or 0.0015; b span +-0.0204 at 0.0015). tau=5.7, sigma=2e-3.
Layout: loco pair follower x=1, leader x=16 (tooth 1, kicked +x = upstream);
cargoes parked at x=34, 66, 98 (troughs 32/64/96 + 2px settle standoff).
T=3200. Pickup k = cycle k (3 pickups on lap 1 -> 5-train, 60px long,
leader-tail gap 68px on the L=128 torus: no necklace closure).
Null control: same track, no locomotive. Baseline |v_drift|: measured on the
working track (C4 protocol at working eps); honest caveat: the trough BOUNDS the
do-nothing loss, both the ratio and the bounded null displacement reported.
Budget: 256^2 IMEX-FFT ~9-11 tu/s -> machine run ~5-6 min (documented one-off).


## UPDATE: C5/C7 climb failure -> E-series envelope -> machine v1 -> noise buckling -> rails v2
- C5 HONEST NEGATIVE: pair CANNOT climb any tested saw at tau=5.7 (even eps=0.0005:
  reversal at b~0; eps=0.00025: b_rev~+0.005). Near-onset up-slope travel dies FAR below
  the quasi-static stall (b*~0.03-0.05 from C3): dynamic reversal, not level stall.
  C7: apex-parked cargo falls down the cliff (apex not a park spot; troughs are).
- E-series: climbing envelope grows with TRAIN LENGTH: pair b_rev~0.000/+0.005,
  3-train b_rev~+0.0104 (eps=0.0005 n1). tau=5.73 helps pairs a little (+0.006).
  => locomotive = 3-TRAIN; tooth apex +0.0068 < 0.0104 (1.53x margin), P=32 frac=0.85
  eps=0.0005, L=160 n_teeth=5. E4: 3-train LAPS this tooth (+173px/2500tu, ~6 cliffs).
  E5: lone blob parks at trough (settle x = trough+2.3); v_drift moving-segment
  -0.0125 px/tu (locked amendment: strongest honest baseline).
- P1: pickup on working track (noiseless): 4-train, t_pu=215, laps forever. 
- M0_pilot (noiseless, 3 cargoes): 3/3 pickups (t=270/600/915), ALL cargo carried
  +182..+218 px; mid-run the 6-train sheds its 3 loco blobs (rear fission at
  near-onset power limit) and the THREE CARGOES continue as their own train
  ("relay tug"); net_up=600px, eff=4.45. ncomp==6 throughout.
- MC v1 CERT FAILED (sigma=2e-3, 3 seeds): TRAIN BUCKLES off-axis after 1-2 pickups,
  reorients into the trough VALLEY (y-direction costs nothing), jams at x~trough.
  Pickups 1/2/1, net_up 30/60/31 px. NULL clean (cargo dx=-0.6px: parked).
- RAILS (the brief's candidate-(a) ingredient): static y-channel added to the SAME
  environment field: b(x,y) = saw(x) + chan_eps*min(|y-80|, 24). R0: restores y
  (86->80, damped). R1/R2 (chan_eps 0.001/0.002): train on-axis (|dy|<0.6) under
  noise, climb intact (v=0.068/0.076 — faster than unrailed: no buckling loss).
- Machine v2 = v1 + chan_eps=0.002 cap=24. Cert battery v2 running.


## FINAL: cert battery v2 PASSED (2026-02-19)
- M2C_seed1/2/3: 3/3 pickups (t=245/515/765 +-5), net_up 756-759 px, eff 5.6x.
- M2C_jitter (+U(-2,2) parks): 3/3, 766 px, 5.68. film_seed5: 3/3, 766 px, 5.67.
- M2C_null: cargo dx -0.5..-0.7 px (parked). b1 all-alive everywhere.
- Grid one-off: dx=0.25 matches (0.5-2.4% per-id; first attempt invalid — stamp
  not resampled; engine patched, rerun clean).
- Self-healing relay bonus: 6-train sheds rear loco (power ceiling), shed blob
  waits at trough (pair-only zone!), re-collected next lap.
DELIVERED: SUMMARY.md, fig1-4, results.json (71), scorecard to parent.
