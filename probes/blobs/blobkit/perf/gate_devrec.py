"""run devrec gates on pod: inline + async_apply variants."""
import json, os, time
import proto_devrec as DR

OUT = os.path.expanduser("~/perf/results/experiments.jsonl")

def emit(row):
    row["ts"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(OUT, "a") as f:
        f.write(json.dumps(row, default=str) + "\n")
    print("[row]", json.dumps(row, default=str)[:400], flush=True)

def main():
    ok1 = DR.gate_batch(n=4, L=64.0, T=500.0, async_apply=False)
    st1 = DR.stats()
    emit(dict(question="P3 devrec gate_batch inline", ok=bool(ok1), stats=st1))
    # reset stats between runs
    for k in DR._STATE["stats"]:
        DR._STATE["stats"][k] = 0 if isinstance(DR._STATE["stats"][k], int) else 0.0
    ok2 = DR.gate_batch(n=4, L=64.0, T=500.0, async_apply=True)
    st2 = DR.stats()
    emit(dict(question="P3 devrec gate_batch async_apply", ok=bool(ok2), stats=st2))
    print("VERDICT:", "ALL PASS" if (ok1 and ok2) else "FAIL", flush=True)

if __name__ == "__main__":
    main()
