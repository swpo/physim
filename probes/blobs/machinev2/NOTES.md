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
