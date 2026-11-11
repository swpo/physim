"""prove_round4 -- the scripted proof of round 4's exam rulings, through verifiers' own vf-eval. No model, no upload.

    VF_RUN_ID=<label> python -B tests/prove_round4.py --store DIR --scratch DIR --instance pilot-<name> \
        --disk-floor-gib 8 --out results/round4_exam.json [--stages a,b,...] [--image physim2-ring:2]

What it shows, on ONE fresh pilot instance of the ring profile (the store holds its hidden side; the output file
holds scores, counts, hashes and commands, never a hidden value):

  reference   the scripted reference policies null, D, P0, C through tools/prove.py (as a rollout's reference
              table is built), and the null policy once more with one fresh box per exam item (the default
              grading mode; the measured grading time at 256 samples per item)
  failures    a submission without predict.py; predictors that always raise, return a wrong shape, return a
              non-finite value, or never return; and a predictor that passes validation and then fails on some
              items in each of those ways. Every item without a valid forecast must carry the NULL policy's
              score for that item, bit for bit, and a reason; never K
  endings     the same valid predictor, left in submission/ by runs that end by a submit, by the script's own
              end, by the wall-time limit, by a failure of the harness (graded from the last checkpoint by the
              env physim2-verifier; ungraded under the stock isolated-verifier, as a control), and by the turn
              limit (the stock bash harness driven by tools/standin_model.py, a local stand-in that calls no
              model). Every graded ending must give the same per-item scores
  round 5     every graded submission once more through round 5's own grader (evaluator.grader.grade, unchanged)
              in a throwaway container (tests/cross_check_round5.py): identical scores on every item with a
              valid forecast

On the worker this file starts vf-eval (through tools/vfrun.py's own child environment, disk floor and stop
path), tools/make_instances.py, tools/prove.py, tools/standin_model.py and the `docker` client; it reads the
store. It runs no predictor, no driver and no clean-up on the worker: those run in the boxes verifiers starts
and in the one named throwaway container of the cross-check (no host mount, no network, removed by its exact
name). It deletes nothing. Stages are resumable: a finished stage is kept in <scratch>/proof_state.json.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(HERE, "agents"))
import vfrun  # noqa: E402

vfrun.require_clean_environment()
import numpy as np  # noqa: E402
import tomli_w  # noqa: E402

from physim2_env import bundle as BUNDLE  # noqa: E402
from physim2_env import grading as GRADING  # noqa: E402
from physim2_env import profiles as PROFILES  # noqa: E402
from physim2_env import rollout_config as RC  # noqa: E402
from predictors import PREDICTORS  # noqa: E402

STAGES = ["instance", "reference", "box", "failures", "mixed", "endings", "failed-run", "turn-cap", "round5"]
PROFILE = "ring"
CHECKS = []


def check(name, ok, **detail):
    CHECKS.append({"check": name, "ok": bool(ok), **detail})
    print(("ok   " if ok else "FAIL ") + name + ("" if ok else " " + json.dumps(detail, default=str)[:600]), flush=True)


class Proof:
    def __init__(self, a):
        self.a = a
        self.store, self.scratch, self.iid = os.path.abspath(a.store), os.path.abspath(a.scratch), a.instance
        self.prof = PROFILES.get(PROFILE)
        self.runs_dir = os.path.join(self.scratch, "runs")
        self.notes = os.path.join(self.scratch, "notes")
        self.state_f = os.path.join(self.scratch, "proof_state.json")
        os.makedirs(self.runs_dir, exist_ok=True)
        self.state = json.load(open(self.state_f)) if os.path.exists(self.state_f) else {"runs": {}, "stages": {}, "commands": []}
        self.floor = vfrun.disk_floor_bytes(a.disk_floor_gib)
        self.hidden = os.path.join(self.store, self.iid, "hidden")
        self._fb = None

    def save(self):
        with open(self.state_f, "w") as f:
            json.dump(self.state, f, indent=1)

    def command(self, argv, env_note=""):
        line = " ".join(str(x) if " " not in str(x) and "{" not in str(x) else "'" + str(x) + "'" for x in argv)
        self.state["commands"].append((env_note + " " if env_note else "") + line.replace(self.store, "$STORE").replace(self.scratch, "$SCRATCH").replace(ROOT, "."))

    # ---- one vf-eval run from a config dict ----
    def vf_eval(self, name, cfg, *, extra_env=None, timeout=2400.0, cwd=None):
        if name in self.state["runs"]:
            return self.state["runs"][name]
        vfrun.run_label()
        vfrun.require_disk(self.floor, f"the run {name}")
        vfrun.require_docker()
        cfg = dict(cfg, output_dir=self.runs_dir, run={"name": name})
        toml = os.path.join(self.runs_dir, f"{name}.toml")
        with open(toml, "wb") as f:
            tomli_w.dump(cfg, f)
        cmd = ["nice", "-n", "10", *vfrun.VF_EVAL, "@", toml, "--no-rich"]
        self.command(["VF_RUN_ID=<label>", ".venv/bin/python", "-B", "tools/vfeval.py", "@", toml, "--no-rich"], "(through tools/vfrun.py's child environment)")
        t0 = time.time()
        rc, out, err, how = vfrun.run_child(cmd, env=vfrun.child_env(extra_env), cwd=cwd or self.runs_dir, timeout=timeout, disk_floor=self.floor)
        vfrun.end_of_child(rc, how, os.path.join(self.runs_dir, f"{name}.stopped.json"), self.floor)
        f = os.path.join(self.runs_dir, name, "traces.jsonl")
        eps = [json.loads(line) for line in open(f)] if os.path.exists(f) else []
        if len(eps) != 1:
            raise SystemExit(f"run {name}: {len(eps)} episodes\n{(out + err)[-2000:]}")
        rec = dict(self.summary(eps[0]), name=name, wall_s=round(time.time() - t0, 1), returncode=rc, config=os.path.basename(toml))
        self.state["runs"][name] = rec
        self.save()
        print(f"run {name}: reward {rec['reward']} ended {rec['ended']!r} fallback {rec['fallback_by_reason']} ({rec['wall_s']:.0f}s)", flush=True)
        return rec

    @staticmethod
    def summary(ep):
        tr = ep["traces"][0]
        ph = (tr.get("info") or {}).get("physim2") or {}
        g, sub, cap = ph.get("grade") or {}, ph.get("submission") or {}, ph.get("capture") or {}
        reward = (tr.get("rewards", {}).get("skill") or {}).get("score")
        tm = tr.get("timing") or {}
        span = lambda k: round(((tm.get(k) or {}).get("end") or 0) - ((tm.get(k) or {}).get("start") or 0), 1)  # noqa: E731
        return {"trace_id": tr["id"], "ok": tr.get("ok"), "errors": [e.get("type") for e in tr.get("errors", [])] + [e.get("type") for e in ep.get("errors", [])],
                "stop_condition": tr.get("stop_condition"), "ended": ph.get("ended"), "graded": reward is not None, "reward": reward,
                "submission": {k: sub.get(k) for k in ("source", "ok", "files", "bytes", "sha256")}, "submission_checkpoint": sub.get("checkpoint"),
                "n_items": g.get("n_items"), "n_failed": g.get("n_failed"), "fallback_by_reason": (g.get("fallback") or {}).get("by_reason"),
                "fallback_policy": (g.get("fallback") or {}).get("policy"), "validation": g.get("validation"), "isolation": g.get("isolation"),
                "grade_seconds": g.get("seconds"), "item_boxes": g.get("item_boxes"), "item_box_wall_s_mean": g.get("item_box_wall_s_mean"),
                "cpu_s_per_item": g.get("cpu_s_mean"), "capture": cap, "checkpoints": ph.get("checkpoints"), "limits": ph.get("limits"),
                "lab": {k: (ph.get("lab") or {}).get(k) for k in ("ticks_used", "resets", "validations", "submissions", "submitted")},
                "wall": {k: span(k) for k in ("setup", "agent", "finalize")}, "verifier_wall_s": g.get("verifier_wall_s"),
                "turns": tr.get("num_turns"), "recovery_error": ph.get("recovery_error"), "grading_error": ph.get("grading_error")}

    def scripted(self, harness, *, task=None, env_id="isolated-verifier", timeouts=None):
        name = harness.pop("_name")
        cfg = {"model": "none/scripted", "num_rollouts": 1, "max_concurrent": 1, "push": False, "client": dict(vfrun.NO_MODEL_CLIENT),
               "env": {"id": env_id,
                       "taskset": {"id": "physim2-env", "store": self.store, "instances": [self.iid], "image": self.a.image,
                                   "task": dict({"agent_key": name, "item_isolation": "shared"}, **(task or {}))},
                       "agent": {"runtime": {"type": "docker"}, "harness": dict({"id": "physim2-script"}, **harness), "retries": {"max_retries": 0}},
                       "retries": {"max_retries": 0}, "verifier": {"retries": 0}}}
        if timeouts:
            cfg["env"]["agent"]["timeout"] = timeouts
        return self.vf_eval(name, cfg)

    def ending(self, name, predictor, end, *, validate=False, linger=0.0, **kw):
        args = ["--predictor", predictor, "--end", end] + (["--validate"] if validate else []) + (["--linger", str(linger)] if linger else [])
        return self.scripted({"_name": name, "agent_dir": os.path.join(HERE, "agents"), "script": "ending_agent.py", "args": args, "label": name,
                              "collect": ["agent_log_ending.json"], "collect_dir": self.notes}, **kw)

    # ---- what the store holds for a run ----
    def scores(self, rec):
        z = np.load(os.path.join(self.hidden, "grades", f"{rec['trace_id']}.npz"))
        return np.asarray(z["es"], float), np.asarray(z["failed"], bool)

    def record(self, rec):
        with open(os.path.join(self.hidden, "grades", f"{rec['trace_id']}.json")) as f:
            return json.load(f)

    def fb(self):
        if self._fb is None:
            self._fb = GRADING.fallback(self.hidden, self.prof["world"], self.prof["config_name"])
        return self._fb

    def skill(self, es):
        ex = GRADING.exam(self.hidden)
        return GRADING.summary(ex, es, ex.references())["skill_vs_O"]

    def captured(self, rec):
        return os.path.join(self.store, self.iid, "captures", rec["trace_id"], "final", "submission")

    def capture_matches(self, rec):
        """Do the files written to the store hash to the manifest of what was graded?"""
        folder = os.path.join(self.store, self.iid, "captures", rec["trace_id"], "final")
        with open(os.path.join(folder, "submission.json")) as f:
            man = json.load(f)
        ok = all(hashlib.sha256(open(os.path.join(folder, "submission", f["path"]), "rb").read()).hexdigest() == f["sha256"] for f in man["files"])
        digest = hashlib.sha256("".join(f"{f['path']}:{f['sha256']}\n" for f in sorted(man["files"], key=lambda f: f["path"])).encode()).hexdigest()
        return ok and man["complete"] and digest == rec["submission"]["sha256"] == man["graded_manifest_sha256"]

    # ============================================================================================ stages
    def stage_instance(self):
        idx = os.path.join(self.store, "index.json")
        have = {r["instance_id"] for r in json.load(open(idx))} if os.path.exists(idx) else set()
        if self.iid not in have:
            argv = [sys.executable, "-B", os.path.join(ROOT, "tools", "make_instances.py"), "--store", self.store, "--profile", PROFILE, "--id", self.iid]
            self.command([".venv/bin/python", "-B", "tools/make_instances.py", "--store", self.store, "--profile", PROFILE, "--id", self.iid])
            r = vfrun.run_helper(argv, capture=True)
            if r.returncode:
                raise SystemExit("make_instances failed: " + r.stderr[-500:])
            self.state["stages"]["instance"] = json.loads(r.stdout.strip().splitlines()[-1])
        row = next(r for r in json.load(open(idx)) if r["instance_id"] == self.iid)
        check("instance: a fresh pilot instance of the ring profile exists under the requested id, with the profile's exam config",
              row["config_name"] == self.prof["config_name"] and row["world"] == "ring", row={k: row[k] for k in ("instance_id", "world", "config_name")})
        r = vfrun.run_helper([sys.executable, "-B", os.path.join(ROOT, "tools", "make_instances.py"), "--store", self.store, "--profile", PROFILE, "--id", self.iid],
                             capture=True)
        check("instance: the same id a second time is refused", r.returncode != 0 and "refused" in (r.stderr + r.stdout), out=(r.stderr + r.stdout)[-200:])

    def stage_reference(self):
        out = os.path.join(self.scratch, "reference.json")
        pols = self.a.policies
        if not os.path.exists(out):
            argv = [sys.executable, "-B", os.path.join("tools", "prove.py"), "--store", self.store, "--scratch", os.path.join(self.scratch, "reference"),
                    "--profile", PROFILE, "--instance", self.iid, "--policies", pols, "--disk-floor-gib", str(self.a.disk_floor_gib), "--out", out]
            self.command(["VF_RUN_ID=<label>", ".venv/bin/python", "-B", *argv[2:]])
            t0 = time.time()
            r = vfrun.run_helper(argv, cwd=ROOT, env=vfrun.child_env(), capture=True)
            if r.returncode:
                raise SystemExit("prove.py failed: " + (r.stdout + r.stderr)[-1500:])
            self.state["stages"]["reference"] = {"wall_s": round(time.time() - t0, 1), "log": r.stdout.strip().splitlines()[-8:]}
            self.save()
        ref = json.load(open(out))
        rolls = ref["per_world"][0]["rollouts"]
        table = {k: {"L": v["L"], "skill_vs_O": v["vs_O"], "skill_vs_C": v["vs_C"]} for k, v in ref["pooled"]["policies"].items()}
        self.state["stages"].setdefault("reference", {}).update(table=table, cost={
            "wall_s_per_policy": ref["rollout_cost"]["vf_eval_wall_s_per_policy"], "wall_s_total": ref["wall_s"],
            "grade_seconds": {p: rolls[p]["grade"]["seconds"] for p in rolls}, "cpu_s_per_item": {p: rolls[p]["grade"]["cpu_s_mean"] for p in rolls}},
            rollouts={p: {"trace_id": rolls[p]["trace_id"], "ended": rolls[p]["ended"], "submission": rolls[p]["submission"], "reward": rolls[p]["reward_skill_vs_O"],
                          "lab_ticks_used": rolls[p]["lab_ticks_used"], "lab_episodes": rolls[p]["lab_episodes"], "n_failed": rolls[p]["grade"]["n_failed"],
                          "box_caps": rolls[p]["box_caps"], "limits": rolls[p]["limits"]} for p in rolls})
        self.save()
        check("reference: every policy is graded, with no failed item", ref["all_graded"] and ref["all_ok"] and ref["n_failed_items_total"] == 0)
        z = np.load(os.path.join(self.hidden, "grades", "null.npz"))
        check("reference: the null policy's per-item scores through the route equal grading.null_scores (what a failed item gets), bit for bit",
              np.array_equal(z["es"], self.fb()["es"]), max_abs_difference=float(np.abs(z["es"] - self.fb()["es"]).max()))
        check("reference: the null policy ended without a submit and was graded on the final collection of submission/",
              rolls["null"]["ended"] == "the agent stopped" and rolls["null"]["submission"]["source"] == "final_collection" and rolls["null"]["lab_ticks_used"] == 0)
        t = table
        check("reference: K = 0 and O = 1 on the skill scale; the null policy near K (it knows the prior, not the world); null and D below P0 below C below O",
              t["K"]["skill_vs_O"] == 0.0 and abs(t["O"]["skill_vs_O"] - 1.0) < 1e-12 and abs(t["null"]["skill_vs_O"]) < 0.15
              and max(t["null"]["skill_vs_O"], t["D"]["skill_vs_O"]) < t["P0"]["skill_vs_O"] < t["C"]["skill_vs_O"] < 1.0,
              table={k: round(v["skill_vs_O"], 4) for k, v in t.items()})
        caps = [rolls[p]["box_caps"] for p in rolls]
        check("reference: every reference box ran under the same caps as a model's box (2 CPUs, 4 GB, 512 processes, read-only root)",
              all(c and c["cpus"] == 2 and c["memory_gb"] == 4 and c["pids"] == 512 and c["read_only_root"] for c in caps), caps=caps[0])
        check("reference: with a 17-tick reset D and S get 6 real episodes of exam shape from 400 ticks", rolls["D"]["lab_episodes"] == 6 and rolls["D"]["lab_ticks_used"] == 390,
              episodes=rolls["D"]["lab_episodes"], ticks=rolls["D"]["lab_ticks_used"])

    def stage_box(self):
        rec = self.scripted({"_name": "null-box", "agent_dir": os.path.join(ROOT, "agents"), "script": "keep_baseline.py", "label": "null-box"},
                            task={"item_isolation": "box"})
        es, failed = self.scores(rec)
        check("box: the null policy graded with one fresh box per item (the default mode) gets the same per-item scores as in one box",
              np.array_equal(es, self.fb()["es"]) and not failed.any() and rec["isolation"] == "box" and rec["item_boxes"] == 64,
              item_boxes=rec["item_boxes"], isolation=rec["isolation"])
        self.state["stages"]["box"] = {"grade_seconds": rec["grade_seconds"], "item_box_wall_s_mean": rec["item_box_wall_s_mean"], "cpu_s_per_item": rec["cpu_s_per_item"],
                                       "n_samples": 256, "note": "grading time of 64 items at 256 samples per item, one fresh box each, on 4 shared cores"}

    def stage_failures(self):
        null_skill = self.skill(self.fb()["es"])
        want = {"none": "no predict.py", "raises": "validation failed: raised", "shape": "validation failed: wrong shape",
                "nan": "validation failed: non-finite values", "timeout": "validation failed: timed out"}
        names = {p: f"fail-{p}" for p in want}
        names["none"] = "fail-nopredict"                     # a first run (fail-none) showed the word "no submission": fixed, run again
        for pred, reason in want.items():
            rec = self.ending(names[pred], pred, "exit", validate=pred in ("raises", "none"))
            es, failed = self.scores(rec)
            store = self.record(rec)
            check(f"failure `{pred}`: graded; all 64 items carry the null policy's score, bit for bit; reason `{reason}`; reward = the null policy's skill, not 0",
                  rec["graded"] and rec["ok"] and failed.all() and np.array_equal(es, self.fb()["es"]) and rec["fallback_by_reason"] == {reason: 64}
                  and rec["fallback_policy"] == "null" and abs(rec["reward"] - null_skill) < 1e-12 and rec["reward"] != 0.0
                  and len(store["fallback_items"]) == 64 and all(x["reason"] == reason for x in store["fallback_items"]),
                  reward=rec["reward"], null_skill=null_skill, by=rec["fallback_by_reason"], graded=rec["graded"], errors=rec["errors"])
        for pred in ("raises", "none"):                      # what the in-box check told the agent
            rec = self.state["runs"][names[pred]]
            f = os.path.join(self.notes, rec["trace_id"], "agent_log_ending.json")
            log = json.load(open(f)) if os.path.exists(f) else {}
            v = log.get("validate") or {}
            check(f"failure `{pred}`: lab.validate in the box had already said no ({'artifact' if pred == 'none' else 'example 0'})",
                  v.get("ok") is False and v.get("stage") == ("artifact" if pred == "none" else "example 0"), validate={k: str(v.get(k))[:120] for k in ("ok", "stage", "error")})
            if pred == "raises":
                check("the laboratory client: experiment(label, None) raised LabError with one line of usage, and every reply went to lab_log.jsonl",
                      str(log.get("bad_experiment", "")).startswith("usage: lab.experiment(label, U)") and "\n" not in str(log.get("bad_experiment"))
                      and log.get("free_episode_shape") == [5, 6] and log.get("lab_log_lines", 0) >= 2, log={k: log.get(k) for k in ("bad_experiment", "lab_log_lines")})
                check("the laboratory itself: an experiment without inputs and without n is rejected with one line of usage, and charged nothing",
                      str(log.get("bad_experiment_at_the_laboratory", "")).startswith("format: usage: experiment(label, inputs)")
                      and "\n" not in str(log.get("bad_experiment_at_the_laboratory")), reply=log.get("bad_experiment_at_the_laboratory"))
                u = log.get("usage_before_end") or {}
                check("lab.usage() reports seconds elapsed and left, and turns; a reset cost 17 ticks", isinstance(u.get("seconds_elapsed"), (int, float))
                      and isinstance(u.get("seconds_left"), (int, float)) and "turns_used" in u and u.get("ticks_used") == 21, usage={k: u.get(k) for k in (
                          "seconds_elapsed", "seconds_left", "turns_used", "turns_left", "ticks_used")})

    def stage_mixed(self):
        rec = self.ending("mixed-submit", "mixed", "submit")
        es, failed = self.scores(rec)
        store = self.record(rec)
        by = rec["fallback_by_reason"] or {}
        fb = self.fb()["es"]
        check("mixed: the predictor passed validation, was submitted, and failed on some items only",
              rec["graded"] and rec["submission"]["source"] == "agent_submission" and 0 < int(failed.sum()) < 64 and (rec["validation"] or {}).get("ok") is True,
              n_failed=int(failed.sum()), by=by)
        check("mixed: each failed item has one of the fixed reasons (raised, wrong shape, non-finite values, timed out), and all three instant kinds occur",
              set(by) <= {"raised", "wrong shape", "non-finite values", "timed out"} and {"raised", "wrong shape", "non-finite values"} <= set(by)
              and sum(by.values()) == int(failed.sum()) == len(store["fallback_items"]), by=by)
        check("mixed: every failed item carries the null policy's score for THAT item, bit for bit; no valid item does",
              np.array_equal(es[failed], fb[failed]) and not any(np.array_equal(es[i], fb[i]) for i in np.flatnonzero(~failed)))
        ex = GRADING.exam(self.hidden)
        check("mixed: no failed item carries K", not any(np.array_equal(es[i], ex.references()["K"][i]) for i in np.flatnonzero(failed)))
        self.state["stages"]["mixed"] = {"n_failed": int(failed.sum()), "by_reason": by, "reward": rec["reward"]}

    def stage_endings(self):
        a = self.ending("end-submit", "valid", "submit")
        b = self.ending("end-exit", "valid", "exit")
        c = self.ending("end-wall", "valid", "sleep", timeouts={"rollout": 40})
        ea, eb, ec = self.scores(a)[0], self.scores(b)[0], self.scores(c)[0]
        check("ending by submit: graded on the copy the submit froze; no failed item", a["graded"] and a["ended"] == "submit" and a["stop_condition"] == "agent_completed"
              and a["submission"]["source"] == "agent_submission" and a["n_failed"] == 0, rec={k: a[k] for k in ("ended", "stop_condition", "submission", "n_failed")})
        check("ending by the script's own end, no submit: the final collection of submission/ is graded; same per-item scores",
              b["graded"] and b["ended"] == "the agent stopped" and b["submission"]["source"] == "final_collection" and np.array_equal(ea, eb))
        check("ending by the wall-time limit (40 s): verifiers stops the run, the final collection is graded; same per-item scores",
              c["graded"] and c["ok"] and c["ended"] == "time limit" and "timeout" in str(c["stop_condition"]) and c["submission"]["source"] == "final_collection"
              and np.array_equal(ea, ec) and 35 <= c["wall"]["agent"] <= 60, stop=c["stop_condition"], agent_s=c["wall"]["agent"], ended=c["ended"])
        check("the statement of the 40-second run said 0.667 minutes (rendered from the run's own config)", abs((c["limits"] or {}).get("wall_minutes", 0) - 0.667) < 1e-3,
              wall_minutes=(c["limits"] or {}).get("wall_minutes"))
        for rec in (a, b, c):
            check(f"capture of `{rec['name']}`: the files written to the store hash to the manifest of what was graded; the workspace copy holds the notes and the lab log",
                  self.capture_matches(rec) and (rec["capture"].get("workspace") or {}).get("n_files", 0) >= 3, capture=rec["capture"])
        sha = {r["submission"]["sha256"] for r in (a, b, c)}
        check("the three endings graded byte-identical submissions", len(sha) == 1, sha=sorted(sha))

    def stage_failed_run(self):
        ref = self.scores(self.ending("end-submit", "valid", "submit"))[0]
        d = self.ending("end-fail", "valid", "fail", linger=14, env_id="physim2-verifier", task={"checkpoint_seconds": 3})
        e = self.ending("end-fail-stock", "valid", "fail", linger=14, env_id="isolated-verifier", task={"checkpoint_seconds": 3})
        check("failed run, stock isolated-verifier (control): the harness exits with status 1, verifiers runs no finalize, and the run has NO grade",
              e["ok"] is False and not e["graded"], rec={k: e[k] for k in ("ok", "graded", "errors")})
        ed = self.scores(d)[0] if d["graded"] else None
        check("failed run, env physim2-verifier: the trace keeps ok = false and its error, and is graded on the last checkpoint of submission/; same per-item scores",
              d["ok"] is False and d["graded"] and d["ended"] == "failed run" and d["submission"]["source"] == "checkpoint" and ed is not None and np.array_equal(ed, ref)
              and (d["submission_checkpoint"] or {}).get("source") == "timer", rec={k: d[k] for k in ("ok", "graded", "ended", "submission", "submission_checkpoint", "errors",
                                                                                                    "recovery_error")})
        check("failed run: the graded copy was written to the store and matches its manifest", d["graded"] and self.capture_matches(d), capture=d["capture"])

    def stage_turn_cap(self):
        name = "end-turns"
        if name not in self.state["runs"]:
            steps = [{"bash": "cd /workspace && cat > submission/predict.py <<'PYEOF'\n" + PREDICTORS["valid"] + "PYEOF\nsed -n 1,3p TASK.md"},
                     {"tool": "lab_call", "arguments": {"op": "usage", "args": {}}},
                     {"bash": "touch /workspace/after_the_last_reply; echo done"},
                     {"say": "this reply is never asked for"}]
            sf = os.path.join(self.scratch, "standin_steps.json")
            with open(sf, "w") as f:
                json.dump(steps, f)
            p = subprocess.Popen([sys.executable, "-B", os.path.join(ROOT, "tools", "standin_model.py"), "--script", sf, "--port", "0",
                                  "--log", os.path.join(self.scratch, "standin_requests.jsonl")], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                 stdin=subprocess.DEVNULL, text=True, env=vfrun.child_env())
            try:
                here = json.loads(p.stdout.readline())
                flat = {"schema": RC.SCHEMA, "model": "standin/echo-1", "exam_profile": PROFILE, "instance": self.iid, "max_turns": 3,
                        "max_output_tokens_per_turn": 1024, "max_context_tokens": 50000, "wall_minutes": 5, "box_memory_gb": 4, "cap_usd": 1.0}
                cfg = RC.expand(flat)
                task = cfg["env"]["taskset"]["task"]
                task.update(item_isolation="shared", spend={"cap_usd": 1.0, "max_context_tokens": 50000, "max_output_tokens": 1024, "model": flat["model"],
                                                           "input_usd_per_mtok": 2.0, "output_usd_per_mtok": 10.0, "cache_read_usd_per_mtok": 0.5,
                                                           "context_window": 100000, "prices_from": "tools/standin_model.py (a local stand-in; nothing is billed)",
                                                           "billed": False})
                cfg["env"]["taskset"].update(store=self.store, image=self.a.image)
                cfg["client"] = {"type": "eval", "base_url": here["base_url"], "api_key_var": vfrun.STAND_IN_VAR}
                self.state["stages"]["turn-cap"] = {"flat_config": flat, "expanded_env_id": cfg["env"]["id"], "harness": cfg["env"]["agent"]["harness"],
                                                    "steps": [next(iter(s)) for s in steps]}
                self.vf_eval(name, cfg, extra_env={vfrun.STAND_IN_VAR: vfrun.STAND_IN_VALUE}, cwd=ROOT)
            finally:
                p.terminate()                                # our own child, by its handle
                p.wait(timeout=30)
        f = self.ending("end-submit", "valid", "submit")
        rec = self.state["runs"][name]
        ef = self.scores(f)[0]
        er = self.scores(rec)[0] if rec["graded"] else None
        check("ending by the turn limit (3 turns; stock bash harness of image 2, a stand-in instead of a model): stop condition max_turns, graded on the "
              "final collection, same per-item scores as the other endings",
              rec["graded"] and rec["ok"] and rec["stop_condition"] == "max_turns" and rec["ended"] == "turn limit"
              and rec["submission"]["source"] == "final_collection" and er is not None and np.array_equal(er, ef)
              and rec["submission"]["sha256"] == f["submission"]["sha256"],
              rec={k: rec[k] for k in ("ok", "graded", "stop_condition", "ended", "submission", "errors")})
        tr = json.loads(open(os.path.join(self.runs_dir, name, "traces.jsonl")).readline())["traces"][0]
        msgs = [n.get("message") or {} for n in tr.get("nodes", [])]
        text = lambda m: m.get("content") if isinstance(m.get("content"), str) else json.dumps(m.get("content"))  # noqa: E731
        first = next((text(m) for m in msgs if m.get("role") == "user"), "") or ""
        check("turn limit: the first message carries the run's own limits (3 turns, 5 minutes, 1024 tokens a reply, context 50,000, spend 1 dollar) and the measured box",
              all(s in first for s in ("**Turns: at most 3.**", "**Wall-clock time: 5 minutes**", "**One reply: at most 1024 tokens**", "**Context: 50,000 tokens.**",
                                       "**Spend: 1 US dollars**", "2 CPU cores, 4 GiB of memory", "(Measured in this box when it started.)")), head=first[:200])
        tools = [text(m) or "" for m in msgs if m.get("role") == "tool"]
        usage = next((t for t in tools if "turns_used" in t), "")
        check("turn limit: lab.usage() through the tool reported turns_used 2, turns_left 1, seconds and the context counters",
              '"turns_used": 2' in usage and '"turns_left": 1' in usage and '"seconds_left"' in usage and '"context_tokens_left"' in usage, usage=usage[-400:])
        replies = sum(1 for n in tr.get("nodes", []) if n.get("sampled"))
        check("turn limit: no reply follows the last reply's tool call (the model made 3 replies and never saw that call's result)", replies == 3,
              replies=replies, tool_results_in_the_trace=len(tools))
        ws = json.load(open(os.path.join(self.store, self.iid, "captures", rec["trace_id"], "final", "workspace.json")))
        check("turn limit: that last tool call did run (its file is in the workspace listing)", any(e[2] == "./after_the_last_reply" for e in ws["listing"]["entries"]))
        lim = rec["limits"] or {}
        check("turn limit: the trace records the limits the statement was rendered from", lim.get("max_turns") == 3 and lim.get("max_context_tokens") == 50000
              and lim.get("harness") == "bash" and lim.get("measured") is True, limits={k: lim.get(k) for k in ("max_turns", "wall_minutes", "max_context_tokens", "harness")})
        ph = tr["info"]["physim2"]
        check("turn limit: the reasoning record is there (3 replies of a stand-in, none with reasoning) and a checkpoint was taken before a model call",
              (ph.get("reasoning") or {}).get("replies") == 3 and (ph.get("reasoning") or {}).get("reasoning_on") is False
              and (ph.get("checkpoints") or {}).get("taken", 0) >= 2, reasoning=ph.get("reasoning"), checkpoints=ph.get("checkpoints"))

    def stage_round5(self):
        """Every graded submission through round 5's own grader, in a throwaway container without any host mount."""
        runs = self.state["runs"]
        ref = self.state["stages"]["reference"]["rollouts"]
        subs = {p: os.path.join(self.store, self.iid, "captures", ref[p]["trace_id"], "final", "submission") for p in ref}
        subs.update(valid=self.captured(runs["end-submit"]), mixed=self.captured(runs["mixed-submit"]))
        out = os.path.join(self.scratch, "round5.npz")
        name = "physim2-port4a-xcheck"
        if not os.path.exists(out):
            env = vfrun.child_env()

            def docker(*args, **kw):
                return subprocess.run(["docker", *args], capture_output=True, env=env, timeout=1800, **kw)
            r = docker("run", "-d", "--name", name, "--network", "none", "--label", f"verifiers.run={vfrun.run_label()}", "--entrypoint", "sleep", self.a.image, "infinity")
            if r.returncode:
                raise SystemExit("could not start the cross-check container: " + r.stderr.decode()[-300:])
            try:
                import io
                import tarfile
                buf = io.BytesIO()
                vec = os.path.abspath(os.path.join(ROOT, "..", "..", ".."))
                with tarfile.open(fileobj=buf, mode="w") as tar:
                    skip = lambda ti: None if any(x in ti.name.split("/") for x in (".venv", "__pycache__", "results", "redteam", "rehearsal")) else ti  # noqa: E731
                    for rel in ("program/round6/vfport", "program/round5/agentenv", "vw1/vw"):
                        tar.add(os.path.join(vec, rel), arcname="src/" + rel, filter=skip)
                    for nm in ("instance.json", "exam.npz"):
                        tar.add(os.path.join(self.hidden, nm), arcname=f"x/store/{self.iid}/hidden/{nm}")
                    for k, d in subs.items():
                        tar.add(d, arcname=f"x/subs/{k}")
                r = docker("cp", "-", f"{name}:/", input=buf.getvalue())
                if r.returncode:
                    raise SystemExit("docker cp failed: " + r.stderr.decode()[-300:])
                cmd = ["exec", "-w", "/src/program/round6/vfport", name, "nice", "-n", "10", "python", "-B", "tests/cross_check_round5.py", "--hidden",
                       f"/x/store/{self.iid}/hidden", "--config", self.prof["config_name"], "--out", "/tmp/round5.npz"] + [f"{k}=/x/subs/{k}" for k in subs]
                self.command(["docker", "run -d --name", name, "--network none --entrypoint sleep", self.a.image, "infinity ; docker cp <code, instance, submissions> ;",
                              "docker", *cmd, "; docker cp", f"{name}:/tmp/round5.npz", "; docker rm -f", name])
                r = docker(*cmd)
                if r.returncode:
                    raise SystemExit("the cross-check failed: " + (r.stdout + r.stderr).decode()[-1500:])
                self.state["stages"]["round5"] = json.loads(r.stdout.decode().strip().splitlines()[-1])
                r = docker("cp", f"{name}:/tmp/round5.npz", out)
                if r.returncode:
                    raise SystemExit("docker cp out failed: " + r.stderr.decode()[-300:])
            finally:
                docker("rm", "-f", name)                     # exactly the container started above
            self.save()
        z = np.load(out)
        res = {}
        for p in list(ref) + ["valid"]:
            route = np.load(os.path.join(self.hidden, "grades", f"{ref[p]['trace_id']}.npz"))["es"] if p in ref else self.scores(runs["end-submit"])[0]
            same = bool(np.array_equal(route, z[f"es_{p}"])) and not z[f"failed_{p}"].any()
            res[p] = {"identical": same, "max_abs_difference": float(np.abs(route - z[f"es_{p}"]).max()), "skill_route": self.skill(route), "skill_round5": self.skill(z[f"es_{p}"])}
            check(f"round 5: `{p}` gets the same score on all 64 items and 7 cells from round 5's own grader as from the route", same, **res[p])
        es, failed = self.scores(runs["mixed-submit"])
        ok_valid = np.array_equal(es[~failed], z["es_mixed"][~failed]) and np.array_equal(failed, z["failed_mixed"])
        check("round 5: `mixed`: round 5's grader fails the same items; on every other item the scores are identical", ok_valid,
              n_failed_route=int(failed.sum()), n_failed_round5=int(z["failed_mixed"].sum()))
        check("round 5: on the failed items round 5 gave K, the route gives the null policy (the one intended difference)",
              np.array_equal(z["es_mixed"][failed], z["K"][failed]) and np.array_equal(es[failed], z["null_fallback"][failed]) and np.array_equal(z["null_fallback"], self.fb()["es"]))
        res["mixed"] = {"identical_on_valid_items": bool(ok_valid), "n_failed": int(failed.sum()), "skill_route_null_fallback": self.skill(es),
                        "skill_round5_K_fallback": self.skill(z["es_mixed"])}
        self.state["stages"].setdefault("round5", {})["comparison"] = res
        self.save()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--instance", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--stages", default=",".join(STAGES))
    ap.add_argument("--policies", default="null,D,P0,C")
    ap.add_argument("--image", default=PROFILES.get(PROFILE)["image"])
    ap.add_argument("--disk-floor-gib", type=float, default=vfrun.DISK_FLOOR_GIB)
    a = ap.parse_args()
    vfrun.DISK_FLOOR_GIB = a.disk_floor_gib
    label = vfrun.run_label()
    if not RC.INSTANCE.fullmatch(a.instance):
        raise SystemExit("refused: --instance must be a pilot name (pilot-...)")
    P = Proof(a)
    t0 = time.time()
    for st in [s for s in STAGES if s in a.stages.split(",")]:
        print(f"== stage {st}", flush=True)
        getattr(P, "stage_" + st.replace("-", "_"))()
        P.save()
    runs = P.state["runs"]
    table = [{"run": k, "ended": r["ended"], "stop_condition": r["stop_condition"], "ok": r["ok"], "graded": r["graded"], "submission_source": r["submission"]["source"],
              "items_fallen_back": r["n_failed"], "by_reason": r["fallback_by_reason"], "reward_skill_vs_O": r["reward"], "wall_s": r["wall_s"]} for k, r in runs.items()]
    raw, info = BUNDLE.public_bundle(P.prof["world"], P.prof["config_name"])
    out = {"what": "round 4, fixer A: the scripted proof of the exam rulings through vf-eval (no model, no upload)",
           "PILOT_NEVER_REUSE_AS_EXAM": True, "instance_id": a.instance,
           "hidden_values_in_this_file": "none (theta, the secret and the items stay in the worker's store)",
           "run_label": label, "image": a.image, "profile": PROFILES.table()[0], "verifiers": __import__("verifiers").__version__,
           "n_checks": len(CHECKS), "n_passed": sum(c["ok"] for c in CHECKS), "failed": [c["check"] for c in CHECKS if not c["ok"]],
           "reference_table": (P.state["stages"].get("reference") or {}).get("table"), "reference_cost": (P.state["stages"].get("reference") or {}).get("cost"),
           "null_policy": {"skill_vs_O": P.skill(P.fb()["es"]) if os.path.isdir(P.hidden) else None, "pool_sha256": info["baseline"]["pool_sha256"]},
           "endings_and_failures": table, "stages": P.state["stages"], "runs": runs, "commands": P.state["commands"],
           "box_contents_at_start": info["file_groups"], "bundle": {"files": info["files"], "bytes": info["bytes"], "baseline": info["baseline"]},
           "checks": CHECKS, "wall_s_this_invocation": round(time.time() - t0, 1)}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w") as f:
        json.dump(out, f, indent=1, default=str)
    print(json.dumps({k: out[k] for k in ("n_checks", "n_passed", "failed")}))
    return 0 if out["n_checks"] == out["n_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
