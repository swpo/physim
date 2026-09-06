# Scientific process audit — E1 #928

**Scope.** Only completed trace `0bdd699154ee4e1d96aac4e0961bc11d`, task `physim-BLOB2v2r2-E1#928`, from the specified `eval_fable_r2/E1/traces.jsonl` (line 1, `traces[0]`). This audit reads saved text and JSON only. It does not run the episode's code, replay a simulation, or start model/evaluation work. Node indices below are zero-based. Times are recorded node timestamps in UTC. Sampled nodes referenced by completed model calls and unique tool-call IDs define actions; contextual copies do not. For example, node 2973 repeats node 2972's edits and is not new work.

## Main finding

The agent did real empirical work: control trials, emission scans, fork comparisons, uncertainty estimates, and data quality checks. Its final code is mainly a **record interpolation pipeline**, with an empirical actuator correction and response uncertainty envelopes. No custom dynamical simulator or learned-law rollout appears in the submitted prediction path. The class called `World` loads recorded arrays; it does not integrate a world model.

- **L3F:** `789.72 + 400 = 1189.72`, well inside the readable base record ending at 2500.
- **L3E:** `1694.78 + 16*50 = 2494.78`, also inside that record. Even the last cubic interpolation stencil can use base samples through 2500.
- Thus these two instances were answered by recorded-history interpolation/counting, not by extrapolating learned dynamics from pre-anchor observations. The contract permitted collecting the whole record before reveal; this is not evidence of a forbidden post-reveal read.
- **Both dose instances used undisturbed recorded means.** Their selected injection ports were 3 and 1. The only dose-dependent mean-response template in the code applies to port 2, so it was not used for either submission. The treatment model affected sigma, not their means.

## Investigation and revisions

- **Data and interpolation.** The agent captured the base at 5tu resolution and recorded fork continuation through 3105 [S1–S2]. It examined port correlations, angle-like ports, control responses and refusals [S3]. `lib.py` loads data; `predict.py` adds interpolation. The continuation was unnecessary for the revealed L3F/L3E targets.
- **Replay hypothesis.** Early notes proposed rare stochastic branching; later notes instead blamed stale/colliding replies under load (`notes/findings.md:14–18,49–56`). The anchor-1000 comparison at lag 400 reported max errors 0.0048/0.0183 for devices 0/1 [S4]. Eight later lag-zero checks reported zero difference [S12; all eight in JSON]. These are sampled checks, not proof of exact determinism. See the parent audit's `CONCURRENCY.md` for state-update evidence.
- **Actuator fitting.** Initial signed-delta fits were weak; contraction toward the global mean followed [S5]. Final fitting used **81 command-step observations**, from a reported 44 trials [S10]. Every fourth observation was held out: coefficients fit on 60, sigma calibrated on 21. “Refit on all batches” did not mean coefficients refit on all 81. The split did not hold out whole trials/anchors.
- **Emission and L2 alternatives.** Emission work included all 12 ports at anchor 1600, selected ports at 2100, and port-1/2 dose series [S8–S9]. A conflicting port-2@900 run was rechecked and removed [S6]. Final envelopes/templates use 1600/2100. Powers 1.3 and 0.85 are empirical extrapolation choices. L2 compared global nowcast, climatology and device blends; final CRPS selection used the two observed devices, not learned hidden-cluster geometry [S7].
- **After reveal.** Ready: node 2970, `2026-09-06T00:58:27.141Z`, `toolu_01UJUVLKFPZJwjCTUQWafJko`; menu: node 2971. Node 2972 changed L1 u3 to sequential clipping and increased L3E sigma [S13–S14]. The accepted revealed command sequence prompted the clipping change; no new world experiment tested it. Node 2976 built all six payloads [S15].

## Exact post-reveal prediction methods

Artifact paths here are relative to embedded `app/probe/`. All six payload objects were compared with the unique sampled `probe_submit` arguments: **exact JSON-object equality**, with an `ok=true` response for each. The builder rounds arrays to five decimals (`build_payloads.py:23–24,26–56`).

**Shared baseline and uncertainty.** Let `B_d(t)` be the recorded device reading. `predict.py:59–81` uses four-point Catmull–Rom interpolation; ports 7 and 11 interpolate sine/cosine and recover the angle with `atan2`. `G(t)` linearly interpolates global mean/variance (`predict.py:83–88`). Base sigma is

`S_d,p(H) = 1.5*sqrt(replay_rms[p,bucket(H)]² + interp_rms[d,p]²) + 0.0005`.

It is repeated across slots (`predict_final.py:35–50`). Its fitted table pools fork-vs-record errors and reference/weak-injection runs; interpolation error uses a heuristic scaled leave-one-out estimate [S11].

