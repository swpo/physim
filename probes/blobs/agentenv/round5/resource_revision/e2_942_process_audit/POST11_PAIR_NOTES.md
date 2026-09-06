# Post11 pair notes — two completed Fable cases

**Two completed cases, not a clean comparative benchmark.** Worlds/seeds, menus, ports and hidden draws differ. Do not average these cases into a benchmark mean or attribute their score difference to model quality. Both used fresh `v2r2`, readied, submitted all six instances successfully, and had zero cap hits and no resource truncation.

## Verified quantities

**[A]** Existing `../e1_928_process_audit/summary.json`: `accounting`, `resources`, `scores`, `ready_and_submission`; existing `validation.json`. **[B]** E2 `summary.json`, same keys; `experiment_summary.json`: `handles`, `reply_accounting`. `paired_summary.json` retains all per-tool counts, per-instance skills, resource meters and input hashes.

| Quantity | E1 #928 [A] | E2 #942 [B] |
|---|---:|---:|
| World | `p4g2_044` | `p6g8_033` |
| Reported episode skill (six-instance mean) | **0.6806623799475607** | **0.6544984435867794** |
| Wall time, not billing | 3h34m47.6s | 5h49m22.1s |
| Sampled model responses / error attempts | **1,216 /23** | **2,218 /40** |
| Error breakdown, all without usage | 22×429;1 reset | 38×429;2×400 |
| Prompt: excludes cache reads, includes cache writes | 4,818,550 | 5,979,370 |
| Cache-read input | 117,000,774 | 213,938,314 |
| All input | 121,819,324 | 219,917,684 |
| Completion / reasoning subset | 1,199,851 /153,020 | 2,265,077 /97,241 |
| Input + completion (no extra reasoning bucket) | **123,019,175** | **222,182,761** |
| Agent / Bash / Write calls | 22 /324 /52 | 35 /665 /276 |
| Unique tools / environment requests / persisted turns | 1,484 /1,065 /891 | 2,336 /1,300 /1,023 |
| Environment timeouts / missing results | 54 /2 | 266 /11 |
| Read / wait requests | 485 /3 | 421 /466 |
| Persisted base / fork read frames | 500 /625 | 500 /895 |
| Live simulated tu | 11,495 | 14,655 |
| Fork replies / distinct returned IDs | 181 /145 | 100 /96 |
| Repeated IDs / IDs with multiple anchors | 22 /15 | 3 /1 |
| Peak logical open / resident forks | 31 /8 | 12 /8 |
| Evictions / reconstructions | 44 /168 | 3 /121 |
| Post-ready world requests / accepted submits | 0 /6 | 0 /6 |

Usage definitions: `.venv/lib/python3.13/site-packages/verifiers/v1/types.py:107–167`; `v1/dialects/anthropic.py:146–160`. Neither audit has actual billing or separate cache-write totals. Error attempts are not known retry chains. Auxiliary `count_tokens` traffic is unrecorded. No dollar or missing-token estimate is justified.

## Strategies: genuine empirical modeling, narrower than learned dynamics

Both investigators calibrated apparatus, compared forks, scanned emissions, fitted uncertainty and revised predictors. **No general learned dynamical simulator appears in either submitted path. This is not “no modeling.”** Empirical contraction and RMS/decorrelation/shrinkage are real narrower predictive models.

- **E1:** L1 uses per-port record-to-global contraction (81 reported command-step observations:60 fit/21 calibration). L2 chooses global nowcast/climatology and repeats slot marginals. L3F interpolates at794.72,814.72,889.72,1189.72; L3E counts crossings through2494.78. Both undisturbed tasks stay inside base2500. Drawn emission ports3/1 leave the mean passive and change sigma; its fitted port2 signed mean template is unused. **Cites:** E1 `SCIENTIFIC_PROCESS.md:9–45`; embedded `app/probe/predict_final.py:53–227`; post-ready clipping node2972/`toolu_017uK4JgPMqyKmAsFk6SS5SR`.
- **E2:** L1 fits actuator-distance contraction toward local means. L2's final payload is a local override:0.7 pooled-device mean +0.3 global mean, repeated across hidden slots; neither case recovers hidden geometry. L3F uses cubic record interpolation at1814.02,1889.02,2189.02, all in base. L4/L4D change **mean and sigma** via measured RMS→decorrelation/shrinkage. **Cites:** embedded `app/models/predictor3.py:79–94,105–116,130–214`; L2 override node5114/`toolu_01KwioQiU29N3GXNPj1gg4YA`.

### Out of base does not necessarily mean extrapolation

