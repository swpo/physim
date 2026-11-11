"""test_rollout_report -- checks of rollout_report.py. No model, no Docker, no credential; a few seconds.

    python -B rollouts/tools/test_rollout_report.py          # one line per check; exit status 1 if any fails

1. Its numbers against the runner's own files, for the two committed traces: qwen_ring_001 (result.json,
   reference_noise.json: written by extract.py and the runner) and scripted_ring_S (the S row of prove.py's table).
2. The paths that no real trace has exercised yet, on SYNTHETIC traces built here from the Qwen trace: requests
   through the laboratory tool (zero, structured, blind inputs, a rejection), reads outside the workspace, network
   attempts, a long stretch, a failed model call, a reply without a tool call, two tool calls in one reply, a
   predictor that ignores its history, a submission without any laboratory use.
The synthetic traces are written to a temporary folder and are not results of anything.
"""
import contextlib
import copy
import io
import json
import os
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import rollout_report as RR  # noqa: E402

REF = os.path.join(R, "qwen_ring_001", "reference", "proof_pilot.json")
FAILED = []


def check(name, ok, detail=""):
    print(("ok    " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail else ""))
    if not ok:
        FAILED.append(name)


def close(a, b, tol=1e-9):
    return a is not None and b is not None and abs(a - b) <= tol


def run(tmp, name, *args):
    out = os.path.join(tmp, name)
    with contextlib.redirect_stdout(io.StringIO()):
        RR.main(["--reference", REF, "--out", out, *args])
    return json.load(open(out + ".json")), open(out + ".md").read()


NULL_PREDICTOR = '''import numpy as np
POOL = np.load("pool.npz")
def predict(history, program, queries, n_samples, seed):
    rng = np.random.default_rng(seed)
    return {l: POOL[f"level{l}"][rng.integers(0, 100, n_samples)] for l in queries}
'''


