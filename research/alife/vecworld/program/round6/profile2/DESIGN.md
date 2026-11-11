# Exam profile 2: design (synthesis for the coordinator and the lead)

11 Nov 2026, design only; joins `spec/SPEC.md` and `feasibility/`; program files read at a5afef952. Sources: [T] `feasibility/timing.json` (key named); [D] `derived.json` from `derive.py`
(arithmetic on [T] and the files it names); FL = `../foundrylong`, A2 = `../dials/dialsA2`. **x86** = measured on 2
pinned cores of the shared cloud container (load 1.2-2.1 from other work: lower bounds). **Mac** = not measured
anywhere: Mac compute time = x86 time / r, r unknown (FEASIBILITY.md infers 0.5 to 2). `feasibility/run_f.sh`,
`run_g.sh`, `run_f32.sh` in one Mac box (about 45 min) measure r; until then every told number is an x86 placeholder.

## 1. Purpose, recommendation, decision rule

The lead wants rollouts on supervenient worlds whose scores say something: "tests that are not trivially easy", where
an agent's way in (simulate, fit, hypothesise, experiment) separates it from the scripts (`../../roadmap/DECISIONS.md`,
Direction). The port's only profile, ring, is solved in closed form (0.964, `../rollouts/README.md`); profile 2 is the
first on a world without a closed form whose science share passes the bar at the ceiling, under decision 2's told
budgets. **Recommendation:** build **F** (foundry hidden weights, `foundry_v1`) first if foundrylong's stage 2 qualifies
it by the rule below, with a 32-episode Lab (2,080 ticks, reset 17, 12,800 nats), 180 minutes of wall time, a
research budget of about 3,800 full episodes (x86 3,783 [D `F.B_res_full_episodes_x86`]), a prediction budget of 0.25
(52.7 s wall and 75 CPU-s per item on x86 [D `F.item_b0.25_x86`]), 150 turns, 64 graded items, queries at 8, 16, 32
ticks pooled. **G** (gliders, triggered items, `gliders_trig_v1`) goes second, only if dialsA2 passes, with an 8-episode Lab,
180 minutes, about 1,140 full episodes (x86 1,143), b_pred 0.05, and only after the box change of section 3: in
today's box neither its generic nor its told-form recipe can be built. F goes first when both qualify, for SPEC §10's
reasons: no public trace of its hidden part, a hypothesis route that fits the box, decision 1's design (a). The rule,
applied to the verdicts as their summary scripts write them:

