"""Checks of the committed correlated noise (b23a593, pinned in pkg/) on the CIPS world.
 (a) default unchanged: member 0 of the previous runner's cached independent_native ensembles (made at ec321ea,
     white noise) re-drawn with the pinned package, byte comparison.
 (b) unit noise from LabStepper._smooth at N=192 (dx 1) and N=288 (dx 2/3), ell = 2 world units: per-point
     variance, correlation at world separations 0..8 vs exp(-r^2/16).
 (c) the generator state after 40 ticks with and without noise_corr is the same (same draws per step).
"""
import json, sys, time
sys.argv = sys.argv[:1]
import numpy as np
import cconv as K
C, LW = K.C, K.LW
res = {"pkg": (K.HERE / "pkg" / "HEAD").read_text().strip()}
t0 = time.process_time()
old = C.OUT / "suite"
suite = json.loads((old / "suite.json").read_text())
w_white = C.world()   # previous runner's declaration: white proportional 0.01
o = K.oracle(w_white, 192)
case = suite["cases"][1]
new = o.sample_truth(case["actions"], case["queries"], 1, truth_seed=C.FORECAST_SEED + 1)["samples"]
with np.load(old / "controls" / case["id"] / "independent_native.npz") as z:
    res["a_default_bytes_equal_member0_c002"] = all(np.array_equal(n[0], z[f"query{i}"][0]) for i, n in enumerate(new))
res["a_cpu_s"] = round(time.process_time() - t0, 1)
rng = np.random.default_rng(1)
for N in (192, 288):
    w = K.world(0.1, N)
    st = LW.LabStepper.__new__(LW.LabStepper); st.world = w; st._filters = {}
    acc2 = np.zeros((N, N)); cf = np.zeros(9); M = 300
    for _ in range(M):
        x = st._smooth(rng.standard_normal((N, N)), K.ELL)
        acc2 += x * x
        ac = np.fft.irfft2(np.abs(np.fft.rfft2(x)) ** 2, s=(N, N)) / (N * N)
        cf += np.interp(np.arange(9) * N / 192, np.arange(N), (ac[0] + ac[:, 0]) / 2) / M
    v = acc2 / M
    res[f"b_N{N}"] = dict(per_point_var_mean=round(float(v.mean()), 4), per_point_var_sd=round(float(v.std()), 4),
                          corr_r0_8=np.round(cf / cf[0], 3).tolist())
res["b_theory_exp(-r^2/16)"] = np.round(np.exp(-np.arange(9) ** 2 / 16), 3).tolist()
st0, _ = C.prepared()
for name, w in (("white", K.world(ell=0)), ("corr", K.world())):
    s = LW.LabStepper(w, dict(w.aux(st0), _grid=(192, 192))); C.one_worker(s.module)
    sim = LW.template(w, st0, 9); s(sim, 40)
    res[f"c_rng_{name}"] = sim["rng"].bit_generator.state["state"]["state"]
res["c_same_draws"] = res.pop("c_rng_white") == res.pop("c_rng_corr")
json.dump(res, open(K.OUT / "noisecheck.json", "w"), indent=1)
print(json.dumps(res, indent=1))
