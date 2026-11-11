# Exam profile 2: specification of F (foundry hidden weights) and G (gliders, triggered items)

Design only (11 Nov 2026); both deciding jobs run (r6-foundrylong-003, r6-dialsa2-001). `{{NAME}}`: a measurement
for `../feasibility`. "x86" = 2 pinned cores of the cloud container (lower bounds). Mac time = x86 time / r, with
r = Mac box speed / x86 speed (`{{MAC_RATIO}}`, in a box under the `--cpus 2` quota) and r_host the same for the
runner's native macOS work (draw, build, null pool, Lab); both inferred until `../DESIGN.md` pin item 8 measures them. FL = `../../foundrylong`, A2 = `../../dials/dialsA2`, VF = `../../vfport`, AE = `../../../round5/agentenv`.
Corrected after the measurements (listed in `../DESIGN.md` section 7): G's cost per member-tick (0.23 CPU-s, not 0.15) and
what follows from it in sections 2, 4, 6, 7; the shape of the W fit behind "39-49 min" in sections 4 and 10. Second
pass, from the critics (`../DESIGN.md` section 8): sections 1, 4, 5, 6, 9, 10, 11, 12.

## 0. The port's objects

| object | F (`foundry`, config `foundry_v1`) | G (`gliders_trig`, config `gliders_trig_v1`) |
|---|---|---|
| image | `physim2-ring:2` reused: its jax 0.12.0.1, numpy, scipy (VF `docker/ring-requirements.txt`) are all tnca, `fl_w`, `a2_lib` import | same |
| box | the ring's caps; `wall_minutes` 180 (request maximum, VF `RUNBOOK_MAC.md` l. 949), `max_turns` 150 | same |
| public world module | `world_foundry.py`: tnca, block view (192 numbers), burn-in 300, P = 16, program mix, nats, screened-prior code, `Simulator` | round 5's `world_gliders.py`, mix restricted to aimed and regional |
| hidden hook (host only) | the instance draw (section 1) | the draw; the hidden law (`dlaw` via `xlaw`, eta = 4) for Lab, items, O, K |
| grading | the ring's: a box per item, failed item = null, fair energy score, K = 0, O = 1 | same |

Scales (F): FL used the hidden world's climatological SD per channel; the port takes public `W.scales()` (AE
`evaluator/instance.py` l. 110; E11: grading unchanged), so F uses the library's mean SD; the pilot reports both.

## 1. Public, hidden, told

