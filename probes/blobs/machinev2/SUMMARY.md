# MACHINE-V2 — multi-cargo logistics line (phase 4, L3 composition) — SUMMARY

**Verdict: V2a HONEST PARTIAL. The full fulfillment-line FUNCTION is certified
3/3 seeds at L=192 — one carrier sweeps a 3-cargo queue, convoys it through the
eta zone, releases the chain at the dock, and the fork sorts ALL THREE real
cargoes onto the branch floor as a clean stack, census frozen, queue integrity
clean, machine cycle 215+-5 tu. The certification FAILS on one locked gate:
the delivered stack does not stay parked — the bonded 3-stack is a
SELF-PROPELLED TRAIN (M4 train-length law biting back), and the parameter
squeeze that would fix it (colder cargo) is closed off by two more discovered
laws (blade compression, slow-convoy buckling). Single-cargo delivery (plug +
1 real cargo) IS certified end-to-end at L=96 in 3 geometries. V2b/V2c/V2d not
reached. Three new quantitative machine laws + a 7-entry interference map are
the deliverables.**

Engine: verbatim factory/sim.py + runjob.py (xv 6-field + eta(x,y) + per-species
b). ANCHOR: GLv4_seed1 reproduced BIT-EXACT before building (net1 293.19/293.02,
net2 80.31, pair stats to 4 decimals). metrics.py locked before cert batteries;
one documented amendment (rec 19: carrier-interaction-end release for fork-first
layouts — before any battery). 46 records in results.json; save-as-you-go.

## The machine (final architecture)
L=192 torus. Carrier lane = M-rail chan(y=48, 0.002). Cargo fork = forkchan
(x0=130, branch -1, slope 3, dy_max 28 -> floor y=20, chan 0.004). eta21 xbox
(0.06, x0=8, x1=140) = tow zone + dock edge. Carrier = blind M-M pair (tau1=5.7,
kick +x). Queue on the lane inside the zone: PLUG at x=26 (sacrificial blade
rider — documented infrastructure, not a delivery) + real cargoes c1/c2/c3 at
56/86/116 (30px spacing), all tau2=5.60 near-onset S.
Function (identical 3/3 seeds): carrier wraps, captures the plug on its BLADE
(push-capture: cargo rides 7.1px AHEAD of the front M), chains c1/c2/c3 via
eta-independent S-S bonds (pickups 640-650/855-865/1075-1085; machine cycle
215+-5 tu), convoys at pair speed 0.072, chain crosses x1 front-to-back, blade
loses the plug at the dock, chain glides on, the fork drops each real cargo
TRANSVERSELY to the floor (y=20.2, 15.3px stack at x~147/162/177), carrier laps
forever, stack is eta-invisible (ghost) + 28px off-lane (double-protected from
fly-bys). Functional throughput 0.6 deliveries/1000tu; service time 1640-2065 tu.

## Why full certification failed (the three laws)
1. STACK-SAFETY LAW (failed gate): the parked bonded 3-stack shuttles +-9px
   (rigid, on-floor, period ~ lap time). P15 isolation control: INTRINSIC — the
   stack alone does it. tau2=5.60 lies between the pair (5.636) and 3-train
   (~5.56) drift thresholds: a single parked cargo is immobile, the delivered
   3-STACK IS A MOTILE TRAIN. Rule: cargo tau2 must be < tau_c(n_max_parked).
   Verified: 5.50/5.55 stacks park (0.02-0.03px/500tu); threshold in (5.55,5.60].
2. BLADE-LOAD LAW (closes the cold-cargo fix at speed): blade core-gap
   compresses with chain load x speed / cargo mobility. At c=0.072, n=4:
   gap_min 5.64-5.95 (tau2=5.60, survives) -> 4.98 (tau2=5.50) = SPLIT at the
   4th pickup, 3/3 seeds. Split floor ~5.3-5.4. Slower carriers restore margin:
   gap 6.01-6.14 at c<=0.050 (BL rigs, 4-chain assembly clean).
