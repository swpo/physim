"""run_report -- what the operator needs to know about ONE finished run, as fixed fields and counts.

    python -B tools/run_report.py --store <store> --run-dir <output folder>/<run name>

Why this exists (host-safety audit, B14): a saved trace holds everything the examined model wrote. Whoever reads
`traces.jsonl` or vf-eval's console output reads that text; an operator that is itself a language model with a
shell on the machine must not. This tool reads the trace and prints

    booleans, numbers, hashes and words from FIXED lists of this file,

and nothing else: no message, no tool argument, no error text of a predictor, no file name chosen by the agent.
A value that is not a number, a boolean or one of the expected words is printed as "(other)" or as its length.
It also counts, without printing them, the places where a hidden value of the instance (the secret, the first
ten characters of each hidden parameter) occurs in the run folder: every count must be 0.

It reads the hidden side of the store (instance.json) to know what to look for. Output: one JSON object.
"""
import argparse
import json
import os
import re
import sys

# A stop condition is a name chosen by verifiers or by this taskset ("agent_completed", "max_turns", "frozen",
# "sandbox_error", ...) and an error type is the name of a Python exception class: both are identifiers, never
# text of the examined model. Anything that is not such an identifier is not printed.
STOP_WORD = re.compile(r"^[a-z][a-z0-9_]{0,39}$")
ERROR_WORD = re.compile(r"^[A-Za-z][A-Za-z0-9]{0,39}$")
SOURCE_WORDS = {"agent_submission", "final_collection", "verifiers_default", "none"}
TOOL_WORDS = {"bash", "edit", "search", "call", "lab.call", "lab_call", "lab__call", "mcp__lab__call"}
REASON_HEADS = ("validation failed (example 0)", "validation failed (example 1)", "validation failed (reproducibility)", "no predictor",
                "grading error", "ungraded rollout settled as K", "the reward ran outside the isolated grader", "submissions attempt limit",
                "collection failed", "freeze failed", "format:", "size:")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def word(v, allowed):
    """A string only if it is one of the expected words (a set) or has the expected form (a pattern); otherwise
    only what kind of thing it is."""
    if v is None or isinstance(v, (bool, int, float)):
        return v
    ok = isinstance(v, str) and (v in allowed if isinstance(allowed, (set, frozenset)) else bool(allowed.match(v)))
    return v if ok else f"(other, {len(str(v))} characters)"


def num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def flag(v):
    return v if isinstance(v, bool) else None


def head(v):
    """Which of the fixed beginnings a reason has (the rest may quote a predictor's own error text: not printed)."""
    if v is None:
        return None
    s = str(v)
    return next((h for h in REASON_HEADS if s.startswith(h)), f"(other, {len(s)} characters)")


