"""make_summary -- study foundrylong, stage 1: job outputs -> results/analysis_stage1.json (CPU, seconds).

    python -B make_summary.py DIR --job r6-foundrylong-001 [--out results/analysis_stage1.json] [--boot 4000]

DIR = a copy of origin/gpu-jobs:jobs/<job>/out/full. Everything is recomputed from the per-item scores
(scores.npz: S__<policy>__s<seed> (items, 3 horizons)) by the rules of DECLARED.md:
  halves     items with an even index are scored, odd ones are the unscored half used for every pick
  L          mean fair energy score at one query over the scored items of the worlds of the analysis set, seed mean
  sigma      (L(null) - L(C)) / (L(K) - L(C)); null = the candidate among P0(largest), FT(N), D(N), Dr(N) with the lowest
             pooled loss at that horizon on the unscored half; C = the C(n) with the lowest such loss
  bounds     worlds resampled as clusters, one training seed drawn per trained policy in each resample; the one-sided
             90% lower bound is the 10th percentile, the upper bound the 90th; all worlds and each world left out
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
BAR = 0.15


def load(d):
    z = np.load(os.path.join(d, "scores.npz"))
    names = [str(n) for n in z["names"]]
    S = {n: np.asarray(z["S__" + n.replace("|", "__").replace("@", "_at_")], float) for n in names}
    meta = dict(world=z["world"].astype(int), item=z["item"].astype(int), klass=np.array([str(k) for k in z["klass"]]),
                horizons=[int(h) for h in z["horizons"]], labels=[str(x) for x in z["labels"]])
    js = {}
    for f in ("info", "train_info", "screen", "gate", "worlds"):
        p = os.path.join(d, f + ".json")
        js[f] = json.load(open(p)) if os.path.exists(p) else None
    return S, meta, js


class A:
    """World means of every scored column on each half: Lw[half][name] (n_worlds, NH)."""

    def __init__(self, S, meta, nb, seed=0):
        self.meta, self.nb = meta, nb
        self.W = len(meta["labels"])
        self.HS = meta["horizons"]
        self.bases = {}
        for n in S:
            self.bases.setdefault(n.split("|")[0], []).append(n)
        for b in self.bases:
            self.bases[b].sort()
        w, it = meta["world"], meta["item"]
        halves = {"scored": it % 2 == 0, "unscored": it % 2 == 1, "all": np.ones(len(it), bool)}
        self.Lw = {hf: {n: np.stack([v[(w == j) & m].mean(0) for j in range(self.W)]) for n, v in S.items()}
                   for hf, m in halves.items()}
        self.S, self.rng = S, np.random.default_rng(seed)

    def has(self, b):
        return b in self.bases

    def L(self, b, j, ws=None, half="scored"):
        """Seed-mean pooled loss of base b at horizon index j over worlds ws."""
        ws = np.arange(self.W) if ws is None else ws
        return float(np.mean([self.Lw[half][n][ws, j].mean() for n in self.bases[b]]))

    def pick(self, cands, j, ws=None):
        cands = [c for c in cands if self.has(c)]
        return min(cands, key=lambda c: self.L(c, j, ws, "unscored"))

    def boot(self, fn, bases, j, ws=None, half="scored", nb=None):
        """fn(dict base -> L) -> float. Point (seed mean), resamples (worlds as clusters, a seed per base), per world."""
        ws = np.arange(self.W) if ws is None else np.asarray(ws)
        nb = self.nb if nb is None else nb
        Lw = self.Lw[half]
        arr = {b: np.stack([Lw[n][ws, j] for n in self.bases[b]]) for b in bases}        # (seeds, n_ws)
        point = fn({b: float(arr[b].mean()) for b in bases})
        rng = np.random.default_rng([17, j, len(ws), int(ws.sum())])
        iw = rng.integers(0, len(ws), size=(nb, len(ws)))
        vals = np.empty(nb)
        sd = {b: rng.integers(0, arr[b].shape[0], size=nb) for b in bases}
        for i in range(nb):
            vals[i] = fn({b: float(arr[b][sd[b][i], iw[i]].mean()) for b in bases})
        per = []
        for k in range(len(ws)):
            try:
                per.append(float(fn({b: float(arr[b][:, k].mean()) for b in bases})))
            except ZeroDivisionError:
                per.append(float("nan"))
        ok = np.isfinite(vals)
        q = lambda p: float(np.quantile(vals[ok], p))
        by_seed = {b: [float(fn({bb: float(arr[bb][s].mean()) if bb == b else float(arr[bb].mean()) for bb in bases}))
                       for s in range(arr[b].shape[0])] for b in bases if arr[b].shape[0] > 1}
        return dict(value=float(point), se=float(vals[ok].std(ddof=1)), p05=q(0.05), p10=q(0.10), p90=q(0.90), p95=q(0.95),
                    per_world=per, median_world=float(np.nanmedian(per)), by_seed_of=by_seed, n_worlds=int(len(ws)))

    def lowo(self, make, j):
        """make(ws) -> (fn, bases[, extra]); the quantity with all worlds and with each world left out."""
        out = []
        for k in [None] + list(range(self.W)):
            ws = np.arange(self.W) if k is None else np.delete(np.arange(self.W), k)
            fn, bases, extra = make(ws)
            q = self.boot(fn, bases, j, ws)
            q.pop("per_world") if k is not None else None
            q.pop("by_seed_of", None) if k is not None else None
            out.append(dict(left_out=None if k is None else self.meta["labels"][k], **extra, **q))
        return out


def verdict(rows):
    lo = min(r["p10"] for r in rows)
    hi = max(r["p90"] for r in rows)
    v = "SURVIVES" if lo >= BAR else ("CLOSED" if hi < BAR else "UNDECIDED")
    return dict(verdict=v, lower_bound_all=rows[0]["p10"], upper_bound_all=rows[0]["p90"], lower_bound_min_over_leave_one_out=lo,
                upper_bound_max_over_leave_one_out=hi, point=rows[0]["value"],
                point_range_leave_one_out=[min(r["value"] for r in rows[1:]), max(r["value"] for r in rows[1:])])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--job", required=True)
    ap.add_argument("--out", default=os.path.join(HERE, "results", "analysis_stage1.json"))
    ap.add_argument("--boot", type=int, default=4000)
    a = ap.parse_args()
    S, meta, js = load(a.dir)
    an = A(S, meta, a.boot)
    HS = an.HS
    p0s = sorted(int(b[3:]) for b in an.bases if b.startswith("P0w"))
    cs = sorted(int(b[1:]) for b in an.bases if b[0] == "C" and b[1:].isdigit())
    Ns = sorted(int(b[3:]) for b in an.bases if b.startswith("FT@"))
    P0 = f"P0w{p0s[-1]}"
    src = f"job {a.job}, out/full/scores.npz"
    out = dict(PILOT_NEVER_REUSE_AS_EXAM=True, job=a.job, source=src, horizons=HS, n_worlds=an.W, labels=meta["labels"],
               n_items_per_world=int((meta["world"] == 0).sum()), scored_items_per_world=int(((meta["world"] == 0) & (meta["item"] % 2 == 0)).sum()),
               boot=a.boot, policies={b: len(v) for b, v in an.bases.items()}, p0_worlds=p0s, c_episodes=cs, lab_budgets=Ns)
    skill = lambda b: (lambda L: (L["K"] - L[b]) / (L["K"] - L["O"]))

    # ---- skills (K = 0, O = 1) per policy and horizon
    out["skill"] = {}
    for b in sorted(an.bases):
        if b in ("K", "O"):
            continue
        out["skill"][b] = {}
        for j, h in enumerate(HS):
            q = an.boot(skill(b), ["K", "O", b], j)
            lo = [an.boot(skill(b), ["K", "O", b], j, np.delete(np.arange(an.W), k), nb=1)["value"] for k in range(an.W)]
            q["leave_one_out_range"] = [float(min(lo)), float(max(lo))]
            out["skill"][b][str(h)] = q

    # ---- sigma by cell, with the picks
    def sigma_make(j, N):
        def make(ws):
            C = an.pick([f"C{n}" for n in cs], j, ws)
            cands = [P0] + ([f"FT@{N}", f"D@{N}", f"Dr@{N}"] if N else [])
            null = an.pick(cands, j, ws)
            fn = lambda L: (L[null] - L[C]) / (L["K"] - L[C])
            return fn, ["K", C, null], dict(null=null, C=C)
        return make
    out["sigma"] = {}
    for j, h in enumerate(HS):
        for N in [0] + Ns:
            rows = an.lowo(sigma_make(j, N), j)
            cell = dict(horizon=h, lab_episodes=N, all=rows[0], leave_one_out=rows[1:], **verdict(rows))
            cell["null_all"], cell["C_all"] = rows[0]["null"], rows[0]["C"]
            cell["nulls_leave_one_out"] = sorted({r["null"] for r in rows[1:]})
            # every candidate's share against the same C (scored half)
            C = rows[0]["C"]
            cell["candidate_share"] = {c: an.boot(lambda L, c=c: (L[c] - L[C]) / (L["K"] - L[C]), ["K", C, c], j)
                                       for c in [P0] + ([f"FT@{N}", f"D@{N}", f"Dr@{N}"] if N else []) if an.has(c)}
            for c in cell["candidate_share"].values():
                c.pop("per_world")
            cell["unscored_half_L"] = {c: an.L(c, j, None, "unscored") for c in [P0] + ([f"FT@{N}", f"D@{N}", f"Dr@{N}"] if N else []) if an.has(c)}
            out["sigma"][f"h{h}_N{N}"] = cell

    # ---- S1 and S1a at 16 ticks, the largest Lab budget
    j16 = HS.index(16) if 16 in HS else len(HS) // 2
    Nd = 32 if 32 in Ns else Ns[-1]
    s1 = out["sigma"][f"h{HS[j16]}_N{Nd}"]
    C = s1["C_all"]
    den = lambda L: L["K"] - L[C]
    S1 = dict(cell=f"{HS[j16]} ticks, {Nd} Lab episodes", bar=BAR, **{k: s1[k] for k in (
        "verdict", "point", "lower_bound_all", "upper_bound_all", "lower_bound_min_over_leave_one_out",
        "upper_bound_max_over_leave_one_out", "point_range_leave_one_out", "null_all", "C_all", "nulls_leave_one_out")},
        median_world=s1["all"]["median_world"], se=s1["all"]["se"], per_world=s1["all"]["per_world"])
    rob = {}
    if len(p0s) > 1:
        rob["gain_last_step_prior_worlds"] = an.boot(lambda L: (L[f"P0w{p0s[-2]}"] - L[P0]) / den(L), ["K", C, P0, f"P0w{p0s[-2]}"], j16)
    if an.has("P0x2"):
        s0 = an.bases[P0][0]
        Lk, Lc = an.L("K", j16), an.L(C, j16)
        rob["gain_double_schedule_seed0"] = float((an.Lw["scored"][s0][:, j16].mean() - an.L("P0x2", j16)) / (Lk - Lc))
    if len(cs) > 1:
        Cb, Cm = f"C{cs[-1]}", f"C{cs[-2]}"
        rob["gain_reference_last_data_step"] = an.boot(lambda L: (L[Cm] - L[Cb]) / (L["K"] - L[Cb]), ["K", Cb, Cm], j16)
    shift_null = (rob.get("gain_last_step_prior_worlds", {}).get("value", 0.0) + max(rob.get("gain_double_schedule_seed0", 0.0) or 0.0, 0.0))
    shift_c = rob.get("gain_reference_last_data_step", {}).get("value", 0.0)
    rob["lower_bound_after_one_more_step_of_the_null"] = S1["lower_bound_min_over_leave_one_out"] - shift_null
    rob["upper_bound_after_one_more_step_of_C"] = S1["upper_bound_max_over_leave_one_out"] + shift_c
    rob["reading"] = ("robust" if (S1["verdict"] == "SURVIVES" and rob["lower_bound_after_one_more_step_of_the_null"] >= BAR)
                      or (S1["verdict"] == "CLOSED" and rob["upper_bound_after_one_more_step_of_C"] < BAR)
                      else ("at this compute" if S1["verdict"] != "UNDECIDED" else "undecided"))
    S1["S1a"] = rob
    S1["stage2_runs"] = bool(S1["verdict"] == "SURVIVES" or (S1["verdict"] == "UNDECIDED" and S1["point"] >= BAR))
    out["S1"] = S1

    # ---- S3: the trend in prior worlds
    out["S3"] = {}
    for j, h in enumerate(HS):
        Cj = an.pick([f"C{n}" for n in cs], j)
        row = dict(C=Cj, s0={str(w): an.boot(lambda L, w=w: (L[f"P0w{w}"] - L[Cj]) / (L["K"] - L[Cj]), ["K", Cj, f"P0w{w}"], j) for w in p0s},
                   skill={str(w): out["skill"][f"P0w{w}"][str(h)]["value"] for w in p0s}, steps=[])
        for w0, w1 in zip(p0s[:-1], p0s[1:]):
            q = an.boot(lambda L: (L[f"P0w{w0}"] - L[f"P0w{w1}"]) / (L["K"] - L[Cj]), ["K", Cj, f"P0w{w0}", f"P0w{w1}"], j)
            q.pop("per_world")
            q["z"] = q["value"] / q["se"] if q["se"] > 0 else None
            q["reading"] = ("still falling" if q["value"] > 2 * q["se"] else ("flat" if (q["p05"] > -0.02 and q["p95"] < 0.02) else "neither"))
            row["steps"].append(dict(frm=w0, to=w1, fall_of_s0=q))
        for v in row["s0"].values():
            v.pop("per_world")
        if an.has("P0x2"):
            s0n = an.bases[P0][0]
            row["double_schedule_seed0_fall_of_s0"] = float((an.Lw["scored"][s0n][:, j].mean() - an.L("P0x2", j)) / (an.L("K", j) - an.L(Cj, j)))
        out["S3"][str(h)] = row

    # ---- S4: the reference's data curve
    out["S4"] = {}
    for j, h in enumerate(HS):
        row = dict(skill={str(n): out["skill"][f"C{n}"][str(h)]["value"] for n in cs}, steps=[])
        for n0, n1 in zip(cs[:-1], cs[1:]):
            q = an.boot(lambda L: (L[f"C{n0}"] - L[f"C{n1}"]) / (L["K"] - L["O"]), ["K", "O", f"C{n0}", f"C{n1}"], j)
            q.pop("per_world")
            row["steps"].append(dict(frm=n0, to=n1, gain_of_skill=q))
        row["verdict"] = ("not converged in data (the last step gains more than 0.01 of skill): C is a lower bound"
                          if row["steps"] and row["steps"][-1]["gain_of_skill"]["value"] > 0.01 else "the last step gains at most 0.01 of skill")
        out["S4"][str(h)] = row

    # ---- S5: actions (all items with a program)
    out["S5"] = {}
    kl, w = meta["klass"], meta["world"]
    if an.has("plugU0"):
        for j, h in enumerate(HS):
            row = {}
            for nm, m in [("program", kl != "a")] + [(c, kl == c) for c in "abcd"]:
                L = {b: np.array([np.mean([S[n][(w == k) & m, j].mean() for n in an.bases[b]]) for k in range(an.W)]) for b in ("K", "O", "plugU0")}
                f = lambda ix: float((L["plugU0"][ix].mean() - L["O"][ix].mean()) / (L["K"][ix].mean() - L["O"][ix].mean()))
                rng = np.random.default_rng(5)
                bt = np.array([f(rng.integers(0, an.W, an.W)) for _ in range(1000)])
                per = (L["plugU0"] - L["O"]) / (L["K"] - L["O"])
                row[nm] = dict(value=f(np.arange(an.W)), p05=float(np.quantile(bt, 0.05)), p95=float(np.quantile(bt, 0.95)),
                               worlds_at_0p10_or_more=int((per >= 0.10).sum()))
            row["verdict"] = "actions matter" if row["program"]["p05"] >= 0.10 else ("observation-only" if row["program"]["p95"] < 0.10 else "undecided")
            out["S5"][str(h)] = row

    # ---- S2: the training rule, from train_info.json
    ti = js["train_info"] or {}
    fam = {}
    for k, v in ti.items():
        if not isinstance(v, dict):
            continue
        f = k.split("|")[0]
        e = fam.setdefault(f, dict(nets=0, trained=np.zeros(len(HS), int), best_step=[], late_gain=[], steps=v.get("steps") or v.get("s_max"),
                                   ms_per_step=[], stopped_early=[]))
        if "cv_mean" in v:                                              # FT: chosen step below s_max
            tr = np.asarray(v["trained"], bool)
            e["nets"] += tr.shape[0]
            e["trained"] += tr.sum(0)
            e["best_step"] += np.asarray(v["step"]).tolist()
            e.setdefault("lr", []).extend(np.asarray(v["lr"]).tolist())
        else:
            tr = np.asarray(v["trained"], bool)
            e["nets"] += tr.shape[0]
            e["trained"] += tr.sum(0)
            e["best_step"] += np.asarray(v["best_step"]).tolist()
            e["late_gain"] += np.asarray(v["late_gain"]).tolist()
            e["ms_per_step"].append(v.get("ms_per_step"))
            if v.get("stopped_early"):
                e["stopped_early"].append(v["stopped_early"])
    out["S2"] = {}
    for f, e in fam.items():
        bs = np.asarray(e["best_step"], float).reshape(-1, len(HS))
        row = dict(nets=int(e["nets"]), schedule_steps=e["steps"], trained_by_horizon={str(h): int(e["trained"][j]) for j, h in enumerate(HS)},
                   best_step_median_by_horizon={str(h): float(np.median(bs[:, j])) for j, h in enumerate(HS)},
                   best_step_max_by_horizon={str(h): float(bs[:, j].max()) for j, h in enumerate(HS)},
                   stopped_early=e["stopped_early"], ms_per_step=[m for m in e["ms_per_step"] if m])
        if e["late_gain"]:
            lg = np.asarray(e["late_gain"], float).reshape(-1, len(HS))
            row["late_gain_max_by_horizon"] = {str(h): float(lg[:, j].max()) for j, h in enumerate(HS)}
            row["late_gain_median_by_horizon"] = {str(h): float(np.median(lg[:, j])) for j, h in enumerate(HS)}
        if "lr" in e:
            lr = np.asarray(e["lr"], float).reshape(-1, len(HS))
            row["chosen_rate_counts_by_horizon"] = {str(h): {str(x): int((lr[:, j] == x).sum()) for x in np.unique(lr)} for j, h in enumerate(HS)}
            row["chosen_step_counts_by_horizon"] = {str(h): {str(int(x)): int((bs[:, j] == x).sum()) for x in np.unique(bs)} for j, h in enumerate(HS)}
        out["S2"][f] = row

    # ---- the job itself
    info = js["info"] or {}
    out["job_info"] = dict(hours=info.get("hours"), failed=info.get("failed"), skipped=info.get("skipped"), finished=info.get("finished"),
                           member_ticks_runner=info.get("member_ticks_runner"), speed=info.get("speed"), clock=info.get("clock"),
                           n_train_worlds=info.get("n_train_worlds"), n_new_ok=info.get("n_new_ok"), n_candidates=info.get("n_candidates"),
                           platform=info.get("platform"),
                           screen=None if not js["screen"] else {k: js["screen"].get(k) for k in ("n_draws", "n_candidates", "speed", "gates")},
                           gate=None if not js["gate"] else {k: js["gate"].get(k) for k in ("n", "n_ok")})
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w") as f:
        json.dump(out, f, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    v = out["S1"]
    print(f"S1 at {v['cell']}: sigma {v['point']:.3f}, lower bound {v['lower_bound_all']:.3f} (min leave-one-out "
          f"{v['lower_bound_min_over_leave_one_out']:.3f}), upper bound {v['upper_bound_all']:.3f} (max {v['upper_bound_max_over_leave_one_out']:.3f}) "
          f"-> {v['verdict']} ({v['S1a']['reading']}); null {v['null_all']}, C {v['C_all']}; stage 2 runs: {v['stage2_runs']}")
    for h in HS:
        print(f"  {h:2d} ticks: skill " + ", ".join(f"{b} {out['skill'][b][str(h)]['value']:.3f}" for b in sorted(out["skill"])))
    print("wrote", a.out)


if __name__ == "__main__":
    main()
