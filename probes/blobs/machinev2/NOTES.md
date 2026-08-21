# machine-v2 — WORKING NOTES (phase 4, L3 composition: logistics line)

## Mission (parent brief, resume message)
V2a THROUGHPUT: one carrier serving 3 queued cargoes (tau2=5.60, spacing>=30px)
on one lane: tow -> dock release -> fork sort; carrier returns (torus lap).
Gate: >=3 deliveries in one run, 3 seeds; cycle time, throughput, queue integrity
(fly-by drag < 1px). Then V2b two-way sort, V2c closed loop, V2d grown part.

## Engine
sim.py + runjob.py = verbatim copies of factory/ (certified GLv4 engine).
Stamp from composite/data. IMEX-FFT dx=0.5 dt=0.02. results.json append per run.

## Design analysis before prototypes (footprint rule arithmetic)
- Parent sketch x=30/60/90 with carrier 39/54.4: cargo2 at 5.6px from front blob
  = inside core-split range (<6). Queue positions must clear the carrier START
  and the tow path. The two forced encounter types:
  E1 HEAD-ON: carrier front blob meets parked on-lane cargo (every lap pickup).
     Known: eta21=0.05 clean swing-around (factory T6); 0.1 in crotch = split
     (GLF). 0.1 on OPEN lane with rails = UNMAPPED -> P1.
  E2 TOW-PAST: carrier+towed cargo1 passes parked cargo2. Outcomes: double-tow
     (cargo2 locks behind cargo1 at same-species d*=15.4)? displacement? split?
     UNMAPPED -> P2.
- Sequential-service reading needs E1 to be a clean pickup (swing-around then
  trail-lock at 8.46 behind rear M). Convoy reading needs E2 = stable 2-cargo
  chain tow. Either can certify V2a; physics decides. Both mapped at L=96.

## Session log
- [t0] dirs made, engine copied, SMOKE_engine ok (rec 1, 10.2 tu/s L=96).
- [t0] ANCHOR_GLv4_seed1 launched (L=160 T=4000, exact certified job).

- P1 (rec 2): HEAD-ON at eta21=0.1, cargo on-axis dy=0: SPLIT at t=570
  (frontM-cargo sep_min 5.80 < 6 core overlap; cargo dragged 17px + pushed to
  y=55.6 first). E1 head-on pickup at 0.1 = FATAL on open lane too (generalizes
  GLF crotch split).
- P2 (rec 3): tow of c1 clean (lock 8.55, 47px) but convoy meets parked c2
  head-on -> same split (sep_min 5.58, t=575). => ONE fix serves both.
- MITIGATION LADDER: eta21 in {0.06,0.07,0.08} head-on with dy=+2 stagger
  (definite swing side; cargo rails recenter after pass). Want: no split AND
  post-swing trailing LOCK (tow). 0.05 anchor = P1b (expect clean pass, no lock).

- P1b/P4 (recs 5-8): HEAD-ON PUSH-CAPTURE certified-grade behavior at eta21 in
  [0.05,0.08]: cargo captured on FRONT branch, rides 7.10-7.16px ahead of front M
  at full pair speed c=0.072, stable 2600-3000tu, ncomp frozen. sep_min during
  capture transient 5.88-6.04 (split edge ~5.8 at eta 0.1 => capture margin is
  force-limited, watch seeds). dy=+2 stagger recentered by rails except 0.08
  (ended y=49.5 — slight off-center ride).
- CHAIN LOGIC (design math): blind pair speed is fixed; front eta link must carry
  n*c/mu for an n-cargo push chain; S-S links carry (n-k)c/mu. Saturation of the
  eta link -> compression below 6px -> split. n_max = THE V2a design number.
- NEXT: P5 (2-chain 0.06), P6 (3-chain 0.06), P6b (3-chain 0.08), P7 (offset
  cargo-rail y=54 vs lane 48, eta 0.1 head-on: graze-capture rescue of rear-tow?).

