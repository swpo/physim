
"""sync_runner.py -- candidate evaluator for COUPLED COUNTERS (metric-locked).

L4 METRIC LOCK (2026-02-17, before certification):
  phase phi_i = piecewise-linear cycle phase from UP-flips of ring i's
  dominant 2-level count; Delta = phi1 - phi2 (cycles).
  slips = hysteretic integer-winding events of Delta (+-1 cycle steps).
  rho = winding(phi1)/winding(phi2) over the analysis window (t >= 2000).
  LOCKED verdict: 0 slips AND max|Delta - median| < 1 cycle over a span
  >= 8 joint cycles. SLIP verdict: >= 3 slips; T_slip = median inter-slip
  interval (also T_slip_rate = span/|net winding| as consistency check).
  G2-slip: oscillator/switch fit r2 >= 0.85 on sin(2*pi*Delta), >= 5 slips.
  G2-tongue: rotation-number plateau (staircase reported separately).

Theory coordinates of a candidate:
  R      = eps1/eps2 detuning ratio (rho_0 = R by the round-1 law T=3.8/eps)
  eps_g  = geometric-mean gain sqrt(eps1*eps2) (fixed 2.77e-3 default)
  kc     = C-leakage coupling
  seed, steps
"""
import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter/sync")
from sync_sim import simulate2
from sync_metrics import l4_analysis, counting_alive
from runner import event_stats, micro_tau
from hier_metrics import compact_top_fit

BASE = dict(ny=8, nx=64, dx=1.0, dt=0.1, a=0.1, b=0.9, Du=1.0, Dv=11.0,
            Dc=10.0, sigma=1.0, kstar2=0.2682, noise_amp=2e-3)


def eval_sync(cand, steps=250000, seed=1):
    R, kc = cand["R"], cand["kc"]
    eps_g = cand.get("eps_g", 2.77e-3)
    eps1 = eps_g * np.sqrt(R)
    eps2 = eps_g / np.sqrt(R)
    p = dict(BASE, eps1=eps1, eps2=eps2, kappa_c=kc, steps=steps,
             meas_every=25, seed=seed, trace_win=(steps // 3, steps // 3 + 15000))
    p.update({k: cand[k] for k in cand if k in ("noise_amp", "kstar2", "Dv")})
    t0 = time.time()
    r = simulate2(p)
    res = {"cand": dict(cand), "eps1": eps1, "eps2": eps2, "seed": seed,
           "steps": steps, "runtime_s": round(time.time() - t0, 1)}
    if "blown" in r:
        res["status"] = "numerics_blowup"
        return res
    t = r["t"]
    al1 = counting_alive(t, r["nz"][:, 0])
    al2 = counting_alive(t, r["nz"][:, 1])
    res["alive1"], res["alive2"] = al1, al2
    if not (al1["alive"] and al2["alive"]):
        res["status"] = "counter_dead"
        return res
    a = l4_analysis(t, r["nz"][:, 0], r["nz"][:, 1])
    if a["status"] != "ok":
        res["status"] = "l4_" + a["status"]
        return res
    delta_t, delta = a.pop("delta_t"), a.pop("delta")
    res.update({k: (round(v, 4) if isinstance(v, float) else v)
                for k, v in a.items()})
    # L1: micro tau from ring-0 pixel trace
    tau1 = micro_tau(r.get("trace"), 0.1) if r.get("trace") is not None else None
    res["tau1"] = round(tau1, 1) if tau1 else None
    # L2: defect-event duration on ring 0 (locked round-1 metric)
    m = t >= 2000
    ev = event_stats(t[m], r["envmin"][m, 0], r["nz"][m, 0])
    res["tau2"] = round(ev["tau2"], 1) if ev.get("tau2") else None
    res["n_events"] = ev["n_events"]
    # L3: mean counter period
    T3 = 0.5 * (a["T1"] + a["T2"])
    res["T3"] = round(T3, 1)
    # L4: verdict-dependent
    verdict = "locked" if a["locked"] else ("slip" if a["n_slips"] >= 3 else "marginal")
    res["verdict"] = verdict
    span_cyc = a["span"] / T3
    res["span_cycles"] = round(span_cyc, 1)
    if verdict == "locked" and span_cyc < 8:
        res["verdict"] = verdict = "marginal"
    if verdict == "slip":
        tau4 = a["T_slip"]
        res["tau4"] = round(tau4, 1) if tau4 else None
        # G2 on sin(2 pi Delta)
        x = np.sin(2 * np.pi * delta)
        ft = compact_top_fit(x, dt=float(delta_t[1] - delta_t[0]))
        res["top_model"], res["top_r2"] = ft["model"], ft["r2"]
        res["top_params"] = {k: (round(v, 2) if isinstance(v, float) else v)
                             for k, v in ft["params"].items()}
        g2 = (ft["r2"] >= 0.85 and a["n_slips"] >= 5
              and ft["model"] in ("oscillator", "switch"))
    else:
        res["tau4"] = None
        g2 = verdict == "locked"   # plateau law certified via staircase table
    # G1: 4-layer separations (tau4 only meaningful in slip regime)
    sep12 = (res["tau2"] / res["tau1"]) if (res["tau2"] and res["tau1"]) else 0.0
    sep23 = (T3 / res["tau2"]) if res["tau2"] else 0.0
    res["sep12"], res["sep23"] = round(sep12, 1), round(sep23, 1)
    if verdict == "slip" and res["tau4"]:
        res["sep34"] = round(res["tau4"] / T3, 1)
        g1 = sep12 >= 5 and sep23 >= 5 and res["sep34"] >= 5 and a["n_slips"] >= 3
    else:
        res["sep34"] = None
        g1 = sep12 >= 5 and sep23 >= 5   # 4th layer = infinite-period plateau
    g5 = res["runtime_s"] <= 300
    res["G1"], res["G2"], res["G5"] = bool(g1), bool(g2), bool(g5)
    res["status"] = "ok"
    return res


if __name__ == "__main__":
    for cand in [dict(R=1.333, kc=2e-3), dict(R=1.333, kc=0.0)]:
        out = eval_sync(cand, steps=160000)
        print(json.dumps(out, indent=None, default=str))
