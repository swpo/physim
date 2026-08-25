"""ds2_worker.py — evaluate a v2 jobs shard sequentially (idempotent).
Usage: ds2_worker.py <shard.json>"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ds2_lib as D2


def done_set():
    try:
        rows = json.load(open(D2.RESULTS2))
    except Exception:
        return set()
    return {(r.get("cand"), r.get("phase")) for r in rows
            if r.get("kind") == "ds2_eval" and r.get("status") is not None}


def main():
    jobs = json.load(open(sys.argv[1]))
    done = done_set()
    for job in jobs:
        key = (job["cand"], job.get("kind", "screen"))
        if key in done:
            print("skip", key, flush=True)
            continue
        row = D2.evaluate_v2(job)
        print(job["cand"], row.get("status"), row.get("interest"),
              row.get("cell"), "ext" if row.get("extended") else "",
              flush=True)


if __name__ == "__main__":
    main()
