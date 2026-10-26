"""O analysis of coev runs with c30's o_measure: kinds = 2-D trait bins of width w/2, per species.
usage: analyze.py tag seed [twin_tag]   (twin: the in-world neutral twin with the same seed)"""
import sys, json, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "20261026T0052-c30-o-measure-tool"))
import o_measure as om
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

WIN = int(os.environ.get("WIN", 10000)); LC = int(os.environ.get("LC", 10000)); NSH = int(os.environ.get("NSH", 8))


def load(tag, seed):
    d = np.load(f"data/{tag}_s{seed}.npz"); m = json.load(open(f"data/{tag}_s{seed}.json"))
    return d["log"].astype(np.float64), d["rec"], m


def kinds_of(tr, bw):
    kx = np.floor(tr[:, 0] / bw).astype(np.int64); ky = np.floor(tr[:, 1] / bw).astype(np.int64)
    return (kx + 100000) * 1000000 + (ky + 100000)


def species(log, sp, n0, bw, T):
    b = log[(log[:, 1] == sp) & (log[:, 2] == 1)]; d = log[(log[:, 1] == sp) & (log[:, 2] != 1)]
    t = b[:, 0].astype(np.int64); k = kinds_of(b[:, 5:7], bw); k0 = kinds_of(np.zeros((1, 2)), bw)[0]
    seen = {k0}; innov = np.zeros(len(k), bool)
    for i, kk in enumerate(k):
        if kk not in seen: innov[i] = True; seen.add(kk)
    return dict(t=t, k=k, innov=innov, dt=d[:, 0].astype(np.int64), k0=k0, n0=n0, tr=b[:, 5:7], ids=b[:, 3], dids=d[:, 3])