| Instance | Concrete inputs and mean | Predictive sigma | Skill in this trace |
|---|---|---|---:|
| **L1** | Anchor 1758.1; commands `[[0.197,0.4786,0.5426],[-0.5066,-0.3148,-0.7374]]`; target 1768.1. Cumulative u1=-0.3096, u2=0.1638, sequentially clipped u3=0. Features `f=[0,0,0.3096,0.09585216,0.1638,1]`. Per-port `w=clip(w_coefs·f,-0.1,1.15)`; mean `B_0 + w*(G_mean-B_0)`. | `max(sigma_coefs·f,S_0,p(10))`, repeated over 13 slots. | 0.222473 |
| **L2** | Anchor 1242.24. Per-port mean is either `G_mean(t_a)` or the unweighted mean of saved global means over time. Same mean for all 13 hidden slots. Logged climatology ports: 3,7,9. | Nowcast: sqrt global variance. Climatology: sqrt(mean global variance + variance of global means). Floor 0.0001. | -0.003351 |
| **L3F** | Device 1; anchor 789.72; H=5,25,100,400. Means are `B_1` at **794.72, 814.72, 889.72, 1189.72**. No autoregression or dynamical rollout. | `S_1,p(H)`. The code's missing-data climatology fallback is not needed at these times. | 0.996427 |
| **L3E** | Anchor 1694.78; port 4; sign 1; threshold **-0.798244**. Interpolate device-0 slots at `t_a+5*k`, k=0…160. In each 10-interval window, count `value<thr` followed by `value>=thr`, then sum over 13 slots. Counts: **[8,6,8,6,7,5,7,7,6,6,6,5,8,5,7,5]**. | `max(0.45,0.18*sqrt(max(count,1)))`. No beyond-record rate fallback is used. | 0.885559 |
| **L4** | Anchor 817.82; port 3; amp 1.8696; dur 13.04; lags 10,25,50,100,175,250. Mean is **only** `B_1(t_a+lag)`; last time 1067.82. | Record uncertainty plus scaled port-3 response envelope, as below. Submitted sigma range 0.0005–0.03815. | 0.989061 |
| **L4D** | Anchor 1169.16; port 1; amp 0.3295; dur 10.68; lags 25,75,150. Mean is **only** `B_1(t_a+lag)`; last time 1319.16. | Record uncertainty plus port-1 envelope. Low-dose scale is floored at 1, so it does **not** shrink this envelope. Sigma range 0.00052–0.04961. | 0.993804 |

Sources: `revealed.json:1`; L1 `predict_final.py:53–74`; L2 `77–116`; L3F `119–129`; L3E `132–184`; L4/L4D `187–227`. Scores are the recorded `metrics.skill_*` values, rounded here; JSON retains full precision.

**Dose sigma details.** Define `q=amp^1.3*(dur/10)^0.85`. For each read-port, the code interpolates measured lag-wise RMS envelopes, multiplies by `max(1,q)`, caps at 1.5 times device-1 climatological SD, and combines in quadrature with base sigma (`predict_final.py:189–210`). For L4, q=2.8265668542. Port 3 was measured only at lags 10,25,50,100,150; the code grows the last envelope by 1.375 at lag 175 and 2.5 at lag 250. Its measured max-port RMS values were about 0.0018–0.0054. For L4D, q=0.2497454642 but the applied multiplier is 1. Its amp-1 port-1 envelopes at 25/75/150 had max-port RMS 0.00655/0.01179/0.04844 (`models_l4_env.json:179–292,407–478`).

The unused port-2 branch adds `clip(template*min(q,3.5),-2.9,2.9)` to the mean, wraps angle ports, and adds `0.6*abs(template adjustment)` in quadrature to sigma (`predict_final.py:211–219`). Neither actual injection selected that branch. High dose-instance scores therefore do not validate this template or a custom emission simulator. No baseline-only ablation or direct treatment-effect truth is supplied here.

## Bounded evidence index

The arrow gives the matched result node, not necessarily the next graph node. All listed call nodes are sampled. Quotes are small excerpts of commands or tool outputs.

