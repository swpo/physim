"""pod_worker.py — evaluate a jobs shard sequentially (idempotent).
Usage: pod_worker.py <shard.json>"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pod_lib as PL


def done_set(P):
    try:
        rws = json.load(open(P["results"]))
    except Exception:
        return set()
    return {(r.get("cand"), r.get("phase")) for r in rws
            if r.get("kind") == "ds2_eval" and r.get("status") is not None}


def main():
    cfg = PL.config()
    P = PL.paths(cfg)
    jobs = json.load(open(sys.argv[1]))
    done = done_set(P)
    for job in jobs:
        key = (job["cand"], job.get("kind", "screen"))
        if key in done:
            print("skip", key, flush=True)
            continue
        row = PL.evaluate(job, cfg)
        print(job["cand"], row.get("status"), row.get("interest"),
              row.get("cell"), f'T={row.get("T_used")}', flush=True)


if __name__ == "__main__":
    main()