- ANCHOR_GLv4_seed1 (rec ~9): BIT-EXACT repro of factory GLv4_seed1 (net1
  293.19/293.02, net2 80.31, end2 [30.25,108.63], pair stats identical to 4
  decimals). Engine + conventions verified. BUILD UNLOCKED.

## V2a ARCHITECTURE DECISION (from P1/P1b/P4 physics)
Head-on at eta 0.1 = split; at 0.05-0.08 = PUSH-CAPTURE (cargo rides ~7.1px
ahead of front M = bulldozer blade; stable, full pair speed). Consequences:
1. On a shared lane with one global eta field, SEQUENTIAL single-service is
   geometrically impossible: the blade captures EVERY on-lane S it meets
   (capture radius = well ring 6-15px; no per-cargo eta). Mapped, not assumed.
2. The natural throughput machine is the BULLDOZER CONVOY: carrier sweeps the
   lane, chains queued cargoes on its blade (c1 on blade, c2/c3 ahead via
   same-species S-S bonds ~15.4 which are eta-INDEPENDENT), delivers the whole
   chain past the dock in one pass; fork sorts the chain down the branch;
   carrier laps empty (past x1 cargo is eta-transparent: ghost pass).
3. Chain force law: blade must transmit n*F(c); compression of blade gap
   (7.1 -> toward 6 core-split) sets n_max. P5 (n=2, 30px spacing, e0.06),
   P6 (n=3, 18px), P6b (n=3, e0.08) measure blade capacity.
4. Delivery: chain crosses x1 while ON-lane (tow well >> fork rail 0.004,
   GLv4 mechanism), releases front-to-back over ~(chain span)/c tu; front
   cargoes stay bonded to still-bladed rear -> pushed until REAR cargo (c1)
   unhooks at x1; then chain relaxes + forkchan drags it down the branch;
   park target = flat branch floor (dy_max=18 off lane) with rear cargo past
   the 15px footprint. Risk: chain jackknife at the crotch (known trap zone).
   D-series (L=96 dock+fork) tests before any L=160 run.
Queue integrity gates: pre-pickup displacement <1px; post-delivery fly-by
immunity >=1 full lap (ghost pass + 18px off-lane margin).

- P5 (n=2, spacing 30, e0.06): PASS. c1 blade 7.0px, c2 S-S chain 14.6, both at
  pair speed 0.0716, conveyed 156-171px, 2500tu, census frozen.
- P6 (n=3, spacing 18, e0.06): PASS. Blade compressed 7.1->6.68 mean (min 5.61,
  split edge ~5.5!), c1 rides 4px off-axis (y=52.2) = blade-overload symptom;
  chain intact at 0.072-0.079. n_max(0.06) >= 3, margin thin.
- P6b (n=3, e0.08): SPLIT t=285 (sep_min 5.39). Deeper well pulls cargo INTO the
  carrier: eta higher = MORE compression. Blade budget: eta21 in [0.05,0.06].
- P7 (offset rail y=54, e0.1): SPLIT t=860. eta 0.1 head-on is fatal even with
  6px stagger. Sequential-service claim at 0.1: DEAD (P1+P7). CONVOY at 0.06 is
  the V2a machine.
- SEQUENTIAL IMPOSSIBILITY (mapped): capture is all-or-nothing at the 15px
  eta-well footprint. Any on-lane (or <15px staggered) parked S is captured by
  the passing blade/chain; any >15px off-lane S is invisible to it. Single-lane
  multi-lap single-service would need an active feeder = new machine. The convoy
  IS the throughput machine; the returning empty carrier re-collects anything
  still in the lane (self-sweeping).
- METRICS LOCK (below) then PD_n2 dock+fork pipeline proto at L=96.