| Ref | Call → result | UTC node timestamp | Unique tool-call ID | Bounded evidence |
|---|---:|---|---|---|
| S1 | 1286→1287 | 2026-09-05 22:25:16.849 | `toolu_01HX4miuZA82Pu2NMJLhDq66` | `99 2010.0 2500.0 {5.0}` |
| S2 | 2225→2226 | 2026-09-05 23:36:43.669 | `toolu_014QKAnzETJsNDFeBKAYth7J` | `121 2505.0 3105.0 {5.0}` |
| S3 | 1057→1073 | 2026-09-05 22:17:25.500 | `toolu_01XjPMw85L7H89WrPD51FqM6` | `port4 ~ p0,p1,p8` |
| S4 | 1155→1164 | 2026-09-05 22:20:57.101 | `toolu_011p2UzXPF6y7X5t18FsNLMn` | `lag   400: max0=0.0048 max1=0.0183` |
| S5 | 1474→1475 | 2026-09-05 22:30:53.984 | `toolu_0153WhZudiLtZ9DkzPRL2Cuc` | `normalized residual fraction with contraction model: 0.658` |
| S6 | 2347→2351 | 2026-09-05 23:52:32.659 | `toolu_01T3b94JJAuTpyPVasHJRuS1` | `remaining lines: 0` |
| S7 | 2692→2696 | 2026-09-06 00:34:38.019 | `toolu_01TKEc9HupvZDTWbtr84GQm4` | `L2 choice: ['now', 'now', 'now', 'clim', 'now', 'now', 'now', 'clim', 'now', 'clim', 'now', 'now']` |
| S8 | 2648→2668 | 2026-09-06 00:32:36.891 | `toolu_01ELLPxWKuHqKvuwzzpxZARP` | Port-2 amplitude/duration response table; e.g. `P2a030` versus `P2a100`. |
| S9 | 2670→2687 | 2026-09-06 00:33:15.058 | `toolu_01EZu9dQxPF18hY36DEQLSMc` | `prof[lag]=np.sqrt((D*D).mean(axis=(0,2))).tolist()` |
| S10 | 2820→2823 | 2026-09-06 00:47:07.810 | `toolu_01Ux2NdFLRzeo1tAT9NzFcEZ` | `N = 81`; `hold=np.arange(N)%4==0` |
| S11 | 2244→2245 | 2026-09-05 23:40:48.062 | `toolu_01VVAQYXGgsPKDJrMj59nQB2` | `weak={'ref','ref2','p3','p6','p7','p11'}` |
| S12 | 2932→2933 | 2026-09-06 00:53:16.927 | `toolu_01DnKMfzv7yrh3eDLan55rXi` | Last of eight checks: `2435 0.0 0.0`. |
| S13 | 2972→2974 | 2026-09-06 00:59:31.902 | `toolu_017uK4JgPMqyKmAsFk6SS5SR` | `u3 = float(np.clip(u3 + c[2], 0.0, 1.0))` |
| S14 | 2972→2975 | 2026-09-06 00:59:31.902 | `toolu_01J2EkQ9Zf2PzXGVBNUxGsYB` | Sigma changed from `max(.35,.15*sqrt(c))` to `max(.45,.18*sqrt(c))` (formula abbreviated). |
| S15 | 2976→2977 | 2026-09-06 00:59:40.292 | `toolu_01G4vFFgH79Dk5KzAtzuymJ1` | `python3 build_payloads.py revealed.json`; six payload shapes printed. |

### Accepted submissions

| Instance | Call → result | UTC node timestamp | Unique tool-call ID |
|---|---:|---|---|
| L1 | 2993→2994 | 2026-09-06 01:00:45.387 | `toolu_012BTyTdFxh9kf37bhPSsocZ` |
| L2 | 2997→2998 | 2026-09-06 01:01:09.699 | `toolu_0192k357iYNLZN3Vh1M255ha` |
| L3F | 3001→3002 | 2026-09-06 01:02:55.263 | `toolu_01WTLCNGj2cQ5Kok9Y7J5ByY` |
| L3E | 2989→2990 | 2026-09-06 01:00:15.186 | `toolu_01Xokr2M25eGPdGxCWWWB79N` |
| L4 | 3005→3006 | 2026-09-06 01:05:28.229 | `toolu_01DNpxZqnFWT7fGsfyRhHkTS` |
| L4D | 3012→3013 | 2026-09-06 01:06:47.811 | `toolu_01BZBJcKHM1jMWwEKDZN3ein` |

## Artifact availability and limits

- The embedded workspace contains the four predictor/loader/builder Python files, four model JSON files, both notes, `revealed.json`, all six payloads, `base_t5.json`, the batch-3 plan, and an append helper. Code lines cited above refer to these saved file strings, not a reconstruction.
- **Missing as workspace files:** `base_chunk_001.jsonl` through `base_chunk_007.jsonl`, `continuation.jsonl`, `global_sweep_600.jsonl`, all three `L1_trials_batch*.jsonl`, `div_A1000_f1.jsonl`, `inj_scan_A/B.jsonl`, `amp_series.jsonl`, `amp_series_p2.jsonl`, `L4_A900.jsonl`, `L4_A2100.jsonl`, and `qc_results.jsonl`. Tool messages retain observations and script outputs, but the archived workspace alone is not the full input set expected by the predictor.
- Four same-trace embedded tool-result text artifacts retain base slices: `toolu_01RwfNZMebZu5TE2gYrgGGsr.txt` (10–130), `toolu_01ScQ8ixYwPH2xvMvT1GSbSb.txt` (510–630), `toolu_01CT9XQ7ju7XvVsoPsvcKBtx.txt` (760–880), and `toolu_016GxLJFpXKQRi8Ek23Qowjo.txt` (2010–2130); all are line 1. They are not a complete replacement for the missing files.
- No independent payload regeneration or model-fit validation was run. L1's clipping change was not retested against the world after reveal. Sigma calibration includes heuristic scaling and weak-injection residuals. Stale/colliding tool-state observations support data-quality caution, but the exact interleaving that caused them is not visible in the trace.
- These are six instance results from one completed trace. They do not prove recovered laws, general performance, or extrapolation accuracy in untested states or doses.
