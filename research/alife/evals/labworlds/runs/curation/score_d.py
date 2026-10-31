"""(d) dt-halved null against a native-vs-native band, with the suite's frozen groups and scales.

python score_d.py phase_membrane|fed_vortices [n_partitions]

Per case the natives are pooled: independent_native A (8, seeds 81000+i), a second native B
(8, seeds 91000+i) and the 2 frozen truths T (71000+i), all independent. Each partition draws
A' (8), B' (8), T' (2) from the 18 per case; band = sum_cases S(B',T') / sum_cases S(A',T')
(5-95% over partitions); null = sum S(X',T') / sum S(A',T') for the new dt-halved ensemble X'
(own seeds 61000+i), reported as the median over partitions. Scores are blobround6_eval's
energy score (checked equal to score_case on the unpartitioned ensembles); per sensor = mean of
that sensor's groups; windows keep the score times <= 10, <= 25 and all (<= 50) tu.
The suite's own numerical_null X shares A's member seeds; it is shown for comparison only.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "pkg"))
from physim import blobround6_eval as scoring  # noqa: E402

SUITE = HERE.parent / "suite"
SHORT = {"phase_membrane": "pm", "fed_vortices": "fv"}
TIMES = [0, 2, 5, 8, 10, 12, 15, 20, 22, 25, 30, 35, 40, 45, 50]
WINDOWS = (10, 25, 50)


def load(path, nq=3):
    with np.load(path) as z:
        return [z[f"query{q}"] for q in range(nq)]


def main(world, n_part=1000):
    w = SHORT[world]
    sd = SUITE / w
    suite = json.loads((sd / "suite.json").read_text())
    groups = suite["groups"]
    dn = HERE / "dnull" / world
    cases = [(i, e) for i, e in enumerate(suite["cases"]) if (dn / "null_indep" / f"{e['request']['id']}.npz").exists()]
    sensors = ("device0", "device1", "global")
    rng = np.random.default_rng(2026)
    per_case = []
    for i, e in cases:
        cid = e["request"]["id"]
        T = load(sd / e["truth"])
        A = load(sd / "controls" / cid / "independent_native.npz")
        B = load(sd / "band" / f"{cid}.npz") if w == "pm" else load(dn / "native_b" / f"{cid}.npz")
        X = load(sd / "controls" / cid / "numerical_null.npz")
        Xn = load(dn / "null_indep" / f"{cid}.npz")
        IG = load(sd / "ignore_actions.npz")
        WG = load(sd / "controls" / cid / "wrong_probe_geometry.npz")
        members = [np.concatenate([a[q] for a in (A, B, T, X, Xn, IG, WG)]) for q in range(3)]
        idx = dict(A=np.arange(8), B=np.arange(8, 16), T=np.arange(16, 18), X=np.arange(18, 26),
                   Xn=np.arange(26, 34), IG=np.arange(34, 42), WG=np.arange(42, 50))
        # check the energy score against score_case once per case (A vs T, all times)
        ref = scoring.score_case(e["request"], {"samples": A}, {"samples": T}, groups=groups,
                                 n_samples=8, n_truth=2, roster=scoring.PublicRoster(
                                     n_ports=A[0].shape[2], device_slots=tuple(int(d["k"]) for d in suite["devices"])))
        D = {}
        for win in WINDOWS:
            for g in groups:
                sel = [s for s in g["selectors"] if TIMES[s["time_index"]] <= win]
                if not sel:
                    continue
                sc = np.asarray([g["scales"][k] for k, s in enumerate(g["selectors"]) if TIMES[s["time_index"]] <= win])
                V = np.column_stack([members[s["query"]][:, s["time_index"], s["port"], s["slot"]] for s in sel]) / sc
                diff = V[:, None, :] - V[None, :, :]
                D[(win, g["id"])] = np.sqrt((diff ** 2).sum(-1)) / math.sqrt(V.shape[1])
        for g in groups:
            mine = D[(50, g["id"])]
            es = mine[np.ix_(idx["A"], idx["T"])].mean() - 0.5 * mine[np.ix_(idx["A"], idx["A"])].mean()
            r = next(x["energy_score"] for x in ref["joint_energy"] if x["id"] == g["id"])
            assert abs(es - r) <= 1e-9 * max(1, abs(r)), (cid, g["id"], es, r)
        per_case.append(dict(cid=cid, family=e["family"], D=D, idx=idx))

    def es(Dm, P, Q):
        return Dm[np.ix_(P, Q)].mean() - 0.5 * Dm[np.ix_(P, P)].mean()

    def cell_scores(c, assign, win, sensor):
        gids = [g["id"] for g in groups if (sensor is None or g["id"].startswith(sensor + "/")) and (win, g["id"]) in c["D"]]
        out = {}
        for name, P in assign.items():
            if name == "T":
                continue
            out[name] = float(np.mean([es(c["D"][(win, gid)], P, assign["T"]) for gid in gids]))
        return out

    cells = [(win, s) for win in WINDOWS for s in (None,) + sensors]
    fixed, parts = {}, {cell: [] for cell in cells}
    for cell in cells:
        tot = {}
        for c in per_case:
            assign = {k: c["idx"][k] for k in ("A", "B", "T", "X", "Xn", "IG", "WG")}
            for k, v in cell_scores(c, assign, *cell).items():
                tot[k] = tot.get(k, 0.0) + v
        fixed[cell] = {k: tot[k] / tot["A"] for k in tot}
    pool = np.arange(18)
    case_parts = {c["cid"]: [] for c in per_case}
    for r in range(n_part):
        sums = {cell: {} for cell in cells}
        for c in per_case:
            p = rng.permutation(pool)
            assign = dict(A=p[:8], B=p[8:16], T=p[16:18], Xn=c["idx"]["Xn"], X=c["idx"]["X"])
            for cell in cells:
                for k, v in cell_scores(c, assign, *cell).items():
                    sums[cell][k] = sums[cell].get(k, 0.0) + v
                if cell == (50, None):
                    v = cell_scores(c, assign, *cell)
                    case_parts[c["cid"]].append((v["B"] / v["A"], v["Xn"] / v["A"]))
        for cell in cells:
            s = sums[cell]
            parts[cell].append((s["B"] / s["A"], s["Xn"] / s["A"], s["X"] / s["A"]))
    rows = []
    for cell in cells:
        a = np.asarray(parts[cell])
        lo, hi = np.percentile(a[:, 0], [5, 95])
        med = float(np.median(a[:, 1]))
        rows.append(dict(window=cell[0], sensor=cell[1] or "aggregate", band=[round(lo, 3), round(hi, 3)],
                         null_indep_median=round(med, 3), passes=bool(lo <= med <= hi),
                         null_indep_frac_above_band=round(float((a[:, 1] > hi).mean()), 3),
                         null_indep_frac_below_band=round(float((a[:, 1] < lo).mean()), 3),
                         suite_null_median=round(float(np.median(a[:, 2])), 3),
                         fixed={k: round(v, 3) for k, v in fixed[cell].items()}))
    pc = []
    for c in per_case:
        a = np.asarray(case_parts[c["cid"]])
        lo, hi = np.percentile(a[:, 0], [5, 95])
        pc.append(dict(case=c["cid"], family=c["family"], band=[round(lo, 3), round(hi, 3)],
                       null_indep_median=round(float(np.median(a[:, 1])), 3)))
    # pairing check: the suite's null X shares member seeds with A
    pair = {}
    for c in per_case:
        Dm = c["D"][(50, groups[0]["id"])]
        for gid in [g["id"] for g in groups]:
            Dm = c["D"][(50, gid)]
            pair.setdefault("X_m vs A_m (same seed)", []).append(np.mean([Dm[18 + m, m] for m in range(8)]))
            pair.setdefault("X_m vs B_m", []).append(np.mean([Dm[18 + m, 8 + m] for m in range(8)]))
            pair.setdefault("Xn_m vs A_m", []).append(np.mean([Dm[26 + m, m] for m in range(8)]))
            pair.setdefault("A_m vs B_m", []).append(np.mean([Dm[m, 8 + m] for m in range(8)]))
    # per group, unpartitioned: X' over the mean of the two native ensembles (case sums)
    by_group = {}
    for win in WINDOWS:
        for g in groups:
            num = sum(es(c["D"][(win, g["id"])], c["idx"]["Xn"], c["idx"]["T"]) for c in per_case)
            den = sum(0.5 * (es(c["D"][(win, g["id"])], c["idx"]["A"], c["idx"]["T"]) +
                             es(c["D"][(win, g["id"])], c["idx"]["B"], c["idx"]["T"])) for c in per_case)
            bb = sum(es(c["D"][(win, g["id"])], c["idx"]["B"], c["idx"]["T"]) for c in per_case) / \
                sum(es(c["D"][(win, g["id"])], c["idx"]["A"], c["idx"]["T"]) for c in per_case)
            by_group[f"{win}/{g['id']}"] = dict(null_over_pooled=round(num / den, 3), B_over_A=round(bb, 3))
    res = dict(world=world, cases=[c["cid"] for c in per_case], partitions=n_part, rows=rows, per_case=pc,
               by_group=by_group,
               mean_member_distance=dict((k, round(float(np.mean(v)), 4)) for k, v in pair.items()))
    (HERE / "dnull" / f"{world}_scores.json").write_text(json.dumps(res, indent=1) + "\n")
    for r in rows:
        print(r)
    for r in pc:
        print(r)
    print(res["mean_member_distance"])


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1000)