def synthetic(base):
    """A rollout that never happened: the first two messages of the Qwen trace, then twelve made-up turns."""
    ep = copy.deepcopy(base)
    tr = ep["traces"][0]
    tr["nodes"], tr["calls"] = tr["nodes"][:2], []
    tr["nodes"][0]["message"]["content"] += " You have at most 40 replies."
    t = [tr["timing"]["agent"]["start"] + 1.0]

    def turn(tool_calls, results, model_s=2.0, tools_s=1.0, error=None):
        calls = [{"id": f"c{len(tr['nodes'])}_{i}", "type": "function", "name": n, "arguments": json.dumps(a)} for i, (n, a) in enumerate(tool_calls)]
        tr["calls"].append({"node": len(tr["nodes"]), "model": "none/synthetic", "finish_reason": "tool_calls" if calls else "stop",
                            "time": {"start": t[0], "end": t[0] + model_s}, "error": error,
                            "usage": None if error else {"prompt_tokens": 100, "completion_tokens": 50, "cached_input_tokens": 900, "cost": 0.001}})
        tr["nodes"].append({"message": {"role": "assistant", "content": "thinking aloud" if not calls else None, "tool_calls": calls}, "sampled": True})
        for c, r in zip(calls, results):
            tr["nodes"].append({"message": {"role": "tool", "tool_call_id": c["id"], "content": r}, "sampled": False})
        t[0] += model_s + tools_s

    def bash(c):
        return ("bash", {"command": c})

    def lab(op, **a):
        return ("lab_call", {"op": op, "args": a})
    ok = lambda r=None: json.dumps({"ok": True, "result": r})  # noqa: E731
    rng = np.random.default_rng(0)
    impulse = np.zeros((8, 24))
    impulse[0, 3] = 0.5
    turn([bash("cat /etc/physim2/lab.json; ls /; env | sort")], ["{}"])                                                          # 1
    turn([bash("curl -s https://example.com/x.tar | tar x; pip install torch")], ["curl: (6) Could not resolve host"])           # 2
    turn([bash("cd /workspace && python -c \"\nimport os, urllib.request\nprint(open('/proc/self/environ').read())\n"
               "print(os.environ.get('PHYSIM2_STORE'))\nurllib.request.urlopen('http://10.0.0.1:8000/x')\n\"")], ["Traceback (most recent call last):\nOSError: no"])  # 3
    turn([lab("reset", label="a")], [ok([0.0] * 6)])                                                                             # 4
    turn([lab("advance", n=16)], [ok([[0.0] * 6] * 16)])                                                                         # 5
    turn([lab("experiment", label="b", inputs=impulse.tolist())], [ok([[0.0] * 6] * 9)])                                         # 6
    turn([lab("experiment", label="c", inputs=(0.05 * rng.normal(size=(8, 24))).tolist())], [ok([[0.0] * 6] * 9)], tools_s=300)  # 7
    turn([lab("advance", inputs=(3.0 * np.ones((4, 24))).tolist())],
         [json.dumps({"ok": False, "error": "violation: 108.0 nats in one tick > 2.0", "kind": "violation"})])                   # 8
    turn([bash("cd /workspace && cat > submission/predict.py << 'EOF'\n" + NULL_PREDICTOR + "EOF"),
          ("edit", {"path": "/workspace/submission/predict.py", "old_str": "0, 100,", "new_str": "0, 64,"})], ["", "ok"])         # 9
    turn([], [])                                                                                                                 # 10
    turn([lab("validate", path="submission")], [ok({"ok": True, "accepted": False})], error=None)                                # 11
    turn([], [], error={"type": "RateLimitError"})                                                                               # 12
    turn([lab("submit", path="submission")], [ok({"ok": True, "accepted": True})])                                               # 13
    tr["timing"]["agent"]["end"] = t[0]
    ph = tr["info"]["physim2"]
    ph["lab"].update(ticks_used=35, resets=3, episodes=3, requests=7, rejected=1, validations=1, submissions=1, submitted=True, total_nats=2.0)
    ph["submission"] = {"source": "agent_submission", "ok": True, "error": None, "files": 1, "bytes": 300, "sha256": "0" * 64}
    ph["grade"].update(L=5.0, skill_vs_O=(ph["grade"]["L_K"] - 5.0) / (ph["grade"]["L_K"] - ph["grade"]["L_O"]), n_failed=3, reason=None)
    tr["rewards"]["skill"]["score"] = ph["grade"]["skill_vs_O"]
    tr["stop_condition"] = ph["stop_condition"] = "frozen"
    tr["id"] = "synthetic"
    return ep


