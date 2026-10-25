"""c19: K2 biomass share sum(K2)/sum(K1+K2) over time in labkit frames.npz of membrane_evo arms (render ch 0 = K1,
ch 1 = K2), plus labkit's L-link and wall radial scores. usage: k2share.py <review dir>"""
import sys, json, glob, numpy as np
out = {}
for arm in ("up", "twin"):
    for d in sorted(glob.glob(f"{sys.argv[1]}/{arm}/seed*")):
        F = np.load(d + "/frames.npz"); R = F["render"].astype(np.float64); f = F["render_f"]; spf = json.load(open(d + "/metrics.json"))["steps_per_frame"]
        k1, k2 = R[:, 0].sum((1, 2)), R[:, 1].sum((1, 2)); sh = k2 / np.maximum(k1 + k2, 1e-9)
        idx = [int(np.argmin(np.abs(f * spf - t))) for t in (10000, 20000, 30000, 40000)]
        fx = open(d + "/FACTS.md").read()
        Lline = [l for l in fx.splitlines() if "radial L link" in l]; Wline = [l for l in fx.splitlines() if "radial membrane (wall)" in l]
        rep = [l for l in fx.splitlines() if l.startswith("- replication")]
        out[f"{arm}/{d.split('seed')[-1]}"] = {"K2_share_t10k_20k_30k_40k": [round(float(sh[i]), 3) for i in idx], "biomass_end": round(float(k1[-1] + k2[-1]), 1),
            "L_radial": Lline[0].split(":", 1)[1].strip()[:120] if Lline else None, "replication": rep[0][2:] if rep else None}
json.dump(out, open(f"{sys.argv[1]}/k2share.json", "w"), indent=1)
for k, v in out.items(): print(k, v["K2_share_t10k_20k_30k_40k"], "biomass", v["biomass_end"], "|", (v["replication"] or "")[60:160])
