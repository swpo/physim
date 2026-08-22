# L0 STAGE-3 CENSUS — carrier catalog, plateau verdict, encounter tables
(2026-02-22, l0-sampler. Data: stage3/outs/ 17 shards, 1068 records, all ok.
Verification sims this analysis: 7 of budget 15, logged in ../results.json.)

## 1. CARRIER CATALOG (kicked act-indexed A1, V4; 24 travelers / 996 worlds)
Rank cand              act ref       c       steady  area  engine(tau_v,D_v,A)
  1  s2_118_41_jit      0  XV        0.3036  1.019   37.5  5.16, 0.69, A=3.58
  2  s2_112_64_jit      1  e1_9513   0.2450  1.029   39.0  6.19, 0.69, A=4.24
  3  s2_113_76_jit      1  e1_9513   0.2083  0.926   39.0  4.42, 0.84, A=3.70
  4  s2_107_48_jit      1  rh1_7000  0.2038  1.016   34.0  4.22, 0.60, A=2.53
  5  s2_128_66_jit      1  e1_9513   0.1904  0.993   40.5  6.07, 0.69, A=4.18
  6  s2_107_21_jit      0  rh1_7000  0.1770  1.010   32.0  5.59, 0.58, A=3.26
  7  s2_117_22_jit      1  rh1_7000  0.0889  0.836   26.0  4.45, 0.57, A=2.51
  8  s2_100_30_jit      1  e1_9513   0.0819  0.890   36.0  6.29, 0.71, A=4.46
  9  s2_128_43_jit      0  e1_9508   0.0561  1.341*  23.0
 10  s2_112_82_jit      0  BFIELD    0.0558  0.922   34.5
 11  s2_107_31_jit      1  XV        0.0399  122.9*  46.5  (bare; late take-off)
 12  s2_106_69_jit      0  BFIELD    0.0375  2.246*  27.5
 13  s2_121_46_jit      0  BFIELD    0.0372  2.302*  28.0
 14  s2_108_18_jit      0  BFIELD    0.0360  2.302*  20.0
 15  s2_130_76_jit      0  BFIELD    0.0321  1.178   31.5
 16  s2_117_71_jit      0  e1_9508   0.0274  1.303*  28.0
 17  s2_108_72_jit      0  BFIELD    0.0237  2.130*  27.5
 18  s2_104_55_jit      0  BFIELD    0.0235  2.457*  26.0
 19  s2_107_33_jit      0  BFIELD    0.0217  1.555*  25.5
 20  s2_102_41_jit      0  BFIELD    0.0193  1.337*  30.0
 21  s2_114_43_jit      1  e1_9513   0.0187  1090*   45.5  (bare; late take-off)
 22  s2_110_11_jit      0  BFIELD    0.0163  2.110*  21.0
 23  s2_116_63_jit      1  e1_9508   0.0161  31.1*   117.5 (big blob, slow slide)
 24  s2_116_77_jit      0  e1_9508   0.0152  1.334*  30.0
(*steady_ratio>1.3 = still ACCELERATING at T=300 — BFIELD stigmergic launchers
build their b-trail slowly; ranks 12-22 are lower bounds on terminal c.
c_repeat/c ratio = 1.000 for all 24: kicked protocol deterministic.)

RECORD VERIFIED: s2_118_41 fresh rerun T=600 -> c=0.30367, window-ratio 1.0001
(4-digit steady). Genome: XV-line 2-act 4-chan; the traveling species' engine
is (tau_v=5.16, D_v=0.69, A=3.58) with k1 fold-dist ~0.02; W cross-drives
0.074/0.096 (near-decoupled twin worlds — the OTHER act also has an engine
at A=2.84*1.69=4.8 but reads multi under pokes).

## 2. MOTILITY GEOGRAPHY
Travelers by reference line (census n / travelers / rate):
  BFIELD 61/10/16.4%   e1_9513 117/5/4.3%   rh1_7000 76/3/3.9%
  e1_9508 159/4/2.5%   XV 133/2/1.5%
  M0 112/0, VVW 151/0, uni_3034 84/0, uni_3050 39/0, M4 58/0, uniform 6/0.
