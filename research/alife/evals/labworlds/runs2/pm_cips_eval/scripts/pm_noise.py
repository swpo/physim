"""Item 1: phase_membrane at intensity 0.01 (ell 2) with dt halved (2 native steps of 0.5 per tick) and its dt/4 null.

  run NAME     one 8-member ensemble on the K pulse program (device0, t=0, amp 3, dur 10) from prep_s0:
               T, A, B natives (dt 0.5), I native on the sham program (ignore actions), N1, N2 dt/4 nulls (dt 0.25)
  det          zero-noise single members at dt 0.5 and dt 0.25 (deterministic dt error)
  analyse      band of 2000 partitions of the 24 natives (P1, P2, truth 8 each); null and ignore ratios;
               groups/scales of the frozen labeval pm suite (as noise_intensity/analyse.py)
Seeds 620000 + k (k = 1.. per ensemble), separate from every earlier namespace.
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, "/home/user/evalwork/pm_cips_eval/scripts")
from common import PC, E, LW, EVALPILOT, OUT
import numpy as np
from physim import blobround6_eval as SC

D = Path(OUT) / "pm_noise"
D.mkdir(parents=True, exist_ok=True)
LEVEL, DT, NULL_DT = 0.01, 0.5, 0.25
PULSE = [dict(t=0, kind="inject", device=0, port=1, amp=3.0, dur=10.0)]
ENS = {"T": ("native", PULSE, 1), "A": ("native", PULSE, 2), "B": ("native", PULSE, 3), "I": ("native", [], 5),
       "N1": ("null", PULSE, 6), "N2": ("null", PULSE, 7)}
SEED0 = 620000
SUITE_PM = Path(EVALPILOT) / "suite" / "pm" / "suite.json"


def setup():
    st = PC.load_state(f"{EVALPILOT}/out/prep_s0.npz", PC.PM_FIELDS)
    info = json.load(open(f"{EVALPILOT}/out/prep_s0.json"))
    devs = [PC.device(0, info["sites"]["centre"], 128), PC.device(1, info["sites"]["other"], 128)]
    return st, devs


def world(kind, level=LEVEL):
    return PC.pm_world(level, NULL_DT if kind == "null" else DT)


def ensemble(name, members=8, level=LEVEL, det=False):
    kind, actions, k = ENS[name] if not det else (name, PULSE, 9)
    st, devs = setup()
    w = world(kind, 0.0 if det else level)
    if det:
        w = PC.replace(w, noise_corr={})
    path = D / (f"det_{kind}.npz" if det else f"{name}.npz")
    meta = dict(name=name, actions=actions, seed=SEED0 + k, members=members, declaration=PC.jsonable(w.declaration()))
    o = LW.oracle(w, st, devs)
    return E.cached(path, lambda: o.sample_truth(actions, E.queries(), members, truth_seed=SEED0 + k), meta=dict(
        request=dict(id=name, actions=actions, queries=E.queries()), **meta))


def load(p):
    with np.load(p, allow_pickle=False) as z:
        return [z[f"query{i}"] for i in range(3)]


def mats(samples, groups, tmax):
    out = {}
    for g in groups:
        sel = [(s, sc) for s, sc in zip(g["selectors"], g["scales"]) if tmax is None or E.TIMES[s["time_index"]] <= tmax]
        out[g["id"]] = np.column_stack([samples[s["query"]][:, s["time_index"], s["port"], s["slot"]] / sc for s, sc in sel])
    return out


def analyse(npart=2000):
    """Partition band as noise_intensity/analyse.py, from precomputed pairwise RMS distances (same energy score)."""
    groups = json.loads(SUITE_PM.read_text())["groups"]
    gids = [g["id"] for g in groups]
    names = [k for k in ENS if (D / f"{k}.npz").exists()]
    ens = {k: load(D / f"{k}.npz") for k in names}
    sizes = {k: ens[k][0].shape[0] for k in names}
    off, o = {}, 0
    for k in names:
        off[k] = np.arange(o, o + sizes[k]); o += sizes[k]
    subsets = {"agg": gids, **{s: [g for g in gids if g.startswith(s + "/")] for s in E.SENSORS}}
    res = {}
    for wname, tmax in (("50tu", None), ("10tu", 10)):
        M = {k: mats(v, groups, tmax) for k, v in ens.items()}
        Dm = {}
        for g in gids:
            V = np.concatenate([M[k][g] for k in names])
            diff = V[:, None, :] - V[None, :, :]
            Dm[g] = np.sqrt((diff ** 2).sum(-1) / V.shape[1])
        nat = np.concatenate([off["T"], off["A"], off["B"]])
        others = [k for k in names if k not in "TAB"] + (["N12"] if "N1" in names and "N2" in names else [])
        idx = dict(off)
        if "N12" in others:
            idx["N12"] = np.concatenate([off["N1"], off["N2"]])

        def es(g, P, T):
            return Dm[g][np.ix_(P, T)].mean() - 0.5 * Dm[g][np.ix_(P, P)].mean()
        rng = np.random.default_rng(0)
        rows = {k: {s: [] for s in subsets} for k in ["P1", "P2", "P12"] + others}
        for _ in range(npart):
            p = nat[rng.permutation(24)]
            i1, i2, it = p[:8], p[8:16], p[16:]
            per = {"P1": {g: es(g, i1, it) for g in gids}, "P2": {g: es(g, i2, it) for g in gids},
                   "P12": {g: es(g, np.concatenate([i1, i2]), it) for g in gids}}
            for k in others:
                per[k] = {g: es(g, idx[k], it) for g in gids}
            for k in rows:
                for s, gs in subsets.items():
                    rows[k][s].append(np.mean([per[k][g] for g in gs]))
        w = {}
        for s in subsets:
            p1 = np.array(rows["P1"][s])
            band = np.array(rows["P2"][s]) / p1
            e = dict(ref_score=round(float(np.median(p1)), 4), band=[round(float(q), 3) for q in np.quantile(band, [0.05, 0.5, 0.95])])
            for k in others:
                den = np.array(rows["P12"][s]) if k == "N12" else p1
                r = np.array(rows[k][s]) / den
                e[k] = [round(float(q), 3) for q in np.quantile(r, [0.05, 0.5, 0.95])]
                e[k + "_frac_above_band95"] = round(float((r > e["band"][2]).mean()), 3)
            w[s] = e
        natv = {g: np.concatenate([M["T"][g], M["A"][g], M["B"][g]]) for g in gids}
        spread = {g: float(np.sqrt(natv[g].var(axis=0, ddof=1).mean())) for g in gids}
        w["spread_rms"] = {g: round(v, 4) for g, v in spread.items()}
        if (D / "det_native.npz").exists() and (D / "det_null.npz").exists():
            D1, D2 = mats(load(D / "det_native.npz"), groups, tmax), mats(load(D / "det_null.npz"), groups, tmax)
            w["det_dt_error_over_spread"] = {g: round(float(np.sqrt(((D1[g] - D2[g]) ** 2).mean()) / spread[g]), 3) for g in gids}
        res[wname] = w
    (D / "analysis.json").write_text(json.dumps(res, indent=1))
    for wname in res:
        for s in subsets:
            print(wname, s, json.dumps(res[wname][s]))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "run":
        for name in sys.argv[2:]:
            ensemble(name)
    elif cmd == "det":
        ensemble("native", members=1, det=True)
        ensemble("null", members=1, det=True)
    else:
        analyse()
