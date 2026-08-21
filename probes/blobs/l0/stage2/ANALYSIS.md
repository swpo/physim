# L0 STAGE-2 HARVEST — ANALYSIS (2026-02-19/20, l0-sampler)
Data: stage2/merged_results.json (3195 candidates; 1263 uniform + 1932 jitter,
0 error rows) + merged_archive.json (404 cells). Pods spent ~325 core-hours
(mean 367 s/cand = 9.8 cand/hr/core). Targeted follow-ups this analysis: 7
short runs (a3 control, 2 mask checks, 4 ablations), logged in results.json.

## 1. YIELD CURVES v2 (data_yield_v2.json)
                     UNIFORM (n=1263)   JITTER (n=1932)
  G0b / G0a pass       83% / 83%          100% / 96%
  osc tails / chem     25% / 10%          86% / 80%
  ALIVE per 100        0.47               51.2
  bond per 100         0.08               24.1
  onset flag per 100   0                  1.4
  cost mean / median   34s / 5s           584s / 273s
Stage-1 predictions vs reality: jitter alive 49%->51% CONFIRMED; uniform cost
40->34s CONFIRMED; uniform alive 2%->0.47% (stage-1 n=2 was small-n luck);
jitter cost 199->584s mean (x3: V3.1 ladder runs only on alive candidates +
3-act evolver elites at 9-10 fields; cost scales with success — good failure
mode). Jitter bond 14->24% (elite pool is binder-rich).

By jitter reference (n / alive% / bond% / mean cost):
  e1_9508   177  89.8%  41.8%  1697s   <- 3-act evolver elite: best alive-rate
  XV        169  78.7%  43.8%   820s      in the whole program
  VVW       197  76.6%  47.2%   903s
  e1_9513   207  56.5%  26.1%  1140s
  M0        208  53.8%  30.8%   268s
  uni_3034  192  43.8%  27.6%   331s   <- stage-1 novelty jitters WELL
  rh1_7000  174  43.7%  12.6%   402s
  BFIELD    207  29.5%   5.8%   123s
  M4        214  27.1%   8.4%   117s
  uni_3050  187  20.9%   1.1%   196s   <- alive-stable but bond-poor
Fold-distance stratification (fix 5 payoff): alive median fold-dist 0.020
(q25-75 0.006-0.030) vs domain 0.27 / die 0.20. The fold shell |1-|k1/k1max||
< ~0.05 is where blobs live, CONFIRMED at n=3195 across all architectures.

## 2. ATLAS TOUR — 404 cells (245 alive-bearing; 68 bond cells)
Coverage: n_act 1/2/3 = 88/167/149 cells; n_tanh 0/1/2/3 = 156/215/28/5;
pair classes: bond 68, repel 67, replicate 53, approach 27, merge 12,
bond_wrap_artifact 6 (filter worked); motility: onset 19 cells, near_onset 3.
2-act BOTH-species-alive: 15 cells (incl 8-count persist|persist|bond cell);
3-act ALL-THREE-alive: 8 cells — including bond+all-alive (see T1).

TOP-10 CELLS (novelty-ranked, exemplar cand + physics guess):
T1  3|5|1|1|1|persist|persist|persist|bond|robust_static (n=4)
    3-species all-persist WITH bond. e1_9508 descendants (evolver 3-act
    elite line). First 3-flavor bonded matter in the program. Physics: three
    near-fold activators sharing staggered inhibitor lengths — a flavor
    lattice candidate. NEXT: encounter table + selective-drift check.
T2  1|2|1|0|0|persist|bond|robust_static (n=41!) — the uni_3034 FAMILY:
    non-oscillatory binder is ROBUST under jitter (41 archive entries, 53
    bonded candidates). See section 3-mechanism: ablation shows tanh channel
    IS the binder. New binding mechanism vs everything certified.
