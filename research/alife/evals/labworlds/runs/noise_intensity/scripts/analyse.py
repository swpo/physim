"""Control separation per noise level: ratios to an independent native, with a native-vs-native band.

For each world and level: the 24 native members (T, A, B; independent seeds) are partitioned at random 2000 times
into a reference predictor P1, a second predictor P2 and a truth Tr (8 each). Per partition, PhySim's joint energy
score per frozen labeval group (scales from the white-noise calibration, the same at every level), averaged over
groups (all 'agg', or one sensor's groups). Band = P2/P1 (5-95%); control ratios X/P1 (ablation) and I/P1
(ignore-actions: the sham-program native scored against the pulse truth); medians over partitions. Also the
designated split (A predicts T), scored with blobround6_eval.score_case. Windows: all 13 score times (to 50 tu)
and the early times <= 10 tu. Spread: RMS member deviation of the 24 natives, in group-scale units.
Deterministic dt screen (zero noise, dt vs dt/2, same pulse program): RMS difference / member spread per group.
"""
import json, sys
from pathlib import Path
import numpy as np

sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
sys.path.insert(0, "/home/user/swpo/residency-environments/scripts/physim/labworlds")
import labeval as LE  # noqa: E402
from physim import blobround6_eval as SC  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "out"
SUITE = Path("/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/suite")
NPART = 2000
WIN = {"50tu": None, "10tu": 10}
SENS = ("device0", "device1", "global")
PULSE = {"pm": [dict(t=0, kind="inject", device=0, port=1, amp=3.0, dur=10.0)],
         "fv": [dict(t=0, kind="inject", device=0, port=0, amp=3.0, dur=10.0)]}


def load(path):
    with np.load(path, allow_pickle=False) as z:
        return [z[f"query{i}"] for i in range(3)]


def group_mats(samples, groups, tmax):
    out = {}
    for g in groups:
        sel = [(s, sc) for s, sc in zip(g["selectors"], g["scales"]) if tmax is None or LE.TIMES[s["time_index"]] <= tmax]
        out[g["id"]] = np.column_stack([samples[s["query"]][:, s["time_index"], s["port"], s["slot"]] / sc
                                        for s, sc in sel])
    return out


def es(x, y):
    return SC._energy_score(x, y)


def summarise(world, d, groups):
    ens = {k: load(d / f"{k}.npz") for k in "TABXI"}
    has_null = (d / "N.npz").exists()
    if has_null:
        ens["N"] = load(d / "N.npz")
    res = {}
    gids = [g["id"] for g in groups]
    subsets = {"agg": gids, **{s: [g for g in gids if g.startswith(s + "/")] for s in SENS}}
    case = dict(id="pulse", actions=PULSE[world], queries=LE.queries())
    rost = LE.roster(WORLD_SPEC[world])
    fixed = {}
    for k in ("B", "X", "I") + (("N",) if has_null else ()):
        r = SC.score_case(case, {"samples": ens[k]}, {"samples": ens["T"]}, groups=groups, n_samples=8, n_truth=8,
                          roster=rost)
        ref = SC.score_case(case, {"samples": ens["A"]}, {"samples": ens["T"]}, groups=groups, n_samples=8, n_truth=8,
                            roster=rost)
        fixed[k] = round(r["joint_energy_equal_group_mean"] / ref["joint_energy_equal_group_mean"], 3)
    res["designated_split_A_predicts_T"] = fixed
    for wname, tmax in WIN.items():
        M = {k: group_mats(v, groups, tmax) for k, v in ens.items()}
        nat = {g: np.concatenate([M["T"][g], M["A"][g], M["B"][g]]) for g in gids}
        rng = np.random.default_rng(0)
        rows = {k: {s: [] for s in subsets} for k in ("P1", "P2", "X", "I", "N")}
        for _ in range(NPART):
            p = rng.permutation(24)
            i1, i2, it = p[:8], p[8:16], p[16:]
            per = {k: {} for k in rows}
            for g in gids:
                tr = nat[g][it]
                per["P1"][g] = es(nat[g][i1], tr)
                per["P2"][g] = es(nat[g][i2], tr)
                per["X"][g] = es(M["X"][g], tr)
                per["I"][g] = es(M["I"][g], tr)
                if has_null:
                    per["N"][g] = es(M["N"][g], tr)
            for k in rows:
                if k == "N" and not has_null:
                    continue
                for s, gs in subsets.items():
                    rows[k][s].append(np.mean([per[k][g] for g in gs]))
        w = {}
        for s in subsets:
            p1 = np.array(rows["P1"][s])
            band = np.array(rows["P2"][s]) / p1
            entry = dict(ref_score=round(float(np.median(p1)), 4),
                         band=[round(float(q), 3) for q in np.quantile(band, [0.05, 0.5, 0.95])])
            for k, name in (("X", "ablation"), ("I", "ignore_actions"), ("N", "dt_half_null")):
                if k == "N" and not has_null:
                    continue
                r = np.array(rows[k][s]) / p1
                entry[name] = [round(float(q), 3) for q in np.quantile(r, [0.05, 0.5, 0.95])]
                entry[name + "_frac_above_band95"] = round(float((r > entry["band"][2]).mean()), 3)
            w[s] = entry
        # spread of the natives and the deterministic dt screen
        spread = {g: float(np.sqrt(nat[g].var(axis=0, ddof=1).mean())) for g in gids}
        w["spread_rms"] = {g: round(v, 4) for g, v in spread.items()}
        det = OUT / "score" / world / "det"
        if (det / "det_dt.npz").exists():
            D1 = group_mats(load(det / "det_dt.npz"), groups, tmax)
            D2 = group_mats(load(det / "det_dt2.npz"), groups, tmax)
            w["det_dt_error_over_spread"] = {g: round(float(np.sqrt(((D1[g] - D2[g]) ** 2).mean()) / spread[g]), 3)
                                             for g in gids}
        res[wname] = w
    return res


WORLD_SPEC = {}


def main():
    worlds = sys.argv[1:] or ["pm", "fv"]
    allres = {}
    for world in worlds:
        WORLD_SPEC[world] = (LE.phase_membrane if world == "pm" else LE.fed_vortices)()
        groups = json.loads((SUITE / world / "suite.json").read_text())["groups"]
        base = OUT / "score" / world
        levels = sorted((float(p.name[1:]), p) for p in base.glob("L*") if all((p / f"{k}.npz").exists() for k in "TABXI"))
        allres[world] = {}
        for lv, d in levels:
            allres[world][f"{lv:g}"] = summarise(world, d, groups)
            r = allres[world][f"{lv:g}"]["50tu"]["agg"]
            print(world, lv, json.dumps(r), allres[world][f"{lv:g}"]["designated_split_A_predicts_T"], flush=True)
    path = OUT / "separation.json"
    old = json.loads(path.read_text()) if path.exists() else {}
    old.update(allres)
    path.write_text(json.dumps(old, indent=1))


if __name__ == "__main__":
    main()
