"""Merge-aware genealogy from ecotrack.py ledgers (RUBRIC L6: a daughter counts only if it stays
separate from its sibling and persists).

usage: python lineage.py S led/run1.json [led/run2.json ...]

For every fission event (>= 2 daughters each >= 25% of the parent's mass), follow each daughter's
descendants (continuations, fissions, fragments, merges) up to S time units later. The event is
SIBLING-SAFE when every pair of daughters has no common descendant within S (they never re-fuse)
and at least two daughter lineages are still present at t + S. Events later than T - S are censored.
Generations: founders, nucleations and fragments are 0; a daughter of a sibling-safe fission is
parent + 1, otherwise it keeps the parent's generation. A merge product takes 0 (strict) or the
largest parental generation (reticulate; confidence capped at medium by the rubric).
"""
import json
import sys
from collections import defaultdict

S = float(sys.argv[1])
rows = []
for f in sys.argv[2:]:
    d = json.load(open(f))
    T = d["T"]
    tr = {t[0]: dict(birth=t[1], end=t[2], born=t[3], endby=t[4], m0=t[5], parents=t[6]) for t in d["tracks"]}
    kids = defaultdict(list)
    for tid, x in tr.items():
        for p in x["parents"]:
            kids[p].append(tid)

    def desc(k, tmax):
        out, st = set(), [k]
        while st:
            u = st.pop()
            if u in out:
                continue
            out.add(u)
            st += [v for v in kids[u] if tr[v]["birth"] <= tmax]
        return out

    ev_of = {}  # daughter track -> event index
    safe = []
    events = d["events"]
    for i, (t, parent, ks, pm) in enumerate(events):
        if t > T - S:
            safe.append(None)
            continue
        D = [desc(k, t + S) for k in ks]
        alive = sum(1 for Dk in D if any(tr[u]["end"] >= t + S or (tr[u]["endby"] == "alive") for u in Dk))
        co = any(D[a] & D[b] for a in range(len(D)) for b in range(a + 1, len(D)))
        safe.append((not co) and alive >= 2)
        for k in ks:
            ev_of[k] = i
    gen_s, gen_r = {}, {}
    for tid in sorted(tr, key=lambda u: (tr[u]["birth"], u)):
        x = tr[tid]
        if x["born"] == "fission":
            p = x["parents"][0]
            inc = 1 if tid in ev_of and safe[ev_of[tid]] else 0
            gen_s[tid] = gen_s.get(p, 0) + inc
            gen_r[tid] = gen_r.get(p, 0) + inc
        elif x["born"] == "merge":
            gen_s[tid] = 0
            gen_r[tid] = max([gen_r.get(p, 0) for p in x["parents"]] + [0])
        else:
            gen_s[tid] = gen_r[tid] = 0
    nsafe = sum(1 for s in safe if s)
    nunc = sum(1 for s in safe if s is not None)
    merges = sum(1 for x in tr.values() if x["born"] == "merge")
    mature_deaths = sum(1 for x in tr.values() if x["endby"] in ("death", "eaten") and x["end"] - x["birth"] >= S)
    eaten = sum(1 for x in tr.values() if x["endby"] == "eaten" and x["end"] - x["birth"] >= S)
    ser = d["series"]
    late = [r for r in ser if r[0] >= 1000]
    mean = lambda c: round(sum(r[c] for r in late) / max(len(late), 1), 1)
    row = dict(run=f, fissions=len(events), uncensored=nunc, sibling_safe=nsafe, merges=merges,
               merge_per_fission=round(merges / max(len(events), 1), 2),
               maxgen_strict=max(gen_s.values() or [0]), maxgen_reticulate=max(gen_r.values() or [0]),
               mature_deaths=mature_deaths, mature_eaten=eaten, prey_bodies_t1000=mean(1), pred_bodies_t1000=mean(2),
               prey_mass_end=round(ser[-1][3]), pred_mass_end=round(ser[-1][4]))
    rows.append(row)
    print(json.dumps(row))
