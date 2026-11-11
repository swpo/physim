# Exam profile 2: design (synthesis for the coordinator and the lead)

11 Nov 2026, design only; revised after two critics (section 8). Joins `spec/SPEC.md` and `feasibility/`; program
files read at a5afef952, FL's addendum 5 at f55bfb8d7. Sources: [T] `feasibility/timing.json` (key named); [D]
`derived.json` from `derive.py`; FL = `../foundrylong`, A2 = `../dials/dialsA2`. **x86** = 2 pinned cores of the
shared cloud container (Xeon @ 2.10 GHz; a critic's rerun was 3-13% faster). **Mac**: not measured.
r = Mac box speed / x86 speed (Mac time = x86 time / r) for work in a box (`--cpus 2` is a quota there, not pinned
cores); r_host the same for work the runner does natively on macOS (draw, build, null pool, Lab, F's gate).
FEASIBILITY.md infers 1 to 2 for scalar work, possibly below 1 for float64 vector work. Neither can be measured yet:
the feasibility scripts hard-code cloud paths and the runbook forbids any `docker run` by hand (vfport
`RUNBOOK_MAC.md` l. 114); pin item 8 adds the way. Until then every told number is an x86 placeholder.

## 1. Purpose, recommendation, decision rule

The lead wants "tests that are not trivially easy" (`../../roadmap/DECISIONS.md`, Direction); ring is solved in
closed form (0.964, `../rollouts/README.md`). Profile 2 is to be the first world without a closed form whose sigma
passes 0.15 at the ceiling under decision 2's told budgets. It cannot pass the roadmap's rho as written: when the
told-hypothesis script closes 0.7 of the gap (T3 of both studies), roadmap rho with S = that script is at least 0.7.
A qualifying profile is accepted on the studies' rho_G only if the lead answers Q2 so, before a profile is chosen.

**Recommendation.** F (foundry hidden weights, `foundry_v1`) first if foundrylong's stage 2 qualifies it: a Lab of 32
episode-equivalents (2,080 ticks, reset 17, 12,800 nats), 180 min, a research budget of about 3,800 full episodes
(x86 3,783 [D `F.B_res_full_episodes_x86`]), a prediction budget of 0.25 of a float64 brute force (52.7 s wall, 75
CPU-s per item on x86 [D `F.item_b0.25_x86`]), 150 turns, 64 graded items, queries at 8, 16, 32 ticks pooled. G
(gliders, triggered items) second, only if dialsA2 passes and after section 3's box change: an 8-episode Lab, 180 min,
about 1,140 full episodes, b_pred 0.05 (with a per-profile grading allowance; 0.025 without). F first when both
qualify, for SPEC §10's reasons.

**F is now unlikely to qualify.** FL addendum 5 (`DEVIATIONS.md`, 23:15) records job 003's log, pooled skill at 16
ticks, not the analysis: C 0.592, P0 0.433, W on the mix Lab 0.401, W(true) 0.524. T3 needs W* >= G* + 0.7 (C - G*),
0.544 with G* = P0. W(true), the pipeline's ceiling, is below that, and W+ cannot reach 0.7 by its recipe (addendum
5, point 1). If the analysis agrees, F is FL's "T1 passes, T3 fails": with W(true) below C the hidden state limits,
not the law (FL `DECLARED.md` §3). Plan for the table's lower row.

**The rule**, on the verdicts as the studies' scripts write them (FL `make_final.py`, `results/analysis_stage2.json`;
A2 `make_summary.py`):

- **F qualifies** if stage 2 is readable (not "incomplete", addendum 5 point 2), T1 passes (one-sided 90% lower bound
  of sigma_G at 16 ticks, N = 32, at least 0.15), T2 does not fail ("not read", only when P0 is within 2 SE of C,
  counts as not failing), and T3, T5 and T6 hold: FL's "pass", or "undecided" with only T4 missing (INFER: an
  inference exam, no claim about designed experiments). T5 ("actions matter", roadmap §1 check 3) is required: stage
  1 gave S5 0.115 (p05 0.077), the input-blind oracle 0.907 (`analysis_stage1.json` `S5.16.program`,
  `skill.plugU0.16`). F qualifies "at this compute" (FL S3); its told research budget is part of the exam.
- **G qualifies** if dialsA2 declares PASS (A2 `DECLARED.md` Part 1) with base nets converged by its rule R9; with
  nets "not converged by the rule", only "at this compute". UNDECIDED and FAIL do not.
- **A missing, cut or incomplete verdict** chooses nothing from that study; the lead decides.

