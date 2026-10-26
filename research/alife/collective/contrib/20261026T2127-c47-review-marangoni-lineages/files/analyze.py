"""Persistence of the swim-far trait in lineages of the Marangoni rods. Reads tables/*.json from extract.py.
Traits are detrended in time within each run (leave-one-out Gaussian kernel, bandwidth 15 frames, on the track's
mid-life frame; early-window traits on start+7, late-window traits on end-7), so that the run-wide rise and fall of
swimming does not masquerade as resemblance. usage: analyze.py out.txt table1.json [table2.json ...]"""
import sys, json, numpy as np
from collections import Counter, defaultdict
from scipy import stats as SS

rng = np.random.default_rng(12345)
NB = 4000; NNULL = 1000; BW = 15.0
out = open(sys.argv[1], "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.write(s + "\n")

runs = [json.load(open(f)) for f in sys.argv[2:]]
R = {}
for d in runs:
    for r in d["rows"]:
        r["T"] = d["T"]; R[(r["run"], r["id"])] = r
rows = list(R.values())
key = lambda r: (r["run"], r["id"])
par = lambda r: R[(r["run"], r["parents"][0])] if r["birth"] == "split" and len(r["parents"]) == 1 else None
fin = lambda r, f: r.get(f) is not None and np.isfinite(r[f])
DIV = [r for r in rows if r["dividing"]]                                            # strict dividing tracks
SB = [r for r in rows if r["birth"] == "split" and r["n"] >= 16 and "v_early" in r]  # split-born, early window full
PS = [r for r in rows if r["n"] >= 10 and r["fate"] in ("divides", "split-other") and "v_late" in r]  # parents ending in a split
tmid = lambda r: (r["start"] + r["end"]) / 2
tearly = lambda r: r["start"] + 7
tlate = lambda r: r["end"] - 7

def detrend(pool, field, name, tf=tmid):
    by = defaultdict(list)
    for r in pool:
        if fin(r, field): by[r["run"]].append(r)
    for u, L in by.items():
        t = np.array([tf(r) for r in L]); y = np.array([r[field] for r in L])
        for i, r in enumerate(L):
            w = np.exp(-0.5 * ((t - t[i]) / BW) ** 2); w[i] = 0
            r[name] = float(y[i] - (w @ y) / w.sum()) if w.sum() > 1e-6 else float(y[i] - y.mean())

for f in ["disp_rl", "vnet", "vpath", "vnet_rl", "straight"]: detrend(DIV, f, f + "_d")
for f in ["v_early", "vpath_early"]: detrend(SB, f, f + "_e", tearly)
for f in ["vnet", "vpath"]: detrend(SB, f, f + "_s")
for f in ["vnet", "vpath"]: detrend(PS, f, f + "_p")
detrend(PS, "v_late", "v_late_p", tlate)

def ci(a, q=(2.5, 97.5)):
    a = np.asarray(a, float); a = a[np.isfinite(a)]
    return (float(np.percentile(a, q[0])), float(np.percentile(a, q[1]))) if len(a) else (np.nan, np.nan)
def fmt(x, c): return f"{x:+.3f} [{c[0]:+.3f}, {c[1]:+.3f}]"
def slope(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    return float(np.cov(x, y, ddof=0)[0, 1] / np.var(x)) if len(x) >= 3 and np.std(x) > 0 else np.nan
def pear(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    return float(np.corrcoef(x, y)[0, 1]) if len(x) >= 3 and np.std(x) > 0 and np.std(y) > 0 else np.nan
def icc(pairs):
    a = np.array([p[0] for p in pairs] + [p[1] for p in pairs]); b = np.array([p[1] for p in pairs] + [p[0] for p in pairs])
    return pear(a, b)
def cluster_boot(groups, stat):
    vals = []
    for _ in range(NB):
        idx = rng.integers(0, len(groups), len(groups)); vals.append(stat([it for i in idx for it in groups[i]]))
    return ci(vals)
def boot_rho(x, y, nb=2000):
    x, y = np.asarray(x, float), np.asarray(y, float); bs = []
    for _ in range(nb):
        i = rng.integers(0, len(x), len(x)); bs.append(SS.spearmanr(x[i], y[i])[0])
    return SS.spearmanr(x, y)[0], ci(bs)

P("=" * 100)
P("Data:", ", ".join(f"{d['label']} ({d['T']} frames, grid {d['H']}, dx {d['dx']:.3f})" for d in runs))
P("Dividing track = born by a split, ends in a split into >= 2 split-born daughters living >= 20 frames (labkit tracker).")
P("D = net displacement over the cycle / median 4 sqrt(lambda_max) of the track (rod lengths). vnet = net/life, vpath = path/life (units/time; 1 frame = 5 time).")
P(f"Traits detrended in time within run (leave-one-out kernel, bandwidth {BW:.0f} frames).")
P(f"dividing tracks: {len(DIV)}; per run: " + ", ".join(f"{k} {v}" for k, v in sorted(Counter(r['run'] for r in DIV).items())))
Ds = np.array([r["disp_rl"] for r in DIV])
P(f"D: median {np.median(Ds):.2f}, IQR {np.percentile(Ds, 25):.2f}-{np.percentile(Ds, 75):.2f}, max {Ds.max():.2f}; >=3: {int((Ds >= 3).sum())}, >=2.5: {int((Ds >= 2.5).sum())}, >=2: {int((Ds >= 2).sum())} of {len(Ds)}")
P("per run: " + "; ".join(f"{u}: n={sum(1 for r in DIV if r['run'] == u)}, >=3 {sum(1 for r in DIV if r['run'] == u and r['disp_rl'] >= 3)}, best {max(r['disp_rl'] for r in DIV if r['run'] == u):.2f}" for u in sorted(set(r['run'] for r in DIV))))
for r in sorted(DIV, key=lambda r: -r["disp_rl"])[:8]:
    p = par(r)
    P(f"  top: {r['run']} #{r['id']} D {r['disp_rl']:.2f} (L4mean {r['disp_rl_L4mean']:.2f}, Feret {r['disp_rl_F']:.2f}) frames {r['start']}-{r['end']} cycle {r['n']} "
      f"vnet {r['vnet']:.3f} straight {r['straight']:.2f} A_birth {r['A_birth']:.0f} | parent #{p['id']} ({p['birth']}) D {p['disp_rl']:.2f} vnet {p['vnet']:.3f} div {p['dividing']}"
      f" | kids D {[round(R[(r['run'], c)]['disp_rl'], 2) for c in r['lasting']]} fates {[R[(r['run'], c)]['fate'] for c in r['lasting']]}")
cyc = np.array([r["n"] for r in DIV]); P(f"cycle (frames): median {np.median(cyc):.0f}, IQR {np.percentile(cyc, 25):.0f}-{np.percentile(cyc, 75):.0f}, range {cyc.min()}-{cyc.max()}")
P(f"parents of dividing tracks: {dict(Counter(par(r)['birth'] + ('/div' if par(r)['dividing'] else '') for r in DIV))}")

# ================================================================================================ (1)
P("\n" + "=" * 100); P("(1) HERITABILITY")
def po(children, parent_ok, fc, fp):
    fam = defaultdict(list)
    for c in children:
        p = par(c)
        if p is None or not parent_ok(p) or not fin(c, fc) or not fin(p, fp): continue
        fam[key(p)].append((p[fp], c[fc], p, c))
    return list(fam.values())
def po_report(name, fams, null_pool, fp, win=8):
    items = [it for f in fams for it in f]
    if len(items) < 4: P(f"  {name}: n={len(items)} pairs, too few"); return
    x = [i[0] for i in items]; y = [i[1] for i in items]
    b = slope(x, y); r_ = pear(x, y); rs = SS.spearmanr(x, y)[0]
    cb = cluster_boot(fams, lambda it: slope([i[0] for i in it], [i[1] for i in it]))
    cr = cluster_boot(fams, lambda it: pear([i[0] for i in it], [i[1] for i in it]))
    byrun = defaultdict(list)
    for q in null_pool:
        if fin(q, fp): byrun[q["run"]].append(q)
    nulls = []
    for _ in range(NNULL):
        xs, ys = [], []
        for (pv, cv, p, c) in items:
            cand = [q for q in byrun[p["run"]] if q is not p and abs(q["end"] - p["end"]) <= win]
            if cand: xs.append(cand[rng.integers(len(cand))][fp]); ys.append(cv)
        nulls.append(slope(xs, ys))
    pnull = np.mean(np.array(nulls) >= b)
    # space-and-time matched null: unrelated track ending within +-win frames and within RAD units of where the parent divided
    RAD = 40.0
    def near(q, p):
        L = p["Lbox"]; dy = (q["y1"] - p["y1"] + L / 2) % L - L / 2; dxx = (q["x1"] - p["x1"] + L / 2) % L - L / 2
        return np.hypot(dy, dxx) <= RAD
    cands = {}
    for (pv, cv, p, c) in items:
        cands[key(p)] = [q for q in byrun[p["run"]] if q is not p and abs(q["end"] - p["end"]) <= 12 and near(q, p)]
    nulls2 = []
    for _ in range(NNULL):
        xs, ys = [], []
        for (pv, cv, p, c) in items:
            cand = cands[key(p)]
            if cand: xs.append(cand[rng.integers(len(cand))][fp]); ys.append(cv)
        nulls2.append(slope(xs, ys))
    ncov = sum(1 for (pv, cv, p, c) in items if cands[key(p)])
    sub = [(pv, cv) for (pv, cv, p, c) in items if cands[key(p)]]
    bsub = slope([a for a, _ in sub], [b_ for _, b_ in sub])
    ncand = np.median([len(cands[key(p)]) for (pv, cv, p, c) in items if cands[key(p)]]) if ncov else 0
    P(f"  {name}: n={len(items)} offspring of {len(fams)} parents; slope {fmt(b, cb)}, r {fmt(r_, cr)}, Spearman {rs:+.3f}")
    P(f"      null, time-matched: slope {np.nanmean(nulls):+.3f} ({ci(nulls)[0]:+.3f}..{ci(nulls)[1]:+.3f}), P(null >= obs) {pnull:.3f}; "
      f"space+time-matched (+-12 fr, <= {RAD:.0f} units; {ncov}/{len(items)} pairs have one, median {ncand:.0f} candidates): observed on that subset {bsub:+.3f}, null {np.nanmean(nulls2):+.3f} ({ci(nulls2)[0]:+.3f}..{ci(nulls2)[1]:+.3f}), P(null >= obs) {np.mean(np.array(nulls2) >= bsub):.3f}")

P("Parent-offspring regressions (cluster bootstrap over parents; null = parent replaced by a random other track of the same run ending within +-8 frames):")
po_report("D on D, both dividing tracks", po(DIV, lambda p: p["dividing"], "disp_rl_d", "disp_rl_d"), DIV, "disp_rl_d")
po_report("vnet on vnet, both dividing tracks", po(DIV, lambda p: p["dividing"], "vnet_d", "vnet_d"), DIV, "vnet_d")
po_report("child D on parent whole-life vnet (parent: any track >=10 fr ending in a split)", po(DIV, lambda p: p in PS, "disp_rl_d", "vnet_p"), PS, "vnet_p")
po_report("broad: child whole-life vnet on parent whole-life vnet (child split-born >=16 fr, any fate)", po(SB, lambda p: p in PS, "vnet_s", "vnet_p"), PS, "vnet_p")
po_report("broad: child whole-life vpath on parent whole-life vpath", po(SB, lambda p: p in PS, "vpath_s", "vpath_p"), PS, "vpath_p")
po_report("carry-over: child early speed (first 15 fr) on parent late speed (last 15 fr)", po(SB, lambda p: p in PS, "v_early_e", "v_late_p"), PS, "v_late_p")
po_report("broad vnet, leading-side daughters only", po([c for c in SB if c.get("front", 0) > 0], lambda p: p in PS, "vnet_s", "vnet_p"), PS, "vnet_p")
po_report("broad vnet, trailing-side daughters only", po([c for c in SB if "front" in c and c["front"] <= 0], lambda p: p in PS, "vnet_s", "vnet_p"), PS, "vnet_p")
po_report("carry-over, leading-side daughters only", po([c for c in SB if c.get("front", 0) > 0], lambda p: p in PS, "v_early_e", "v_late_p"), PS, "v_late_p")

P("Sister-sister intraclass correlation (double-entry; bootstrap over pairs; null = unrelated pairs born within +-3 frames, same run):")
def sis_report(name, pool, f, win=3):
    fam = defaultdict(list)
    for c in pool:
        p = par(c)
        if p is not None and fin(c, f): fam[key(p)].append(c)
    sp = [(g[0], g[1]) for g in fam.values() if len(g) == 2]
    if len(sp) < 4: P(f"  {name}: n={len(sp)} pairs, too few"); return
    r0 = icc([(a[f], b[f]) for a, b in sp])
    bs = [icc([(sp[i][0][f], sp[i][1][f]) for i in rng.integers(0, len(sp), len(sp))]) for _ in range(NB)]
    byrun = defaultdict(list)
    for q in pool:
        if fin(q, f): byrun[q["run"]].append(q)
    nulls = []
    for _ in range(NNULL):
        pr = []
        for a, b in sp:
            cand = [q for q in byrun[a["run"]] if abs(q["start"] - a["start"]) <= win and q["parents"] != a["parents"]]
            if cand: pr.append((a[f], cand[rng.integers(len(cand))][f]))
        nulls.append(icc(pr) if len(pr) >= 4 else np.nan)
    def near0(q, a, rad=40.0):
        L = a["Lbox"]; dy = (q["y0"] - a["y0"] + L / 2) % L - L / 2; dxx = (q["x0"] - a["x0"] + L / 2) % L - L / 2
        return np.hypot(dy, dxx) <= rad
    cn = {key(a): [q for q in byrun[a["run"]] if abs(q["start"] - a["start"]) <= 6 and q["parents"] != a["parents"] and near0(q, a)] for a, b in sp}
    sub = [(a[f], b[f]) for a, b in sp if cn[key(a)]]
    isub = icc(sub) if len(sub) >= 4 else np.nan
    nulls2 = []
    for _ in range(NNULL):
        pr = [(a[f], cn[key(a)][rng.integers(len(cn[key(a)]))][f]) for a, b in sp if cn[key(a)]]
        nulls2.append(icc(pr) if len(pr) >= 4 else np.nan)
    P(f"  {name}: n={len(sp)} pairs; ICC {fmt(r0, ci(bs))}; null time-matched {np.nanmean(nulls):+.3f} ({ci(nulls)[0]:+.3f}..{ci(nulls)[1]:+.3f}); "
      f"space+time-matched (+-6 fr, <=40 units; {len(sub)} pairs): observed on subset {isub:+.3f}, null {np.nanmean(nulls2):+.3f} ({ci(nulls2)[0]:+.3f}..{ci(nulls2)[1]:+.3f})")
sis_report("D, both sisters dividing", DIV, "disp_rl_d")
sis_report("vnet, both sisters dividing", DIV, "vnet_d")
sis_report("early speed, sisters any fate (>=16 fr)", SB, "v_early_e")
sis_report("whole-life vnet, sisters any fate", SB, "vnet_s")
sis_report("whole-life vpath, sisters any fate", SB, "vpath_s")

P("Top-quartile parents (top 25% of their run's detrended values):")
def topq(children, parents_pool, fp, fc, label):
    q75 = {u: np.percentile([r[fp] for r in parents_pool if r["run"] == u and fin(r, fp)], 75) for u in set(r["run"] for r in parents_pool)}
    qc = {u: np.percentile([r[fc] for r in children if r["run"] == u and fin(r, fc)], 75) for u in set(r["run"] for r in children)}
    ft, fr_ = defaultdict(list), defaultdict(list)
    for c in children:
        p = par(c)
        if p is None or p not in parents_pool or not fin(c, fc) or not fin(p, fp): continue
        (ft if p[fp] >= q75[p["run"]] else fr_)[key(p)].append(c)
    gt, gr = list(ft.values()), list(fr_.values())
    if not gt or not gr: P(f"  {label}: too few"); return
    kt = [c for g in gt for c in g]; kr = [c for g in gr for c in g]
    allc = [c[fc] for c in children if fin(c, fc)]
    mt, mr, ma = np.mean([c[fc] for c in kt]), np.mean([c[fc] for c in kr]), np.mean(allc)
    bs = []
    for _ in range(NB):
        a = [c[fc] for i in rng.integers(0, len(gt), len(gt)) for c in gt[i]]; b = [c[fc] for i in rng.integers(0, len(gr), len(gr)) for c in gr[i]]
        bs.append((np.mean(a) - ma, np.mean(a) - np.mean(b)))
    bs = np.array(bs)
    P(f"  {label}: children of top-quartile parents n={len(kt)} ({len(gt)} parents): mean minus population {fmt(mt - ma, ci(bs[:, 0]))}; "
      f"minus children of other parents (n={len(kr)}) {fmt(mt - mr, ci(bs[:, 1]))}; population SD {np.std(allc):.3f}; "
      f"children in top quartile: {sum(c[fc] >= qc[c['run']] for c in kt)}/{len(kt)} vs {sum(c[fc] >= qc[c['run']] for c in kr)}/{len(kr)}")
topq(DIV, DIV, "disp_rl_d", "disp_rl_d", "D -> D (dividing parents and children)")
topq(DIV, PS, "vnet_p", "disp_rl_d", "parent vnet -> child D")
topq(SB, PS, "vnet_p", "vnet_s", "parent vnet -> child vnet (broad)")
topq(SB, PS, "v_late_p", "v_early_e", "parent late speed -> child early speed (broad)")

P("Lineages (grandparent -> parent -> child):")
def chains(children, ok):
    out_ = []
    for c in children:
        p = par(c)
        if p is None or not ok(p): continue
        g = par(p)
        if g is None or not ok(g): continue
        out_.append((g, p, c))
    return out_
ch = chains(DIV, lambda p: p["dividing"])
P(f"  all three dividing tracks: {len(ch)} chains")
for g, p, c in ch: P(f"   {c['run']}: #{g['id']} D {g['disp_rl']:.2f} -> #{p['id']} {p['disp_rl']:.2f} -> #{c['id']} {c['disp_rl']:.2f}")
if len(ch) >= 4:
    P(f"  r(grandparent D, grandchild D) {pear([g['disp_rl_d'] for g, p, c in ch], [c['disp_rl_d'] for g, p, c in ch]):+.3f}")
chb = chains([r for r in SB if fin(r, "vnet_s")], lambda p: p in PS and fin(p, "vnet_p"))
if len(chb) >= 6:
    gx = np.array([g["vnet_p"] for g, p, c in chb]); px_ = np.array([p["vnet_p"] for g, p, c in chb]); cx_ = np.array([c["vnet_s"] for g, p, c in chb])
    bs = []
    for _ in range(NB):
        i = rng.integers(0, len(chb), len(chb)); bs.append(pear(gx[i], cx_[i]))
    P(f"  broad (vnet, grandparent and parent: tracks ending in a split; child: split-born >=16 fr): {len(chb)} chains; r(GP, C) {fmt(pear(gx, cx_), ci(bs))}; r(P, C) {pear(px_, cx_):+.3f}; r(GP, P) {pear(gx, px_):+.3f}")
for side, okc in [("leading", lambda c: c.get("front", 0) > 0), ("trailing", lambda c: "front" in c and c["front"] <= 0)]:
    cs = [(g, p, c) for g, p, c in chb if okc(c) and okc(p)]
    if len(cs) >= 6:
        gx = np.array([g["vnet_p"] for g, p, c in cs]); px_ = np.array([p["vnet_p"] for g, p, c in cs]); cx_ = np.array([c["vnet_s"] for g, p, c in cs])
        bs = []
        for _ in range(NB):
            i = rng.integers(0, len(cs), len(cs)); bs.append(pear(gx[i], cx_[i]))
        P(f"  {side}-daughter lines (P {side} daughter of GP, C {side} daughter of P): {len(cs)} chains; r(GP, C) {fmt(pear(gx, cx_), ci(bs))}; r(P, C) {pear(px_, cx_):+.3f}; r(GP, P) {pear(gx, px_):+.3f}")
    else: P(f"  {side}-daughter lines: {len(cs)} chains, too few")
def gen(r):
    k = 0
    while True:
        p = par(r)
        if p is None: return k
        k += 1; r = p
P("  D by generation (split ancestors): " + ", ".join(f"gen {g}: median {np.median([r['disp_rl'] for r in DIV if gen(r) == g]):.2f} (n={sum(1 for r in DIV if gen(r) == g)})" for g in sorted(set(gen(r) for r in DIV))))

P("Carry-over at fission (direction, side):")
cpa = [c["cos_parent"] for c in SB if "cos_parent" in c]
P(f"  cos(parent travel, daughter travel), split-born >=16 fr: mean {np.mean(cpa):+.2f}, share > 0 {np.mean(np.array(cpa) > 0):.2f} (n={len(cpa)})")
fr = [c for c in SB if "front" in c and fin(c, "v_early_e")]
f1 = [c["v_early_e"] for c in fr if c["front"] > 0]; f0 = [c["v_early_e"] for c in fr if c["front"] <= 0]
bs = [np.mean(rng.choice(f1, len(f1))) - np.mean(rng.choice(f0, len(f0))) for _ in range(NB)]
P(f"  early speed, daughter on parent's leading side minus trailing side: {fmt(np.mean(f1) - np.mean(f0), ci(bs))} (n={len(f1)} vs {len(f0)}; SD {np.std(f1 + f0):.3f})")
P(f"  cos(parent, daughter): leading {np.mean([c['cos_parent'] for c in fr if c['front'] > 0 and 'cos_parent' in c]):+.2f}, trailing {np.mean([c['cos_parent'] for c in fr if c['front'] <= 0 and 'cos_parent' in c]):+.2f}")
P(f"  fates leading: {dict(Counter(c['fate'] for c in fr if c['front'] > 0))}; trailing: {dict(Counter(c['fate'] for c in fr if c['front'] <= 0))}")
# within sister pairs: does the leading sister win?
fam = defaultdict(list)
for c in fr: fam[key(par(c))].append(c)
pairs = [g for g in fam.values() if len(g) == 2 and (g[0]["front"] > 0) != (g[1]["front"] > 0)]
lead_faster = sum(1 for g in pairs if max(g, key=lambda c: c["front"])["v_early"] > min(g, key=lambda c: c["front"])["v_early"])
P(f"  sister pairs split leading/trailing: {len(pairs)}; leading sister faster in {lead_faster} (binomial p {SS.binomtest(lead_faster, len(pairs)).pvalue:.3f})")
P("Determinants of daughter early speed (split-born >=16 fr; Spearman with detrended early speed):")
for f in ["front", "A_birth", "L_birth", "crowd_birth", "cos_parent"]:
    xy = [(c[f], c["v_early_e"]) for c in SB if fin(c, f) and fin(c, "v_early_e")]
    x, y = zip(*xy); rho, cc = boot_rho(x, y); P(f"  {f:12s} rho {fmt(rho, cc)} n={len(x)}")
xy = [(par(c)["v_late_p"], c["v_early_e"]) for c in SB if par(c) is not None and fin(par(c), "v_late_p") and fin(c, "v_early_e")]
x, y = zip(*xy); rho, cc = boot_rho(x, y); P(f"  parent late speed rho {fmt(rho, cc)} n={len(x)}")
d1 = [c["disp_rl"] for c in DIV if "front" in c and c["front"] > 0]; d0 = [c["disp_rl"] for c in DIV if "front" in c and c["front"] <= 0]
P(f"  dividing tracks: D of leading-side daughters median {np.median(d1):.2f} (n={len(d1)}) vs trailing {np.median(d0):.2f} (n={len(d0)}); Mann-Whitney p {SS.mannwhitneyu(d1, d0).pvalue:.3f}")
P("Does swimming feed growth? early speed vs relative area gain over the same first 15 frames (split-born living >= 30 fr, so no division in the window):")
G = [r for r in SB if r["n"] >= 30 and fin(r, "A_k") and r["A_0"] > 0]
detrend(G, "v_early", "v_early_g", tearly)
for r in G: r["g15"] = np.log(r["A_k"] / r["A_0"])
detrend(G, "g15", "g15_d", tearly)
x = [r["v_early_g"] for r in G]; y = [r["g15_d"] for r in G]; rho, cc = boot_rho(x, y)
P(f"  Spearman(detrended early speed, detrended log area gain) {fmt(rho, cc)} n={len(G)}")
G2 = [r for r in SB if r["dividing"] and fin(r, "A_k") and r["A_0"] > 0 and r["n"] >= 22]
if len(G2) > 8:
    x = [r["v_early"] for r in G2]; y = [np.log(r["A_k"] / r["A_0"]) for r in G2]; rho, cc = boot_rho(x, y)
    P(f"  dividing tracks with cycle >= 22 fr: Spearman(early speed, log area gain over the first 15 fr) {fmt(rho, cc)} n={len(G2)}")

# ================================================================================================ (2)
P("\n" + "=" * 100); P("(2) DETERMINANTS of D among dividing tracks (Spearman; values centred on their run mean, time not removed)")
preds = ["n", "A_birth", "L_birth", "L4med", "A_end", "ring_s", "ring_contrast", "ring_pol_rl", "crowd", "crowd_birth", "nnd", "ncomp_birth",
         "start", "cy", "cx", "straight", "vpath", "vnet", "cos_axis"]
def rcentre(pool, f, name):
    mu = {u: np.mean([r[f] for r in pool if r["run"] == u and fin(r, f)]) for u in set(r["run"] for r in pool)}
    for r in pool:
        if fin(r, f): r[name] = r[f] - mu[r["run"]]
for f in preds + ["disp_rl"]: rcentre(DIV, f, f + "_c")
for f in preds:
    xy = [(r[f + "_c"], r["disp_rl_c"]) for r in DIV if fin(r, f + "_c")]
    if len(xy) < 6: continue
    x, y = zip(*xy); rho, cc = boot_rho(x, y); P(f"  D vs {f:14s} rho {fmt(rho, cc)} n={len(x)}")
P("Decomposition: log D = log straightness + log path speed + log (cycle-1) - log rod length (+const), run-centred;")
P("share_k = cov(log D, component_k) / var(log D), shares sum to 1:")
comp = defaultdict(list)
for r in DIV:
    comp["logD"].append(np.log(r["disp_rl"])); comp["straight"].append(np.log(r["straight"])); comp["vpath"].append(np.log(r["vpath"]))
    comp["cycle"].append(np.log(r["n"] - 1)); comp["-L"].append(-np.log(r["L4med"])); comp["run"].append(r["run"])
ru = np.array(comp["run"])
def rc(a):
    a = np.array(a, float).copy()
    for u in set(ru): a[ru == u] -= a[ru == u].mean()
    return a
LD = rc(comp["logD"]); parts = {k: rc(comp[k]) for k in ["straight", "vpath", "cycle", "-L"]}
def shares(i):
    v = np.var(LD[i]); return {k: np.cov(LD[i], parts[k][i], ddof=0)[0, 1] / v for k in parts}
s0 = shares(np.arange(len(LD))); bsh = [shares(rng.integers(0, len(LD), len(LD))) for _ in range(NB)]
for k in parts: P(f"  {k:9s}: {fmt(s0[k], ci([b[k] for b in bsh]))}")
P(f"  n={len(LD)}; Spearman(cycle, path speed) {SS.spearmanr([r['n'] for r in DIV], [r['vpath'] for r in DIV])[0]:+.3f}, "
  f"(cycle, straightness) {SS.spearmanr([r['n'] for r in DIV], [r['straight'] for r in DIV])[0]:+.3f}, (cycle, net speed) {SS.spearmanr([r['n'] for r in DIV], [r['vnet'] for r in DIV])[0]:+.3f}, "
  f"(cycle, D) {SS.spearmanr([r['n'] for r in DIV], [r['disp_rl'] for r in DIV])[0]:+.3f}")
lc = [r for r in DIV if r["n"] > np.median(cyc)]; sc = [r for r in DIV if r["n"] <= np.median(cyc)]
P(f"  cycle > median ({np.median(cyc):.0f} fr): n={len(lc)}, median D {np.median([r['disp_rl'] for r in lc]):.2f}, >=2: {sum(r['disp_rl'] >= 2 for r in lc)}, >=2.5: {sum(r['disp_rl'] >= 2.5 for r in lc)}, >=3: {sum(r['disp_rl'] >= 3 for r in lc)}; "
  f"cycle <= median: n={len(sc)}, median D {np.median([r['disp_rl'] for r in sc]):.2f}, >=2: {sum(r['disp_rl'] >= 2 for r in sc)}, >=2.5: {sum(r['disp_rl'] >= 2.5 for r in sc)}, >=3: {sum(r['disp_rl'] >= 3 for r in sc)}")
def pct(r, f): v = [q[f] for q in DIV if q["run"] == r["run"] and fin(q, f)]; return 100 * np.mean(np.array(v) <= r[f])
P("  top D tracks, within-run percentiles:")
for r in sorted(DIV, key=lambda r: -r["disp_rl"])[:max(4, len(DIV) // 12)]:
    P(f"   {r['run']} #{r['id']} D {r['disp_rl']:.2f}: cycle {r['n']} (pct {pct(r, 'n'):.0f}), vpath pct {pct(r, 'vpath'):.0f}, straight {r['straight']:.2f} (pct {pct(r, 'straight'):.0f}), "
      f"A_birth pct {pct(r, 'A_birth'):.0f}, L4med pct {pct(r, 'L4med'):.0f}, crowd pct {pct(r, 'crowd'):.0f}, ring_pol pct {pct(r, 'ring_pol_rl'):.0f}, born frame {r['start']}")
X_names = ["n", "A_birth", "ring_s", "ring_pol_rl", "crowd", "start"]
ok = [r for r in DIV if all(fin(r, f + "_c") for f in X_names)]
X = np.array([[r[f + "_c"] for f in X_names] for r in ok]); y = np.array([r["disp_rl_c"] for r in ok])
X = (X - X.mean(0)) / X.std(0); yz = (y - y.mean()) / y.std()
def fit(i): A = np.c_[np.ones(len(i)), X[i]]; return np.linalg.lstsq(A, yz[i], rcond=None)[0][1:]
b0 = fit(np.arange(len(ok))); bb = np.array([fit(rng.integers(0, len(ok), len(ok))) for _ in range(NB)])
A = np.c_[np.ones(len(ok)), X]; res = yz - A @ np.linalg.lstsq(A, yz, rcond=None)[0]
P(f"  multiple regression of D (z) on standardised run-centred predictors, n={len(ok)}, R^2={1 - res.var() / yz.var():.2f}:")
for j, f in enumerate(X_names): P(f"    {f:12s} beta {fmt(b0[j], ci(bb[:, j]))}")
P(f"  ring polarity (s-weighted band centroid along travel / rod length; negative = surfactant at the rear): median {np.median([r['ring_pol_rl'] for r in DIV]):+.3f}, "
  f"share negative {np.mean([r['ring_pol_rl'] < 0 for r in DIV]):.2f}; within-track frame correlation polarity vs speed median {np.nanmedian([r.get('ring_pol_speed_corr', np.nan) for r in DIV]):+.2f}")

# ================================================================================================ (3)
P("\n" + "=" * 100); P("(3) FITNESS")
x = [r["vnet_d"] for r in DIV]; y = [r["n"] for r in DIV]; rho, cc = boot_rho(x, y)
P(f"  dividing tracks: Spearman(net speed detrended, cycle) {fmt(rho, cc)} n={len(x)}")
x = [r["vpath_d"] for r in DIV]; rho, cc = boot_rho(x, y); P(f"  dividing tracks: Spearman(path speed detrended, cycle) {fmt(rho, cc)}")
x = [r["disp_rl_d"] for r in DIV]; rho, cc = boot_rho(x, y); P(f"  dividing tracks: Spearman(D detrended, cycle) {fmt(rho, cc)}")
P("  Fates of split-born tracks (>=16 fr) by early-speed quartile (first 15 fr; quartiles of detrended early speed within run):")
qs = {u: np.percentile([r["v_early_e"] for r in SB if r["run"] == u], [25, 50, 75]) for u in set(r["run"] for r in SB)}
qq = lambda r: int(np.searchsorted(qs[r["run"]], r["v_early_e"], side="right"))
tab = defaultdict(Counter)
for r in SB: tab[qq(r)][r["fate"]] += 1
fates = ["divides", "merges", "split-other", "vanishes", "run-end"]
P("   quartile " + " ".join(f"{f:>11s}" for f in fates) + "   P(divide|resolved)  P(merge|resolved)")
for q in range(4):
    c = tab[q]; res_ = sum(c[f] for f in fates if f != "run-end")
    P(f"   Q{q + 1}       " + " ".join(f"{c[f]:11d}" for f in fates) + f"   {c['divides'] / max(res_, 1):.2f} ({c['divides']}/{res_})        {c['merges'] / max(res_, 1):.2f} ({c['merges']}/{res_})")
resolved = [r for r in SB if r["fate"] != "run-end"]
for fname in ["divides", "merges"]:
    x = np.array([r["v_early_e"] for r in resolved]); y = np.array([r["fate"] == fname for r in resolved])
    bs = []
    for _ in range(2000):
        i = rng.integers(0, len(x), len(x)); bs.append(SS.pointbiserialr(y[i], x[i])[0])
    P(f"  point-biserial r(early speed, {fname}) among resolved: {fmt(SS.pointbiserialr(y, x)[0], ci(bs))} n={len(x)}")
# avoid overlap of the speed window with the cycle: only tracks living >= 30 frames
res30 = [r for r in resolved if r["n"] >= 30]
x = np.array([r["v_early_e"] for r in res30]); y = np.array([r["fate"] == "divides" for r in res30])
P(f"  same, only tracks living >= 30 fr (speed window ends >= 15 fr before the fate): r(early speed, divides) {SS.pointbiserialr(y, x)[0]:+.3f} n={len(x)}; "
  f"r(early speed, merges) {SS.pointbiserialr(np.array([r['fate'] == 'merges' for r in res30]), x)[0]:+.3f}")
x = [r["v_early_e"] for r in SB]
P(f"  Spearman(early speed, log growth A_end/A_birth): {SS.spearmanr(x, [np.log(r['A_end'] / r['A_birth']) for r in SB])[0]:+.3f}; (early speed, A_birth): {SS.spearmanr(x, [r['A_birth'] for r in SB])[0]:+.3f}; n={len(x)}")
for Hh in (40, 60):
    def alive_desc(r, f):
        stack, cnt = [r], 0
        while stack:
            q = stack.pop()
            if q["start"] > f: continue
            if q["start"] <= f <= q["end"]: cnt += 1; continue
            stack.extend(R[(q["run"], c)] for c in q["children"] if R[(q["run"], c)]["birth"] == "split")
        return cnt
    DD = [(r["v_early_e"], alive_desc(r, r["start"] + Hh), r) for r in SB if r["start"] + Hh <= r["T"] - 1]
    x = [a for a, _, _ in DD]; y = [b for _, b, _ in DD]; rho, cc = boot_rho(x, y)
    P(f"  living split-descendants {Hh} fr after birth vs early speed: Spearman {fmt(rho, cc)} n={len(x)}; by quartile: " +
      ", ".join(f"Q{q + 1} {np.mean([b for a, b, r in DD if qq(r) == q]):.2f} (zero {np.mean([b == 0 for a, b, r in DD if qq(r) == q]):.2f}, n={sum(1 for a, b, r in DD if qq(r) == q)})" for q in range(4)))
FAR = [r for r in rows if r["birth"] == "split" and r["n"] >= 20 and r["disp_rl"] >= 3]
P(f"  split-born tracks (>=20 fr) with whole-life D >= 3: {len(FAR)} (dividing among them: {sum(r['dividing'] for r in FAR)}); fates {dict(Counter(r['fate'] for r in FAR))}; median life {np.median([r['n'] for r in FAR]) if FAR else 0:.0f} fr "
  f"vs dividing {np.median(cyc):.0f}; growth A_end/A_birth {np.median([r['A_end'] / r['A_birth'] for r in FAR]) if FAR else 0:.2f} vs dividing {np.median([r['A_end'] / r['A_birth'] for r in DIV]):.2f}; "
  f"vnet {np.median([r['vnet'] for r in FAR]) if FAR else 0:.3f} vs dividing {np.median([r['vnet'] for r in DIV]):.3f}; born frame median {np.median([r['start'] for r in FAR]) if FAR else 0:.0f} vs dividing {np.median([r['start'] for r in DIV]):.0f}")
for r in sorted(DIV, key=lambda r: -r["disp_rl"])[:6]:
    p = par(r); sis = [R[(r["run"], c)] for c in p["children"] if c != r["id"]]
    kids = [R[(r["run"], c)] for c in r["children"]]
    P(f"   family of {r['run']} #{r['id']} (D {r['disp_rl']:.2f}): parent {p['birth']} D {p['disp_rl']:.2f}; sister(s) " +
      ", ".join(f"#{s['id']} D {s['disp_rl']:.2f} {s['fate']}" for s in sis) + "; daughters " + ", ".join(f"#{k['id']} D {k['disp_rl']:.2f} life {k['n']} {k['fate']}" for k in kids))

# ================================================================================================ (4)
P("\n" + "=" * 100); P("(4) PERSISTENCE OVER TIME (runs of 200 frames; by the frame of division)")
D200 = [r for r in DIV if r["T"] >= 150]
for lo_, hi_ in [(0, 60), (60, 100), (100, 140), (140, 181)]:
    h = [r for r in D200 if lo_ <= r["end"] < hi_]
    if not h: P(f"  divides in frames {lo_}-{hi_ - 1}: n=0"); continue
    d = np.array([r["disp_rl"] for r in h])
    P(f"  divides in frames {lo_:3d}-{hi_ - 1:3d}: n={len(d):3d}, median D {np.median(d):.2f}, >=2: {(d >= 2).sum():2d} ({np.mean(d >= 2):.2f}), >=2.5: {(d >= 2.5).sum()}, >=3: {(d >= 3).sum()}, "
      f"median cycle {np.median([r['n'] for r in h]):.0f}, median vnet {np.median([r['vnet'] for r in h]):.3f}, median straight {np.median([r['straight'] for r in h]):.2f}")
h1 = [r for r in D200 if r["end"] < 100]; h2 = [r for r in D200 if r["end"] >= 100]
a = np.array([r["disp_rl"] for r in h1]); b = np.array([r["disp_rl"] for r in h2])
if len(a) and len(b):
    bs = [np.median(rng.choice(b, len(b))) - np.median(rng.choice(a, len(a))) for _ in range(NB)]
    P(f"  halves by division frame (<100 vs >=100): n {len(a)} vs {len(b)}; median D {np.median(a):.2f} -> {np.median(b):.2f}, difference {fmt(np.median(b) - np.median(a), ci(bs))}; Mann-Whitney p {SS.mannwhitneyu(a, b).pvalue:.3f}")
    for thr in [2.0, 2.5, 3.0]:
        P(f"  fraction >= {thr}: {np.mean(a >= thr):.3f} ({(a >= thr).sum()}/{len(a)}) -> {np.mean(b >= thr):.3f} ({(b >= thr).sum()}/{len(b)}); Fisher p {SS.fisher_exact([[(a >= thr).sum(), (a < thr).sum()], [(b >= thr).sum(), (b < thr).sum()]])[1]:.3f}")
P("  per run (halves by division frame): " + "; ".join(
    f"{u}: {np.median([r['disp_rl'] for r in h1 if r['run'] == u]):.2f} (n={sum(1 for r in h1 if r['run'] == u)}) -> {np.median([r['disp_rl'] for r in h2 if r['run'] == u]) if any(r['run'] == u for r in h2) else float('nan'):.2f} (n={sum(1 for r in h2 if r['run'] == u)})"
    for u in sorted(set(r["run"] for r in D200))))
S200 = [r for r in SB if r["T"] >= 150]
a = [r["v_early"] for r in S200 if r["start"] < 100]; b = [r["v_early"] for r in S200 if r["start"] >= 100]
P(f"  early speed of all split-born (>=16 fr), born before/after frame 100: median {np.median(a):.3f} (n={len(a)}) -> {np.median(b):.3f} (n={len(b)}); Mann-Whitney p {SS.mannwhitneyu(a, b).pvalue:.4f}")
a = [r for r in S200 if r["start"] < 100]; b = [r for r in S200 if r["start"] >= 100]
P(f"  fates of those born before frame 100: {dict(Counter(r['fate'] for r in a))}; after: {dict(Counter(r['fate'] for r in b))}")
out.close()
