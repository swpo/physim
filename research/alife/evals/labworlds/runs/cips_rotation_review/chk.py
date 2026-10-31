"""Review checks for cips_rotation. usage: chk.py stencil | rerun | plant ISO T_END"""
import os
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[v] = "1"
import sys, json, time
import numpy as np
sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
from physim import labworld as LW
LAB = "/home/user/physim/research/alife"
sys.path.insert(0, LAB)
from labkit import metrics as M
ROT = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/cips_rotation"
sys.path.insert(0, ROT)
WORLD = f"{LAB}/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py"
HERE = os.path.dirname(os.path.abspath(__file__))


def load(iso):
    w = LW.LabWorld(path=os.path.join(ROT, "world_iso.py") if iso else WORLD, fields=("e", "p", "F", "s"),
                    steps_per_tick=1, native_dt=0.1, overrides={}, dx=1.0, sys_path=(LAB,))
    m = w.load(); m.ops.WORKERS = 1
    return m


mode = sys.argv[1]
if mode == "stencil":
    m0, m1 = load(0), load(1)
    N = 96; yy, xx = np.mgrid[0:N, 0:N].astype(float)
    e = np.full((N, N), 0.5)
    out = {}
    for name, f in (("std", m0.vf_flux_div), ("iso", m1.vf_flux_div_iso)):
        r = {}
        for (a, b) in ((8, 0), (6, 6), (12, 0), (9, 9), (16, 0), (11, 11)):   # |k| pairs roughly equal: (8,0)~(6,6)
            k = 2 * np.pi * np.array([a, b]) / N
            p = np.cos(k[0] * xx + k[1] * yy)
            D = -f(e, p, 1.0) / 0.25          # = discrete lap p
            sym = float((D * p).sum() / (p * p).sum())
            r[f"k=({a},{b}) |k|={np.hypot(*k):.3f}"] = round(sym / -(k @ k), 4)
        rng = np.random.default_rng(0)
        er, pr = np.clip(rng.random((N, N)), 0, 1), rng.random((N, N))
        r["sum_div_random"] = float(f(er, pr, 3.0).sum())
        out[name] = r
    print(json.dumps(out, indent=1))
elif mode == "rerun":
    from rotdiv import rotated_xi
    res = {}
    m0 = load(0)
    s = m0.init(5, (192, 192)); q = s["par"]
    xi, _ = rotated_xi(5, 30.0, 192)
    e30 = np.clip(q["e0"] + q["noise"] * xi, 0, 1)
    Z = np.load(f"{ROT}/out/r30_s5_snaps.npz")
    res["r30_s5_e_t0_maxabs_vs_stored_f16"] = float(np.abs(e30 - Z["e_t0"].astype(float)).max())
    m1 = load(1)
    s = m1.init(5, (192, 192)); t0 = time.process_time()
    for k in range(10000):
        s = m1.step(s)
    Z = np.load(f"{ROT}/out/iso_s5_snaps.npz")
    ref = Z["e_t1000"].astype(float)
    res["iso_s5_e_t1000_maxabs_vs_stored_f16"] = float(np.abs(s["e"] - ref).max())
    res["iso_s5_t"] = s["t"]; res["cpu_s"] = round(time.process_time() - t0, 1)
    seg = M.segment(s["e"], 0.5, 6, True)
    res["iso_s5_bodies_t1000"] = int(seg["n"])
    print(json.dumps(res, indent=1))
elif mode == "plant":
    iso, T = int(sys.argv[2]), float(sys.argv[3])
    from rotdiv import comp_moments, wrap
    m = load(iso)
    m.P["noise"] = 0.0
    s = m.init(5, (192, 192)); q = s["par"]
    assert q["noise"] == 0.0
    N = 192; yy, xx = np.mgrid[0:N, 0:N].astype(float)
    # four planted ellipses, 96 apart (fuel/product interaction lengths ~10 and ~3 wu), e = 0.9, area ~ 230
    bodies = [((48, 48), 20, 1.3), ((48, 144), 20, 2.0), ((144, 48), 65, 1.3), ((144, 144), 100, 2.0)]
    e = s["e"].copy()
    for (cy, cx), ang, asp in bodies:
        a = np.sqrt(230 / np.pi * asp); b = a / asp; th = np.radians(ang)
        X, Y = xx - cx, yy - cy
        u = np.cos(th) * X + np.sin(th) * Y; v = -np.sin(th) * X + np.cos(th) * Y
        e = np.where((u / a) ** 2 + (v / b) ** 2 < 1, 0.9, e)
    s["e"] = e; s["p"] = m._ss_p(e, s["F"], q["kc"], q["ks"])
    hist = []
    t0 = time.process_time()
    nst = int(round(T / 0.1))
    for k in range(nst + 1):
        if k % 1000 == 0:
            seg = M.segment(s["e"], 0.5, 6, True)
            A, R = comp_moments(seg["lab"], seg["n"], N)
            row = [round(k * 0.1)]
            for (cy, cx), _, _ in bodies:
                d = np.hypot(wrap(seg["cy"] - cy, N), wrap(seg["cx"] - cx, N))
                j = int(np.argmin(d)) if seg["n"] else -1
                row.append((round(float(A[j]), 1), round(float(R[j]), 2), int(seg["area"][j]), round(float(d[j]), 1)) if j >= 0 and d[j] < 30 else None)
            row.append(int(seg["n"]))
            hist.append(row); print(row, flush=True)
        if k < nst:
            s = m.step(s)
    json.dump(dict(iso=iso, bodies=bodies, hist=hist, cpu_s=round(time.process_time() - t0, 1)),
              open(os.path.join(HERE, f"plant_iso{iso}.json"), "w"), indent=1)
