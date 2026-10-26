"""python run.py TAG T PARAMS_JSON SEEDS... : runs the complex world, writes runs/TAG_sS.json with
cohort new kinds (born in a 1000-step window, reaching a* replications within 1000 steps), top-20
overlap, kind counts, population, mean size; and runs/TAG_sS.npz with the replication log."""
import sys, os, time, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import world
tag, T = sys.argv[1], int(sys.argv[2]); p = json.loads(sys.argv[3]); seeds = [int(s) for s in sys.argv[4:]]
os.makedirs(f"{HERE}/runs", exist_ok=True)

def cohort(t, k, T, astar=50, Lc=1000, win=1000, topk=20):
    o = np.argsort(t, kind="stable"); t = t[o].astype(np.int64); k = k[o]
    u, fi, inv = np.unique(k, return_index=True, return_inverse=True)
    idx = np.argsort(inv, kind="stable"); g = inv[idx]; starts = np.r_[0, np.flatnonzero(np.diff(g)) + 1]
    cc = np.empty(len(g), np.int64); cc[idx] = np.arange(len(g)) - np.repeat(starts, np.diff(np.r_[starts, len(g)]))
    run_a = cc + 1; birth = t[fi]; nb = T // win
    hit = run_a == astar; th = t[hit]; bh = birth[inv[hit]]; ok = (th - bh) <= Lc
    coh = np.bincount(bh[ok] // win, minlength=nb)[:nb]
    newk = np.bincount(t[run_a == 1] // win, minlength=nb)[:nb]
    tops = []
    for b in range(nb):
        s = (t >= b * win) & (t < (b + 1) * win)
        if not s.any(): tops.append(set()); continue
        uu, c = np.unique(k[s], return_counts=True); tops.append(set(uu[np.argsort(-c)[:topk]].tolist()))
    return dict(cohort=coh.tolist(), new_kinds=newk.tolist(), ov=[len(tops[0] & x) / topk for x in tops],
                ovp=[1.0] + [len(tops[i - 1] & tops[i]) / topk for i in range(1, nb)])

for s in seeds:
    t0 = time.time(); S = world.init(s, p=p); topshare = []; phen = []
    for t in range(T):
        world.step(S)
        if (t + 1) % 100 == 0 and S["n"] and "feat" in S:
            n = S["n"]; cm = S["comp"][:n]; msk = np.arange(cm.shape[1])[None, :] < S["ln"][:n, None]
            ph = (S["feat"][cm] * msk[..., None]).sum(1) / S["ln"][:n, None]
            phen.append(ph.mean(0).round(3).tolist())
        if (t + 1) % 1000 == 0 and S["n"]:
            u, c = np.unique(S["key"][:S["n"]], return_counts=True); topshare.append(round(float(c.max() / S["n"]), 3))
    L = world.logs(S)
    if L["pop"][-1] == 0:
        print(tag, s, "extinct", int(np.argmax(L["pop"] == 0)), flush=True); continue
    r = cohort(L["rep_t"], L["rep_k"], T)
    r.update(tag=tag, seed=s, p=p, pop_mean=float(L["pop"][T // 2:].mean()), reps=int(len(L["rep_t"])), uniq=int(len(np.unique(L["rep_k"]))),
             msize=[round(float(v), 2) for v in L["msize"][999::1000]], topshare=topshare, phen=phen, secs=round(time.time() - t0))
    json.dump(r, open(f"{HERE}/runs/{tag}_s{s}.json", "w"))
    np.savez_compressed(f"{HERE}/runs/{tag}_s{s}.npz", rep_t=L["rep_t"], rep_k=L["rep_k"], rep_s=L["rep_s"], pop=L["pop"], msize=L["msize"])
    print(tag, s, f"{r['secs']}s pop={r['pop_mean']:.0f} uniq={r['uniq']} late_cohort={sum(r['cohort'][2:])} cohort={r['cohort'][:10]} ov_end={r['ov'][-1]} top={topshare[::2]} msize={r['msize'][::2]}", flush=True)
