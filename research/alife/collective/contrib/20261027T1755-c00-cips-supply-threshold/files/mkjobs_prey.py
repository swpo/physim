"""Jobs for world 2: c52 prey only (pred_on 0), kF ramps and constant fractions from a formed state."""
import json, sys
O = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/paperexp/supply-ramp"
ENV = "OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1"
PY = "/home/user/labenv/bin/python -m labkit.run"
DT = 0.2
KF0 = 0.1

def job(sd, name, state, sched, T, spf, log_every=50, snap_every=0, save_at=(), save_prefix=None):
    d = f"{O}/prey/s{sd}/{name}"
    wp = {"pred_on": 0, "state": state, "sched": sched, "log": f"{d}/log.jsonl", "log_every": log_every,
          "snap_every": snap_every, "snap_dir": f"{d}/snaps", "save_at": list(save_at),
          "save_prefix": save_prefix or f"{O}/states/prey_s{sd}_{name}"}
    frames = int(round(T / (spf * DT)))
    return (f"mkdir -p {d} && cd /home/user/physim/research/alife && WORLD_P='{json.dumps(wp)}' {ENV} {PY} {O}/world_ramp_prey.py "
            f"--out {d}/pack --seeds {sd} --frames {frames} --spf {spf} --no-movie > {d}/run.log 2>&1")

which = sys.argv[1]; seeds = [int(x) for x in sys.argv[2].split(",")]
jobs = []
for sd in seeds:
    st = f"{O}/states/prey_s{sd}_3000.npz"
    if which == "p1":
        jobs.append(job(sd, "form", None, [[0, KF0]], 3000, 500, 250, 0, save_at=(3000,), save_prefix=f"{O}/states/prey_s{sd}"))
    else:
        jobs.append(job(sd, "R4000", st, [[0, KF0], [4000, 0.0]], 4600, 500, 50, 500))
        jobs.append(job(sd, "R1000", st, [[0, KF0], [1000, 0.0]], 1600, 200, 50, 250))
        jobs.append(job(sd, "R100", st, [[0, KF0], [100, 0.0]], 600, 50, 25, 50))
        for f in (1.0, 0.5, 0.25, 0.1):
            jobs.append(job(sd, f"C{f:g}", st, [[0, KF0 * f]], 2000, 500, 50, 1000))
open(f"{O}/jobs_{which}.txt", "w").write("\n".join(jobs) + "\n")
print(len(jobs))
if which == "p3":
    jobs = []
    for sd in seeds:
        st = f"{O}/states/prey_s{sd}_3000.npz"
        for f in (0.75, 0.625):
            jobs.append(job(sd, f"C{f:g}", st, [[0, KF0 * f]], 2000, 500, 50, 1000))
    open(f"{O}/jobs_p3.txt", "w").write("\n".join(jobs) + "\n")
    print(len(jobs))
