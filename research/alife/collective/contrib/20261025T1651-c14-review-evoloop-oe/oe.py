"""Novelty readout from geno_run census files: established signal genotypes (>= 20 copies in one census),
time each first established, the dominant genotype's side over time, and standing diversity (>= 2 copies)."""
import sys, json, gzip
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 3, figsize=(14, 3.6)); out = {}
for k, fn in enumerate(sys.argv[1:-1]):
    d = json.load(gzip.open(fn) if fn.endswith('.gz') else open(fn)); C = d["census"]
    seen, est, first_est, T, nseen, nest, dom, div = set(), set(), {}, [], [], [], [], []
    for c in C:
        sig = c["sig"]; seen |= set(sig)
        for g, n in sig.items():
            if n >= 20 and g not in est: est.add(g); first_est[g] = c["t"]
        T.append(c["t"]); nseen.append(len(seen)); nest.append(len(est))
        top = max(sig.items(), key=lambda x: x[1])[0] if sig else "0|"; dom.append(int(top.split("|")[0]))
        div.append(sum(1 for n in sig.values() if n >= 2))
    lab = f"{fn.split('/')[-1]}"
    ax[0].semilogy(T, nest, label=lab + " established"); ax[0].semilogy(T, nseen, ":", label=lab + " any")
    ax[1].plot(T, dom, label=lab); ax[2].plot(T, div, lw=0.7, label=lab)
    out[lab] = dict(T=T[-1], any_readouts=len(seen), established=sorted(first_est.items(), key=lambda x: x[1]), dominant_final_side=dom[-1], last_new_established=max(first_est.values()) if first_est else None, standing_div_last_50=sum(div[-50:]) / max(len(div[-50:]), 1))
for a, t in zip(ax, ["cumulative genotypes (solid: >= 20 copies)", "side of dominant genotype", "genotypes with >= 2 copies"]):
    a.set_title(t, fontsize=9); a.set_xlabel("step"); a.legend(fontsize=6)
fig.tight_layout(); fig.savefig(sys.argv[-1], dpi=90); print(json.dumps(out, indent=1))
