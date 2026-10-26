"""o_resync (c30) on genotype censuses of coevbits runs: alive genotype counts every DT steps, per species.
usage: resync.py tag twin_tag seeds..."""
import sys, os, json, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife/collective/contrib/20261026T0330-c30-o-resync-tool")
from o_resync import new_adaptive
DT = int(os.environ.get("DT", 1000)); WIN = 10  # censuses per window (10000 steps)


def censuses(tag, seed, sp):
    d = np.load(f"/home/user/physim/research/alife/collective/contrib/wip-c37/coev/data/{tag}_s{seed}.npz"); log = d["log"].astype(np.float64); m = json.load(open(f"/home/user/physim/research/alife/collective/contrib/wip-c37/coev/data/{tag}_s{seed}.json"))
    p = m["prm"]; n0 = int(p["Np0"] if sp == 0 else p["Nq0"]); T = int(m["t_end"])
    e = log[log[:, 1] == sp]; e = e[np.argsort(e[:, 0], kind="stable")]
    g = {}; cnt = {0: n0}; rows = []; k = 0
    first = 0 if sp == 0 else int(p["Np0"])
    for i in range(first, first + n0): g[i] = 0
    for tc in range(0, T, DT):
        while k < len(e) and e[k, 0] < tc:
            t, _, ty, iid, par, gg, _ = e[k]; iid = int(iid)
            if ty == 1:
                gg = int(gg); g[iid] = gg; cnt[gg] = cnt.get(gg, 0) + 1
            else:
                gg = g.pop(iid, None)
                if gg is not None:
                    cnt[gg] -= 1
                    if cnt[gg] == 0: del cnt[gg]
            k += 1
        rows.append(dict(cnt))
    return rows


tag, twin = sys.argv[1], sys.argv[2]; out = {}
for seed in map(int, sys.argv[3:]):
    for sp, nm in (((1, "pred"), (0, "prey")) if os.environ.get("SP") != "pred" else ((1, "pred"),)):
        for gen in (1, 2, 4):
            for t_, lab in ((tag, "real"), (twin, "twin")):
                r = new_adaptive(censuses(t_, seed, sp), g=gen, win=WIN)
                late = int(sum(r["by_cross"][2:])); out[f"s{seed}_{nm}_g{gen}_{lab}"] = dict(late=late, **r)
            print(seed, nm, "g", gen, "late new-adaptive real", out[f"s{seed}_{nm}_g{gen}_real"]["late"], "twin", out[f"s{seed}_{nm}_g{gen}_twin"]["late"],
                  "| real by_cross", out[f"s{seed}_{nm}_g{gen}_real"]["by_cross"], flush=True)
json.dump(out, open(f"data/resync_{tag}_vs_{twin}.json", "w"))
