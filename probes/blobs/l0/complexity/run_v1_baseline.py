"""run_v1_baseline.py — v1 cost baseline: statics x s1-2, T=2500, metrics_v1,
6 parallel procs (same shape as wave A). For the <=1.5x cost gate."""
import subprocess, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = [("m0", 1), ("m0", 2), ("m4", 1), ("m4", 2), ("xv", 1), ("xv", 2)]
procs = []
for w, seed in SPEC:
    log = os.path.join(HERE, "logs_v2", f"v1base_{w}_s{seed}.log")
    cmd = ["python3", os.path.join(HERE, "soup_assay.py"), w,
           "--seed", str(seed), "--T", "2500", "--workers", "2",
           "--tag", f"v1base_{w}", "--metrics", "metrics_v1"]
    procs.append((w, seed, subprocess.Popen(
        cmd, stdout=open(log, "w"), stderr=subprocess.STDOUT, cwd=HERE)))
for w, seed, p in procs:
    print(w, seed, "rc", p.wait(), flush=True)