T3  2|4|0|1|1|multi|persist|repel|onset — s2_107_48 (rh1_7000 line):
    FASTEST steady traveler in program history: c=0.204 px/tu VERIFIED by
    fresh kicked rerun (steady c_prev 0.201; M4 pair record was 0.14).
    rh1_7000 = 2-act 4-chan two-timescale world (tau 5.8/0.7 x2), W cross
    0.24. Physics guess: strong v-shadow asymmetric heterodimer near onset.
T4  1|2|1|1|1|persist|repel|onset (n=6) + 13 BFIELD masked-travelers:
    jittered M6 worlds that SELF-LAUNCH in plain A1 (gamma 0.043-0.067,
    tau_b 167-251, D_b~0): the M6 autophoresis window reproduced by blind
    sampling — gamma>=0.005 certified threshold, all sampled gammas above.
T5  s2_101_61_jit (XV line) 2|4|0|1|1|multi|persist|bond|onset:
    TRUE asymmetric onset: travel ONLY at tau1-1% (c=0.0255), persists at
    +1/+2/+5 — a one-sided drift window edge caught in-ladder. Rotor-zone
    analogue in jittered xv space.
T6  1|1|2|1|1|persist|merge|robust_static (n=19) — uni_3050 family:
    tanh-dominated (2 tanh + 1 id) with exciting K entry; merge-or-repel
    pair logic (no bond). Alive-robust but bond-poor: deposit channels
    saturate the interaction. Complementary regime to T2.
T7  2|4|0|1|1|persist|persist|bond|robust_static (n=8): two-species bonded
    matter OUTSIDE certified refs (XV/rh1 jitter mix) — cross-species-bond
    generalization of M7's RT2 exists across a whole cell, not one point.
T8  near_onset cells (n=3 cells / 4 cands): coast-classified ladder steps =
    critical-slowing shelf worlds; cheap M1-style motility candidates for
    stage 3 (dial straight to the shelf).
T9  s2_128_26_uni 2|2|1|0|0|persist|die|bond|robust_static: the ONLY
    uniform-random non-osc binder outside T2's family: 2-act (one dies,
    survivor bonds at 13.2/14.1 from d0 8/12) with THREE mixed channels;
    fold-dist 0.08/0.09. Independent invention of monotone-tail binding —
    mechanism NOT the uni_3034 clone (no exciting channel: K=[0.26,0.56,
    1.71] all-inhibiting; likely tanh-saturation well again, unablated).
T10 1|2|0|1|1|persist|bond|* M0/M4-jitter bond cells (n=2+3+...): the M2
    binding zoo re-found by blind jitter — sanity anchor that the pipeline
    rediscovers certified physics without being told.

## 3. d*/wl LAW v2 (830 osc-tail bond outcomes)
First shell: n=677 in ratio 1.0-1.7, mean 1.369 +- 0.126 — controller's
[1.2, 1.5] band holds (79% of first-shell mass); peak bin 1.3-1.4.
Second shell: n=148, mean 1.924. Ladder spacing 1.92-1.37 = 0.55 wl,
consistent with stage-1 (half-wavelength shell ladder; tail-lock at
alternating phase). >2.6: 1 outlier. The law is ORDER-OF-SHELL physics as
the controller ruled: d* = (1.37 +- 0.13 + 0.55k) * wl_G0c.
CAVEAT (honest): consecutive-shell spacings measured WITHIN one candidate
(139 pairs) center at 0.44 wl, below the population 0.55 — A2's T=400 may
truncate slow relaxations mid-shell; per-candidate shell assignment is
noisier than the population statistics.
NON-OSC binders (54): d* 24.3 +- 3.7 px (range 13-30), NO wavelength to
compare. 53/54 are uni_3034-family jitters + 1 independent uniform (T9).
MECHANISM SETTLED BY ABLATION (4 runs, logged):
  baseline           -> bond d*=27.9
  K_tanh = 0         -> approach->infinity (repulsion-only, NO bond)
  K_exc  = 0         -> dies
  K_exc flipped +    -> dies
  => The EXCITING fast channel (K=-1.03+-0.16 conserved across all 53
  jitters) is the EXISTENCE ingredient; the tanh channel (K_tanh=+0.90
  +-0.11) is the BINDING ingredient. Binding without oscillatory tails =
  saturating-inhibitor plateau well: tanh output flattens near the blob,
  creating a finite-range attraction shelf invisible to G0c linearization
  (gprime(0)=0). NEW MECHANISM CLASS, name proposal: "plateau bond".
  d* weakly correlates with the slow channel's sqrt(tau*D) (r=0.39, d*~3.8
  sqrt(A)) — no clean single-length law yet; d*-theory needs the tanh
  saturation radius (nonlinear, stage-3 question).