def o_stats(S, T, tw=None):
    sh = [om.rb_shadow(S["t"], S["innov"], S["dt"], n0=[S["k0"]] * S["n0"], seed=q) for q in range(NSH)]
    ast = max(om.calibrate_astar(a, b, LC, 99.9, t0=WIN) for a, b in sh[:3])
    real = om.cohort(S["t"], S["k"], T, ast, LC, WIN)["sig"]
    env = [om.cohort(a, b, T, ast, LC, WIN)["sig"] for a, b in sh]
    ov = om.top_overlap(S["t"], S["k"], T, WIN, 20)
    out = dict(astar=ast, sig=real, shadow_sig=env, shadow_max=np.max(env, 0).tolist(), top_first=ov["first"], top_prev=ov["prev"],
               births=len(S["t"]), innovations=int(S["innov"].sum()))
    if tw is not None:
        out["twin_sig"] = om.cohort(tw["t"], tw["k"], T, ast, LC, WIN)["sig"]
        twsh = [om.rb_shadow(tw["t"], tw["innov"], tw["dt"], n0=[tw["k0"]] * tw["n0"], seed=q) for q in range(NSH)]
        out["twin_shadow_max"] = np.max([om.cohort(a, b, T, ast, LC, WIN)["sig"] for a, b in twsh], 0).tolist()
        out["twin_innovations"] = int(tw["innov"].sum())
    # revisits: share of each window's births whose bin was first entered >= 2 windows earlier
    first = {}
    for tt, kk in zip(S["t"], S["k"]): first.setdefault(kk, tt)
    fk = np.array([first[kk] for kk in S["k"]]); w = S["t"] // WIN
    out["old_bin_share"] = [float(np.mean(fk[w == i] < (i - 1) * WIN)) if (w == i).any() else None for i in range(T // WIN)]
    return out


def alive_at(S, n0ids, times):
    """Trait clouds of the living population at the given times (from the birth/death log)."""
    born = dict(zip(S["ids"], S["t"])); dead = dict(zip(S["dids"], S["dt"])); trait = dict(zip(S["ids"], map(tuple, S["tr"])))
    for i in n0ids: born[i] = -1; trait[i] = (0.0, 0.0)
    ids = np.array(list(born)); bt = np.array([born[i] for i in ids]); dt = np.array([dead.get(i, 10 ** 12) for i in ids])
    tr = np.array([trait[i] for i in ids])
    return [tr[(bt <= t) & (dt > t)] for t in times]


def main():
    tag, seed = sys.argv[1], int(sys.argv[2]); twin = sys.argv[3] if len(sys.argv) > 3 else None
    log, rec, m = load(tag, seed); p = m["prm"]; bw = p["w"] * float(os.environ.get("BWF", 0.5)); T = int(m["t_end"]) // WIN * WIN
    Np0, Nq0 = p["Np0"], p["Nq0"]
    res = dict(tag=tag, seed=seed, T=T, win=WIN, Lc=LC, bin=bw, mean_success=m["mean_success"])
    sps = {}
    for sp, n0 in ((0, Np0), (1, Nq0)):
        S = species(log, sp, n0, bw, T); sps[sp] = S
        tw = None
        if twin:
            tl, _, tm = load(twin, seed); tw = species(tl, sp, n0, bw, T)
        if len(S["t"]) < 10: continue
        res["prey" if sp == 0 else "pred"] = o_stats(S, T, tw)
    gens = {}
    for sp, nm in ((0, "prey"), (1, "pred")):
        N = rec[:, 1 + sp].mean()
        gens[nm] = float(len(sps[sp]["t"]) / max(N, 1))  # births per mean head = generations
    res["generations"] = gens
    res["pred_extinct_t"] = float(rec[np.argmax(rec[:, 2] == 0), 0]) if (rec[:, 2] == 0).any() else None
    json.dump(res, open(f"data/{tag}_s{seed}_o{os.environ.get("SUF", "")}.json", "w"), indent=1)
    # figure
    times = np.linspace(0, T - 1, 6).astype(int)
    cp = alive_at(sps[0], range(Np0), times); cq = alive_at(sps[1], range(Np0, Np0 + Nq0), times)
    fig = plt.figure(figsize=(18, 9))
    allp = np.concatenate([c for c in cp + cq if len(c)]); lim = np.abs(allp).max() * 1.05 + 0.5
    for j, t in enumerate(times):
        ax = fig.add_subplot(2, 6, j + 1)
        if len(cp[j]): ax.scatter(cp[j][:, 0], cp[j][:, 1], s=2, c="tab:blue", alpha=.4, label="prey")
        if len(cq[j]): ax.scatter(cq[j][:, 0], cq[j][:, 1], s=8, c="tab:red", alpha=.7, label="predator")
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect("equal"); ax.set_title(f"t={t}  prey {len(cp[j])} pred {len(cq[j])}", fontsize=9)
        if j == 0: ax.legend(fontsize=7, loc="upper left")
    ax = fig.add_subplot(2, 4, 5)
    ax.scatter(rec[:, 3], rec[:, 4], c=rec[:, 0], s=2, cmap="Blues"); al = rec[:, 2] > 0
    ax.scatter(rec[al, 5], rec[al, 6], c=rec[al, 0], s=2, cmap="Reds"); ax.set_aspect("equal"); ax.set_title("mean trait path (dark = late)", fontsize=9)
    ax = fig.add_subplot(2, 4, 6); ax.plot(rec[:, 0], rec[:, 1], label="prey"); ax.plot(rec[:, 0], rec[:, 2], label="pred"); ax.legend(fontsize=7); ax.set_title("population", fontsize=9)
    ax = fig.add_subplot(2, 4, 7); x = np.arange(T // WIN) * WIN
    for nm, c in (("prey", "tab:blue"), ("pred", "tab:red")):
        if nm not in res: continue
        r = res[nm]; ax.plot(x, r["sig"], "-o", c=c, ms=3, label=f"{nm} real")
        ax.plot(x, r["shadow_max"], "--", c=c, label=f"{nm} shadow max ({NSH})")
        if "twin_sig" in r: ax.plot(x, r["twin_sig"], ":", c=c, lw=2, label=f"{nm} neutral twin")
    ax.set_title(f"cohort novelty per {WIN} (a* from shadow, Lc={LC})", fontsize=9); ax.legend(fontsize=6)
    ax = fig.add_subplot(2, 4, 8)
    for nm, c in (("prey", "tab:blue"), ("pred", "tab:red")):
        if nm in res: ax.plot(x, res[nm]["top_first"], c=c, label=f"{nm} top-20 overlap w/ first"); ax.plot(x, res[nm]["old_bin_share"], ":", c=c, label=f"{nm} births into old bins")
    ax.set_ylim(-.05, 1.05); ax.legend(fontsize=6); ax.set_title("replacement / revisits", fontsize=9)
    fig.suptitle(f"coev {tag} seed {seed}: {json.dumps({k: p[k] for k in ('S', 'eps', 'w', 'sig_p', 'sig_q', 'neutral')})}", fontsize=10)
    fig.tight_layout(); fig.savefig(f"data/{tag}_s{seed}_o{os.environ.get("SUF", "")}.png", dpi=80)
    for nm in ("prey", "pred"):
        if nm in res:
            r = res[nm]; print(nm, "a*", r["astar"], "innov", r["innovations"], "\n real", r["sig"], "\n shmax", r["shadow_max"],
                               ("\n twin " + str(r["twin_sig"]) + "\n twshmax " + str(r["twin_shadow_max"])) if "twin_sig" in r else "",
                               "\n top_first", np.round(r["top_first"], 2).tolist(), "\n oldbin", [None if v is None else round(v, 2) for v in r["old_bin_share"]])
    print("gens", gens, "pred extinct", res["pred_extinct_t"])


if __name__ == "__main__":
    main()
