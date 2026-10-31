"""Review re-runs for noise_intensity (pm, intensity 0.03, ell 2): reproducibility of T[:2], a fresh native F
(fixed-ensemble calibration of 'share above band95'), and a fresh dt/2 null N2. One process, OMP 1."""
import os, sys, json, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from pathlib import Path
NI = Path("/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/noise_intensity")
sys.path.insert(0, str(NI / "scripts"))
import nsweep as NS  # noqa
import analyse as AN  # noqa
LE = NS.LE
HERE = Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
W, LV = "pm", 0.03
spec = NS.make_spec(W, LV)
pulse = NS.WORLD[W]["pulse"]
d = NI / "out" / "score" / W / f"L{LV:g}"

def run(variant, seed, members, name):
    p = OUT / f"{name}.npz"
    if p.exists():
        with np.load(p) as z: return [z[f"query{i}"] for i in range(3)]
    t0 = time.process_time()
    r = LE.make_oracle(spec, variant).sample_truth(pulse, LE.queries(), members, truth_seed=seed)["samples"]
    np.savez_compressed(p, **{f"query{i}": a for i, a in enumerate(r)})
    print(name, f"{time.process_time()-t0:.1f} cpu-s", flush=True)
    return r

res = {}
rep = run("native", NS.SEED0 + 1, 2, "T_repro2")
T = AN.load(d / "T.npz")
res["repro_T_first2_max_abs_diff"] = max(float(np.abs(a - b[:2]).max()) for a, b in zip(rep, T))
F = run("native", 600100, 8, "F_native_fresh")
N2 = run("numerical_null", 600106, 8, "N2_dt2_fresh")
groups = json.loads((AN.SUITE / W / "suite.json").read_text())["groups"]
gids = [g["id"] for g in groups]
ens = {k: AN.load(d / f"{k}.npz") for k in "TABN"}
ens["F"], ens["N2"] = F, N2
subsets = {"agg": gids, **{s: [g for g in gids if g.startswith(s + "/")] for s in AN.SENS}}
for wname, tmax in AN.WIN.items():
    M = {k: AN.group_mats(v, groups, tmax) for k, v in ens.items()}
    nat = {g: np.concatenate([M["T"][g], M["A"][g], M["B"][g]]) for g in gids}
    rng = np.random.default_rng(0)
    rows = {k: {s: [] for s in subsets} for k in ("P1", "P2", "F", "N", "N2")}
    for _ in range(500):
        p = rng.permutation(24); i1, i2, it = p[:8], p[8:16], p[16:]
        per = {k: {} for k in rows}
        for g in gids:
            tr = nat[g][it]
            per["P1"][g] = AN.es(nat[g][i1], tr); per["P2"][g] = AN.es(nat[g][i2], tr)
            for k in ("F", "N", "N2"):
                per[k][g] = AN.es(M[k][g], tr)
        for k in rows:
            for s, gs in subsets.items():
                rows[k][s].append(np.mean([per[k][g] for g in gs]))
    out = {}
    for s in subsets:
        p1 = np.array(rows["P1"][s]); band = np.array(rows["P2"][s]) / p1
        b95 = float(np.quantile(band, 0.95))
        e = dict(band95=round(b95, 3))
        for k in ("F", "N", "N2"):
            r = np.array(rows[k][s]) / p1
            e[k] = [round(float(np.median(r)), 3), round(float((r > b95).mean()), 3)]
        out[s] = e
    res[wname] = out
(OUT / "recheck.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
