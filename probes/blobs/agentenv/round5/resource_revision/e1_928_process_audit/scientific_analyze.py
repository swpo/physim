from pathlib import Path
import json, sys, re
TRACE_ID = "0bdd699154ee4e1d96aac4e0961bc11d"
TRACE_PATH = Path.home() / "v3work/ops/recovery_20260905/eval_fable_r2/E1/traces.jsonl"

def selected_trace():
    with TRACE_PATH.open("rb") as f:
        for line_num, raw in enumerate(f, 1):
            if TRACE_ID.encode() not in raw:
                continue
            record = json.loads(raw)
            for index, trace in enumerate(record.get("traces", [])):
                if trace.get("id") == TRACE_ID:
                    assert trace.get("is_completed") is True
                    assert trace["task"]["data"]["name"] == "physim-BLOB2v2r2-E1#928"
                    return line_num, [(["traces", index], trace)]
    raise RuntimeError("Exact completed trace ID not found")

def shape(obj):
    if isinstance(obj,dict):
        return {k: (list(v) if isinstance(v,dict) else {"type":type(v).__name__, "len":len(v)} if isinstance(v,(list,str)) else v) for k,v in obj.items()}
    return {"type":type(obj).__name__, "len":len(obj)}

def utc(ts):
    from datetime import datetime, timezone
    return datetime.fromtimestamp(ts, timezone.utc).isoformat(timespec="milliseconds") if isinstance(ts,(int,float)) else ts

def model_tools(trace):
    seen_nodes=set(); seen_tools=set()
    for call in trace["calls"]:
        if "node" not in call: continue
        ni=call["node"]
        if ni in seen_nodes: continue
        seen_nodes.add(ni)
        node=trace["nodes"][ni]
        if not node.get("sampled"): continue
        for tool in node["message"].get("tool_calls",[]):
            tid=tool["id"]
            if tid in seen_tools: continue
            seen_tools.add(tid)
            try: args=json.loads(tool["arguments"])
            except (ValueError,TypeError): args=tool["arguments"]
            yield ni, node, tool, args

def is_safe_name(name):
    return name.startswith("app/probe/") and not name.endswith(".sh") and not re.search(r"(?:secret|credential|token|password|\.env|private.?key)",name,re.I)


