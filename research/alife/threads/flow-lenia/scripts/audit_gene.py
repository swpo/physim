"""Level-of-selection audit of fl_forager_gene2 snapshots (record_gene.py output).

python threads/flow-lenia/scripts/audit_gene.py RUN.npz [RUN2.npz ...] --out evo3/audit.json

Bodies: periodic connected components of blur1(matter) > 0.15 (area >= 6) in every snapshot.
Links: a child at t+1 overlaps a parent at t. Main parent = largest overlap (in child matter).
Price split of the change in body-matter-weighted mean log g per interval (exact identity):
  between  = sum_i (W_i/sum W)(z_i - zbar)        growth, fission and death of bodies
  within   = sum_j (w_j/sum W)(z_j - z_p(j))      children with exactly one parent
  fusion   = same sum over children with >= 2 parents
  nucl     = children without a parent (relative to zbar)
Kinds: high if body mean log g > HIGH (0.2), else low. Ledger per kind: births (fission
children), deaths, inter-kind fusions (outcome kind), flips (1-to-1 kind change in an interval
with a mutation event inside the body), conversions (1-to-1 kind change without an event),
off-kind daughters (fission child of the other kind than its parent).
Origin of each final high body: walk back the main-parent chain to the first low->high link.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from scipy import ndimage

HIGH = 0.2


def plabel(m, thr=0.15):
    lab, n = ndimage.label(ndimage.gaussian_filter(m, 1, mode="wrap") > thr)
    if n == 0:
        return lab, 0
    par = np.arange(n + 1)

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for a, b in list(zip(lab[0], lab[-1])) + list(zip(lab[:, 0], lab[:, -1])):
        if a and b:
            ra, rb = find(a), find(b)
            if ra != rb:
                par[rb] = ra
    roots = np.array([find(k) for k in range(n + 1)])
    uniq, new = np.unique(roots, return_inverse=True)
    lab = new[lab]  # root 0 stays 0
    area = np.bincount(lab.ravel())
    small = np.nonzero(area < 6)[0]
    small = small[small > 0]
    if len(small):
        lab[np.isin(lab, small)] = 0
    u2, lab = np.unique(lab, return_inverse=True)
    return lab.reshape(m.shape), len(u2) - 1


def audit(path):
    d = np.load(path)
    M, Z, T = d["matter"].astype(np.float32), d["logg"].astype(np.float32), d["t"]
    meta = json.loads(Path(str(path).replace(".npz", ".json")).read_text())
    ev = meta["events"]
    ev_by_interval = {}
    for e in ev:
        k = int(np.searchsorted(T, e["t"], side="right")) - 1  # event happened during interval k -> k+1
        ev_by_interval.setdefault(k, []).append(e)
    labs, bodies = [], []
    for f in range(len(T)):
        lab, n = plabel(M[f])
        w = ndimage.sum(M[f], lab, range(1, n + 1)) if n else np.zeros(0)
        zw = ndimage.sum(M[f] * Z[f], lab, range(1, n + 1)) if n else np.zeros(0)
        labs.append(lab)
        bodies.append({"w": np.asarray(w), "z": np.asarray(zw) / np.maximum(w, 1e-12)})
    terms = {"between": [], "within": [], "fusion": [], "nucl": [], "total": []}
    led = {k: {"births": 0, "deaths": 0, "flips": 0, "conversions": 0, "offkind_daughters": 0,
               "fusions_interkind_won": 0} for k in ("low", "high")}
    fusions_interkind = 0
    main_parent = []  # per interval: array child -> main parent (or -1)
    link_type = []    # per interval: child -> 'fission'|'single'|'fusion'|'nucl'
    gen = [np.zeros(len(bodies[0]["w"]), int)]
    kind = lambda z: "high" if z > HIGH else "low"
    for f in range(len(T) - 1):
        a, b = labs[f], labs[f + 1]
        na, nb = len(bodies[f]["w"]), len(bodies[f + 1]["w"])
        mk = (a > 0) & (b > 0)
        ov = np.zeros((na + 1, nb + 1))
        np.add.at(ov, (a[mk], b[mk]), M[f + 1][mk])
        ov = ov[1:, 1:]
        wb, zb = bodies[f + 1]["w"], bodies[f + 1]["z"]
        wa, za = bodies[f]["w"], bodies[f]["z"]
        mp = np.full(nb, -1)
        npar = np.zeros(nb, int)
        if na and nb:
            sig = ov > 0.02 * np.maximum(wb[None, :], 1e-9)
            npar = sig.sum(0)
            mp = np.where(npar > 0, ov.argmax(0), -1)
        nch = np.bincount(mp[mp >= 0], minlength=na) if na else np.zeros(0, int)
        SW = wb.sum()
        zbar = (wa * za).sum() / max(wa.sum(), 1e-12) if na else 0.0
        zbar1 = (wb * zb).sum() / max(SW, 1e-12) if nb else zbar
        Wi = np.bincount(mp[mp >= 0], weights=wb[mp >= 0], minlength=na) if na else np.zeros(0)
        between = (Wi / max(SW, 1e-12) * (za - zbar)).sum() if na else 0.0
        has = mp >= 0
        within = (wb[has & (npar == 1)] / SW * (zb[has & (npar == 1)] - za[mp[has & (npar == 1)]])).sum() if SW else 0.0
        fusion = (wb[has & (npar >= 2)] / SW * (zb[has & (npar >= 2)] - za[mp[has & (npar >= 2)]])).sum() if SW else 0.0
        nucl = (wb[~has] / SW * (zb[~has] - zbar)).sum() if SW else 0.0
        for k, v in zip(("between", "within", "fusion", "nucl", "total"), (between, within, fusion, nucl, zbar1 - zbar)):
            terms[k].append(float(v))
        # ledger
        evs = ev_by_interval.get(f, [])
        lt = np.array(["nucl"] * nb, dtype=object)
        g1 = np.zeros(nb, int)
        for j in range(nb):
            if mp[j] < 0:
                continue
            p = mp[j]
            if npar[j] >= 2:
                lt[j] = "fusion"
                pars = np.nonzero(ov[:, j] > 0.02 * wb[j])[0]
                ks = {kind(za[q]) for q in pars}
                if len(ks) > 1:
                    fusions_interkind += 1
                    led[kind(zb[j])]["fusions_interkind_won"] += 1
                g1[j] = gen[f][p]
            elif nch[p] >= 2:
                lt[j] = "fission"
                led[kind(zb[j])]["births"] += 1
                if kind(zb[j]) != kind(za[p]):
                    led[kind(zb[j])]["offkind_daughters"] += 1
                g1[j] = gen[f][p] + 1
            else:
                lt[j] = "single"
                g1[j] = gen[f][p]
                if kind(zb[j]) != kind(za[p]):
                    inside = any(b[e["y"], e["x"]] == j + 1 or a[e["y"], e["x"]] == p + 1 for e in evs)
                    led[kind(zb[j])]["flips" if inside else "conversions"] += 1
        for i in range(na):
            if nch[i] == 0 and not (ov[i] > 0).any():
                led[kind(za[i])]["deaths"] += 1
        main_parent.append(mp)
        link_type.append(lt)
        gen.append(g1)
    # persistence: how many following intervals each body continues 1-to-1 (no split, no merge)
    nF = len(T)
    run = [np.zeros(len(bodies[f]["w"]), int) for f in range(nF)]
    for f in range(nF - 2, -1, -1):
        mp, lt = main_parent[f], link_type[f]
        nch = np.bincount(mp[mp >= 0], minlength=len(bodies[f]["w"]))
        for j in range(len(mp)):
            p = mp[j]
            if p >= 0 and lt[j] == "single" and nch[p] == 1:
                run[f][p] = run[f + 1][j] + 1
    PERS = 10
    pgen = [np.zeros(len(bodies[0]["w"]), int)]
    pbirths = {"low": 0, "high": 0}
    pfusions = 0
    for f in range(nF - 1):
        mp, lt = main_parent[f], link_type[f]
        g1 = np.zeros(len(mp), int)
        kids = {}
        for j, p in enumerate(mp):
            if p >= 0:
                kids.setdefault(p, []).append(j)
        for p, js in kids.items():
            persistent = len(js) >= 2 and sum(run[f + 1][j] >= PERS for j in js) >= 2
            for j in js:
                g1[j] = pgen[f][p] + (1 if persistent and run[f + 1][j] >= PERS else 0)
                if persistent and run[f + 1][j] >= PERS:
                    pbirths[kind(bodies[f + 1]["z"][j])] += 1
        for j in range(len(mp)):
            if lt[j] == "fusion" and run[f + 1][j] >= PERS:
                pfusions += 1
        pgen.append(g1)
    # origin of final high bodies
    origins = {"born_high_from_low (offkind daughter)": 0, "flip (mutation inside body)": 0,
               "takeover after a patch (event in lineage <= 50 intervals before)": 0, "conversion (no event)": 0,
               "fusion": 0, "nucleated": 0}

    def hit_before(f, jj, K=50):
        """Was any mutation event inside this lineage's main-parent chain in the K intervals before f?"""
        for _ in range(K):
            if f <= 0:
                return False
            if any(labs[f][e["y"], e["x"]] == jj + 1 for e in ev_by_interval.get(f - 1, [])):
                return True
            p = main_parent[f - 1][jj]
            if p < 0:
                return False
            f, jj = f - 1, p
        return False
    fl = len(T) - 1
    for j in range(len(bodies[fl]["w"])):
        if kind(bodies[fl]["z"][j]) != "high":
            continue
        f, jj, tag = fl, j, "nucleated"
        while f > 0:
            p = main_parent[f - 1][jj]
            if p < 0:
                tag = "nucleated"
                break
            if kind(bodies[f - 1]["z"][p]) == "low":
                t = link_type[f - 1][jj]
                if t == "fission":
                    tag = "born_high_from_low (offkind daughter)"
                elif t == "fusion":
                    tag = "fusion"
                else:
                    evs = ev_by_interval.get(f - 1, [])
                    if any(labs[f][e["y"], e["x"]] == jj + 1 or labs[f - 1][e["y"], e["x"]] == p + 1 for e in evs):
                        tag = "flip (mutation inside body)"
                    elif hit_before(f - 1, p):
                        tag = "takeover after a patch (event in lineage <= 50 intervals before)"
                    else:
                        tag = "conversion (no event)"
                break
            f, jj = f - 1, p
        origins[tag] += 1
    cum = {k: float(np.sum(v)) for k, v in terms.items()}
    nb_final = len(bodies[fl]["w"])
    return {"run": Path(path).stem, "cum": cum, "ledger": led, "fusions_interkind": fusions_interkind,
            "origins_final_high": origins, "final_bodies": nb_final,
            "final_high": int(sum(kind(z) == "high" for z in bodies[fl]["z"])),
            "max_gen_final": int(gen[fl].max()) if nb_final else 0,
            "max_persistent_gen_final": int(pgen[fl].max()) if nb_final else 0,
            "persistent_births": pbirths, "persistent_fusions": pfusions, "events": len(ev),
            "mean_body_frac_hit": float(np.mean([e["body_frac"] for e in ev])) if ev else 0.0,
            "series": {k: np.cumsum(v).round(4).tolist() for k, v in terms.items()}, "t": T[1:].tolist()}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+"); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    res = [audit(p) for p in a.runs]
    Path(a.out).write_text(json.dumps(res))
    for r in res:
        c = r["cum"]
        print(f"{r['run']}: total {c['total']:+.3f} = between {c['between']:+.3f} within {c['within']:+.3f} "
              f"fusion {c['fusion']:+.3f} nucl {c['nucl']:+.3f} | bodies {r['final_bodies']} high {r['final_high']} "
              f"maxgen {r['max_gen_final']} pgen {r['max_persistent_gen_final']} pbirths {r['persistent_births']} pfus {r['persistent_fusions']} | high births {r['ledger']['high']['births']} offkind {r['ledger']['high']['offkind_daughters']} "
              f"flips {r['ledger']['high']['flips']} conv {r['ledger']['high']['conversions']} deaths(low/high) "
              f"{r['ledger']['low']['deaths']}/{r['ledger']['high']['deaths']} | origins {r['origins_final_high']}")