## PD pipeline design (locked reasoning)
- Queue spacing: S-S bond basin edge 19.5px => queue spacing must be >19.5 or the
  queue self-bonds (P6's 18px pre-bonded). Cert spacing = 30 (P3-verified static).
  PD2 proto uses 24 + a null.
- Dock release of a PUSH chain: c1 (bladed, rearmost) crosses x1 -> eta at its
  position ->0 -> whole chain (S-S bonds are eta-independent) detaches and glides
  as a bonded train; fork slides the train down-branch as a unit.
- GHOST PASS: past the dock eta=0 => M and S are mutually invisible (different
  field triplets; factory R1 eta21=0 shuttle-through). The carrier drives THROUGH
  parked cargo harmlessly outside the eta zone. Fly-by immunity out there is by
  species transparency; inside the zone it's the 15px rule.
- V2a consequence (honest deviation from brief sketch): single-service laps are
  impossible (blade captures everything in-lane within the zone); the machine is
  a ONE-PASS CONVOY that picks the queue up sequentially (staggered t_pick) and
  delivers the chain at the dock; carrier keeps lapping (fly-by gates still real).

- PD2 (rec 16) DISSECTED: c2 (chain cargo) DELIVERED clean (pushed past elbow
  while chained, slid to y=30). c1 (bladed cargo) = CROTCH LIMIT CYCLE: crotch
  deflects it off blade axis mid-slope -> blade slips -> abandoned mid-slope ->
  backward-surf to lane (GLF trap) -> re-captured each lap -> repeat; each cycle
  jostles sorted c2 via compressed S-S bond (14.1 < 15.4): flyby 3.76px FAIL.
  ALSO: PD2_null: 24px queue spacing creeps 1.4-1.5px/2000tu (S-S tail) > 1px
  gate: cert queue spacing = 30px (P3: 0.53-0.58px/1500tu).
- MID-SLOPE ABANDONMENT RULE (new interference law): a push-delivered cargo must
  cross the dock edge with the branch ELBOW already behind it, else the b2 tilt
  surfs it back to the crotch. Equivalently: [x0, elbow] must lie INSIDE the eta
  zone and x1 - x0 >= (dy_max/slope) - glide_margin. FIX-B geometry: slope 4,
  x0 = x1-4 (elbow x1+0.5), glide 6.5-7.5px -> all cargoes park past elbow on
  the FLAT floor, then the parked chain slides -y down to the branch floor
  together (isotropic bonds preserve spacing).
- FIX-A alternative (crotch as blade->rear-tow converter at eta 0.08): if the
  crotch slip drops cargo into the REAR slot and 0.08 rear-tow holds (v_max
  ~0.11 > c=0.059), the cargo finishes the zone GLv4-style. Test n=1.

- PB0 (rec 18): slope-4 flat-floor FAILED WORSE: crotch spit-back to x=60 (8px
  BEFORE x0=68); limit cycle 60<->70 every lap; never crossed x1. MECHANISM
  NAILED: backsurf force = chan_eps*slope*sign(y-ytgt) acts on any OFF-LINE blob
  on the slope; bladed cargo is held at lane y while its line descends => off-line
  => backsurf ~ slope. Steeper slope = harder ejection. ON-LINE blobs feel zero
  backsurf. PA1 (rec 17): eta 0.08 blade split at t=180 (confirms P6b: blade
  budget is eta21 <= 0.06).
- PD2's chained c2 delivered BECAUSE the S-S bond (eta-independent) pushed it
  over the elbow while IT was on-line; only the bladed cargo is crotch-trapped.
- NEW ARCHITECTURE (PF1): FORK-FIRST, SHALLOW SLOPE. slope 1.2 => bladed cargo
  tracks its descending line closely (off-line few px only), detaches from blade
  ON-LINE, then every carrier return-lap DRAGS it down-branch (well ring at
  dy<15 has +x pull along the line) instead of ejecting. eta zone ends AT the
  elbow (x1=elbow): sorted floor is eta-free. Return laps FINISH the last
  delivery (drag-assisted descent).
- METRICS AMENDMENT (pre-cert, documented): RELEASED(k) = x1-crossing+glide OR
  carrier-interaction end (min dist to all carrier blobs > 15px sustained 300tu
  after pick). Fork-first layouts sort without an x1 lane crossing.

- PF1 (rec 20): shallow slope 1.2 keeps cargo ON-line (no crotch eject — slope
  rule confirmed) but blade slips at dy~9 (cargo veers off +x, decelerates,
  carrier passes); cargo left at dy 8-9 INSIDE well reach AND inside the zone:
  every return lap drags it back up-slope (measured y 40->48 during each zone
  transit), then re-blades it down: limit cycle, never sorted.
- SYNTHESIS -> P8 ARCHITECTURE (blade-convoy + past-dock stack + transverse drop):
  * eta zone ends at x1; cargo crossing x1 loses the well INSTANTLY (well =
    eta(x_cargo)*(u1-u0): eta=0 => invisible, exact ghost — species couple ONLY
    via eta). Blade abandons the last cargo at x1 + ~7px glide (DK glide law).
  * chain members past x1 keep being pushed by still-bladed rear members (S-S
    bonds are eta-independent): whole chain ends parked past x1 in a ~15px-spaced
    STACK. Parked stack is INVISIBLE to lapping carrier (eta=0) — fly-by immunity
    by construction, even on-lane.
  * fork line: x0 just past last queue slot, elbow (dy_max/slope) BEFORE x1+glide:
    every parked cargo sits ABOVE the branch FLOOR line (dy=18>15): pure
    TRANSVERSE drop to y=30 (certified GLv4 drop mechanism — no along-line force
    needed, no crotch contact: cargo never touches the crotch region x~x0).
- P8 (L=96 n=2 full pipeline) + P9 (n=1 solo abandon-glide) launched.

## V2a CERT LAYOUT (L=160, ready to launch on P8/P9 PASS)
- Lane y=48, M rails chan 0.002; cargo forkchan x0=101, branch -1, slope 2.0,
  dy_max 18 (elbow x=110), chan 0.004.
- eta21 xbox eta0=0.06, x0=8, x1=104 (dock edge; zone ends before elbow).
- Carrier blind pair at x=2,17.4 kicked +x. Queue: c1=26, c2=56, c3=86
  (spacing 30 = certified static; all inside zone).
- Expected: blade captures c1 (~t 100), chains c2 (~t 500), c3 (~t 900);
  convoy at ~0.072; c3/c2/c1 cross x1 in front-to-back order; stack parks at
  x ~111/126/141 (all past elbow 110); transverse drop to floor y=30
  (dy=18 > 15 footprint); carrier laps; stack invisible (eta=0 + species
  transparency) — one verification fly-by included in T.
- T=3500 (delivery ~1700 + settle + >=1 stack fly-by). 3 seeds {1,2,3}.
- Blade budget honest note: chain rides the PUSH branch (gap < d*=7.92, core
  repulsion) so n_max is set by the split floor (~5.3px at eta 0.06, PB0
  survived 5.34); P6 3-chain mean gap 6.68 min 5.61 OK; sequential-assembly
  transients are the seed risk.

- P9 (rec 21): mid-slope release trap CONFIRMED in isolation (x1=60 inside slope
  region 57-66): blade pushes cargo to 60.7 (eta half-dead), cargo tracks its
  descending line to dy~8.5, blade slips, cargo creeps BACK up-slope to lane
  (measured 400tu), slides -x to 50, re-bladed next lap: LIMIT CYCLE (period =
  lap time 1330tu). NEVER sorts.
- FORCE GEOMETRY (from tracks): (a) slope region x in [x0, elbow]: off-line blob
  feels backsurf db/dx = -eps*slope*sign(y-ytgt): parked/slow blobs are REJECTED
  backward; ON-line blobs feel none. (b) blade y-reach: cargo rides 7.1 ahead;
  well reach 15 => blade holds cargo only to dy ~ 8 below lane (PF1 slip at
  dy~9 QED). => the blade can never deliver INTO a deep branch; the cargo must
  cross x1 near lane level and drop TRANSVERSELY (certified GLv4 drop) after
  release. (c) S-S pushed members cross slopes fine (PD2/PB1 c2 delivered).
- LOCKED V2a GEOMETRY RULE: elbow = x0 + dy_max/slope <= x1 - 3w (slope region
  crossed at FULL blade power); queue entirely at x <= x0 - 6; stack parks past
  x1 (eta-free + transverse-drop zone); every parked position past elbow.
- P10 (L=96, n=2, slope 3, x0=48, elbow 54, x1=64, queue 14/42) + P11 (n=1)
  launched = the slope-3 full-power crossing test.

- P8 (rec 23): c2 (chain-pushed) DELIVERED (y=30.4, x=73.3, past elbow, floor).
  c1 (bladed) parked ON-LINE mid-slope at dy=6.75 (elbow 66 > x1=60 again):
  stable (eta-free + bond to c2 + on-line) but FAILS y_sort>=15. Chain-pushed
  cargoes always deliver; the bladed (last) cargo needs elbow <= x1 - 3.
- P10 (rec 22): SPLIT t=135 — QUEUE SPACING LAW: at 16px the forming S-S bond
  (sep>15.4 attractive) pulls the next cargo INTO the accelerating c1: blade gap
  5.03 < split floor. 18 (P6) survived 5.61; 30 (P5/P8) clean 5.84. Cert = 30.
- GEOMETRY LAW (final): elbow = x0 + dy_max/slope <= x1 - 3 (slope crossed at
  full blade power); bladed cargo glides ~7px past x1 onto the FLAT floor line
  (dy=18) -> pure transverse drop; stack = bonded cargoes at ~14.5 spacing on
  the floor, all past elbow, eta-free (ghost) + dy 18 > 15 (double-protected).
- P11 (running) IS the corrected n=1 geometry (elbow 54 <= 61). If it delivers,
  launch P12 (n=2, spacing 30: queue 26/56, x0=62 slope 3 elbow 68, x1=71)
  then V2a L=160 cert x3.

- P11 (rec 24): slope 3, elbow 54 < x1: bladed cargo entered slope, RAIL dragged
  it down-line (3px/px), blade slipped at dy~9 (x~51), off-line backsurf ejected
  it to x=39: lap-period limit cycle. With P9/PF1: BLADE-SORT IMPOSSIBILITY LAW:
  blade y-hold reach ~8 < y_sort 15; on-line mid-slope park is a ghost dead-end;
  off-line mid-slope = backsurf eject. A blade can NEVER fork-sort its own cargo.
  Chain-PUSHED cargoes sorted 3/3 across PD2/PB1/P8.
- ARCHITECTURE FIX: sacrificial PLUG cargo at queue REAR (carrier meets it
  first): plug takes the blade slot permanently; all real cargoes are chain-
  pushed -> sorted. Plug ends as a ghost (mid-slope dy~8 or on-lane past x1,
  eta-free, invisible to carrier). Plug = machine infrastructure (pusher shoe).
  Deliverables = real cargoes only (documented BEFORE cert).
- P12 geometry (L=96 proto): carrier 70/85.4 (wrap approach), plug@16, c1@40,
  fork x0=52 slope 3 elbow 58 <= x1-3=61, x1=64, dy_max 18. Expect: c1 pushed
  over elbow -> transverse drop y->30 SORTED; plug ghosts mid-slope; carrier laps.

- P12 (rec 25): PLUG ARCHITECTURE WORKS: real cargo c1 DELIVERED to floor
  (62.6, 30.2) via chain-push over the elbow + transverse drop; plug = blade
  rider in a lap-period limit cycle (re-bladed each lap -> mid-slope blade-slip
  dy~8-9 -> backsurf home). BUT delivered cargo wobbles +-2.3px (x 62.2-66.8)
  because the plug's cycle apex (54.8, 40) comes within ~14 of the floor cargo
  = inside S-S basin (15.4). P8 same story (c2 wobble 3.55px). FIX: floor depth
  dy_max=28 (y=20): plug cycle bottom y>=39 -> min distance ~19 > basin.
  ELBOW RULE REVISED: elbow<=x1-3 does NOT deliver the bladed plug (P12
  disproves: blade slips at line-depth ~8-9 regardless); it's unnecessary —
  chain-pushed cargoes cross slopes at full power (4/4 delivered: PD2,PB1,P8,
  P12). Fork can sit late in the zone.
- P13 (launched): P12 + dy_max=28 + queue spacing 24 (dynamic-pickup safety
  test; 16 split, 18/30 ok). Gates: c1 floor y=20 park, post-sort wobble <1px,
  plug-to-c1 min distance > 15.4, census frozen, 2+ laps.
- V2a CERT (on P13 pass): L=192 T=4000 (zone 8..136, fork x0=126 slope 3
  dy_max 28, queue 26/56/86/116 spacing 30, carrier 2/17.4): plug + 3 REAL
  DELIVERIES; 3 seeds parallel (~45min wall each, 1.5 tu/s est).

- P13 (rec 26): PASS — deep floor dy_max=28: c1 delivered (72.2, 20.2), post-
  delivery wobble 0.71px < 1 gate; plug-c1 min dist 24.1 > basin 15.4; census
  frozen. V2a architecture LOCKED: blade-plug + chain-push + late fork +
  transverse deep drop.
- P14 (flat 4-chain blade-load test, L=96 spacing 26) launched: gate = census
  frozen + blade gap > 5.3 through 3 pickup transients + 4-chain at pair speed.
  On pass -> V2a cert x3 at L=192 (T=5000: delivery ~2000 + full second-lap
  fly-by of sorted stack at ~4700).

- P14 (rec 27): PASS. 4-chain assembly certified at L=96: pickups t=10/130/280
  (26px gaps), blade gap min 5.33 (> split floor) through all transients, chain
  14.5-14.8 at pair speed 0.072, census frozen. Queue-approach suction ~0.5px
  in the last 100tu before pickup (bond tail) — queue gate applies BEFORE
  approach; static 30px spacing certified by P3 (0.55px/1500tu).

## V2a CERT BATTERY (locked geometry, launched)
L=192 T=5000 dx=0.5 noise=0.002. eta21 xbox (0.06, x0=8, x1=140, w=3).
M rails chan(48, 0.002). Cargo forkchan(48, x0=130, br-1, slope 3, dy_max 28,
chan 0.004, cap 30) -> elbow 139.3, floor y=20.
Carrier blind pair 160/175.4 kicked +x (approach through wrap, 42.6px).
Queue: PLUG@26 (sacrificial blade rider, documented infrastructure, NOT a
delivery), c1@56, c2@86, c3@116 (spacing 30).
Expected: chain pickups ~500/700/900/1100; convoy 0.072; c3->c2->c1 pushed over
elbow onto floor; plug slips mid-slope ~x=133, backsurf, laps with carrier;
stack parks ~147/162/177 at y=20 (28 off-lane, eta-free double-ghost);
T covers delivery (~2300) + >=1 full lap fly-by (lap 2670).
GATES (locked metrics.py + amendment rec 19): 3/3 delivered (picked+released+
sorted), queue integrity <1px pre-pickup, fly-by immunity <1px post-sort,
census frozen, cycle times + throughput reported. Seeds 1,2,3 + no-carrier
null (T=2000).

- V2a_null (rec 28): no-carrier control CLEAN of deliveries (4/4 parked on lane,
  census frozen). Fine structure: q0-q2 creep +0.7-0.9px/2000tu (+x, tail-sum
  drift), q3@116 creeps -1.33px/2000tu toward x~115 and decelerates: the FORK
  SHOULDER (b2 rises on-lane for x>x0 as the valley line departs) is a soft -x
  wall with ~15px reach — same footprint rule, new instance (fork shoulder
  repels parked on-lane cargo within ~15px of x0). Queue slots must sit >=15px
  before x0 (ours: 116 vs x0=130 = exactly 14 — marginal; drift at t<=1100
  (c3's expected pickup) ~0.45px < 1px gate, acceptable for cert; recorded).

## V2a CERT BATTERY RESULT (recs 29-31 + null 28): 3 seeds — PIPELINE FUNCTION
COMPLETE, END-STATE GATE FAILED (honest partial):
- ALL MACHINE PHASES WORK 3/3 seeds, near-identical timings (pickups 640-650/
  855-865/1075-1085; machine cycle 210-225tu; all 3 cargoes + plug conveyed,
  chain crosses dock front-to-back, all 3 real cargoes land ON THE FLOOR
  y=20.2 in a 15.3px-spaced stack; plug parks mid-slope ~(131,45); census
  frozen 6/6; queue integrity PASS pre-pickup (<1px).
- FAILED GATE: post-sort park. The floor stack is NOT static: it shuttles +-10px
  in x at period ~ lap time (1195tu), rigid (c3-c1 = 30.5+-0.6), on-floor
  (y 19.8-21.6), peak speed 0.046. ALSO plug pre-pick disp 2.1-2.3px > 1
  (blade wake reaches through the 42.6px start gap at L=192 —- start distance
  effect, documented).
- Stack-shuttle driver: NOT the carrier directly (fly-by min dist 29.6 at
  floor depth 28; transverse). Suspect: plug mid-slope cycle apex reaches
  20.5px of stack rear (inside S-S tail range ~ 2nd shell 25.7) once per lap
  -> periodic kick + rigid bonded stack + flat floor (zero x-restoring force
  once past the elbow line's x-clip) = free rigid-body oscillation.
- CONTROLS LAUNCHED: P15 stack-alone (no species1, no plug) and P16 stack+plug
  (no carrier) at exact delivered geometry: attribution before any redesign.

- P15/P16 (recs 32-33) ATTRIBUTION COMPLETE: stack-alone run shuttles IDENTICALLY
  (amplitude ~9px, period ~1600tu, rigid, all walls soft: elbow wall x~139 vs
  wrap wall x~190). Plug/carrier innocent (P16 same oscillation; plug itself
  drifts -7.5px, secondary). ROOT CAUSE = M4 TRAIN-LENGTH LAW BITES BACK:
  tau2=5.60 sits between the 3-train and pair drift thresholds. Thresholds:
  single 5.748 > pair 5.636 > 3-train ~5.562 (fit: c_shuttle=0.046 =
  sqrt(0.056*(5.60-tau_c3)) -> tau_c3=5.562). Single cargo parks; the DELIVERED
  BONDED 3-STACK IS A SELF-PROPELLED TRAIN bouncing in the floor box.
  ** NEW MACHINE LAW (stack-safety corollary to the near-onset cargo law):
  cargo tau2 must lie BELOW tau_c(n_max) of the largest bonded stack the machine
  ever parks, while staying hot enough to tow. For n=3: tau2 < 5.56. **
- FIX: tau2=5.50 (rotor-zone floor; parked-stack margin 0.06; still near-onset,
  response ~1/(5.748-tau) => ~60% of the 5.60 well: est v_max ~0.08 > c_pair
  0.059). T-tests at L=96: T1 stack-park (5.50/5.55), T2 blade-capture+chain.
  On pass: V2a re-battery at tau2=5.50 (3 seeds + null; over the L>=160 budget
  — documented as the honest cost of the discovered stack law).

- T1 (recs 34-35): stack-park PASS at tau2=5.50 AND 5.55 (net 0.64-1.08px/1500tu,
  decelerating; last-500tu 0.02-0.03px). Shuttle threshold in (5.55,5.60] —
  consistent with tau_c3~5.56 prediction. Stack-safety law CONFIRMED.
- T2 (rec 36): full pipeline at tau2=5.50 PASS at L=96: blade-capture, chain tow,
  delivery to floor (68.1, 20.25), park 0.3px/500tu WITH plug cycling at 22px.
  Response margin held (near-onset amplification still sufficient at 5.50).
- V2a FINAL BATTERY: tau2=5.50, L=192, 3 seeds (geometry unchanged). Null reuse
  JUSTIFIED+documented: the 5.60 null (rec 28) upper-bounds 5.50 queue drift
  (susceptibility decreases away from onset); budget honesty: this re-battery
  puts L>=160 runs at 10 total (>6 planned) — the cost of discovering the
  stack-shuttle law; T=5000 unchanged (covers delivery + full-lap fly-by).

- V2aF (tau2=5.50) FAILED 2/3 seeds so far: census_change at t~1080 = c3 (4th)
  pickup transient. Blade gap min 4.98 < split floor (~5.3). MECHANISM (new
  quantitative law): BLADE COMPRESSION ~ CHAIN LOAD / CARGO MOBILITY. Colder
  cargo (5.50) has lower near-onset mobility -> same convoy speed needs more
  transmitted force -> blade core-gap compresses: gap(min) 5.64-5.95 (5.60,
  c=0.072, n=4) -> 4.98 (5.50, same load) -> SPLIT. The near-onset dial trades
  parked-stack stability against blade capacity: TAU2 SQUEEZE, resolved by a
  2nd dial: CONVOY SPEED (tau1) sets the load.
- CANDIDATE FIX TESTS (L=140 blade-load rigs, scalar eta21=0.06, flat rails,
  4-chain assembly): A tau1=5.68 (c~0.050) tau2=5.55; B tau1=5.67 (c~0.044)
  tau2=5.50. Gate: blade gap min >= 5.6 through 4 pickups; census frozen.
  Winner -> final battery (T=6000, timing rescaled; budget breach documented).

- BL_A/BL_B (recs 43-44): BOTH PASS 4-chain assembly with slower carriers:
  blade gap min 6.07 (tau1=5.68/tau2=5.55) and 6.14 (5.67/5.50) >> split floor;
  census frozen; chains at 14.6-15.1. BLADE-LOAD LAW confirmed: gap_min rises
  from 4.98 (c=0.072, tau2=5.50) to 6.14 (c=0.044, same cargo) — load ~ n*c/mu.
- FINAL GEOMETRY LOCKED (V2aG): tau1=5.67 (c~0.044), tau2=5.50 (stack margin
  0.06 below tau_c3~5.56; blade margin 6.14). Queue 20/50/80/110 (c3 now 20px
  from fork x0=130 — outside the measured ~15px shoulder-halo reach; the 5.60
  null's q3 creep 1.42px was at gap 14). Carrier 160/175.4. T=6000 (delivery
  ~3600 at the slower c + post-delivery lane pass over the parked stack =
  fly-by gate + settle). Seeds 1,2,3 + fresh null (positions changed).
  BUDGET: honest overrun — L>=160 runs total will be 17 (planned <=6): cost of
  two discovered laws (stack-shuttle, blade-load). All documented.

- V2aG (tau2=5.50, tau1=5.67, rec 45): seed2 census_change t=2000 — NOT blade
  compression (gap min 6.01 OK). NEW MODE: SLOW-CONVOY BUCKLING: plug transverse
  oscillation grows over ~2 laps (y 48->56->46), convoy jams, c1/c2 forced into
  a y-split pair -> split. M5's "v1 buckles without rails" at convoy scale: rails
  (0.002/0.004) do not stabilize the blade contact at c~0.044. Seeds 1/3 KILLED
  mid-run to conserve budget (same params; partial tracks not saved — honest
  cost documented).
- THE TAU2 SQUEEZE IS CLOSED (both walls mapped):
    stack-safe: tau2 <= 5.55 (T1)   blade-safe at c=0.072: tau2 >= ~5.6 (V2aF)
    blade-safe at c=0.044: tau2=5.50 OK but convoy buckles (V2aG).
  For n=3+plug at L=192 the operating window of THIS architecture is empty or
  knife-edge. n=1 (plug+cargo) is CERTIFIED end-to-end at L=96 (P12/P13/T2:
  delivery + park + all gates). n=3 at 5.60: complete function 3/3 seeds, fails
  only the post-sort park gate (stack = self-propelled train).
- FINAL VERDICT RECORDS + SUMMARY + film below. V2b/V2c/V2d NOT REACHED.

- V2aG_seed3 (rec 43-ish): census_change t~2000, same buckling mode as seed2 (appended before process kill). V2aG = 2/2 completed seeds buckled + 1 killed. Verdict records already reflect this.
