"""(c50) Readouts for Q:marangoni-swimmer-spread: the three-kind Marangoni ladder in the sink-disc environment.
usage: spread_stats.py frames.npz world.py table.json metrics.json mut.jsonl label outdir
Bodies and tracks: labkit's own segmentation and tracker (as extract.py). Kind of a body at a rendered frame = argmax_k of
the summed s_k over the body dilated by 2 px (render channels 2-4), purity = that share; a track's kind = majority kind over
its rendered frames. Pre-registered trait: the ladder value of the kind (20/40/60, the arm's MARS in the ladder; in the twin
and drive-off arms the same labels with no effect) averaged over living bodies (purity >= 0.6), per rendered frame.
M gate (PROTOCOL): a dividing track (split-born, >= 2 daughters living >= 20 frames, extract.py) passes if its net
displacement is >= 3 of its own rod lengths (median 4 sqrt(lambda_max), disp_rl) AND its rear tip advances >= 2/3 of the
net displacement (translation, not growth on one side); the sqrt(area) unit (DA = net / sqrt(mean area)) is reported too.
Cohorts: dividing tracks binned by birth frame in windows of one median cycle of the run.
Selection: descendants alive two median cycles after each dividing track's birth, passers vs non-passers of the same kind."""
import sys, json, importlib.util, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR, metrics as M
from scipy import ndimage as ndi
fn, wpath, tabf, metf, mutf, label, outdir = sys.argv[1:8]
LAD = np.array([20.0, 40.0, 60.0])
F = np.load(fn); mat = F["matter"].astype(np.float32); R = F["render"]; rf = [int(x) for x in F["render_f"]]
rindex = {f: i for i, f in enumerate(rf)}
spec = importlib.util.spec_from_file_location("w", wpath); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True); byid = {t["id"]: t for t in tracks}
T = len(comps)
out = []
def P(s): print(s); out.append(s)


def kind_of(f, comp):
    i = rindex.get(f)
    if i is None: return None
    m = comps[f]["lab"] == comp + 1
    mw = np.pad(m, 2, mode="wrap"); m2 = ndi.binary_dilation(mw, iterations=2)[2:-2, 2:-2]
    tot = np.array([R[i, 2 + k][m2].astype(np.float64).sum() for k in range(3)], float)
    if tot.sum() <= 0: return None
    return int(tot.argmax()), float(tot.max() / tot.sum())


TK = {}
for t in tracks:
    TK[t["id"]] = [(t["start"] + k,) + q for k in range(len(t["comp"])) if (q := kind_of(t["start"] + k, t["comp"][k]))]
def tkind(tid):
    ks = TK.get(tid, [])
    return int(np.bincount([x[1] for x in ks], minlength=3).argmax()) if ks else None
def last_kind(tid):
    ks = [x for x in TK.get(tid, []) if x[2] >= 0.6]
    return ks[-1][1] if ks else None

P(f"== {label}: {T} frames, {len(tracks)} tracks")
P("frame  bodies  k0 k1 k2 (pure>=0.6)  trait_mean(ladder value)  area-weighted")
traj = []
for f in rf:
    c = np.zeros(3); ca = np.zeros(3)
    for j in range(len(comps[f]["area"])):
        q = kind_of(f, j)
        if q and q[1] >= 0.6: c[q[0]] += 1; ca[q[0]] += comps[f]["area"][j]
    tm = float(c @ LAD / c.sum()) if c.sum() else np.nan; ta = float(ca @ LAD / ca.sum()) if ca.sum() else np.nan
    traj.append((f, int(len(comps[f]["area"])), *[int(x) for x in c], tm, ta))
for r in traj[::6] + [traj[-1]]:
    P(f"{r[0]:5d} {r[1]:6d}   {r[2]:3d} {r[3]:3d} {r[4]:3d}   {r[5]:6.2f}   {r[6]:6.2f}")
# mutation events
muts = [json.loads(l) for l in open(mutf)] if mutf != "-" else []
nmut = sum(len(e["events"]) for e in muts if e["frame"] < T)
mut_from = np.zeros((3, 3), int)
mut_at = {}
for e in muts:
    f = e["frame"]
    if f >= T: continue
    lab, n = W._bodies(mat[f])
    for x in e["events"]:
        mut_from[x["from"], x["to"]] += 1
        cl = comps[f]["lab"][lab == x["body"]]; cl = cl[cl > 0]
        if len(cl): mut_at.setdefault(f, set()).add(int(np.bincount(cl).argmax()) - 1)
P(f"mutation events {nmut}; from->to counts {mut_from.tolist()}")
chg = expl = 0
for t in tracks:
    ks = [x for x in TK[t["id"]] if x[2] >= 0.6]
    for (f0, k0, _), (f1, k1, _) in zip(ks, ks[1:]):
        if k1 != k0:
            chg += 1
            expl += any(t["start"] <= g <= t["end"] and t["comp"][g - t["start"]] in mut_at.get(g, set()) for g in range(f0 + 1, f1 + 1))
P(f"kind changes along tracks: {chg}; at a logged mutation: {expl}; unexplained (conversions): {chg - expl}")
met = json.load(open(metf))
births = np.zeros(3, int); off = nd = 0
for e in met.get("persistent_splits", []):
    p = byid.get(e["parent"]); pk = last_kind(e["parent"]) if p else None
    if pk is None: continue
    births[pk] += 1
    for c in e["children"]:
        ct = byid.get(c)
        ks = [x for x in TK.get(c, []) if ct and x[0] >= ct["start"] + 5 and x[2] >= 0.6]
        if ks: nd += 1; off += ks[0][1] != pk
