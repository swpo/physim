"""make_summary -- study foundryexam: results/analysis.json from a job's outputs (CPU, about a minute).

    python -B make_summary.py JOB_OUT/full --job r6-foundryexam-001 [--status status.json] [--out results]

Reads per arm scores.npz (fair energy score per item and cell of every policy), meta.json, worlds.json and
train_info.json, and the job's gate.json and info.json. Everything is recomputed here from the per-item
scores; the job's own quick report is not used. Error bars: hidden worlds are resampled as clusters and, in
the same resample, one training seed is drawn for every policy that has several (DESIGN.md criterion 1 and
8), so every interval of a quantity that involves a trained net carries the seed-to-seed variance of the
seed-mean it is quoted for. Shares follow round5/agentenv/evaluator/acceptance.py (pooled energy score over
the valid cells; sigma, rho; no clipping).
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
VW1 = os.path.abspath(os.path.join(HERE, "..", "..", "..", "vw1"))
sys.path.insert(0, VW1)
from vw.scoring import cells_ok, public_report, skill_report  # noqa: E402

NB = 4000
BUDGETS = (8, 32, 128, 512)
S_BUDGETS = (0, 2, 8, 32, 128, 512)


def load_arm(d, arm):
    z = np.load(os.path.join(d, arm, "scores.npz"))
    names = [str(n) for n in z["names"]]
    S = {n: z["S__" + n.replace("|", "__").replace("@", "_at_")] for n in names}
    meta = json.load(open(os.path.join(d, arm, "meta.json")))
    worlds = json.load(open(os.path.join(d, arm, "worlds.json")))
    info = json.load(open(os.path.join(d, arm, "train_info.json")))
    return S, z["world"], np.array([str(k) for k in z["klass"]]), z["group"], meta, worlds, info


def by_base(S):
    out = {}
    for k in sorted(S):
        out.setdefault(k.split("|")[0], []).append(k)
    return out


class Arm:
    def __init__(self, S, world, klass):
        self.S, self.world, self.klass = S, np.asarray(world), klass
        self.bases = by_base(S)
        self.valid = cells_ok(S["K"], S["O"])
        if not self.valid.any():
            self.valid = np.ones(S["K"].shape[1], bool)
        self.L = {k: v[:, self.valid].sum(1) for k, v in S.items()}             # per item, pooled over valid cells
        self.ids = sorted(set(self.world.tolist()))
        self.rows = [np.flatnonzero(self.world == w) for w in self.ids]
        rng = np.random.default_rng(0)
        nW = len(self.ids)
        self.boot_w = rng.integers(0, nW, size=(NB, nW))
        self.boot_seed = {b: rng.integers(0, len(ks), size=NB) for b, ks in self.bases.items()}
        # per world mean of every scored column: (n_worlds,) so that a resample is a mean of world means
        self.Lw = {k: np.array([v[r].mean() for r in self.rows]) for k, v in self.L.items()}

    def Lmean(self, base, rows=None):
        """Seed-mean pooled score (optionally over a subset of items)."""
        v = np.mean([self.L[k] for k in self.bases[base]], 0)
        return float(v.mean() if rows is None else v[rows].mean())

    def quantity(self, fn, bases, sel=None):
        """fn(L: dict base -> float) -> float. Point (seed-mean, all worlds), world-cluster + seed bootstrap,
        per-world values, per-seed-0/1 values. sel: optional boolean item mask (e.g. a program class)."""
        if sel is None:
            Lw = self.Lw
        else:
            Lw = {k: np.array([self.L[k][r[sel[r]]].mean() if sel[r].any() else np.nan for r in self.rows])
                  for b in bases for k in self.bases[b]}
        smean = {b: np.mean([Lw[k] for k in self.bases[b]], 0) for b in bases}    # (n_worlds,)
        point = fn({b: float(np.nanmean(smean[b])) for b in bases})
        bt = np.empty(NB)
        for i in range(NB):
            w = self.boot_w[i]
            bt[i] = fn({b: float(np.nanmean(Lw[self.bases[b][self.boot_seed[b][i]]][w])) for b in bases})
        bw = np.array([fn({b: float(np.nanmean(smean[b][self.boot_w[i]])) for b in bases}) for i in range(0, NB, 4)])
        per = []
        for j in range(len(self.ids)):
            try:
                per.append(float(fn({b: float(smean[b][j]) for b in bases})))
            except ZeroDivisionError:
                per.append(float("nan"))
        seeds = {}
        for b in bases:
            if len(self.bases[b]) > 1:
                vals = []
                for k in self.bases[b]:
                    Ls = {bb: float(np.nanmean(smean[bb])) for bb in bases}
                    Ls[b] = float(np.nanmean(Lw[k]))
                    vals.append(float(fn(Ls)))
                seeds[b] = vals
        ok = np.isfinite(bt)
        per_a = np.array(per, float)
        return dict(value=float(point), se=float(bt[ok].std(ddof=1)), p05=float(np.quantile(bt[ok], 0.05)),
                    p95=float(np.quantile(bt[ok], 0.95)), se_worlds_only=float(bw[np.isfinite(bw)].std(ddof=1)),
                    per_world=per, median_world=float(np.nanmedian(per_a)), by_seed_of=seeds, n_worlds=len(self.ids))


def oes_fn(b):
    return lambda L: (L["K"] - L[b]) / (L["K"] - L["O"])


def vsc_fn(b):
    return lambda L: (L["K"] - L[b]) / (L["K"] - L["C"])


def interp_budget(Ns, vals, target):
    """Smallest N (linear in log2 N) at which vals reaches target (vals: skill, higher is better)."""
    Ns, vals = np.asarray(Ns, float), np.asarray(vals, float)
    if vals[0] >= target:
        return f"at most {int(Ns[0])}"
    for i in range(1, len(Ns)):
        if vals[i] >= target:
            f = (target - vals[i - 1]) / (vals[i] - vals[i - 1])
            return float(2 ** (np.log2(Ns[i - 1]) + f * (np.log2(Ns[i]) - np.log2(Ns[i - 1]))))
    return f"more than {int(Ns[-1])}"


def verdict_interval(q, bar, above=True):
    lo, hi = q["p05"], q["p95"]
    if above:
        return "pass" if lo >= bar else ("fail" if hi < bar else "undecided")
    return "pass" if hi <= bar else ("fail" if lo > bar else "undecided")


def analyse_arm(d, arm):
    S, world, klass, group, meta, worlds, info = load_arm(d, arm)
    # the ceiling C is the better (lower pooled score over the arm) of the net trained from scratch and P0 fine-tuned
    # on the same true-weight simulations (DESIGN.md section 4); the other is kept as Cscratch or Cft
    ceiling = "scratch"
    if any(k.startswith("Cft|") for k in S):
        A0 = Arm(S, world, klass)
        if A0.Lmean("Cft") < A0.Lmean("C"):
            ceiling = "fine-tuned P0"
            S = {(k.replace("C|", "Cscratch|", 1) if k.startswith("C|") else k): v for k, v in S.items()}
            S = {(k.replace("Cft|", "C|", 1) if k.startswith("Cft|") else k): v for k, v in S.items()}
    A = Arm(S, world, klass)
    B = A.bases
    out = dict(arm=arm, eps=meta.get("eps"), n_hidden=meta["n_hidden"], n_items=int(len(world)), cells=meta["cells"],
               valid_cells=A.valid.tolist(), hidden_labels=meta["hidden_labels"], groups=meta["groups"],
               group_of_world=meta["group_of_world"], policies={b: len(k) for b, k in B.items()}, ceiling_is=ceiling)
    # ---- skill table
    tab = {}
    for b in B:
        if b in ("K",):
            continue
        need = ["K", "O", b]
        q = A.quantity(oes_fn(b), need)
        row = dict(L=A.Lmean(b), oes_pooled=q)
        if "C" in B and b != "C":
            row["share_of_C"] = A.quantity(vsc_fn(b), ["K", "C", b])
        tab[b] = row
    out["L_K"], out["L_O"] = A.Lmean("K"), A.Lmean("O")
    out["table"] = tab
    # per-cell OES (equal-weight mean over cells), seed-mean scores, by program class
    M = {b: np.mean([S[k] for k in ks], 0) for b, ks in B.items()}
    R = skill_report({"climatology": M["K"], "oracle": M["O"], **{b: M[b] for b in B if b not in ("K", "O")}},
                     valid=A.valid, n_boot=200, groups=klass)
    R = public_report(R)
    out["oes_cellmean"] = {b: R["aggregate"][b] for b in R["aggregate"]}
    out["oes_by_cell"] = {b: R["oes"][b] for b in R["oes"]}
    out["oes_by_class"] = R.get("by_group")
    # ---- acceptance
    Nmax = max(n for n in BUDGETS if f"D@{n}" in B)
    cand = [b for b in (f"D@{Nmax}", f"FT@{Nmax}", f"Dr@{Nmax}", "P0", "S@0") if b in B]
    noexp = [b for b in ("P0", "S@0", "P0s") if b in B]

    def sigma(L):
        return (min(L[b] for b in cand) - L["C"]) / (L["K"] - L["C"])

    def sigma_at(N):
        cc = [b for b in (f"D@{N}", f"FT@{N}", f"Dr@{N}", "P0", "S@0") if b in B]
        return cc, (lambda L: (min(L[b] for b in cc) - L["C"]) / (L["K"] - L["C"]))

    def share_noexp(L):
        return (L["K"] - min(L[b] for b in noexp)) / (L["K"] - L["C"])
    acc = dict(null_candidates=cand, no_experiment_policies=noexp)
    acc["sigma"] = A.quantity(sigma, ["K", "C"] + cand)
    Lp = {b: A.Lmean(b) for b in cand}
    acc["null_is"] = min(Lp, key=Lp.get)
    acc["sigma_verdict"] = verdict_interval(acc["sigma"], 0.15, True)
    acc["sigma_by_budget"] = {}
    for N in BUDGETS:
        cc, f = sigma_at(N)
        if len(cc) > 2:
            acc["sigma_by_budget"][str(N)] = A.quantity(f, ["K", "C"] + cc)
    acc["sigma_no_lab"] = A.quantity(lambda L: (min(L[b] for b in noexp) - L["C"]) / (L["K"] - L["C"]), ["K", "C"] + noexp)
    acc["share_noexp"] = A.quantity(share_noexp, ["K", "C"] + noexp)
    v = acc["share_noexp"]
    acc["trivial_verdict"] = ("trivially easy for the recipe" if v["p05"] >= 0.95 else
                              "not trivially easy for the recipe" if v["p95"] <= 0.85 else "undecided")
    acc["rho"] = {}
    for N in S_BUDGETS:
        if f"S@{N}" in B:
            acc["rho"][str(N)] = A.quantity(lambda L, N=N: (L["P0"] - L[f"S@{N}"]) / (L["P0"] - L["C"]), ["P0", "C", f"S@{N}"])
    if acc["rho"]:
        last = acc["rho"][str(max(int(k) for k in acc["rho"]))]
        acc["rho_verdict_at_largest_budget"] = verdict_interval(last, 0.7, False)
    for N in BUDGETS:
        if f"FT@{N}" in B:
            acc.setdefault("rho_finetune", {})[str(N)] = A.quantity(
                lambda L, N=N: (L["P0"] - L[f"FT@{N}"]) / (L["P0"] - L["C"]), ["P0", "C", f"FT@{N}"])
    out["acceptance"] = acc
    # ---- gaps in OES units (pooled), with intervals
    gaps = {}
    pairs = [("C", "P0"), ("C", "P0s"), ("P0", "P0s"), ("O", "C"), ("C", "S@0"), ("C", "Cscratch"), ("C", "Cft")] + [("C", f"S@{N}") for N in S_BUDGETS[1:]] \
        + [(f"S@{N}", "P0") for N in S_BUDGETS[1:]] + [(f"FT@{N}", "P0") for N in BUDGETS] + [("C", f"D@{N}") for N in BUDGETS] \
        + [("P0", f"P0w{n}") for n in (16, 64)] + [("S@0", "P0")]
    for a, b in pairs:
        if a in B and b in B:
            gaps[f"{a} - {b}"] = A.quantity(lambda L, a=a, b=b: (L[b] - L[a]) / (L["K"] - L["O"]), ["K", "O", a, b])
            g = gaps[f"{a} - {b}"]
            g["z"] = g["value"] / g["se"] if g["se"] > 0 else None
    out["gaps_oes"] = gaps
    # ---- state-given gap (round 5's screen)
    sg = {}
    for b in ("plugPrior", "plug03", "plug10", "plug30", "plugTrue", "plugU0"):
        if b in B:
            sg[b] = A.quantity(lambda L, b=b: 1.0 - (L["K"] - L[b]) / (L["K"] - L["O"]), ["K", "O", b])
    out["state_given_loss"] = sg
    # ---- actions matter
    act = {}
    if "plugU0" in B and "plugTrue" in B:
        f = lambda L: (L["plugU0"] - L["plugTrue"]) / (L["K"] - L["O"])
        sel = np.isin(klass, ["b", "c", "d"])
        act["classes_bcd"] = A.quantity(f, ["K", "O", "plugU0", "plugTrue"], sel=sel)
        for c in "abcd":
            act[f"class_{c}"] = A.quantity(f, ["K", "O", "plugU0", "plugTrue"], sel=(klass == c))
        act["verdict"] = ("actions matter" if act["classes_bcd"]["p05"] >= 0.10 else
                          "observation-only" if act["classes_bcd"]["p95"] < 0.10 else "undecided")
        act["worlds_at_least_0p10"] = int(np.sum(np.array(act["classes_bcd"]["per_world"]) >= 0.10))
        # what the best trained predictor could gain: the input-blind loss in units of C's own error above the oracle
        if "C" in B:
            act["blind_loss_over_C_excess"] = A.quantity(lambda L: (L["plugU0"] - L["plugTrue"]) / (L["C"] - L["O"]),
                                                         ["C", "O", "plugU0", "plugTrue"], sel=sel)
    out["actions"] = act
    # ---- budgets
    bud = {}
    curves = {}
    for fam in ("D", "Dr", "FT", "S"):
        Ns = [n for n in (S_BUDGETS if fam == "S" else BUDGETS) if f"{fam}@{n}" in B]
        if Ns:
            curves[fam] = dict(N=Ns, share_of_C=[(A.Lmean("K") - A.Lmean(f"{fam}@{n}")) / (A.Lmean("K") - A.Lmean("C")) for n in Ns],
                               oes_pooled=[(A.Lmean("K") - A.Lmean(f"{fam}@{n}")) / (A.Lmean("K") - A.Lmean("O")) for n in Ns])
    bud["curves"] = curves
    Ns = [n for n in BUDGETS if f"D@{n}" in B and f"Dr@{n}" in B]
    if Ns:
        best = [max((A.Lmean("K") - min(A.Lmean(f"D@{n}"), A.Lmean(f"Dr@{n}"))) / (A.Lmean("K") - A.Lmean("C")), -9.0) for n in Ns]
        p0 = (A.Lmean("K") - A.Lmean("P0")) / (A.Lmean("K") - A.Lmean("C"))
        bud["data_only_best_share_of_C"] = dict(N=Ns, value=best)
        bud["N90_data_only"] = interp_budget(Ns, best, 0.9)
        bud["N_P0_data_only"] = interp_budget(Ns, best, p0)
        bud["P0_share_of_C"] = p0
        if "FT" in curves:
            bud["N90_finetune"] = interp_budget(curves["FT"]["N"], curves["FT"]["share_of_C"], 0.9)
    out["budgets"] = bud
    # ---- convergence, stationarity, seeds
    conv = {}
    for k, v in info.items():
        if not isinstance(v, dict) or "converged" not in v:
            continue
        c = v["converged"]
        fam = k.split("|")[0]
        e = conv.setdefault(fam, dict(nets=0, ok=0, late_share_max=0.0, steps=v["steps"], stopped_early=0, best_step_median=[]))
        if c is not None:
            e["nets"] += len(c["ok"])
            e["ok"] += int(sum(c["ok"]))
            e["late_share_max"] = max(e["late_share_max"], float(max(c["late_share"])))
        e["stopped_early"] += int(bool(v.get("stopped_early")))
        e["best_step_median"] += list(v["best_step"])
    for e in conv.values():
        e["best_step_median"] = float(np.median(e["best_step_median"])) if e["best_step_median"] else None
    out["convergence"] = conv
    curves_t = {}
    for k, v in info.items():
        if isinstance(v, dict) and "hist" in v and k.split("|")[0].split()[-1] in ("P0", "A", "P0s", "C") or \
                (isinstance(v, dict) and "hist" in v and (" C|" in k or k.startswith(("P0|", "A|", "P0s|")))):
            curves_t[k] = dict(step=[h["step"] for h in v["hist"]], val_mean=[float(np.mean(h["val"])) for h in v["hist"]],
                               train=[h["train"] for h in v["hist"]])
    out["training_curves"] = curves_t
    ts = [h["tick_share"] for h in worlds["hidden"]]
    out["stationarity"] = dict(first17_max=float(max(t["first17"] for t in ts)), all33_max=float(max(t["all33"] for t in ts)),
                               first17_median=float(np.median([t["first17"] for t in ts])),
                               all33_median=float(np.median([t["all33"] for t in ts])),
                               sampling_floor=ts[0]["sampling_floor"],
                               verdict="stationary" if max(t["all33"] for t in ts) <= 0.01 else "not stationary in at least one world")
    out["lab_nats"] = dict(mean=float(np.mean([h["lab"]["mean"] for h in worlds["hidden"]])),
                           max=float(np.max([h["lab"]["max"] for h in worlds["hidden"]])))
    out["train_worlds"] = [g["n_train"] for g in worlds["groups"]]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job_out")
    ap.add_argument("--job", default="r6-foundryexam-001")
    ap.add_argument("--status", default=None)
    ap.add_argument("--out", default=os.path.join(HERE, "results"))
    ap.add_argument("--name", default="analysis.json")
    a = ap.parse_args()
    d = a.job_out
    info = json.load(open(os.path.join(d, "info.json")))
    gate = json.load(open(os.path.join(d, "gate.json")))
    res = dict(PILOT_NEVER_REUSE_AS_EXAM=True, job=a.job, source=f"origin/gpu-jobs:jobs/{a.job}/out/full",
               job_info={k: info[k] for k in ("size", "arms", "platform", "member_ticks_public_simulator", "hours", "failed",
                                              "skipped", "clock", "config") if k in info},
               gate=dict(passed=gate["passed"], thresholds=gate["thresholds"], burn=gate["burn"], M=gate["M"],
                         tick_r2_median=float(np.median([r["tick_r2"] for r in gate["rows"] if r["ok"]]))),
               bootstrap=dict(n=NB, what="hidden worlds resampled as clusters; one training seed drawn per policy per resample"),
               arms={})
    if a.status and os.path.exists(a.status):
        st = json.load(open(a.status))
        res["status"] = {k: st.get(k) for k in ("job_id", "state", "exit_code", "gpu", "provider", "rate_usd_hr", "cost",
                                                 "started_at", "finished_at", "review", "pod", "message") if k in st}
    for arm in info["arms"]:
        if os.path.exists(os.path.join(d, arm, "scores.npz")):
            res["arms"][arm] = analyse_arm(d, arm)
            r = res["arms"][arm]
            print(arm, "worlds", r["n_hidden"], "sigma", round(r["acceptance"]["sigma"]["value"], 3), "+-",
                  round(r["acceptance"]["sigma"]["se"], 3), r["acceptance"]["sigma_verdict"], "| no-exp share",
                  round(r["acceptance"]["share_noexp"]["value"], 3), r["acceptance"]["trivial_verdict"])
            print("  OES pooled:", {b: round(v["oes_pooled"]["value"], 3) for b, v in r["table"].items()})
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, a.name), "w") as f:
        json.dump(res, f, indent=1)
    print("wrote", os.path.join(a.out, a.name))


if __name__ == "__main__":
    main()