Overall 2.4% of alive worlds travel — matches stage-2's A3 ladder finding
(27 onset flags/996 alive = 2.7%) — the two independent protocols agree.
TWO MOTILITY MECHANISMS ONLY:
  (a) stigmergic self-launch (BFIELD line, 10/24): slow tanh b-channel,
      c ~ 0.02-0.06 and still accelerating; M6 physics, now shown robust
      under +-15% whole-genome jitter.
  (b) two-timescale v/w engines (14/24, ALL in XV/rh1/e1 lines): private
      slow-v + fast-wide-w per species, A=tau_v*D_v in 2.5-4.5, c up to 0.30.
      NONE of the M0/VVW-family (single shared-w, tau~3) jitters travel:
      drift needs either the near-onset A~4 corner (M4's, none sampled
      alive+traveling here) or the two-timescale engine geometry.
Six stage-2 "masked travelers" did NOT reproduce in the census (persist,
c~0.002-0.008): those were coast-boundary cases at the +-1% ladder edge —
consistent with conservative steadiness gating, honestly reclassified.

ENGINE DECOMPOSITION (local follow-ups, logged): s2_107_48's act1 + its 2
channels run STANDALONE (3 fields): c identical (0.2038). One-dial island:
travel +-10% on all dials; c rises with Du*1.1 (0.2788 in-situ) and D_v*0.9
(0.2516 standalone); COMBINED Du*1.1 & D_v*0.9 standalone: c=0.3439 — NEW
RECORD, beats the census record with 3 fields. Speed dial = raise Du/D_v
contrast until the replicate edge (tau_v +10-15% replicates; D_v +15% stalls).
=> machine-v3 carriers: engine_10748 variants give c 0.20-0.34 in a 3-field
world; XV-line s2_118_41 gives 0.30 in 6 fields with a second species slot.

## 3. PLATEAU-BOND DESIGN RULE (pair grids d0 8-28, T=800)
uni_3034 family (d* ~ 28):
  baseline: bond basin d0 12-24, d*=28.0 (merge at d0<=10) — basin is WIDE.
  thr*0.8:  d*=29.8, basin grows (bond at 28 too). thr*1.2: basin shrinks
            (bond 16,24 only, d*=29.4). thr*0.6/1.4: bond LOST (pairs run to
            antipodal 30.1-32 = repel-only). => thr window ~[0.6,0.9]*base,
            d* rises ~+1.8px per -20% thr. WEAK lever, STRONG existence gate.
  sc*0.5/0.75: intact (d* 28.5/28.4). sc*1.5: basin thins; sc*2: only d0=24
            bonds. => saturation sharpness is a BASIN dial, not a d* dial.
  K_tanh*1.2/1.4: intact, d* 28.1/26.8 (harder pull-in shortens d* slightly);
            K_tanh*0.8/0.6: bond lost / marginal (16-18 only). => K_tanh is
            the bond-STRENGTH dial; existence needs K_tanh >~ base.
  SLOW-CHANNEL SURPRISE: tau_slow*0.5 -> THREE shells (20.8/24.5/28.5)
            appear; tau_slow*2 -> replication; D_slow*2 -> all merge til 14
            then antipodal; D_slow*0.5 -> dies. => d* is set by the SLOW ID
            CHANNEL's screening structure, not by the tanh channel; the tanh
            plateau only opens a window where that structure can hold blobs.
  REVISED MECHANISM PICTURE: tanh channel = existence + capture (plateau
  well); slow id channel = spacing quantizer (d* and shell count). d* is
  tunable 20-30px via tau_slow — INDEPENDENT of u-tail wavelength physics.
s2_128_26 ATTRIBUTION SETTLED (ablations + 2 verification cuts):
  K0(id,3.3/3.1)=0: bond keeps (d*=14.4). K1(tanh)=0: REPEL to 66 (bond
  LOST — resolves the stage-2 controller-audit discrepancy: their tanh-cut
  kept a bond at 14.9; the discrepancy object is the K path they cut vs
  mine; with BOTH the drive W[1][0]=0 and feedback K[0][1]=0 cut here, bond
  is lost both ways at T=800). K2(id,2.3/2.3)=0: merge (repulsion source).
  => SAME mechanism CLASS as uni_3034: tanh=binder, id=spacer/repeller,
  at 2x shorter d* (14 vs 28) because its id-channels are 2-3x shorter-
  ranged. ONE mechanism family, two length scales. (Controller's stage-2
  d*=14.9-after-tanh-cut remains unexplained in detail — flagged, likely
  their cut left the W drive intact and mine cut both; not blocking.)

