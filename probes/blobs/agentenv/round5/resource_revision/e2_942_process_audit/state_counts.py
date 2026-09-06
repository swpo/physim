"""Read-only state/experiment accounting for one exact completed E2 trace.
Run from repository root: .venv/bin/python probes/blobs/agentenv/round5/resource_revision/e2_942_process_audit/state_counts.py
Uses only stdlib. Does not execute trace code, project world tools, or predictors.
Only output is experiment_summary.json beside this script.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import math
import re

SOURCE = Path.home() / "v3work/ops/recovery_20260905/eval_fable_r2/E2/traces.jsonl"
TARGET = "ae982494a72144c186f58a687a99cd33"
TASK = "physim-BLOB2v2r2-E2#942"
OUT = Path(__file__).resolve().parent
WORLD = {"read", "wait", "adjust", "fork", "inject", "reset"}
TOOLS = ("read", "fork", "reset", "adjust", "inject", "wait", "status", "ready", "submit")
SLOTS = {0: 13, 1: 19}
STEP = 5.0


def utc(value):
    return datetime.fromtimestamp(value, timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z") if value is not None else None


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


def load():
    found = []
    raw = SOURCE.read_bytes()
    for line_no, line in enumerate(raw.splitlines(), 1):
        if TARGET.encode() not in line:
            continue
        outer = json.loads(line)
        for trace in outer.get("traces", []):
            if trace.get("id") == TARGET:
                found.append((trace, line_no, outer.get("id")))
    assert len(found) == 1
    trace, line_no, episode_id = found[0]
    assert trace["task"]["data"]["name"] == TASK
    scope = dict(source=str(SOURCE), source_line=line_no, trace_id=TARGET, task=TASK,
                 episode_id=episode_id, source_sha256=hashlib.sha256(raw).hexdigest(),
                 selected_trace_sha256=hashlib.sha256(json.dumps(trace, sort_keys=True, separators=(",", ":")).encode()).hexdigest())
    nodes, calls = trace["nodes"], trace["calls"]
    workspace = trace["info"]["physim"].get("workspace", {})
    completed = [(ci, c) for ci, c in enumerate(calls) if "node" in c]
    sampled = [c["node"] for _, c in completed]
    assert len(sampled) == len(set(sampled))
    assert set(sampled) == {ni for ni, n in enumerate(nodes) if n.get("sampled")}
    result_nodes = defaultdict(list)
    for ni, n in enumerate(nodes):
        if n["message"]["role"] == "tool":
            result_nodes[n["message"]["tool_call_id"]].append(ni)
    for tid, nn in result_nodes.items():
        assert all(nodes[n]["message"] == nodes[nn[0]]["message"] for n in nn), tid
    rows, seen = [], set()
    for ci, c in completed:
        ni = c["node"]
        for ordinal, tool in enumerate(nodes[ni]["message"].get("tool_calls", [])):
            tid = tool["id"]
            assert tid not in seen
            seen.add(tid)
            rn = result_nodes[tid][0] if tid in result_nodes else None
            value = decode(nodes[rn]["message"].get("content")) if rn is not None else None
            row = dict(node=ni, model_call=ci, ordinal=ordinal, id=tid, tool=tool["name"],
                       kind=tool["name"].removeprefix("mcp__probe__"), args=json.loads(tool["arguments"]),
                       timestamp=nodes[ni].get("timestamp"), result_node=rn,
                       result_timestamp=nodes[rn].get("timestamp") if rn is not None else None,
                       result_nodes=result_nodes.get(tid, []), value=value,
                       preview_only=False, recovered_persisted=False)
            if isinstance(value, str) and value.startswith("<persisted-output>"):
                match = re.search(r"Full output saved to: (\S+)", value)
                path = "app/" + match[1] if match else None
                row["persisted_path"] = path
                if path in workspace:
                    row["value"] = value = decode(workspace[path])
                    row["recovered_persisted"] = True
                else:
                    row["preview_only"] = True
            if value is None:
                outcome = "no_result_recorded"
            elif value == "The operation timed out.":
                outcome = "tool_timeout"
            elif isinstance(value, dict) and "error" in value:
                text = str(value["error"])
                outcome = "unknown_context" if text.startswith("unknown context") else "argument_error" if text.startswith("ports must") else "explicit_error"
            elif isinstance(value, dict) and value.get("result") == "adjust_rejected":
                outcome = "partial_adjustment_then_refused" if value["steps_applied"] else "adjustment_refused"
            elif isinstance(value, str) and (value.startswith("<tool_use_error>") or value.startswith("InputValidationError:")):
                outcome = "tool_error_text"
            else:
                outcome = "success_response"
            row["outcome"] = outcome
            rows.append(row)
    rows.sort(key=lambda r: (r["timestamp"], r["node"], r["ordinal"]))
    return trace, scope, rows, result_nodes, completed


def ref(row):
    return dict(node=row["node"], tool_id=row["id"], result_node=row["result_node"])


def timed_ref(row):
    return dict(**ref(row), model_call=row["model_call"], sampled_node_utc=utc(row["timestamp"]),
                result_node_utc=utc(row["result_timestamp"]))


def devices(value):
    if value in ("all", "", None):
        return [0, 1]
    if isinstance(value, str):
        value = json.loads(value)
    if isinstance(value, int):
        return [value]
    return list(value)


def read_metadata(row):
    value, args = row["value"], row["args"]
    assert row["kind"] == "read" and row["outcome"] == "success_response"
    if isinstance(value, dict):
        steps = value["steps"]
        return dict(ctx=value["ctx"], t=value["t"], frames=len(steps),
                    first_t=steps[0]["t"] if steps else None,
                    frame_times=[s["t"] for s in steps], preview_only=False)
    # The unrecovered previews retain the response header and first frame.
    # Infer only grid-time metadata, never sensor values, from them.
    assert row["preview_only"]
    text = value.replace(r'\"', '"')
    ctx = re.search(r'"ctx"\s*:\s*"([^"\\]+)"', text).group(1)
    times = [float(x) for x in re.findall(r'"t"\s*:\s*([-+0-9.eE]+)', text)[:2]]
    assert len(times) == 2
    end, first = times
    stride = max(1, int(args.get("stride", 1)))
    n = int(round((end - first) / (STEP * stride))) + 1
    assert ctx == "base" and int(args.get("window", 1)) == 25 and stride == 1
    assert 1 <= n <= 25
    return dict(ctx=ctx, t=end, frames=n, first_t=first,
                frame_times=[first + STEP * stride * j for j in range(n)], preview_only=True)


def context(row):
    a = row["args"]
    if row["kind"] in {"reset", "fork"}:
        return a.get("fork") or None
    if row["kind"] in {"read", "wait", "adjust", "inject"}:
        return a.get("ctx", "base")
    return None


def state_analysis(trace, rows):
    nodes, phy = trace["nodes"], trace["info"]["physim"]
    probe = [r for r in rows if r["tool"].startswith("mcp__probe__")]
    byid = {r["id"]: r for r in rows}
    bytool = {tool: dict(issued=sum(r["kind"] == tool for r in probe),
                        outcomes=dict(Counter(r["outcome"] for r in probe if r["kind"] == tool))) for tool in TOOLS}
    forks = [r for r in probe if r["kind"] == "fork" and r["outcome"] == "success_response"]
    resets = [r for r in probe if r["kind"] == "reset" and r["outcome"] == "success_response"]
    statuses = [r for r in probe if r["kind"] == "status" and isinstance(r["value"], dict)]
    frows, anchors, status_anchors = defaultdict(list), defaultdict(set), defaultdict(set)
    for r in forks:
        v = r["value"]
        frows[v["fork"]].append(r)
        anchors[v["fork"]].add(v["anchor_t"])
    for r in statuses:
        for ctx in r["value"]["contexts"]:
            status_anchors[ctx["id"]].add(ctx["anchor_t"])
    # A status can expose a handle whose spawning call timed out. Do not
    # silently count such a handle as an acknowledged fork response.
    observed_anchors = {fid: set(aa) | status_anchors.get(fid, set()) for fid, aa in anchors.items()}
    for fid, aa in status_anchors.items():
        observed_anchors.setdefault(fid, set()).update(aa)
    naive = dict(sensor=0.0, adjust=0.0, injection=0.0, sim_tu=0.0,
                 log_entries=0, reads_base=0, reads_fork=0, fork_spawns=len(forks),
                 resets=len(resets), turns=sum(r["outcome"] not in {"tool_timeout", "no_result_recorded"} for r in probe))
    base_reads, injections, adjustments = [], [], []
    metered_rows = defaultdict(list)
    for r in probe:
        kind, v, a = r["kind"], r["value"], r["args"]
        if kind == "read" and r["outcome"] == "success_response":
            md = read_metadata(r)
            r["read_metadata"] = md
            cost = md["frames"] * sum(SLOTS[d] for d in devices(a.get("devices", "all"))) * STEP
            naive["sensor"] += cost
            base = md["ctx"] == "base"
            naive["reads_base" if base else "reads_fork"] += md["frames"]
            if base:
                base_reads.append(dict(**ref(r), **md))
            else:
                window = int(a.get("window", 1))
                naive["sim_tu"] += window * STEP
                naive["log_entries"] += int(window > 0)
            metered_rows[kind].append(r)
        elif kind == "adjust" and isinstance(v, dict) and "steps_applied" in v:
            applied, rejected = v["steps_applied"], v["result"] == "adjust_rejected"
            cost = sum(abs(x) for x in v["applied"]) * (applied + int(rejected))
            naive["adjust"] += cost
            naive["sensor"] += len(v["steps_read"]) * SLOTS[v["device"]] * STEP
            naive["reads_base" if v["ctx"] == "base" else "reads_fork"] += len(v["steps_read"])
            if v["ctx"] != "base":
                naive["sim_tu"] += applied * STEP
                naive["log_entries"] += int(applied > 0)
            adjustments.append(dict(**ref(r), ctx=v["ctx"], anchor_set=sorted(observed_anchors.get(v["ctx"], set())),
                                    device=v["device"], u=v["applied"], requested_steps=v["steps_requested"],
                                    applied_steps=applied, read_frames=len(v["steps_read"]), result=v["result"],
                                    t=v["t"], reply_derived_adjust=cost))
            metered_rows[kind].append(r)
        elif kind == "wait" and r["outcome"] == "success_response":
            if v["ctx"] != "base":
                naive["sim_tu"] += int(a.get("steps", 1)) * STEP
                naive["log_entries"] += 1
            metered_rows[kind].append(r)
        elif kind == "inject" and r["outcome"] == "success_response":
            amp, dur = v["amp"], v["dur"]
            cost = abs(amp) * (1 + 4 * max(0, abs(amp) - 0.5)) * dur
            naive["injection"] += cost
            naive["log_entries"] += 2
            injections.append(dict(**ref(r), ctx=v["ctx"], anchor_set=sorted(observed_anchors.get(v["ctx"], set())),
                                   port=v["port"], amp=amp, dur=dur, t=v["t"], reply_derived_injection=cost))
            metered_rows[kind].append(r)
    naive = {k: round(v, 9) if isinstance(v, float) else v for k, v in naive.items()}
    diffs = {k: round(v - phy["meters"][k], 9) for k, v in naive.items()}

    # Fork ledger: operations keyed by the returned handle, not an invented
    # experiment identity. Reused handles and unacknowledged spawns stay explicit.
    fid_ops = defaultdict(list)
    for r in probe:
        fid = context(r)
        if fid and fid != "base":
            fid_ops[fid].append(r)
    ledger = []
    for fid in sorted(set(observed_anchors) | set(fid_ops), key=lambda fid: (min(observed_anchors.get(fid, {1e99})), min([r["node"] for r in frows.get(fid, [])] + [r["node"] for r in fid_ops[fid]] + [99999]))):
        rr = fid_ops[fid]
        aa = sorted(observed_anchors.get(fid, set()))
        observed_t = []
        for r in rr:
            if isinstance(r["value"], dict) and isinstance(r["value"].get("t"), (int, float)):
                observed_t.append(r["value"]["t"])
        own_reply_max_t = max(observed_t) if observed_t else None
        observed_t.extend(x["t_now"] for r in statuses for x in r["value"]["contexts"] if x["id"] == fid)
        successful_adj = [x for x in adjustments if x["ctx"] == fid]
        successful_inj = [x for x in injections if x["ctx"] == fid]
        category = ("anchor_ambiguous" if len(aa) > 1 else "emission" if successful_inj else
                    "actuator" if any(r["kind"] == "adjust" for r in rr) else
                    "global_wait_only" if any(r["kind"] == "wait" for r in rr) and not any(r["kind"] == "read" for r in rr) else
                    "unperturbed_read" if any(r["kind"] == "read" for r in rr) else "no_measurement_reply")
        ledger.append(dict(fork=fid, anchor_set=aa, kind=category,
                           fork_replies=[ref(r) for r in frows.get(fid, [])],
                           issued=dict(Counter(r["kind"] for r in rr)),
                           timeout_or_missing=dict(Counter(r["kind"] + ":" + r["outcome"] for r in rr if r["outcome"] in {"tool_timeout", "no_result_recorded"})),
                           own_reply_max_t=own_reply_max_t, observed_max_t=max(observed_t) if observed_t else None,
                           max_observed_elapsed_tu=max(observed_t) - aa[0] if observed_t and len(aa) == 1 else None,
                           accepted_adjustment_steps=sum(x["applied_steps"] for x in successful_adj),
                           injection_replies=len(successful_inj),
                           successful_reset_replies=sum(r["kind"] == "reset" and r["outcome"] == "success_response" for r in rr)))
    anchor_summary = []
    for a in sorted({a for aa in observed_anchors.values() for a in aa}):
        ll = [x for x in ledger if a in x["anchor_set"]]
        unambig = [x for x in ll if len(x["anchor_set"]) == 1]
        anchor_summary.append(dict(anchor_t=a,
            acknowledged_fork_replies=sum(r["value"]["anchor_t"] == a for r in forks),
            distinct_ids_in_fork_replies=len({r["value"]["fork"] for r in forks if r["value"]["anchor_t"] == a}),
            additional_ids_seen_only_in_status=sum(not x["fork_replies"] for x in unambig),
            ambiguous_ids=sum(len(x["anchor_set"]) > 1 for x in ll),
            unambiguous_handle_categories=dict(Counter(x["kind"] for x in unambig)),
            unambiguous_accepted_adjustment_steps=sum(x["accepted_adjustment_steps"] for x in unambig),
            unambiguous_injections=sum(x["injection_replies"] for x in unambig),
            largest_unambiguous_reported_elapsed_tu=max([x["max_observed_elapsed_tu"] for x in unambig if x["max_observed_elapsed_tu"] is not None], default=None)))
    duplicate_forks = [dict(fork=fid, anchor_set=sorted(observed_anchors[fid]),
                            replies=[dict(**timed_ref(r), requested_t=r["args"].get("t"), returned_t=r["value"]["t"], anchor_t=r["value"]["anchor_t"]) for r in rr])
                       for fid, rr in frows.items() if len(rr) > 1]
    reset_groups = defaultdict(list)
    for r in resets:
        reset_groups[r["value"]["fork"]].append(r)
    repeated_resets = [dict(fork=fid, replies=[ref(r) for r in rr]) for fid, rr in reset_groups.items() if len(rr) > 1]

    # For a clock comparison, require that the earlier response really is in
    # the later sampled node's ancestor context. Wall-time sorting alone is
    # insufficient. A mismatched delta is evidence, not a causal diagnosis.
    def observation(row, fid):
        v = row["value"]
        if not isinstance(v, dict):
            return None
        if v.get("ctx", v.get("fork")) == fid and isinstance(v.get("t"), (float, int)):
            return float(v["t"])
        if row["kind"] == "status":
            return next((float(x["t_now"]) for x in v.get("contexts", []) if x["id"] == fid), None)
        return None

    def previous_in_context(row, fid):
        ni = nodes[row["node"]].get("parent")
        while ni is not None:
            m = nodes[ni]["message"]
            if m["role"] == "tool":
                old = byid.get(m["tool_call_id"])
                if old is not None:
                    t = observation(old, fid)
                    if t is not None:
                        return old, t, ni
            ni = nodes[ni].get("parent")
        return None

    clock_mismatch = []
    compared = 0
    for r in probe:
        if r["kind"] not in {"read", "wait", "adjust", "inject"}:
            continue
        fid = context(r)
        if not fid or fid == "base":
            continue
        t = observation(r, fid)
        if t is None:
            continue
        prev = previous_in_context(r, fid)
        if not prev:
            continue
        old, old_t, observed_node = prev
        if r["kind"] == "read":
            expected_delta = STEP * int(r["args"].get("window", 1))
        elif r["kind"] == "wait":
            expected_delta = STEP * int(r["args"].get("steps", 1))
        elif r["kind"] == "adjust":
            expected_delta = STEP * r["value"]["steps_applied"]
        else:
            expected_delta = 0
        compared += 1
        actual = t - old_t
        if abs(actual - expected_delta) > 1e-6:
            between = [x for x in fid_ops[fid] if old["timestamp"] < x["timestamp"] < r["timestamp"]]
            clock_mismatch.append(dict(fork=fid, anchor_set=sorted(observed_anchors.get(fid, set())),
                                       previous=dict(**ref(old), t=old_t, kind=old["kind"], seen_as_ancestor_node=observed_node),
                                       current=dict(**ref(r), t=t, kind=r["kind"], args=r["args"]),
                                       expected_delta_from_this_reply=expected_delta, actual_delta=actual,
                                       delta_difference=actual - expected_delta,
                                       intervening_timeout_or_missing_calls=[ref(x) for x in between if x["outcome"] in {"tool_timeout", "no_result_recorded"}],
                                       other_issued_same_context_calls_between=len(between),
                                       backward=actual < 0, shortfall=actual < expected_delta))

    same_node = defaultdict(list)
    for r in probe:
        same_node[r["node"]].append(r)
    multi_nodes = [dict(node=ni, calls=[dict(**ref(r), kind=r["kind"], context=context(r), outcome=r["outcome"]) for r in rr]) for ni, rr in same_node.items() if len(rr) > 1]
    ready = next(r for r in probe if r["kind"] == "ready")
    after_ready = [r for r in probe if r["timestamp"] > ready["timestamp"]]
    crossing = [r for r in probe if r["kind"] in WORLD and r["timestamp"] < ready["timestamp"]
                and r["result_timestamp"] is not None and r["result_timestamp"] > ready["timestamp"]]
    missing = [r for r in probe if r["outcome"] == "no_result_recorded"]
    final_world = max((r for r in probe if r["kind"] in WORLD), key=lambda r: r["timestamp"])
    base_frames = [t for r in base_reads for t in r["frame_times"]]
    assert sorted(set(base_frames)) == [STEP * i for i in range(1, 501)]
    return dict(
        tools=bytool,
        persisted_state=dict(meters=phy["meters"], resident_cache=phy["resident_cache"], time_to_ready=phy["time_to_ready"],
                             resource_truncated=phy["resource_truncated"], cap_hits=phy["cap_hits"],
                             final_status=dict(**ref(statuses[-1]), phase=statuses[-1]["value"]["phase"], contexts=statuses[-1]["value"]["contexts"]),
                             max_observed_status_contexts=max(len(r["value"]["contexts"]) for r in statuses),
                             final_resident_count=None, final_resident_count_note="Not recorded. ready5 removes open handles from the cache, but this is not a final live-registry snapshot."),
        reply_accounting=dict(sums=naive, reply_minus_persisted=diffs,
                              note="These are reply-derived counterfactual sums under the current source formulas, not a reconstruction of persisted transactions or all server work. Timeouts and missing replies are excluded, not assigned zero execution.",
                              inferred_preview_base_frames=sum(r["frames"] for r in base_reads if r["preview_only"])),
        handles=dict(successful_fork_replies=len(forks), unique_returned_ids=len(frows),
                     unique_handles_seen_in_status_or_fork=len(observed_anchors),
                     fork_ids_returned_more_than_once=len(duplicate_forks),
                     fork_ids_with_multiple_anchor_times=sum(len(aa) > 1 for aa in observed_anchors.values()),
                     successful_reset_replies=len(resets), unique_successfully_reset_ids=len(reset_groups),
                     fork_from_fork_issued=sum(bool(r["args"].get("fork")) for r in probe if r["kind"] == "fork"),
                     duplicate_fork_evidence=duplicate_forks, repeated_reset_evidence=repeated_resets,
                     status_only_handles=[dict(fork=fid, anchor_set=sorted(aa), refs=[ref(r) for r in statuses if any(x["id"] == fid for x in r["value"]["contexts"])]) for fid, aa in status_anchors.items() if fid not in anchors]),
        base_record=dict(successful_read_replies=len(base_reads), frames=len(base_frames), distinct_grid_times=len(set(base_frames)),
                         min_t=min(base_frames), max_t=max(base_frames), preview_only_replies=sum(r["preview_only"] for r in base_reads),
                         repeated_grid_times={str(t): n for t, n in Counter(base_frames).items() if n > 1},
                         read_ranges=[{k:v for k,v in r.items() if k != "frame_times"} for r in base_reads],
                         note="The trace has one full first-frame reply and 20 header/preview-only base chunks; 500 grid times do not imply that all 500 raw sensor arrays are available in this snapshot."),
        anchors=anchor_summary,
        injections=injections,
        adjustment_totals=dict(reply_count=len(adjustments), accepted_control_steps=sum(x["applied_steps"] for x in adjustments),
                               read_frames=sum(x["read_frames"] for x in adjustments),
                               responses_with_positive_applied_steps=sum(x["applied_steps"] > 0 for x in adjustments),
                               device_counts=dict(Counter(x["device"] for x in adjustments))),
        adjustments=adjustments,
        handle_ledger=ledger,
        clocks=dict(ancestor_ordered_comparisons=compared, nonadditive_deltas=len(clock_mismatch),
                    shortfalls=sum(x["shortfall"] for x in clock_mismatch), backwards=sum(x["backward"] for x in clock_mismatch),
                    evidence=clock_mismatch,
                    note="Earlier tool response is present in the later model node's ancestry. Deltas compare that observed time with this reply's claimed advancement. Intervening or background requests, repeated handles, timeouts, and whole-state replacement prevent a unique causal explanation."),
        parallel_surface=dict(multi_probe_call_nodes=len(multi_nodes), calls_in_multi_probe_nodes=sum(len(x["calls"]) for x in multi_nodes),
                              same_node_fork_fork_pairs=sum(sum(r["kind"] == "fork" for r in rr) > 1 for rr in same_node.values()),
                              nodes=multi_nodes),
        ready_boundary=dict(ready=timed_ref(ready), post_ready_probe_counts=dict(Counter(r["kind"] for r in after_ready)),
                            post_ready_world_calls=[ref(r) for r in after_ready if r["kind"] in WORLD],
                            pre_ready_world_calls_with_result_nodes_after_ready=[timed_ref(r) for r in crossing],
                            pre_ready_missing_world_results=[dict(**timed_ref(r), kind=r["kind"], args=r["args"]) for r in missing],
                            last_world_call=dict(**timed_ref(final_world), kind=final_world["kind"], args=final_world["args"]),
                            seconds_last_world_sampled_node_to_ready=ready["timestamp"] - final_world["timestamp"],
                            last_20_world_calls=[dict(**timed_ref(r), kind=r["kind"], args=r["args"], outcome=r["outcome"]) for r in [x for x in probe if x["kind"] in WORLD][-20:]],
                            transaction_timing_available=False))



def compact_summary(result, trace, rows):
    """Persist counts and small exact evidence, not a full row/stream dump."""
    def short(r):
        return f"N{r['node']}/{r['tool_id']}/R{r['result_node']}"
    inj_groups = defaultdict(list)
    for x in result.pop("injections"):
        inj_groups[(tuple(x["anchor_set"]), x["amp"], x["dur"])].append(x)
    result["injection_protocol_groups"] = [dict(anchor_set=list(key[0]), amp=key[1], dur=key[2],
        replies=len(xx), ports_in_reply_order=[x["port"] for x in xx],
        issued_nodes=[x["node"] for x in xx], example_first=short(xx[0]), example_last=short(xx[-1]))
        for key, xx in inj_groups.items()]
    adj_groups = defaultdict(list)
    for x in result.pop("adjustments"):
        kind = "multi_step_axis" if x["requested_steps"] > 1 else "single_step_axis_or_zero" if sum(abs(v)>1e-8 for v in x["u"])<=1 else "single_step_multiaxis"
        adj_groups[(tuple(x["anchor_set"]), kind)].append(x)
    result["adjustment_protocol_groups"] = [dict(anchor_set=list(key[0]), kind=key[1], replies=len(xx),
        applied_steps=sum(x["applied_steps"] for x in xx), read_frames=sum(x["read_frames"] for x in xx),
        refused_replies=sum(x["result"]=="adjust_rejected" for x in xx), issued_nodes=[x["node"] for x in xx],
        example_first=short(xx[0]), example_last=short(xx[-1])) for key,xx in adj_groups.items()]
    ranges = result["base_record"].pop("read_ranges")
    result["base_record"]["representative_read_ranges"] = [ranges[0], ranges[1], ranges[-1]]
    result["base_record"]["omitted_read_ranges"] = len(ranges) - 3
    ledger = result.pop("handle_ledger")
    result["handle_protocol_counts"] = dict(Counter(x["kind"] for x in ledger))
    result["handle_protocol_note"] = "Observed request/reply categories, not independent realized experiments. They include one multi-anchor alias and one status-only handle. Per-anchor maxima include status observations and can disagree with a branch's own replies."
    result["selected_long_handle_evidence"] = [x for x in ledger if x["kind"] != "anchor_ambiguous" and x["max_observed_elapsed_tu"] is not None and x["max_observed_elapsed_tu"] >= 600]
    result["handles_without_reset_acknowledgment"] = [dict(fork=x["fork"], anchor_set=x["anchor_set"], fork_replies=x["fork_replies"], own_reply_max_t=x["own_reply_max_t"]) for x in ledger if not x["successful_reset_replies"]]
    result["clocks"]["evidence"] = [dict(fork=x["fork"], anchor_set=x["anchor_set"],
        previous=short(x["previous"]), previous_t=x["previous"]["t"], previous_seen_as_ancestor=x["previous"]["seen_as_ancestor_node"],
        current=short(x["current"]), current_kind=x["current"]["kind"], current_t=x["current"]["t"],
        expected_delta=x["expected_delta_from_this_reply"], actual_delta=x["actual_delta"],
        intervening_context_argument_requests=x["other_issued_same_context_calls_between"],
        intervening_timeout_or_missing=len(x["intervening_timeout_or_missing_calls"])) for x in result["clocks"]["evidence"]]
    pn = result["parallel_surface"].pop("nodes")
    result["parallel_surface"]["node_operation_counts"] = [dict(node=x["node"], tools=dict(Counter(r["kind"] for r in x["calls"]))) for x in pn]
    result["parallel_surface"]["selected_multi_call_evidence"] = [x for x in pn if x["node"] in {1359}]
    rb = result["ready_boundary"]
    rb["last_3_world_calls"] = rb.pop("last_20_world_calls")[-3:]
    rb["pre_ready_missing_world_results"] = [dict(call=short(x), sampled_node_utc=x["sampled_node_utc"], kind=x["kind"], ctx=x["args"].get("ctx")) for x in rb["pre_ready_missing_world_results"]]
    last_timeout = max((r for r in rows if r["kind"] in WORLD and r["outcome"] == "tool_timeout"),key=lambda r:r["timestamp"])
    rb["last_world_tool_timeout"] = dict(**timed_ref(last_timeout),kind=last_timeout["kind"],args=last_timeout["args"])
    last_agent = max((r for r in rows if r["tool"] == "Agent"), key=lambda r:r["timestamp"])
    rb["last_data_capture_agent"] = dict(**timed_ref(last_agent), description=last_agent["args"].get("description"),
        run_in_background=last_agent["args"].get("run_in_background"),
        result_node_before_ready=last_agent["result_timestamp"] < next(r["timestamp"] for r in rows if r["kind"] == "ready"))
    root = Path.cwd()
    srcs = {".venv/lib/python3.13/site-packages/verifiers/v1/mcp/server.py": [[175,206],[227,249]],
            "environments/physim/physim/servers/blob.py": [[158,166],[224,259],[310,338],[503,546],[587,650],[686,700],[741,812],[816,886],[928,945],[949,977]],
            "environments/physim/physim/blobcore.py": [[146,149]]}
    result["current_source_basis"] = [dict(path=p,sha256=hashlib.sha256((root/p).read_bytes()).hexdigest(),line_ranges=ll) for p,ll in srcs.items()]
    result["current_source_note"] = "Static inspection of current local installed/native files only. The trace lacks GET/fn/PUT timing, write versions, transaction logs, and final resident-registry contents. No historical transaction order or exact simulator work is inferred."
    return result


def main():
    trace, scope, rows, result_nodes, completed = load()
    result = compact_summary(state_analysis(trace, rows), trace, rows)
    result = dict(scope=scope,
                  counting=dict(sampled_model_nodes=len(completed), unique_sampled_tool_ids=len(rows),
                                tool_result_graph_nodes=sum(len(x) for x in result_nodes.values()),
                                unique_result_ids=len(result_nodes), identical_result_copy_nodes=sum(len(x)-1 for x in result_nodes.values()),
                                note="Each sampled call/node/tool-ID is counted once. Later identical graph copies of results are not new calls."),
                  **result)
    (OUT / "experiment_summary.json").write_text(json.dumps(result, separators=(",", ":"), ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(OUT / "experiment_summary.json"),
                      "reply_accounting": result["reply_accounting"],
                      "handles": {k:v for k,v in result["handles"].items() if not isinstance(v,list)},
                      "clock_counts": {k:v for k,v in result["clocks"].items() if k != "evidence"},
                      "anchors": result["anchors"],
                      "adjustment_totals": result["adjustment_totals"]}, indent=2))


if __name__ == "__main__":
    main()
