"""(c27) c30's o_measure statistics on fresh-seed runs: real vs Rechtsteiner-Bedau shadow."""
import glob, os, json, numpy as np, o_measure as om
out = {}
for sub, T, win in (("runs", 2000, 200), ("long", 20000, 1000)):
    for p in sorted(glob.glob(f"{sub}/*.npz")):
        L = {k: v for k, v in np.load(p).items()}; tag = f"{sub}/{os.path.basename(p)[:-4]}"
        if L["pop"][-1] == 0: out[tag] = {"extinct_at": int(np.argmax(L["pop"] == 0))}; continue
        sh = om.shadow(L, seed=1)
        a = om.stats(L, T, win=win, Lc=1000); b = om.stats(sh | {"mut_n": L["mut_n"]}, T, win=win, Lc=1000)
        out[tag] = {"unique_k2": int(a["cum_unique"][-1]), "shadow_unique_k2": int(b["cum_unique"][-1]),
                    "cohort_new": a["cohort_new"].tolist(), "shadow_cohort_new": b["cohort_new"].tolist(),
                    "mean_size_last": round(float(a["mean_size"][-1]), 2), "top20_overlap_first": [round(v, 2) for v in a["top_overlap_first"]]}
        print(tag, json.dumps({k: v for k, v in out[tag].items()}))
json.dump(out, open("results_c27.json", "w"), indent=1)