def scientific_summary(trace, line_num):
    ws=trace["info"]["physim"]["workspace"]
    tools=list(model_tools(trace))
    tool_by_id={tool["id"]:(ni,node,tool,args) for ni,node,tool,args in tools}
    def response_for(tid):
        for ri,node in enumerate(trace["nodes"]):
            m=node["message"]
            if m.get("role")=="tool" and m.get("tool_call_id")==tid:
                return ri,node,m.get("content")
        raise AssertionError("Missing result for " + tid)
    def ref(tid):
        ni,node,tool,args=tool_by_id[tid]
        ri,rnode,_=response_for(tid)
        return dict(node_index=ni, timestamp_utc=utc(node["timestamp"]),tool_call_id=tid,
                    tool=tool["name"],response_node_index=ri,
                    response_timestamp_utc=utc(rnode["timestamp"]))
    def artifact(path, lo, hi=None, quote=None):
        path="app/probe/"+path
        assert is_safe_name(path) and path in ws
        hi=lo if hi is None else hi
        lines=ws[path].splitlines()
        assert 1<=lo<=hi<=len(lines)
        out=dict(filename=path,line_start=lo,line_end=hi)
        if quote:
            assert quote in "\n".join(lines[lo-1:hi])
            out["quote"]=quote
        return out
    def decode(content):
        if isinstance(content,str):
            try: content=json.loads(content)
            except ValueError: return content
        if isinstance(content,dict) and "result" in content:
            return decode(content["result"])
        return content
    def flat(a):
        return [x for aa in a for x in flat(aa)] if isinstance(a,list) else [a]
    def dims(a):
        return [len(a)]+dims(a[0]) if isinstance(a,list) and a else []

    evidence_specs=[
      ("S1","toolu_01HX4miuZA82Pu2NMJLhDq66","Late base-chunk coverage", "response", "99 2010.0 2500.0 {5.0}"),
      ("S2","toolu_014QKAnzETJsNDFeBKAYth7J","Recorded continuation coverage", "response", "121 2505.0 3105.0 {5.0}"),
      ("S3","toolu_01XjPMw85L7H89WrPD51FqM6","Port relationship regression", "response", "port4 ~ p0,p1,p8"),
      ("S4","toolu_011p2UzXPF6y7X5t18FsNLMn","Replay comparison", "response", "lag   400: max0=0.0048 max1=0.0183"),
      ("S5","toolu_0153WhZudiLtZ9DkzPRL2Cuc","L1 contraction exploration", "response", "normalized residual fraction with contraction model: 0.658"),
      ("S6","toolu_01T3b94JJAuTpyPVasHJRuS1","Removal of anomalous p2@900 run", "response", "remaining lines: 0"),
      ("S7","toolu_01TKEc9HupvZDTWbtr84GQm4","Final predictor dry-run choices", "response", "L2 choice: ['now', 'now', 'now', 'clim', 'now', 'now', 'now', 'clim', 'now', 'clim', 'now', 'now']"),
      ("S8","toolu_01ELLPxWKuHqKvuwzzpxZARP","Port-2 dose scan summary", "response", "P2a030 [(10, -0.039, 0.0046), (25, -0.155, 0.0173)"),
      ("S9","toolu_01EZu9dQxPF18hY36DEQLSMc","Envelope/template construction", "command", "prof[lag]=np.sqrt((D*D).mean(axis=(0,2))).tolist()"),
      ("S10","toolu_01Ux2NdFLRzeo1tAT9NzFcEZ","L1 final fit", "response", "N = 81"),
      ("S11","toolu_01VVAQYXGgsPKDJrMj59nQB2","Uncertainty table construction", "command", "weak={'ref','ref2','p3','p6','p7','p11'}"),
      ("S12","toolu_01DnKMfzv7yrh3eDLan55rXi","Last of eight lag-zero QC checks", "response", "2435 0.0 0.0"),
      ("S13","toolu_017uK4JgPMqyKmAsFk6SS5SR","Post-reveal L1 state clipping", "new_string", "u3 = float(np.clip(u3 + c[2], 0.0, 1.0))"),
      ("S14","toolu_01J2EkQ9Zf2PzXGVBNUxGsYB","Post-reveal event sigma increase", "new_string", "sigma = np.maximum(0.45, 0.18 * np.sqrt(np.maximum(c, 1)))"),
      ("S15","toolu_01G4vFFgH79Dk5KzAtzuymJ1","Build actual payloads", "command", "python3 build_payloads.py revealed.json"),
    ]
    evidence=[]
    for label,tid,method,source,quote in evidence_specs:
        item=ref(tid)
        value=response_for(tid)[2] if source=="response" else tool_by_id[tid][3][source]
        assert quote in value, (label,quote)
        item.update(label=label,method=method,quote_location=source,quote=quote)
        evidence.append(item)

    rev=json.loads(ws["app/probe/revealed.json"])
    methods={
      "L1":dict(method="Empirical actuator contraction of recorded baseline toward global mean",
        mean="B0(t_a+5L) + clip(w_coefs dot f,-0.1,1.15)*(Gmean(t_a+5L)-B0(t_a+5L))",
        sigma="max(sigma_coefs dot f, base_sigma(device=0, H=5L)), repeated across 13 slots",
        features=[0,0,0.3096,0.09585216,0.1638,1],
        feature_definition=["u3_final","u3_final squared","abs(cumulative u1)","cumulative u1 squared","abs(cumulative u2)","1"],
        cumulative_u=[-0.3096,0.1638,0],u3_state_rule="start at 0; clip(state+command_u3,0,1) each command",
        target_times=[1768.1],direct_mean_response_fit_used=True,custom_dynamical_simulator_used=False,
        sources=[artifact("predict_final.py",53,74),artifact("models_l1.json",1,252)],
        evidence_labels=["S5","S10","S13","S15"]),
      "L2":dict(method="Port-wise choice between global nowcast and global climatology; slot-exchangeable marginals",
        mean="Global mean at t_a or unweighted mean of all saved global means; repeat over 13 hidden slots",
        sigma="sqrt(global variance at t_a) or sqrt(mean global variance + variance of global means); floor 1e-4",
        logged_climatology_ports=[3,7,9],logged_nowcast_ports=[0,1,2,4,5,6,8,10,11],
        choice_rule="Lower cumulative Gaussian CRPS on both observed devices, every fourth recorded time in [600,2300]",
        target_times=[1242.24],hidden_sensor_geometry_learned=False,custom_dynamical_simulator_used=False,
        sources=[artifact("predict_final.py",77,116),artifact("predict.py",83,88)],evidence_labels=["S7","S15"]),
      "L3F":dict(method="Recorded-history interpolation, not a learned-law forecast rollout",
        mean="B1(t_a+H), H=[5,25,100,400]",sigma="base_sigma(device=1,H), repeated across slots",
        target_times=[794.72,814.72,889.72,1189.72],last_target_time=1189.72,
        wholly_inside_readable_base=True,recorded_continuation_needed=False,
        missing_data_climatology_fallback_used=False,custom_dynamical_simulator_used=False,
        sources=[artifact("predict_final.py",119,129, "m = self.w.record_at(device, t_a + H)"),artifact("predict.py",59,81)],
        evidence_labels=["S4","S11","S15"]),
      "L3E":dict(method="Count upward crossings in interpolated recorded device-0 port-4 streams",
        sample_times="1694.78 + 5*k for k=0..160",threshold_used=-0.798244,sign=1,device=0,slots=13,
        window_rule="16 windows of ten adjacent sample intervals; sum (value<thr and next_value>=thr) over all slots",
        mean=json.loads(ws["app/probe/payload_L3E.json"])["mean"],
        sigma="max(0.45,0.18*sqrt(max(count,1))) per window",
        submitted_sigma=json.loads(ws["app/probe/payload_L3E.json"])["sigma"],
        last_target_time=2494.78,wholly_inside_readable_base=True,recorded_continuation_needed=False,
        beyond_record_rate_fallback_used=False,custom_dynamical_simulator_used=False,
        sources=[artifact("predict_final.py",132,184),artifact("payload_L3E.json",1)],evidence_labels=["S14","S15"]),
      "L4":dict(method="Undisturbed record mean plus empirical response uncertainty; no treatment mean adjustment for selected port 3",
        mean="B1(t_a+lag), lag=[10,25,50,100,175,250]",
        sigma="sqrt(base_sigma(1,lag)^2 + capped_scaled_envelope(port=3,lag)^2), repeated over slots",
        target_times=[827.82,842.82,867.82,917.82,992.82,1067.82],last_target_time=1067.82,
        dose_scale=1.8696**1.3*(13.04/10)**.85,applied_dose_scale=max(1,1.8696**1.3*(13.04/10)**.85),
        envelope_measured_lags=[10,25,50,100,150],late_lag_envelope_growth={"175":1.375,"250":2.5},
        treatment_mean_adjustment_used=False,port2_template_used=False,custom_dynamical_simulator_used=False,
        wholly_inside_readable_base=True,
        sources=[artifact("predict_final.py",187,224),artifact("models_l4_env.json",407,478)],evidence_labels=["S9","S15"]),
      "L4D":dict(method="Undisturbed record mean plus empirical response uncertainty; no treatment mean adjustment for selected port 1",
        mean="B1(t_a+lag), lag=[25,75,150]",
        sigma="sqrt(base_sigma(1,lag)^2 + capped_scaled_envelope(port=1,lag)^2), repeated over slots",
        target_times=[1194.16,1244.16,1319.16],last_target_time=1319.16,
        dose_scale=.3295**1.3*(10.68/10)**.85,applied_dose_scale=1,
        low_dose_envelope_shrunk=False,
        envelope_measured_lags=[10,25,50,75,100,150,175,250],
        treatment_mean_adjustment_used=False,port2_template_used=False,custom_dynamical_simulator_used=False,
        wholly_inside_readable_base=True,
        sources=[artifact("predict_final.py",187,227),artifact("models_l4_env.json",179,292)],evidence_labels=["S9","S15"]),
    }
    for ni,node,tool,args in tools:
        if not tool["name"].endswith("__submit"): continue
        name=args["instance"].split("@")[0]
        payload=json.loads(args["payload"]) if isinstance(args["payload"],str) else args["payload"]
        stored=json.loads(ws[f"app/probe/payload_{name}.json"])
        result=decode(response_for(tool["id"])[2])
        assert payload==stored and result.get("ok") is True
        item=methods[name]
        item.update(instance=args["instance"],revealed_parameters=rev[name],
                    skill=trace["metrics"]["skill_"+name],payload_shape=dims(payload["mean"]),
                    mean_range=[min(flat(payload["mean"])),max(flat(payload["mean"]))],
                    sigma_range=[min(flat(payload["sigma"])),max(flat(payload["sigma"]))],
                    submission={**ref(tool["id"]),"accepted":True,"matches_archived_payload":True},
                    payload_artifact=artifact(f"payload_{name}.json",1))
    assert all(v.get("submission") for v in methods.values())

    qc_ids=["toolu_01F7vwjSEQgTKfyDfAy7cRwP","toolu_01JX9mm9ZG3dm1noDYoVqg4g", "toolu_01QWLmgCmnRaPu2qVJXvFrpZ", "toolu_0131e5jaFk4NNGXDLf2HWpvA", "toolu_011eWeoz6vFgBMSwgKHd45ni", "toolu_017TWSZ6hzhNsXin2nWiTjx7", "toolu_01Hztwc7Esac5qPjsALWafTQ", "toolu_01DnKMfzv7yrh3eDLan55rXi"]
    qc=[]
    for tid in qc_ids:
        text=response_for(tid)[2]
        vals=text.split()
        assert len(vals)==3 and float(vals[1])==float(vals[2])==0
        qc.append({**ref(tid),"anchor":float(vals[0]),"max_difference_device0":0,"max_difference_device1":0,"quote":text})

    missing=[f"app/probe/data/base_chunk_{i:03d}.jsonl" for i in range(1,8)]+["app/probe/data/"+fn for fn in ["continuation.jsonl","global_sweep_600.jsonl", "L1_trials_batch1.jsonl","L1_trials_batch2.jsonl","L1_trials_batch3.jsonl", "div_A1000_f1.jsonl","inj_scan_A.jsonl","inj_scan_B.jsonl","amp_series.jsonl","amp_series_p2.jsonl","L4_A900.jsonl","L4_A2100.jsonl","qc_results.jsonl"]]
    assert all(name not in ws for name in missing)
    retained=[]
    for name,data in ws.items():
        if name.startswith("app/.vf-claude/"+TRACE_ID+"/") and "/tool-results/" in name and name.endswith(".txt"):
            obj=decode(data)
            steps=obj["steps"]
            times=sorted({s["t"] for s in steps})
            retained.append(dict(filename=name,line_start=1,line_end=1,sample_count=len(times),time_range=[times[0],times[-1]]))
    return dict(
      trace_id=TRACE_ID,task="physim-BLOB2v2r2-E1#928",source=str(TRACE_PATH),source_line=line_num,source_nested_path=["traces",0],
      status={"is_completed":trace["is_completed"],"ok":trace["ok"]},
      scope="Read-only inspection of this exact trace and its embedded workspace. No trace code execution, prediction regeneration, simulation, model/evaluation launch, GPU or remote process action.",
      action_selection="Completed model-call node references with sampled=true; unique tool-call IDs; results matched by tool_call_id. Contextual copies such as node2973 are not new actions.",
      top_findings=[
        "Substantial empirical exploration, but deployed means mainly reconstruct saved record values rather than roll out learned dynamics.",
        "L3F last target1189.72 and L3E last target2494.78 are inside the fully readable base [0,2500]; continuation is unused for these instances.",
        "Actual L4 port3 and L4D port1 predictions have undisturbed-record means. Dose influences uncertainty only; unused port2 template cannot explain their scores.",
        "No custom dynamical simulator is used by the retained final prediction path. Scores are instance-level evidence, not proof of recovered laws."
      ],
      methods_investigated=[
        {"method":"Port correlations and linear relations","evidence":["S3"]},
        {"method":"Apparatus controls/refusals, single/multiple command steps, delta regression then per-port contraction","evidence":["S5","S10","S13"]},
        {"method":"Fork divergence versus record, interpolation error, event-count definitions, lag-zero QC","evidence":["S4","S11","S12"]},
        {"method":"Emission port scans, selected second anchor, amplitude/duration series, RMS envelopes and port2 mean template","evidence":["S6","S8","S9"]},
        {"method":"L2 marginal global nowcast/climatology/device blends, CRPS selection","evidence":["S7"]}
      ],
      code_built=[
        {"filename":"app/probe/lib.py","role":"Recorded data loading, linear interpolation helper, threshold counts"},
        {"filename":"app/probe/predict.py","role":"World class loads records and continuation; cubic/circular device interpolation; linear global interpolation"},
        {"filename":"app/probe/predict_final.py","role":"Final six prediction methods and uncertainty rules"},
        {"filename":"app/probe/build_payloads.py","role":"Dispatch revealed parameters, check shapes/NaNs/positive sigma, round to five decimals and save payloads"}
      ],
      shared_method={
        "record_interpolator":"Four-point Catmull-Rom; sine/cosine interpolation and atan2 for ports7 and11",
        "record_source":artifact("predict.py",59,81,"Cubic (Catmull-Rom) interpolation at scalar time t; angle ports via sin/cos."),
        "global_interpolator":"Linear interpolation of saved mean/variance", "global_source":artifact("predict.py",83,88),
        "base_sigma":"1.5*sqrt(replay_rms[p,bucket(H)]^2+interp_rms[d,p]^2)+0.0005; constant over slots",
        "base_sigma_source":artifact("predict_final.py",35,50),
        "lag_buckets":json.loads(ws["app/probe/models_sigma.json"])["lag_buckets"],
        "dose_sigma":"q=amp^1.3*(dur/10)^0.85. Interpolate empirical RMS profile in lag, extrapolate later lags by min(3,1+1.5*(lag-last_lag)/100). Multiply by max(1,q), cap at1.5*device1 climatological SD over600..2300 and all slots. Combine in quadrature with base_sigma.",
        "unused_port2_branch":"Mean += clip(template*min(q,3.5),-2.9,2.9); wrap ports7/11; sigma adds0.6*abs(mean_adjustment) in quadrature",
        "unused_port2_source":artifact("predict_final.py",211,219,"if port == 2 and int(lag) in self.p2tmpl:")},
      l1_training={"reported_trials":44,"command_step_observations":81,"coefficient_fit_observations":60,"sigma_calibration_observations":21,
                   "split":"hold = np.arange(N)%4==0; sample-wise, not whole-trial or anchor holdout",
                   "refit_all_81":False,"evidence":"S10","model":artifact("models_l1.json",1,252)},
      post_reveal_changes=[
        {"change":"L1 raw cumulative u3 replaced by sequential clipping to[0,1]", "motivation":"Revealed accepted sequence crosses inferred lower bound; no post-reveal world test", "evidence":"S13"},
        {"change":"L3E sigma max(0.35,0.15sqrt(max(c,1))) -> max(0.45,0.18sqrt(max(c,1)))", "evidence":"S14"}
      ],
      ready=ref("toolu_01UJUVLKFPZJwjCTUQWafJko"),instances=methods,
      evidence=evidence,qc_checks=qc,
      artifact_availability={"available_probe_files":[name for name in ws if is_safe_name(name)],
        "missing_expected_data_files":missing,"retained_raw_tool_result_slices":retained,
        "not_self_contained":"Workspace lacks the bulk JSONL input files loaded by the retained code. Some observations and build scripts remain in messages. This audit did not reconstruct or rerun the pipeline."},
      limits=[
        "Only six concrete instance scores in one trace; no cohort or theory-proof claim.",
        "No independent regeneration of payloads or model fit; raw training/input files absent from embedded workspace layout.",
        "L1 held-out samples can share trials/anchors with fitted samples; the post-reveal clipping change was not empirically retested.",
        "RMS noise table includes weak-injection residuals, and interpolation/dose scaling is heuristic, not a calibrated dynamical law.",
        "Agent notes changed from rare stochastic branching to server-state anomaly interpretation. Observable repeated/stale/colliding replies do not reveal the exact internal request interleaving.",
        "No independent baseline-only ablation or treatment-effect target arrays are present; causal contribution to dose scores is not quantified."
      ])

