# E2 #942 — scientific process and bounded evidence

Root recovered the missing scientific handoff from the immutable trace. This is static evidence checking, not a simulation, model evaluation, or independent regeneration of all predictor inputs. `scientific_summary.json` contains exact artifact excerpts, input hashes, tool IDs, and sixteen literal global saves matched back to actual returned world measurements.

## Scientific workflow and submitted methods

The agent captured the base record, delegated fork-divergence and post-base runs, scanned actuator channels, collected free global streams, scanned all 13 emission ports, tested doses, fitted narrower empirical predictors, and revised them. It used 35 Agent invocations. Parallel collection and later more serial batches are visible; so are failures and changed hypotheses. [SCIENTIFIC_PROCESS.md](SCIENTIFIC_PROCESS.md) gives calibration counts, data quality limits, abandoned alternatives, and exact message/artifact references.

| Instance | Actual submitted path; target time(s) | Raw instance CRPS | Skill |
|---|---|---:|---:|
| L1 | Empirical actuator-distance contraction of device-0 record toward a local mean; **752.6** after one command. | 0.024033 | 0.522456 |
| L2 | Post-ready local rebuild: 0.7 device-pooled mean + 0.3 global mean at **1458.66**, repeated across all 13 hidden slots. | 0.082542 | 0.126002 |
| L3F | Cubic recorded-device interpolation at **1814.02, 1889.02, 2189.02**; calibrated replay/interpolation sigma. All are inside base 2500. | 0.003990 | 0.956350 |
| L3S | Saved-global interpolation and window averaging over **2260.72–2460.72** and **2660.72–2860.72**. The second is outside base but covered by pre-ready future samples. | 0.000849 | 0.951778 |
| L4 | Record + empirical RMS-derived shrinkage toward a local mean, with response uncertainty; port **6**, amp **2.7998**, dur **10.5**. Times **839.94, 854.94, 879.94, 929.94, 1004.94, 1079.94**. | 0.066575 | 0.404015 |
| L4D | Same RMS/decorrelation/shrinkage method; port **11**, amp **0.8124**, dur **16.78**. Times **1371, 1421, 1496**. | 0.002930 | 0.966390 |

Artifact references below are line numbers in the exact embedded `app/models/predictor3.py` string: L1 79–94, L3F 105–116, L3S 44–76 and 118–128, emissions 130–214. **Final L2 is not the saved `predict_L2` function at 97–103**: Bash node 5114, `toolu_01KwioQiU29N3GXNPj1gg4YA`, overrides its payload using the device/global blend. This is a marginal hidden-sensor estimate, not recovered hidden geometry.

### Global coverage is not the device continuation

A pre-ready fresh-anchor-2500 capture planned at node 4013 (`toolu_01FArZ3E2DiK4KjzcSpJQaCG`) recorded **16 global observations at 2525, 2550, …, 2900**, every 25 tu. These bracket the entire revealed second L3S window. The final code line 74–75 averages **41 linearly interpolated global samples** over each 200-tu window. It does not learn a dynamics law to reach 2860.72.

The device continuation is different: retained `cont_r1` saves have 80 distinct frames from 2505 to 3000, with a **2800 → 2905 gap**; `cont_r3b` adds 40 frames at 2905–3100. The combined device record ends at 3100 but is **not uniformly sampled at 5 tu** past 2500. Do not conflate that gap with the global stream used for L3S. The source comment calling the extension deterministic is the agent's interpretation, not a certified property.

### Emission response is a real narrower model, not a passive-mean-only copy of E1

For E2, measured per-port RMS `M` gives `alpha=clip(1-M²/(2*v),0,1)` and `mean=alpha*record+(1-alpha)*local_mean`; response magnitude/spread also changes sigma (`predictor3.py:168–209`). This changes the **mean**, unlike E1's two drawn dose cases. It is a fitted magnitude/decorrelation model, not a signed spatial-response template or general simulator.

The distinction between the two drawn ports has data support, not just scores. At training anchor 1200, amp 1, dur 10, the logged all-port device-1 RMS versus base at lags 175/250 was about **0.2249/0.2118 for injection port 6**, versus **0.0117/0.0108 for port 11** (node 2364 → 2365, `toolu_01YYUePYZxCJ71Foe7dctYBd`). A separate audit calculation from retained literal sensor observations finds port-6 versus port-11 RMS **0.22694/0.22093** at those lags. These support a much larger late response in that measured comparison, not a pure causal effect or hidden-condition truth.

The drawn L4 amplitude 2.7998 is above the apparatus limit 1. Its scaling beyond measured effective amplitude is heuristic and bounded; this episode's L4 CRPS 0.066575 / skill 0.404015 is a conditional strong-dose result, **not direct training validation above amp 1**. The two off-anchor validation examples use lower doses and L4D lags, not strong-dose lag-250 truth. Port 11's smaller measured residuals and near-baseline shrinkage must not be generalized to all ports or inferred from the high L4D skill alone.

## 6. Ready → closed-book payloads

Ready: **03:13:08.486Z**, node **5090 → 5091**, `toolu_017NUVZLCyYuN5ApLCGKPHa4`. Reported ready meters are **14,655 simulated tu / 1,016 environment turns**.

- **No sampled world-tool request after ready**: no read, wait, adjust, fork, inject, or reset. The nine Bash commands, eight Read calls, and one Edit are local file/predictor operations. No world transport appears in the inspected submitted path.
- Node 5092 builds all payloads from revealed parameters and `predictor3`. Node 5114 replaces L2 locally. Node 5128 fixes emission-sigma broadcasting; 5131 rebuilds L4/L4D with shape assertions; 5135 rounds those two payloads to four decimals. These changes precede their first accepted submissions, with no post-ready experiments.
- Six accepts, one each, in order **L3S, L1, L2, L3F, L4D, L4**. No rejected submissions or resubmissions. Every submitted payload object equals its archived `app/models/sub_*_i1.json` object exactly; hashes and tool IDs are in `summary.json` and [TIMELINE.md](TIMELINE.md).
- Final status, node **5147 → 5148**, `toolu_012PuXHtRXzJWggvxMdsgkqj`, reports all six flags true, phase revealed, head 2500, and `contexts=[]`. Status does not expose resource meters; these come from final trace metadata.
- Six submits plus one status account for **1,016 → 1,023 turns**. Simulated tu stays **14,655**. Post-ready work has 26 sampled model responses, one further 429 attempt, and 43,248 recorded output tokens.

No pre-ready tool request has a *recorded* result timestamp after ready. Missing replies and timed-out work still leave a late-server-work gap: absence of a later recorded result is not proof that no background server request remained. Node/result timestamps are not native execution times. See the bounded late-work evidence in `CONCURRENCY.md`.


## Static evidence check

Run `.venv/bin/python probes/blobs/agentenv/round5/resource_revision/e2_942_process_audit/finalize_scientific_evidence.py` from the repository root. It executes only audit code, never `predictor3.py` or any embedded command. It verifies coverage, selected final code paths, the L2 local override, all six accepted payload objects, and no sampled post-ready world request. It does not certify simulator transactions, causal response validation, complete generator inputs, or a general theory.
