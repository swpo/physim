"""bff_o.png and results.json from data/ (spontaneous stats, seeded stats, functional census).
python make_fig.py"""
import os, sys, json, gzip, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from o_measure import census_shadow
from o_bff import early, sig_per_window
J_ = lambda f: [json.loads(l) for l in open(f"{HERE}/data/{f}")]
sp = {s: J_(f"spont_stats_s{s}.jsonl") for s in (0, 1)}; sd = J_("seeded_stats_s0.jsonl")
fr = json.load(gzip.open(f"{HERE}/data/func_census_s0.json.gz", "rt")); rows = [r["census"] for r in fr]; ts = np.array([r["t"] for r in fr]); N = 32768
J = len(rows); Lc = 20; win = 20; nb = (J + win - 1) // win
bR, aR = early(rows, Lc); res = {"spontaneous_max_hoe": {s: max(x["hoe"] for x in sp[s]) for s in sp}, "spontaneous_epochs": {s: sp[s][-1]["t"] for s in sp}}
fig, ax = plt.subplots(2, 3, figsize=(17, 8.5))
for s in sp: ax[0, 0].plot([x["t"] for x in sp[s]], [x["hoe"] for x in sp[s]], label=f"spontaneous seed {s}")
ax[0, 0].plot([x["t"] for x in sd], [x["hoe"] for x in sd], label="32 planted replicators", c="C3"); ax[0, 0].legend(fontsize=8)
ax[0, 0].set_title("high-order entropy (H0 - zlib bits/byte), soup 2^17 / 2^15"); ax[0, 0].set_xlabel("epoch")
a = ax[0, 1]; a.plot([x["t"] for x in sd], [x["exact_P"] for x in sd], c="C3", label="exact planted tape")
a.plot([x["t"] for x in sd], [x["mean_steps"] for x in sd], c="k", label="mean instructions per interaction"); a.set_yscale("log"); a.legend(fontsize=8)
a.set_title("seeded soup: the planted tape is gone by epoch 1000;\nreplicators keep running longer"); a.set_xlabel("epoch")
top1 = [max(r.values()) / N for r in rows]; npres = [len(r) for r in rows]
a = ax[0, 2]; a.plot(ts, top1, c="C0"); a.set_ylabel("share of the commonest functional kind", color="C0"); a2 = a.twinx(); a2.plot(ts, npres, c="C1"); a2.set_ylabel("functional kinds with >= 3 tapes", color="C1")
a.set_title("functional kinds (executed instructions only)"); a.set_xlabel("epoch")
ids = {}; seq = []
for r in rows[::win]:
    g = max(r, key=r.get); seq.append(ids.setdefault(g, len(ids)))
ax[1, 0].step(ts[::win], seq, where="post"); ax[1, 0].set_title("identity of the commonest functional kind per 1000 epochs\n(0 = first; a new id = a kind never on top before)"); ax[1, 0].set_xlabel("epoch")
res.update(top1_functional_share_per_1000=np.round(top1[::win], 3).tolist(), functional_kinds_present_per_1000=npres[::win], top1_id_sequence=seq,
           functional_kinds_total=len(bR), replicating_share_last=fr[-1]["replicating_share"], executed_bytes_first_last=[fr[0]["mean_executed"], fr[-1]["mean_executed"]])
for i, g in enumerate((25, 50)):
    shs = [early(census_shadow(rows, q, g=g), Lc) for q in range(8)]
    pool = np.concatenate([[v for k, v in A.items() if B[k] >= 1 and B[k] + Lc < J] for B, A in shs])
    ast = float(np.percentile(pool, 99.0))
    real = sig_per_window(bR, aR, ast, win, nb, Lc, J); env = np.array([sig_per_window(B, A, ast, win, nb, Lc, J) for B, A in shs])
    x = (np.arange(nb) + 0.5) * 1000; a = ax[1, 1 + i]; k = nb - 1
    a.plot(x[:k], real[:k], "o-", c="C3", label="real"); a.plot(x[:k], env.mean(0)[:k], "k--", label="shadow mean (8)"); a.fill_between(x[:k], env.min(0)[:k], env.max(0)[:k], color="k", alpha=0.15, label="shadow range")
    a.set_title(f"new functional kinds reaching a*={ast:.0f} tape-censuses\nwithin 1000 epochs; census shadow with g={g} WF generations/census"); a.legend(fontsize=8); a.set_xlabel("epoch of birth")
    res[f"cohort_g{g}"] = dict(astar=ast, real=real.tolist(), shadow_mean=env.mean(0).round(2).tolist(), shadow_max=env.max(0).tolist())
plt.tight_layout(); plt.savefig(f"{HERE}/bff_o.png", dpi=70)
json.dump(res, open(f"{HERE}/results.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if not k.startswith("cohort")})[:600])
