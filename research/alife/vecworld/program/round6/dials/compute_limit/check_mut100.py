"""check_mut100 -- does the box side at which pooled small boxes stop transferring move with a parameter?

Round 6, dials/compute_limit. The pools of run_boxes.py at mut128 = 100 (a mutation event every 100 time units
per 128 x 128 px: every 20 ticks at 128 px, every 80 ticks at 64 px, as at 64 and 32 px with mut128 = 25) are
scored like analyse.py's transfer table: truth = the 128 px members, sources = the 64 px members, naive rescale
against pooling four boxes. Declared parameters (eps 0.4, mut128 100): PILOT_NEVER_REUSE_AS_EXAM, nothing hidden.

  python -B check_mut100.py <scratch dir>      -> results/mut100.json   (needs m100_b64_s*.npz, m100_b128_s*.npz)
"""
import glob
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyse as A  # noqa: E402


def load(S, H):
    L = [np.load(f)["l2"].astype(float) for f in sorted(glob.glob(os.path.join(S, f"m100_b{H}_s*.npz")))]
    T = min(x.shape[1] for x in L)
    return np.concatenate([x[:, :T] for x in L], 0)


def main():
    S = sys.argv[1]
    rng = np.random.default_rng(100)
    P64, P128 = load(S, 64), load(S, 128)
    T = min(P64.shape[1], P128.shape[1])
    P64, P128 = P64[:, :T], P128[:, :T]
    B8 = P128.shape[0]
    anch = [a for a in (80, 100, 120, 140, 160, 180, 200, 220, 240) if a + 8 <= T]
    items = [(a, h) for a in anch for h in A.HS if a + h <= T]
    sc = np.array([P128[:, anch[0] - 1:, 0].std(), P128[:, anch[0] - 1:, 1].std()])
    syn = A.pool_tiles(P64, np.random.default_rng([64, 100]), 64, 4)
    fixed = {"ridge64": ("ridge", A.ridge_fit(P64, 4.0)), "ridge64pool4": ("ridge", A.ridge_fit(syn, 1.0)),
             "law64": ("law", A.law_fit(P64, "law"), 4.0), "lin64": ("law", A.law_fit(P64, "lin"), 4.0),
             "const64": ("law", A.law_fit(P64, "const"), 4.0), "law64pool4": ("law", A.law_fit(syn, "law"), 1.0)}
    pol = {}

    def put(name, i, Xf, y):
        d = pol.setdefault(name, {"all": np.zeros(B8), "s_b": np.zeros(B8), "n": np.zeros(B8)})
        d["all"][i] += A.fair_es(Xf, y, sc)
        d["s_b"][i] += A.fair_es(Xf[:, 1:2], y[1:2], sc[1:2])
        d["n"][i] += 1

    for i in range(B8):
        others = np.array([j for j in range(B8) if j != i])
        clim = P128[others][:, A.LAB + 19:].reshape(-1, 2)
        r0 = np.random.default_rng([i, 100])
        own = {"ridge128_loo": ("ridge", A.ridge_fit(P128[others], 1.0)),
               "law128_loo": ("law", A.law_fit(P128[others], "law"), 1.0)}
        for (a, h) in items:
            x0, y = P128[i, a - 1].copy(), P128[i, a + h - 1]
            put("K", i, clim[r0.integers(0, len(clim), 64)], y)
            put("Ktick", i, P128[others, a + h - 1], y)
            put("Ktick64", i, P64[:, a + h - 1] * np.array([4.0, 1.0]), y)
            put("Ktick64pool4", i, syn[:, a + h - 1], y)
            for name, m in {**fixed, **own}.items():
                for _ in range(4):
                    Xf = A.ridge_predict(m[1], x0, h, r0) if m[0] == "ridge" else A.law_predict(m[1], x0, h, r0, m[2])
                    put(name, i, Xf, y)

    def L(name, cell, idx=None):
        v = pol[name][cell] / pol[name]["n"]
        return v.mean() if idx is None else v[idx].mean()

    def skill(name, cell):
        boot = [1 - L(name, cell, idx) / L("K", cell, idx) for idx in rng.integers(0, B8, (1000, B8))]
        return [round(float(1 - L(name, cell) / L("K", cell)), 4), round(float(np.std(boot)), 4)]

    def diff(n1, n2, cell):
        boot = [(L(n2, cell, idx) - L(n1, cell, idx)) / L("K", cell, idx) for idx in rng.integers(0, B8, (1000, B8))]
        v = (L(n2, cell) - L(n1, cell)) / L("K", cell)
        se = float(np.std(boot))
        return [round(float(v), 4), round(se, 4), round(float(v / max(se, 1e-9)), 2)]

    def fs(l2):
        sb = l2[..., 1]
        t75 = np.array([np.argmax(s >= 0.75) + 1 if (s >= 0.75).any() else np.nan for s in sb])
        t25 = np.array([np.argmax(s >= 0.25) + 1 if (s >= 0.25).any() else np.nan for s in sb])
        c = A.law_fit(l2, "law")
        d = t75 - t25
        return dict(members=int(l2.shape[0]), N_mean=round(float(l2[:, A.LAB:, 0].mean()), 3),
                    s_b_mean_at_tick={str(t): round(float(sb[:, t - 1].mean()), 3) for t in (100, 140, 180, 220, 260, 300) if t <= T},
                    ticks_from_s25_to_s75_mean_se=[round(float(np.nanmean(d)), 1),
                                                   round(float(np.nanstd(d, ddof=1) / np.sqrt(max(np.isfinite(d).sum(), 1))), 1)],
                    members_reaching_s75=int(np.isfinite(t75).sum()),
                    law_per_8_ticks=dict(b1=round(c["co"][0], 4), b2=round(c["co"][1], 4), v=round(c["v"], 4)))

    cmp_ = {}
    for cell in ("all", "s_b"):
        for a, b in (("ridge128_loo", "ridge64pool4"), ("ridge128_loo", "ridge64"), ("Ktick", "Ktick64pool4"),
                     ("Ktick", "Ktick64"), ("ridge64pool4", "ridge64"), ("law128_loo", "law64"), ("law64", "lin64"),
                     ("law64", "const64"), ("law64", "ridge64pool4"), ("law128_loo", "law64pool4")):
            cmp_[f"{a} - {b} |{cell}"] = diff(a, b, cell)
    out = dict(
        what="transfer from 64 px boxes to a 128 px box at mut128 = 100 (eps 0.4): the 64 px box has one mutation event "
             "per 80 ticks, as the 32 px box has at mut128 = 25; rows as in summary.json transfer_128",
        PILOT_NEVER_REUSE_AS_EXAM=True, parameters="declared, not hidden: eps 0.4, mut128 100, others vxlib.THETA0",
        ticks=int(T), truth_members=B8, items_per_member=len(items), scale_sd=[round(float(v), 4) for v in sc],
        finite_size={"64": fs(P64), "128": fs(P128)},
        skill={c: {k: skill(k, c) for k in sorted(pol) if k != "K"} for c in ("all", "s_b")},
        paired_differences=dict(note="first minus second: skill difference, bootstrap se, z (paired over the truth members)", **cmp_))
    with open(os.path.join(HERE, "results", "mut100.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