## 4. STACK VERDICT (machine stack-safety question) — PLATEAU STACKS PARK
stack_probe T=2000 (V4 gate: COM<=2px, blob<=4px, census intact):
  s2_128_26  n=2/3/3+noise: PARKED (COM 0.00, blob 0.02-0.06, spacing
             14.03-14.06 +-0.0004) — dead-still to 4 digits, noise-proof.
  uni_3034   n=2/3 with dressed stamps: die (dressing overdose at 27.9px
             overlap); RE-RUN BARE (its native variant, 2 sims): n=3 PARKED
             (COM ~1e-14, end blobs relax 1.4px to spacing 29.34, then
             frozen; noisy seed: COM 2e-4, spacing_std 4e-4). PARKED.
  M4 control n=2/3: parked clean; n=3+noise sigma=2e-3: SHUTTLES (COM 86px!)
             — reproduces machine-v2's stack-safety law (M4 stacks are
             latent trains; noise releases them).
=> ANSWER TO MACHINE-V2: plateau-bonded stacks are SELF-PROPULSION-FREE
   cargo. Both plateau worlds pass where the M4 control fails. d* menu:
   14.0px (s2_128_26) or 20-30px tunable (uni_3034 tau_slow dial). These
   stacks sit at d* set by channel screening, not tail shells — no
   tail-phase coupling => no traveling-bond branch to fall into.

## 5. ENCOUNTER TABLES (6 three-flavor worlds; d0 8/12/16; cross + same)
Classification per world:
  s2_116_63 (repl|fragile cell):   PREDATORY-UNSTABLE. 0-x: replicate on
    contact (all d0); 1-2 approach/repel. Species 0 is an infection vector.
  s2_131_74 (merge|fragile):      MIXED. 0-2 static-locks at ALL d0 (frozen
    cross-species lattice!), 2-2 bonds 14.7-14.9; but 1-x replicates.
  s2_116_46 (bond|robust):        MOSTLY-INERT. 0-0 bonds 13.1; 0-2 static/
    repel; NO replication anywhere; one 8px cross_bond collapse (d*=0.4 =
    core-merge artifact of a deep well — logged as caveat).
  s2_130_83 (repl|robust):        FRAGILE-SPECIES world: 1-1 and 2-2 die at
    all d0 (self-annihilating flavors), 0-x replicates at close range.
  s2_101_58 (repel|onset):        PREDATION CONFIRMED: 1-2 kill_j at ALL d0
    (species 1 eats species 2, conserved at 8/12/16); 0-1 replicates;
    0-0 bonds at 14.6. World with food chain + self-bonding apex — flag
    for world catalog as an ecology primitive, NOT a rail candidate.
  s2_111_17 (repel|robust):       THE SPECIES-RAIL NOMINEE. ZERO replication
    in 18 assays. 1-2 cross_bond d*=11.1 (from d0=8; static-locks at
    12/16); same-species: 1-1 bonds 15.2/16.5, 2-2 bonds 14.0/16.3,
    0-x repel/approach only. Three distinguishable port behaviors:
    sp1&sp2 bind each other AND themselves; sp0 is a pure repeller
    (natural fence/sorter blade material).
NOMINATION for machine v3: s2_111_17 — criteria met (cross-bond exists
d*=11.1; no replication in any of 18 encounter assays; species
port-distinguishable by bond menu). Runner-up s2_116_46 (inert-robust,
one deep-well caveat).

## Cost note
Census 996 worlds: 65.2 core-hr (shard walls); island+plateau+encounter
13.6 core-hr. Stage-3 pods total ~79 core-hr — under the 100-150 budget;
the census answer (2.4%, two mechanisms only) closes the motility gap.
