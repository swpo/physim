"""check_round4_step3 -- section D of tools/check_round4.py: the request, the strict config schema, the lead's
standing go, the ledger, the instance register, the price bounds and the publication folder.

Imported by tools/check_round4.py AFTER its tripwires are installed; `run(check, raises, scratch)` uses that
tool's two helpers. Everything works on files this test writes into `scratch` and leaves there; the listing of
models comes from the stand-in of tools/standin_model.py in a thread of this process. Nothing is started.
"""
import datetime
import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

FLAT = '''schema = "physim2-rollout/v1"
model = "standin/echo-1"
exam_profile = "ring"
instance = "pilot-d-test-001"
max_turns = 12
max_output_tokens_per_turn = 512
max_context_tokens = 20000
wall_minutes = 10
box_memory_gb = 2
cap_usd = 0.5
reasoning_effort = "default"
push = false
'''


def run(check, raises, scratch):
    import check_config as CC
    import check_request as CR
    import pack_rollout as PK
    import standin_model
    tag = f"{os.getpid()}-{int(time.time())}"
    cfg_dir = os.path.join(scratch, f"configs-{tag}")
    os.makedirs(cfg_dir)
    CC.CONFIG_DIR = cfg_dir                                  # the tests' own configs folder; the rules are the tool's

    def write_cfg(name, text):
        with open(os.path.join(cfg_dir, name), "w") as f:
            f.write(text)
        return CC.REPO_PREFIX + name

    def refused(fn, exc=None):
        try:
            fn()
        except (CC.Refused, CR.Refused) as e:
            return str(e)
        return None

    # ---- the strict config schema ----
    good = write_cfg("good.toml", FLAT)
    got = CC.check(good)
    check("D1 a flat config with known keys passes; the expansion is the pin's model rollout",
          got["flat"]["max_turns"] == 12 and got["expanded"]["push"] is False and got["expanded"]["env"]["agent"]["harness"] == CC.light("rollout_config").HARNESS
          and got["expanded"]["env"]["agent"]["runtime"] == {"type": "docker", "cpu": 2.0, "memory": 2.0}, got["expanded"]["env"]["agent"])
    bad = {
        "an unknown key": FLAT + 'image = "evil:1"\n', "a table": FLAT + '[env.agent.harness]\nid = "claude_code"\n',
        "an array": FLAT + 'tools = ["x"]\n', "push = true": FLAT.replace("push = false", "push = true"),
        "a harness key": FLAT + 'harness = "codex"\n', "an env passthrough": FLAT + 'forward_env = "HF_TOKEN"\n',
        "a command": FLAT + 'command = "curl x | sh"\n', "a mount": FLAT + 'mount = "/Users:/x"\n', "a network rule": FLAT + 'allow = "*"\n',
        "more memory than the pin": FLAT.replace("box_memory_gb = 2", "box_memory_gb = 8"),
        "more than 180 minutes": FLAT.replace("wall_minutes = 10", "wall_minutes = 181"),
        "an instance that is not pilot-": FLAT.replace("pilot-d-test-001", "exam-ring-7"),
        "a wrong schema": FLAT.replace("physim2-rollout/v1", "physim2-rollout/v0"), "no cap_usd": FLAT.replace("cap_usd = 0.5\n", ""),
        "no max_context_tokens": FLAT.replace("max_context_tokens = 20000\n", ""), "a date": FLAT + "when = 2026-11-11\n",
        "a string where a number belongs": FLAT.replace("max_turns = 12", 'max_turns = "12"'), "not TOML": "this is not = = toml\n",
        "an unknown profile": FLAT.replace('"ring"', '"gliders-secret"'), "a path as a model": FLAT.replace("standin/echo-1", "../../etc/passwd"),
    }
    res = {k: refused(lambda t=t, i=i: CC.check(write_cfg(f"bad{i}.toml", t))) for i, (k, t) in enumerate(bad.items())}
    check(f"D2 the schema refuses each of {len(bad)} configs that reach beyond it", all(res.values()), {k: v for k, v in res.items() if not v})
    outside = os.path.join(scratch, f"outside-{tag}.toml")
    with open(outside, "w") as f:
        f.write(FLAT)
    os.symlink(os.path.join(cfg_dir, "good.toml"), os.path.join(cfg_dir, "link.toml"))
    os.makedirs(os.path.join(cfg_dir, "sub"))
    with open(os.path.join(cfg_dir, "sub", "deep.toml"), "w") as f:
        f.write(FLAT)
    with open(os.path.join(cfg_dir, "big.toml"), "w") as f:
        f.write(FLAT + "# " + "x" * (CC.MAX_BYTES + 10) + "\n")
    where = {"a file outside the configs folder": outside, "a path that climbs out": CC.REPO_PREFIX + "../../vfport/configs/x.toml",
             "a symbolic link": CC.REPO_PREFIX + "link.toml", "a sub-folder": CC.REPO_PREFIX + "sub/deep.toml",
             "a missing file": CC.REPO_PREFIX + "nope.toml", "an upper-case name": CC.REPO_PREFIX + "Good.toml",
             "another extension": CC.REPO_PREFIX + "good.json", "too large": CC.REPO_PREFIX + "big.toml", "an empty path": ""}
    res = {k: refused(lambda v=v: CC.check(v)) for k, v in where.items()}
    check(f"D3 ... and each of {len(where)} files that are not a plain small file directly in round6/rollouts/configs/", all(res.values()), {k: v for k, v in res.items() if not v})
    RC = CC.light("rollout_config")
    exp = RC.expand({k: v for k, v in got["flat"].items()})
    tampered = {"another harness": lambda e: e["env"]["agent"]["harness"].update(id="codex"), "search on": lambda e: e["env"]["agent"]["harness"].update(search=True),
                "an env passthrough": lambda e: e["env"]["agent"]["harness"].update(forward_env=["HF_TOKEN"]),
                "another image": lambda e: e["env"]["taskset"].update(image="python:3.12"), "a retry": lambda e: e["env"]["agent"]["retries"].update(max_retries=3),
                "a client": lambda e: e.update(client={"base_url": "http://x"}), "push": lambda e: e.update(push=True),
                "a tool server url": lambda e: e["env"]["taskset"].setdefault("task", {}).update(tools={"url": "http://x"}),
                "a system prompt file": lambda e: e["env"]["taskset"].update(system_prompt="../x.txt"), "two rollouts": lambda e: e.update(num_rollouts=2),
                "another runtime": lambda e: e["env"]["agent"]["runtime"].update(type="subprocess"), "a gpu": lambda e: e["env"]["agent"]["runtime"].update(gpu="1")}
    res = {}
    for k, fn in tampered.items():
        e = json.loads(json.dumps(exp))
        fn(e)
        res[k] = bool(CC.fixed_violations(e, got["flat"], RC, CC.light("profiles")))
    check(f"D4 an expansion that differs from the pin's model rollout in any of {len(tampered)} ways is caught, independently of expand()",
          all(res.values()) and CC.fixed_violations(exp, got["flat"], RC, CC.light("profiles")) == [], res)
    sch = CC.schema()
    check("D5 the schema as data: the keys, the fixed part, the forbidden fields and the exam profiles with their item counts",
          set(sch["keys"]) == set(RC.FLAT_KEYS) and sch["fixed_by_the_pin"]["push"] is False and "forward_env" in sch["forbidden_fields"]
          and [(r["profile"], r["items"]) for r in sch["exam_profiles"]] == [("ring", 64)] and sch["exam_profiles"][0]["reference_policies"], sch["exam_profiles"])

    # ---- the request ----
    pin, pin_sha = "ab" * 20, CR.pin_sha256()
    req = {"schema": "rollout-job/v1", "job_id": f"d-test-{tag}"[:40], "purpose": "a test of the request route", "requester": "fixer B",
           "pin": pin, "pin_sha256": pin_sha, "config": good, "exam_profile": "ring", "instance": "pilot-d-test-001", "model": "standin/echo-1",
           "caps": {"max_turns": 12, "max_output_tokens": 512, "wall_minutes": 10, "box_memory_gb": 2}, "cap_usd": 0.5}
    check("D6 a well-formed request passes its own shape check", CR.validate_request(req) == [], CR.validate_request(req))
    variants = {"an extra key": dict(req, command="x"), "a missing key": {k: v for k, v in req.items() if k != "pin"},
                "another schema": dict(req, schema="rollout-job/v2"), "a short pin": dict(req, pin="abc"), "a pin_sha256 that is not hex": dict(req, pin_sha256="z" * 64),
                "a job id with a slash": dict(req, job_id="../x"), "an instance that is not pilot-": dict(req, instance="exam-1"),
                "an extra cap": dict(req, caps=dict(req["caps"], gpus=1)), "180 minutes exceeded": dict(req, caps=dict(req["caps"], wall_minutes=181)),
                "memory above the pin": dict(req, caps=dict(req["caps"], box_memory_gb=6)), "a negative cap": dict(req, cap_usd=-1),
                "a cap that is true": dict(req, cap_usd=True), "caps as a list": dict(req, caps=[1, 2]), "a control character": dict(req, purpose="a\nb"),
                "not an object": [req]}
    res = {k: bool(CR.validate_request(v)) for k, v in variants.items()}
    check(f"D7 each of {len(variants)} malformed requests is refused", all(res.values()), {k: v for k, v in res.items() if not v})
    rp = os.path.join(scratch, f"req-{tag}.json")
    with open(rp, "w") as f:
        json.dump(req, f)
    r = CR.read_request(rp)
    check("D8 the pin: the sha256 of this checkout's PIN.sha256 and the commit must both be the request's",
          CR.check_pin(r, head=pin)["pin"] == pin and refused(lambda: CR.check_pin(r, head="cd" * 20))
          and refused(lambda: CR.check_pin(dict(r, pin_sha256="0" * 64), head=pin)))
    check("D9 request and config must agree on profile, instance, model, the four caps and cap_usd",
          CR.check_config(r)["name"] == "good.toml" and all(refused(lambda v=v: CR.check_config(v)) for v in (
              dict(r, model="other/model"), dict(r, instance="pilot-other-001"), dict(r, cap_usd=0.6), dict(r, caps=dict(r["caps"], max_turns=13)),
              dict(r, caps=dict(r["caps"], max_output_tokens=1024)), dict(r, caps=dict(r["caps"], wall_minutes=11)),
              dict(r, caps=dict(r["caps"], box_memory_gb=4)), dict(r, exam_profile="gliders"))))

    # ---- the pilot folder: go, ledger, instances ----
    pilot = os.path.join(scratch, f"pilot-{tag}")
    os.mkdir(pilot, 0o700)
    os.mkdir(os.path.join(pilot, "store"), 0o700)
    p = dict(CR.require_pilot(pilot), **CR.pilot_paths(pilot, r["job_id"]))
    loose = os.path.join(scratch, f"loose-{tag}")
    os.mkdir(loose, 0o755)
    check("D10 the pilot folder must be a 0700 directory of this user", refused(lambda: CR.require_pilot(loose)) and refused(lambda: CR.require_pilot(loose + "-none")))
    today = datetime.date(2026, 11, 11)
    check("D11 no standing go, no step 3", "no LEAD-GO-MODEL-SPEND.json" in (refused(lambda: CR.read_go(p, today)) or ""))

    def go(obj):
        with open(p["go"], "w") as f:
            json.dump(obj, f)
    bad_go = {"another schema": {"schema": "x", "ceiling_usd": 5, "date": "2026-11-11"}, "no ceiling": {"schema": CR.GO_SCHEMA, "date": "2026-11-11"},
              "a ceiling of zero": {"schema": CR.GO_SCHEMA, "ceiling_usd": 0, "date": "2026-11-11"}, "an extra key": {"schema": CR.GO_SCHEMA, "ceiling_usd": 5, "date": "2026-11-11", "run": "now"},
              "a date in the future": {"schema": CR.GO_SCHEMA, "ceiling_usd": 5, "date": "2026-12-24"}, "a date 31 days old": {"schema": CR.GO_SCHEMA, "ceiling_usd": 5, "date": "2026-10-11"},
              "not a date": {"schema": CR.GO_SCHEMA, "ceiling_usd": 5, "date": "yesterday"}, "a list": [1]}
    res = {}
    for k, v in bad_go.items():
        go(v)
        res[k] = bool(refused(lambda: CR.read_go(p, today)))
    go({"schema": CR.GO_SCHEMA, "ceiling_usd": 1.0, "date": "2026-11-11"})
    g = CR.read_go(p, today)
    check(f"D12 the go file: {len(bad_go)} wrong forms are refused; a ceiling and a date of the last 30 days pass", all(res.values()) and g == {"ceiling_usd": 1.0, "date": "2026-11-11"}, res)

    s = standin_model.Standin([{"say": "x"}]).start()
    entry = CR.fetch_model_entry("standin/echo-1", s.base_url)
    prices = CR.prices_of(entry)
    b = CR.bounds(got["flat"], prices)
    worst = (20000 * 2.0 + 512 * 10.0) / 1e6
    check("D13 listed prices, fetched without a credential: one worst-case call = 20,000 x $2/M + 512 x $10/M = $0.04512",
          abs(b["worst_call_usd"] - worst) < 1e-12 and abs(b["bound_usd"] - 0.5 - worst) < 1e-12 and prices["cache_read"] == 0.5 and prices["context_window"] == 100000
          and not s.requests, b)
    check("D14 the crude bound, turns x (context WINDOW x input + reply x output): 12 x (100,000 x $2/M + 512 x $10/M) = $2.46",
          abs(b["crude_bound_usd"] - 12 * (100000 * 2.0 + 512 * 10.0) / 1e6) < 1e-9, b["crude_bound_usd"])
    check("D15 a cap below one worst-case call is refused; so is a context cap above the model's window, and an unlisted model",
          refused(lambda: CR.bounds(dict(got["flat"], cap_usd=0.04), prices)) and refused(lambda: CR.bounds(dict(got["flat"], max_context_tokens=200000), prices))
          and refused(lambda: CR.fetch_model_entry("not/listed", s.base_url)) and refused(lambda: CR.fetch_model_entry("m", "http://example.org/v1"))
          and refused(lambda: CR.prices_of({"entry": {"pricing": {"input_usd_per_mtok": 1.0}, "context_window": 5}})))
    s.stop()
    check("D16 an empty ledger sums to zero, and this run's bound fits under a ceiling of $1", CR.check_ceiling(p, g, b)["sum_usd"] == 0.0)
    CR.ledger_append(p, {"event": "reserved", "job_id": "earlier-1", "bound_usd": 0.4, "billed": True})
    open_sum = CR.ledger_sum(CR.ledger_rows(p))
    check("D17 a job that was reserved and never closed counts at its whole bound: 0.4 + 0.545 fits under $1",
          abs(open_sum["sum_usd"] - 0.4) < 1e-12 and open_sum["counted_at_their_bound"] == ["earlier-1"] and CR.check_ceiling(p, g, b)["after_this_run_at_most_usd"] < 1.0)
    CR.ledger_append(p, {"event": "ended", "job_id": "earlier-1", "status": "done", "counted_usd": 0.1, "count_complete": True})
    CR.ledger_append(p, {"event": "reserved", "job_id": "earlier-2", "bound_usd": 0.3, "billed": True})
    CR.ledger_append(p, {"event": "ended", "job_id": "earlier-2", "status": "cut", "counted_usd": 0.05, "count_complete": False})
    CR.ledger_append(p, {"event": "reserved", "job_id": "standin-1", "bound_usd": 50.0, "billed": False})
    sm = CR.ledger_sum(CR.ledger_rows(p))
    check("D18 a closed job counts what was counted (0.1); a cut job without a complete count stays at its bound (0.3); a stand-in run counts nothing",
          abs(sm["sum_usd"] - 0.4) < 1e-12 and sm["counted_at_their_bound"] == ["earlier-2"], sm)
    CR.ledger_append(p, {"event": "reserved", "job_id": "earlier-3", "bound_usd": 0.2, "billed": True})
    check("D19 the ceiling: 0.6 in the ledger plus this run's bound of 0.545 would exceed $1 -> refused", bool(refused(lambda: CR.check_ceiling(p, g, b))))
    check("D20 a job id that the ledger holds is never run again", refused(lambda: CR.check_job_is_new(p, dict(r, job_id="earlier-2"))) and CR.check_job_is_new(p, r) is None)
    st = CR.check_instance(p, r, must_exist=False)
    CR.register_instance(p, r)
    check("D21 an instance name is new before it is made; once registered it belongs to its job",
          st == {"job": None, "in_index": False, "in_store": False} and refused(lambda: CR.check_instance(p, r, must_exist=False))
          and refused(lambda: CR.check_instance(p, dict(r, job_id="another-job"), must_exist=False))
          and refused(lambda: CR.check_instance(p, dict(r, job_id="another-job"), must_exist=True))
          and refused(lambda: CR.check_instance(p, r, must_exist=True)))
    with open(os.path.join(p["store"], "index.json"), "w") as f:
        json.dump([{"instance_id": "pilot-d-test-001"}, {"instance_id": "pilot-stray-001"}], f)
    os.makedirs(os.path.join(p["store"], "pilot-d-test-001", "hidden"))
    check("D22 ... and passes as this job's instance once the store holds it; a name the store holds unregistered is refused for everybody",
          CR.check_instance(p, r, must_exist=True)["in_index"] and refused(lambda: CR.check_instance(p, dict(r, instance="pilot-stray-001"), must_exist=False)))

    # ---- the spend log's total ----
    log = os.path.join(scratch, f"spendlog-{tag}.jsonl")
    with open(log, "w") as f:
        for row in ({"event": "meter", "worst_call_usd": 0.04512, "bound_on_the_bill_usd": 0.54512, "billed": False},
                    {"event": "sent", "n": 1}, {"event": "settled", "n": 1, "usd": 0.002, "basis": "usage at the listed prices"},
                    {"event": "sent", "n": 2}, {"event": "settled", "n": 2, "usd": 0.04512, "basis": "worst case: no usage reported"},
                    {"event": "sent", "n": 3}, {"event": "refused", "condition": "spend_cap"}):
            f.write(json.dumps(row) + "\n")
    t = CR.spend_log_total(log)
    check("D23 a spend log with an attempt that never settled: counted = settled + one worst case for it, and the count is not complete",
          abs(t["counted_usd"] - (0.002 + 0.04512 + 0.04512)) < 1e-12 and t["never_settled"] == 1 and t["complete"] is False and t["worst_case_calls"] == 2
          and t["stopped"] == "spend_cap" and t["within_bound"], t)
    check("D24 no spend log: nothing was counted because nothing could be sent", CR.spend_log_total(log + ".none") == {"present": False, "counted_usd": None, "attempts": 0, "complete": False})

    # ---- the publication folder, from a made-up job folder ----
    job, hidden = p["job"], os.path.join(p["store"], "pilot-d-test-001", "hidden")
    trace_id = "a" * 32
    os.makedirs(os.path.join(p["run_dir"]))
    os.makedirs(os.path.join(hidden, "labs", trace_id))
    os.makedirs(os.path.join(hidden, "grades"))
    final = os.path.join(p["store"], "pilot-d-test-001", "captures", trace_id, "final")
    os.makedirs(os.path.join(final, "submission"))
    fake_key, team = "pk-test-" + "Z9" * 20, "team-test-0123456789"
    env = {"PRIME_API_KEY": fake_key, "PRIME_TEAM_ID": team}
    with open(os.path.join(hidden, "instance.json"), "w") as f:
        json.dump({"secret_hex": "5e" * 32, "theta": [0.2311345678, 0.0344456789], "theta_names": ["D", "gamma"], "world": "ring"}, f)
    trace = {"id": trace_id, "ok": True, "is_completed": True, "stop_condition": "spend_cap", "errors": [], "timing": {"start": 100.0, "agent": {"start": 100.0, "end": 160.0}},
             "rewards": {"skill": {"score": 0.42, "weight": 1.0}}, "tools": [{"name": "bash", "description": "run", "parameters": {}}],
             "task": {"data": {"instance_id": "pilot-d-test-001", "secret_commitment": "c0" * 32}},
             "agent": {"config": {"headers": {"X-Prime-Team-ID": team, "Authorization": "Bearer abcdefghijklmnopqrstuvwxyz012345"}, "api_key_var": "PRIME_API_KEY"}},
             "nodes": [{"timestamp": 101.0, "message": {"role": "user", "content": f"task text; store at {pilot}/store"}},
                       {"timestamp": 105.0, "sampled": True, "message": {"role": "assistant", "content": "I will look.", "tool_calls": [{"id": "c1", "name": "bash", "arguments": "{\"command\": \"ls\\n```\\nrm -rf /\"}"}]}},
                       {"timestamp": 106.0, "message": {"role": "tool", "tool_call_id": "c1", "name": "bash", "content": "TASK.md\n"}}],
             "calls": [{"node": 1, "usage": {"prompt_tokens": 900, "completion_tokens": 30}, "finish_reason": "tool_calls"}],
             "info": {"physim2": {"lab": {"ticks_used": 17}, "box_caps": {"cpus": 2}, "grade": {"skill_vs_O": 0.42, "n_failed": 1, "valid_cells": [True]},
                                  "submission": {"source": "final_collection", "ok": True}, "lab_bearer_required": True}}}
    with open(os.path.join(p["run_dir"], "traces.jsonl"), "w") as f:
        f.write(json.dumps({"traces": [trace]}) + "\n")
    with open(os.path.join(hidden, "labs", trace_id, "log.jsonl"), "w") as f:
        f.write(json.dumps({"t": 1.0, "op": "reset", "ok": True, "kind": None, "error": None, "detail": None, "ticks": 17, "ticks_used": 17, "total_nats": 0.0, "seconds": 0.1}) + "\n")
        f.write(json.dumps({"t": 2.0, "op": "advance", "ok": False, "kind": "infrastructure", "error": "infrastructure error", "detail": f"Traceback ... {pilot}/store/x.py", "ticks": 0, "ticks_used": 17, "total_nats": 0.0, "seconds": 0.1}) + "\n")
    with open(os.path.join(hidden, "grades", trace_id + ".json"), "w") as f:
        json.dump({"name": trace_id, "n_items": 2, "n_failed": 1, "errors": ["Traceback: the predictor said something"], "detail": "free text",
                   "fallback_items": [{"item": 1, "reason": "raised"}], "fallback": {"policy": "null"}}, f)
    import numpy as np
    np.savez(os.path.join(hidden, "grades", trace_id + ".npz"), es=np.array([[1.0, 2.0], [3.0, 4.0]]), failed=np.array([False, True]), cpu=np.array([0.1, 0.0]))
    with open(os.path.join(final, "submission.json"), "w") as f:
        json.dump({"n_files": 2, "bytes": 30, "n_skipped": 0, "complete": True, "archive": "ok"}, f)
    with open(os.path.join(final, "submission", "predict.py"), "w") as f:
        f.write("def predict(*a):\n    return {}\n")
    with open(os.path.join(final, "submission", "notes.txt"), "w") as f:
        f.write("my key is " + fake_key + "\n")
    with open(p["request"], "w") as f:
        json.dump(req, f)
    for name, text in ((p["config"], FLAT), (p["resolved"], 'model = "standin/echo-1"\n'), (p["reference"], json.dumps({"all_graded": True, "pooled": {}})),
                       (p["model_entry"], json.dumps(entry)), (os.path.join(job, "vf-eval.log"), "a log line with " + fake_key + "\n")):
        with open(name, "w") as f:
            f.write(text)
    with open(p["spend_log"], "w") as f:
        f.write(open(log).read())
    with open(p["status"], "w") as f:
        json.dump({"stages": {"rollout": {"ended": True, "status": "done"}}}, f)
    CR.ledger_append(p, {"event": "reserved", "job_id": r["job_id"], "bound_usd": 0.54512, "cap_usd": 0.5, "worst_call_usd": 0.04512, "billed": False})
    out = PK.pack(rp, pilot, environ=env)
    folder = out["out"]
    man = json.load(open(os.path.join(folder, "MANIFEST.json")))
    names = sorted(x["path"] for x in man["files"])
    want = ["PILOT_NEVER_REUSE_AS_EXAM.txt", "config.toml", "grades.json", "key_scan.json", "lab_log.jsonl", "model_entry.json", "reference.json", "request.json",
            "resolved.toml", "status.json", "submission.json", "submission/predict.py", "trace.redacted.jsonl", "transcript.md", "usage.json"]
    check("D25 the publication folder holds the files of the protocol, each with sha256 and size in MANIFEST.json",
          names == want and all(len(x["sha256"]) == 64 and x["bytes"] == os.path.getsize(os.path.join(folder, x["path"])) for x in man["files"]), names)
    left = {x["file"]: x["why"] for x in man["left_out"]}
    check("D26 a file that holds the key's VALUE is left out and listed (here: a submission file the agent wrote)",
          "submission/notes.txt" in left and "PRIME_API_KEY" in left["submission/notes.txt"] and not os.path.exists(os.path.join(folder, "submission", "notes.txt")), left)
    blob = b"".join(open(os.path.join(folder, *x["path"].split("/")), "rb").read() for x in man["files"]) + open(os.path.join(folder, "MANIFEST.json"), "rb").read()
    check("D27 no published byte holds the key, the team id, the pilot folder's path, the instance's secret or a hidden parameter",
          fake_key.encode() not in blob and team.encode() not in blob and pilot.encode() not in blob and b"5e5e5e5e" not in blob and b"0.23113456" not in blob)
    ks = json.load(open(os.path.join(folder, "key_scan.json")))
    check("D28 the key scan reports names and counts only, also for the job folder's own files (the log with the key in it)",
          ks["verdict"].startswith("HITS") and [x["file"] for x in ks["job_folder_files_with_a_credential"]] == ["vf-eval.log"]
          and fake_key not in json.dumps(ks) and ks["machine_details_replaced"] >= 1, ks)
    tr_left = "trace.redacted.jsonl" in left
    stat = json.load(open(os.path.join(folder, "status.json")))
    check("D29 status.json: the stop condition, the reward, the laboratory counters, the ledger rows, and what is missing",
          stat["trace"]["stop_condition"] == "spend_cap" and stat["trace"]["reward_skill_vs_O"] == 0.42 and stat["trace"]["lab"] == {"ticks_used": 17}
          and stat["marker"] == PK.MARK and stat["ledger"][0]["event"] == "reserved" and stat["missing"] == [] and stat["trace"]["credential_like_fields_removed_from_the_trace"] >= 2, stat["trace"])
    usage = json.load(open(os.path.join(folder, "usage.json")))
    check("D30 usage.json: every attempt with its cost and basis, the total, and the attempt that never settled at the worst case",
          usage["attempts"] == 3 and abs(usage["counted_usd"] - t["counted_usd"]) < 1e-12 and usage["calls"][2]["settled"] is False and usage["worst_case_calls"] == 2, usage["calls"])
    gr = json.load(open(os.path.join(folder, "grades.json")))
    lab = [json.loads(x) for x in open(os.path.join(folder, "lab_log.jsonl"))]
    check("D31 grades per item with the fallback reason, without the predictor's own text; the laboratory log without worker-side detail",
          gr["items"][1] == {"item": 1, "failed": True, "fallback_reason": "raised", "energy_score_by_cell": [3.0, 4.0], "cpu_s": 0.0}
          and "errors" not in gr["record"] and "detail" not in gr["record"] and lab[1] == {"t": 2.0, "op": "advance", "ok": False, "kind": "infrastructure", "ticks": 0, "ticks_used": 17, "total_nats": 0.0, "seconds": 0.1}, (gr["items"], lab))
    text = open(os.path.join(folder, "transcript.md")).read()
    check("D32 the transcript keeps the model's text as data: a fence the text cannot close, tool call and result in order",
          "**tool call** `bash`" in text and "````" in text and "rm -rf /" in text and text.index("[1] assistant") < text.index("[2] tool result") and PK.MARK in text)
    red = open(os.path.join(folder, "trace.redacted.jsonl")).read() if not tr_left else ""
    check("D33 the redacted trace: the team header and the Authorization header are removed by field name; the public commitment and the key variable's NAME stay",
          not tr_left and red.count(PK.REMOVED) >= 2 and "abcdefghijklmnopqrstuvwxyz012345" not in red and "c0c0c0" in red and "PRIME_API_KEY" in red, left)
    check("D34 the folder is never overwritten, and a job without a folder is refused", refused(lambda: PK.pack(rp, pilot, environ=env))
          and refused(lambda: PK.pack(rp, loose)))
    one = {"prompt_tokens": 900}
    check("D35 generic credential shapes are found by the scan: a bearer token, a private key block, an sk- key, a token in a url",
          set(PK.scan(b"Authorization: Bearer " + b"a" * 30 + b"\n-----BEGIN OPENSSH PRIVATE KEY-----\nsk-" + b"B" * 30 + b" https://user:hunter2hunter2@host/x", {}, {}))
          == {"bearer token", "private key block", "sk- key", "basic auth in a url"} and PK.scan(json.dumps(one).encode(), {}, {}) == {})
