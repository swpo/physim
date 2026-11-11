"""adv_fit -- the adversary's form-free repairs of the public law, fitted on the Lab and scored as gvh.py scores.

    python -B adv_fit.py IN.npz [OUT.json] [designer's gvh json, for the paired check and its H column] [ACT.npz]

Input: adv_sim.py's arrays (gvh.py's own Lab episodes, test items, truths and public runs; focus view at every
tick; the public law's mean response to 8 transformed programs). DESIGN-STAGE CHECK, state given, tiny size,
PILOT values (never to be reused as an exam).

Every recipe knows only: the public simulator, the program of each episode, and ONE hidden-world future per Lab
episode (the focus view at every tick 1..32, which the Lab shows; gvh.py's recipes use 4 ticks of it). None knows
that there is a carrier, where it converts, or that a route saturates.

    G2        gvh.py's per-horizon gain, recomputed here (alignment check against the designer's file)
    ceiling_true_mean   NOT a policy: the test truths' own mean with the public spread (is the gap a mean shift?)
    A_out     lagged gain: truth response(t) = sum_k a_k * public response(t - k), k in 0, 2, 4, 8, 16 ticks
    A_in      filter bank on the command: truth response(t) = sum_j a_j * public response to program j, the
              programs being the command delayed by 0, 4, 8, 16 ticks, as given or blurred over 3 x 3 bumps
    A_both    A_in and A_out together
    A_in_dur  A_in with every coefficient linear in the pulse duration (a strong pulse may enter differently)
    A_act     (with ACT.npz, from adv_act.py) the public law run under a linearly filtered command (direct gain,
              first-order lag with gain, time constant and blur: 4 numbers on a 39-point grid, least squares on the Lab)
Coefficients are shared over ticks, one set per coordinate, ridge strength by leave-one-EPISODE-out on the Lab;
the forecast ensemble is the public no-input ensemble moved by the fitted response (spread: the public futures
under the program or without it, whichever scores better leave-one-episode-out on the Lab).
Reported as gvh.py reports: L pooled over h = 4, 8, 16, 32 and the share of the public-to-oracle gap closed,
bootstrap SE over test members, for Lab sizes 4, 8, 16 (the first n episodes).
"""
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "vw1")))

import numpy as np  # noqa: E402
from vw.scoring import energy_fair, energy_loo  # noqa: E402

HS = (4, 8, 16, 32)
LAGS = (0, 2, 4, 8, 16)
ALPHAS = (1e-3, 1e-2, 1e-1, 1.0, 10.0)


def lagged(d, lags=LAGS):
    """d (n, T+1, 2) -> (n, len(lags), T+1, 2): the response delayed by each lag (zero before)."""
    out = np.zeros((d.shape[0], len(lags)) + d.shape[1:])
    for k, lg in enumerate(lags):
        out[:, k, lg:] = d[:, :d.shape[1] - lg]
    return out


def features(kind, B, F):
    """(n, p, T+1, 2) regressors of the truth's response, by recipe."""
    d0 = B[:, 0]                                             # d0b0: the public response to the command itself
    if kind == "A_out":
        return lagged(d0)
    if kind == "A_in":
        return B
    if kind == "A_both":
        return np.concatenate([B, lagged(d0)[:, 1:]], 1)
    if kind == "A_in_dur":
        dur = np.abs(F[:, 1])[:, None, None, None]           # duration / 20
        return np.concatenate([B, B * dur], 1)
    raise ValueError(kind)


def ridge(X, y, a):
    return np.linalg.solve(X.T @ X + a * len(X) * np.eye(X.shape[1]), X.T @ y)


def fit_predict(Phi_l, r_l, Phi_t):
    """Per coordinate: ridge over (episode, tick) rows, strength by leave-one-episode-out. Phi (n, p, T+1, 2),
    r (n, T+1, 2). Returns predicted response on the test (m, T+1, 2), the Lab's leave-one-out prediction, alphas."""
    n, p, T1, _ = Phi_l.shape
    pred, loo, alphas, coefs = np.zeros((Phi_t.shape[0], T1, 2)), np.zeros_like(r_l), [], []
    for c in range(2):
        X = Phi_l[:, :, 1:, c].transpose(0, 2, 1)            # (n, T, p)
        s = np.sqrt((X ** 2).mean((0, 1))) + 1e-12
        X = X / s
        y = r_l[:, 1:, c]
        best = None
        for a in ALPHAS:
            P = np.zeros_like(y)
            for i in range(n):
                k = np.arange(n) != i
                P[i] = X[i] @ ridge(X[k].reshape(-1, p), y[k].reshape(-1), a)
            sse = float(((P - y) ** 2).sum())
            if best is None or sse < best[0]:
                best = (sse, a, P)
        w = ridge(X.reshape(-1, p), y.reshape(-1), best[1])
        loo[:, 1:, c] = best[2]
        pred[:, 1:, c] = (Phi_t[:, :, 1:, c].transpose(0, 2, 1) / s) @ w
        alphas.append(best[1])
        coefs.append((w / s).tolist())
    return pred, loo, alphas, coefs