E2 L3S windows are2260.72–2460.72 and2660.72–2860.72. Before reveal, a fresh anchor2500 capture recorded **16 globals at2525,2550,…,2900, every25tu**, which cover the second window. The predictor averages41 **linear global-interpolation** samples per200tu window (`predictor3.py:44–76,119–128`). Exact capture: plan node4013/`toolu_01FArZ3E2DiK4KjzcSpJQaCG`; fork node4016/`toolu_01PzHLUnhsFM9kiRdMdL7cQK`; handle`fceee3e6210a425daa3830b8d928cd49a`.

Device continuation is separate: retained `cont_r1` has80 distinct frames2505–3000 with a2800→2905 gap; `cont_r3b` has40 frames2905–3100. **Do not claim uniform5tu device coverage after2500 or confuse its gap with the L3S globals.** E1 collected continuation through3105, but its drawn L3F/L3E did not need it (E1 node2225→2226/`toolu_014QKAnzETJsNDFeBKAYth7J`, `SCIENTIFIC_PROCESS.md:18,54`).

Record and allowed future sampling before reveal are **permitted, not misconduct**. These successful undisturbed instances do not, by themselves, establish learned dynamical extrapolation.

### Emission evidence, not score-only explanations

At E2 training anchor1200, amp1, dur10, logged all-port device1 RMS versus base at lags175/250 is approximately**0.2249/0.2118 for port6** and **0.0117/0.0108 for port11** (node2364→2365, `toolu_01YYUePYZxCJ71Foe7dctYBd`). An independent audit calculation from retained literals gives port6-versus-port11 RMS0.22694/0.22093. These support a larger late response at that measured condition, not hidden-condition truth or a causal ablation.

E2 L4 draws port6, amp2.7998, dur10.5: **CRPS0.066575 / skill0.404015**. Its bounded above-apparatus scaling is heuristic (`predictor3.py:135,168–209`), with **no direct training validation above amp1**. E2 L4D draws port11, amp0.8124, dur16.78: **CRPS0.002930 / skill0.966390**. The two off-anchor checks use lower doses and L4D lags, not strong-dose lag250. Do not infer weak effects from high skill alone, or generalize port11's smaller measured residuals to all ports. E1's high dose scores likewise do not validate its unused port2 mean template (E1 `SCIENTIFIC_PROCESS.md:43–45`).

## Integrity and boundary checks are separate from task discrimination

E1 has same-node distinct fork calls returning one ID at different anchors and repeated advancing-base times (E1 `CONCURRENCY.md`, nodes93,670,1892). E2 has its own ID-reuse/clock/reset evidence; nodes231/244/254 return one handle at2500 and1000. **E2 has no same-node fork/fork pair.** Its38 identical copied result nodes are graph copies, not state defects. Exact refs are in E2 `CONCURRENCY.md`.

Native `_with_state` uses whole-state GET/function/PUT; the shared-state mechanism is relevant, but transaction timing and commit history are unavailable. E1 ordinary replies exceed persisted turns by118. E2 ordinary replies equal1,023 turns, yet reply-derived sensor/sim sums fall8,355 slot-tu/625tu below final meters. A matching counter is not transaction exactness. State integrity defects and whether task success distinguishes modeling from lookup are **different issues**.

Both have zero sampled world requests after ready and six accepted payloads exactly matching archived objects. E1 submits L3E,L1,L2,L3F,L4,L4D; E2 submits L3S,L1,L2,L3F,L4D,L4. E2's local L2 override and sigma-shape fix occur before first submission. Bulk missing inputs prevent full independent predictor regeneration. Timeouts/missing replies leave unknown native late-work completion; no post-ready world access is evidenced. See both timelines.

## Two cheaper controls — designs only, not executed

1. **Model-free native integrity regression.** Use small deterministic handlers through actual MCP/whole-state transport with event barriers, not sleeps or a frontier rollout. Test same-context and different-fork concurrent mutations: unique IDs/stable anchors, additive meters/clocks, durable resets, cache lifecycle, and ready's gate against delayed requests. Add six scripted shape-valid submissions and a large-output persistence check. This is a wiring diagnostic, not scientific performance.
2. **Declared scientific controls.** Keep record-plus-allowed-continuation and passive/no-emission-mean controls separate from empirical RMS/shrinkage. For later valid comparisons, predeclare targets outside **all captured streams**, active-response ports/doses, and anchor/protocol holdouts. Report strata and failures; do not select quiet ports or only favorable completions after scoring.

Neither proposal imposes pressure/time caps on investigators. No model calls, simulations, pilots, production fix or environment test was run here. A diagnostic pass is not a performance estimate.

**Operator stop context:** all runs stopped; two reported completions; E1#929 unscored `HarnessError`; queued E2#943 operator-canceled after about11minutes; other queued tasks had no model stage. These are not additional scored cases. E1's existing audit was used without re-auditing its raw trace. E2 input and selected-trace hashes are verified in `validation.json`; `paired_summary.json` hashes the E1 audit inputs used.