| | G qualifies | G does not |
|---|---|---|
| **F qualifies** | F first; G second, after its box change | F only |
| **F does not** | G, after its box change and a yes to Q4 | no profile-2 rollout as a test of science; a compute-limited F only if its scripted pilot gives sigma_box >= 0.15 and the lead chooses it; else the next world from the cards |

Model rollouts wait for section 5's pilot. Scores are per instance; ordering models needs two or more instances
(roadmap §1 item 5).

## 2. The candidates, slots filled

### F: foundry hidden weights (SPEC §0-3; all 250 weights hidden; 64 graded, 32 `sel` items)

| slot | x86, measured | Mac |
|---|---|---|
| `F_R64_BOX` | 121.9 member-ticks/s (`F.derived.member_ticks_per_s_full_episode_batched`); one process uses 1.73 cores | 121.9 r |
| `F_R32_BOX` | 217.1 float32 (`F.sim_float32_measured.16`) | 217 r |
| `F_T_JIT` | 8.2 s (`F.plug_in_item_m256.T_JIT_item_s`) | 8.2 / r |
| brute force, one item (256 x 48 member-ticks) | 117.9 s float64 at the plug-in rate 104.2; 56.6-66.2 s float32 [D] | / r |
| `T_BOX`, `T_SETUP` | 2.7 s (vfport `RUNBOOK_MAC.md`); 600 s assumed | pilot |
| draw, build, null pool | 533 s, 1,248 s, 1,462 s [D] | / r_host |

**Told:** Lab of 32 episode-equivalents (`max_ticks` 2,080, reset 17, 100 nats per tick, 400 per episode, 12,800 in
all); 180 min, B_res = 60 x 180 x R_box / 348 = 3,783 full float64 episodes; b_pred 0.25 of a float64 brute force:
`wall_seconds` 52.7, `cpu_seconds` 75.4 per process (RLIMIT_CPU is per process; 2 x wall bounds the box) [D]. In
float32 the same seconds buy 0.45-0.52 of a brute force (0.67-0.79 with the 15 s slack) [D]: told "in float64".
Also told: the 4 GiB includes `/workspace` and `/tmp`; peaks of the simulator's run, its gradient and a net step are
0.56, 2.2 and 1.6 GB [T]; two large ones at once exceed the cap.

**References** (skill at 16 ticks, K = 0, O = 1; FL `analysis_stage1.json`; "log" = job 003 per addendum 5):

