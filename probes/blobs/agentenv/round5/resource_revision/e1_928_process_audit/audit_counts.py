"""Read-only audit of one completed trace. Never executes trace code or world tools."""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import inspect
import json
import re
from verifiers.v1.types import Usage

ROOT = Path.cwd()
OUT = ROOT / "probes/blobs/agentenv/round5/resource_revision/e1_928_process_audit"
SOURCE = Path.home() / "v3work/ops/recovery_20260905/eval_fable_r2/E1/traces.jsonl"
TARGET = "0bdd699154ee4e1d96aac4e0961bc11d"

def utc(t):
    return datetime.fromtimestamp(t, timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z") if t is not None else None

def decode(value):
    for _ in range(6):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except (ValueError, TypeError):
                return value
        elif isinstance(value, dict) and set(value) == {"result"} and isinstance(value["result"], str):
            value = value["result"]
        elif isinstance(value, list) and len(value) == 1 and isinstance(value[0], dict) and value[0].get("type") == "text":
            value = value[0].get("text", "")
        else:
            return value
    return value

found = []
with SOURCE.open() as fh:
    for lineno, line in enumerate(fh, 1):
        if TARGET not in line:
            continue
        outer = json.loads(line)
        for item in outer.get("traces", []):
            if item.get("id") == TARGET:
                found.append((lineno, outer.get("id"), item))
assert len(found) == 1, f"Expected one exact trace, found {len(found)}"
lineno, episode_id, tr = found[0]
assert tr["task"]["data"]["name"] == "physim-BLOB2v2r2-E1#928"
assert tr["is_completed"] and tr["ok"]
phy = tr["info"]["physim"]
workspace = phy.get("workspace", {})
nodes = tr["nodes"]
calls = tr["calls"]
completed = [(i, c) for i, c in enumerate(calls) if "node" in c]
assert len(completed) == sum(bool(n.get("sampled")) for n in nodes)
results = {}
for ni, n in enumerate(nodes):
    if n["message"]["role"] == "tool":
        tid = n["message"]["tool_call_id"]
        assert tid not in results
        results[tid] = (ni, n)
rows = []
seen = set()
for ci, c in completed:
    ni = c["node"]
    for tool in nodes[ni]["message"].get("tool_calls", []):
        assert tool["id"] not in seen
        seen.add(tool["id"])
        rr = results.get(tool["id"])
        row = dict(node=ni, model_call_index=ci, tool_call_id=tool["id"], tool=tool["name"],
                   timestamp=nodes[ni].get("timestamp"), args=json.loads(tool["arguments"]),
                   result_node=rr[0] if rr else None,
                   result_timestamp=rr[1].get("timestamp") if rr else None,
                   result=decode(rr[1]["message"].get("content")) if rr else None)
        row["persisted_output"] = False
        row["persisted_recovered"] = False
        if isinstance(row["result"], str) and row["result"].startswith("<persisted-output>"):
            row["persisted_output"] = True
            match = re.search(r"Full output saved to: (\S+)", row["result"])
            row["persisted_path"] = "app/" + match[1] if match else None
            if row["persisted_path"] in workspace:
                row["result"] = decode(workspace[row["persisted_path"]])
                row["persisted_recovered"] = True
        r = row["result"]
        if r is None:
            outcome = "no_result_recorded"
        elif isinstance(r, str) and r == "The operation timed out.":
            outcome = "tool_timeout"
        elif isinstance(r, dict) and "error" in r:
            err = r["error"]
            outcome = "unknown_context" if err.startswith("unknown context") else "malformed_argument" if err.startswith("ports must") else "other_error"
        elif isinstance(r, dict) and r.get("result") == "adjust_rejected":
            outcome = "partial_adjustment_then_refused" if r["steps_applied"] else "adjustment_refused"
        elif isinstance(r, str) and re.match(r"Exit code [1-9][0-9]*", r):
            outcome = "nonzero_shell_exit"
        elif isinstance(r, str) and "SyntaxError:" in r and row["tool"] == "Bash":
            outcome = "returned_with_embedded_code_error"
        else:
            outcome = "success_response" if row["tool"].startswith("mcp__probe__") else "returned_without_explicit_error"
        row["outcome"] = outcome
        rows.append(row)
rows.sort(key=lambda x: (x["timestamp"], x["node"]))
probe = [r for r in rows if r["tool"].startswith("mcp__probe__")]
ready = next(r for r in rows if r["tool"] == "mcp__probe__ready")
ready_t = ready["timestamp"]
post = [r for r in rows if r["timestamp"] > ready_t]

usage = Usage.aggregate(Usage.model_validate(c["usage"]) for _, c in completed)
assert usage is not None
usage_dict = usage.model_dump(exclude_none=True)
usage_dict.update(input_tokens=usage.input_tokens, total_tokens=usage.total_tokens,
                  cache_write_tokens=None, provider_uncached_input_excluding_cache_writes=None,
                  billed_dollars=None,
                  reason="prompt_tokens merges provider input_tokens + cache_creation_input_tokens; cache reads are separate; reasoning is a subset of completion. No cost field is recorded.")
post_completed = [(i,c) for i,c in completed if nodes[c["node"]]["timestamp"] > ready_t]
post_usage = Usage.aggregate(Usage.model_validate(c["usage"]) for _,c in post_completed)
pre_usage = Usage.aggregate(Usage.model_validate(c["usage"]) for _,c in completed if nodes[c["node"]]["timestamp"] <= ready_t)

def bucket(u):
    out = u.model_dump(exclude_none=True)
    out.update(input_tokens=u.input_tokens, total_tokens=u.total_tokens)
    return out

def ref(r):
    return dict(node=r["node"], model_call_index=r["model_call_index"], tool_call_id=r["tool_call_id"],
                timestamp_utc=utc(r["timestamp"]), result_node=r["result_node"])

bytool = {}
for r in rows:
    d = bytool.setdefault(r["tool"], dict(calls=0, outcomes={}))
    d["calls"] += 1
    d["outcomes"][r["outcome"]] = d["outcomes"].get(r["outcome"], 0) + 1
    if r["persisted_output"]:
        d["persisted_outputs"] = d.get("persisted_outputs", 0) + 1
        d["persisted_outputs_recovered"] = d.get("persisted_outputs_recovered", 0) + int(r["persisted_recovered"])

forks = [r for r in probe if r["tool"] == "mcp__probe__fork" and r["outcome"] == "success_response"]
resets = [r for r in probe if r["tool"] == "mcp__probe__reset" and r["outcome"] == "success_response"]
fid_anchors = defaultdict(set)
fid_rows = defaultdict(list)
for r in forks:
    fid = r["result"]["fork"]
    fid_anchors[fid].add(float(r["result"]["anchor_t"]))
    fid_rows[fid].append(r)

def context_key(fid):
    anchors = sorted(fid_anchors.get(fid, set()))
    return ",".join(f"{x:g}" for x in anchors) if len(anchors) <= 1 else "AMBIGUOUS:" + ",".join(f"{x:g}" for x in anchors)

injections = []
adjustments = defaultdict(list)
naive = dict(sensor=0.0, adjust=0.0, injection=0.0, sim_tu=0.0, log_entries=0, reads_base=0, reads_fork=0)
base_frames = []
base_ranges = []
fid_end = defaultdict(list)
for r in probe:
    name = r["tool"].removeprefix("mcp__probe__")
    a, v = r["args"], r["result"]
    if isinstance(v, dict) and isinstance(v.get("t"), (int, float)):
        fid = v.get("ctx", v.get("fork"))
        if fid and fid != "base":
            fid_end[fid].append(float(v["t"]))
    if name == "read" and r["outcome"] == "success_response":
        n = len(v["steps"]) if isinstance(v, dict) else (1 if a.get("window",1) == 0 else a.get("window",1) // a.get("stride",1))
        dev = a.get("devices", "all")
        slots = {"all":32,"0":13,"[0]":13,"1":19,"[1]":19}[dev]
        naive["sensor"] += n * slots * 5
        base = a.get("ctx", "base") == "base"
        naive["reads_base" if base else "reads_fork"] += n
        if not base:
            naive["sim_tu"] += a.get("window",1)*5
            naive["log_entries"] += int(a.get("window",1) > 0)
        else:
            if isinstance(v, dict):
                ts = [float(s["t"]) for s in v["steps"]]
            else:
                match = re.search(r'\\"t\\":\s*([0-9.]+)',v)
                end = float(match[1])
                ts = [end - 5*a.get("stride",1)*(n-1-j) for j in range(n)]
            base_frames.extend(ts)
            base_ranges.append(dict(**ref(r), start=min(ts), end=max(ts), frames=len(ts),
                                    values_available=isinstance(v,dict)))
    elif name == "adjust" and isinstance(v,dict) and "steps_applied" in v:
        applied = v["steps_applied"]
        rejected = v["result"] == "adjust_rejected"
        cost = sum(abs(x) for x in v["applied"]) * (applied + int(rejected))
        naive["adjust"] += cost
        naive["sensor"] += len(v["steps_read"]) * (13 if v["device"]==0 else 19) * 5
        naive["reads_base" if v["ctx"]=="base" else "reads_fork"] += len(v["steps_read"])
        if v["ctx"]!="base":
            naive["sim_tu"] += applied*5
            naive["log_entries"] += int(applied > 0)
        adjustments[v["ctx"]].append(dict(**ref(r), u=v["applied"], device=v["device"], requested_steps=v["steps_requested"],
                                         applied_steps=applied, result=v["result"], response_t=v["t"], adjustment_meter_if_persisted=cost))
    elif name == "wait" and r["outcome"] == "success_response" and v["ctx"] != "base":
        naive["sim_tu"] += a.get("steps",1)*5
        naive["log_entries"] += 1
    elif name == "inject" and r["outcome"] == "success_response":
        amp, dur = v["amp"], v["dur"]
        cost = abs(amp)*(1+4*max(0,abs(amp)-.5))*dur
        naive["injection"] += cost
        naive["log_entries"] += 2
        injections.append(dict(**ref(r), fork=v["ctx"], reported_anchor_set=sorted(fid_anchors[v["ctx"]]),
                               port=v["port"], amp=amp, dur_tu=dur, start_t=v["t"], injection_meter_if_persisted=cost))

inj_group = Counter((context_key(r["fork"]),r["port"],r["amp"],r["dur_tu"]) for r in injections)
adj_groups = []
for fid, seq in adjustments.items():
    adj_groups.append(dict(fork=fid, reported_anchor_set=sorted(fid_anchors[fid]), anchor_ambiguous=len(fid_anchors[fid])!=1, sequence=seq))

anchor_table = []
for anchor in sorted({a for aset in fid_anchors.values() for a in aset}):
    fids = {fid for fid,aset in fid_anchors.items() if anchor in aset}
    acknowledgments = [r for r in forks if float(r["result"]["anchor_t"])==anchor]
    unambig = {fid for fid in fids if len(fid_anchors[fid])==1}
    adj = [s for fid in unambig for s in adjustments.get(fid, [])]
    inj = [r for r in injections if r["fork"] in unambig]
    span = [max(fid_end[fid])-anchor for fid in unambig if fid in fid_end]
    anchor_table.append(dict(anchor_t=anchor, fork_success_responses=len(acknowledgments),
                             distinct_returned_ids=len(fids), ids_with_multiple_reported_anchors=len(fids-unambig),
                             unambiguous_adjustment_responses=len(adj), unambiguous_applied_control_steps=sum(s["applied_steps"] for s in adj),
                             unambiguous_injection_responses=len(inj), largest_unambiguous_observed_elapsed_tu=max(span) if span else 0))

dup_fork_evidence = []
for fid, rr in fid_rows.items():
    if len(rr)>1:
        dup_fork_evidence.append(dict(fork=fid, returned_times=len(rr), reported_anchors=sorted(fid_anchors[fid]),
                                     calls=[dict(**ref(r), requested_anchor=r["args"].get("t"), returned_anchor=r["result"]["anchor_t"]) for r in rr]))

submissions = []
for r in probe:
    if r["tool"]=="mcp__probe__submit":
        v=r["result"]
        payload=json.loads(r["args"]["payload"]) if isinstance(r["args"]["payload"],str) else r["args"]["payload"]
        artifact = workspace.get("app/probe/payload_"+r["args"]["instance"].split("@")[0]+".json")
        submissions.append(dict(**ref(r), instance=r["args"]["instance"], accepted=v.get("ok") is True,
                                accepted_shape=v.get("shape"), exact_match_to_workspace_payload=(json.loads(artifact)==payload) if artifact else None))
assert len(submissions)==6 and all(s["accepted"] for s in submissions)
final_status = next(r for r in reversed(rows) if r["tool"] == "mcp__probe__status" and isinstance(r["result"],dict))
errors=[dict(call_index=i, type=c["error"]["type"], status_code=c["error"].get("status_code"),
             start_utc=utc(c["time"]["start"]),end_utc=utc(c["time"]["end"]),usage_recorded="usage" in c)
        for i,c in enumerate(calls) if "error" in c]
metrics_diff={k: v-phy["meters"][k] for k,v in naive.items()}
status_contexts=[len(r["result"]["contexts"]) for r in probe if r["tool"]=="mcp__probe__status" and isinstance(r["result"],dict)]
summary = dict(
    scope=dict(trace_id=TARGET,episode_id=episode_id,task=tr["task"]["data"]["name"],world=phy["world"],world_seed=phy["world_seed"],
               source=str(SOURCE),source_line=lineno,selected_trace_sha256=hashlib.sha256(json.dumps(tr,sort_keys=True,separators=(",",":")).encode()).hexdigest(),
               source_bytes_at_read=SOURCE.stat().st_size,scope_note="Only this completed fresh-resource instance. Not a cohort mean. No legacy capped results used."),
    completion=dict(is_completed=tr["is_completed"],ok=tr["ok"],stop_condition=tr["stop_condition"],trace_errors=tr["errors"],
                    resource_truncated=phy["resource_truncated"],resource_stop=phy["resource_stop"],cap_hits=phy["cap_hits"],
                    start_utc=utc(tr["timing"]["start"]),scoring_end_utc=utc(tr["timing"]["scoring"]["end"]),
                    elapsed_wall_seconds=tr["timing"]["scoring"]["end"]-tr["timing"]["start"],wall_time_is_not_billing=True),
    accounting=dict(message_graph_nodes=len(nodes),sampled_model_nodes=len(completed),model_request_records=len(calls),completed_model_calls=len(completed),
                    request_errors=len(errors),request_error_types=dict(Counter(e["type"] for e in errors)),finish_reasons=dict(Counter(c["finish_reason"] for _,c in completed)),
                    model_names=dict(Counter(c["model"] for c in calls)),tool_call_occurrences_in_context_graph=sum(len(n["message"].get("tool_calls",[])) for n in nodes),
                    unique_tool_calls=len(rows),recorded_tool_results=len(results),environment_tool_requests=len(probe),environment_persisted_turns=phy["meters"]["turns"],
                    delegated_Agent_invocations=bytool["Agent"]["calls"],all_tool_arguments_valid_json=True,
                    total_usage=usage_dict,through_ready_usage=bucket(pre_usage),after_ready_usage=bucket(post_usage),
                    usage_scope="All completed model calls in this one trace, including delegated branches. Context copies are not counted again.",
                    auxiliary_requests=dict(recorded_extra_usage_entries=len(tr["extra_usage"]),count_tokens_request_count=None,
                                            note="verifiers relays /v1/messages/count_tokens outside model turns and never records it on this trace. extra_usage is judge/off-graph usage, not a count_tokens log."),
                    missing_retry_usage_note="All 23 errored requests lack usage. A connection reset may hide partial generation. No token or dollar amount is imputed.",
                    request_errors_detail=errors),
    tools=bytool,
    resources=dict(policy=phy["resource_policy"],persisted_meters=phy["meters"],resident_cache=phy["resident_cache"],time_to_ready=phy["time_to_ready"],
                   read_meter_units="Number of read frames; each may contain several ports/devices. Not tool-call counts.",
                   sensor_units="5 tu times selected sensor-slot count per read frame; independent of number of ports. Global statistics are free.",
                   adjustment_units="sum(abs(u)) times accepted steps plus the first rejected step, if any.",
                   injection_units="abs(amp) * (1 + 4*max(0,abs(amp)-0.5)) * dur; not dollars.",
                   sim_units="Live control advancement only. Base record reads and cache rebuild/replay work do not add sim_tu.",
                   rebuild_note="168 counts cold reconstruction, including initial construction at spawn; not necessarily 168 evicted-fork reloads. Evictions and rebuilds do not by themselves close logical handles.",
                   observed_status_peak_contexts=max(status_contexts),
                   observed_reply_naive_meter_sums=naive,observed_reply_minus_persisted_meters=metrics_diff,
                   reconciliation_note="Reply-derived sums are NOT actual meters. Concurrent/state anomalies and timeouts prevent exact per-operation reconstruction from this trace. Final persisted meters are the reported environment accounting, not proof all server work is billed there.",
                   fork_success_responses=len(forks),unique_returned_fork_ids=len(fid_rows),fork_ids_returned_multiple_times=sum(len(rr)>1 for rr in fid_rows.values()),
                   fork_ids_with_multiple_reported_anchors=sum(len(a)>1 for a in fid_anchors.values()),
                   reset_success_responses=len(resets),unique_successfully_reset_ids=len({r["result"]["fork"] for r in resets}),
                   successful_or_error_reply_requests=len(probe)-sum(r["outcome"] in {"tool_timeout","no_result_recorded"} for r in probe),
                   successful_or_error_reply_minus_persisted_turns=len(probe)-sum(r["outcome"] in {"tool_timeout","no_result_recorded"} for r in probe)-phy["meters"]["turns"]),
    ready_and_submission=dict(ready=ref(ready),ready_model_call_end_utc=utc(calls[ready["model_call_index"]]["time"]["end"]),
                              first_post_reveal_model_request_start_utc=utc(calls[ready["model_call_index"]+1]["time"]["start"]),
                              node_timestamp_note="Tool-use node time is the sampled model response time. Tool-result node time may be when the next model response is recorded, not actual tool execution time.",
                              post_ready_tool_counts=dict(Counter(r["tool"] for r in post)),post_ready_completed_model_calls=len(post_completed),
                              post_ready_request_errors=sum(c["time"]["start"]>ready_t for c in calls if "error" in c),
                              world_tool_requests_after_ready=[ref(r) for r in post if r["tool"] in {"mcp__probe__read","mcp__probe__wait","mcp__probe__adjust","mcp__probe__fork","mcp__probe__inject","mcp__probe__reset"}],
                              submissions=submissions,final_status=ref(final_status),all_submitted_flags=final_status["result"].get("submitted"),
                              final_status_open_contexts=final_status["result"].get("contexts")),
    experiments=dict(all_successful_fork_sources="base anchors; no fork-from-fork calls",reported_anchor_count=len(anchor_table),
                     base_record=dict(successful_read_responses=len(base_ranges),reported_frames=len(base_frames),distinct_grid_times=len(set(base_frames)),min_t=min(base_frames),max_t=max(base_frames),
                                      repeated_grid_times={str(k):v for k,v in Counter(base_frames).items() if v>1},
                                      persisted_output_responses=sum(r["persisted_output"] for r in rows),full_persisted_outputs_in_workspace=sum(r["persisted_recovered"] for r in rows),
                                      preview_only_base_chunks=sum(r["persisted_output"] and not r["persisted_recovered"] for r in rows),
                                      note="13 base chunks have only response previews in this audit; frame spans/counts use their request and reported end time. Agent-saved full binary/text datasets are not all embedded."),
                     per_reported_anchor=anchor_table,
                     injection_protocol_counts=[dict(anchor_label=k[0],port=k[1],amp=k[2],dur_tu=k[3],success_responses=v) for k,v in sorted(inj_group.items())],
                     accepted_injection_responses=injections,
                     adjustment_sequences=adj_groups,
                     duplicate_fork_response_evidence=dup_fork_evidence),
    scores=dict(instance_reward=tr["rewards"],instance_detail=phy["detail"],scope="Raw per-instance metrics for this one world/seed. Not a cohort mean or proof of learned dynamics."),
    artifact_availability=dict(embedded_artifact_count=len(workspace),embedded_files=[dict(path=p,bytes=len(v.encode()) if isinstance(v,str) else None) for p,v in workspace.items()],
                               unavailable_note="The workspace snapshot includes final predictors/models/payloads and four persisted read outputs, but not all captured JSONL/NPZ datasets. No trace code, simulations or payload generators were rerun."),
    evidence_sources=dict(usage_definition=".venv/lib/python3.13/site-packages/verifiers/v1/types.py:107-167",
                          anthropic_usage=".venv/lib/python3.13/site-packages/verifiers/v1/dialects/anthropic.py:146-160",
                          auxiliary_semantics=".venv/lib/python3.13/site-packages/verifiers/v1/dialects/anthropic.py:1-6,273; v1/dialects/base.py:113-115; v1/interception/server.py:705-729",
                          environment_meter_code="environments/physim/physim/servers/blob.py:565-647,718-811,828-886,902-966",
                          injection_price="environments/physim/physim/blobcore.py:146-149",
                          source_caveat="Definitions inspected in the current installed/project code. No claim that every line is an immutable historical source snapshot.")
)
OUT.mkdir(parents=True,exist_ok=True)
register_keys = ("per_reported_anchor", "injection_protocol_counts", "accepted_injection_responses", "adjustment_sequences", "duplicate_fork_response_evidence")
register = {k: summary["experiments"].pop(k) for k in register_keys}
register["trace_id"] = TARGET
register["interpretation"] = "Bounded call/response register, not an authoritative committed state history; no raw sensor arrays."
summary["experiments"]["detailed_register"] = "experiment_register.json"
summary["experiments"]["readable_protocol_tables"] = "EXPERIMENTS.md"
summary["resources"]["matched_state_anomaly_evidence"] = "CONCURRENCY.md"
summary["accounting"]["reasoning_note"] = "The Anthropic adapter labels reasoning_tokens a re-tokenized raw-thinking estimate inside completion_tokens, not visible-summary tokens or an extra total bucket."
summary["accounting"]["retry_chains"] = None
summary["accounting"]["retry_note"] = "No retry_of metadata. Error request records and repeated success replies are counted separately; identical read/fork arguments may be intentional experiments."
summary["scores"]["instance_skills_full_precision"] = {k: v for k, v in tr["metrics"].items() if k.startswith("skill_")}
summary["ready_and_submission"]["offline_path_review"] = "All ten post-ready Bash commands inspect local files or run the saved offline predictor/builder. No world/network client appears in these commands or their embedded prediction path."
summary["reports"] = {"main": "REPORT.md", "timeline": "TIMELINE.md", "state_anomalies": "CONCURRENCY.md", "experiments": "EXPERIMENTS.md", "science": "SCIENTIFIC_PROCESS.md"}
summary["recommendations"] = {
    "status": "Recommendations only; no new budgets or live changes imposed in this audit.",
    "next_native_test_recipe": "NEXT_NATIVE_TEST.md (not executed)",
    "test_ladder": [
        "Deterministic native transport/lifecycle/scripted controls, including concurrent mutations across different contexts sharing rollout state, dependencies, argument formats, artifact persistence, phase gates and six submissions.",
        "One short cheap-model wiring smoke, diagnostic only, with diagnostic allowance separate from scientific exploration freedom.",
        "One full frontier pilot with normal scientific freedom and process/integrity review.",
        "Predeclare a limited seed/world set, with within-record versus out-of-record and weak versus active-emission controls.",
        "Broaden to a balanced model panel only after stable transport/protocol behavior."],
    "cheap_first_limit": "A cheap model can fail valid tools or miss long-context/parallel stress. A pass is not a scientific performance result, and a failure is not proof the environment is invalid."}
science_path = OUT/"scientific_summary.json"
if science_path.exists():
    science = json.loads(science_path.read_text())
    assert science["trace_id"] == TARGET
    summary["scientific_process"] = {
        "detail": "scientific_summary.json",
        "main_findings": science["top_findings"],
        "actual_methods": {k: v["method"] for k,v in science["instances"].items()},
        "limitation": "Most bulk fit/capture inputs are absent. Source/action/payload comparisons were inspected, not regenerated by running the episode code."}
(OUT/"experiment_register.json").write_text(json.dumps(register,indent=2)+"\n")
(OUT/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")

md=["# Experiment accounting — one completed run", "", "Trace `"+TARGET+"`; task `physim-BLOB2v2r2-E1#928`.","",
    "## Scope and interpretation", "",
    "These tables describe calls and replies, not a clean randomized trial register. The trace has repeated fork IDs, unknown-context errors, and timeouts. A successful response does not prove its state change survived in the final state. The final environment meters are listed separately in REPORT.md and summary.json.","",
    "- 183 fork requests: 181 success-shaped replies, 2 timeouts, 145 distinct returned IDs. All sources were base anchors; none were nested forks.",
    "- 62 reported anchor times. An ID reused at multiple anchors is marked ambiguous. IDs can therefore occur in more than one anchor row.",
    "- 102 adjustment responses carry applied-step information: 99 fully accepted, 2 partly applied then refused, 1 refused at the first step. 9 other calls return unknown-context errors; 1 times out.",
    "- 46 injection acknowledgments: amplitude 0.05–1.0; duration 5–20 tu. 18 other injections return unknown-context errors; 3 time out. No out-of-range emission was acknowledged.",
    "- Base coverage: 58 success-shaped read responses, 505 reported frames but 500 distinct grid times, t=5..2500. Repeated t=165 (4 replies), 220 (2), 245 (2). The extra frames are not five extra base-time steps.",
    "- Long unambiguous reported continuations include t=600→2500 (1900 tu, global-stat sweep) and t=2500→3105 (605 tu). No per-fork duration stop is recorded.","",
    "## Injection protocols with success-shaped responses", "",
    "An anchor label with `AMBIGUOUS` lists every anchor reported for that fork ID. It does not identify which underlying state produced the response.","",
    "| Reported anchor(s) | Port | Amplitude | Duration (tu) | Replies |", "|---|---:|---:|---:|---:|"]
for (a,p,amp,dur), count in sorted(inj_group.items()):
    md.append(f"| {a} | {p} | {amp:g} | {dur:g} | {count} |")
md += ["", "## Per-anchor summary", "",
       "Adjustment/injection columns include only IDs with one reported anchor. `Elapsed` is the largest observed response time minus that anchor, not a reconstructed physical history.","",
       "| Anchor | Fork replies / IDs | Multi-anchor IDs | Adjust replies / applied steps | Injection replies | Elapsed (tu) |",
       "|---:|---:|---:|---:|---:|---:|"]
for a in anchor_table:
    md.append(f"| {a['anchor_t']:g} | {a['fork_success_responses']} / {a['distinct_returned_ids']} | {a['ids_with_multiple_reported_anchors']} | {a['unambiguous_adjustment_responses']} / {a['unambiguous_applied_control_steps']} | {a['unambiguous_injection_responses']} | {a['largest_unambiguous_observed_elapsed_tu']:g} |")
md += ["", "## Adjustment sequence register", "",
       "`experiment_register.json → adjustment_sequences` preserves all 102 response-bearing commands, grouped by fork ID and ordered by sampled tool-call time. Each entry gives the exact u vector, device, requested/applied step counts, result, node, model-call index, tool-call ID and UTC timestamp. Multi-anchor IDs are explicitly flagged. These commands are observations of replies, not proof of an unbroken accepted state trajectory.","",
       "Initial range tests at anchor 600 include single-axis ±1 commands, five fully accepted 10-step blocks, one 50-step block, a u3=+1 request accepting 1/10 steps, u3=-1 accepting 0/10, and u3=+0.5 accepting 2/3. Later trials use continuous mixed commands and short sequences. The scientific notes explain the fitted artifact and which branch was used after reveal.","",
       "## Reconciliation", "",
       "| Meter | Naive successful-reply sum | Persisted final meter | Difference |", "|---|---:|---:|---:|"]
for k,v in naive.items():
    md.append(f"| {k} | {v:g} | {phy['meters'][k]:g} | {v-phy['meters'][k]:+g} |")
md += ["", "The reply tally gives 150 reset acknowledgments (140 distinct IDs), versus 133 persisted resets. All non-timeout/non-missing environment replies total 1009, versus 891 persisted environment turns. The trace does not preserve the authoritative per-operation commit history needed to allocate these gaps. Do not add the naive totals to the meters.", ""]
(OUT/"EXPERIMENTS.md").write_text("\n".join(md))
print(json.dumps(dict(trace=TARGET,completed_model_calls=len(completed),usage=usage_dict,tools=len(rows),environment_calls=len(probe),summary_bytes=(OUT/"summary.json").stat().st_size),indent=2))
