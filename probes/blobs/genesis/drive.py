"""drive.py — genesis job driver (bfield verbatim)."""
import sys, os, json, subprocess, time

BASE = os.path.dirname(os.path.abspath(__file__))
PY = "/Users/spoho/Documents/prime/test/physim/.venv/bin/python"

jobs = json.load(open(sys.argv[1]))
npar = int(sys.argv[2]) if len(sys.argv) > 2 else 3

# skip jobs already in results.json
done = set()
try:
    for r in json.load(open(os.path.join(BASE, "results.json"))):
        done.add(r["id"])
except Exception:
    pass
queue = [j for j in jobs if j["id"] not in done]
print(f"{len(queue)} to run ({len(jobs)-len(queue)} already done)", flush=True)

running = []
while queue or running:
    while queue and len(running) < npar:
        j = queue.pop(0)
        pr = subprocess.Popen([PY, os.path.join(BASE, "runjob.py"), json.dumps(j)],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        running.append((j["id"], pr, time.time()))
        print(f"[start] {j['id']}", flush=True)
    time.sleep(5)
    still = []
    for jid, pr, t0 in running:
        if pr.poll() is None:
            still.append((jid, pr, t0))
        else:
            out = pr.stdout.read().strip()
            print(f"[done {time.time()-t0:5.0f}s] {out[-400:]}", flush=True)
    running = still
print("ALL DONE", flush=True)
