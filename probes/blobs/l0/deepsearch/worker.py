"""worker.py — evaluate a jobs shard sequentially. Idempotent: skips cands
already present in results.json with same phase. Usage: worker.py <shard.json>"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ds_lib as DL


def done_set():
    try:
        rows = json.load(open(DL.RESULTS))
    except Exception:
        return set()
    return {(r.get("cand"), r.get("phase")) for r in rows
            if r.get("kind") == "ds_eval" and r.get("status") is not None}


def main():
    jobs = json.load(open(sys.argv[1]))
    done = done_set()
    for job in jobs:
        key = (job["cand"], job.get("kind", "screen"))
        if key in done:
            print("skip", key, flush=True)
            continue
        if job.get("gt_npz"):        # battery-only recompute from saved run
            import soup_sim
            rec = soup_sim.load_run(job["gt_npz"])
            recT = DL.truncate_rec(rec, job.get("T", DL.T_SCREEN))
            import metrics_v1 as MV
            out = MV.full_battery(recT)
            row = dict(kind="ds_eval", phase=job.get("kind", "screen"),
                       cand=job["cand"], gen=job.get("gen"), op=job.get("op"),
                       parents=None, T=job.get("T", DL.T_SCREEN),
                       seed=rec["seed"], status="ok",
                       na=rec["na"], nc=rec["nc"],
                       interest=out["interest"], cell=DL.cell_key(out),
                       summary=DL.lean_summary(out), origin="gt",
                       genome=job.get("genome"))
            DL.append_result(row)
            print("gt", job["cand"], round(out["interest"], 1), row["cell"],
                  flush=True)
            continue
        row = DL.evaluate(job)
        print(job["cand"], row.get("status"), row.get("interest"),
              row.get("cell"), flush=True)


if __name__ == "__main__":
    main()