def count_tool_calls(node, counts):
    """Tool calls by name, wherever the trace keeps them: objects under a key `tool_calls`. A name outside the
    fixed list is counted as (other); it is never printed."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "tool_calls" and isinstance(v, list):
                for c in v:
                    name = c.get("name") if isinstance(c, dict) else None
                    if name is None and isinstance(c, dict) and isinstance(c.get("function"), dict):
                        name = c["function"].get("name")
                    if isinstance(c, dict) and c.get("namespace") == "lab" and isinstance(name, str):
                        name = "lab." + name
                    key = name if isinstance(name, str) and name in TOOL_WORDS else "(other)"
                    counts[key] = counts.get(key, 0) + 1
            else:
                count_tool_calls(v, counts)
    elif isinstance(node, list):
        for v in node:
            count_tool_calls(v, counts)


def hidden_hits(run_dir, hidden):
    inst = json.load(open(os.path.join(hidden, "instance.json")))
    needles = {"secret": str(inst["secret_hex"]).encode()}
    for n, v in zip(inst["theta_names"], inst["theta"]):
        needles[f"hidden_parameter_{len(needles)}"] = repr(float(v))[:10].encode()
    del inst
    hits, files = {k: 0 for k in needles}, 0
    for root, _, names in os.walk(run_dir):
        for nm in names:
            try:
                raw = open(os.path.join(root, nm), "rb").read()
            except OSError:
                continue
            files += 1
            for k, v in needles.items():
                hits[k] += raw.count(v)
    return {"files_scanned": files, "needles": len(needles), "hits": hits, "total_hits": sum(hits.values())}


def report(store, run_dir):
    f = os.path.join(run_dir, "traces.jsonl")
    if not os.path.isfile(f):
        return {"traces_file": False, "episodes": 0}
    out = {"traces_file": True, "episodes": 0, "rollouts": []}
    for line in open(f):
        ep = json.loads(line)
        out["episodes"] += 1
        for tr in ep.get("traces", []):
            info = tr.get("info") or {}
            ph = info.get("physim2") or {}
            g, lab, sub, vb = ph.get("grade") or {}, ph.get("lab") or {}, ph.get("submission") or {}, ph.get("verifier_box") or {}
            data = (tr.get("task") or {}).get("data") or {}
            reward = (tr.get("rewards", {}).get("skill") or {}).get("score")
            calls = {}
            count_tool_calls(tr, calls)
            iid = data.get("instance_id")
            iid = iid if isinstance(iid, str) and re.fullmatch(r"[a-z0-9][a-z0-9_.-]{0,63}", iid) else None
            layers = g.get("layers") or {}
            timing = tr.get("timing") or {}
            rec = {
                "instance_id": iid,
                "1_ok": flag(tr.get("ok")), "1_reward_present": reward is not None, "1_reward_skill_vs_O": num(reward),
                "1_trace_errors": [word(e.get("type"), ERROR_WORD) for e in tr.get("errors", []) if isinstance(e, dict)],
                "1_episode_errors": [word(e.get("type"), ERROR_WORD) for e in ep.get("errors", []) if isinstance(e, dict)],
                "2_network_restricted": flag(ph.get("network_restricted")), "2_verifier_box_network_restricted": flag(vb.get("network_restricted")),
                "2_single_use": flag(ph.get("single_use")), "2_item_isolation": word(ph.get("item_isolation"), {"box", "shared"}),
                "3_lab": {k: num(lab.get(k)) for k in ("ticks_used", "resets", "requests", "rejected", "validations", "submissions", "infrastructure_errors")},
                "3_lab_submitted": flag(lab.get("submitted")), "3_tool_calls_by_name": calls,
                "4_submission_source": word(sub.get("source"), SOURCE_WORDS), "4_submission_ok": flag(sub.get("ok")),
                "4_submission_files": num(sub.get("files")), "4_submission_bytes": num(sub.get("bytes")),
                "4_submission_sha256": sub.get("sha256") if isinstance(sub.get("sha256"), str) and HEX64.match(sub["sha256"]) else None,
                "4_submission_error": head(sub.get("error")), "4_stop_condition": word(ph.get("stop_condition"), STOP_WORD), "4_trace_stop_condition": word(tr.get("stop_condition"), STOP_WORD),
                "5_validation_ok": flag((g.get("validation") or {}).get("ok")), "5_n_items": num(g.get("n_items")), "5_n_failed": num(g.get("n_failed")),
                "5_layers": {"rlimits": flag(layers.get("rlimits")), "uid": num(layers.get("uid")), "cleanup": flag(layers.get("cleanup"))},
                "5_isolation": word(g.get("isolation"), {"box", "shared"}), "5_item_boxes": num(g.get("item_boxes")),
                "5_item_box_wall_s_mean": num(g.get("item_box_wall_s_mean")),
                "5_infrastructure_failed_items": num(g.get("infrastructure_failed_items")), "5_skill_vs_O": num(g.get("skill_vs_O")),
                "5_reason": head(g.get("reason")), "5_grading_error": word(ph.get("grading_error"), ERROR_WORD),
                "5_marked_not_an_exam": "NOT_AN_EXAM" in ph, "5_between_item_state_marked": "between_item_state" in ph,
                "5_predictor_uid": num(vb.get("predictor_uid")), "5_container_evidence_count": len(vb.get("container_evidence") or []),
                "6_task_row_keys": sorted(k for k in data if isinstance(k, str) and re.fullmatch(r"[a-z_]{1,32}", k)),
                "6_commitment_is_64_hex": bool(isinstance(data.get("secret_commitment"), str) and HEX64.match(data["secret_commitment"])),
                "7_num_input_tokens": num(tr.get("num_input_tokens")), "7_num_output_tokens": num(tr.get("num_output_tokens")),
                "7_wall_s": {k: num((timing.get(k) or {}).get("end", 0) - (timing.get(k) or {}).get("start", 0))
                             if isinstance(timing.get(k), dict) and num((timing.get(k) or {}).get("end")) is not None
                             and num((timing.get(k) or {}).get("start")) is not None else None
                             for k in ("boot", "setup", "agent", "finalize")},
                "7_verifier_wall_s": num(g.get("verifier_wall_s")),
            }
            if iid:
                hidden = os.path.join(store, iid, "hidden")
                rec["6_hidden_values_in_the_run_folder"] = hidden_hits(run_dir, hidden) if os.path.isfile(os.path.join(hidden, "instance.json")) \
                    else "instance not in the store"
            out["rollouts"].append(rec)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", required=True)
    ap.add_argument("--run-dir", required=True)
    a = ap.parse_args()
    json.dump(report(os.path.abspath(os.path.expanduser(a.store)), os.path.abspath(os.path.expanduser(a.run_dir))), sys.stdout, indent=1)
    sys.stdout.write("\n")