def main():
    q = os.path.join(R, "qwen_ring_001")
    with tempfile.TemporaryDirectory(prefix="rollout-report-test-") as tmp:
        # ---- 1a. the Qwen rollout against the runner's files ----
        rep, md = run(tmp, "qwen", "--trace", os.path.join(q, "trace.redacted.jsonl"), "--model-entry", os.path.join(q, "model_entry.json"),
                      "--lab-record", os.path.join(q, "lab_record.json"), "--items", os.path.join(q, "per_item_scores.json"))
        res, noise = json.load(open(os.path.join(q, "result.json"))), json.load(open(os.path.join(q, "reference_noise.json")))["policies"]
        P, tab = rep["scores"]["policies"], res["table_one_instance"]["policies"]
        check("qwen: L, skill vs O and vs C of every row equal extract.py's table",
              all(close(P[k]["L"], tab[k]["L"]) and close(P[k]["skill_vs_O"], tab[k]["vs_O"]) and close(P[k]["skill_vs_C"], tab[k]["vs_C"]) for k in tab), f"{len(tab)} rows")
        check("qwen: bootstrap se and 5 to 95 % range equal the runner's reference_noise.json (3 decimals)",
              all(close(round(P[k]["boot_se"], 3), noise[k]["se"]) and close(round(P[k]["boot_p05"], 3), noise[k]["p05"]) and close(round(P[k]["boot_p95"], 3), noise[k]["p95"]) for k in noise))
        nb = res["noise_one_instance_bootstrap_over_items"]["mean_loss_minus_reference"]
        check("qwen: the agent's loss minus each policy's, with its range, equals extract.py's",
              all(close(P[k]["agent_minus_policy"]["mean_loss"], nb[k]["point"], 1e-6) and close(P[k]["agent_minus_policy"]["p05"], nb[k]["p05"], 1e-6) for k in nb))
        check("qwen: reward", rep["scores"]["reward_in_trace"] == res["outcome"]["reward_skill_vs_O"] == 0.0)
        u, ru = rep["usage"], res["usage"]
        keys = ["n_calls", "billed_input_tokens", "prompt_tokens_uncached", "cached_input_tokens", "completion_tokens", "cost_usd_all_input_at_full_price",
                "cost_usd_with_cache_read_price", "provider_reported_cost_usd", "cost_usd_for_the_ledger"]
        check("qwen: usage and cost equal extract.py's", all(u[k] == ru[k] for k in keys), ", ".join(f"{k}={u[k]}" for k in keys[-4:]))
        check("qwen: what the caps allowed is the ledger's $1.22", round(u["bound_by_caps_usd"], 2) == 1.22, str(u["bound_by_caps_usd"]))
        w, rw = rep["wall_s"], res["wall_s"]
        check("qwen: wall clock", all(close(round(w[k], 1), rw[k]) for k in ("boot", "setup", "agent", "finalize")) and close(w["agent_model"], rw["agent_split"]["model"]["duration"]))
        tl = rep["timeline"]
        check("qwen: turns and tool calls", len(tl["turns"]) == res["turns"] == 40 and len(tl["rows"]) == sum(res["tool_calls_by_name"].values()))
        check("qwen: model and tool seconds of the turns add up to the agent phase",
              close(sum(t["model_s"] for t in tl["turns"]), rw["agent_split"]["model"]["duration"], 2.5) and
              close(sum(t["model_s"] + t["tools_s"] for t in tl["turns"]), w["agent"], 6.0))
        lr, by = tl["lab_requests"], res["lab_requests_by_op"]
        check("qwen: laboratory log matched to turns: every request has a turn, sums equal the counters",
              all(x["turn"] for x in lr) and sum(x["ticks"] for x in lr) == res["lab"]["ticks_used"] == 306 and len(lr) == res["lab"]["requests"]
              and sum(not x["ok"] for x in lr) == res["lab"]["rejected"] and {o: sum(x["op"] == o for x in lr) for o in by} == {o: v["n"] for o, v in by.items()})
        check("qwen: 18 episodes, all with zero inputs", [e["inputs"] for e in tl["lab_episodes"] if e["episode"]] == ["zero (0 nats charged)"] * 18)
        ids = {f["id"] for f in rep["flags"]}
        check("qwen: flags", ids == {"ended_by_a_cap_or_error", "last_tool_result_never_seen", "lab_errors", "python_errors", "no_graded_submission", "predictor_outside_submission",
                                    "box_differs_from_the_task_row"}, str(sorted(ids)))
        check("qwen: the predictor it wrote (outside submission/) reads its history", rep["predictor_check"]["history"]["reads"] > 0 and rep["predictor_check"]["lines"] > 200)
        check("qwen: the report carries the pilot marker", rep[RR.MARK] is True and RR.MARK in md)
        rep2, _ = run(tmp, "qwen_min", "--trace", os.path.join(q, "trace.redacted.jsonl"))
        check("qwen: with the trace and the reference table alone the score rows are the same (every item failed, so K by rule)",
              all(close(rep2["scores"]["policies"][k]["skill_vs_O"], P[k]["skill_vs_O"]) for k in P) and rep2["usage"].get("cost_usd_for_the_ledger") is None)
        # ---- 1b. a scripted agent: the S rollout of the reference table ----
        s = os.path.join(R, "scripted_ring_S")
        rep, md = run(tmp, "s", "--trace", os.path.join(s, "trace.redacted.jsonl"), "--lab-record", os.path.join(s, "lab_record.json"))
        proof = json.load(open(REF))
        row = proof["per_world"][0]["rollouts"]["S"]
        A = rep["scores"]["policies"]["AGENT"]
        check("scripted S: reward and skill equal the S row of prove.py's table", close(rep["scores"]["reward_in_trace"], row["reward_skill_vs_O"]) and close(A["skill_vs_O"], row["reward_skill_vs_O"])
              and rep["scores"]["reference"]["twin_policy"] == "S" and A["boot_se"] == rep["scores"]["policies"]["S"]["boot_se"], f"{A['skill_vs_O']:.6f}")
        check("scripted S: laboratory counters equal prove.py's", rep["outcome"]["lab"]["ticks_used"] == row["lab_ticks_used"] == 392 and close(rep["outcome"]["lab"]["total_nats"], row["lab_total_nats"])
              and rep["outcome"]["lab"]["requests"] == row["lab_requests"])
        eps = [e for e in rep["timeline"]["lab_episodes"] if e["episode"]]
        check("scripted S: 8 episodes of 49 ticks; nats per episode add up to the counter", len(eps) == 8 and {e["ticks"] for e in eps} == {49} and close(sum(e["nats"] for e in eps), row["lab_total_nats"], 1e-5))
        check("scripted S: wall clock equals prove.py's", close(sum(rep["wall_s"][k] for k in ("boot", "setup", "agent", "finalize", "verifier")), row["wall_s"]["total"], 1e-6))
        check("scripted S: no model, no cost, one flag (2 CPUs in the box, 4 in the task row)", rep["usage"]["n_calls"] == 0 and rep["timeline"]["script"]["exit_code"] == 0
              and [x["id"] for x in rep["flags"]] == ["box_differs_from_the_task_row"])
        # ---- 2. synthetic traces ----
        base = json.loads(open(os.path.join(q, "trace.redacted.jsonl")).readline())
        f = os.path.join(tmp, "synthetic.jsonl")
        json.dump(synthetic(base), open(f, "w"))
        rep, md = run(tmp, "syn", "--trace", f, "--prices", "1,10,0.1", "--long-s", "120")
        rows = rep["timeline"]["rows"]
        k = lambda turn: [r["kinds"] for r in rows if r["turn"] == turn]  # noqa: E731
        d = lambda turn: next(r["detail"] for r in rows if r["turn"] == turn)  # noqa: E731
        check("synthetic: kinds of the laboratory tool calls", (k(4), k(5), k(8), k(11), k(13)) == ([["lab"]], [["lab"]], [["lab"]], [["validate"]], [["submit"]]))
        check("synthetic: input classes zero / structured / blind", (d(5)["inputs"]["class"], d(6)["inputs"]["class"], d(7)["inputs"]["class"]) == ("zero", "structured", "blind"))
        check("synthetic: ticks of the tool requests add up; a rejected request costs nothing", [d(t)["ticks"] for t in (4, 5, 6, 7, 8)] == [1, 16, 9, 9, 0])
        check("synthetic: nats of the impulse = 0.5^2 / (2 * 0.3^2)", close(d(6)["nats"], 0.25 / 0.18, 1e-9), f"{d(6)['nats']:.4f}")
        check("synthetic: a reply without a tool call, and two calls in one reply", k(10) == [["talk"]] and k(9) == [["write"], ["write"]])
        fl = {x["id"]: x for x in rep["flags"]}
        check("synthetic: reads outside the workspace are flagged at turns 1 and 3", fl.get("outside_the_workspace", {}).get("turns") == [1, 3], "; ".join(fl.get("outside_the_workspace", {}).get("items", [])))
        check("synthetic: network attempts are flagged at turns 2 and 3", fl.get("network_attempt", {}).get("turns") == [2, 3], "; ".join(fl.get("network_attempt", {}).get("items", [])))
        check("synthetic: the laboratory's rejection is flagged at turn 8", fl.get("lab_errors", {}).get("turns") == [8])
        check("synthetic: the long stretch is flagged at turn 7", fl.get("long_stretches", {}).get("turns") == [7])
        check("synthetic: a predictor that ignores history and program is flagged (the edit was applied to the tracked file)",
              "predictor_ignores_history" in fl and "predictor_ignores_program" in fl and rep["predictor_check"]["source"].endswith("`submission/predict.py`)") and "predictor_outside_submission" not in fl)
        check("synthetic: no false alarm", not {"ended_by_a_cap_or_error", "submission_without_lab_use", "no_graded_submission", "last_tool_result_never_seen", "lab_use_not_visible"} & set(fl), str(sorted(fl)))
        check("synthetic: a turn cap that the task text states is not marked as untold", [b["note"] for b in rep["budgets"] if b["budget"] == "model turns"] == [""])
        check("synthetic: a failed model call is counted and not priced", rep["usage"]["n_calls_failed"] == 1 and rep["usage"]["n_calls_without_usage"] == 1
              and close(rep["usage"]["cost_usd_all_input_at_full_price"], (12 * 1000 * 1 + 12 * 50 * 10) / 1e6))
        check("synthetic: without per-item scores the agent's row has its mean only", rep["scores"]["agent_per_item_source"] is None and rep["scores"]["policies"]["AGENT"].get("boot_se") is None
              and close(rep["scores"]["policies"]["AGENT"]["L"], 5.0) and "give --items" in md)
        ep = json.loads(open(os.path.join(q, "trace.redacted.jsonl")).readline())
        ph = ep["traces"][0]["info"]["physim2"]
        ph["submission"].update(ok=True, error=None, files=1)
        ph["lab"].update(ticks_used=0)
        json.dump(ep, open(f, "w"))
        rep, _ = run(tmp, "syn2", "--trace", f)
        check("synthetic: a graded submission with 0 laboratory ticks is flagged", {"submission_without_lab_use", "collected_without_submit"} <= {x["id"] for x in rep["flags"]})
        ep = json.loads(open(os.path.join(q, "trace.redacted.jsonl")).readline())      # turn 17 now runs a script the trace never shows
        tr = ep["traces"][0]
        tr["nodes"][tr["calls"][16]["node"]]["message"]["tool_calls"][0]["arguments"] = json.dumps({"command": "cd /workspace && python collect.py"})
        json.dump(ep, open(f, "w"))
        rep, _ = run(tmp, "syn3", "--trace", f, "--lab-record", os.path.join(q, "lab_record.json"))
        r17 = next(r for r in rep["timeline"]["rows"] if r["turn"] == 17)
        rep0, _ = run(tmp, "syn4", "--trace", f)
        check("synthetic: laboratory use hidden in an unseen script is a `lab` turn with the laboratory's log, and unseen without it",
              r17["kinds"] == ["lab"] and r17["detail"]["kinds_from_the_laboratory_log"] == ["lab"] and next(r for r in rep0["timeline"]["rows"] if r["turn"] == 17)["kinds"] == ["other"])
    # ---- 3. the two static readers ----
    cls = lambda code, expr: RR.input_class_static(expr, code)[0]  # noqa: E731
    check("static inputs: integer, zeros, written zeros, random", (cls("", "16"), cls("U = np.zeros((16, 24))\n", "U"), cls("U = np.zeros((16, 24))\nU[0, 3] = 1.0\n", "U"),
                                                                    cls("U = 0.1 * rng.normal(size=(16, 24))\n", "U"), cls("", "n=16"), cls("", "make()")) ==
          ("zero", "zero", "structured", "blind", "zero", "unknown"))
    check("static inputs: two statements on one line; a helper that draws at random",
          (cls("U = np.zeros((32, 24)); U[:, 0:4] = 0.5\n", "U"), cls("def probe(k):\n    return 0.1 * rng.normal(size=(k, 24))\nU = probe(8)\n", "U"),
           cls("def probe(k):\n    u = np.zeros((k, 24))\n    u[0, 3] = 1\n    return u\nU = probe(8)\n", "U")) == ("structured", "blind", "structured"))
    pc = RR.predictor_check("import m\ndef predict(history, program, queries, n_samples, seed):\n    return m.go(history, program['test'], queries, n_samples, seed)\n")
    check("static predictor: passing history to a helper counts as a read", pc["history"]["reads"] == 1 and pc["program"]["reads"] == 1)
    pc = RR.predictor_check("def predict(history, program, queries, n_samples, seed):\n    T = history.shape[0]\n    return {}\n")
    check("static predictor: reading only the shape of history is seen", pc["history"]["shape_only"] and pc["program"]["reads"] == 0)
    print(f"{len(FAILED)} check(s) failed" if FAILED else "all checks passed")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
