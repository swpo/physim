"""settle -- close the books on a run: every rollout that was left WITHOUT a reward is recorded with the NULL
policy's forecast on every item (ruling E3: never K).

Since round 4 a run that fails is graded by the env itself (physim2_verifier: the last checkpoint of submission/
is graded in fresh boxes), so a trace without a reward is rare. It still happens when vf-eval itself was cut
(killed outright, the machine slept, the outer time limit or the disk watchdog stopped it): no trace was saved,
or a trace without a reward, and the boxes are gone. No task hook can run then. The operator rule: such a
rollout counts as the null policy (the baseline that every box starts with, physim2_env/public/
baseline_predict.py), and the instance stays closed for that agent (`single_use`). This tool applies the rule
and writes the record next to the other grades, so that evaluator.grader.table and anyone reading the store
sees a score for every rollout that opened a laboratory. It grades nothing and starts nothing: the checkpoint
of a cut run, if one was taken, stays in the store (<instance>/captures/<rollout>/) and is named in the output.

usage: python tools/settle.py --store DIR --run-dir <output_dir>/<run name> [--dry-run]
       python tools/settle.py --store DIR --instance ID --name ROLLOUT_NAME [--dry-run]     (a run that left no trace)
Prints one JSON line per rollout: trace id, instance, graded, reward, settled_as_null, why.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
REASON = "ungraded run"                                      # one word of grading.FALLBACK_REASONS


def as_null(store: str, iid: str, name: str, why: str, write: bool) -> dict:
    """Record `name` on instance `iid` as the null policy, unless a grade record exists. Returns what was done."""
    from physim2_env import grading as G
    hidden = os.path.join(store, iid, "hidden")
    rec = {"instance_id": iid, "name": name, "settled_as_null": False, "why": why,
           "laboratory_was_opened": os.path.isdir(os.path.join(hidden, "labs", name)),
           "checkpoint_in_the_store": os.path.exists(os.path.join(store, iid, "captures", name, "checkpoint.tar"))}
    if os.path.exists(os.path.join(hidden, "grades", f"{name}.npz")):
        rec["note"] = "a grade record already exists; left as it is"
    elif not write:
        rec["would_settle_as_null"] = True
    else:
        row = next(r for r in json.load(open(os.path.join(store, "index.json"))) if r["instance_id"] == iid)
        world, config_name = row["world"], row["config_name"]       # the public index: pointers only
        fb = G.fallback(hidden, world, config_name)
        got = G.score_as_null(hidden, name, REASON, fb, {"settled": True}, detail=why)
        rec.update(settled_as_null=True, reward=got["skill_vs_O"], n_items=got["n_items"])
    return rec


def settle(store: str, run_dir: str, write: bool = True) -> list[dict]:
    out = []
    f = os.path.join(run_dir, "traces.jsonl")
    for line in open(f) if os.path.exists(f) else ():
        ep = json.loads(line)
        for tr in ep.get("traces", []):
            data = (tr.get("task") or {}).get("data") or {}
            iid = data.get("instance_id")
            reward = (tr.get("rewards", {}).get("skill") or {}).get("score")
            errors = [e.get("type") for e in tr.get("errors", [])] + [e.get("type") for e in ep.get("errors", [])]
            rec = {"trace_id": tr.get("id"), "instance_id": iid, "graded": reward is not None, "reward": reward, "errors": errors,
                   "settled_as_null": False}
            if reward is None and iid:
                why = "no reward on the trace (" + (", ".join(sorted(set(str(e) for e in errors))) or "no error recorded") + ")"
                rec.update(as_null(store, iid, str(tr.get("id")), why, write))
            out.append(rec)
    return out


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    import vfrun
    vfrun.require_clean_environment()                      # before the package is imported: see vfrun.ENV_REFUSE
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", required=True)
    ap.add_argument("--run-dir", default=None)
    ap.add_argument("--instance", default=None, help="with --name: a run that was cut before it saved a trace")
    ap.add_argument("--name", default=None, help="the rollout's name in the store (the folder under <instance>/hidden/labs)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.run_dir and not (a.instance or a.name):
        rows = settle(a.store, a.run_dir, write=not a.dry_run)
    elif a.instance and a.name and not a.run_dir:
        import re
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,80}", a.instance) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,80}", a.name):
            raise SystemExit("refused: --instance and --name are plain names")
        rows = [as_null(a.store, a.instance, a.name, "the run was cut before it saved a trace", write=not a.dry_run)]
    else:
        raise SystemExit("usage: --run-dir DIR, or --instance ID --name ROLLOUT_NAME")
    for r in rows:
        print(json.dumps(r))
