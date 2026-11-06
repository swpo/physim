"""calibrate.py -- calibrate the VW-0 certificate estimators on linear-Gaussian worlds.

For each world: run the generic (model-free, designer-side) estimators in vecworld.Designer
and compare with the closed forms in lingauss.ClosedForms. Also checks the composition
operators (product, stack, refine) against the closed forms of the composed linear system,
and the exam harness against the exact Kalman reference.

    OMP_NUM_THREADS=1 python calibrate.py [--quick]
Writes calibration/results.json and calibration/summary.md.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time

import numpy as np

import vecworld as vw
from lingauss import ClosedForms, LinearGaussian, lumpable_refinement, random_lg, ring

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "calibration")
HOR, PAS, BLK = (1, 2, 4, 8, 16), (0, 1, 2, 4, 8, 16), (4,)


def worlds():
    """(label, LinearGaussian giving the closed forms, VectorWorld built by the generic code)."""
    out = []
    r = ring()
    out.append(("ring", r, r.world(1)))
    rc = ring(conserve=True)
    out.append(("ring-conserved", rc, rc.world(2)))
    rl = random_lg()
    out.append(("random", rl, rl.world(3)))
    # concatenation through vecworld.product, closed form from the block-diagonal system
    cat = vw.VectorWorld(vw.product(r.spec(), rl.spec(), name="ring+random"), 4)
    out.append(("concat(ring,random)", LinearGaussian.concat(r, rl), cat))
    # stacking: level 2 = sums of adjacent level-1 blocks (6 -> 3)
    C2 = np.kron(np.eye(3), np.ones((1, 2)))
    st = vw.VectorWorld(vw.stack(r.spec(), lambda h1, m: h1 @ C2.T, 3, name="stack(ring)"), 5)
    out.append(("stack(ring)", r.stacked(C2), st))
    # downward refinement: exactly lumpable (eta=0) and leaky (eta=0.3)
    for eta in (0.0, 0.3):
        Af, Psi, Qf, Lam = lumpable_refinement(r, eta=eta)
        lgf = r.refined(Af, Psi, Qf, Lam, name=f"refine(ring,eta={eta})")
        Lq, Fs = lgf.Lq, lgf.Fs
        spec = vw.refine(r.spec(), law=lambda h, xi, Af=Af, Lq=Lq: h @ Af.T + xi @ Lq.T, n_fine=Af.shape[0],
                         psi=lambda x, Psi=Psi: x @ Psi.T, init=lambda rng, Fs=Fs: Fs @ rng.standard_normal(Fs.shape[1]),
                         noise_dim=Lq.shape[1], lift=lambda u, Lam=Lam: u @ Lam.T, name=lgf.name)
        out.append((lgf.name, lgf, vw.VectorWorld(spec, 1)))     # world_seed 1: same permutations as ring
    return out


def zstats(est, cf, se):
    est, cf, se = np.asarray(est, float), np.asarray(cf, float), np.asarray(se, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        z = (est - cf) / se
        rel = np.abs(est - cf) / np.maximum(np.abs(cf), 1e-12)
    ok = np.isfinite(z)
    return {"max_abs_z": float(np.max(np.abs(z[ok]))) if ok.any() else float("nan"),
            "rms_z": float(np.sqrt(np.mean(z[ok] ** 2))) if ok.any() else float("nan"),
            "max_rel": float(np.max(rel[np.isfinite(rel)])), "n": int(ok.sum())}


def calibrate_world(label, lg, w, N, n_or, quick):
    t = time.time()
    d, cf = w.designer, ClosedForms(lg, w)
    cl = d.closure(HOR, PAS, BLK, n_traj=N, n_oracle=n_or, n_rep=16, n_programs=2, rate=0.5, seed=7)
    cc = cf.closure(HOR, PAS, BLK)
    res = {"world": label, "n0": lg.n0, "n_obs": w.n_obs, "n_in": w.n_in}
    res["closure"] = {"est": {k: cl[k] for k in ("V0", "Vu", "Ve", "gap_nats", "ceiling", "block_gap_nats")},
                      "se": cl["se"], "atay_est": cl["atay"],
                      "cf": {k: cc[k] for k in ("V0", "Vu", "Ve", "gap_nats", "ceiling", "block_gap_nats")},
                      "atay_cf": cc["atay"], "p_inf_cf": cc["p_inf"]}
    agree = {k: zstats(cl[k], cc[k], cl["se"][k]) for k in ("Vu", "Ve", "gap_nats", "ceiling", "block_gap_nats")}
    # program independence: each program's gap table against the closed form
    agree["per_program_gap_max_abs_diff"] = float(max(np.max(np.abs(p["gap_nats"] - cc["gap_nats"]))
                                                      for p in cl["per_program"]))
    res["closure"]["agreement"] = agree
    lk, lc = d.leak(PAS, n_traj=N, seed=7), cf.leak(PAS)
    res["leak"] = {"est": {"info_nats": lk["info_nats"], "dim": lk["dim"], "rank": lk["rank"],
                           "mu_p1": lk["mu"][1], "mu_pmax": lk["mu"][-1]},
                   "cf": {"info_nats": lc["info_nats"], "dim": lc["dim"], "rank": lc["rank"],
                          "mu_p1": lc["mu"][1], "mu_pmax": lc["mu"][-1], "mu_inf": lc["inf"]["mu"]},
                   "max_rel_info": float(np.max(np.abs(lk["info_nats"][1:] - lc["info_nats"][1:])
                                                / lc["info_nats"][1:])),
                   "max_abs_mu": float(max(np.max(np.abs(a - b)) for a, b in zip(lk["mu"], lc["mu"]))),
                   "dims_equal": bool(np.array_equal(lk["dim"], lc["dim"]))}
    ic, icc = d.input_capacity(L=8, p=8, n_states=2, n_traj=N, seed=7), cf.input_capacity(L=8, p=8)
    keys = ("excitable_dim_per_tick", "visible_dim", "capacity_bits_upper", "capacity_channels",
            "atom_snr_median", "atom_visible_frac", "command_bits_upper")
    res["input_capacity"] = {
        "est": {k: ic[k] for k in keys} | {"singular_values": ic["singular_values"]},
        "cf": {k: icc[k] for k in keys} | {"singular_values": icc["singular_values"]},
        "response_max_abs_err": float(np.max(np.abs(ic["response"] - icc["response"]))),
        "sv_max_rel": float(np.max(np.abs(ic["singular_values"] - icc["singular_values"])
                                   / np.maximum(icc["singular_values"], 1e-9 * icc["singular_values"][0]))),
        "capacity_rel": float(abs(ic["capacity_bits_upper"] - icc["capacity_bits_upper"]) / icc["capacity_bits_upper"]),
    }
    oc, occ = d.observation_capacity((1, 16), n_traj=N, seed=7), cf.observation_capacity((1, 16))
    res["observation_capacity"] = {"est": {"rate_bits": oc["rate_bits"], "channel_bits_upper": oc["channel_bits_upper"]},
                                   "cf": {"rate_bits": occ["rate_bits"], "rate_bits_inf": occ["rate_bits_inf"],
                                          "channel_bits_upper": occ["channel_bits_upper"]},
                                   "rate_abs_err_bits": float(np.max(np.abs(oc["rate_bits"] - occ["rate_bits"])))}
    if w.spec.invariants:
        res["invariant_drift"] = d.invariant_drift(T=50, B=16)
    res["seconds"] = time.time() - t
    return res


def calibrate_exam(label, lg, w, n_items, quick):
    cf = ClosedForms(lg, w)
    ex = vw.Exam(w, n_items=n_items, prefix=16, horizon=16, queries=(1, 2, 4, 8, 16), exam_seed=3)
    sc = ex.score(n_rep=32, references={"kalman": cf.kalman_predict}, ceiling="kalman")
    qs = sc["queries"]
    return {"world": label, "queries": qs, "n_items": n_items,
            "mse_kalman": sc["mse"]["kalman"], "mse_kalman_se": sc["mse_se"]["kalman"],
            "cf_kalman": [float(np.trace(cf.Se(q, 17))) for q in qs],
            "mse_persistence": sc["mse"]["persistence"], "oracle": sc["oracle"],
            "cf_oracle": [float(np.trace(cf.Su(q))) for q in qs],
            "skill_oracle_vs_kalman": sc["skill"]["kalman"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()
    N, n_or, n_items = (8000, 2000, 60) if a.quick else (40000, 8000, 400)
    os.makedirs(OUT, exist_ok=True)
    results = {"N": N, "n_oracle": n_or, "n_rep": 16, "horizons": HOR, "pasts": PAS, "blocks": BLK, "worlds": []}
    ws = worlds()
    for label, lg, w in ws:
        r = calibrate_world(label, lg, w, N, n_or, a.quick)
        results["worlds"].append(r)
        ag = r["closure"]["agreement"]
        print(f"{label:24s} {r['seconds']:6.1f}s  gap max|z|={ag['gap_nats']['max_abs_z']:.2f} "
              f"Ve max|z|={ag['Ve']['max_abs_z']:.2f}  Vu max|z|={ag['Vu']['max_abs_z']:.2f}  "
              f"leak rel={r['leak']['max_rel_info']:.4f}  sv rel={r['input_capacity']['sv_max_rel']:.4f}  "
              f"obs err={r['observation_capacity']['rate_abs_err_bits']:.4f}", flush=True)
    # composition identities in closed form
    by = {label: (lg, w) for label, lg, w in ws}
    g = {lab: ClosedForms(*by[lab]).closure(HOR, PAS, BLK)["gap_nats"] for lab in by}
    comp = {"concat_gap_minus_sum_max_abs": float(np.max(np.abs(g["concat(ring,random)"] - g["ring"] - g["random"]))),
            "lumpable_refinement_gap_minus_base_max_abs": float(np.max(np.abs(g["refine(ring,eta=0.0)"] - g["ring"]))),
            "leaky_refinement_gap_minus_base": (g["refine(ring,eta=0.3)"] - g["ring"]),
            "stack_vs_base_gap": {"stack": g["stack(ring)"], "ring": g["ring"]}}
    r0 = ring()
    for eta in (0.0, 0.3):
        Af, Psi, Qf, Lam = lumpable_refinement(r0, eta=eta)
        lab = f"refine(ring,eta={eta})"
        lgf, wf = by[lab]
        for T in (1, 4):
            est = vw.commutation_error(wf, lambda x, Psi=Psi: x @ Psi.T, by["ring"][1], T=T, n=4000, n_rep=16)
            comp[f"commutation_{lab}_T{T}"] = {"est": est["delta2"], "mc_bias": est["mc_bias"],
                                               "cf": ClosedForms(lgf, wf).commutation_delta2(r0, Psi, T)}
    results["composition"] = comp
    print("composition", json.dumps(vw.jsonable({k: v for k, v in comp.items() if "commutation" in k or "max_abs" in k})))
    results["exam"] = [calibrate_exam(lab, *by[lab], n_items, a.quick) for lab in ("ring", "random")]
    for e in results["exam"]:
        print("exam", e["world"], np.round(e["mse_kalman"], 3), np.round(e["cf_kalman"], 3),
              np.round(e["oracle"], 3), np.round(e["cf_oracle"], 3))
    with open(os.path.join(OUT, "results.json" if not a.quick else "results_quick.json"), "w") as f:
        json.dump(vw.jsonable(results), f, indent=1)
    if not a.quick:
        write_summary(results)


def write_summary(R):
    L = ["# VW-0 estimator calibration on linear-Gaussian worlds", "",
         f"N = {R['N']} trajectories per program (3 programs: empty + 2 random admissible), oracle "
         f"{R['n_oracle']} x {R['n_rep']} fresh-noise branches; 8-fold standard errors. "
         "z = (estimate - closed form)/SE over all horizons 1-16 and pasts 0-16.", "",
         "| world | n0 | gap max abs z | gap rms z | Ve max abs z | Vu max abs z | ceiling max abs z | block-gap max abs z |"
         " leak info max rel err | leak dims equal | response max abs err | sing. value max rel err | capacity rel err | obs rate abs err (bits) |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in R["worlds"]:
        a = r["closure"]["agreement"]
        L.append(f"| {r['world']} | {r['n0']} | {a['gap_nats']['max_abs_z']:.2f} | {a['gap_nats']['rms_z']:.2f} | "
                 f"{a['Ve']['max_abs_z']:.2f} | {a['Vu']['max_abs_z']:.2f} | {a['ceiling']['max_abs_z']:.2f} | "
                 f"{a['block_gap_nats']['max_abs_z']:.2f} | {r['leak']['max_rel_info']:.4f} | {r['leak']['dims_equal']} | "
                 f"{r['input_capacity']['response_max_abs_err']:.1e} | {r['input_capacity']['sv_max_rel']:.4f} | "
                 f"{r['input_capacity']['capacity_rel']:.4f} | {r['observation_capacity']['rate_abs_err_bits']:.4f} |")
    r = R["worlds"][0]
    c = r["closure"]
    L += ["", "## ring world (n0 = 24, n_obs = 6): closure, estimate +- SE / closed form", "",
          "| tau | Vu | Ve(p=1) | Ve(p=16) | gap(p=0) nats | gap(p=1) nats | gap(p=16) nats | gap(p=inf) nats | ceiling(p=16) |",
          "|---|---|---|---|---|---|---|---|---|"]
    P = list(R["pasts"])
    for i, h in enumerate(R["horizons"]):
        e, s, f = c["est"], c["se"], c["cf"]
        L.append(f"| {h} | {e['Vu'][i]:.3f}+-{s['Vu'][i]:.3f} / {f['Vu'][i]:.3f} | "
                 f"{e['Ve'][i][P.index(1)]:.3f} / {f['Ve'][i][P.index(1)]:.3f} | "
                 f"{e['Ve'][i][-1]:.3f}+-{s['Ve'][i][-1]:.3f} / {f['Ve'][i][-1]:.3f} | "
                 f"{e['gap_nats'][i][0]:.3f} / {f['gap_nats'][i][0]:.3f} | "
                 f"{e['gap_nats'][i][P.index(1)]:.3f}+-{s['gap_nats'][i][P.index(1)]:.3f} / {f['gap_nats'][i][P.index(1)]:.3f} | "
                 f"{e['gap_nats'][i][-1]:.3f}+-{s['gap_nats'][i][-1]:.3f} / {f['gap_nats'][i][-1]:.3f} | "
                 f"{c['p_inf_cf']['gap_nats'][i]:.3f} | {e['ceiling'][i][-1]:.4f} / {f['ceiling'][i][-1]:.4f} |")
    L += ["", "## Atay one-step split (nats): estimate / closed form (p_max = 16; closed form p = inf in brackets)", "",
          "| world | leak | memory | residual |", "|---|---|---|---|"]
    for r in R["worlds"]:
        ae, ac, ai = r["closure"]["atay_est"], r["closure"]["atay_cf"], r["closure"]["p_inf_cf"]["atay"]
        L.append(f"| {r['world']} | {ae['leak']:.4f} / {ac['leak']:.4f} | {ae['memory']:.4f} / {ac['memory']:.4f} "
                 f"[{ai['memory']:.4f}] | {ae['residual']:.4f} / {ac['residual']:.4f} [{ai['residual']:.4f}] |")
    L += ["", "## Leak, input and observation capacity: estimate / closed form", "",
          "| world | leak info p=1 (nats) | leak info p=16 | leak dim p=16 / rank | excitable dim/tick | visible dim | "
          "capacity bound (bits/tick) | atom SNR median | atoms visible | obs rate p=16 (bits/tick) | obs channel bound (bits) |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in R["worlds"]:
        le, lc = r["leak"]["est"], r["leak"]["cf"]
        ie, icf = r["input_capacity"]["est"], r["input_capacity"]["cf"]
        oe, ocf = r["observation_capacity"]["est"], r["observation_capacity"]["cf"]
        L.append(f"| {r['world']} | {le['info_nats'][1]:.3f} / {lc['info_nats'][1]:.3f} | "
                 f"{le['info_nats'][-1]:.3f} / {lc['info_nats'][-1]:.3f} | {le['dim'][-1]}/{le['rank']} / {lc['dim'][-1]}/{lc['rank']} | "
                 f"{ie['excitable_dim_per_tick']} | {ie['visible_dim']} / {icf['visible_dim']} | "
                 f"{ie['capacity_bits_upper']:.3f} / {icf['capacity_bits_upper']:.3f} | "
                 f"{ie['atom_snr_median']:.3f} / {icf['atom_snr_median']:.3f} | "
                 f"{ie['atom_visible_frac']:.3f} / {icf['atom_visible_frac']:.3f} | "
                 f"{oe['rate_bits'][-1]:.3f} / {ocf['rate_bits'][-1]:.3f} | {oe['channel_bits_upper']:.3f} / {ocf['channel_bits_upper']:.3f} |")
    C = R["composition"]
    L += ["", "## Composition", "",
          f"- concat: closed-form gap(concat) - gap(ring) - gap(random), max over the table: {C['concat_gap_minus_sum_max_abs']:.1e} nats (additive).",
          f"- exactly lumpable refinement (level -1, n = 48): gap minus base gap, max: {C['lumpable_refinement_gap_minus_base_max_abs']:.1e} nats (the refinement is invisible at level 1).",
          f"- leaky refinement (eta = 0.3): gap minus base gap at p = 16, tau = 1..16: "
          + ", ".join(f"{v[-1]:.3f}" for v in C["leaky_refinement_gap_minus_base"]) + " nats."]
    for k, v in C.items():
        if k.startswith("commutation"):
            L.append(f"- {k}: delta^2 estimate {v['est']:.4f} (MC bias removed {v['mc_bias']:.4f}) / closed form {v['cf']:.4f}")
    L += ["", "## Exam harness: Kalman reference (exact level-1 ceiling) and oracle, MSE estimate +- SE / closed form", "",
          "| world | tau | persistence | Kalman | Kalman closed form | oracle | oracle closed form |", "|---|---|---|---|---|---|---|"]
    for e in R["exam"]:
        for i, q in enumerate(e["queries"]):
            L.append(f"| {e['world']} | {q} | {e['mse_persistence'][i]:.3f} | {e['mse_kalman'][i]:.3f}+-{e['mse_kalman_se'][i]:.3f} | "
                     f"{e['cf_kalman'][i]:.3f} | {e['oracle'][i]:.3f} | {e['cf_oracle'][i]:.3f} |")
    with open(os.path.join(OUT, "summary.md"), "w") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
