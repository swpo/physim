"""Static read-only audit of E2 #942. Never executes trace code, a world tool, or a predictor.
Run from repository root with .venv/bin/python <this file>.
"""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import inspect
import json
import re
from verifiers.v1.types import Usage

ROOT = Path.cwd()
OUT = ROOT / "probes/blobs/agentenv/round5/resource_revision/e2_942_process_audit"
SOURCE = Path.home() / "v3work/ops/recovery_20260905/eval_fable_r2/E2/traces.jsonl"
TARGET = "ae982494a72144c186f58a687a99cd33"
TASK = "physim-BLOB2v2r2-E2#942"
WORLD_TOOLS = {"mcp__probe__" + n for n in ("read", "wait", "adjust", "fork", "inject", "reset")}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def utc(t):
    return datetime.fromtimestamp(t, timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z") if t is not None else None


def decode(value):
    for _ in range(8):
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


def select_trace():
    raw = SOURCE.read_bytes()
    found = []
    for line_no, line in enumerate(raw.splitlines(), 1):
        if TARGET.encode() not in line:
            continue
        outer = json.loads(line)
        for trace in outer.get("traces", []):
            if trace.get("id") == TARGET:
                found.append((line_no, outer.get("id"), outer.get("ok"), trace))
    assert len(found) == 1, f"Expected one exact nested trace; found {len(found)}"
    line_no, episode, outer_ok, trace = found[0]
    assert trace["task"]["data"]["name"] == TASK
    return trace, dict(source=str(SOURCE), source_line=line_no, episode_id=episode,
                       source_sha256_at_read=sha(raw), source_bytes_at_read=len(raw),
                       selected_trace_sha256=sha(canonical(trace)), outer_ok=outer_ok)


def parse_rows(trace):
    nodes, calls = trace["nodes"], trace["calls"]
    workspace = trace["info"]["physim"].get("workspace", {})
    completed = [(i, c) for i, c in enumerate(calls) if "node" in c]
    completed_nodes = [c["node"] for _, c in completed]
    assert len(completed_nodes) == len(set(completed_nodes))
    assert set(completed_nodes) == {i for i, n in enumerate(nodes) if n.get("sampled")}
    results = {}
    result_occurrences = defaultdict(list)
    for ni, n in enumerate(nodes):
        if n["message"]["role"] == "tool":
            tid = n["message"]["tool_call_id"]
            result_occurrences[tid].append(ni)
            if tid in results:
                assert n["message"] == results[tid][1]["message"], f"Conflicting result copies for {tid}"
            else:
                results[tid] = (ni, n)  # first original; later graph copies are not invocations
    rows, seen = [], set()
    for ci, call in completed:
        ni = call["node"]
        for tool in nodes[ni]["message"].get("tool_calls", []):
            assert tool["id"] not in seen
            seen.add(tool["id"])
            rr = results.get(tool["id"])
            row = dict(node=ni, model_call_index=ci, tool_call_id=tool["id"], tool=tool["name"],
                       timestamp=nodes[ni].get("timestamp"), args=json.loads(tool["arguments"]),
                       result_node=rr[0] if rr else None,
                       result_node_occurrences=result_occurrences.get(tool["id"], []),
                       result_timestamp=rr[1].get("timestamp") if rr else None,
                       result=decode(rr[1]["message"].get("content")) if rr else None,
                       persisted_output=False, persisted_recovered=False)
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
                err = str(r["error"])
                outcome = "unknown_context" if err.startswith("unknown context") else "malformed_argument" if err.startswith("ports must") else "other_error"
            elif isinstance(r, dict) and r.get("result") == "adjust_rejected":
                outcome = "partial_adjustment_then_refused" if r["steps_applied"] else "adjustment_refused"
            elif isinstance(r, str) and re.match(r"Exit code [1-9][0-9]*", r):
                outcome = "nonzero_shell_exit"
            elif isinstance(r, str) and "SyntaxError:" in r and row["tool"] == "Bash":
                outcome = "returned_with_embedded_code_error"
            elif isinstance(r, str) and (r.startswith("<tool_use_error>") or r.startswith("InputValidationError:")):
                outcome = "tool_error_text"
            else:
                outcome = "success_response" if row["tool"].startswith("mcp__probe__") else "returned_without_explicit_error"
            row["outcome"] = outcome
            rows.append(row)
    rows.sort(key=lambda r: (r["timestamp"], r["node"], r["tool_call_id"]))
    return rows, results, completed


def ref(row):
    return dict(node=row["node"], model_call_index=row["model_call_index"], tool_call_id=row["tool_call_id"],
                timestamp_utc=utc(row["timestamp"]), result_node=row["result_node"])


def usage_bucket(calls):
    records = [Usage.model_validate(c["usage"]) for _, c in calls if c.get("usage")]
    u = Usage.aggregate(records)
    if u is None:
        return None
    d = u.model_dump(exclude_none=True)
    d.update(input_tokens=u.input_tokens, total_tokens=u.total_tokens,
             usage_records=len(records), missing_usage_records=len(calls) - len(records))
    return d


def main():
    trace, scope = select_trace()
    phy = trace["info"]["physim"]
    workspace = phy.get("workspace", {})
    nodes, calls = trace["nodes"], trace["calls"]
    rows, results, completed = parse_rows(trace)
    probe = [r for r in rows if r["tool"].startswith("mcp__probe__")]
    ready_rows = [r for r in rows if r["tool"] == "mcp__probe__ready"]
    assert len(ready_rows) == 1
    ready = ready_rows[0]
    ready_t = ready["timestamp"]
    post = [r for r in rows if r["timestamp"] > ready_t]
    post_completed = [(i, c) for i, c in completed if nodes[c["node"]]["timestamp"] > ready_t]
    through_ready = [(i, c) for i, c in completed if nodes[c["node"]]["timestamp"] <= ready_t]
    error_calls = [(i, c) for i, c in enumerate(calls) if "error" in c]
    assert len(completed) + len(error_calls) == len(calls)
    errors = [dict(call_index=i, type=c["error"]["type"], status_code=c["error"].get("status_code"),
                   provider_code="content_policy_violation" if "content_policy_violation" in c["error"].get("message", "") else "rate_limited" if "rate_limited" in c["error"].get("message", "") else None,
                   start_utc=utc(c["time"]["start"]), end_utc=utc(c["time"]["end"]),
                   usage_recorded=c.get("usage") is not None,
                   retry_metadata_keys=[k for k in c if "retry" in k.lower()]) for i, c in error_calls]
    bytool = {}
    for r in rows:
        d = bytool.setdefault(r["tool"], dict(calls=0, outcomes={}))
        d["calls"] += 1
        d["outcomes"][r["outcome"]] = d["outcomes"].get(r["outcome"], 0) + 1
        if r["persisted_output"]:
            d["persisted_outputs"] = d.get("persisted_outputs", 0) + 1
            d["persisted_outputs_recovered"] = d.get("persisted_outputs_recovered", 0) + int(r["persisted_recovered"])
    payload_artifacts = {}
    for path, content in workspace.items():
        if path.startswith("app/models/sub_") and path.endswith(".json"):
            payload_artifacts[path] = json.loads(content)
    submissions = []
    for r in rows:
        if r["tool"] != "mcp__probe__submit":
            continue
        payload = json.loads(r["args"]["payload"]) if isinstance(r["args"]["payload"], str) else r["args"]["payload"]
        matches = [p for p, artifact in payload_artifacts.items() if artifact == payload]
        submissions.append(dict(**ref(r), instance=r["args"]["instance"], accepted=isinstance(r["result"], dict) and r["result"].get("ok") is True,
                                accepted_shape=r["result"].get("shape") if isinstance(r["result"], dict) else None,
                                matching_workspace_payloads=matches, payload_object_sha256=sha(canonical(payload))))
    statuses = [r for r in rows if r["tool"] == "mcp__probe__status" and isinstance(r["result"], dict) and "phase" in r["result"]]
    final_status = statuses[-1]
    after_issued_before_ready_results = [r for r in rows if r["timestamp"] < ready_t and r["result_timestamp"] is not None and r["result_timestamp"] > ready_t]
    usage = usage_bucket(completed)
    usage.update(cache_write_tokens=None, provider_uncached_input_excluding_cache_writes=None, billed_dollars=None,
                 interpretation="prompt_tokens excludes cache reads and includes Anthropic cache creation; reasoning is a subset of completion. No price or retry usage is imputed.")
    timing = trace["timing"]
    scope.update(trace_id=TARGET, task=TASK, world=phy["world"], world_seed=phy["world_seed"],
                 selection="Exact nested trace ID and exact task assertion; excludes canceled E2 #943, E1 #929 error, diagnostics and all other cohorts.",
                 source_sha256_after_counting=sha(SOURCE.read_bytes()))
    assert scope["source_sha256_at_read"] == scope["source_sha256_after_counting"]
    scope["source_unchanged_during_counting"] = True
    schema_files = [ROOT/".venv/lib/python3.13/site-packages/verifiers/v1/types.py", ROOT/".venv/lib/python3.13/site-packages/verifiers/v1/dialects/anthropic.py"]
    summary = dict(
        scope=scope,
        completion=dict(is_completed=trace["is_completed"], ok=trace["ok"], stop_condition=trace["stop_condition"],
                        trace_errors=trace["errors"], score_status=phy["score_status"], readied_metric=trace["metrics"].get("readied"),
                        resource_policy=phy["resource_policy"], resource_truncated=phy["resource_truncated"], resource_stop=phy["resource_stop"], cap_hits=phy["cap_hits"],
                        start_utc=utc(timing["start"]), scoring_end_utc=utc(timing["scoring"]["end"]),
                        elapsed_wall_seconds=timing["scoring"]["end"]-timing["start"], wall_time_is_not_billing=True),
        accounting=dict(message_graph_nodes=len(nodes), sampled_model_nodes=len(completed), model_request_records=len(calls), completed_model_calls=len(completed),
                        completed_with_usage=sum(c.get("usage") is not None for _, c in completed), request_errors=len(errors),
                        request_error_types=dict(Counter(e["type"] for e in errors)), request_error_status_codes=dict(Counter(str(e["status_code"]) for e in errors)),
                        request_errors_with_usage=sum(e["usage_recorded"] for e in errors),
                        request_error_provider_codes=dict(Counter(e["provider_code"] for e in errors)),
                        reported_usage_field_coverage=dict(Counter(k for _,c in completed for k,v in c.get("usage",{}).items() if v is not None)),
                        missing_finish_reason_call_indices=[i for i,c in completed if c.get("finish_reason") is None],
                        empty_completed_response_call_indices=[i for i,c in completed if not nodes[c["node"]]["message"].get("content") and not nodes[c["node"]]["message"].get("tool_calls")],
                        finish_reasons=dict(Counter(str(c.get("finish_reason")) for _,c in completed)),
                        model_names=dict(Counter(c["model"] for c in calls)), tool_call_occurrences_in_context_graph=sum(len(n["message"].get("tool_calls", [])) for n in nodes),
                        unique_tool_calls=len(rows), recorded_tool_results=len(results),
                        tool_result_graph_nodes=sum(n["message"]["role"] == "tool" for n in nodes),
                        repeated_result_ids=sum(len(r["result_node_occurrences"]) > 1 for r in rows),
                        duplicate_result_copies=sum(max(0, len(r["result_node_occurrences"])-1) for r in rows),
                        repeated_result_contents_identical=True,
                        result_ids_not_in_sampled_tool_calls=len(set(results)-{r["tool_call_id"] for r in rows}),
                        environment_tool_requests=len(probe), environment_persisted_turns=phy["meters"]["turns"],
                        delegated_Agent_invocations=bytool.get("Agent", {}).get("calls", 0), all_tool_arguments_valid_json=True,
                        total_usage=usage, through_ready_usage=usage_bucket(through_ready), after_ready_usage=usage_bucket(post_completed),
                        usage_scope="All completed calls in this one trace, including delegated branches; deduplicated sampled call/node/tool IDs, not context occurrences.",
                        auxiliary_requests=dict(recorded_extra_usage_entries=len(trace["extra_usage"]), count_tokens_requests=None,
                                                note="extra_usage is judge/off-graph usage, not an auxiliary-request log. Anthropic count_tokens requests are relayed, never recorded here."),
                        error_usage_note="Error attempts without recorded usage have unknown token consumption; no partial output, retry tokens or billing is imputed.",
                        known_retry_chains=None,
                        retry_note="No retry_of metadata links attempts to successful completions. Repeated error attempts are not a known count of retry chains; repeated tool calls may be intentional experiments.",
                        reasoning_note="Anthropic adapter labels reasoning_tokens a re-tokenized raw-thinking estimate within completion, not an additional output bucket."),
        tools=bytool,
        resources=dict(policy=phy["resource_policy"], persisted_meters=phy["meters"], resident_cache=phy["resident_cache"], time_to_ready=phy["time_to_ready"],
                       observed_status_peak_contexts=max(len(r["result"].get("contexts", [])) for r in statuses),
                       state_analysis="experiment_summary.json and CONCURRENCY.md (independent E2 response analysis)"),
        ready_and_submission=dict(ready=ref(ready), ready_result_node=ready["result_node"],
                                  ready_model_call_end_utc=utc(calls[ready["model_call_index"]]["time"]["end"]),
                                  ready_result_graph_timestamp_utc=utc(ready["result_timestamp"]),
                                  node_timestamp_note="Tool-use node time is the sampled response time; a tool-result node may be recorded at the next model response rather than at server completion. Node order is not a native transaction log.",
                                  post_ready_tool_counts=dict(Counter(r["tool"] for r in post)), post_ready_completed_model_calls=len(post_completed),
                                  post_ready_request_errors=sum(c["time"]["start"]>ready_t for _,c in error_calls),
                                  world_tool_requests_after_ready=[ref(r) for r in post if r["tool"] in WORLD_TOOLS],
                                  pre_ready_tool_requests_with_later_recorded_results=[dict(**ref(r),tool=r["tool"], result_timestamp_utc=utc(r["result_timestamp"])) for r in after_issued_before_ready_results],
                                  submissions=submissions, final_status=ref(final_status),
                                  final_status_resource_note="Status exposes phase/head/context/submission state, not meters. Resource totals and time-to-ready meters come from final trace info.physim.", all_submitted_flags=final_status["result"].get("submitted"),
                                  final_status_open_contexts=final_status["result"].get("contexts")),
        scores=dict(instance_reward=trace["rewards"], instance_detail=phy["detail"],
                    instance_skills_full_precision={k:v for k,v in trace["metrics"].items() if k.startswith("skill_")},
                    scope="One completed E2 world/seed, not a cohort mean, paired performance estimate, or proof of learned dynamics."),
        artifact_availability=dict(embedded_artifact_count=len(workspace),
                                   embedded_files=[dict(path=p, bytes=len(v.encode()) if isinstance(v,str) else None, sha256=sha(v.encode()) if isinstance(v,str) else None) for p,v in workspace.items()],
                                   caveat="Artifact snapshot is selective. No full predictor regeneration, trace code execution, simulation or world query was performed."),
        evidence_sources=dict(usage_definition=".venv/lib/python3.13/site-packages/verifiers/v1/types.py:107-167",
                              anthropic_usage=".venv/lib/python3.13/site-packages/verifiers/v1/dialects/anthropic.py:146-160",
                              auxiliary_semantics=".venv/lib/python3.13/site-packages/verifiers/v1/dialects/anthropic.py:1-6,273",
                              inspected_source_hashes={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in schema_files},
                              source_caveat="Current installed definitions were inspected. No claim that source lines are immutable historical snapshots."),
        reports=dict(main="REPORT.md", timeline="TIMELINE.md", science="SCIENTIFIC_PROCESS.md", states="CONCURRENCY.md", experiments="EXPERIMENTS.md", paired="POST11_PAIR_NOTES.md")
    )
    evidence = dict(trace_id=TARGET, request_errors=errors,
                    ready=dict(**ref(ready),result=ready["result"]),
                    post_ready_calls=[dict(**ref(r),tool=r["tool"],outcome=r["outcome"]) for r in post],
                    missing_tool_results=[dict(**ref(r), tool=r["tool"]) for r in rows if r["result_node"] is None],
                    copied_tool_results=[dict(**ref(r),tool=r["tool"],result_node_occurrences=r["result_node_occurrences"],identical_content=True) for r in rows if len(r["result_node_occurrences"])>1],
                    response_calls_with_missing_finish_reason=[dict(call_index=i,node=c["node"],usage=c["usage"],tool_call_ids=[x["id"] for x in nodes[c["node"]]["message"].get("tool_calls",[])]) for i,c in completed if c.get("finish_reason") is None],
                    persisted_outputs=[dict(**ref(r),tool=r["tool"],path=r.get("persisted_path"), recovered=r["persisted_recovered"]) for r in rows if r["persisted_output"]],
                    counted_invocation_identity="Unique tool IDs on sampled nodes referenced once by completed model calls. No raw sensor arrays or full model context copied.")
    state_path = OUT / "experiment_summary.json"
    if state_path.exists():
        state = json.loads(state_path.read_text())
        assert state["scope"]["trace_id"] == TARGET
        summary["resources"].update(
            observed_reply_naive_meter_sums=state["reply_accounting"]["sums"],
            observed_reply_minus_persisted_meters=state["reply_accounting"]["reply_minus_persisted"],
            reply_meter_note=state["reply_accounting"]["note"],
            fork_success_responses=state["handles"]["successful_fork_replies"],
            unique_returned_fork_ids=state["handles"]["unique_returned_ids"],
            fork_ids_returned_multiple_times=state["handles"]["fork_ids_returned_more_than_once"],
            fork_ids_with_multiple_reported_anchors=state["handles"]["fork_ids_with_multiple_anchor_times"],
            final_logical_context_count=len(final_status["result"]["contexts"]),
            final_resident_count=state["persisted_state"]["final_resident_count"],
            final_resident_count_note=state["persisted_state"]["final_resident_count_note"])
        summary["experiments"] = dict(
            reported_anchor_count=len(state["anchors"]),
            fork_from_fork_issued=state["handles"]["fork_from_fork_issued"],
            base_record={k:v for k,v in state["base_record"].items() if k != "read_ranges"},
            detailed_protocols="experiment_summary.json#/anchors,/injection_protocol_groups,/adjustment_protocol_groups")
    summary["evidence_sources"]["extra_usage_definition"] = ".venv/lib/python3.13/site-packages/verifiers/v1/trace.py:349-350"
    summary["evidence_sources"]["auxiliary_semantics"] += "; v1/dialects/base.py:113-115; v1/interception/server.py:703-727"
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/"summary.json").write_text(json.dumps(summary, indent=2)+"\n")
    (OUT/"accounting_evidence.json").write_text(json.dumps(evidence, indent=2)+"\n")
    print(json.dumps({"trace_id":TARGET, "source_sha256":scope["source_sha256_at_read"], "completed_model_calls":len(completed),
                      "errors":len(errors), "unique_tools":len(rows), "environment_requests":len(probe), "usage":usage,
                      "tools":bytool, "ready":ref(ready), "post_ready":summary["ready_and_submission"]}, indent=2))


if __name__ == "__main__":
    main()
