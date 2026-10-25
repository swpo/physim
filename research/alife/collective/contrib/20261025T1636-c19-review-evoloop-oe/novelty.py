"""c19: novelty readout of geno_run.py censuses (c16's design): established genotype = signal readout ('sig') that
reaches >= 20 copies in some census; checks the form '44' + (side+2) x '7'; last time a new genotype became
established; dominant side at the end; largest peak of any genotype not of that form; distinct readouts seen.
Also a plot of the dominant genotype's side and the number of genotypes with >= 2 copies over time.
usage: novelty.py out.png geno_s*.json"""
import sys, json, collections
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(10, 3.4)); res = {}
for fn in sys.argv[2:]:
    d = json.load(open(fn)); C = d["census"]; seen = set(); est = {}; peak = collections.Counter(); dom = []; div = []
    for c in C:
        for g, k in c["sig"].items():
            seen.add(g); peak[g] = max(peak[g], k)
            if k >= 20 and g not in est: est[g] = c["t"]
        top = max(c["sig"].items(), key=lambda x: x[1]) if c["sig"] else ("0|", 0)
        dom.append(int(top[0].split("|")[0])); div.append(sum(1 for k in c["sig"].values() if k >= 2))
    rule = lambda g: g.split("|")[1] == "44" + "7" * (int(g.split("|")[0]) + 2)
    nonrule = max([k for g, k in peak.items() if not rule(g)] or [0])
    res[f"seed{d['seed']}"] = {"readouts_seen": len(seen), "established": sorted(([t, g] for g, t in est.items())), "all_established_follow_rule": all(rule(g) for g in est),
                              "last_new_established_t": max(est.values()), "dominant_side_final": dom[-1], "max_peak_nonrule": nonrule, "loops_final": C[-1]["n"]}
    T = [c["t"] for c in C]; ax[0].plot(T, dom, label=f"seed {d['seed']}"); ax[1].plot(T, div, label=f"seed {d['seed']}")
ax[0].set_title("hole side of the most common genotype", fontsize=9); ax[1].set_title("genotypes with >= 2 copies", fontsize=9)
for a in ax: a.set_xlabel("step"); a.legend(fontsize=7)
plt.tight_layout(); plt.savefig(sys.argv[1], dpi=80); json.dump(res, open(sys.argv[1].replace(".png", ".json"), "w"), indent=1)
print(json.dumps(res, indent=1))