- **F qualifies** if FL's `results/analysis_stage2.json` (job r6-foundrylong-003) has T1 passing (one-sided 90% lower
  bound of sigma_G at 16 ticks, N = 32, at least 0.15), T2 not failing (lower bound not above 0.7), T3 and T6 holding,
  and neither T1 nor T3 marked incomplete. That is FL's "pass", or its "undecided" with only T4 and/or T5 missing
  (SPEC's INFER: then an inference exam, with no claim about designed experiments). FL's "fail", T1 undecided, and T1
  holding with T3 failing (SPEC's STATE) do not qualify.
- **G qualifies** if dialsA2 declares PASS (T1-T5 and the zero point, A2 `DECLARED.md` Part 1); UNDECIDED and FAIL
  do not (A2 R21 sends undecided to the lead).

| | G qualifies | G does not |
|---|---|---|
| **F qualifies** | F first; G second, after its box change | F only |
| **F does not** | G, after its box change and a yes to Q4 | none as a test of science; a compute-limited F (decision 1(c)) only if its scripted pilot gives sigma_box >= 0.15 and the lead chooses it; else the next world from the cards |

In every cell, model rollouts wait for the scripted pilot of section 5.

## 2. The candidates, slots filled

### F: foundry hidden weights

World, draw, library and items as SPEC §0-3 (all 250 weights hidden; 64 graded and 32 `sel` items).

| slot | x86, measured | Mac |
|---|---|---|
| `F_R64_BOX` | 121.9 member-ticks/s, full episodes at B = 16 (`F.derived.member_ticks_per_s_full_episode_batched`); SPEC used FL's 124 | 121.9 r |
| `F_R32_BOX` (the agent's float32 simulator) | 217.1 (`F.sim_float32_measured.16`) | 217 r |
| `F_T_JIT` | 8.2 s (`F.plug_in_item_m256.T_JIT_item_s`) | 8.2 / r |
| brute force, one item (256 x 48 member-ticks) | 117.9 s at the plug-in rate 104.2 (`F.plug_in_item_m256`) [D] | / r |
| `T_BOX`, `T_SETUP` | 2.7 s (vfport `RUNBOOK_MAC.md`); 600 s assumed (SPEC §6) | pilot |
| `F_T_DRAW_MAC`, instance build, null pool (once) | 533 s, 1,248 s, 1,462 s [D] (member-ticks of SPEC §1, 2, 7) | / r |

**Budgets told** (x86 values until the Mac's replace them): Lab of 32 episode-equivalents (`max_ticks` 2,080, reset
17, 100 nats per tick, 400 per episode, 12,800 in all); 180 min, B_res = 60 x 180 x R_box / 348 = 3,783 full float64
episodes ("thinking counts; background processes run between turns"); b_pred 0.25 of 117.9 s: `wall_seconds` 52.7,
`cpu_seconds` 75.4 per item (SPEC §4's formulas) [D]. The ring's 30 CPU-s would be 0.19 of brute force [T
`F.prediction_budget`].

**References in two tiers** (skill at 16 ticks, K = 0, O = 1; FL stage 1, `README.md`, `results/analysis_stage1.json`):

| row | tier | where, when | expected |
|---|---|---|---|
| K, O, null (ridge on the null pool) | both | Mac, before | 0, 1, weak |
| P0(1,000) | ceiling | Mac, before: FL's published `inputs/stage1/params_p0w1000.npz` | 0.421 |
| C(16,384) at the hidden weights | ceiling, top of every scale | GPU, after | 0.581, a lower bound (FL S4) |
| FT(32), Dr(32), D(32) | ceiling | GPU, after | 0.455, 0.352, 0.190 |
| W(32), W+(32), W(true) | ceiling | GPU, after | stage 2 pending; W(true) 0.78 on one world (FL CPU test) |
| P0_box (16 library worlds, 142 min [D]) | box | Mac, after, scripted rollout | below P0(64)'s 0.273 (inferred) |
| FT_box, Dr_box, D_box | box | Mac, after | Dr and D cost minutes: near their ceiling values |
| W_box (one start, at most 143 steps of job 003's shape, 101 min [D]) | box | Mac, after | measured by the pilot; FL CPU test: 0.37 in 60 steps from another world's weights, still improving |

Ceiling sigma(16, 32) = 0.218 (p10 0.187); 0.157 at 8 ticks, 0.297 at 32 (FL `analysis_stage1.json`
`sigma.h*_N32.all`). If the ridge is the best generic recipe a box reaches, sigma_box is about (0.581 - 0.352) / 0.581
= 0.39 [D] (inferred; FT_box may beat the ridge). P0(1,000) costs 64 h on 2 cores, 17 x B_res
(`F.recipes.pilot_recipes_cpu_hours`): the agent can buy the fit, not the generic recipe.

**Grading on the Mac:** 64 x (52.7 + 2.7) + 600 = 4,144 s with every item at its limit, 0.43 of the 9,600 s allowance
(vfport `tools/vfrun.py` `GRADING_ALLOWANCE_S`); it holds while r >= 0.31 [D].

### G: gliders, triggered items

As SPEC §0-3 (theta and the stress-conversion term at eta 4 hidden; aimed or regional programs; 64 + 32 items).

| slot | x86, measured |
|---|---|
| `G_CPU_S_PER_MEMBER_TICK_BOX` | 0.230 (8.68 member-ticks/s at B = 1, `G.derived.core_s_per_member_tick_best`); round 5's 0.15 was 1.5 x too low |
| `G_T_JIT` | 11.5 s (`G.derived.T_JIT_sim_item_s`), plus about 20 s to compile a 50-tick start |
| brute force, one item (256 x 32) | 944 s (`G.derived.plug_in_item_m256_s`) |
| instance build; null pool (once) | 4,800 s [D]; 4,837 s (`G.derived.null_pool_512_s`) |
| batch | B <= 64 in every box: B = 256 peaks at 4.61 GB, over the cap (`G.sim_measured.256.peak_rss_mb`) |
| `A2_NETS_PUBLIC` | probably yes: A2's request lists `nets.npz` among its public outputs; study A's is in git (`origin/gpu-jobs:jobs/r6-dialsa-003/out/nets.npz`) |

**Budgets told** (x86): Lab of 8 episode-equivalents (392 ticks, reset 17, 3,200 nats); 180 min, B_res = 1,143 [D];
b_pred 0.05 of 944 s: `wall_seconds` 73.7, `cpu_seconds` 117.4 [D]. The allowance caps b_pred at 0.118 at r = 1 [D].

**References in two tiers:** K, O and the null on the Mac before; P0 (A2's public-form net) and C (A2's true-form net
at (theta, eta / 4)), both published, on the Mac before; CFT, FT(8), D(8), S(8), RES(8), H(8) and H_mix(8) on the GPU
after, from A2's families. At the box tier only D_box and a few-point S_box can be built (FT_box and RES_box too if the
package carries the public-form net); no H_box: the three families take 48 h on 2 cores and a box holds 142 theta points
x 8 episodes against 768 [D, T `G.recipes.box.180`]. Expected values: A2 pending (base nets unconverged by its rule at
48,000 steps; the 192,000 rung training, A2 `PROGRESS.md`).

**Grading:** 64 x (73.7 + 2.7) + 600 = 5,489 s, 0.57 of the allowance; it holds while r >= 0.48 [D].

## 3. Is the box the right size?

The box: 2 CPUs, 4 GB including `/workspace` (in memory), 180 min of wall time including the model's thinking.

**F: the right size for the science route; the wall clock is the risk.** It fits one weight-fit start of job 003's
shape (143 steps of 42.5 s, 101 min, peak 2.2 GB, [T `F.fit_step_T32`]) or 3-4 starts of 200 steps at FL's smaller CPU
shape (39-49 min each, FL `summary.json` `exam_profile.W_fit_on_2_cores`); the Lab takes 87 s, FT and D minutes. The
generic recipe at pilot size does not fit (P0(210) 14.4 h, P0(1,000) 64 h; a box reaches P0 on about 16 worlds), so
the box weakens the generic route more than the science route (sigma_box about 0.39 against 0.22): the shape decision 2
asks for. But in `qwen_ring_002` the model's thinking took 1,705 of 2,313 s of the agent phase, 0.74
(`../rollouts/qwen_ring_002/RESULT.md`). At that share 180 min leave about 47 min of foreground compute, half a fit
start: an agent that does not run its fit in the background is held back by compute management, not science. Smallest
changes, cheapest first: (a) none beyond the told sentence, with the pilot running W_box once more with half the wall
idle and checking that it still clears the box G* (one scripted rollout, about 4.2 h of Mac); (b) count CPU time, not
wall time (Q1): new box code, no extra Mac hours; (c) `wall_minutes` 240: +1 h of Mac per rollout and +4 h per box
tier, and a change of the 180 maximum in vfport `tools/check_request.py`. CPUs and memory stay.

**G: the wrong size; today's box makes it a test of compute.** A box holds 1,143 full episodes (9.45 s each). The
told-form route needs three families (48 h on 2 cores) and base nets of 4.1 to 33 h each; the generic route needs the
public family (16.1 h) and a net (at least 4.1 h) [T]. An agent can build neither. Smallest change: (i) ship A2's
public family and public-form net in the package (costly, no science, like F's library; Q3), which makes P0 free and
FT and RES affordable; (ii) G's agent box at 8 CPUs (item boxes keep 2): B = 1 is the fastest batch, so throughput
should scale with processes (inferred), about 570 theta points x 8 episodes in 180 min, 0.74 of A2's family. Cost: a G
rollout takes 8 Mac cores, so G rollouts and box-tier scripts run one at a time (18.1 h of box tier per instance [D]),
and `profiles.py` changes. A smaller world voids A2's verdict; fewer items do not help. Box caps are the lead's decision.

## 4. Costs

**GPU, ceiling rows per instance** (A100 40GB, $1.99/h):
- **F: about $2.1** (0.92 h of work, 0.12 h of pod overhead; cap $3.66) [D `gpu.F_per_instance`]: C(16,384) x 2 seeds,
  FT(8, 32) with cross-validation, D, Dr, W(32) with 4 starts x 143 steps, W+(32). From FL job 001's stage clocks and
  GPU speed (`origin/gpu-jobs:jobs/r6-foundrylong-001/out/full/info.json`; 16-world lockstep times taken as upper
  bounds for one world), its overhead (billed $4.9154 / 1.99 minus 2.355 h of run, `status.json`) and job 003's 1.55 s
  per step of 8 fits (FL `PROGRESS.md`). The 32-candidate prescreen and W(true) are not in it.
- **G: about $1-1.5** (inferred): C is A2's published net; the rest are fine-tunes and inferences, priced by A2's
  request at 21.2 ms per lockstep fine-tune step and 1,300 member-ticks/s, plus the same overhead. A2's stage clocks
  replace this when its job ends.

**Mac hours** (x86-equivalent; divide the computed parts by r) [D `mac_x86_equivalent`]:

| | F | G |
|---|---|---|
| per profile, once: null pool | 0.41 h | 1.34 h |
| per instance, before: draw, build | 0.49 h | 1.33 h |
| per instance, before: null and P0 (and G's C) graded in boxes, each at most | 1.15 h | 1.52 h |
| **per rollout: 180-min agent phase and grading, every item at its limit** | **4.16 h** | **4.53 h** |
| per instance, after: box tier, 4 scripted rollouts one at a time | 16.6 h | 18.1 h |

Four F box-tier boxes at once take 4.2 h if the Mac has 8 free cores and 16 GB (not known).

**Model dollars per rollout:**
- **Qwen** (`qwen3.6-35b-a3b`, $0.11 in, $1.01 out, $0.099 cache read per million): `qwen_ring_002` used 143 of 150
  turns, 7.28 M billed input and 74 k output tokens, $0.805 (RESULT.md). At 150 turns: **$0.89** [D], assuming context
  grows linearly with the turn index as there, with the same cache share and tool outputs; it stopped at 143 turns with 21 min
  left, so turns, not wall time, limit Qwen. Crude bound (every prompt at the 200 k context): $4.54 [D]; `cap_usd` 3.
- **Astra** (`gpt-6-astra`, $10 in, $50 out, cache reads not listed): `astra_ring_001` used 14 of 22 turns and 20,917 of
  70,000 tokens, $2.48 listed, $1.02 by the provider's cost fields (RESULT.md). At the same caps with all 22 turns:
  **$5.63 listed** (about $2.3 at the provider ratio 0.41), bound $19.02 (`ledger.json`); 70,000 tokens in all (the ring used 20,917) is likely
  binding for reading F's package, writing a fit and checking it. At 150 turns with Qwen's context per turn
  (50,900 billed input tokens): **$82 listed, about $34** at that ratio [D], assuming the ratio holds.

## 5. Pin changes for the next port round, and the scripted pilot

From SPEC §11 (its numbering in brackets; line counts are SPEC's estimates, and the port's first estimate was a tenth
of its outcome, vfport `README.md` §2). **Now, independent of the verdicts:** 1. `profiles.py`, two entries with
`b_pred`, `tiers`, `pool_sha256` [1], 60 lines; 2. `exam_configs/foundry_v1.json`, `gliders_trig_v1.json` with the
item limits of section 2 [2], 40; 3. `tools/make_pool.py`, the kept null pool [5], 90; 4. `bundle.py`: pool, F's
library (G's family and net if Q3), `VENDOR_DROPPED`, budgets [3], 80; 5. `TASK.md.tmpl`: hidden sentence by kind,
compute-budget section [4], 90; 6. `tools/check_request.py`, the grading bound [11], and `tools/pack_rollout.py`, publish
a pilot's hidden instance [12], 70; 7. `tests/exam_pure.py` [13], 250. **After the verdicts, for the qualifying
profile:** 8. `physim2_env/hidden/` and `tools/make_instances.py`, the draw and G's hidden law [6], 250; 9.
`lab_tools.py` `VfLabService` from the hidden hook [7], 30; 10. the two public world modules [8], 340; 11.
`tools/prove.py` tiers [9], 80; 12. `agents/ref_foundry.py`, `ref_gliders_trig.py`, box-tier scripts [10], 650. About
2,000 lines, plus a GPU reference job outside the pin (about 400). Items 3 and 8 add host-side compute: a host-safety
re-audit. F alone drops G's parts of 8, 10, 12. Outside the pin: G's `box_cpus` if the lead takes section 3 (ii); any
wheel download with `--platform manylinux2014_aarch64` alone must also name `manylinux_2_27_aarch64` (`timing.json`
`image.first_try`); the image needs no change (`image.check`).

**Scripted pilot, before any model rollout** (SPEC §9 plus two checks), one public pilot instance on the cloud
container, then on the Mac as runbook step 2:
0. Measure r on the Mac (the three feasibility scripts) and recompute every told number.
1. Every scripted policy through the real boxes; every item graded, none failed (the layers of `RUNBOOK_MAC.md` step 2a).
2. Told numbers (R_box, T_JIT, B_res, item seconds) within 10% of measured.
3. W_box (F) or H_box (G) inside B_res with its predictor inside the item limits; **new:** again with half the wall
   idle, still above the box-tier G*.
4. A brute-force predictor killed at the limit and scored as null.
5. null < D_box, O above C, sigma_box >= 0.15 at the point estimate. **New:** SPEC's D_box <= P0_box may fail for F
   (P0 on 16 worlds can fall below D(32)); report it, do not gate on it.
6. Grading inside the allowance with margin; leak scans and the collision refusal of a planted public world;
   `lab_log.jsonl` equal to the Lab's record; F's sigma under both scales; one GPU job adds the ceiling rows.

## 6. Open questions for the lead

- **Q1.** Research budget: wall clock including thinking (now; Qwen waited out 0.74 of its agent phase), or CPU time only (new box code)?
- **Q2.** Which rho is the bar: the studies' generic share (L(P0) - L(G*)) / (L(P0) - L(C)) <= 0.7, or the roadmap's
  rho with S = the told-hypothesis script (W, H), which fails by construction whenever T3 passes (W* closing 0.7 of the
  G*-to-C gap forces rho >= 0.7)?
- **Q3.** May the package carry costly, science-free material: F's screened library (110 h of screening on 2 cores)
  and, for G, A2's public family and public-form net?
- **Q4.** If G is the one that qualifies: a pilot rollout while its defect's form is public here, with an 8-CPU agent box?

Unanswered, SPEC's defaults hold: the ridge null (its Q3), the cards if both fail (Q5), the box tier on the Mac (Q6).

## 7. Corrections made to spec/ and feasibility/

`spec/SPEC.md` (plain errors, noted in its header): G's cost is 0.23 CPU-s per member-tick (measured), not 0.15, so §2
G build 52 to 80 min, §4 B_res 1,756 to 1,143, A2's family 3.5 to 5.4 x B_res, brute force 614 to 944 s, the
prediction term 31 to 47 s, §6 G's T_JIT room 92 to 76 s, §7 G's pool 1.7 to 2.7 core-hours. §4 and §10: "a W fit
takes 39-49 min" was FL's smaller CPU shape (4 x 2 x 2 per step); job 003's shape (8 x 4 x 2) takes 101 min for one
143-step start; both are now stated. Unchanged: SPEC's vfport line numbers are those of 3991d8cd (at a5afef952,
`RUNBOOK_MAC.md` l. 643 and l. 970). `feasibility/`: checked against `timing.json` and `raw/`; no error found.