REPORT_MARKDOWN = "# Scientific process audit — E1 #928\n\n**Scope.** Only completed trace `0bdd699154ee4e1d96aac4e0961bc11d`, task `physim-BLOB2v2r2-E1#928`, from the specified `eval_fable_r2/E1/traces.jsonl` (line 1, `traces[0]`). This audit reads saved text and JSON only. It does not run the episode's code, replay a simulation, or start model/evaluation work. Node indices below are zero-based. Times are recorded node timestamps in UTC. Sampled nodes referenced by completed model calls and unique tool-call IDs define actions; contextual copies do not. For example, node 2973 repeats node 2972's edits and is not new work.\n\n## Main finding\n\nThe agent did real empirical work: control trials, emission scans, fork comparisons, uncertainty estimates, and data quality checks. Its final code is mainly a **record interpolation pipeline**, with an empirical actuator correction and response uncertainty envelopes. No custom dynamical simulator or learned-law rollout appears in the submitted prediction path. The class called `World` loads recorded arrays; it does not integrate a world model.\n\n- **L3F:** `789.72 + 400 = 1189.72`, well inside the readable base record ending at 2500.\n- **L3E:** `1694.78 + 16*50 = 2494.78`, also inside that record. Even the last cubic interpolation stencil can use base samples through 2500.\n- Thus these two instances were answered by recorded-history interpolation/counting, not by extrapolating learned dynamics from pre-anchor observations. The contract permitted collecting the whole record before reveal; this is not evidence of a forbidden post-reveal read.\n- **Both dose instances used undisturbed recorded means.** Their selected injection ports were 3 and 1. The only dose-dependent mean-response template in the code applies to port 2, so it was not used for either submission. The treatment model affected sigma, not their means.\n\n## Investigation and revisions\n\n- **Data and interpolation.** The agent captured the base at 5tu resolution and recorded fork continuation through 3105 [S1–S2]. It examined port correlations, angle-like ports, control responses and refusals [S3]. `lib.py` loads data; `predict.py` adds interpolation. The continuation was unnecessary for the revealed L3F/L3E targets.\n- **Replay hypothesis.** Early notes proposed rare stochastic branching; later notes instead blamed stale/colliding replies under load (`notes/findings.md:14–18,49–56`). The anchor-1000 comparison at lag 400 reported max errors 0.0048/0.0183 for devices 0/1 [S4]. Eight later lag-zero checks reported zero difference [S12; all eight in JSON]. These are sampled checks, not proof of exact determinism. See the parent audit's `CONCURRENCY.md` for state-update evidence.\n- **Actuator fitting.** Initial signed-delta fits were weak; contraction toward the global mean followed [S5]. Final fitting used **81 command-step observations**, from a reported 44 trials [S10]. Every fourth observation was held out: coefficients fit on 60, sigma calibrated on 21. “Refit on all batches” did not mean coefficients refit on all 81. The split did not hold out whole trials/anchors.\n- **Emission and L2 alternatives.** Emission work included all 12 ports at anchor 1600, selected ports at 2100, and port-1/2 dose series [S8–S9]. A conflicting port-2@900 run was rechecked and removed [S6]. Final envelopes/templates use 1600/2100. Powers 1.3 and 0.85 are empirical extrapolation choices. L2 compared global nowcast, climatology and device blends; final CRPS selection used the two observed devices, not learned hidden-cluster geometry [S7].\n- **After reveal.** Ready: node 2970, `2026-09-06T00:58:27.141Z`, `toolu_01UJUVLKFPZJwjCTUQWafJko`; menu: node 2971. Node 2972 changed L1 u3 to sequential clipping and increased L3E sigma [S13–S14]. The accepted revealed command sequence prompted the clipping change; no new world experiment tested it. Node 2976 built all six payloads [S15].\n\n## Exact post-reveal prediction methods\n\nArtifact paths here are relative to embedded `app/probe/`. All six payload objects were compared with the unique sampled `probe_submit` arguments: **exact JSON-object equality**, with an `ok=true` response for each. The builder rounds arrays to five decimals (`build_payloads.py:23–24,26–56`).\n\n**Shared baseline and uncertainty.** Let `B_d(t)` be the recorded device reading. `predict.py:59–81` uses four-point Catmull–Rom interpolation; ports 7 and 11 interpolate sine/cosine and recover the angle with `atan2`. `G(t)` linearly interpolates global mean/variance (`predict.py:83–88`). Base sigma is\n\n`S_d,p(H) = 1.5*sqrt(replay_rms[p,bucket(H)]² + interp_rms[d,p]²) + 0.0005`.\n\nIt is repeated across slots (`predict_final.py:35–50`). Its fitted table pools fork-vs-record errors and reference/weak-injection runs; interpolation error uses a heuristic scaled leave-one-out estimate [S11].\n\n| Instance | Concrete inputs and mean | Predictive sigma | Skill in this trace |\n|---|---|---|---:|\n| **L1** | Anchor 1758.1; commands `[[0.197,0.4786,0.5426],[-0.5066,-0.3148,-0.7374]]`; target 1768.1. Cumulative u1=-0.3096, u2=0.1638, sequentially clipped u3=0. Features `f=[0,0,0.3096,0.09585216,0.1638,1]`. Per-port `w=clip(w_coefs·f,-0.1,1.15)`; mean `B_0 + w*(G_mean-B_0)`. | `max(sigma_coefs·f,S_0,p(10))`, repeated over 13 slots. | 0.222473 |\n| **L2** | Anchor 1242.24. Per-port mean is either `G_mean(t_a)` or the unweighted mean of saved global means over time. Same mean for all 13 hidden slots. Logged climatology ports: 3,7,9. | Nowcast: sqrt global variance. Climatology: sqrt(mean global variance + variance of global means). Floor 0.0001. | -0.003351 |\n| **L3F** | Device 1; anchor 789.72; H=5,25,100,400. Means are `B_1` at **794.72, 814.72, 889.72, 1189.72**. No autoregression or dynamical rollout. | `S_1,p(H)`. The code's missing-data climatology fallback is not needed at these times. | 0.996427 |\n| **L3E** | Anchor 1694.78; port 4; sign 1; threshold **-0.798244**. Interpolate device-0 slots at `t_a+5*k`, k=0…160. In each 10-interval window, count `value<thr` followed by `value>=thr`, then sum over 13 slots. Counts: **[8,6,8,6,7,5,7,7,6,6,6,5,8,5,7,5]**. | `max(0.45,0.18*sqrt(max(count,1)))`. No beyond-record rate fallback is used. | 0.885559 |\n| **L4** | Anchor 817.82; port 3; amp 1.8696; dur 13.04; lags 10,25,50,100,175,250. Mean is **only** `B_1(t_a+lag)`; last time 1067.82. | Record uncertainty plus scaled port-3 response envelope, as below. Submitted sigma range 0.0005–0.03815. | 0.989061 |\n| **L4D** | Anchor 1169.16; port 1; amp 0.3295; dur 10.68; lags 25,75,150. Mean is **only** `B_1(t_a+lag)`; last time 1319.16. | Record uncertainty plus port-1 envelope. Low-dose scale is floored at 1, so it does **not** shrink this envelope. Sigma range 0.00052–0.04961. | 0.993804 |\n\nSources: `revealed.json:1`; L1 `predict_final.py:53–74`; L2 `77–116`; L3F `119–129`; L3E `132–184`; L4/L4D `187–227`. Scores are the recorded `metrics.skill_*` values, rounded here; JSON retains full precision.\n\n**Dose sigma details.** Define `q=amp^1.3*(dur/10)^0.85`. For each read-port, the code interpolates measured lag-wise RMS envelopes, multiplies by `max(1,q)`, caps at 1.5 times device-1 climatological SD, and combines in quadrature with base sigma (`predict_final.py:189–210`). For L4, q=2.8265668542. Port 3 was measured only at lags 10,25,50,100,150; the code grows the last envelope by 1.375 at lag 175 and 2.5 at lag 250. Its measured max-port RMS values were about 0.0018–0.0054. For L4D, q=0.2497454642 but the applied multiplier is 1. Its amp-1 port-1 envelopes at 25/75/150 had max-port RMS 0.00655/0.01179/0.04844 (`models_l4_env.json:179–292,407–478`).\n\nThe unused port-2 branch adds `clip(template*min(q,3.5),-2.9,2.9)` to the mean, wraps angle ports, and adds `0.6*abs(template adjustment)` in quadrature to sigma (`predict_final.py:211–219`). Neither actual injection selected that branch. High dose-instance scores therefore do not validate this template or a custom emission simulator. No baseline-only ablation or direct treatment-effect truth is supplied here.\n\n## Bounded evidence index\n\nThe arrow gives the matched result node, not necessarily the next graph node. All listed call nodes are sampled. Quotes are small excerpts of commands or tool outputs.\n\n| Ref | Call → result | UTC node timestamp | Unique tool-call ID | Bounded evidence |\n|---|---:|---|---|---|\n| S1 | 1286→1287 | 2026-09-05 22:25:16.849 | `toolu_01HX4miuZA82Pu2NMJLhDq66` | `99 2010.0 2500.0 {5.0}` |\n| S2 | 2225→2226 | 2026-09-05 23:36:43.669 | `toolu_014QKAnzETJsNDFeBKAYth7J` | `121 2505.0 3105.0 {5.0}` |\n| S3 | 1057→1073 | 2026-09-05 22:17:25.500 | `toolu_01XjPMw85L7H89WrPD51FqM6` | `port4 ~ p0,p1,p8` |\n| S4 | 1155→1164 | 2026-09-05 22:20:57.101 | `toolu_011p2UzXPF6y7X5t18FsNLMn` | `lag   400: max0=0.0048 max1=0.0183` |\n| S5 | 1474→1475 | 2026-09-05 22:30:53.984 | `toolu_0153WhZudiLtZ9DkzPRL2Cuc` | `normalized residual fraction with contraction model: 0.658` |\n| S6 | 2347→2351 | 2026-09-05 23:52:32.659 | `toolu_01T3b94JJAuTpyPVasHJRuS1` | `remaining lines: 0` |\n| S7 | 2692→2696 | 2026-09-06 00:34:38.019 | `toolu_01TKEc9HupvZDTWbtr84GQm4` | `L2 choice: ['now', 'now', 'now', 'clim', 'now', 'now', 'now', 'clim', 'now', 'clim', 'now', 'now']` |\n| S8 | 2648→2668 | 2026-09-06 00:32:36.891 | `toolu_01ELLPxWKuHqKvuwzzpxZARP` | Port-2 amplitude/duration response table; e.g. `P2a030` versus `P2a100`. |\n| S9 | 2670→2687 | 2026-09-06 00:33:15.058 | `toolu_01EZu9dQxPF18hY36DEQLSMc` | `prof[lag]=np.sqrt((D*D).mean(axis=(0,2))).tolist()` |\n| S10 | 2820→2823 | 2026-09-06 00:47:07.810 | `toolu_01Ux2NdFLRzeo1tAT9NzFcEZ` | `N = 81`; `hold=np.arange(N)%4==0` |\n| S11 | 2244→2245 | 2026-09-05 23:40:48.062 | `toolu_01VVAQYXGgsPKDJrMj59nQB2` | `weak={'ref','ref2','p3','p6','p7','p11'}` |\n| S12 | 2932→2933 | 2026-09-06 00:53:16.927 | `toolu_01DnKMfzv7yrh3eDLan55rXi` | Last of eight checks: `2435 0.0 0.0`. |\n| S13 | 2972→2974 | 2026-09-06 00:59:31.902 | `toolu_017uK4JgPMqyKmAsFk6SS5SR` | `u3 = float(np.clip(u3 + c[2], 0.0, 1.0))` |\n| S14 | 2972→2975 | 2026-09-06 00:59:31.902 | `toolu_01J2EkQ9Zf2PzXGVBNUxGsYB` | Sigma changed from `max(.35,.15*sqrt(c))` to `max(.45,.18*sqrt(c))` (formula abbreviated). |\n| S15 | 2976→2977 | 2026-09-06 00:59:40.292 | `toolu_01G4vFFgH79Dk5KzAtzuymJ1` | `python3 build_payloads.py revealed.json`; six payload shapes printed. |\n\n### Accepted submissions\n\n| Instance | Call → result | UTC node timestamp | Unique tool-call ID |\n|---|---:|---|---|\n| L1 | 2993→2994 | 2026-09-06 01:00:45.387 | `toolu_012BTyTdFxh9kf37bhPSsocZ` |\n| L2 | 2997→2998 | 2026-09-06 01:01:09.699 | `toolu_0192k357iYNLZN3Vh1M255ha` |\n| L3F | 3001→3002 | 2026-09-06 01:02:55.263 | `toolu_01WTLCNGj2cQ5Kok9Y7J5ByY` |\n| L3E | 2989→2990 | 2026-09-06 01:00:15.186 | `toolu_01Xokr2M25eGPdGxCWWWB79N` |\n| L4 | 3005→3006 | 2026-09-06 01:05:28.229 | `toolu_01DNpxZqnFWT7fGsfyRhHkTS` |\n| L4D | 3012→3013 | 2026-09-06 01:06:47.811 | `toolu_01BZBJcKHM1jMWwEKDZN3ein` |\n\n## Artifact availability and limits\n\n- The embedded workspace contains the four predictor/loader/builder Python files, four model JSON files, both notes, `revealed.json`, all six payloads, `base_t5.json`, the batch-3 plan, and an append helper. Code lines cited above refer to these saved file strings, not a reconstruction.\n- **Missing as workspace files:** `base_chunk_001.jsonl` through `base_chunk_007.jsonl`, `continuation.jsonl`, `global_sweep_600.jsonl`, all three `L1_trials_batch*.jsonl`, `div_A1000_f1.jsonl`, `inj_scan_A/B.jsonl`, `amp_series.jsonl`, `amp_series_p2.jsonl`, `L4_A900.jsonl`, `L4_A2100.jsonl`, and `qc_results.jsonl`. Tool messages retain observations and script outputs, but the archived workspace alone is not the full input set expected by the predictor.\n- Four same-trace embedded tool-result text artifacts retain base slices: `toolu_01RwfNZMebZu5TE2gYrgGGsr.txt` (10–130), `toolu_01ScQ8ixYwPH2xvMvT1GSbSb.txt` (510–630), `toolu_01CT9XQ7ju7XvVsoPsvcKBtx.txt` (760–880), and `toolu_016GxLJFpXKQRi8Ek23Qowjo.txt` (2010–2130); all are line 1. They are not a complete replacement for the missing files.\n- No independent payload regeneration or model-fit validation was run. L1's clipping change was not retested against the world after reveal. Sigma calibration includes heuristic scaling and weak-injection residuals. Stale/colliding tool-state observations support data-quality caution, but the exact interleaving that caused them is not visible in the trace.\n- These are six instance results from one completed trace. They do not prove recovered laws, general performance, or extrapolation accuracy in untested states or doses.\n"