| row | tier | where, when | expected |
|---|---|---|---|
| K, O, null (ridge on the null pool) | both | Mac, before | 0, 1, weak |
| P0(1,000) | ceiling | Mac, before (FL's published params) | 0.421 (log 0.433) |
| C(16,384) at the hidden weights | ceiling; the scale's top by definition, not the best possible (FL S4) | GPU, after | 0.581 (log 0.592) |
| FT(32), Dr(32), D(32) | ceiling | GPU, after | 0.455, 0.352, 0.190 |
| W(32), W+(32), W(true) | ceiling | GPU, after | log: 0.401, capped, 0.524 |
| W_lib(32): W at 0 steps from the library world with the lowest Lab loss | both | GPU, Mac, after | new: if it takes most of W's gain, the exam is a library lookup |
| P0_box (section 5's sweep), FT_box, Dr_box, D_box | box | Mac, after, scripted | below P0(64)'s 0.273 (inferred); FT, Dr, D near ceiling |
| W_box (one start, at most 143 steps of job 003's shape, 101 min [D]) | box | Mac, after | pilot |

Every Lab-using row runs its own reference Lab on the instance (mix programs, the told budget), the same for every
rollout there, never the agent's `lab_log.jsonl`. The agent's place a_t is reported against C, W* and W(true).
Ceiling sigma(16, 32) = 0.218 (p10 0.187); 0.157 at 8 ticks, 0.297 at 32 (`sigma.h*_N32.all`). Per world at 16 ticks
it runs from 0.126 to 0.478, 6 of 16 below 0.15 (8 of 16 at 8 ticks; `per_world`): hence section 5's instance gate.
If the ridge is the best generic recipe a box reaches, sigma_box is about 0.39 [D] (inferred; a better P0_box or
FT_box may beat it). P0(1,000) costs 64 h on 2 cores, 17 x B_res (`F.recipes.pilot_recipes_cpu_hours`).

**Grading:** 67 calls (three example calls precede the 64 items, vfport `TASK.md.tmpl` l. 135) x (52.7 + 2.7) + 600
= 4,311 s at every limit, 0.45 of the 9,600 s allowance (`tools/vfrun.py` `GRADING_ALLOWANCE_S`), holding while
r >= 0.32 [D]. Verifiers' own limits (setup 900 + finalize 900 + scoring (n + 3) x (wall + 40) + 600, vfport
`taskset.py` l. 740-741) sum to 8,610 s at r = 1, inside 9,600 only while r >= 0.72 [D]: pin item 6.

### G: gliders, triggered items (SPEC §0-3; theta and the term at eta 4 hidden)

| slot | x86, measured |
|---|---|
| `G_CPU_S_PER_MEMBER_TICK_BOX` | 0.230 (8.68 member-ticks/s at B = 1, `G.derived.core_s_per_member_tick_best`) |
| `G_T_JIT` | 29.1 s: 11.5 s imports and run compile (`G.derived.T_JIT_sim_item_s`) + 17.6 s start compile, needed without state-assimilation code (`G.sim_measured.1.compile_s_start50`) |
| brute force, one item (256 x 32) | 944 s (`G.derived.plug_in_item_m256_s`) |
| build; null pool | 4,800 s [D]; 4,837 s (`G.derived.null_pool_512_s`) |
| batch | B <= 64: B = 256 peaks at 4.61 GB (`G.sim_measured.256.peak_rss_mb`) |
| `A2_NETS_PUBLIC` | probably (A2's request lists `nets.npz` as public) |

**Told** (x86): Lab of 8 episode-equivalents (392 ticks, reset 17, 3,200 nats); B_res = 1,143 [D]; b_pred 0.05 of 944
s: `wall_seconds` 91.3, `cpu_seconds` 152.6 [D]. A2's "there may be none" is untrue with eta always 4; told instead:
"the simulator lacks a mechanism of the world; which, where and how strong is not said" (no script reads it).

**References:** K, O, null, P0 (A2's public-form net) and C (its true-form net) on the Mac before; CFT, FT, D, S, RES,
H, H_mix (N = 8) on the GPU after, each with its own reference Lab. The box tier has D_box and a few-point S_box; no
H_box, so box-tier rho cannot be read (a box holds 142 theta points x 8 episodes against 768 [T
`G.recipes.box.180`]). A2's base nets were unconverged at 48,000 steps (A2 `PROGRESS.md`): an undertrained G*
inflates sigma_G.

**Grading:** 67 x (91.3 + 2.7) + 600 = 6,897 s (r >= 0.65) [D]; verifiers' limits sum to 11,196 s at r = 1, over
9,600: G needs pin item 6, or b_pred <= 0.025 [D].

## 3. Is the box the right size?

The box: 2 CPUs, 4 GB including `/workspace` and `/tmp`, 180 min of wall time including the model's turns.

**F: right for the science route; turns and blocking set the compute.** Model time is per turn: 11.9 s in
`qwen_ring_002` (1,705 s over 143 turns), at most 25.6 s in `astra_ring_001` (359 s over 14 turns, commands included).
At 150 turns about 150 min (Qwen) or 116 min (Astra's bound) of the 180 remain [D]. That fits one fit start of job
003's shape (143 steps of 42.5 s, 101 min, 2.2 GB [T `F.fit_step_T32`]) or 3-4 starts of FL's smaller CPU shape (39-49
min, FL `summary.json` `exam_profile.W_fit_on_2_cores`); the Lab takes 87 s, FT and D minutes. Memory admits one large
job at a time (a fit and a net training reach 3.8 GB before `/workspace` and `/tmp`). P0 at pilot size does not fit
(P0(1,000) 64 h), so the box weakens the generic route more than the science route (sigma_box about 0.39 against
0.22), as decision 2 intends. Open: how long one command may block; a longer fit runs in the background and is polled
with turns (pilot step 3 measures it). If compute management rather than science limits: (a) the told sentences alone,
with pilot step 3 run again with 64 min idle; (b) count the agent box's CPU-seconds, read by the host from the engine
(the in-box counter is not trusted there, vfport `grading.py` l. 247) (Q1); (c) `wall_minutes` 240: +1 h of Mac per
rollout, +4 h per box tier, the 180 maximum of `check_request.py` raised. Each score carries the rollout's model-wait
seconds and CPU-seconds (pin item 9).

**G: the wrong size; today's box makes it a test of compute.** The told-form route needs three families (48 h on 2
cores) and base nets of 4.1 to 33 h each; the generic route the public family (16.1 h) and a net (4.1 h or more) [T].
Smallest change: (i) ship A2's public family and public-form net (costly, no science; Q3), making P0 free and FT and
RES affordable; (ii) G's agent box at 8 CPUs (item boxes keep 2): B = 1 is fastest, so throughput should scale with
processes (inferred), about 570 theta points x 8 episodes in 180 min, 0.74 of A2's family; (iii) pin item 6. G
rollouts and box-tier scripts then run one at a time (19.7 h of box tier per instance [D]). A smaller world voids A2's
verdict. Box caps are the lead's decision; G scores before the change are pilot only.

## 4. Costs

**GPU, ceiling rows per instance** (A100 40GB, $1.99/h). **F: about $2.1** (0.92 h of work, 0.12 h of overhead; cap
$3.66) [D `gpu.F_per_instance`]: C(16,384) x 2 seeds, FT(8, 32), D, Dr, W(32) 4 starts x 143 steps, W+(32), from FL
job 001's stage clocks and overhead (`origin/gpu-jobs:jobs/r6-foundrylong-001/out/full/info.json`, `status.json`) and
job 003's 1.55 s per step (FL `PROGRESS.md`); prescreen, W(true), W_lib not in it. **G: about $1-1.5**, inferred
from A2's request prices; no stage clocks behind it yet.

**Mac hours** (x86-equivalent; box work / r, host work / r_host) [D `mac_x86_equivalent`]:

| | F | G |
|---|---|---|
| per profile, once: null pool | 0.41 h | 1.34 h |
| per instance, before: draw and build; F's gate per draw | 0.49 h; 0.29 h | 1.33 h |
| per instance, before: null and P0 (and G's C) graded, each at most | 1.20 h | 1.92 h |
| **per model rollout: 180-min agent phase and grading at every limit** | **4.21 h** | **4.93 h** |
| per instance, after: box tier, 4 scripted rollouts one at a time | 16.8 h | 19.7 h |
| **per instance with one model rollout** | **23.9 h** (70% box tier) | **29.8 h** |

The P0_box sweep runs once per profile on the cloud container: no Mac hours.

**Model dollars per rollout.** Qwen (`qwen3.6-35b-a3b`, $0.11 in, $1.01 out per million): `qwen_ring_002`, 143
turns, $0.805; at 150 turns **$0.89** [D], context growing linearly with turns as there; crude bound $4.54 [D].
Astra (`gpt-6-astra`, $10 in, $50 out): `astra_ring_001`, 14 of 22 turns, $2.48 listed, $1.02 by the provider; at
the ring's caps **$5.63 listed** (its 70,000 tokens likely bind for F); 150 turns with Qwen's context growth **$85.9
listed, about $35** at the provider ratio 0.41 [D].

## 5. Pin changes and the scripted pilot

SPEC §11 lists them (its numbers in brackets; about 2,300 lines plus a GPU job of about 400; the port's first
estimate was a tenth of its outcome, vfport `README.md` §2). **Now:** 1-5 profiles, configs, null pool, bundle, task
statement (float64 wording, memory peaks); 6 [11, 12] the grading allowance per profile = verifiers' setup + finalize
+ scoring limits, publishing a pilot's instance; 7 tests; 8 [14] **new** `agents/time_box.py`, a scripted policy
(physim2-script harness, like `agents/probe_caps.py`) running feasibility's timing modes with relative paths in the
agent's box and an item box, plus `make_instances.py` logging its own clock (r_host); 9 [15] **new** model-wait
seconds and engine CPU-seconds in the run report. **After the verdicts:** 10 [6] the hidden draw, F's gate, G's law;
11 the Lab's hidden hook; 12 world modules; 13 `prove.py` tiers; 14 [10] box-tier scripts with W_lib. Items 3, 8 and
10 need a host-safety re-audit.

**Declared before the pilot.** (i) P0_box's allocation: a sweep of library worlds (16, 64, 256, 1,000), episodes per
world and steps inside B_res, once per profile on held-out library worlds on the cloud container; the best on `sel`
is P0_box, FT_box starts from it (FL S3: s0(16) 0.531, 0.390, 0.276 at 64, 210, 1,000 worlds, `S3.16.s0`). (ii) F's
instance gate, part of the told draw: per draw, on the Mac host before any rollout, g = (L(Dr) - L(W(true))) / (L(K) -
L(W(true))) on the 32 `sel` items with a reference Lab of 32 episodes and 64 members (about 17 min x86 [D
`F.gate_per_draw_s_x86`]); threshold from stage 2's per-world K, Dr and W(true); redraws counted and published. (iii)
The instance's sha256 committed in git before the first rollout; every model on the same instances; published after
the last, then on the collision list, never reused.

**Scripted pilot, before any model rollout:** one public pilot instance, cloud container first, then the Mac as
runbook step 2.
0. r and r_host from pin item 8; every told number recomputed from the in-box measurement.
1. Every scripted policy through the real boxes; every item graded, none failed (`RUNBOOK_MAC.md` step 2a).
2. Told numbers within 20% of a second in-box measurement (10% fails on noise alone).
3. W_box (F) or H_box (G) inside B_res, its predictor inside the item limits; again with 64 min idle, still above the
   box-tier G*; the longest a command may block, measured.
4. A float32 brute force killed at the limit and scored as null (x86: 64.8-74.4 s against 52.7 s [D]).
5. null < D_box, O above C, sigma_box >= 0.15 at the point estimate on the exam's scales (library mean SD; FL's
   hidden-SD scale beside it). D_box <= P0_box reported, not gated, for F.
6. Grading inside the allowance with margin; leak scans; collision refusal of a planted public world;
   `lab_log.jsonl` equal to the Lab's record; one GPU job adds the ceiling rows.

## 6. Open questions for the lead

- **Q1.** Research budget: wall clock including model turns (now; about 30 min of Qwen's at 150 turns, at most 64 of
  Astra's), or the agent box's CPU-seconds read from the engine (new code)?
- **Q2.** Which rho is the bar: the studies' (L(P0) - L(G*)) / (L(P0) - L(C)) <= 0.7, or the roadmap's with S = the
  told-hypothesis script (W, H), which fails by construction whenever T3 passes? Needed before a profile is chosen.
- **Q3.** May the package carry costly, science-free material: F's screened library (110 h of screening on 2 cores)
  and, for G, A2's public family and public-form net?
- **Q4.** If G qualifies: a pilot rollout while its defect's form is public here, with an 8-CPU agent box, scores
  labelled pilot only?

Unanswered, SPEC's defaults hold: the ridge null (its Q3), the cards if both fail (Q5), box tier on the Mac (Q6).

## 7. Corrections made to spec/ and feasibility/

First pass: G's cost 0.23 CPU-s per member-tick, not 0.15; job 003's fit shape takes 101 min per start, not 39-49.
Second pass: every "fixed" item of section 8, in SPEC (header, §1, §4-§6, §9-§12), FEASIBILITY.md ("Not measured")
and `derive.py`.

## 8. Critics' items

Compute and cost:
- C1-C3, speeds and F's item: sound, cautious; no change.
- C4, r cannot be measured as planned: fixed (header, pin item 8, pilot step 0, FEASIBILITY.md).
- C5, "47 min of foreground compute": fixed, per-turn arithmetic (section 3, Q1); idle 64 min; blocking measured.
- C6, three example calls omitted; G's verifiers limits over 9,600 s: fixed (67 calls, pin item 6, G's b_pred).
- C7, G's T_JIT without the start compile: fixed, 29.1 s.
- C8, fit plus net training over 4 GiB: fixed (told peaks; one large job at a time).
- C9, 10% check fails on noise: fixed, 20% against an in-box remeasurement.
- C10, ratio defined two ways: fixed (r and r_host; FEASIBILITY's own words).
- C11, no Mac total: fixed, 23.9 h (F), 29.8 h (G).
- C12, GPU dollars: F sound; G marked as having no stage clocks.
- C13, Astra's line grew context linearly: fixed, $85.9 listed.
- C14, image: sound.

Exam validity:
- V1, one instance, no redraw rule: fixed (gate; same instances for every model; ordering needs two or more).
- V2, roadmap rho fails by construction: stated in section 1; open as Q2.
- V3, INFER admits T5 missing: fixed (T5 required, T2 "not read" defined, SPEC §10 aligned).
- V4, wall clock includes thinking: open (Q1); its 0.74 premise was wrong (C5); model-wait and CPU-seconds reported
  with each score.
- V5, P0_box one allocation: fixed, a sweep once per profile (per instance it would add 16.8 Mac-hours).
- V6, C is not the top: fixed (wording; a_t also against W* and W(true)).
- V7, library lookup: fixed, W_lib in both tiers.
- V8, the told fraction is float64's: fixed (wording; float32 brute force in pilot step 4, killed with 12-22 s to spare
  on x86).
- V9, G's public form, untrue sentence, no H_box, unconverged nets: fixed (sentence, convergence rule, pilot-only
  label); Q4 open.
- V10, fresh draw: fixed (sha256 committed before, published after, never reused).
- V11, ceiling rows' Lab: fixed, own reference Labs.
- V12, grading scales: fixed, sigma_box gated on the exam's scales; T1 under them needs job 003's samples.
- V13, cut or incomplete study: fixed (the lead decides; "at this compute" in F's rule).
