"""Write one shell command per arm (labkit.run of world_ramp.py from a saved formed state)."""
import json, sys
O = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/paperexp/supply-ramp"
ENV = "OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1"
PY = "/home/user/labenv/bin/python -m labkit.run"

def job(sd, name, state, sched, T, spf, log_every=100, snap_every=0, save_at=(), extra=None):
    d = f"{O}/arms/s{sd}/{name}"
    wp = {"state": state, "sched": sched, "log": f"{d}/log.jsonl", "log_every": log_every,
          "snap_every": snap_every, "snap_dir": f"{d}/snaps", "save_at": list(save_at), "save_prefix": f"{O}/states/s{sd}_{name}"}
    if extra: wp.update(extra)
    frames = int(round(T / (spf * 0.1)))
    return (f"mkdir -p {d} && cd /home/user/physim/research/alife && WORLD_P='{json.dumps(wp)}' {ENV} {PY} {O}/world_ramp.py "
            f"--out {d}/pack --seeds {sd} --frames {frames} --spf {spf} --no-movie > {d}/run.log 2>&1")

which = sys.argv[1]
seeds = [int(x) for x in sys.argv[2].split(",")]
jobs = []
for sd in seeds:
    st = f"{O}/states/s{sd}_6000.npz"
    if which == "main":
        jobs.append(job(sd, "R4000", st, [[0, 0.2], [4000, 0.0]], 4600, 500, 100, 1000, save_at=(2000, 3000, 3200, 3400, 3600, 3800, 4600)))
        jobs.append(job(sd, "R1000", st, [[0, 0.2], [1000, 0.0]], 1600, 200, 100, 500))
        jobs.append(job(sd, "R100", st, [[0, 0.2], [100, 0.0]], 600, 100, 50, 100))
        for f in (1.0, 0.75, 0.5, 0.25, 0.15, 0.1):
            jobs.append(job(sd, f"C{f:g}", st, [[0, 0.2 * f]], 2000, 500, 100, 2500))
open(f"{O}/jobs_{which}.txt", "w").write("\n".join(jobs) + "\n")
print(len(jobs), "jobs")

if which == "b2":
    jobs = []
    for sd in seeds:
        s34 = f"{O}/states/s{sd}_R4000_3400.npz"
        jobs.append(job(sd, "C0.125", f"{O}/states/s{sd}_6000.npz", [[0, 0.025]], 2000, 500, 100, 2500))
        jobs.append(job(sd, "H0.03", s34, [[0, 0.03]], 1500, 500, 100, 500))
        jobs.append(job(sd, "H0.025", s34, [[0, 0.03], [100, 0.025]], 1600, 400, 100, 400))
        jobs.append(job(sd, "UP", f"{O}/states/s{sd}_R4000_4600.npz", [[0, 0.0], [2000, 0.2]], 4000, 500, 100, 500))
        jobs.append(job(sd, "TURN", s34, [[0, 0.03], [1000, 0.2]], 2000, 500, 100, 250))
    open(f"{O}/jobs_b2.txt", "w").write("\n".join(jobs) + "\n")
    print(len(jobs), "jobs")

if which == "b3":
    jobs = []
    st = f"{O}/states/s90_6000.npz"
    jobs.append(job(90, "R8000", st, [[0, 0.2], [8000, 0.0]], 8400, 1000, 100, 1000))
    # dt/2 check of the threshold bracket: abrupt steps to 0.03 and 0.025 at dt 0.05 (labkit frames counted at dt 0.1, so T is doubled here)
    for f, k in (("0.15", 0.03), ("0.125", 0.025)):
        jobs.append(job(90, f"C{f}_dthalf", st, [[0, k]], 2400, 1000, 200, 0, extra={"dt": 0.05}))
    open(f"{O}/jobs_b3.txt", "w").write("\n".join(jobs) + "\n")
    print(len(jobs), "jobs")