3. SLOW-CONVOY BUCKLING (closes the slow fix): at tau1=5.67 (c~0.044) the blade
   contact goes transversely unstable over ~2 laps (plug y-oscillation grows
   48->56->46, chain jams, forced y-split pair -> split) despite both rails.
   M5's "buckles without rails" honest negative, reborn at convoy scale.
=> For n=3 + plug, the operating window (stack-safe AND blade-safe AND
   buckle-safe) is empty or knife-edge in this architecture. Certified capacity
   of THIS line: n=1 real cargo per pass (P12/P13/T2 end-to-end at L=96, all
   gates incl. park <1px, plug-cargo min dist 24 > 15.4 footprint, census).

## INTERFERENCE MAP (7 mapped entries — the design handbook payload)
I1 Head-on pickup at eta21>=0.1 = cargo SPLIT (open lane, dy<=6 stagger, crotch).
I2 eta21 0.05-0.08 head-on = PUSH-CAPTURE blade: rails convert factory's
   swing-around into permanent front capture; blade is stable at 7.10-7.16px,
   full pair speed. => sequential single-service is IMPOSSIBLE on one railed
   lane: the blade captures every in-zone on-lane S it meets. Convoy or nothing.
I3 Queue spacing: <=16px self-bonds (feeds the blade -> split); 24px creeps
   1.4px/2000tu (S-S tail); 30px certified (0.5-0.9px).
I4 Fork-shoulder halo: on-lane parked cargo within ~15px of forkchan x0 is
   repelled -x (1.33px/2000tu measured). Queue must end >=15px before x0.
I5 Crotch/slope traps (4 limit cycles mapped): a BLADED cargo can never be
   fork-sorted — blade y-hold reach ~8px < y_sort 15; on-line mid-slope park at
   eta=0 is a ghost dead-end (re-bladed next lap); off-line = backsurf ejection
   ~ chan_eps*slope. Blade-slip happens at line-depth dy~8-9 for slope 1.2-4.
I6 Chain-PUSH sorts: S-S bonds are eta-independent and cross fork slopes at
   full power — every chain-pushed cargo delivered+sorted (6/6 across protos).
   The plug converts the un-sortable blade slot into machine infrastructure.
I7 Mid-slope parking contact: the plug's limit-cycle apex approaches the stack
   rear to ~20.5px (2nd-shell range) once per lap — periodic kick amplifies the
   free stack train (V2a wobble). Deep floor (28px) + tau2<tau_c3 kills both.

## Files
results.json (46 records: 1 anchor, 20 protos, 4+2 cert batteries + controls,
2 blade rigs, 3 metrics/amendment/verdicts) · sim.py runjob.py (factory verbatim)
· metrics.py (locked + 1 pre-cert amendment) · analyze_v2a.py · strips.py ·
strips/fig1_layout.png fig2_delivery_film.png fig3_throughput_stacklaw.png ·
NOTES.md (full session log incl. two killed runs) · data/ (tracks + snaps).

## Budget honesty
L>=160 runs: 15 (plan <=6). Overrun = the discovered-law cascade (stack shuttle
-> re-battery; blade law -> re-battery; buckling -> killed 2 runs mid-flight).
Each re-battery decision recorded in NOTES before launch. L=96 protos: 22.

## Handoff
- To certify n>=3 park: EITHER colder cargo + per-segment eta boost at pickup
  (needs eta amplitude shaping — new primitive), OR de-bond the stack on the
  floor (spacing >19.5 at release: fork with per-cargo branch offsets), OR park
  cargoes in separate wells (teeth on the branch floor — genesis grooves).
- V2b two-way sort: needs species-tagged rails per cargo class (3rd species) or
  per-cargo eta; tau-contrast alone cannot split a chain (both classes chain
  behind one blade).
- The plug primitive (sacrificial blade rider) is reusable: it converts the
  un-sortable blade slot into infrastructure and self-parks as a ghost.
