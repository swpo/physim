"""make_summary2 -- study foundrylong, stage 2: job outputs -> results/analysis_stage2.json (CPU, seconds).

    python -B make_summary2.py DIR --job r6-foundrylong-002 [--out results/analysis_stage2.json] [--boot 4000]

The rules of DECLARED.md (stage 2) with the details of DEVIATIONS.md addendum 3. Halves, L, bounds and leave-one-out as
in make_summary.py (imported). Policies (base names in scores.npz): P0w1000 (3 seeds), C16384 (1), FT{c}@32 (3),
D{c}@32 (3), Dr{c}@32, W{c} (2 fits), Wp{c} (W+, 1), Wtrue, Wprior, K, O, Kp, plugTrue, plugU0, plugPrior; c = m (mix
Lab) or d (designed Lab).
  G*(c)   the best of P0w1000, FT{c}@32, D{c}@32, Dr{c}@32 on the unscored half
  W*(c)   the better of W{c} and Wp{c} on the unscored half
  T1 sigma_G = (L(G*) - L(C)) / (L(K) - L(C)), mix, 16 ticks: pass if the 10th percentile >= 0.15 with all worlds and each
     left out; fail if the 90th percentile < 0.15 likewise; else undecided
  T2 rho_G = (L(P0) - L(G*)) / (L(P0) - L(C)): read only if L(P0) - L(C) > 2 SE; "fail" if its 10th percentile > 0.7
  T3 r = (L(G*) - L(W*)) / (L(G*) - L(C)) >= 0.7 at the point, and W* beats G* at t >= 3 (paired over worlds)
  T4 L(W*, mix) - L(W*, designed) > 2 SE (paired over worlds) and > L(G*, mix) - L(G*, designed) at the point
  T5 (L(plugU0) - L(O)) / (L(K) - L(O)) on items with a program: 5th percentile >= 0.10
  T6 T1 and T3 at the point at 8 and 32 ticks, and at 16 ticks with each world left out
PILOT ONLY: the job's hidden worlds are public pilot material; never an exam.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from make_summary import BAR, A, load, verdict  # noqa: E402

REC, TSTAT, SHARE = 0.7, 3.0, 0.7


def sdiv(x, y):
    return x / y if y != 0 else float("nan")


def paired(an, b1, b2, j, ws=None):
    """Per-world L(b1) - L(b2) (seed means), scored half: mean, SE over worlds, t."""
    ws = np.arange(an.W) if ws is None else ws
    d = np.array([np.mean([an.Lw["scored"][n][k, j] for n in an.bases[b1]]) - np.mean([an.Lw["scored"][n][k, j] for n in an.bases[b2]])
                  for k in ws])
    se = float(d.std(ddof=1) / np.sqrt(len(d)))
    return dict(mean=float(d.mean()), se=se, t=float(d.mean() / se) if se > 0 else None, median=float(np.median(d)),
                worlds_positive=int((d > 0).sum()), n=int(len(d)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--job", required=True)
    ap.add_argument("--out", default=os.path.join(HERE, "results", "analysis_stage2.json"))
    ap.add_argument("--boot", type=int, default=4000)
    a = ap.parse_args()
    S, meta, js = load(a.dir)
    an = A(S, meta, a.boot)
    HS = an.HS
    j16 = HS.index(16)
    C = "C16384"
    gen = lambda c: ["P0w1000", f"FT{c}@32", f"D{c}@32", f"Dr{c}@32"]
    hyp = lambda c: [f"W{c}", f"Wp{c}"]
    out = dict(PILOT_NEVER_REUSE_AS_EXAM=True, job=a.job, source=f"job {a.job}, out/full/scores.npz", horizons=HS, n_worlds=an.W,
               labels=meta["labels"], boot=a.boot, policies={b: len(v) for b, v in an.bases.items()})
    skill = lambda b: (lambda L: (L["K"] - L[b]) / (L["K"] - L["O"]))
    out["skill"] = {}
    for b in sorted(an.bases):
        if b in ("K", "O"):
            continue
        out["skill"][b] = {}
        for j, h in enumerate(HS):
            q = an.boot(skill(b), ["K", "O", b], j)
            lo = [an.boot(skill(b), ["K", "O", b], j, np.delete(np.arange(an.W), k), nb=1)["value"] for k in range(an.W)]
            q["leave_one_out_range"] = [float(min(lo)), float(max(lo))]
            q.pop("by_seed_of", None)
            out["skill"][b][str(h)] = q
    out["picks"] = {f"h{h}": {c: dict(G=an.pick(gen(c), j), W=an.pick(hyp(c), j)) for c in "md" if an.has(f"W{c}")} for j, h in enumerate(HS)}

    def sigma_G(j, c="m"):
        def make(ws):
            g = an.pick(gen(c), j, ws)
            return (lambda L: sdiv(L[g] - L[C], L["K"] - L[C])), ["K", C, g], dict(G=g)
        return an.lowo(make, j)

    def recovery(j, c="m", ws=None):
        g, w = an.pick(gen(c), j, ws), an.pick(hyp(c), j, ws)
        q = an.boot(lambda L: sdiv(L[g] - L[w], L[g] - L[C]), [g, w, C], j, ws)
        q.pop("per_world", None) if ws is not None else None
        p = paired(an, g, w, j, ws)
        return dict(G=g, W=w, recovery=q, W_beats_G=p, holds=bool(q["value"] >= REC and (p["t"] or 0) >= TSTAT))

    # T1, T6 (sigma_G at every horizon), T3 at every horizon and leave-one-out at 16
    out["T1"], out["T3"] = {}, {}
    for j, h in enumerate(HS):
        rows = sigma_G(j)
        out["T1"][str(h)] = dict(all=rows[0], leave_one_out=[{k: r[k] for k in ("left_out", "G", "value", "p10", "p90")} for r in rows[1:]],
                                 **verdict(rows))
        out["T1"][str(h)]["verdict"] = {"SURVIVES": "pass", "CLOSED": "fail", "UNDECIDED": "undecided"}[out["T1"][str(h)]["verdict"]]
        out["T3"][str(h)] = recovery(j)
    out["T3"]["16"]["leave_one_out"] = [dict(left_out=meta["labels"][k], **{kk: v for kk, v in recovery(j16, ws=np.delete(np.arange(an.W), k)).items()
                                                                           if kk in ("G", "W", "holds")},
                                             recovery_value=recovery(j16, ws=np.delete(np.arange(an.W), k))["recovery"]["value"])
                                        for k in range(an.W)]
    # T2
    g16 = an.pick(gen("m"), j16)
    gap = an.boot(lambda L: L["P0w1000"] - L[C], ["P0w1000", C], j16)
    rho = an.boot(lambda L: sdiv(L["P0w1000"] - L[g16], L["P0w1000"] - L[C]), ["P0w1000", g16, C], j16)
    rho.pop("per_world", None)
    out["T2"] = dict(G=g16, P0_minus_C=dict(value=gap["value"], se=gap["se"]), read=bool(gap["value"] > 2 * gap["se"]), rho_G=rho,
                     verdict=("not read" if gap["value"] <= 2 * gap["se"] else ("fail" if rho["p10"] > SHARE else ("pass" if rho["p90"] <= SHARE else "undecided"))))
    # T4
    t4 = {}
    if an.has("Wd"):
        for j, h in enumerate(HS):
            wm, wd = an.pick(hyp("m"), j), an.pick(hyp("d"), j)
            gm, gd = an.pick(gen("m"), j), an.pick(gen("d"), j)
            pw, pg = paired(an, wm, wd, j), paired(an, gm, gd, j)
            same = {b: paired(an, f"{b}m" if b in ("W", "Wp") else f"{b}m@32", f"{b}d" if b in ("W", "Wp") else f"{b}d@32", j)
                    for b in ("W", "Wp", "FT", "D", "Dr") if an.has(f"{b}d" if b in ("W", "Wp") else f"{b}d@32")}
            dd = np.array([np.mean([an.Lw["scored"][n][k, j] for n in an.bases[wm]]) - np.mean([an.Lw["scored"][n][k, j] for n in an.bases[wd]])
                           - np.mean([an.Lw["scored"][n][k, j] for n in an.bases[gm]]) + np.mean([an.Lw["scored"][n][k, j] for n in an.bases[gd]])
                           for k in range(an.W)])
            t4[str(h)] = dict(W_mix=wm, W_designed=wd, G_mix=gm, G_designed=gd, gain_W=pw, gain_G=pg,
                              difference=dict(mean=float(dd.mean()), se=float(dd.std(ddof=1) / np.sqrt(len(dd)))), same_policy=same,
                              holds=bool(pw["mean"] > 2 * pw["se"] and pw["mean"] > pg["mean"]))
    out["T4"] = t4
    # T5
    kl, w = meta["klass"], meta["world"]
    t5 = {}
    for j, h in enumerate(HS):
        row = {}
        for nm, m in [("program", kl != "a")] + [(c, kl == c) for c in "abcd"]:
            L = {b: np.array([np.mean([S[n][(w == k) & m, j].mean() for n in an.bases[b]]) for k in range(an.W)]) for b in ("K", "O", "plugU0")}
            f = lambda ix: float((L["plugU0"][ix].mean() - L["O"][ix].mean()) / (L["K"][ix].mean() - L["O"][ix].mean()))
            rng = np.random.default_rng(5)
            bt = np.array([f(rng.integers(0, an.W, an.W)) for _ in range(1000)])
            row[nm] = dict(value=f(np.arange(an.W)), p05=float(np.quantile(bt, 0.05)), p95=float(np.quantile(bt, 0.95)))
        row["verdict"] = "actions matter" if row["program"]["p05"] >= 0.10 else ("observation-only" if row["program"]["p95"] < 0.10 else "undecided")
        t5[str(h)] = row
    out["T5"] = t5
    # T6
    jj = {h: HS.index(h) for h in (8, 32) if h in HS}
    t6_h = {str(h): dict(T1_point=out["T1"][str(h)]["point"] >= BAR, T3_point=out["T3"][str(h)]["holds"]) for h in jj}
    t6_lo = dict(T1_point_min=min(r["value"] for r in out["T1"]["16"]["leave_one_out"]),
                 T3_all=all(r["holds"] for r in out["T3"]["16"]["leave_one_out"]))
    out["T6"] = dict(other_horizons=t6_h, leave_one_out_16=t6_lo,
                     holds=bool(all(v["T1_point"] and v["T3_point"] for v in t6_h.values()) and t6_lo["T1_point_min"] >= BAR and t6_lo["T3_all"]))
    T = dict(T1=out["T1"]["16"]["verdict"], T2=out["T2"]["verdict"], T3=out["T3"]["16"]["holds"], T4=out["T4"].get("16", {}).get("holds"),
             T5=out["T5"]["16"]["verdict"], T6=out["T6"]["holds"])
    if T["T1"] == "fail" or T["T2"] == "fail":
        v = "fail"
    elif T["T1"] == "pass" and T["T2"] in ("pass", "not read") and T["T3"] and T["T4"] and T["T5"] == "actions matter" and T["T6"]:
        v = "pass"
    else:
        v = "undecided"
    out["verdict"] = dict(criteria=T, stage2=v)
    # W diagnostics: W at the truth and at another world, against C
    out["W_pipeline"] = {str(h): dict(Wtrue_minus_C=paired(an, C, "Wtrue", j), Wtrue_skill=out["skill"]["Wtrue"][str(h)]["value"] if an.has("Wtrue") else None)
                         for j, h in enumerate(HS) if an.has("Wtrue")}
    p = os.path.join(a.dir, "w_info.json")
    if os.path.exists(p):
        wi = json.load(open(p))
        out["W_fits"] = {c: dict(z_dist_net_rms_median=float(np.median(v["z_dist_net_rms"])), eval_loss_median=float(np.median(v["eval_loss"])),
                                 prescreen_best_median=float(np.median(np.min(v["prescreen_loss"], 1))))
                         for c, v in wi.items() if isinstance(v, dict) and "z_dist_net_rms" in v}
    for f in ("info",):
        if js.get(f):
            out["job_info"] = {k: js[f].get(k) for k in ("hours", "failed", "skipped", "clock", "speed", "finished")}
    # completeness (review of r6-foundrylong-002/003, minor 3): exit 0 does not mean complete
    inc = []
    info = js.get("info") or {}
    inc += [f"failed: {x}" for x in info.get("failed") or []] + [f"skipped: {x}" for x in info.get("skipped") or []]
    if not info.get("finished"):
        inc.append("info.json: not finished")
    w_steps = (info.get("config") or {}).get("w_steps")
    for c, recs in ((k[1], v) for k, v in (info.get("speed") or {}).items() if k.startswith("w") and k.endswith("_fit")):
        cut = [r["steps"] for r in recs if r["steps"] != w_steps]
        if cut:
            inc.append(f"W{c}: fits cut at steps {cut} (planned {w_steps})")
    for b, n in {"P0w1000": 3, "C16384": 1, "FTm@32": 3, "Dm@32": 3, "Drm@32": 1, "Wm": 2, "Wpm": 1, "FTd@32": 3, "Dd@32": 3, "Drd@32": 1,
                 "Wd": 2, "Wpd": 1, "Wtrue": 1, "plugU0": 1}.items():
        if len(an.bases.get(b, [])) < n:
            inc.append(f"{b}: {len(an.bases.get(b, []))} of {n}")
    out["completeness"] = dict(w_steps=w_steps, incomplete=inc)
    if inc:
        out["verdict"]["stage2"] += " (incomplete: " + "; ".join(inc) + ")"
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w") as f:
        json.dump(out, f, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print(json.dumps(out["verdict"], indent=1))
    for h in HS:
        print(h, "sigma_G", round(out["T1"][str(h)]["point"], 3), [round(out["T1"][str(h)][k], 3) for k in ("lower_bound_min_over_leave_one_out", "upper_bound_max_over_leave_one_out")],
              "recovery", round(out["T3"][str(h)]["recovery"]["value"], 3), "t", out["T3"][str(h)]["W_beats_G"]["t"])
    print("wrote", a.out)


if __name__ == "__main__":
    main()