P(f"persistent splits by parent kind k0/k1/k2: {births.tolist()}; daughters checked {nd}, off-kind {off}")
mk = np.zeros(3, int); mx = 0
for t in tracks:
    if t["birth"] == "merge" and TK[t["id"]]:
        mk[TK[t["id"]][0][1]] += 1
        mx += len(set(last_kind(p) for p in t["parents"] if last_kind(p) is not None)) > 1
P(f"merge products by kind: {mk.tolist()}; merges of two different kinds: {mx}")
# deaths by kind: tracks that vanish (no children) before the run end
dk = np.zeros(3, int)
for t in tracks:
    if not t["children"] and t["end"] < T - 1 and last_kind(t["id"]) is not None: dk[last_kind(t["id"])] += 1
P(f"vanishings (no children, before run end) by last kind: {dk.tolist()}")


# rear-tip translation test (mtips.py) for every dividing track
def rear_ok(t):
    n = len(t["cy"])
    sy = M._wrap(np.diff(t["cy"]), H); sx = M._wrap(np.diff(t["cx"]), Wd)
    cy = np.concatenate([[0], np.cumsum(sy)]); cx = np.concatenate([[0], np.cumsum(sx)])
    net = np.hypot(cy[-1], cx[-1]); u = np.array([cy[-1], cx[-1]]) / max(net, 1e-9)
    rear = []
    for k in (0, n - 1):
        m = comps[t["start"] + k]["lab"] == t["comp"][k] + 1
        ys, xs = np.nonzero(m)
        p = (cy[k] + M._wrap(ys - t["cy"][k], H)) * u[0] + (cx[k] + M._wrap(xs - t["cx"][k], Wd)) * u[1]
        rear.append(p.min())
    return float((rear[1] - rear[0]) / max(net, 1e-9))


rows = json.load(open(tabf))["rows"]
dv = [r for r in rows if r["dividing"]]
FT = W.META["steps_per_frame"] * W.P["dt"]
mc = float(np.median([r["cycle"] for r in dv])) / FT if dv else 40.0
def alive_desc(tid, f):
    o, st, seen = [], [tid], set()
    while st:
        x = st.pop()
        if x in seen: continue
        seen.add(x); t = byid[x]
        if t["start"] <= f <= t["end"]: o.append(x)
        elif t["end"] < f: st += t["children"]
    return o
D = []
for r in dv:
    k = tkind(r["id"])
    rr = rear_ok(byid[r["id"]])
    DA = r["net"] / np.sqrt(r["A_mean"])
    f2 = int(r["start"] + 2 * mc)
    desc = len(alive_desc(r["id"], f2)) if f2 < T else None
    D.append(dict(id=r["id"], start=r["start"], kind=k, D=r["disp_rl"], DA=DA, rear=rr, vpath=r["vpath"], cycle=r["cycle"],
                  pass_rl=bool(r["disp_rl"] >= 3 and rr >= 2 / 3), pass_A=bool(DA >= 3 and rr >= 2 / 3), desc2=desc))
P(f"dividing tracks {len(D)}; median cycle {mc:.1f} frames ({mc * FT:.0f} t)")
P("kind  n_div  medD  sh_pass(rl)  sh_pass(sqrtA)  v_path  cycle")
for k in range(3):
    g = [d for d in D if d["kind"] == k]
    if not g: P(f"k{k}  0"); continue
    P(f"k{k} {len(g):5d} {np.median([d['D'] for d in g]):5.2f}  {sum(d['pass_rl'] for d in g)}/{len(g)}  {sum(d['pass_A'] for d in g)}/{len(g)}  {np.median([d['vpath'] for d in g]):.3f} {np.median([d['cycle'] for d in g]):.0f}")
P("cohort(birth frames)  n_div  trait_mean_of_dividers  pass_rl  pass_sqrtA  k0/k1/k2")
w = max(int(round(mc)), 1)
for a in range(0, T, w):
    g = [d for d in D if a <= d["start"] < a + w and d["kind"] is not None]
    if not g: continue
    kc = np.bincount([d["kind"] for d in g], minlength=3)
    P(f"  {a:3d}-{a + w - 1:3d}  {len(g):4d}  {np.mean([LAD[d['kind']] for d in g]):6.2f}  {sum(d['pass_rl'] for d in g)}/{len(g)}  {sum(d['pass_A'] for d in g)}/{len(g)}  {kc.tolist()}")
P("descendants alive at birth + 2 median cycles, passers (rl) vs non-passers, by kind:")
for k in range(3):
    a = [d["desc2"] for d in D if d["kind"] == k and d["pass_rl"] and d["desc2"] is not None]
    b = [d["desc2"] for d in D if d["kind"] == k and not d["pass_rl"] and d["desc2"] is not None]
    P(f"  k{k}: passers n={len(a)} mean {np.mean(a) if a else float('nan'):.2f}; non-passers n={len(b)} mean {np.mean(b) if b else float('nan'):.2f}")
json.dump(dict(label=label, traj=traj, div=D, births=births.tolist(), muts=nmut, conv=chg - expl, mc=mc), open(f"{outdir}/{label}.json", "w"))
open(f"{outdir}/{label}.txt", "w").write("\n".join(out) + "\n")
