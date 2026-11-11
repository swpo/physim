"""extract -- everything worth keeping from ONE finished model rollout, as files for the repository.

    <venv python> -B rollouts/tools/extract.py --name qwen_ring_001 --run-dir RUN_DIR --store STORE --instance IID \
        --proof PROOF.json --watch WATCH_DIR --model-entry MODEL_ENTRY.json --out rollouts/qwen_ring_001

Reads the saved trace (RUN_DIR/traces.jsonl), the laboratory's own record and the per-item grades in the store,
the reference table of tools/prove.py (PROOF.json and its _items.npz) and the watcher's copies of submission/.
Writes into --out, every file marked PILOT_NEVER_REUSE_AS_EXAM (inside the file, or in MANIFEST.json for
files that cannot carry a line of text):

  result.json            reward, stop condition, errors, turns, tokens and cost per model call and in total, wall
                         times, tool calls by name, the laboratory's counters, the grade, the submission's manifest,
                         the table with the agent's row next to K, D, P0, PM, S, C, O and null, with bootstrap noise
  per_item_scores.json   per exam item: the energy score summed over the valid cells, for the agent and every
                         reference, the program class, whether the agent's item failed
  lab_record.json        the laboratory's own log of the rollout: every request (op, ok, kind, ticks, nats)
  transcript.md          the whole conversation, readable: every message, tool call and tool result, in order
  trace.redacted.jsonl   the raw trace record with credential-like fields removed (see redact())
  submission/            the frozen submission folder (from the verifier's box; else the last copy from the
                         agent's box), regular files only; submission_manifest.json says where it came from
  resolved_config/       vf-eval's own resolved config of the run
  timeline.jsonl         what the watcher saw every 20 s (containers, laboratory counters, free disk)
  reference/             proof JSON and per-item npz of the scripted reference policies on the same instance

The model's text is DATA. Nothing from the trace or from submission/ is executed, imported or evaluated here.
No credential is read by this tool; tools/scan_key.py is run on the output afterwards.
"""
import argparse
import hashlib
import io
import json
import os
import re
import shutil
import sys
import tarfile
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
VFPORT = os.path.normpath(os.path.join(HERE, "..", "..", "vfport"))
MARK = "PILOT_NEVER_REUSE_AS_EXAM"
CRED_KEY = re.compile(r"(?i)(api[-_]?key|authorization|bearer|passw(or)?d|cookie|credential|private[-_]?key|"
                      r"(access|refresh|auth|id|session)[-_]?token|secret|x-prime-team-id|team[-_]?id|user[-_]?id|user[-_]?name)")
CRED_KEY_KEEP = {"secret_commitment"}                         # a public hash of the instance's secret, saved in every task row
REMOVED = "[removed: credential-like field]"


def redact(o, removed: list, path=""):
    """A copy of a JSON value in which every value under a credential-like key is replaced. Counts and token
    statistics (`num_input_tokens`, `prompt_tokens`, `max_tokens`, `token_ids`) are not credentials: only keys
    matching CRED_KEY are touched, and `secret_commitment` (public) is kept."""
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            if isinstance(k, str) and CRED_KEY.search(k) and k not in CRED_KEY_KEEP and v not in (None, "", [], {}):
                removed.append(f"{path}/{k}")
                out[k] = REMOVED
            else:
                out[k] = redact(v, removed, f"{path}/{k}")
        return out
    if isinstance(o, list):
        return [redact(v, removed, f"{path}[]") for v in o]
    return o


def fence(text: str) -> str:
    """A fenced block that the text itself cannot close."""
    text = "" if text is None else str(text)
    n = max([3] + [len(m) + 1 for m in re.findall(r"`{3,}", text)])
    return "`" * n + "\n" + text + ("" if text.endswith("\n") else "\n") + "`" * n