if __name__ == "__main__":
    line_num, found = selected_trace()
    trace = next(obj for _,obj in found if obj.get("id") == TRACE_ID and "nodes" in obj)
    mode = sys.argv[1] if len(sys.argv)>1 else "schema"
    if mode == "schema":
        print("task", trace["task"])
        print("physim shape", json.dumps(shape(trace["info"]["physim"])))
        print("node 0", json.dumps(shape(trace["nodes"][0])))
        print("node 1", json.dumps(shape(trace["nodes"][1])))
        print("call 0", json.dumps(shape(trace["calls"][0])))
        print("call 1", json.dumps(shape(trace["calls"][1])))
        print("scores", trace["rewards"], {k:v for k,v in trace["metrics"].items() if k.startswith("skill")})

    elif mode == "graph":
        for ni in [trace["calls"][j]["node"] for j in range(3)]:
            node=trace["nodes"][ni]
            print("NODE",ni,"sampled",node.get("sampled"),"timestamp",node.get("timestamp"),"message",shape(node["message"]))
            content=node["message"].get("content")
            if isinstance(content,list):
                for block in content:
                    print("block",shape(block) if isinstance(block,dict) else type(block).__name__)
                    if isinstance(block,dict) and block.get("type") == "tool_use":
                        print("tool", block.get("id"), block.get("name"))
            if node["message"].get("tool_calls"):
                print("tool calls shape",shape(node["message"]["tool_calls"][0]))
        ws=trace["info"]["physim"]["workspace"]
        print("artifact shape",shape(ws["app/probe/predict_final.py"]))

    elif mode == "artifacts":
        for name,data in trace["info"]["physim"]["workspace"].items():
            if is_safe_name(name):
                print(name,len(data),"chars", len(data.splitlines()), "lines")
    elif mode == "artifact":
        name=sys.argv[2]
        assert is_safe_name(name)
        data=trace["info"]["physim"]["workspace"][name]
        lo=int(sys.argv[3]) if len(sys.argv)>3 else 1
        hi=int(sys.argv[4]) if len(sys.argv)>4 else len(data.splitlines())
        for i,line in enumerate(data.splitlines(),1):
            if lo<=i<=hi:
                print(f"{i}: {line}")
    elif mode == "tools":
        for ni,node,tool,args in model_tools(trace):
            name=tool["name"]
            if name.endswith("__ready") or name.endswith("__submit"):
                print(ni,utc(node["timestamp"]),tool["id"],name, str(args)[:150] if "submit" not in name else str({k:v for k,v in args.items() if k != "payload"})[:150])

    elif mode == "toolnames":
        from collections import Counter
        print(Counter(t["name"] for _,_,t,_ in model_tools(trace)))
        for ni,node,tool,args in list(model_tools(trace))[-30:]:
            print(ni,utc(node["timestamp"]),tool["id"],tool["name"], list(args) if isinstance(args,dict) else type(args).__name__)

    elif mode == "nodes":
        lo=int(sys.argv[2]); hi=int(sys.argv[3]) if len(sys.argv)>3 else lo
        maxchars=int(sys.argv[4]) if len(sys.argv)>4 else 3000
        callnodes={c["node"] for c in trace["calls"] if "node" in c}
        for ni in range(lo,hi+1):
            node=trace["nodes"][ni]; msg=node["message"]
            print("NODE",ni,"sampled",node.get("sampled"),"model_call",ni in callnodes,"time",utc(node.get("timestamp")),"role",msg.get("role"),"tool_call_id",msg.get("tool_call_id"))
            for k in ["content","reasoning_content"]:
                val=msg.get(k)
                if isinstance(val,str) and val:
                    if re.search(r"(?:\.sh(?:\s|[\"\'])|api[_-]?key|authorization:|bearer |private.?key|BEGIN .*KEY)",val,re.I):
                        print(k,"[not inspected: safety filter]")
                    else: print(k, val[:maxchars])
            for tool in msg.get("tool_calls",[]):
                args=json.loads(tool["arguments"])
                print("TOOL",tool["name"],tool["id"])
                if tool["name"].endswith("__submit"):
                    print("instance",args.get("instance"),"payload chars",len(args.get("payload","")))
                elif re.search(r"(?:\.sh(?:\s|[\"\'])|api[_-]?key|authorization:|bearer |private.?key|BEGIN .*KEY)",tool["arguments"],re.I):
                    print("arguments [not inspected: safety filter]")
                else: print("arguments",str(args)[:maxchars])

    elif mode == "science_timeline":
        wanted=set(sys.argv[2:]) or {"Agent","Write","Edit","TaskCreate"}
        for ni,node,tool,args in model_tools(trace):
            if tool["name"] not in wanted: continue
            raw=tool["arguments"]
            if re.search(r"(?:\.sh(?:\s|[\"\'])|api[_-]?key|authorization:|bearer |private.?key|BEGIN .*KEY)",raw,re.I): continue
            if tool["name"] == "Bash":
                info=args.get("description","")
            elif tool["name"] == "Agent":
                info=args.get("description","")+" | "+str(args.get("prompt",""))[:800]
            elif tool["name"] in {"Write","Edit"}:
                info=args.get("file_path","")
            else:
                info=args.get("subject","")+" | "+args.get("description","")[:300]
            print(ni,utc(node["timestamp"]),tool["id"],tool["name"],info)
    elif mode == "search":
        pattern=re.compile(sys.argv[2],re.I)
        lo=int(sys.argv[3]) if len(sys.argv)>3 else 0
        hi=int(sys.argv[4]) if len(sys.argv)>4 else len(trace["nodes"])-1
        seen=set()
        for call in trace["calls"]:
            ni=call.get("node")
            if ni is None or ni in seen or not lo<=ni<=hi: continue
            seen.add(ni); node=trace["nodes"][ni]
            if not node.get("sampled"): continue
            msg=node["message"]
            parts=[]
            for k in ["content","reasoning_content"]:
                value=msg.get(k)
                if isinstance(value,str):
                    for match in pattern.finditer(value):
                        part=value[max(0,match.start()-100):match.end()+240].replace("\n"," ")
                        if not re.search(r"(?:api[_-]?key|authorization:|bearer |private.?key|BEGIN .*KEY)",part,re.I):
                            parts.append(part)
            if parts:
                tids=[t["id"] for t in msg.get("tool_calls",[])]
                print(ni,utc(node["timestamp"]),tids," || ".join(parts[:4]))
    elif mode == "submits":
        ws=trace["info"]["physim"]["workspace"]
        for ni,node,tool,args in model_tools(trace):
            if not tool["name"].endswith("__submit"): continue
            p=json.loads(args["payload"]) if isinstance(args["payload"],str) else args["payload"]
            name=args["instance"].split("@")[0]
            saved=json.loads(ws[f"app/probe/payload_{name}.json"])
            print(ni,utc(node["timestamp"]),tool["id"],args["instance"],"matches artifact",p==saved)
            for ri,rnode in enumerate(trace["nodes"]):
                rm=rnode["message"]
                if rm.get("role")=="tool" and rm.get("tool_call_id")==tool["id"]:
                    print("response",ri,utc(rnode.get("timestamp")), str(rm.get("content"))[:250])
                    break

    elif mode == "evidence":
        ids={int(n) for n in sys.argv[2:]}
        for ni,node,tool,args in model_tools(trace):
            if ni not in ids: continue
            raw=tool["arguments"]
            if re.search(r"(?:\.sh(?:\s|[\"\'])|api[_-]?key|authorization:|bearer |private.?key|BEGIN .*KEY)",raw,re.I): continue
            print("NODE",ni,utc(node.get("timestamp")),tool["id"],tool["name"])
            if tool["name"] == "Bash":
                print("description",args.get("description"))
                for ln,line in enumerate(args.get("command","").splitlines(),1):
                    print(f"command line {ln}: {line}")
            elif tool["name"] not in {"Write","Agent"} and not tool["name"].endswith("__submit"):
                print("arguments",str(args)[:1500])
            for ri,rnode in enumerate(trace["nodes"]):
                rm=rnode["message"]
                if rm.get("role")=="tool" and rm.get("tool_call_id")==tool["id"]:
                    content=rm.get("content","")
                    if re.search(r"(?:api[_-]?key|authorization:|bearer |private.?key|BEGIN .*KEY)",str(content),re.I):
                        content="[not inspected: safety filter]"
                    print("RESPONSE",ri,utc(rnode.get("timestamp")),str(content)[:5500])
                    break

    elif mode == "retained_data":
        ws=trace["info"]["physim"]["workspace"]
        for name,data in ws.items():
            if name.startswith("app/.vf-claude/"+TRACE_ID+"/") and "/tool-results/" in name and name.endswith(".txt"):
                print("FILE",name,"chars",len(data),"lines",len(data.splitlines()))
                try: obj=json.loads(data)
                except ValueError: print("nonJSON",data[:100]); continue
                print("shape",shape(obj))
                def times(x):
                    ts=[]
                    if isinstance(x,dict):
                        if isinstance(x.get("t"),(int,float)): ts.append(x["t"])
                        for k,v in x.items():
                            if k in {"provider_state","signature","token_ids"}: continue
                            if isinstance(v,(dict,list)): ts+=times(v)
                            elif isinstance(v,str) and k in {"text","result","content"}:
                                try: ts+=times(json.loads(v))
                                except ValueError: pass
                    elif isinstance(x,list):
                        for v in x: ts+=times(v)
                    return ts
                ts=sorted(set(times(obj)))
                print("times",len(ts),ts[:4],ts[-4:])

    elif mode == "summary_data":
        import math
        ws=trace["info"]["physim"]["workspace"]
        detail=trace["info"]["physim"]["detail"]
        print("detail shape",shape(detail))
        for k,v in detail.get("instances",{}).items() if isinstance(detail.get("instances"),dict) else enumerate(detail.get("instances",[])):
            print("instance detail",k,shape(v))
        def flatten(v):
            return [x for vv in v for x in flatten(vv)] if isinstance(v,list) else [v]
        def dims(v):
            return [len(v)]+dims(v[0]) if isinstance(v,list) and v else []
        for k in ["L1","L2","L3F","L3E","L4","L4D"]:
            p=json.loads(ws[f"app/probe/payload_{k}.json"])
            m=flatten(p["mean"]); s=flatten(p["sigma"])
            print(k,"shape",dims(p["mean"]),"meanrange",[min(m),max(m)],"sigmarange",[min(s),max(s)])
        rev=json.loads(ws["app/probe/revealed.json"])
        for k in ["L4","L4D"]:
            a=rev[k]["amp"]; d=rev[k]["dur"]
            print(k,"scale",a**1.3*(d/10)**.85)
        data=json.loads(ws["app/probe/models_l4_env.json"])
        print("env shape",shape(data))
        for port in [1,3]:
            print("env port",port,"max by lag",{k:max(v) for k,v in data["envelope"][str(port)].items()})

    elif mode == "model_lines":
        data=trace["info"]["physim"]["workspace"]["app/probe/models_l4_env.json"]
        lines=data.splitlines()
        for i,line in enumerate(lines,1):
            if line.startswith('  "') and line.endswith(': {'):
                j=next((j for j in range(i+1,len(lines)+1) if lines[j-1].startswith('  "') and lines[j-1].endswith(': {')),len(lines)-1)
                print(i,j-1,line)

    elif mode == "write_report":
        out=Path(__file__).resolve().parent
        assert out.name=="e1_928_process_audit"
        summary=scientific_summary(trace,line_num)
        (out/"scientific_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
        (out/"SCIENTIFIC_PROCESS.md").write_text(REPORT_MARKDOWN)
        print("Wrote",out/"scientific_summary.json")
        print("Wrote",out/"SCIENTIFIC_PROCESS.md")
        print("Validated",len(summary["instances"]),"matching accepted submissions;",len(summary["evidence"]),"bounded action quotes;",len(summary["qc_checks"]),"QC checks.")