def main():
    d = np.load(sys.argv[1])
    out_path = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "-" else None
    ref = json.load(open(sys.argv[3])) if len(sys.argv) > 3 and sys.argv[3] != "-" else None
    act = np.load(sys.argv[4]) if len(sys.argv) > 4 else None
    y_lab, pub_lab, pub0_lab, Yt, pub, pub0 = (d[k] for k in ("y_lab", "pub_lab", "pub0_lab", "Yt", "pub", "pub0"))
    B_lab, B_test, F_lab, F_test, tm = d["B_lab"], d["B_test"], d["F_lab"], d["F_test"], d["test_member"]
    hs = list(HS)
    sc = Yt[:, :, hs].reshape(-1, len(HS), 2).std(0)
    sc = np.maximum(sc, 0.1 * np.median(sc[sc > 1e-9]))      # gvh.py's scale (test truths)
    s_lab = y_lab[:, 1:].reshape(-1, 2).std(0)               # the recipes' own scale (Lab only)

    def es(X):                                               # (n_items, n_horizons)
        return np.stack([energy_fair(X[:, :, h], Yt[:, :, h], sc[j]) for j, h in enumerate(hs)], 1)
    L = {"pub": es(pub), "pub0": es(pub0),
         "O": np.stack([energy_loo(Yt[:, :, h], sc[j]) for j, h in enumerate(hs)], 1)}
    if "Hh" in d:
        L["H"] = es(d["Hh"])

    # G2 exactly as gvh.py (four horizons, test scale): the alignment check
    n_all = len(y_lab)
    dl = (pub_lab.mean(1) - pub0_lab.mean(1))[:, hs] / sc
    yl = (y_lab - pub0_lab.mean(1))[:, hs] / sc
    dt_ = (pub.mean(1) - pub0.mean(1))[:, hs]
    G2 = pub.copy()
    for j, h in enumerate(hs):
        g = float((dl[:, j] * yl[:, j]).sum() / max((dl[:, j] ** 2).sum(), 1e-12))
        G2[:, :, h] += ((g - 1.0) * dt_[:, j])[:, None]
    L["G2"] = es(G2)
    # NOT a policy: the truths' own mean per item with the public spread (how much of the gap is conditional mean)
    L["ceiling_true_mean"] = es(Yt.mean(1, keepdims=True) + pub - pub.mean(1, keepdims=True))

    info = {}
    for n in (4, 8, 16):
        if n > n_all or B_lab.shape[1] == 0:                 # no filter bank in the input (adv_sim.py bank=0)
            continue
        r_l = (y_lab[:n] - pub0_lab[:n].mean(1)) / s_lab     # the Lab's response (one future) about the public no-input mean
        dev = {"p": pub_lab[:n] - pub_lab[:n].mean(1, keepdims=True), "0": pub0_lab[:n] - pub0_lab[:n].mean(1, keepdims=True)}
        dev_t = {"p": pub - pub.mean(1, keepdims=True), "0": pub0 - pub0.mean(1, keepdims=True)}
        for kind in ("A_out", "A_in", "A_both", "A_in_dur"):
            Pl, Pt = features(kind, B_lab[:n], F_lab[:n]) / s_lab, features(kind, B_test, F_test) / s_lab
            pred, loo, alphas, coefs = fit_predict(Pl, r_l, Pt)
            # spread: chosen on the Lab, leave-one-episode-out fair energy score of the single truth
            lab_es = {}
            for v in ("p", "0"):
                ens = pub0_lab[:n].mean(1, keepdims=True) + loo[:, None] * s_lab + dev[v]
                lab_es[v] = float(sum(energy_fair(ens[:, :, h] / s_lab, y_lab[:n, None, h] / s_lab).mean() for h in hs))
            v = min(lab_es, key=lab_es.get)
            X = pub0.mean(1, keepdims=True) + pred[:, None] * s_lab + dev_t[v]
            L[f"{kind}_n{n}"] = es(X)
            info[f"{kind}_n{n}"] = {"ridge_strength_per_coordinate": alphas, "spread_from": {"p": "public under the program", "0": "public without input"}[v],
                                    "lab_loo_energy": lab_es, "coefficients_per_coordinate": coefs}

    if act is not None:
        for n, g in zip(act["best_n"].tolist(), act["best_g"].tolist()):
            L[f"A_act_n{n}"] = es(act[f"ens_g{g}"])
            info[f"A_act_n{n}"] = {"fit_g0_g1_tau_blur": act["grid"][g].tolist(), "lab_sse": float(act["sse"][g, :n].sum()),
                                   "lab_sse_public_law": float(act["sse"][2, :n].sum()), "spread_from": "the filtered public run itself"}
    Lh = {k: v for k, v in L.items()}                        # per item and horizon
    L = {k: v.sum(1) for k, v in L.items()}
    rb = np.random.default_rng(1)
    members = sorted(set(tm.tolist()))

    def share(idx, k, base="pub"):
        return (L[base][idx].mean() - L[k][idx].mean()) / (L[base][idx].mean() - L["O"][idx].mean())
    out = {"PILOT_NEVER_REUSE_AS_EXAM": True,
           "what": "state-given check on sublevel_second/gvh.py's own items: form-free repairs of the public law (see adv_fit.py docstring)",
           "input": os.path.basename(sys.argv[1]), "truth_pilot": dict(zip(d["truth_keys"].tolist(), d["truth_vals"].tolist())),
           "size_nlab_seed_R_RB": d["meta"].tolist(), "n_test_items": int(len(tm)), "test_members": members,
           "bank_programs": d["names"].tolist(), "lags_ticks": list(LAGS), "cpu_s_sim_gvh_part_bank_total": d["cpu"].tolist(),
           "L": {k: float(v.mean()) for k, v in L.items()}, "share_of_pub_to_O_gap": {}, "recipes": info}
    all_idx = np.arange(len(tm))
    boots = [np.concatenate([np.flatnonzero(tm == m_) for m_ in rb.choice(members, size=len(members))]) for _ in range(400)]
    for k in L:
        if k in ("pub", "O"):
            continue
        out["share_of_pub_to_O_gap"][k] = {"value": float(share(all_idx, k)), "se_members": float(np.std([share(b, k) for b in boots], ddof=1))}
    gap = Lh["pub"] - Lh["O"]
    heavy = max(members, key=lambda m_: gap[tm == m_].sum())
    out["gap_pub_to_O"] = {"share_by_horizon": (gap.sum(0) / gap.sum()).tolist(), "horizons": hs,
                           "share_by_test_member": {str(m_): float(gap[tm == m_].sum() / gap.sum()) for m_ in members},
                           "heaviest_member": int(heavy)}
    out["closed_by_horizon"] = {k: ((Lh["pub"] - v).sum(0) / gap.sum(0)).tolist() for k, v in Lh.items() if k not in ("pub", "O")}
    out["closed_h_le_16"] = {k: float((Lh["pub"] - v)[:, :3].sum() / gap[:, :3].sum()) for k, v in Lh.items() if k not in ("pub", "O")}
    out["closed_without_heaviest_member"] = {k: float((Lh["pub"] - v)[tm != heavy].sum() / gap[tm != heavy].sum())
                                             for k, v in Lh.items() if k not in ("pub", "O")}
    if "Hh" in d:
        out["H_fit_lam_rho_DX"] = d["H_fit"].tolist()
    if ref is not None:                                      # the designer's file for the same seed: are the items the same?
        out["designer_file"] = {"L": ref["L"], "share": {k: v["value"] for k, v in ref["share_of_pub_to_O_gap"].items()},
                                "H_fit": {k: ref["H_fit"][k] for k in ("lam", "rho", "DX")},
                                "max_abs_diff_L_pub_pub0_O_G2": float(max(abs(out["L"][k] - ref["L"][k]) for k in ("pub", "pub0", "O", "G2")))}
        # with identical items the designer's H is paired: the adversary's share of what H closes
        out["designer_file"]["H_share"] = ref["share_of_pub_to_O_gap"]["H"]
    print("L", {k: round(v, 3) for k, v in out["L"].items()})
    for k, v in out["share_of_pub_to_O_gap"].items():
        extra = info.get(k, {})
        print(f"  {k:14s} share {v['value']:+.3f} (se {v['se_members']:.3f})  by h {np.round(out['closed_by_horizon'][k], 2).tolist()}  "
              f"h<=16 {out['closed_h_le_16'][k]:+.2f}  w/o heaviest {out['closed_without_heaviest_member'][k]:+.2f}  "
              f"{extra.get('fit_g0_g1_tau_blur', '')}")
    print("  gap by horizon", np.round(out["gap_pub_to_O"]["share_by_horizon"], 2).tolist(), "by member",
          {k: round(v, 2) for k, v in out["gap_pub_to_O"]["share_by_test_member"].items()})
    if ref is not None:
        print("  designer:", {k: round(v, 3) for k, v in ref["L"].items()}, "max |dL|", out["designer_file"]["max_abs_diff_L_pub_pub0_O_G2"])
    if out_path:
        json.dump(out, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main()
