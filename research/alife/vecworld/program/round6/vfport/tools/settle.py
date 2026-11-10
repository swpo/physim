"""settle -- close the books on a run: every rollout that verifiers left WITHOUT a reward is recorded as K.

verifiers skips finalize and scoring when the agent's harness fails (rollout.py:479, envs/isolated_verifier/env.py:
107): a model that kills its own harness process, or a harness that exits non-zero, ends its rollout ungraded.
No task hook runs then, so the environment cannot grade it; the operator rule is that such a rollout counts as K
and that the instance stays closed for that agent (`single_use`, on by default, refuses a second opening). This
tool applies the rule to a finished run directory and writes the K record next to the other grades, so that
evaluator.grader.table and anyone reading the store sees a score for every rollout that opened a laboratory.

usage: python tools/settle.py --store DIR --run-dir <output_dir>/<run name> [--dry-run]
Prints one JSON line per rollout: trace id, instance, graded, reward, settled_as_K, why.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))


def settle(store: str, run_dir: str, write: bool = True) -> list[dict]:
    from physim2_env import grading as G
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
                   "settled_as_K": False}
            if reward is None and iid:
                hidden = os.path.join(store, iid, "hidden")
                rec["laboratory_was_opened"] = os.path.isdir(os.path.join(hidden, "labs", str(tr.get("id"))))
                rec["why"] = "no reward on the trace (" + (", ".join(sorted(set(str(e) for e in errors))) or "no error recorded") + ")"
                g = os.path.join(hidden, "grades", f"{tr.get('id')}.npz")
                if os.path.exists(g):
                    rec["note"] = "a grade record already exists; left as it is"
                elif write:
                    k = G.score_as_k(hidden, str(tr.get("id")), "ungraded rollout settled as K: " + rec["why"], {"settled": True})
                    rec.update(settled_as_K=True, reward=0.0, n_items=k["n_items"])
                else:
                    rec["would_settle_as_K"] = True
            out.append(rec)
    return out


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    import vfrun
    vfrun.require_clean_environment()                      # before the package is imported: see vfrun.ENV_REFUSE
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", required=True)
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    for r in settle(a.store, a.run_dir, write=not a.dry_run):
        print(json.dumps(r))