## 4. A3 POSTMORTEM — "0 travelers" is FALSE; the ladder WORKS
Controller first-pass saw A1 travel=0 (true: symmetric A1 can't reveal
drift) but the LADDER found 49 travel steps across 27 onset-flagged
candidates + 5 coast steps. Breakdown after masking analysis:
- 22/27 are MASKED ALREADY-TRAVELERS: travel at BOTH -1% AND +1% with
  |c_m - c_p| < 10%. Their BASE genome travels too — the base A1 poke is
  symmetric (kick_px=0) so the blob sits on the unstable symmetric branch
  and reads persist (BF5 lesson, now measured at scale). VERIFIED: fresh
  kicked A1 on s2_107_48 base -> steady travel c=0.2038.
- 5/27 are TRUE ONSETS (asymmetric ladder response, e.g. s2_101_61 travels
  only at -1%).
- CONTROL (fresh run): ref M4 tau=6.0 (certified c=0.1234): symmetric A1
  -> persist c~7.6e-13; kicked A1 -> travel c=0.12346 (0.05% on cert).
  The pipeline detects certified drift when kicked. LADDER NOT MIS-FIRING.
- Ladder "domain/replicate" steps (421/325 of 3665): tau+-5% steps off
  narrow islands — real island-edge physics (M4's mapped replication
  ceiling), not a bug.
FIX FOR STAGE 3 (one line): A1 panel gets kick_px=0.5 ALWAYS (the V3.1
steadiness gate already separates coast from travel, so kicks cost nothing
statistically). Expected: ~22 more A1-travel candidates for free + drift
windows measurable in-batch.

## 5. STAGE-3 RECOMMENDATION
Worth another pod run? YES, but smaller and targeted (~100-150 core-hours),
because three NEW questions now have cheap, specific experiments:
 a) TRAVEL CENSUS (fix applied): kicked A1 => how common is motility really?
    Re-run ~400 alive-cell exemplars/jitters at ~60 core-hours. Answers the
    biggest open gap (M1-equivalents in new families; T3's c=0.2 line).
 b) PLATEAU-BOND PHYSICS: jitter T2/T9 with a d*-focused battery (A2 at
    d0 6..30 step 2, T=800) + tanh-radius theory probe: does d* scale with
    thr/sc/W of the tanh channel? (~20 core-hours; would give the first
    non-G0c binding design rule — directly useful for machine building at
    a second length scale independent of wl.)
 c) 3-FLAVOR MATTER (T1): encounter tables + per-species tau dial on the
    e1_9508 bonded line (~20 core-hours; feeds L3 composition: 3-species
    machines need conversion/selectivity rules).
 NOT worth more: blind uniform at current settings (0.47 alive/100,
 mechanism yield ~1 novelty/600 candidates; the two we have are being
 mined by jitter already). If uniform continues, bias it: sample fold-dist
 log-uniform in [0.003, 0.1] (alive median 0.02) — predicted alive-rate
 x5-10 from the fold-shell stratification.
Bundle changes for stage 3: kick_px=0.5 default in A1; optional A2 extended
d0 grid mode; elites file += T1-T9 exemplars.

## Files
data_yield_v2.json (curves), this ANALYSIS.md; follow-up runs in
../results.json (kinds a3_postmortem_control, mask_check, ablate_3034).