def content_text(c) -> str:
    if c is None:
        return ""
    if isinstance(c, str):
        return c
    parts = []
    for p in c:
        if isinstance(p, dict) and p.get("type") == "text":
            parts.append(p.get("text", ""))
        else:
            parts.append(f"[content part of type {p.get('type') if isinstance(p, dict) else type(p).__name__}]")
    return "\n".join(parts)


def pretty_args(arguments: str) -> str:
    try:
        a = json.loads(arguments)
    except (ValueError, TypeError):
        return fence(arguments)
    if isinstance(a, dict):
        blocks = []
        for k, v in a.items():
            if isinstance(v, str) and ("\n" in v or len(v) > 100):
                blocks.append(f"`{k}`:\n\n{fence(v)}")
            else:
                blocks.append(f"`{k}`: `{json.dumps(v)}`" if not isinstance(v, (dict, list)) else f"`{k}`:\n\n{fence(json.dumps(v, indent=1))}")
        return "\n\n".join(blocks) if blocks else "(no arguments)"
    return fence(json.dumps(a, indent=1))


def transcript(tr: dict, head: str) -> tuple[str, dict]:
    nodes, calls = tr.get("nodes") or [], tr.get("calls") or []
    call_of = {c.get("node"): (i, c) for i, c in enumerate(calls) if c.get("node") is not None}
    t0 = (tr.get("timing") or {}).get("start") or (nodes[0].get("timestamp") if nodes else 0) or 0
    out, tool_counts, turn = [head], {}, 0
    tools = tr.get("tools") or []
    if tools:
        out.append("## Tools offered to the model\n")
        for t in tools:
            name = (t.get("namespace") + "." if t.get("namespace") else "") + str(t.get("name"))
            out.append(f"### `{name}`\n\n{fence(t.get('description') or '')}\n\nparameters:\n\n{fence(json.dumps(t.get('parameters'), indent=1))}\n")
    out.append("## Conversation\n")
    for i, n in enumerate(nodes):
        m = n.get("message") or {}
        role = m.get("role")
        ts = n.get("timestamp")
        when = f"t = {ts - t0:.0f} s" if isinstance(ts, (int, float)) and t0 else ""
        if role == "assistant":
            if n.get("sampled"):
                turn += 1
            ci = call_of.get(i)
            u = (ci[1].get("usage") or {}) if ci else {}
            usage = (f"; call {ci[0] + 1}: {u.get('prompt_tokens', 0) + (u.get('cached_input_tokens') or 0)} tokens in "
                     f"({u.get('cached_input_tokens') or 0} cached), {u.get('completion_tokens')} out"
                     f"{', ' + str(u.get('reasoning_tokens')) + ' reasoning' if u.get('reasoning_tokens') else ''}, "
                     f"finish `{ci[1].get('finish_reason')}`") if ci else ""
            out.append(f"### [{i}] assistant, turn {turn} ({when}{usage})\n")
            if m.get("reasoning_content"):
                out.append("reasoning:\n\n" + fence(m["reasoning_content"]) + "\n")
            if m.get("content"):
                out.append(fence(m["content"]) + "\n")
            for c in m.get("tool_calls") or []:
                name = (c.get("namespace") + "." if c.get("namespace") else "") + str(c.get("name"))
                tool_counts[name] = tool_counts.get(name, 0) + 1
                out.append(f"**tool call** `{name}` (id `{c.get('id')}`)\n\n{pretty_args(c.get('arguments'))}\n")
            if not (m.get("content") or m.get("tool_calls") or m.get("reasoning_content")):
                out.append("(empty message)\n")
        elif role == "tool":
            out.append(f"### [{i}] tool result{' `' + m['name'] + '`' if m.get('name') else ''} (for `{m.get('tool_call_id')}`; {when})\n\n"
                       + fence(content_text(m.get("content"))) + "\n")
        else:
            out.append(f"### [{i}] {role} ({when})\n\n" + fence(content_text(m.get("content"))) + "\n")
    failed = [(i, c) for i, c in enumerate(calls) if c.get("error")]
    if failed:
        out.append("## Model calls that ended in an error\n")
        for i, c in failed:
            out.append(f"- call {i + 1}: `{(c.get('error') or {}).get('type')}`\n\n{fence(json.dumps(c.get('error'), indent=1))}\n")
    return "\n".join(out), {"turns": turn, "tool_calls_by_name": tool_counts, "nodes": len(nodes)}


