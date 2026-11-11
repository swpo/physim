"""exam_pure -- checks of round 4's exam-side changes that touch nothing: pure functions only, under tripwires.

    .venv/bin/python -B tests/exam_pure.py [--trace FILE.jsonl]

tools/tripwires.py is installed before the package is imported: nothing here can start a process, remove,
rename or change a file, or send a signal (a hit fails the run). Covered: the flat rollout config (schema,
defaults, expansion), the profiles, the box measurement parser, the reasoning record (on made-up traces and,
with --trace, on a saved one), the capture's name rules, the ending words, and that tools/run_report.py carries
the grader's list of fallback reasons.
"""
import argparse
import json
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, ROOT)
import tripwires  # noqa: E402

TW = tripwires.install()
import physim2_env  # noqa: E402,F401
import run_report as RR  # noqa: E402
from physim2_env import capture as CAPTURE  # noqa: E402
from physim2_env import grading as GRADING  # noqa: E402
from physim2_env import profiles as PROFILES  # noqa: E402
from physim2_env import rollout_config as RC  # noqa: E402
from physim2_env import taskset as TASKSET  # noqa: E402

CHECKS = []


def check(name, ok, **detail):
    CHECKS.append({"check": name, "ok": bool(ok), **detail})
    print(("ok   " if ok else "FAIL ") + name + ("" if ok else " " + json.dumps(detail, default=str)[:400]), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trace", default=None, help="a saved trace (one JSON line) to compute the reasoning record of")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    good = {"schema": RC.SCHEMA, "instance": "pilot-abc-001", "max_context_tokens": 200000, "cap_usd": 5}
    check("config: the smallest valid file passes, and gets the ring defaults (qwen/qwen3.6-35b-a3b, 150 turns, 60 minutes, 8192 tokens, 4 GB)",
          RC.validate(good) == [] and RC.DEFAULTS == {"model": "qwen/qwen3.6-35b-a3b", "exam_profile": "ring", "max_turns": 150, "max_output_tokens_per_turn": 8192,
                                                      "wall_minutes": 60, "box_memory_gb": 4, "reasoning_effort": "default", "push": False})
    bad = {"unknown key": dict(good, system_prompt="x"), "a table": dict(good, env={"id": "x"}), "an array": dict(good, instance=["pilot-abc-001"]),
           "push true": dict(good, push=True), "turns as bool": dict(good, max_turns=True), "turns 0": dict(good, max_turns=0), "turns 401": dict(good, max_turns=401),
           "wall 181": dict(good, wall_minutes=181), "wall as float": dict(good, wall_minutes=60.5), "memory 4.5": dict(good, box_memory_gb=4.5),
           "memory 0.5": dict(good, box_memory_gb=0.5), "cap 0": dict(good, cap_usd=0), "cap 501": dict(good, cap_usd=501), "cap nan": dict(good, cap_usd=float("nan")),
           "instance not a pilot": dict(good, instance="exam-ring-1"), "instance with a path": dict(good, instance="pilot-../x"), "model with a space": dict(good, model="a/b c"),
           "model with a path": dict(good, model="../etc/passwd"), "profile unknown": dict(good, exam_profile="gliders"), "effort unknown": dict(good, reasoning_effort="ultra"),
           "summary key (removed: the route refused it)": dict(good, reasoning_summary="auto"), "summary key default": dict(good, reasoning_summary="default"),
           "schema other": dict(good, schema="physim2-rollout/v2"), "no schema": {k: v for k, v in good.items() if k != "schema"},
           "no instance": {k: v for k, v in good.items() if k != "instance"}, "no context cap": {k: v for k, v in good.items() if k != "max_context_tokens"},
           "no cap_usd": {k: v for k, v in good.items() if k != "cap_usd"}, "image key": dict(good, image="x:1"), "harness key": dict(good, harness="codex"),
           "not a dict": ["x"]}
    passed = [k for k, v in bad.items() if RC.validate(v) == []]
    check(f"config: {len(bad)} bad files are each refused (unknown keys, tables, arrays, ranges, types, missing required keys)", not passed, passed=passed)
    full = dict(good, model="openai/gpt-6-astra", max_turns=22, max_output_tokens_per_turn=16384, wall_minutes=45, box_memory_gb=2, reasoning_effort="low")
    c = RC.expand(full)
    check("config: expansion puts every limit where verifiers or the task enforces it, and fixes the rest",
          c["model"] == "openai/gpt-6-astra" and c["push"] is False and c["num_rollouts"] == 1 and c["sampling"] == {"max_tokens": 16384, "reasoning_effort": "low"}
          and c["env"]["id"] == "physim2-verifier" and c["env"]["taskset"] == {"id": "physim2-env", "image": "physim2-ring:2", "instances": ["pilot-abc-001"],
                                                                              "task": {"limits": {"max_context_tokens": 200000, "cap_usd": 5.0, "box_cpus": 2.0, "box_memory_gb": 2.0}}}
          and c["env"]["agent"] == {"max_turns": 22, "timeout": {"rollout": 2700.0}, "runtime": {"type": "docker", "cpu": 2.0, "memory": 2.0},
                                    "harness": {"id": "bash", "edit": True, "search": False}, "retries": {"max_retries": 0}}
          and c["env"]["retries"] == {"max_retries": 0} and c["env"]["verifier"] == {"retries": 0}, cfg=c)
    check("config: no token cap of verifiers is set on the whole run (none is disclosed)", not any(k in c["env"]["agent"] for k in ("max_total_tokens", "max_input_tokens",
                                                                                                                              "max_output_tokens")))
    c2 = RC.expand(dict(good, reasoning_effort="high"))
    check("config: an effort travels as `reasoning_effort` alone; no `reasoning` object is ever sent (the summary key was removed)",
          c2["sampling"] == {"max_tokens": 8192, "reasoning_effort": "high"} and "reasoning_summary" not in RC.FLAT_KEYS)
    try:
        RC.expand(dict(good, max_turns=0))
        refused = False
    except ValueError:
        refused = True
    check("config: expand refuses what validate refuses", refused)
    t = PROFILES.table()
    check("profiles: the ring profile: 64 items, 256 samples per item, 400 ticks, a reset costs 17, image 2, six reference policies",
          len(t) == 1 and t[0]["profile"] == "ring" and t[0]["items"] == 64 and t[0]["samples_per_item"] == 256 and t[0]["lab_ticks"] == 400 and t[0]["reset_cost_ticks"] == 17
          and t[0]["image"] == "physim2-ring:2" and t[0]["reference_policies"] == ["null", "D", "P0", "PM", "S", "C"] and t[0]["exam_config"] == "ring_r4", table=t)
    capped = TASKSET.parse_box("/sys/fs/cgroup/cpu.max=200000 100000 \n/sys/fs/cgroup/memory.max=4294967296 \n/sys/fs/cgroup/pids.max=512 \nnproc=2\n"
                               "workspace=tmpfs 1048576\ntmp=tmpfs 524288\nrootfs=ro,relatime,lowerdir=/x")
    free = TASKSET.parse_box("/sys/fs/cgroup/cpu.max=max 100000 \n/sys/fs/cgroup/memory.max=max \n/sys/fs/cgroup/pids.max=max \nnproc=4\nworkspace=overlay 263174212\n"
                             "tmp=overlay 263174212\nrootfs=rw,relatime")
    v1 = TASKSET.parse_box("/sys/fs/cgroup/cpu.max=absent \n/sys/fs/cgroup/cpu/cpu.cfs_quota_us=150000 \n/sys/fs/cgroup/cpu/cpu.cfs_period_us=100000 \n"
                           "/sys/fs/cgroup/memory/memory.limit_in_bytes=2147483648 \n/sys/fs/cgroup/pids/pids.max=100 \n")
    check("box: a capped box is read as 2 CPUs, 4 GiB, 512 processes, 1024 and 512 MiB of memory-backed space, read-only root",
          {k: capped[k] for k in ("cpus", "memory_gib", "pids", "workspace_mib", "tmp_mib", "read_only_root")} == {
              "cpus": 2.0, "memory_gib": 4.0, "pids": 512, "workspace_mib": 1024.0, "tmp_mib": 512.0, "read_only_root": True}, capped=capped)
    check("box: an uncapped box is read as no limits (the size of a shared disk is nobody's quota)",
          {k: free[k] for k in ("cpus", "memory_gib", "pids", "workspace_mib", "tmp_mib", "read_only_root")} == {
              "cpus": None, "memory_gib": None, "pids": None, "workspace_mib": None, "tmp_mib": None, "read_only_root": False}, free=free)
    check("box: cgroup v1 files are read too, and garbage gives no limits rather than an error", v1["cpus"] == 1.5 and v1["memory_gib"] == 2.0 and v1["pids"] == 100
          and TASKSET.parse_box("garbage\n=\n\x00")["cpus"] is None)

    def trace(calls, nodes, sampling=None):
        return {"agent": {"config": {"sampling": sampling or {}}}, "calls": calls, "nodes": nodes}
    node = lambda **m: {"sampled": True, "message": m}  # noqa: E731
    r = TASKSET.reasoning_record(trace(
        [{"sampling": {"max_tokens": 9, "reasoning_effort": "high"}, "usage": {"reasoning_tokens": 40}}, {"sampling": {"reasoning": {"summary": "auto", "effort": "low"}},
                                                                                                         "usage": {"reasoning_tokens": 0}}, {"sampling": {}, "usage": None}],
        [{"sampled": False, "message": {"role": "user"}}, node(reasoning_content="thinking"), node(provider_state=[{"type": "reasoning.encrypted"}]),
         node(provider_state=[{"type": "reasoning.encrypted"}, {"type": "reasoning.summary"}]), node(content="plain")], {"reasoning_effort": "high"}))
    check("reasoning: requested effort, what each call was sent, and replies by kind (readable, encrypted only, none)",
          r["requested_effort"] == "high" and r["sent_effort"] == ["high", "low"] and r["sent_summary"] == ["auto"] and r["replies"] == 4
          and r["replies_with_readable_reasoning"] == 2 and r["replies_with_encrypted_reasoning_only"] == 1 and r["replies_without_reasoning"] == 1
          and r["reasoning_tokens"] == 40 and r["calls_with_reasoning_tokens"] == 1 and r["reasoning_on"] is True, record=r)
    r0 = TASKSET.reasoning_record(trace([], []))
    check("reasoning: a run without a model call records nothing asked and nothing seen", r0["replies"] == 0 and r0["reasoning_on"] is None and r0["requested_effort"] is None)
    rx = TASKSET.reasoning_record(trace([{"sampling": {"reasoning_effort": "x" * 99 + " <script>"}, "usage": {}}], [node(content="a")], {"reasoning_effort": "DROP TABLE; --"}))
    check("reasoning: a value that is not a plain word is never copied into the record", rx["requested_effort"] is None and rx["sent_effort"] is None)
    if a.trace:
        with open(a.trace) as f:
            tr = json.loads(f.readline())
        tr = tr["traces"][0] if "traces" in tr else tr
        rr = TASKSET.reasoning_record(tr)
        check("reasoning: the saved trace of rollout astra_ring_001: 14 replies, 8 with readable reasoning, 4 with encrypted reasoning only, 2 without; 5,242 reasoning tokens",
              rr["replies"] == 14 and rr["replies_with_readable_reasoning"] == 8 and rr["replies_with_encrypted_reasoning_only"] == 4 and rr["replies_without_reasoning"] == 2
              and rr["reasoning_tokens"] == 5242 and rr["requested_effort"] is None and rr["reasoning_on"] is True, record=rr)
    kept = [CAPTURE.safe_parts(n, r) for n, r in (("workspace/submission/a.py", "/workspace/submission"), ("./notes/x y.txt", ""), ("r/..../x", "r"))]
    no = [CAPTURE.safe_parts(n, r)[1] for n, r in (("/abs", ""), ("a/../b", ""), ("workspace/other/a", "workspace/submission"), ("workspace/submission", "workspace/submission"),
                                                    ("/".join(["d"] * 40), ""))]
    check("capture: the name rules (pure): kept names are rewritten to safe characters; absolute, parent, foreign, empty and too deep names are refused",
          kept == [(["a.py"], None), (["notes", "x_y.txt"], None), (["____", "x"], None)]
          and no == ["absolute path", "parent path", "outside the root", "empty name", "too deep"], kept=kept, no=no)
    T = types.SimpleNamespace
    E = TASKSET.Physim2Task._ending
    check("endings: the fixed words", [E(T(stop_condition=s), lab) for s, lab in (("agent_completed", {"submitted": True}), ("max_turns", {}), ("agent_timeout", {}),
                                                                                 ("timeout", {}), ("max_total_tokens", {}), ("agent_completed", {}), ("spend_cap", {}),
                                                                                 ("max_context_tokens", {}), ("model_request_refused", {}), (None, {}))]
          == ["submit", "turn limit", "time limit", "time limit", "token limit", "the agent stopped", "spend limit", "context limit", "stopped", "ended"])
    check("run report: its copy of the grader's fallback reasons equals grading.FALLBACK_REASONS, and it knows every ending word",
          tuple(RR.FALLBACK_REASONS) == tuple(GRADING.FALLBACK_REASONS) and RR.head("no predict.py") == "no predict.py"
          and RR.head("validation failed: timed out") == "validation failed: timed out" and RR.head("submission has no predict.py") == "submission has no predict.py"
          and RR.head("Traceback: secret text of a predictor").startswith("(other,") and {"submit", "turn limit", "time limit", "failed run"} <= RR.ENDED_WORDS)
    fbk = RR.fallback({"policy": "null", "n_items": 3, "by_reason": {"raised": 2, "text chosen by an agent": 1}, "baseline_pool_sha256": "0" * 64})
    check("run report: fallback counts are printed by the grader's words only; any other key is counted as (other)", fbk["by_reason"] == {"raised": 2, "(other)": 1})
    check("run report: the turns of a saved trace are its sampled nodes (verifiers does not save num_turns; the round-4 rehearsal's report printed null)",
          RR.num_turns({"nodes": [{"sampled": True}, {"sampled": False}, {"sampled": True}, {}, "x"]}) == 2 and RR.num_turns({"num_turns": 7, "nodes": []}) == 7
          and RR.num_turns({}) is None)
    check("tripwires: nothing in this run tried to start, remove, move or change anything", TW.hits == [], hits=TW.hits[:5])
    out = {"tool": "tests/exam_pure.py", "where": "the worker, under tools/tripwires.py", "n_checks": len(CHECKS), "n_passed": sum(c["ok"] for c in CHECKS),
           "failed": [c["check"] for c in CHECKS if not c["ok"]], "tripwire_names": len(TW.names), "tripwire_hits": TW.hits, "checks": CHECKS}
    if a.out:
        with open(a.out, "w") as f:
            json.dump(out, f, indent=1, default=str)
    print(json.dumps({k: out[k] for k in ("n_checks", "n_passed", "failed")}))
    return 0 if out["n_checks"] == out["n_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
