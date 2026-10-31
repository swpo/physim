"""Independent check of the c40 CIPS runner work (reviewer, not the author's code).

One case: the fuel pulse program (device0, port F, amp 3, t=5, dur 10), noise 0, to 20 tu, from the
author's prepared state (cips_runner/out/prep.npz).
 (a) parity WITH the action: my own loop (module init/step + my own Gaussian source, gain 0.1) vs the
     runner on the current branch HEAD (LW.oracle -> LabOracleRunner), device0/device1/global readouts.
 (b) dt ladder through the runner: dt 0.1 (1 step/tick), 0.05 (2), 0.025 (4); device0 offsets
     |0.1-0.05| and |0.05-0.025|; a ratio near 2 is first-order convergence (a genuine time error),
     a ratio near 1 or wild would point to a scheduling/injection bug in the null.
"""
import os, sys, json, time, subprocess
os.environ["OMP_NUM_THREADS"] = "1"
sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
import numpy as np
from physim import labworld as LW
from physim.devices import ProbeDevice

LAB = "/home/user/physim/research/alife"
WORLD = f"{LAB}/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py"
RUN = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/cips_runner/out"
OUT = os.path.dirname(os.path.abspath(__file__))
FIELDS = ("e", "p", "F", "s")
N = 192
z = np.load(f"{RUN}/prep.npz")
st = {f: z[f].astype(np.float64) for f in FIELDS}; st["t"] = float(z["t"])
info = json.load(open(f"{RUN}/prep.json"))


def devs():
    out = []
    for i, (lat, ds, rot, k) in enumerate((("square", 3.0, 0.3, 13), ("hex", 6.0, 1.1, 19))):
        c = np.asarray(info["sites"][f"device{i}"], float) + 0.5
        out.append(ProbeDevice(dev_id=i, lattice=lat, n_rings=3, base_ds=ds, center=c, L=float(N), secret_rot=rot,
                               reflect=False, motion_theta=0.0, motion_reflect=False, node_perm=np.arange(k)))
    return out


TIMES = [0, 2, 5, 8, 10, 12, 15, 20]
TICKS = [int(round(t / 0.02)) for t in TIMES]
PULSE = dict(t=5, kind="inject", device=0, port=2, amp=3.0, dur=10.0)
GAIN = {"e": 0.01, "p": 0.1, "F": 0.1, "s": 0.1}
CLIP = {"e": (0.0, 1.0), "p": (0.0, 1.0), "F": (0.0, None), "s": (0.0, None)}


def world(dt, spt):
    return LW.LabWorld(path=WORLD, fields=FIELDS, steps_per_tick=spt, native_dt=dt,
                       ports={f: LW.Port(gain=GAIN[f], clip=CLIP[f]) for f in FIELDS},
                       noise={f: ("proportional", 0.0) for f in FIELDS}, overrides={} if dt == 0.1 else {"dt": dt},
                       dx=1.0, sys_path=(LAB,), carry=("t",))


def read(F, D):
    return [D[0].sample(F, 1.0), D[1].sample(F, 1.0), np.stack((F.mean(axis=(1, 2)), F.var(axis=(1, 2))), axis=1)]


res = {"head": subprocess.run(["git", "-C", "/home/user/swpo/residency-environments", "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True).stdout.strip()}
cpu = {}
# (a) my own loop
t0 = time.process_time()
m = LW.LabWorld(path=WORLD, fields=FIELDS, steps_per_tick=1, native_dt=0.1, sys_path=(LAB,)).load()
m.ops.WORKERS = 1
s = m.init(0, (N, N))
for f in FIELDS:
    s[f] = st[f].copy()
s["t"] = st["t"]
D = devs()
cy = (np.arange(N) + 0.5)
yc, xc = D[0].center
dyy = (cy - yc + N / 2) % N - N / 2
dxx = (cy - xc + N / 2) % N - N / 2
bump = np.exp(-(dyy[:, None] ** 2 + dxx[None, :] ** 2) / (2 * 2.0 ** 2))
mine = {0: read(np.stack([s[f] for f in FIELDS]), D)}
for k in range(TICKS[-1]):
    if 250 <= k < 750:
        s["F"] = np.clip(s["F"] + 0.1 * 3.0 * 0.1 * bump, 0.0, None)
    s = m.step(s)
    if k + 1 in TICKS:
        mine[k + 1] = read(np.stack([s[f] for f in FIELDS]), D)
cpu["own_loop"] = time.process_time() - t0
q = [dict(sensor=x, t=TIMES) for x in ("device0", "device1", "global")]
runs = {}
for dt, spt in ((0.1, 1), (0.05, 2), (0.025, 4)):
    t0 = time.process_time()
    o = LW.oracle(world(dt, spt), st, devs())
    o._stepper.module.ops.WORKERS = 1
    runs[dt] = o.sample_truth([PULSE], q, 1, truth_seed=3)["samples"]
    cpu[f"runner_dt{dt}"] = time.process_time() - t0
    res.setdefault("runner_class", type(o).__name__)
par = {}
for qi, sensor in enumerate(("device0", "device1", "global")):
    ref = np.stack([mine[t][qi] for t in TICKS])
    par[sensor] = float(np.abs(runs[0.1][qi][0] - ref).max())
res["parity_with_pulse_max_abs"] = par
# (b) ladder at device0 (RMS over nodes, per field, per time)
ens = np.load(f"{RUN}/suite/controls/c002/independent_native.npz")
ens0 = ens["query0"]  # (8, 15, 4, 13)
allT = [0, 2, 5, 8, 10, 12, 15, 20, 22, 25, 30, 35, 40, 45, 50]
idx = [allT.index(t) for t in TIMES]
lad = {}
for p, f in enumerate(FIELDS):
    a = runs[0.1][0][0, :, p, :]; b = runs[0.05][0][0, :, p, :]; c = runs[0.025][0][0, :, p, :]
    o1 = np.sqrt(((a - b) ** 2).mean(-1)); o2 = np.sqrt(((b - c) ** 2).mean(-1))
    spr = np.sqrt((ens0[:, idx, p, :].std(axis=0) ** 2).mean(-1))
    lad[f] = dict(off_01_005_over_spread=np.round(o1 / spr, 3).tolist(), off_005_0025_over_spread=np.round(o2 / spr, 3).tolist(),
                  ratio=np.round(o1 / np.maximum(o2, 1e-300), 2).tolist())
res["times"] = TIMES
res["ladder_device0"] = lad
res["cpu_s"] = {k: round(v, 1) for k, v in cpu.items()}
json.dump(res, open(f"{OUT}/pulse_parity_ladder.json", "w"), indent=1)
print(json.dumps(res, indent=1))