def usage_and_cost(tr: dict, entry: dict) -> dict:
    p = entry["entry"]["pricing"]
    p_in, p_out = p["input_usd_per_mtok"], p["output_usd_per_mtok"]
    p_cache = p.get("cache_read_usd_per_mtok")
    rows, tot = [], {"prompt_tokens_uncached": 0, "cached_input_tokens": 0, "completion_tokens": 0, "reasoning_tokens": 0}
    provider_cost, n_cost, n_no_usage = 0.0, 0, 0
    for i, c in enumerate(tr.get("calls") or []):
        u, tm = c.get("usage"), c.get("time") or {}
        row = {"call": i + 1, "node": c.get("node"), "model": c.get("model"), "finish_reason": c.get("finish_reason"),
               "error": (c.get("error") or {}).get("type") if c.get("error") else None,
               "seconds": None if tm.get("end") is None or tm.get("start") is None else round(tm["end"] - tm["start"], 2)}
        if u is None:
            n_no_usage += 1
        else:
            row.update(prompt_tokens_uncached=u.get("prompt_tokens"), cached_input_tokens=u.get("cached_input_tokens") or 0,
                       completion_tokens=u.get("completion_tokens"), reasoning_tokens=u.get("reasoning_tokens") or 0, provider_cost=u.get("cost"))
            tot["prompt_tokens_uncached"] += u.get("prompt_tokens") or 0
            tot["cached_input_tokens"] += u.get("cached_input_tokens") or 0
            tot["completion_tokens"] += u.get("completion_tokens") or 0
            tot["reasoning_tokens"] += u.get("reasoning_tokens") or 0
            if isinstance(u.get("cost"), (int, float)):
                provider_cost += u["cost"]
                n_cost += 1
        rows.append(row)
    billed_in = tot["prompt_tokens_uncached"] + tot["cached_input_tokens"]
    cost_cache = (tot["prompt_tokens_uncached"] * p_in + tot["cached_input_tokens"] * (p_cache if p_cache is not None else p_in)
                  + tot["completion_tokens"] * p_out) / 1e6
    cost_full = (billed_in * p_in + tot["completion_tokens"] * p_out) / 1e6
    return {"calls": rows, "n_calls": len(rows), "n_calls_without_usage": n_no_usage,
            "billed_input_tokens": billed_in, **tot,
            "trace_num_input_tokens_counted_once": tr.get("num_input_tokens"), "trace_num_output_tokens": tr.get("num_output_tokens"),
            "trace_num_total_tokens_what_the_caps_see": tr.get("num_total_tokens"),
            "price_usd_per_mtok": {"input": p_in, "output": p_out, "cache_read": p_cache, "source": entry.get("source"),
                                   "fetched_unix": entry.get("fetched_unix")},
            "cost_usd_with_cache_read_price": round(cost_cache, 6), "cost_usd_all_input_at_full_price": round(cost_full, 6),
            "provider_reported_cost_usd": round(provider_cost, 6) if n_cost else None, "calls_with_provider_cost": n_cost,
            "cost_usd_for_the_ledger": round(max(cost_full, provider_cost if n_cost else 0.0), 6),
            "note": "the ledger takes the larger of: all billed input at the full input price plus output, and the provider's own cost "
                    "field if it reports one. Calls without usage (errors) are counted but cannot be priced."}


