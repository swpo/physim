
"""Measurement-adequacy certification + CRPS cross-check (DESIGN v0.15), v2.
Fixed verbatim contract templates (same channel, protocol, stat for every
world instance) -> clean variance decomposition:
  A = Var_instances(mu) / mean_instances(tau^2)
CRPS cross-check: instance-aware oracle (own-seed quantiles) vs climatology
(pooled quantiles) -> per-contract gap; Spearman(log A, gap) tests whether
CRPS recovers the auditable adequacy signal.
"""
import json, numpy as np
from scipy.stats import spearmanr
from physim.engine import make_world
from physim.session import (PhysimSession, Contract, truth_statistic,
                            answer_scale, crps_accuracy, QLEVELS)

def hold(u, T): return {"t": int(T), "u": [round(float(x),3) for x in u]}

def templates(w, chans):
    n_in = w.p.n_in
    z = np.zeros(n_in)
    c1, c2 = chans[0], chans[1 % len(chans)]
    return [
        Contract(0, "S1", [hold(z, 700)], c1, stat="mean"),
        Contract(1, "S1", [hold(z, 700)], c2, stat="sd"),
        Contract(2, "S2", [hold(np.full(n_in, 0.8), 1100)], c1, stat="mean"),
        Contract(3, "S2", [hold(np.full(n_in, -0.6), 1100)], c1, stat="mean"),
        Contract(4, "S3", [hold(np.full(n_in, -0.85), 650), hold(z, 900)], c1, stat="mean"),
        Contract(5, "S4", [hold(np.full(n_in, -1.0), 1500)], c1, stat="mean"),
        Contract(6, "S2", [hold(np.full(n_in, 0.4), 1100)], c2, stat="mean"),
        Contract(7, "S3", [hold(np.full(n_in, -0.7), 650), hold(z, 900)], c2, stat="sd"),
    ]

def adequacy_table(difficulty, seeds, ensemble):
    worlds = [make_world(difficulty, s_) for s_ in seeds]
    live_sets = [set(np.where(~w.true_is_dead().astype(bool))[0].tolist())
                 if hasattr(w, "true_is_dead") else set(range(w.p.n_out)) for w in worlds]
    common = sorted(set.intersection(*live_sets))[:2] or [0, 1]
    per_id = {}
    for s_, w in zip(seeds, worlds):
        ranges = w.true_channel_range()
        for c in templates(w, common):
            mu, tau, samples = truth_statistic(w, c, ensemble=ensemble)
            scale = answer_scale(tau, float(ranges[c.channel]), c.stat,
                                 getattr(w.p, "reaction", "tanh"))
            per_id.setdefault(c.id, {"stratum": c.stratum, "rows": []})["rows"].append(
                {"seed": s_, "mu": mu, "tau": tau, "samples": samples, "scale": scale})
    out = []
    for cid, d in sorted(per_id.items()):
        mus = np.array([r["mu"] for r in d["rows"]])
        taus = np.array([r["tau"] for r in d["rows"]])
        scale = float(np.mean([r["scale"] for r in d["rows"]]))
        A = float(mus.var() / max((taus**2).mean(), 1e-12))
        gaps, ors, cls = [], [], []
        for r in d["rows"]:
            own = r["samples"]
            pooled = [x for rr in d["rows"] for x in rr["samples"]]
            q_own = {str(p): float(np.quantile(own, p)) for p in QLEVELS}
            q_pool = {str(p): float(np.quantile(pooled, p)) for p in QLEVELS}
            a_or = crps_accuracy(own, scale, {"mean": float(np.mean(own)), "quantiles": q_own})["accuracy_crps"]
            a_cl = crps_accuracy(own, scale, {"mean": float(np.mean(pooled)), "quantiles": q_pool})["accuracy_crps"]
            ors.append(a_or); cls.append(a_cl); gaps.append(a_or - a_cl)
        out.append({"id": cid, "stratum": d["stratum"], "A": round(A, 2),
                    "gap": round(float(np.mean(gaps)), 3),
                    "oracle": round(float(np.mean(ors)), 3),
                    "climatology": round(float(np.mean(cls)), 3)})
    return out

report = {}
for diff, seeds, ens in (("B2", range(5), 4), ("C4", range(3), 4), ("D2", range(4), 4)):
    tbl = adequacy_table(diff, seeds, ens)
    report[diff] = tbl
    print("== %s ==  (fixed templates, common-live channels)" % diff, flush=True)
    print(" id  stratum   A_ratio  CRPSgap  oracle  climatology")
    for r in tbl:
        print("%3d  %s  %8s  %7.3f  %6.3f  %10.3f" % (r["id"], r["stratum"], r["A"], r["gap"], r["oracle"], r["climatology"]), flush=True)
    rho, pv = spearmanr([np.log10(max(r["A"],1e-9)) for r in tbl], [r["gap"] for r in tbl])
    print(" Spearman(log A, CRPS gap) = %.3f (p=%.4f)" % (rho, pv), flush=True)
json.dump(report, open("/tmp/adequacy_report.json","w"), indent=1)