**F.** Public: `round5/foundry/tnca.py` (law, noise, wind channel, initial distribution); the screened prior as code
(`draw_theta`, round 5's weights-only pre-screen and threshold, the screen of `job2.py`, FL's exam-time gate; FL
`DECLARED.md` §2); a library of screened worlds: FL stage 1's 1,000 P0 training worlds (2 MB), minus every world ever
hidden (foundryexam arms P, N30, N10, centres 3078, 1672, 7567; the cards' worlds). It samples the prior; screening
15,040 draws took 110 h on 2 x86 cores (FL `results/summary.json` `exam_profile.reference_rows_hours_on_2_cores_float64`),
unpayable in a box and not science. Hidden: the 250 numbers, the noise secret, the futures. Told: all 250 are hidden,
drawn by the public procedure; section 4.

**G.** Public: round 5's gliders law and viability prior. Hidden: theta (4 numbers); presence, form and rate of the
missing term (XW of `defect_gliders/dlaw.py`, threshold 0.12, ramp 0.05, eta = 4 as in A2's criteria). Told: "the simulator lacks a mechanism of the world; which, where and how strong is not said" (A2's "there may
be none" is untrue when eta is always 4; no scripted policy reads the sentence).

**The draw**, at the runner's `instance` stage on the Mac (VF `tools/vfrun.py` l. 665-680), after pin and image are
fixed, so the image cannot hold it. Entropy: `Secret()` (`os.urandom(32)`, AE `instance.py` l. 69); draws use its
`SeedSequence` children, never `draw_theta(seed, index)` with an integer seed, so no public stream (F seeds 2026-2028,
+7919; G [6601, 4], round 5's) is re-entered. A check keeps pilot worlds out: F refuses a draw equal to a published
world (hash of 16 weights) or correlated with one above 0.9 (a 30% neighbour is 0.954, `tnca.perturb_theta`); G
refuses theta within 0.05 box widths of a published truth in every coordinate. A refusal replaces the secret itself
(new `os.urandom`) and is counted. F's `max_tries` rises from 64 (AE l. 63) to 400: about 1 screened draw in 18 is accepted (818 of 15,040; FL
`README.md`), so 64 fail with probability 0.03. One F draw: about 65,000 member-ticks, 8.7 min at
124 member-ticks/s (x86 float64); `{{F_T_DRAW_MAC}}`. F's gate, part of the told draw: g = (L(Dr) − L(W(true))) /
(L(K) − L(W(true))) on the 32 `sel` items (reference Lab of 32 episodes, 64 members, about 17 min x86) at least a
threshold declared from FL stage 2's per-world values; a draw below it is redrawn, the count published. The
instance's sha256 is committed in git before the first rollout; all models run on the same instances; it is
published after the last and then joins the collision list.

## 2. Items

| | F | G |
|---|---|---|
| graded / `sel` (reference picks only) | 64 / 32 | 64 / 32 |
| history | 17 frames after burn-in 300, no input | 16 input-free ticks + anchor |
| program | FL's mix: none, blind 200, aimed 200, regional 400 nats, equal shares, commands in the first 4 test ticks | aimed 200 or regional 300 nats, equal shares, from the anchor |
| trigger | none | every item; queries count from the program's start |
| queries (level 1) | 8, 16, 32 ticks | 8, 12, 16 ticks |
| R, climatology runs, samples | 12, 256, 256 (ruling E12) | 12, 256, 256 |
| build (AE: n(B+P) + nRH + n_clim(B+H)) | 152,192 member-ticks, 20.5 min x86 | 41,664 member-ticks, 80 min on 2 x86 cores at the measured 8.68 member-ticks/s |

All horizons are pooled: FL's sigma with 32 episodes is 0.157, 0.218, 0.297 at 8, 16, 32 ticks
(`results/analysis_stage1.json` `sigma.h*_N32.all.value`).

## 3. The Lab

| | F | G |
|---|---|---|
| episode-equivalents N | 32 (FL criteria) | 8 (A2's primary N) |
| `max_ticks`, `reset_cost` | 2,080 = 32 × (17 + 48), 17 (E13: one item history) | 392 = 8 × (17 + 32), 17 |
| nats | 100 per tick, 400 per episode (FL); total 12,800 | 100, 400 (round 5); total 3,200 |
| reply | block view, float32, quantised | block view, `QUANTUM` 1e-3 |

The client appends every reply to `/workspace/lab_log.jsonl` (VF `README.md` §8.13;
F: a few MB); grading boxes never see it, so the predictor carries what it needs in `submission/` (64 MiB).

## 4. The agent's compute (decision 2)

Unit: one full level-0 episode for one member, T_ep = 348 ticks (F; FL `exam_profile.seconds_per_full_episode_348_ticks`)
or 82 (G; AE `results/cost.json`). R_box = member-ticks per second of the 2-CPU box.

**Research budget**, told: B_res = 60 × wall_minutes × R_box / T_ep. F, x86 float64: 60 × 180 × 124 / 348 = 3,850
(float32 about 7,300). G: 60 × 180 × 8.68 / 82 = 1,143 (measured 0.23 CPU-s per member-tick, not round 5's 0.15). Mac: `{{F_R64_BOX}}`, `{{F_R32_BOX}}`,
`{{G_CPU_S_PER_MEMBER_TICK_BOX}}`. P0(1,000) simulates 64,000 prior episodes (17 × F's B_res); a W fit takes 39-49
min for 200 steps at FL's CPU shape (4 episodes × 2 members × 2 anchors per step; FL `exam_profile`), 101 min for
one start of job 003's shape (8 × 4 × 2, 143 steps, 42.5 s per step, `../feasibility`); A2's P0 family (6,144 episodes) is 5.4 × G's B_res. Enforced by the 2 CPUs and the wall time (vfrun stops at 60 × wall_minutes + 9,600 s,
`tools/vfrun.py` l. 778). Told: thinking counts; background processes run between turns.

**Prediction budget**, per item: U_item = 256 × (P + H_max) member-ticks (burn-in excluded: states can be carried),
12,288 (F) and 8,192 (G); brute force takes U_item / R_box: 99 s (F, x86 float64), 944 s (G, measured).
With b_pred = 0.25 (F) and 0.05 (G): `wall_seconds = b_pred × U_item / R_box + {{T_JIT}} + 15`, `cpu_seconds =
2 × (b_pred × U_item / R_box + {{T_JIT}})`; `{{F_T_JIT}}`, `{{G_T_JIT}}` = import and compile in a fresh item box.
x86: 25 s (F) and 47 s (G; round 5 gave 60 CPU-s, AE `configs/exam_gliders.json`). RLIMIT_CPU is per process (VF
`public/_item.py` l. 563): the 2-CPU box times `wall_seconds` bounds the total. Told: "{cpu} CPU-seconds and {wall} s
per item, {b_pred} of simulating 256 members over the item in float64" (in float32 the same seconds buy about 0.5 of
it, `../DESIGN.md` section 2); the memory cap includes `/workspace` and `/tmp`, with the measured peaks of the
simulator's run, its gradient and a net step. DESIGN fills these at the plug-in rate (F brute force 117.9 s) and
with G's T_JIT including the start compile (29.1 s).

## 5. References in two tiers

| row | F | G |
|---|---|---|
| K, O, null | Mac, before the rollout | Mac, before |
| PM | none (zero weights: a dead world); W(prior), another library world's weights, instead (FL: -0.75 at 16 ticks) | Mac, before |
| P0 | Mac, before: FL stage 1's public, instance-free P0(1,000) seed 0, a prebuilt submission | Mac, before: A2's public-form net |
| C | GPU, after: C(16,384) at the hidden weights (the scale's top by definition; FL S4: not converged) | Mac, before: A2's true-form net at (theta, eta/4), if public (`{{A2_NETS_PUBLIC}}`); CFT: GPU, after |
| FT, D, Dr / RES, S (ceiling) | GPU, after (N = 32 and 8) | GPU, after (N = 8) |
| S*, the scripted hypothesis | W(32), W+(32), W(true): GPU, after; W_lib(32), W at 0 steps from the library world with the lowest Lab loss: both tiers | H(8), H_mix(8): GPU, after |
| box tier: P0, FT, D, S* | Mac, after: scripted rollouts (`physim2-script`, $0) in the real box with the agent's limits | same |

One GPU job per instance (outside the pin) reads the instance published after the rollout, reusing FL's and A2's
code (`{{F_GPU_REF_USD}}`, `{{G_GPU_REF_USD}}`; C(16,384) is 0.038 A100-hours, FL). Every Lab-using row runs its
own reference Lab on the instance, never the agent's log. P0_box's allocation (library worlds, episodes per world,
steps within B_res) is picked once per profile by a declared sweep on held-out library worlds; FT_box starts from it. Mac: at most 4 × (180 min + grading), 16 h (`{{BOX_TIER_HOURS}}`).

Reading, per tier t, with C always the GPU C: sigma_t = (L(G*_t) − L(C)) / (L(K) − L(C)), G*_t the best generic
recipe picked on `sel` (F: P0, FT, D, Dr; G: P0, D, S, FT, RES); rho_t = (L(P0_t) − L(S*_t)) / (L(P0_t) − L(C))
(roadmap §1) and the studies' generic share beside it; the agent's place a_t = (L(G*_t) − L(agent)) / (L(G*_t) −
L(C)), also against W* and W(true). Bars are verdicts only in the 16-world studies; F's gate (section 1) screens the
instance (FL per-world sigma at 16 ticks: 0.126 to 0.478); an ordering of models needs two or more instances.

## 6. Grading on the Mac

(n_items + 3) × (wall_seconds + `{{T_BOX}}`) + `{{T_SETUP}}` <= 9,600 s (`GRADING_ALLOWANCE_S`, VF `tools/vfrun.py`
l. 469; three example calls precede the items, VF `TASK.md.tmpl` l. 135). Verifiers' own limits, 900 + 900 +
(n_items + 3) × (wall_seconds + 40) + 600 (VF `taskset.py` l. 740-741), must also fit: G's do not at b_pred 0.05
(11,196 s), F's only while r >= 0.72; hence an allowance per profile (section 11, row 11). `T_BOX` is 2.7 s on x86 (VF `RUNBOOK_MAC.md` l. 622). With 64 items and `T_SETUP` = 600 s (first pass, 64 calls), T_JIT may reach
about 98 s (F) or 76 s (G); a rollout's 64 items take 0.8 to 1.7 h. The bound holds for every row graded in boxes
(`{{GATE_REF_HOURS}}`).

## 7. The null pool

Built once per profile and kept (VF `profiles.py` `BASELINE_WORLDS`); it depends on no instance. F: 8 episodes on each of 64 library worlds, 178,176 member-ticks, 24 min x86 float64, about 19 MB
float32. G: 512 public-law episodes at prior draws, 4,837 s on 2 x86 cores, 2.7 core-hours (`../feasibility`; `profiles.py` says 1.7). A new tool builds it on the Mac
once; `bundle.null_pool` checks its sha256. The baseline is the ring's ridge on the pool: weak, honest (Q3).

## 8. Gaming and leaks, closed by design

1. Closed form: none for F (neural automaton, hidden fine state; even the true weights reach only 0.78 at 16 ticks,
   FL `README.md`) or G (nonlinear bodies, events). Dr, the closed-form ridge, is a row.
2. Jointly chosen samples: 256 bound the gain near 1/(m − 1) = 0.4% of the score (E12); the pilot measures it on O.
3. Reset tricks: a reset costs one item history (E13).
4. Image: built before the instance. Bundle: no `dlaw.py`, `xlaw.py` or the term's constants (G), no published
   hidden world (F); tests scan.
5. Lab replies: block view, quantised; no theta, fine state, seed or scale; neutral errors (round 5's `LabService`).
6. Zero-science predictors (PM, W(prior), P0) are rows; idling earns the weak null.
7. Looking up public worlds: section 1's check; the library excludes every world ever hidden.
8. G's form is public (`dlaw.py`, `DECISIONS.md`, `dialsA/README.md`): a model trained on this repository may know
   it. Acceptable for a pilot, transcripts read for it; a quotable type-(b) exam needs an unpublished form.
9. Brute force at grading: b_pred < 1 and the wall bound kill it; the item is scored as null.
10. The first rollouts' faults (`rollouts/README.md`) stay closed. New: compilation in every fresh item box (told);
    the hidden world runs float64, the agent may use float32; thinking eats wall time (told).

## 9. The pilot before any model rollout

Scripted, like round 5's `proof_ring`: cloud container (x86 Docker) first, then the Mac as runbook step 2. One pilot instance per profile; every policy runs through the real boxes. It must show: every item graded, none
failed, the layers of VF `RUNBOOK_MAC.md` step 2a; r and r_host measured in the box (section 11, row 14) and the
told numbers computed from it, then within 20% of a second measurement; W_box (F) or H_box (G) finishing inside B_res
with its predictor inside the item limits, again with 64 min idle, and the longest blocking command measured; a
float32 brute-force predictor killed at the limit and scored as null; null < D_box (D_box <= P0_box reported, not
gated, for F), O above C, sigma_box >= 0.15 at the point estimate on the exam's scales; grading inside section 6 with margin; the scans of 8.4 and the collision check refusing a planted public
world; `lab_log.jsonl` equal to the Lab's record; F's sigma under both scales. One GPU job adds its ceiling rows.

## 10. Decision rule: which profile first

F's stage 2 (FL `DECLARED.md` §2): PASS (T1-T6); INFER (T1, T3, T5, T6 hold, T2 does not fail, T4 does not hold;
"undecided" by its rule, never quoted as a pass); STATE (T1 holds, T3 fails); FAIL (T1 fails, T2's lower bound above
0.7, or the stages disagree). T2 "not read" (P0 within 2 SE of C) counts as not failing. G (A2): PASS with base nets
converged by R9 (else "at this compute"), UNDECIDED, FAIL. A missing or incomplete verdict (FL addendum 5) chooses
nothing; the lead decides. Any choice also needs Q2's answer (roadmap rho fails by construction when T3 holds).

| F \ G | PASS | UNDECIDED or FAIL |
|---|---|---|
| PASS or INFER | F first, G second | F |
| STATE, FAIL or incomplete | G | neither as a test of science |

F first when both qualify: its hidden part has no public trace (G's form is public, 8.8); its hypothesis fits the box
(one W start of 143 steps at job 003's shape: 101 min on 2 x86 cores; 200 steps at FL's CPU shape: 39-49 min) while G's told-form recipe needs 6,144-episode families; it is decision 1's default design (a).
Both fail: F as a compute-limited exam (decision 1(c); FL S3: P0 still falling at 1,000 worlds) only if its pilot
gives sigma_box >= 0.15 and the lead wants that test (Q5); otherwise the next world comes from the cards. Items 1-5
and 11-15 below do not depend on the verdicts and can start now.

## 11. Pin changes for the next port round

| # | file, function | change | lines |
|---|---|---|---|
| 1 | `physim2_env/profiles.py` | two entries; `b_pred`, `tiers`, `pool_sha256` replace `BASELINE_WORLDS` | 60 |
| 2 | `exam_configs/foundry_v1.json`, `gliders_trig_v1.json` | sections 2-4, `budget`, `n_sel` | 40 |
| 3 | `bundle.py` `null_pool`, `public_bundle`, `statement` | kept pool; F's library; `VENDOR_DROPPED` (G); budgets | 80 |
| 4 | `TASK.md.tmpl` | hidden sentence by kind; a compute-budget section | 90 |
| 5 | `tools/make_pool.py` (new) | build and record the null pool | 90 |
| 6 | `physim2_env/hidden/` (new, host only), `tools/make_instances.py` | section 1's draw and F's gate; G's hidden law | 300 |
| 7 | `lab_tools.py` `VfLabService` | Lab and O from the hidden hook (type b) | 30 |
| 8 | world modules, a lookup ahead of AE's `world_module` | two public modules | 340 |
| 9 | `tools/prove.py` | tiers; prebuilt P0, G's C | 80 |
| 10 | `agents/ref_foundry.py`, `ref_gliders_trig.py` | box-tier scripts, W_lib | 700 |
| 11 | `tools/check_request.py`, `tools/vfrun.py` | the section-6 bound; allowance per profile = 1,800 + scoring limit | 50 |
| 12 | `tools/pack_rollout.py` | publish a pilot's hidden instance after the key scan; check its committed sha256 | 40 |
| 13 | `tests/exam_pure.py` | told = computed; allowance; pool sha; bundle scans; no integer-seed draw; collision refusal; type-(b) Lab equals the public law at eta 0 only | 250 |
| 14 | `agents/time_box.py` (new), `tools/make_instances.py` | a scripted policy (physim2-script) timing the feasibility modes in the agent's box and an item box, relative paths; the instance stage logs its own clock (r_host) | 150 |
| 15 | `tools/run_report.py` | each score with the model-wait seconds and the agent box's CPU-seconds read from the engine | 40 |

About 2,300 lines, plus a GPU reference job outside the pin (400); the port's first estimate was a tenth of the
outcome (750 against 7,310, VF `README.md` §2). Items 5-7 and 14 add host-side or in-box compute: a host-safety re-audit. Out: the
sealed store (task #34), multi-instance exams, cgroup CPU caps (unless Q1), per-instance scales, a hidden defect family
for G, a GPU in a box, a new image.

## 12. Questions only the lead can answer

- Q1. Research budget: wall clock including the model's turns (as now; about 12 s per turn for Qwen, at most 26 s for
  Astra), or the agent box's CPU-seconds read from the engine (new code)?
- Q2. May the package carry costly, science-free material: F's screened-world library (recommended)?
- Q3. Null: the weak ridge (recommended), or the public P0(1,000) net (the generic recipe at 17 × the agent's compute)?
- Q4. A G pilot rollout while the defect's form is public here?
- Q5. If both fail: a compute-limited F, or back to the cards?
- Q6. Box-tier references on the Mac (up to 16 h per instance) or on a GPU pod's CPUs (faster, other hardware)?