def unpack_submission(tar_path: str, dst: str) -> dict:
    """Regular files only, names kept inside dst, nothing executed. Returns a manifest."""
    man = {"files": [], "skipped": [], "bytes": 0}
    with tarfile.open(tar_path) as tf:
        for m in tf.getmembers():
            parts = [p for p in m.name.split("/") if p not in ("", ".")]
            if parts[:1] == ["submission"]:
                parts = parts[1:]
            if not parts:
                continue
            if not m.isreg() or ".." in parts or m.size > (64 << 20):
                if not m.isdir():
                    man["skipped"].append({"name": m.name[:200], "why": "not a regular file" if not m.isreg() else "name or size"})
                continue
            target = os.path.join(dst, *parts)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            data = tf.extractfile(m).read()
            with open(target, "wb") as f:
                f.write(data)
            os.chmod(target, 0o644)
            man["files"].append({"path": "/".join(parts), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
            man["bytes"] += len(data)
    man["files"].sort(key=lambda r: r["path"])
    return man


def boot(per_item: dict, name: str, n_boot=4000, seed=0) -> dict:
    """Bootstrap over the items of this ONE instance: the skill on the K-to-O and K-to-C scales, and paired
    differences of the mean loss against each reference. Says nothing about other hidden worlds."""
    rng = np.random.default_rng(seed)
    n = len(per_item["K"])
    idx = rng.integers(0, n, size=(n_boot, n))
    L = {k: np.asarray(v)[idx].mean(1) for k, v in per_item.items()}
    out = {"n_items": n, "n_boot": n_boot}
    for scale in ("O", "C"):
        if scale in L:
            s = (L["K"] - L[name]) / (L["K"] - L[scale])
            point = (np.mean(per_item["K"]) - np.mean(per_item[name])) / (np.mean(per_item["K"]) - np.mean(per_item[scale]))
            out[f"skill_vs_{scale}"] = {"point": float(point), "se": float(s.std()), "p05": float(np.quantile(s, 0.05)), "p95": float(np.quantile(s, 0.95))}
    out["mean_loss_minus_reference"] = {}
    for k in per_item:
        if k == name:
            continue
        d = L[name] - L[k]
        out["mean_loss_minus_reference"][k] = {"point": float(np.mean(per_item[name]) - np.mean(per_item[k])), "p05": float(np.quantile(d, 0.05)),
                                                "p95": float(np.quantile(d, 0.95)), "share_of_resamples_agent_better": float((d < 0).mean())}
    return out


def main():
    ap = argparse.ArgumentParser()
    for k in ("name", "run-dir", "store", "instance", "proof", "watch", "model-entry", "out"):
        ap.add_argument("--" + k, required=True)
    ap.add_argument("--command-file", default="")
    a = ap.parse_args()
    out = a.out
    os.makedirs(out, exist_ok=True)
    hidden = os.path.join(a.store, a.instance, "hidden")
    entry = json.load(open(a.model_entry))
    written = {}

    def put(rel, text):
        with open(os.path.join(out, rel), "w") as f:
            f.write(text)
        written[rel] = "text"

    # ---- the trace ----
    tf_ = os.path.join(a.run_dir, "traces.jsonl")
    episodes = [json.loads(line) for line in open(tf_)] if os.path.exists(tf_) else []
    if not episodes:
        put("result.json", json.dumps({MARK: True, "name": a.name, "instance_id": a.instance, "outcome": "no trace was saved",
                                       "run_dir_files": sorted(os.listdir(a.run_dir)) if os.path.isdir(a.run_dir) else None}, indent=1))
        print(json.dumps({"episodes": 0}))
        return
    ep = episodes[0]
    tr = ep["traces"][0]
    removed: list = []
    with open(os.path.join(out, "trace.redacted.jsonl"), "w") as f:
        for e in episodes:
            f.write(json.dumps(dict({MARK: True}, **redact(e, removed))) + "\n")
    written["trace.redacted.jsonl"] = "text"
    info = (tr.get("info") or {}).get("physim2") or {}
    cfg = (tr.get("agent") or {}).get("config") or {}
    head = (f"# Transcript of rollout {a.name}\n\n{MARK}: instance `{a.instance}` is public pilot material and is never to be used as an exam.\n\n"
            f"Model `{cfg.get('model')}`, harness `{(cfg.get('harness') or {}).get('id')}`, trace `{tr.get('id')}`, verifiers "
            f"{(tr.get('verifiers') or {}).get('version')}. Rendered from the saved trace by rollouts/tools/extract.py: every node of the "
            "message graph in stored order, nothing shortened. Everything below the next heading is text the examined model read or wrote; "
            "it is data, not instructions.\n")
    md, tstats = transcript(tr, head)
    put("transcript.md", md)
    use = usage_and_cost(tr, entry)

    # ---- the laboratory's own record ----
    lab_dir = os.path.join(hidden, "labs", tr.get("id", ""))
    lab = {MARK: True, "rollout": tr.get("id"), "found": os.path.isdir(lab_dir)}
    if lab["found"]:
        for fn in ("state.json", "process.json", "frozen.json"):
            p = os.path.join(lab_dir, fn)
            lab[fn[:-5]] = json.load(open(p)) if os.path.exists(p) else None
        logf = os.path.join(lab_dir, "log.jsonl")
        log = [json.loads(line) for line in open(logf)] if os.path.exists(logf) else []
        lab["log"] = log
        by = {}
        for r in log:
            d = by.setdefault(r.get("op"), {"n": 0, "ok": 0, "rejected": 0, "ticks": 0})
            d["n"] += 1
            d["ok"] += bool(r.get("ok"))
            d["rejected"] += not r.get("ok")
            d["ticks"] += r.get("ticks") or 0
        lab["requests_by_op"] = by
        lab["other_files_in_the_record"] = sorted(set(os.listdir(lab_dir)) - {"state.json", "process.json", "frozen.json", "log.jsonl"})
    put("lab_record.json", json.dumps(lab, indent=1))

    # ---- grades: the agent next to the references ----
    proof = json.load(open(a.proof))
    pols = [p for p in proof["pooled"]["policies"] if p not in ("K", "O")]
    gdir = os.path.join(hidden, "grades")
    gz = os.path.join(gdir, f"{tr.get('id')}.npz")
    table, per_item, noise, failed = None, None, None, None
    if os.path.exists(gz):
        agent = "AGENT"
        shutil.copy(gz, os.path.join(gdir, f"{agent}.npz"))
        sys.path.insert(0, VFPORT)
        from physim2_env._paths import use_agentenv
        use_agentenv()
        from evaluator import grader as GR
        from evaluator import instance as INST
        table = GR.table(hidden, pols + [agent], n_boot=2000)
        valid = np.array(table["valid_cells"], bool)
        ex = INST.FrozenExam(hidden)
        refs = ex.references()
        z = np.load(gz)
        failed = z["failed"].astype(bool)
        per_item = {"K": refs["K"][:, valid].sum(1), "O": refs["O"][:, valid].sum(1)}
        for p in pols:
            per_item[p] = np.load(os.path.join(gdir, f"{p}.npz"))["es"][:, valid].sum(1)
        per_item[agent] = z["es"][:, valid].sum(1)
        noise = boot(per_item, agent)
        put("per_item_scores.json", json.dumps({
            MARK: True, "instance_id": a.instance, "what": "energy score per exam item, summed over the valid (level, time) cells; lower is better. "
            "AGENT is the model's submission as graded (a failed item is scored as K).", "cells": table["cells"], "valid_cells": table["valid_cells"],
            "program_class_per_item": ex.classes.tolist(), "agent_item_failed": failed.tolist(),
            "agent_predictor_cpu_s_per_item": [round(float(v), 3) for v in z["cpu"]],
            "per_item": {k: [round(float(v), 6) for v in vals] for k, vals in per_item.items()},
            "agent_per_item_per_cell": [[round(float(v), 6) for v in row] for row in z["es"]]}, indent=1))

    # ---- submission/ ----
    sub = {MARK: True, "source": None}
    boxes = {}
    try:
        boxes = json.load(open(os.path.join(a.watch, "boxes.json")))
    except (OSError, ValueError):
        pass
    order = boxes.get("boxes_in_order") or []
    cands = [(n, "verifier box (the frozen copy that was graded)" if i == 1 else "agent box (the watcher's last copy before the box was removed)")
             for i, n in reversed(list(enumerate(order)))]
    for name, what in cands:
        tp = os.path.join(a.watch, name + ".submission.tar")
        if os.path.exists(tp):
            dst = os.path.join(out, "submission")
            shutil.rmtree(dst, ignore_errors=True)
            os.makedirs(dst)
            man = unpack_submission(tp, dst)
            sub.update(source=what, container=name, tar_bytes=os.path.getsize(tp), copied_unix=os.path.getmtime(tp), **man)
            for r in man["files"]:
                written["submission/" + r["path"]] = "model-written file"
            break
    sub["frozen_manifest_of_the_laboratory"] = (lab.get("frozen") or None) if lab.get("found") else None
    sub["collection_recorded_in_the_trace"] = info.get("submission")
    put("submission_manifest.json", json.dumps(sub, indent=1))

    # ---- copies ----
    for src, rel in ((os.path.join(a.watch, "timeline.jsonl"), "timeline.jsonl"), (a.model_entry, "model_entry.json")):
        if os.path.exists(src):
            shutil.copy(src, os.path.join(out, rel))
            written[rel] = "copy"
    rc = os.path.join(a.run_dir, "configs")
    if os.path.isdir(rc):
        shutil.rmtree(os.path.join(out, "resolved_config"), ignore_errors=True)
        shutil.copytree(rc, os.path.join(out, "resolved_config"))
        for root, _, names in os.walk(os.path.join(out, "resolved_config")):
            for n in names:
                p = os.path.join(root, n)
                if n.endswith(".json"):                      # the client's headers name the operator's team
                    try:
                        d = json.load(open(p))
                        with open(p, "w") as f:
                            json.dump(redact(d, removed, "resolved_config"), f, indent=1)
                    except ValueError:
                        pass
                written[os.path.relpath(p, out)] = "copy of vf-eval's resolved config (credential-like fields removed)"
    os.makedirs(os.path.join(out, "reference"), exist_ok=True)
    items_f = os.path.splitext(a.proof)[0] + "_items.npz"
    for src in (a.proof, items_f):
        if os.path.exists(src):
            shutil.copy(src, os.path.join(out, "reference", os.path.basename(src)))
            written["reference/" + os.path.basename(src)] = "reference table of tools/prove.py (scores, counters, commitments; no hidden value)"

    # ---- the result ----
    tm = tr.get("timing") or {}
    span = lambda k: None if not tm.get(k) or tm[k].get("end") is None or tm[k].get("start") is None else round(tm[k]["end"] - tm[k]["start"], 1)  # noqa: E731
    g = info.get("grade") or {}
    reward = ((tr.get("rewards") or {}).get("skill") or {}).get("score")
    res = {
        MARK: True, "name": a.name, "instance_id": a.instance, "secret_commitment": info.get("secret_commitment"),
        "model": cfg.get("model"), "harness": (cfg.get("harness") or {}).get("id"), "trace_id": tr.get("id"),
        "verifiers": (tr.get("verifiers") or {}).get("version"),
        "command": open(a.command_file).read().strip() if a.command_file and os.path.exists(a.command_file) else None,
        "caps": {k: cfg.get(k) for k in ("max_turns", "max_total_tokens", "max_output_tokens", "max_input_tokens")},
        "sampling": cfg.get("sampling"), "timeout": cfg.get("timeout"),
        "box": {k: ((tr.get("agent") or {}).get("runtime") or {}).get(k) for k in ("type", "image", "cpu", "memory", "allow", "block", "workdir")},
        "outcome": {"episode_ok": ep.get("ok"), "trace_ok": tr.get("ok"), "is_completed": tr.get("is_completed"), "stop_condition": tr.get("stop_condition"),
                    "is_timeout": tr.get("is_timeout"), "trace_errors": tr.get("errors"), "episode_errors": ep.get("errors"),
                    "reward_skill_vs_O": reward, "graded": reward is not None},
        "turns": tstats["turns"], "message_nodes": tstats["nodes"], "tool_calls_by_name": tstats["tool_calls_by_name"],
        "usage": use,
        "wall_s": {k: span(k) for k in ("boot", "setup", "agent", "finalize", "scoring")} | {"verifier": g.get("verifier_wall_s"),
                   "agent_split": {k: v for k, v in (tm.get("agent") or {}).items() if k not in ("start", "end")}},
        "lab": info.get("lab"), "lab_requests_by_op": lab.get("requests_by_op"),
        "submission": info.get("submission"), "verifier_box": info.get("verifier_box"),
        "grade": {k: g.get(k) for k in ("skill_vs_O", "n_items", "n_failed", "reason", "isolation", "item_boxes", "item_box_wall_s_mean",
                                        "infrastructure_failed_items", "validation", "layers", "cpu_s_mean", "cpu_s_max", "seconds",
                                        "verifier_wall_s", "L", "L_K", "L_O")},
        "network_restricted": info.get("network_restricted"), "single_use": info.get("single_use"), "item_isolation": info.get("item_isolation"),
        "agent_key": info.get("agent_key"), "agent_box_cpu_s_unverified": info.get("agent_box_cpu_s_unverified"),
        "table_one_instance": None if table is None else {
            "what": "evaluator.grader.table on this one instance: L = mean energy score over the 64 items (sum over valid cells); "
                    "vs_O = (L_K - L) / (L_K - L_O), vs_C = (L_K - L) / (L_K - L_C). AGENT = the model. Reference policies were graded "
                    "with all items in one verifier box (prove.py), the model with one fresh box per item; prove.py's box check shows "
                    "the two modes give identical per-item scores for the same files.",
            "policies": table["policies"], "valid_cells": table["valid_cells"], "cells": table["cells"],
            "oes_per_cell": {k: v["per_cell"] for k, v in table["oes"].items()},
            "oes_by_program_class": table.get("oes_by_program_class"), "policy_labels": proof.get("policy_labels")},
        "noise_one_instance_bootstrap_over_items": noise,
        "agent_items_failed": None if failed is None else int(failed.sum()),
        "reference_box_check": proof.get("one_box_per_item_check_world_0"),
        "credential_like_fields_removed_from_the_raw_trace": sorted(set(removed)),
        "extracted_unix": time.time(),
    }
    put("result.json", json.dumps(res, indent=1, default=str))
    put("MANIFEST.json", json.dumps({MARK: True, "note": "every file of this folder is pilot material of instance " + a.instance
                                     + "; files that cannot carry the marker themselves (the model's own files under submission/, "
                                     "the npz, copies) are covered by this manifest.", "files": dict(sorted(written.items()))}, indent=1))
    print(json.dumps({"episodes": len(episodes), "reward": reward, "turns": tstats["turns"], "calls": use["n_calls"],
                      "billed_input_tokens": use["billed_input_tokens"], "completion_tokens": use["completion_tokens"],
                      "cost_usd_for_the_ledger": use["cost_usd_for_the_ledger"], "removed_fields": len(set(removed)),
                      "submission_files": len(sub.get("files") or []), "submission_source": sub.get("source")}))


if __name__ == "__main__":
    main()
